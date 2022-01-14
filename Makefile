.PHONY: all clean tar

NAME=bartender
VERSION=0.1.0
ARCH=armhf

prefix = /usr

PKG=${NAME}-${VERSION}-${ARCH}
PKG_TAR=build/${PKG}.tar.gz
USR_DIR=$(prefix)/share/bartender
INSTALL_DIR=${PKG}${USR_DIR}

# Systemd variables
SYSTEMD_DIR=${PKG}/lib/systemd/system
SYSTEMD_TEMPLATE_FILES := $(wildcard systemd/*.template)
SYSTEMD_TARGET_FILES := \
	$(patsubst \
		%.template, \
		%.service, \
		${SYSTEMD_TEMPLATE_FILES})

all: opendrinks backend venv frontend/build companion ${SYSTEMD_TARGET_FILES}

venv: requirements.txt
	python3 -m venv venv
	VIRTUAL_ENV=$(shell pwd)/venv \
	  PATH=$(shell pwd)/venv/bin:$(PATH) \
	  pip3 install -r requirements.txt

frontend/build: frontend
	cd frontend && \
	npm install && \
	npm run build

systemd/%.service: systemd/%.template
	sed \
		-e 's%<BARTENDER_DIR>%${USR_DIR}%g' \
		$< > $@

${PKG_TAR}: all
	-rm ${PKG_TAR}
	-rm -rf ${PKG}
	install -d ${INSTALL_DIR}
	cp -r opendrinks ${INSTALL_DIR}/
	cp -r backend ${INSTALL_DIR}/
	cp -r frontend/build ${INSTALL_DIR}/
	mv ${INSTALL_DIR}/build ${INSTALL_DIR}/frontend
	cp -r companion ${INSTALL_DIR}/

	mkdir -p ${SYSTEMD_DIR}
	cp systemd/*.service ${SYSTEMD_DIR}
	$(foreach service,$(SYSTEMD_TARGET_FILES),systemctl enable $(notdir $(service)) --root=$(PKG);)

	install -d ${PKG}/DEBIAN
	cp debian/control ${PKG}/DEBIAN
	cp systemd/*.service ${PKG}/DEBIAN/

	install -d build
	tar -czvf $@ ${PKG}

tar: ${PKG_TAR}

clean:
	-rm -rf ${PKG_TAR}
	-rm -rf ${PKG}
	-rm -rf venv
	-rm -rf frontend/build
	-rm systemd/*.service

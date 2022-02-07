.PHONY: all clean install tar deb

NAME=bartender
VERSION=0.1.0
ARCH=armhf

prefix = /usr

PKG=${NAME}-${VERSION}-${ARCH}
PKG_TAR=build/${PKG}.tar.gz
PKG_DEB=build/${PKG}.deb
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

install: all
	-rm ${PKG_TAR}
	-rm -rf ${PKG}
	install -d ${INSTALL_DIR}
	cp -r linux/* ${PKG}/
	cp -r opendrinks ${INSTALL_DIR}/
	cp -r backend ${INSTALL_DIR}/
	ln -sf ${USR_DIR}/opendrinks ${INSTALL_DIR}/backend/opendrinks
	cp -r frontend/build ${INSTALL_DIR}/
	mv ${INSTALL_DIR}/build ${INSTALL_DIR}/frontend
	ln -sf ${USR_DIR}/opendrinks/images ${INSTALL_DIR}/frontend/images/drinks/images
	cp -r venv ${INSTALL_DIR}/

	mkdir -p ${SYSTEMD_DIR}
	cp systemd/*.service ${SYSTEMD_DIR}
	$(foreach service,$(SYSTEMD_TARGET_FILES),systemctl enable $(notdir $(service)) --root=$(PKG);)

	find ${INSTALL_DIR} -name ".*" -prune -exec rm -rf {} \;

	install -d ${PKG}/DEBIAN
	cp debian/control ${PKG}/DEBIAN
	cp debian/postinst ${PKG}/DEBIAN
	cp debian/postrm ${PKG}/DEBIAN
	cp systemd/*.service ${PKG}/DEBIAN/

${PKG_TAR}: install
	install -d build
	tar -czvf $@ ${PKG}

tar: ${PKG_TAR}

${PKG_DEB}: install
	install -d build
	dpkg-deb -b ${PKG} ${PKG_DEB}

deb: ${PKG_DEB}

clean:
	-rm -rf ${PKG_TAR}
	-rm -rf ${PKG}
	-rm -rf venv
	-rm -rf frontend/build
	-rm systemd/*.service

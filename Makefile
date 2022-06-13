.PHONY: all clean install tar deb cachesetup deb_signed

SHELL := /bin/bash

NAME=bartender
VERSION=0.1.3

ifeq ($(shell uname -m),armv7l)
	ARCH=armhf
else ifeq ($(shell uname -m),aarch64)
	ARCH=arm64
endif

CORES=$(shell nproc)

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

all: opendrinks backend venv frontend/build ${SYSTEMD_TARGET_FILES}

cachesetup:
	mkdir -p .cache
	npm config set cache .cache/npm --global
	pip config set global.cache-dir .cache/pip

venv: requirements.txt
	python3 -m venv venv --upgrade-deps
	VIRTUAL_ENV=$(shell pwd)/venv \
		PATH=$(shell pwd)/venv/bin:$(PATH) \
		pip install -I wheel
	VIRTUAL_ENV=$(shell pwd)/venv \
	  PATH=$(shell pwd)/venv/bin:$(PATH) \
		pip3 install -I -r requirements.txt

	# Don't add this flag until after the install is complete, otherwise attempts
	# to use system installed version of setuptools.
	sed -i "s/include-system-site-packages = false/include-system-site-packages = true/" venv/pyvenv.cfg

frontend/node_modules: frontend
	cd frontend && \
	npm -d install

frontend/build: frontend/node_modules
	cd frontend && \
	npm -d run build

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
	chmod a+w ${INSTALL_DIR}/backend/database_server
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
	sed \
		-e 's%<ARCH>%${ARCH}%g' \
		-e 's%<VERSION>%${VERSION}%g' \
		debian/control > ${PKG}/DEBIAN/control
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

deb_signed: deb
	echo ${GPG_SIGNING_KEY} | base64 --decode | gpg --import
	dpkg-sig -s builder ${PKG_DEB}
	dpkg-sig -c ${PKG_DEB}

clean:
	-rm -rf ${PKG_TAR}
	-rm -rf ${PKG}
	-rm -rf venv
	-rm -rf frontend/build
	-rm -rf frontend/node_modules
	-rm systemd/*.service
	-rm -rf .cache
	-rm -rf build

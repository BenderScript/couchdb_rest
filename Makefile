PACKAGE_TAG = couchdb_rest
PACKAGE_NAME =$(PACKAGE_TAG)_api
wheel_version := $(shell python3 -c 'import __init__ as version; print(version.__version__)')
WHEEL := $(PACKAGE_NAME)-$(wheel_version)-py3-none-any.whl

COVERAGE=coverage run -m

PYTHON=python3
MAKE=make
PYTEST=pytest
OS := $(shell uname)
PIP := pip3
export DB_TYPE=COUCHDB

MAGEN_HELPER=./lib/magen_helper

include $(MAGEN_HELPER)/make_common/docker_common.mk
include $(MAGEN_HELPER)/make_common/package_common.mk
include $(MAGEN_HELPER)/make_common/doc_common.mk


init:
	@git submodule update --init --recursive

default: common_default

clean: common_clean

test: common_test

package: common_package

install: common_install

uninstall: common_uninstall

all: common_all

list: common_list

update: common_update

test_travis: common_test_travis

upload: common_upload

run_unit_test: common_run_unit_test

pre_test: common_pre_test

coverage_report: common_coverage_report

.PHONY:  pre_test coverage_report all build_docker

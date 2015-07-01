THIS_MAKEFILE_PATH := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
SCRIPT_DIR := $(shell cd $(dir $(THIS_MAKEFILE_PATH));pwd)

setup:
	${SCRIPT_DIR}/scripts/setup_project.sh

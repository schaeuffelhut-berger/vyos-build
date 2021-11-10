SHELL := /bin/bash

build_dir := build

.PHONY: all
all:
	@echo "Make what specifically?"
	@echo "The most common target is 'iso'"

.PHONY: check_build_config
check_build_config:
	@scripts/check-config


.PHONY: iso
.ONESHELL:
iso: check_build_config clean
	@echo "It's not like I'm building this specially for you or anything!"
	cd $(build_dir)
	set -o pipefail
	lb build 2>&1 | tee build.log; if [ $$? -ne 0 ]; then exit 1; fi
	cd ..
	@scripts/copy-image
	exit 0

.PHONY: prepare-package-env
.ONESHELL:
prepare-package-env:
	@set -e
	@scripts/pbuilder-config
	@scripts/pbuilder-setup

.PHONY: test
.ONESHELL:
test:
	if [ ! -f build/live-image-amd64.hybrid.iso ]; then
		echo "Could not find build/live-image-amd64.hybrid.iso"
		exit 1
	fi
	scripts/check-qemu-install --debug --uefi build/live-image-amd64.hybrid.iso

.PHONY: test-no-interfaces
.ONESHELL:
test-no-interfaces:
	if [ ! -f build/live-image-amd64.hybrid.iso ]; then
		echo "Could not find build/live-image-amd64.hybrid.iso"
		exit 1
	fi
	scripts/check-qemu-install --debug --no-interfaces build/live-image-amd64.hybrid.iso

.PHONY: testd
.ONESHELL:
testd:
	if [ ! -f build/live-image-amd64.hybrid.iso ]; then
		echo "Could not find build/live-image-amd64.hybrid.iso"
		exit 1
	fi
	scripts/check-qemu-install --debug --configd build/live-image-amd64.hybrid.iso

.PHONY: testc
.ONESHELL:
testc:
	if [ ! -f build/live-image-amd64.hybrid.iso ]; then
		echo "Could not find build/live-image-amd64.hybrid.iso"
		exit 1
	fi
	scripts/check-qemu-install --debug --configd --configtest build/live-image-amd64.hybrid.iso

.PHONY: clean
.ONESHELL:
clean:
	@set -e
	cd $(build_dir)
	lb clean

	rm -f config/binary config/bootstrap config/chroot config/common config/source
	rm -f build.log
	rm -f vyos-*.iso
	rm -f *.img
	rm -f *.xz
	rm -f *.vhd
	rm -f *.raw
	rm -f *.tar.gz
	rm -f *.qcow2
	rm -f *.mf
	rm -f *.ovf
	rm -f *.ova

.PHONY: purge
purge:
	rm -rf build packer_build packer_cache testinstall-*.img

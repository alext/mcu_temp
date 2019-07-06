
.PHONY: deploy
deploy:
	./scripts/deploy.sh

vendor/esp8266-%.bin:
	curl -L https://www.micropython.org/resources/firmware/esp8266-$*.bin \
		-o $@

.PHONY: flash_device
flash_device: vendor/esp8266-20190529-v1.11.bin
	esptool.py --port $${PORT} --baud 921600 write_flash 0 $<

.PHONY: flash_device
verify_device: vendor/esp8266-20190529-v1.11.bin
	esptool.py --port $${PORT} --baud 921600 verify_flash 0 $<

.PHONY: erase_Device
erase_device:
	esptool.py --port $${PORT} erase_flash

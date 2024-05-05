OBJS = start.o stage2.o

CC = gcc
OBJCOPY = objcopy
CFLAGS = -DSMP -isystem pppwn/freebsd-headers/include -Wl,--build-id=none -Os -fno-stack-protector
LDFLAGS = -T linker.ld -nostartfiles -nostdlib

ifneq ($(filter $(FW), 850 900 903 904 950 960 1000 1001 1050 1070 1071 1100),)
CFLAGS += -DFIRMWARE=$(FW)
else
$(error "Invalid firmware")
endif

TARGET = stage2_$(FW)

all: $(TARGET).bin

%.bin: %.elf
	$(OBJCOPY) -S -O binary $^ $@

$(TARGET).elf: $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	@rm -f $(TARGET).bin $(TARGET).elf $(OBJS)

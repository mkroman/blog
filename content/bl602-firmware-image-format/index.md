+++
title = "Documenting the BouffaloLab BL602 firmware image format"
date = 2020-11-21

[taxonomies]
tags = ["bl602", "firmware", "risc-v", "documentation"]
categories = ["electronics", "firmware"]
+++

The BL602 is a new WiFi and Bluetooth 5 capable SoC from [Bouffalo Lab][1] based
on [SiFive's E24 core][2] which is a 32-bit
RISC-V processor with the IMAFC extension set.

I've challenged myself to write my [own RISC-V OS][mikroos] from scratch in
Rust - and one of the first things I require is a tool to convert an elf file to the
specific firmware image format that is read by the programming tool.

Since I couldn't find a resource that described the format, I went through the
source files and wrote this article in the hopes of making it easier to
understand.

<!-- more -->

I've made some tables describing the different structures and their fields,
with some comments from the source, and some from myself.

## Firmware image

The file starts with a a [boot header](#boot-header) which contains structures
that describe different boot parameters, clock parameters and flash parameters.

Immediately following the boot header is the [image data](#image-data), which
also includes an address that the image should be written to.


### Boot header (aka `Boot_Header_Config`) {#boot-header}

| Offset | Size (bytes) | Field                     | Purpose   |
|--------|--------------|---------------------------|------------------------------------------------------------------------------------------|
| 0x00   | 0x04         | magic                     | Magic number - can be either 'BFNP' or 'BFAP' for CPU1 or CPU2 firmware, respectively    |
| 0x04   | 0x04         | rivision<sup>[sic]</sup>  | Boot header revision number?                                                             |
| 0x08   | 0x5C         | [flashCfg](#flash-config) | Structure containing necessary information on how to communicate with the external flash |
| 0x64   | 0x10         | [clkCfg](#clock-config)   | Structure containing clock information                                                   |
| 0x74   | 0x04         | bootCfg                   | Boot config flags                                                                        |
| 0x78   | 0x04         | imgSegmentInfo            | segmentCnt or imgLen                                                                     |
| 0x7c   | 0x04         | bootEntry                 | Entry point of the image                                                                 |
| 0x80   | 0x04         | imgStart                  | ramAddr or flashOffset[^1]                                                               |
| 0x84   | 0x20         | hash                      | SHA-256 hash of the whole image                                                          |
| 0xa4   | 0x04         | rsv1                      ||
| 0xa8   | 0x04         | rsv2                      ||
| 0xac   | 0x04         | crc32                     ||

### Clock config (aka `Boot_Clk_Config` and `Boot_Sys_Clk_Config`) {#clock-config}

| Offset | Size (bytes) | Field         | Purpose |
|--------|--------------|--------------|---------|
| 0x00   | 0x04         | magic        | Magic number - always 'PCFG' |
| 0x04   | 0x01         | xtalType     |                                                   |
| 0x05   | 0x01         | pllClk       |                                                   |
| 0x06   | 0x01         | hclkDiv      |                                                   |
| 0x07   | 0x01         | bclkDiv      |                                                   |
| 0x08   | 0x01         | flashClkType |                                                   |
| 0x09   | 0x01         | flashClkDiv  |                                                   |
| 0x0a   | 0x02         | rsvd\[2\]    |                                                   |
| 0x0c   | 0x04         | crc32        | CRC32 checksum of the cfg struct |

### Flash config (aka `Boot_Flash_Config` and `SPI_Flash_Cfg_Type`) {#flash-config}

| Offset | Size (bytes) | Field                | Purpose                                           |
|--------|--------------|----------------------|---------------------------------------------------|
| 0x00   | 0x04         | magic                | Magic number - always 'FCFG'                      |
| 0x04   | 0x01         | ioMode               | Serail flash interface mode                       |
| 0x05   | 0x01         | cReadSupport         | Support continuous read mode                      |
| 0x06   | 0x01         | clkDelay             | SPI clock delay                                   |
| 0x07   | 0x01         | clkInvert            | SPI clock phase invert                            |
| 0x08   | 0x01         | resetEnCmd           | Flash enable reset command                        |
| 0x09   | 0x01         | resetCmd             | Flash reset command                               |
| 0x0a   | 0x01         | resetCreadCmd        | Flash reset continuous read command               |
| 0x0b   | 0x01         | resetCreadCmdSize    | Flash reset continuous read command size          |
| 0x0c   | 0x01         | jedecIdCmd           | JEDEC ID command                                  |
| 0x0d   | 0x01         | jedecIdCmdDmyClk     | JEDEC ID command dummy clock                      |
| 0x0e   | 0x01         | qpiJedecIdCmd        | QPI JEDEC ID comamnd                              |
| 0x0f   | 0x01         | qpiJedecIdCmdDmyClk  | QPI JEDEC ID command dummy clock                  |
| 0x10   | 0x01         | sectorSize           | *1024bytes                                        |
| 0x11   | 0x01         | mid                  | Manufacturer ID                                   |
| 0x12   | 0x02         | pageSize             | Page size                                         |
| 0x14   | 0x01         | chipEraseCmd         | Chip erase cmd                                    |
| 0x15   | 0x01         | sectorEraseCmd       | Sector erase command                              |
| 0x16   | 0x01         | blk32EraseCmd        | Block 32K erase command                           |
| 0x17   | 0x01         | blk64EraseCmd        | Block 64K erase command                           |
| 0x18   | 0x01         | writeEnableCmd       | Need before every erase or program                |
| 0x19   | 0x01         | pageProgramCmd       | Page program cmd                                  |
| 0x1a   | 0x01         | qpageProgramCmd      | QIO page program cmd                              |
| 0x1b   | 0x01         | qppAddrMode          | QIO page program address mode                     |
| 0x1c   | 0x01         | fastReadCmd          | Fast read command                                 |
| 0x1d   | 0x01         | frDmyClk             | Fast read command dummy clock                     |
| 0x1e   | 0x01         | qpiFastReadCmd       | QPI fast read command                             |
| 0x1f   | 0x01         | qpiFrDmyClk          | QPI fast read command dummy clock                 |
| 0x20   | 0x01         | fastReadDoCmd        | Fast read dual output command                     |
| 0x21   | 0x01         | frDoDmyClk           | Fast read dual output command dummy clock         |
| 0x22   | 0x01         | fastReadDioCmd       | Fast read dual io comamnd                         |
| 0x23   | 0x01         | frDioDmyClk          | Fast read dual io command dummy clock             |
| 0x24   | 0x01         | fastReadQoCmd        | Fast read quad output comamnd                     |
| 0x25   | 0x01         | frQoDmyClk           | Fast read quad output comamnd dummy clock         |
| 0x26   | 0x01         | fastReadQioCmd       | Fast read quad io comamnd                         |
| 0x27   | 0x01         | frQioDmyClk          | Fast read quad io comamnd dummy clock             |
| 0x28   | 0x01         | qpiFastReadQioCmd    | QPI fast read quad io comamnd                     |
| 0x29   | 0x01         | qpiFrQioDmyClk       | QPI fast read QIO dummy clock                     |
| 0x2a   | 0x01         | qpiPageProgramCmd    | QPI program command                               |
| 0x2b   | 0x01         | writeVregEnableCmd   | Enable write reg                                  |
| 0x2c   | 0x01         | wrEnableIndex        | Write enable register index                       |
| 0x2d   | 0x01         | qeIndex              | Quad mode enable register index                   |
| 0x2e   | 0x01         | busyIndex            | Busy status register index                        |
| 0x2f   | 0x01         | wrEnableBit          | Write enable bit pos                              |
| 0x30   | 0x01         | qeBit                | Quad enable bit pos                               |
| 0x31   | 0x01         | busyBit              | Busy status bit pos                               |
| 0x32   | 0x01         | wrEnableWriteRegLen  | Register length of write enable                   |
| 0x33   | 0x01         | wrEnableReadRegLen   | Register length of write enable status            |
| 0x34   | 0x01         | qeWriteRegLen        | Register length of contain quad enable            |
| 0x35   | 0x01         | qeReadRegLen         | Register length of contain quad enable status     |
| 0x36   | 0x01         | releasePowerDown     | Release power down command                        |
| 0x37   | 0x01         | busyReadRegLen       | Register length of contain busy status            |
| 0x38   | 0x04         | readRegCmd\[4\]      | Read register command buffer                      |
| 0x3c   | 0x04         | writeRegCmd\[4\]     | Write register command buffer                     |
| 0x40   | 0x01         | enterQpi             | Enter qpi command                                 |
| 0x41   | 0x01         | exitQpi              | Exit qpi command                                  |
| 0x42   | 0x01         | cReadMode            | Config data for continuous read mode              |
| 0x43   | 0x01         | cRExit               | Config data for exit continuous read mode         |
| 0x44   | 0x01         | burstWrapCmd         | Enable burst wrap command                         |
| 0x45   | 0x01         | burstWrapCmdDmyClk   | Enable burst wrap command dummy clock             |
| 0x46   | 0x01         | burstWrapDataMode    | Data and address mode for this command            |
| 0x47   | 0x01         | burstWrapData        | Data to enable burst wrap                         |
| 0x48   | 0x01         | deBurstWrapCmd       | Disable burst wrap command                        |
| 0x49   | 0x01         | deBurstWrapCmdDmyClk | Disable burst wrap command dummy clock            |
| 0x4a   | 0x01         | deBurstWrapDataMode  | Data and address mode for this command            |
| 0x4b   | 0x01         | deBurstWrapData      | Data to disable burst wrap                        |
| 0x4c   | 0x02         | timeEsector          | 4K erase time                                     |
| 0x4e   | 0x02         | timeE32k             | 32K erase time                                    |
| 0x50   | 0x02         | timeE64k             | 64K erase time                                    |
| 0x52   | 0x02         | timePagePgm          | Page program time                                 |
| 0x54   | 0x02         | timeCe               | Chip erase time in ms                             |
| 0x56   | 0x01         | pdDelay              | Release power down command delay time for wake up |
| 0x57   | 0x01         | qeData               | QE set data                                       |
| 0x58   | 0x04         | crc32                | CRC32 checksum of the cfg struct                  |

Immediately after these headers follows the actual image to write:

### Image data {#image-data}

| Offset | Size (bytes)   | Field      | Purpose                                           |
|--------|----------------|------------|---------------------------------------------------|
| 0x00   | 0x04           | Address    | Where to write the image |
| 0x04   | 0x04           | Image size | The size of the following image |
| 0x08   | \<Image size\> | Image data | The image data to be written to `Address` |

Sources:
* [bl602_sflash.h](https://github.com/bouffalolab/bl_iot_sdk/blob/ee4a10b1a1e3609243bd5e7b3a45f02d768f6c14/components/bl602/bl602_std/bl602_std/StdDriver/Inc/bl602_sflash.h#L54-L130)
* [blsp_bootinfo.h](https://github.com/bouffalolab/bl_iot_sdk/blob/fef645af6c0cd170a53e57f2a1b568071eea73d6/customer_app/bl602_boot2/bl602_boot2/blsp_bootinfo.h)

[2]: https://www.sifive.com/cores/e24
[1]: https://www.bouffalolab.com/
[mikroos]: https://github.com/mkroman/mikroos

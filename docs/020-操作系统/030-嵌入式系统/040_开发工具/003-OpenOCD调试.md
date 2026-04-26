# OpenOCD调试

## 概述

OpenOCD（Open On-Chip Debugger）是一个开源的片上调试工具，通过JTAG或SWD接口调试和烧写嵌入式设备。

## OpenOCD特点

1. **多调试器支持**：J-Link、ST-Link、FTDI等
2. **多目标支持**：ARM、MIPS、RISC-V等
3. **GDB服务**：作为GDB远程调试代理
4. **Telnet控制**：提供命令行控制接口
5. **烧写功能**：支持Flash编程

## 安装OpenOCD

### 从包管理器安装

```bash
# Ubuntu/Debian
sudo apt install openocd

# Fedora
sudo dnf install openocd

# macOS
brew install open-ocd
```

### 从源码编译

```bash
git clone https://github.com/openocd-org/openocd.git
cd openocd
./bootstrap
./configure --enable-jlink --enable-ftdi --enable-stlink
make
sudo make install
```

## 基本使用

### 启动OpenOCD

```bash
# 使用配置文件启动
openocd -f interface/jlink.cfg -f target/stm32f4x.cfg

# 常见调试器配置
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg    # ST-Link
openocd -f interface/ftdi/dp_busblazer.cfg -f target/...  # FTDI
```

### 连接目标

```bash
# OpenOCD启动后会监听两个端口：
# - GDB端口：3333
# - Telnet端口：4444

# 连接Telnet
telnet localhost 4444

# 连接GDB
gdb-multiarch
(gdb) target remote localhost:3333
```

## Telnet命令

### 基本命令

```bash
# 查看目标状态
> targets

# 复位目标
> reset
> reset halt       # 复位并停止
> reset run        # 复位并运行

# 停止/继续执行
> halt
> resume

# 读写内存
> mdw 0x20000000 10    # 读10个字
> mwb 0x20000000 0x55  # 写字节
> mwh 0x20000000 0x5555  # 写半字
> mww 0x20000000 0x55AA55AA  # 写字

# 读写寄存器
> reg                  # 列出所有寄存器
> reg r0               # 读取r0
> reg r0 0x12345678    # 写r0
> reg pc 0x08000100    # 写PC

# 断点操作
> bp 0x08000100 2 hw   # 设置硬件断点
> bp 0x08000100 2      # 设置软件断点
> rbp 0x08000100       # 删除断点
> bps                  # 列出断点

# 单步执行
> step                 # 单步进入
> step 10              # 单步10次
```

### Flash烧写

```bash
# 查看Flash信息
> flash banks

# 擦除Flash
> flash erase_sector 0 0 last    # 擦除所有扇区
> flash erase_sector 0 0 10      # 擦除扇区0-10

# 写入Flash
> flash write_image erase myfirmware.bin 0x08000000

# 验证Flash
> flash verify_bank 0 myfirmware.bin 0x08000000

# 快速烧写
> program myfirmware.bin verify reset 0x08000000
```

## GDB调试

### 连接OpenOCD

```bash
gdb-multiarch myprogram.elf
(gdb) target remote localhost:3333
(gdb) monitor reset halt
(gdb) load
(gdb) break main
(gdb) continue
```

### OpenOCD GDB扩展

```bash
(gdb) monitor reset halt      # 复位并停止
(gdb) monitor flash banks     # 查看Flash
(gdb) monitor meminfo         # 内存信息
(gdb) monitor reg             # 寄存器信息
```

## 配置文件

### 简单配置文件

```tcl
# myboard.cfg

# 选择调试器
source [find interface/jlink.cfg]

# 设置传输方式（JTAG或SWD）
transport select swd

# 设置时钟频率
adapter speed 4000

# 目标芯片配置
set CHIPNAME stm32f407
set ENDIAN little

# 配置DAP
swd newdap $_CHIPNAME cpu -irlen 4 -ircapture 0x1 -irmask 0xf -expected-id 0x2ba01477

# 创建目标
target create $_CHIPNAME.cpu cortex_m -endian $_ENDIAN -chain-position $_CHIPNAME.cpu

# 配置Flash
flash bank $_CHIPNAME.flash stm32f2x 0 0 0 0 $_CHIPNAME.cpu

# 复位配置
$_CHIPNAME.cpu configure -event reset-init {
    adapter speed 4000
}
```

### 自定义初始化脚本

```tcl
# init.cfg

init

# 复位目标并停止
reset halt

# 配置时钟等
mww 0x40023800 0x00000100   # RCC配置

# 恢复执行
resume
```

## 常见芯片配置

### STM32F4系列

```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg
```

### STM32H7系列

```bash
openocd -f interface/stlink.cfg -f target/stm32h7x.cfg
```

### ESP32

```bash
openocd -f interface/ftdi/esp32_devkitj_v1.cfg -f target/esp32.cfg
```

### 树莓派（RPi Pico）

```bash
openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg
```

## 烧写脚本示例

### 完整烧写流程

```tcl
# flash.cfg

source [find interface/stlink.cfg]
source [find target/stm32f4x.cfg]

init
reset halt

# 解锁Flash（如需要）
stm32f2x unlock 0

# 擦除并烧写
flash erase_sector 0 0 last
flash write_image myfirmware.bin 0x08000000
flash verify_bank 0 myfirmware.bin 0x08000000

# 复位运行
reset run

shutdown
```

```bash
openocd -f flash.cfg
```

## 调试技巧

### 查看调用栈

```bash
(gdb) backtrace
#0  0x08001234 in my_function () at main.c:100
#1  0x08001456 in main () at main.c:200
```

### 查看变量

```bash
(gdb) print my_variable
(gdb) print *my_pointer
(gdb) print/x my_variable    # 十六进制显示
```

### 内存查看

```bash
(gdb) x/10x 0x20000000       # 查看10个字，十六进制
(gdb) x/10i 0x08000100       # 查看10条指令
(gdb) x/10s 0x20000000       # 查看字符串
```

### 实时查看

```bash
# 持续刷新变量
(gdb) display my_variable
(gdb) display/x *0x20000000
```

## 常见问题

### 连接失败

```bash
Error: JTAG chain inspection failed
```

解决：
- 检查调试器连接
- 检查目标供电
- 降低时钟频率：`adapter speed 1000`
- 尝试SWD模式：`transport select swd`

### Flash烧写失败

```bash
Error: flash write failed
```

解决：
- 确保Flash已解锁
- 检查地址是否对齐
- 检查Flash大小是否足够

### 调试不稳定

解决：
- 降低调试时钟频率
- 检查电源稳定性
- 检查JTAG/SWD线路长度

## 参考资料

- [OpenOCD官网](http://openocd.org/)
- [OpenOCD文档](http://openocd.org/documentation/)
- [OpenOCD配置](http://openocd.org/documentation/userguide/configuration/)

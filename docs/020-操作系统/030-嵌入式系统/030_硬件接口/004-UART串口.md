# UART串口

## 概述

UART（Universal Asynchronous Receiver/Transmitter，通用异步收发传输器）是最常用的串行通信接口，用于设备间的数据传输。

## UART特点

1. **异步通信**：无需时钟线，依靠波特率同步
2. **两线制**：TX（发送）、RX（接收）
3. **全双工**：可同时收发
4. **简单可靠**：协议简单，应用广泛
5. **灵活配置**：可设置波特率、数据位、校验位、停止位

## UART帧格式

```
空闲(高电平)
    | START | D0 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | PARITY | STOP |
___|___|___|___|___|___|___|___|___|___|_______|_______|__________|

    起始位(1位) + 数据位(5-9位) + 校验位(0/1位) + 停止位(1-2位)
```

### 常用配置

- **波特率**：9600、19200、38400、57600、115200、230400等
- **数据位**：5、6、7、8位（常用8位）
- **校验位**：无校验、奇校验、偶校验
- **停止位**：1位、1.5位、2位

常用配置示例：`115200-8-N-1`（115200波特率，8数据位，无校验，1停止位）

## Linux串口编程

### 使用termios

```c
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

int serial_open(const char *device, int baud)
{
    int fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    
    struct termios options;
    tcgetattr(fd, &options);
    
    // 设置波特率
    cfsetispeed(&options, B115200);
    cfsetospeed(&options, B115200);
    
    // 8N1配置
    options.c_cflag &= ~PARENB;        // 无校验
    options.c_cflag &= ~CSTOPB;        // 1停止位
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;            // 8数据位
    
    options.c_cflag |= (CLOCAL | CREAD);
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    options.c_oflag &= ~OPOST;
    
    tcsetattr(fd, TCSANOW, &options);
    
    return fd;
}

// 发送数据
write(fd, "Hello", 5);

// 接收数据
char buf[256];
int len = read(fd, buf, sizeof(buf));

close(fd);
```

### 阻塞与非阻塞

```c
// 阻塞读取
fcntl(fd, F_SETFL, 0);

// 非阻塞读取
fcntl(fd, F_SETFL, FNDELAY);

// 设置超时
options.c_cc[VMIN] = 0;    // 最小字符数
options.c_cc[VTIME] = 10; // 超时（0.1秒为单位）
```

### 串口工具

```bash
# minicom
minicom -s                     # 配置
minicom -D /dev/ttyUSB0        # 连接

# screen
screen /dev/ttyUSB0 115200

# picocom
picocom -b 115200 /dev/ttyUSB0

# stty设置参数
stty -F /dev/ttyUSB0 115200 cs8 -cstopb -parenb
```

## STM32 UART编程

### HAL库方式

```c
#include "stm32f4xx_hal.h"

UART_HandleTypeDef huart1;

void UART1_Init(void)
{
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    HAL_UART_Init(&huart1);
}

// 发送数据
HAL_UART_Transmit(&huart1, (uint8_t *)"Hello", 5, 100);

// 接收数据
uint8_t rx_buf[256];
HAL_UART_Receive(&huart1, rx_buf, 10, 100);
```

### 中断方式

```c
uint8_t rx_data;

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1)
    {
        // 处理接收数据
        process_data(rx_data);
        
        // 重新启动接收
        HAL_UART_Receive_IT(&huart1, &rx_data, 1);
    }
}

// 启动中断接收
HAL_UART_Receive_IT(&huart1, &rx_data, 1);
```

### DMA方式

```c
uint8_t tx_buf[256];
uint8_t rx_buf[256];

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
    // 发送完成
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    // 接收完成
}

// DMA发送
HAL_UART_Transmit_DMA(&huart1, tx_buf, 256);

// DMA接收
HAL_UART_Receive_DMA(&huart1, rx_buf, 256);
```

### 重定向printf

```c
#include <stdio.h>

#ifdef __GNUC__
int __io_putchar(int ch)
{
    HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF);
    return ch;
}
#else
int fputc(int ch, FILE *f)
{
    HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF);
    return ch;
}
#endif
```

## ESP32 UART编程

```c
#include "driver/uart.h"

#define UART_NUM    UART_NUM_1
#define BUF_SIZE    1024

void uart_init(void)
{
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };
    
    uart_param_config(UART_NUM, &uart_config);
    uart_set_pin(UART_NUM, 4, 5, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM, BUF_SIZE * 2, BUF_SIZE * 2, 0, NULL, 0);
}

// 发送数据
const char *data = "Hello";
uart_write_bytes(UART_NUM, data, strlen(data));

// 接收数据
uint8_t *data = (uint8_t *) malloc(BUF_SIZE);
int len = uart_read_bytes(UART_NUM, data, BUF_SIZE, 100 / portTICK_RATE_MS);
```

## 树莓派串口编程

### serial（Python）

```python
import serial
import time

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# 发送数据
ser.write(b'Hello')

# 接收数据
data = ser.read(10)
data = ser.readline()  # 读取一行

ser.close()
```

### 异步读写

```python
import serial
import threading

def read_thread(ser):
    while True:
        data = ser.readline()
        if data:
            print(f"Received: {data}")

ser = serial.Serial('/dev/ttyS0', 115200)
thread = threading.Thread(target=read_thread, args=(ser,))
thread.start()

ser.write(b'Hello\n')
```

## RS-232与RS-485

### RS-232

- 电平：±3V~±15V
- 距离：最大15米
- 全双工
- 点对点通信

### RS-485

- 电平：差分信号（-7V~+12V）
- 距离：最大1200米
- 半双工
- 多点通信（最多32个节点）

```c
// RS-485方向控制
#define RS485_TX()  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, GPIO_PIN_SET)
#define RS485_RX()  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_8, GPIO_PIN_RESET)

void rs485_send(uint8_t *data, uint16_t len)
{
    RS485_TX();
    HAL_UART_Transmit(&huart1, data, len, 100);
    RS485_RX();
}
```

## 串口应用协议

### AT命令

```c
// 发送AT命令
void send_at_cmd(const char *cmd)
{
    char buf[256];
    sprintf(buf, "AT%s\r\n", cmd);
    HAL_UART_Transmit(&huart1, (uint8_t *)buf, strlen(buf), 100);
}

// 等待响应
int wait_response(const char *expected, uint32_t timeout)
{
    char buf[256];
    uint32_t start = HAL_GetTick();
    
    while (HAL_GetTick() - start < timeout) {
        // 接收并检查响应
        if (strstr(buf, expected) != NULL) {
            return 0;
        }
    }
    return -1;
}
```

### Modbus RTU

```c
uint16_t modbus_crc16(uint8_t *data, uint16_t len)
{
    uint16_t crc = 0xFFFF;
    for (uint16_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 0x0001)
                crc = (crc >> 1) ^ 0xA001;
            else
                crc >>= 1;
        }
    }
    return crc;
}

// 发送Modbus请求
void modbus_read_holding_regs(uint8_t slave, uint16_t addr, uint16_t count)
{
    uint8_t frame[8];
    frame[0] = slave;
    frame[1] = 0x03;  // 功能码
    frame[2] = addr >> 8;
    frame[3] = addr & 0xFF;
    frame[4] = count >> 8;
    frame[5] = count & 0xFF;
    
    uint16_t crc = modbus_crc16(frame, 6);
    frame[6] = crc & 0xFF;
    frame[7] = crc >> 8;
    
    HAL_UART_Transmit(&huart1, frame, 8, 100);
}
```

## 串口调试

### 常用工具

- **minicom**：Linux终端串口工具
- **PuTTY**：Windows串口终端
- **SSCOM**：串口调试助手
- **Tera Term**：多功能终端

### 调试技巧

1. **检查连接**：TX接RX，RX接TX，GND接GND
2. **确认波特率**：双方波特率必须一致
3. **查看数据格式**：确认8N1等配置
4. **使用逻辑分析仪**：观察波形和时序

### 常见问题

1. **乱码**
   - 波特率不匹配
   - 时钟源偏差大

2. **无法接收**
   - TX/RX接反
   - 线路未连接

3. **数据丢失**
   - 缓冲区溢出
   - 中断优先级问题
   - 处理速度跟不上

## 参考资料

- [Serial Programming](https://www.cmrr.umn.edu/~strupp/serial.html)
- [Linux Serial HOWTO](https://tldp.org/HOWTO/Serial-HOWTO.html)
- [STM32 UART HAL](https://www.st.com/en/embedded-software/stm32cube-hal.html)

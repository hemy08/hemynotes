# GPIO编程

## 概述

GPIO（General Purpose Input/Output，通用输入输出）是嵌入式系统中最基础的硬件接口，用于控制外部设备或读取外部信号。

## GPIO工作模式

### 输入模式

| 模式 | 说明 |
|------|------|
| 浮空输入 | 引脚既不上拉也不下拉 |
| 上拉输入 | 引脚通过电阻连接到VCC |
| 下拉输入 | 引脚通过电阻连接到GND |
| 模拟输入 | 用于ADC采集 |

### 输出模式

| 模式 | 说明 |
|------|------|
| 推挽输出 | 输出高/低电平，有驱动能力 |
| 开漏输出 | 只能输出低电平，需要外接上拉 |
| 开漏复用 | 复用功能开漏输出 |

## Linux GPIO编程

### sysfs方式（旧API）

```bash
# 导出GPIO
echo 18 > /sys/class/gpio/export

# 设置方向
echo out > /sys/class/gpio/gpio18/direction
echo in > /sys/class/gpio/gpio18/direction

# 设置电平
echo 1 > /sys/class/gpio/gpio18/value
echo 0 > /sys/class/gpio/gpio18/value

# 读取电平
cat /sys/class/gpio/gpio18/value

# 设置边沿触发
echo rising > /sys/class/gpio/gpio18/edge
echo falling > /sys/class/gpio/gpio18/edge
echo both > /sys/class/gpio/gpio18/edge

# 释放GPIO
echo 18 > /sys/class/gpio/unexport
```

### libgpiod方式（新API）

```c
#include <gpiod.h>

struct gpiod_chip *chip;
struct gpiod_line *line;
int value;

// 打开GPIO控制器
chip = gpiod_chip_open_by_name("gpiochip0");

// 获取GPIO线
line = gpiod_chip_get_line(chip, 18);

// 设置为输出
gpiod_line_request_output(line, "myapp", 0);

// 设置电平
gpiod_line_set_value(line, 1);
gpiod_line_set_value(line, 0);

// 设置为输入
gpiod_line_request_input(line, "myapp");

// 读取电平
value = gpiod_line_get_value(line);

// 释放资源
gpiod_line_release(line);
gpiod_chip_close(chip);
```

### GPIO中断

```c
#include <gpiod.h>
#include <poll.h>

struct gpiod_line_event event;

// 设置为输入并启用中断
gpiod_line_request_rising_edge_events(line, "myapp");

// 等待事件
while (1) {
    if (gpiod_line_event_wait(line, NULL) == 1) {
        gpiod_line_event_read(line, &event);
        if (event.event_type == GPIOD_LINE_EVENT_RISING_EDGE) {
            printf("Rising edge detected\n");
        }
    }
}
```

## STM32 GPIO编程

### HAL库方式

```c
#include "stm32f4xx_hal.h"

// GPIO初始化
void GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

// 设置电平
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);

// 翻转电平
HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);

// 读取电平
GPIO_PinState state = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_5);
```

### 输入模式配置

```c
GPIO_InitTypeDef GPIO_InitStruct = {0};

__HAL_RCC_GPIOA_CLK_ENABLE();

GPIO_InitStruct.Pin = GPIO_PIN_0;
GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
GPIO_InitStruct.Pull = GPIO_PULLUP;        // 上拉输入
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
```

### 外部中断配置

```c
void EXTI_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    HAL_NVIC_SetPriority(EXTI0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}

// 中断服务函数
void EXTI0_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

// 回调函数
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_0)
    {
        // 中断处理
    }
}
```

## ESP32 GPIO编程

### 基本使用

```c
#include "driver/gpio.h"

// 配置GPIO
gpio_config_t io_conf = {
    .pin_bit_mask = (1ULL << GPIO_NUM_2),
    .mode = GPIO_MODE_OUTPUT,
    .pull_up_en = GPIO_PULLUP_DISABLE,
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .intr_type = GPIO_INTR_DISABLE
};
gpio_config(&io_conf);

// 设置电平
gpio_set_level(GPIO_NUM_2, 1);
gpio_set_level(GPIO_NUM_2, 0);

// 读取电平
int level = gpio_get_level(GPIO_NUM_2);
```

### GPIO中断

```c
#include "driver/gpio.h"

static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    uint32_t gpio_num = (uint32_t) arg;
    // 中断处理
}

void gpio_interrupt_init(void)
{
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << GPIO_NUM_0),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_NEGEDGE
    };
    gpio_config(&io_conf);
    
    gpio_install_isr_service(0);
    gpio_isr_handler_add(GPIO_NUM_0, gpio_isr_handler, (void*) GPIO_NUM_0);
}
```

## 树莓派GPIO编程

### RPi.GPIO（Python）

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# 输出控制
GPIO.output(18, GPIO.HIGH)
GPIO.output(18, GPIO.LOW)

# PWM输出
pwm = GPIO.PWM(18, 1000)  # 1kHz
pwm.start(50)              # 50%占空比
pwm.ChangeDutyCycle(75)    # 改变占空比
pwm.stop()

GPIO.cleanup()
```

### 输入检测

```python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 轮询检测
if GPIO.input(17) == GPIO.LOW:
    print("Button pressed")

# 边沿检测
GPIO.wait_for_edge(17, GPIO.FALLING)

# 中断回调
def callback(channel):
    print("Edge detected on channel", channel)

GPIO.add_event_detect(17, GPIO.RISING, callback=callback)

GPIO.cleanup()
```

### WiringPi（C）

```c
#include <wiringPi.h>

int main(void)
{
    wiringPiSetupGpio();
    
    pinMode(18, OUTPUT);
    
    digitalWrite(18, HIGH);
    digitalWrite(18, LOW);
    
    // 软件PWM
    softPwmCreate(18, 0, 100);
    softPwmWrite(18, 50);
    
    return 0;
}
```

## 设备树GPIO配置

### 在设备树中定义GPIO

```dts
/ {
    my_device {
        compatible = "vendor,my-device";
        led-gpios = <&gpio0 18 GPIO_ACTIVE_HIGH>;
        button-gpios = <&gpio0 17 GPIO_ACTIVE_LOW>;
    };
};
```

### 在驱动中使用

```c
#include <linux/gpio.h>
#include <linux/of_gpio.h>

struct device_node *np = of_find_node_by_name(NULL, "my_device");
int led_gpio = of_get_named_gpio(np, "led-gpios", 0);

gpio_request(led_gpio, "led");
gpio_direction_output(led_gpio, 1);
gpio_set_value(led_gpio, 0);
gpio_free(led_gpio);
```

## 常见应用场景

### LED控制

```c
void led_on(void)
{
    gpio_set_level(LED_GPIO, 1);
}

void led_off(void)
{
    gpio_set_level(LED_GPIO, 0);
}

void led_blink(int times)
{
    for (int i = 0; i < times; i++) {
        led_on();
        delay_ms(500);
        led_off();
        delay_ms(500);
    }
}
```

### 按键检测

```c
#define KEY_GPIO    17
#define KEY_PRESSED 0

int key_scan(void)
{
    if (gpio_get_level(KEY_GPIO) == KEY_PRESSED) {
        delay_ms(20);  // 消抖
        if (gpio_get_level(KEY_GPIO) == KEY_PRESSED) {
            while (gpio_get_level(KEY_GPIO) == KEY_PRESSED);
            return 1;
        }
    }
    return 0;
}
```

### 继电器控制

```c
#define RELAY_GPIO  18

void relay_on(void)
{
    gpio_set_level(RELAY_GPIO, 1);
}

void relay_off(void)
{
    gpio_set_level(RELAY_GPIO, 0);
}
```

## 注意事项

1. **电平匹配**：确保GPIO电平与外设匹配（3.3V/5V）
2. **驱动能力**：GPIO输出电流有限，大负载需要驱动电路
3. **上下拉选择**：按键等输入需要配置合适的上下拉
4. **消抖处理**：机械按键需要消抖处理
5. **保护措施**：必要时添加限流电阻和保护电路

## 参考资料

- [Linux GPIO文档](https://www.kernel.org/doc/html/latest/driver-api/gpio/)
- [libgpiod文档](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/about/)
- [STM32 HAL库](https://www.st.com/en/embedded-software/stm32cube-hal.html)
- [ESP-IDF GPIO](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html)

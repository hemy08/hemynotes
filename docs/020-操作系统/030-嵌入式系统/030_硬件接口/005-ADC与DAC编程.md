# ADC与DAC编程

## 概述

ADC（Analog-to-Digital Converter，模数转换器）和DAC（Digital-to-Analog Converter，数模转换器）是连接模拟世界和数字世界的重要接口。

## ADC基础

### ADC参数

| 参数 | 说明 |
|------|------|
| 分辨率 | 位数，如8位、12位、16位 |
| 采样率 | 每秒采样次数（SPS） |
| 输入范围 | 可测量的电压范围 |
| 精度 | 测量值与真实值的偏差 |
| 通道数 | 可测量的模拟通道数量 |

### 分辨率计算

```
分辨率 = 满量程电压 / (2^位数 - 1)

例：12位ADC，参考电压3.3V
分辨率 = 3.3V / 4095 ≈ 0.8mV
```

## Linux ADC编程

### 使用IIO子系统

```c
#include <stdio.h>
#include <stdlib.h>

int read_adc(int channel)
{
    char path[64];
    char buf[16];
    int value;
    
    // 读取原始值
    snprintf(path, sizeof(path), 
             "/sys/bus/iio/devices/iio:device0/in_voltage%d_raw", 
             channel);
    FILE *f = fopen(path, "r");
    if (!f) return -1;
    fgets(buf, sizeof(buf), f);
    fclose(f);
    
    value = atoi(buf);
    
    // 读取缩放因子
    snprintf(path, sizeof(path),
             "/sys/bus/iio/devices/iio:device0/in_voltage%d_scale",
             channel);
    f = fopen(path, "r");
    if (f) {
        fgets(buf, sizeof(buf), f);
        fclose(f);
        float scale = atof(buf);
        return (int)(value * scale);
    }
    
    return value;
}

// 转换为电压
float adc_to_voltage(int raw, int bits, float vref)
{
    return (raw * vref) / ((1 << bits) - 1);
}
```

### 使用libiio

```c
#include <iio.h>

struct iio_context *ctx;
struct iio_device *dev;
struct iio_channel *ch;

// 连接到本地IIO
ctx = iio_create_local_context();

// 获取ADC设备
dev = iio_context_find_device(ctx, "adc0");

// 获取通道
ch = iio_device_find_channel(dev, "voltage0", false);

// 启用通道
iio_channel_enable(ch);

// 读取数据
int buf[100];
iio_device_read(dev, buf, sizeof(buf));
```

## STM32 ADC编程

### HAL库单次转换

```c
#include "stm32f4xx_hal.h"

ADC_HandleTypeDef hadc1;

void ADC_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = DISABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    HAL_ADC_Init(&hadc1);
    
    sConfig.Channel = ADC_CHANNEL_0;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_480CYCLES;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
}

uint16_t read_adc(void)
{
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, 100);
    uint16_t value = HAL_ADC_GetValue(&hadc1);
    HAL_ADC_Stop(&hadc1);
    return value;
}
```

### 多通道扫描模式

```c
uint16_t adc_values[4];

void ADC_Multi_Init(void)
{
    hadc1.Init.ScanConvMode = ENABLE;
    hadc1.Init.NbrOfConversion = 4;
    
    // 配置多个通道
    ADC_ChannelConfTypeDef sConfig = {0};
    
    sConfig.Channel = ADC_CHANNEL_0;
    sConfig.Rank = 1;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    sConfig.Channel = ADC_CHANNEL_1;
    sConfig.Rank = 2;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // ... 其他通道
}

void read_all_channels(void)
{
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_values, 4);
}
```

### 中断方式

```c
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
    if (hadc->Instance == ADC1) {
        uint16_t value = HAL_ADC_GetValue(hadc);
        // 处理ADC值
    }
}

void start_adc_interrupt(void)
{
    HAL_ADC_Start_IT(&hadc1);
}
```

## ESP32 ADC编程

```c
#include "driver/adc.h"

void adc_init(void)
{
    // 配置ADC1
    adc1_config_width(ADC_WIDTH_BIT_12);
    adc1_config_channel_atten(ADC1_CHANNEL_0, ADC_ATTEN_DB_11);
}

int read_adc(void)
{
    return adc1_get_raw(ADC1_CHANNEL_0);
}

// 使用ESP-IDF高级API
#include "esp_adc/adc_oneshot.h"

adc_oneshot_unit_handle_t adc1_handle;

void adc_oneshot_init(void)
{
    adc_oneshot_unit_init_cfg_t init_config = {
        .unit_id = ADC_UNIT_1,
    };
    adc_oneshot_new_unit(&init_config, &adc1_handle);
    
    adc_oneshot_chan_cfg_t config = {
        .atten = ADC_ATTEN_DB_11,
        .bitwidth = ADC_BITWIDTH_12,
    };
    adc_oneshot_config_channel(adc1_handle, ADC_CHANNEL_0, &config);
}

int read_adc_oneshot(void)
{
    int adc_raw;
    adc_oneshot_read(adc1_handle, ADC_CHANNEL_0, &adc_raw);
    return adc_raw;
}
```

## DAC编程

### Linux DAC编程

```c
// 通过IIO写入DAC值
void write_dac(int value)
{
    char path[64];
    snprintf(path, sizeof(path),
             "/sys/bus/iio/devices/iio:device0/out_voltage0_raw");
    
    FILE *f = fopen(path, "w");
    if (f) {
        fprintf(f, "%d", value);
        fclose(f);
    }
}
```

### STM32 DAC编程

```c
#include "stm32f4xx_hal.h"

DAC_HandleTypeDef hdac;

void DAC_Init(void)
{
    DAC_ChannelConfTypeDef sConfig = {0};
    
    hdac.Instance = DAC;
    HAL_DAC_Init(&hdac);
    
    sConfig.DAC_Trigger = DAC_TRIGGER_NONE;
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
}

void set_dac(uint16_t value)
{
    // 12位DAC，值范围0-4095
    HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, value);
    HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
}

// 输出正弦波
void output_sine(void)
{
    const uint16_t sine_table[100] = { /* 正弦表 */ };
    int i = 0;
    
    while (1) {
        HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, sine_table[i]);
        i = (i + 1) % 100;
        HAL_Delay(10);
    }
}
```

### ESP32 DAC编程

```c
#include "driver/dac.h"

void dac_init(void)
{
    dac_output_enable(DAC_CHANNEL_1);
}

void set_dac(uint8_t value)
{
    // 8位DAC，值范围0-255
    dac_output_voltage(DAC_CHANNEL_1, value);
}
```

## 电压转换工具函数

```c
// ADC值转电压
float adc_to_voltage(uint16_t adc_value, float vref, uint8_t bits)
{
    return (adc_value * vref) / ((1 << bits) - 1);
}

// 电压转ADC值
uint16_t voltage_to_adc(float voltage, float vref, uint8_t bits)
{
    return (uint16_t)((voltage / vref) * ((1 << bits) - 1));
}

// ADC值转温度（热敏电阻）
float adc_to_temperature(uint16_t adc_value, float vref, uint8_t bits)
{
    float vout = adc_to_voltage(adc_value, vref, bits);
    float r_thermistor = 10000.0 * vout / (vref - vout);  // 10K上拉
    
    // B值方程
    float b_value = 3950.0;
    float t0 = 298.15;  // 25°C in Kelvin
    float r0 = 10000.0;
    
    float temp = 1.0 / (1.0/t0 + 1.0/b_value * log(r_thermistor/r0));
    return temp - 273.15;  // 转换为摄氏度
}
```

## 常见ADC芯片

### MCP3008（SPI接口）

```c
uint16_t mcp3008_read(uint8_t channel)
{
    uint8_t tx[3] = {
        0x01,
        (0x80 | (channel << 4)),
        0x00
    };
    uint8_t rx[3] = {0};
    
    cs_low();
    spi_transfer(tx, rx, 3);
    cs_high();
    
    return ((rx[1] & 0x03) << 8) | rx[2];
}
```

### ADS1115（I2C接口）

```c
// 配置ADS1115
void ads1115_config(uint8_t channel)
{
    uint16_t config = 0x8483;  // 单次转换，通道0，±4.096V，128SPS
    config |= (channel << 12);
    
    uint8_t data[3] = {0x01, config >> 8, config & 0xFF};
    i2c_write(0x48, data, 3);
}

// 读取ADS1115
int16_t ads1115_read(void)
{
    uint8_t data[2];
    i2c_write(0x48, (uint8_t[]){0x00}, 1);
    i2c_read(0x48, data, 2);
    
    return (data[0] << 8) | data[1];
}
```

## 参考资料

- [Linux IIO子系统](https://www.kernel.org/doc/html/latest/driver-api/iio/)
- [STM32 ADC HAL](https://www.st.com/en/embedded-software/stm32cube-hal.html)
- [ESP-IDF ADC](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html)

# FreeRTOS入门

## 概述

FreeRTOS是一个流行的开源实时操作系统内核，专为嵌入式系统设计，支持多种处理器架构。

## FreeRTOS特点

1. **小巧高效**：内核代码约9000行C代码
2. **可移植性强**：支持40+处理器架构
3. **实时性强**：确定性调度，微秒级响应
4. **开源免费**：MIT许可证

## 任务管理

### 创建任务

```c
#include "FreeRTOS.h"
#include "task.h"

void vTaskFunction(void *pvParameters) {
    while (1) {
        // 任务代码
        vTaskDelay(pdMS_TO_TICKS(1000));  // 延时1秒
    }
}

int main(void) {
    xTaskCreate(
        vTaskFunction,       // 任务函数
        "TaskName",          // 任务名称
        128,                 // 栈大小（字）
        NULL,                // 参数
        1,                   // 优先级
        NULL                 // 任务句柄
    );
    
    vTaskStartScheduler();    // 启动调度器
    return 0;
}
```

### 任务优先级

```c
#define PRIORITY_HIGH      5
#define PRIORITY_NORMAL    3
#define PRIORITY_LOW       1

xTaskCreate(vHighTask, "High", 128, NULL, PRIORITY_HIGH, NULL);
xTaskCreate(vNormalTask, "Normal", 128, NULL, PRIORITY_NORMAL, NULL);
xTaskCreate(vLowTask, "Low", 128, NULL, PRIORITY_LOW, NULL);
```

### 任务状态

```c
// 挂起任务
vTaskSuspend(xTaskHandle);

// 恢复任务
vTaskResume(xTaskHandle);

// 删除任务
vTaskDelete(xTaskHandle);
```

## 任务延时

### 相对延时

```c
vTaskDelay(pdMS_TO_TICKS(100));    // 延时100ms
```

### 绝对延时

```c
TickType_t xLastWakeTime = xTaskGetTickCount();
const TickType_t xFrequency = pdMS_TO_TICKS(100);

while (1) {
    // 任务代码
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
}
```

## 信号量

### 二值信号量

```c
SemaphoreHandle_t xSemaphore;

xSemaphore = xSemaphoreCreateBinary();

// 获取信号量
if (xSemaphoreTake(xSemaphore, pdMS_TO_TICKS(100)) == pdTRUE) {
    // 获取成功
    xSemaphoreGive(xSemaphore);  // 释放
}

// 中断中释放
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
xSemaphoreGiveFromISR(xSemaphore, &xHigherPriorityTaskWoken);
portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
```

### 计数信号量

```c
SemaphoreHandle_t xCountingSemaphore;

xCountingSemaphore = xSemaphoreCreateCounting(10, 0);  // 最大10，初始0
```

### 互斥量

```c
SemaphoreHandle_t xMutex;

xMutex = xSemaphoreCreateMutex();

if (xSemaphoreTake(xMutex, portMAX_DELAY) == pdTRUE) {
    // 临界区
    xSemaphoreGive(xMutex);
}
```

## 队列

### 创建队列

```c
QueueHandle_t xQueue;

xQueue = xQueueCreate(10, sizeof(uint32_t));  // 10个uint32_t元素

// 发送数据
uint32_t data = 123;
xQueueSend(xQueue, &data, pdMS_TO_TICKS(100));

// 接收数据
uint32_t received;
xQueueReceive(xQueue, &received, pdMS_TO_TICKS(100));
```

### 队列集

```c
QueueSetHandle_t xQueueSet;
xQueueSet = xQueueCreateSet(10);

xQueueAddToSet(xQueue1, xQueueSet);
xQueueAddToSet(xSemaphore, xQueueSet);
```

## 软件定时器

```c
TimerHandle_t xTimer;

void vTimerCallback(TimerHandle_t xTimer) {
    // 定时器回调
}

xTimer = xTimerCreate(
    "Timer",                        // 名称
    pdMS_TO_TICKS(1000),            // 周期1000ms
    pdTRUE,                         // 自动重载
    NULL,                           // 参数
    vTimerCallback                  // 回调函数
);

xTimerStart(xTimer, 0);             // 启动定时器
xTimerStop(xTimer, 0);              // 停止定时器
```

## 任务通知

```c
// 发送通知
xTaskNotify(xTaskHandle, 0x01, eSetBits);

// 等待通知
uint32_t ulNotificationValue;
xTaskNotifyWait(0x00, 0xFFFFFFFF, &ulNotificationValue, portMAX_DELAY);
```

## 内存管理

FreeRTOS提供5种内存管理方案：

| 方案 | 说明 |
|------|------|
| heap_1 | 只分配不释放 |
| heap_2 | 可分配释放，不合并 |
| heap_3 | 包装标准malloc/free |
| heap_4 | 可分配释放，合并相邻块 |
| heap_5 | 多内存区域 |

## 配置FreeRTOS

### FreeRTOSConfig.h

```c
#define configUSE_PREEMPTION            1       // 抢占式调度
#define configUSE_IDLE_HOOK             1       // 空闲任务钩子
#define configUSE_TICK_HOOK             1       // 时钟钩子
#define configCPU_CLOCK_HZ              (72000000UL)
#define configTICK_RATE_HZ              ((TickType_t)1000)
#define configMAX_PRIORITIES            (5)
#define configMINIMAL_STACK_SIZE        ((unsigned short)128)
#define configTOTAL_HEAP_SIZE           ((size_t)(10 * 1024))
#define configUSE_16_BIT_TICKS          0
```

## 常用API速查

| API | 说明 |
|-----|------|
| `xTaskCreate()` | 创建任务 |
| `vTaskDelete()` | 删除任务 |
| `vTaskDelay()` | 延时 |
| `vTaskSuspend()` | 挂起任务 |
| `vTaskResume()` | 恢复任务 |
| `uxTaskPriorityGet()` | 获取优先级 |
| `vTaskPrioritySet()` | 设置优先级 |

## 参考资料

- [FreeRTOS官网](https://www.freertos.org/)
- [FreeRTOS API参考](https://www.freertos.org/a00106.html)
- [Mastering FreeRTOS](https://www.freertos.org/Documentation/RTOS_book.html)

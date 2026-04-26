# FreeRTOS IPC详解

## 概述

进程间通信（IPC）是RTOS中任务间数据交换和同步的核心机制，FreeRTOS提供了多种IPC方式。

## IPC类型比较

| IPC类型 | 特点 | 适用场景 |
|---------|------|----------|
| 信号量 | 同步、资源计数 | 资源共享、事件同步 |
| 互斥量 | 互斥访问、优先级继承 | 临界区保护 |
| 事件集 | 多事件同步、位操作 | 多条件等待 |
| 队列 | 数据传输、FIFO | 任务间数据传递 |
| 邮箱 | 固定大小数据传输 | 高效数据传递 |
| 任务通知 | 轻量、快速 | 简单同步/数据传递 |

## 信号量

### 二值信号量

用于任务同步，相当于一个标志。

```c
#include "FreeRTOS.h"
#include "semphr.h"

SemaphoreHandle_t binary_sem;

void setup(void)
{
    binary_sem = xSemaphoreCreateBinary();
}

// 等待信号量（阻塞）
void waiting_task(void *pvParameters)
{
    while (1) {
        if (xSemaphoreTake(binary_sem, portMAX_DELAY) == pdTRUE) {
            // 事件发生，执行处理
            process_event();
        }
    }
}

// 发送信号量（非阻塞）
void ISR_handler(void)
{
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    
    xSemaphoreGiveFromISR(binary_sem, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

### 计数信号量

用于资源计数。

```c
SemaphoreHandle_t counting_sem;

void setup(void)
{
    // 最大计数10，初始值5
    counting_sem = xSemaphoreCreateCounting(10, 5);
}

// 获取资源
int acquire_resource(void)
{
    if (xSemaphoreTake(counting_sem, pdMS_TO_TICKS(100)) == pdTRUE) {
        return 0;  // 成功
    }
    return -1;  // 资源不足
}

// 释放资源
void release_resource(void)
{
    xSemaphoreGive(counting_sem);
}

// 查看当前计数
UBaseType_t count = uxSemaphoreGetCount(counting_sem);
```

## 互斥量

### 基本互斥量

```c
SemaphoreHandle_t mutex;

void setup(void)
{
    mutex = xSemaphoreCreateMutex();
}

void critical_section_task(void *pvParameters)
{
    while (1) {
        // 获取互斥量
        if (xSemaphoreTake(mutex, pdMS_TO_TICKS(1000)) == pdTRUE) {
            // 临界区
            shared_resource++;
            
            // 释放互斥量
            xSemaphoreGive(mutex);
        }
    }
}
```

### 递归互斥量

同一个任务可以多次获取。

```c
SemaphoreHandle_t recursive_mutex;

void setup(void)
{
    recursive_mutex = xSemaphoreCreateRecursiveMutex();
}

void nested_function(void)
{
    // 可以多次获取
    xSemaphoreTakeRecursive(recursive_mutex, portMAX_DELAY);
    xSemaphoreTakeRecursive(recursive_mutex, portMAX_DELAY);
    
    // 必须释放相同次数
    xSemaphoreGiveRecursive(recursive_mutex);
    xSemaphoreGiveRecursive(recursive_mutex);
}
```

### 优先级继承

FreeRTOS互斥量自动实现优先级继承，防止优先级反转。

```
优先级反转问题：
任务L(低)持有互斥量
任务H(高)等待互斥量 -> 被阻塞
任务M(中)就绪 -> 抢占L -> H被M延迟！

优先级继承解决：
H等待时，L临时提升到H的优先级
L快速完成并释放互斥量
H立即获得互斥量运行
```

## 事件集

### 创建和使用

```c
#include "event_groups.h"

EventGroupHandle_t event_group;

#define EVENT_BIT_0    (1 << 0)
#define EVENT_BIT_1    (1 << 1)
#define EVENT_BIT_2    (1 << 2)

void setup(void)
{
    event_group = xEventGroupCreate();
}

// 等待事件（任意一个）
void wait_any_event(void *pvParameters)
{
    EventBits_t bits;
    
    bits = xEventGroupWaitBits(
        event_group,
        EVENT_BIT_0 | EVENT_BIT_1,  // 等待的位
        pdTRUE,                      // 退出时清除
        pdFALSE,                     // 任意一个即可
        portMAX_DELAY               // 超时
    );
    
    if (bits & EVENT_BIT_0) {
        // 事件0发生
    }
    if (bits & EVENT_BIT_1) {
        // 事件1发生
    }
}

// 等待事件（全部）
void wait_all_events(void *pvParameters)
{
    EventBits_t bits;
    
    bits = xEventGroupWaitBits(
        event_group,
        EVENT_BIT_0 | EVENT_BIT_1,
        pdTRUE,
        pdTRUE,                      // 全部需要
        portMAX_DELAY
    );
}

// 设置事件
void set_event(void)
{
    xEventGroupSetBits(event_group, EVENT_BIT_0);
}

// 中断中设置事件
void ISR_set_event(void)
{
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    
    xEventGroupSetBitsFromISR(event_group, EVENT_BIT_0, 
                              &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

// 清除事件
xEventGroupClearBits(event_group, EVENT_BIT_0);

// 获取当前值
EventBits_t bits = xEventGroupGetBits(event_group);
```

## 队列

### 创建和使用

```c
#include "queue.h"

QueueHandle_t queue;

typedef struct {
    uint8_t id;
    uint32_t data;
} Message;

void setup(void)
{
    // 创建队列：10个元素，每个元素大小为sizeof(Message)
    queue = xQueueCreate(10, sizeof(Message));
}

// 发送任务
void sender_task(void *pvParameters)
{
    Message msg;
    msg.id = 1;
    msg.data = 100;
    
    // 发送消息（阻塞直到有空间）
    xQueueSend(queue, &msg, portMAX_DELAY);
    
    // 发送到队首
    xQueueSendToFront(queue, &msg, pdMS_TO_TICKS(100));
    
    // 发送，如果满则覆盖
    xQueueOverwrite(queue, &msg);
}

// 接收任务
void receiver_task(void *pvParameters)
{
    Message msg;
    
    // 接收消息（阻塞）
    if (xQueueReceive(queue, &msg, portMAX_DELAY) == pdPASS) {
        // 处理消息
        process_message(&msg);
    }
    
    // 查看（不删除）
    xQueuePeek(queue, &msg, pdMS_TO_TICKS(100));
}

// 中断中接收
void ISR_handler(void)
{
    Message msg;
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    
    xQueueReceiveFromISR(queue, &msg, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

### 队列信息

```c
// 查看队列中消息数量
UBaseType_t waiting = uxQueueMessagesWaiting(queue);

// 查看空闲空间
UBaseType_t spaces = uxQueueSpacesAvailable(queue);

// 查询队列是否为空/满
BaseType_t empty = xQueueIsQueueEmptyFromISR(queue);
BaseType_t full = xQueueIsQueueFullFromISR(queue);
```

## 邮箱

FreeRTOS的邮箱是轻量级的消息传递机制，实际上是单元素队列。

```c
QueueHandle_t mailbox;

void setup(void)
{
    // 邮箱：大小为1的队列
    mailbox = xQueueCreate(1, sizeof(uint32_t));
}

// 发送数据（覆盖之前的数据）
void mailbox_send(uint32_t data)
{
    xQueueOverwrite(mailbox, &data);
}

// 接收数据
uint32_t mailbox_receive(void)
{
    uint32_t data;
    xQueuePeek(mailbox, &data, 0);  // 不删除
    return data;
}
```

## 任务通知

任务通知是FreeRTOS最快的IPC机制，每个任务有一个32位通知值。

### 发送通知

```c
// 发送通知（设置位）
void notify_task(TaskHandle_t task)
{
    xTaskNotify(task, 0x01, eSetBits);
}

// 发送通知（增加值）
void increment_notification(TaskHandle_t task)
{
    xTaskNotify(task, 1, eIncrement);
}

// 发送通知（设置值）
void set_notification(TaskHandle_t task, uint32_t value)
{
    xTaskNotify(task, value, eSetValueWithOverwrite);
}

// 中断中发送
void ISR_notify(void)
{
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    
    vTaskNotifyGiveFromISR(task_handle, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

### 接收通知

```c
void waiting_task(void *pvParameters)
{
    uint32_t notification_value;
    
    // 等待通知
    xTaskNotifyWait(0x00,           // 进入时不清除
                    0xFFFFFFFF,     // 退出时全部清除
                    &notification_value,
                    portMAX_DELAY);
    
    if (notification_value & 0x01) {
        // 位0被设置
    }
    
    // 等待信号量式通知
    uint32_t count = ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
}
```

## IPC选择指南

### 同步场景

```c
// 简单事件同步 -> 任务通知（最快）
xTaskNotify(task, 0x01, eSetBits);

// 多事件同步 -> 事件集
xEventGroupSetBits(event_group, EVENT_BIT_0 | EVENT_BIT_1);

// 资源计数 -> 计数信号量
xSemaphoreGive(counting_sem);

// 中断到任务同步 -> 二值信号量或任务通知
xSemaphoreGiveFromISR(binary_sem, &xHigherPriorityTaskWoken);
```

### 互斥场景

```c
// 简单临界区 -> 互斥量
xSemaphoreTake(mutex, portMAX_DELAY);
// 临界区代码
xSemaphoreGive(mutex);

// 可能嵌套 -> 递归互斥量
xSemaphoreTakeRecursive(recursive_mutex, portMAX_DELAY);
```

### 数据传递场景

```c
// 固定大小数据 -> 队列
xQueueSend(queue, &data, portMAX_DELAY);

// 可变大小数据 -> 队列 + 指针
void *ptr = pvPortMalloc(size);
xQueueSend(queue, &ptr, portMAX_DELAY);

// 高速数据流 -> 流缓冲区或环形缓冲区
```

## 参考资料

- [FreeRTOS IPC文档](https://www.freertos.org/a00106.html)
- [任务通知](https://www.freertos.org/tasknotifications.html)

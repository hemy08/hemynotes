# RT-Thread基础

## 概述

RT-Thread是一个国产开源实时操作系统，专为物联网和嵌入式设备设计，具有体积小巧、启动快速、实时性强、可裁剪等特点。

## RT-Thread特点

1. **小巧轻量**：最小内核仅3KB ROM，1KB RAM
2. **实时性强**：抢占式调度，微秒级中断响应
3. **模块化设计**：组件可裁剪，按需配置
4. **丰富组件**：文件系统、网络协议栈、设备框架等
5. **国产自主**：完全自主知识产权，中文文档完善
6. **生态完善**：支持40+处理器架构，200+开发板

## 内核架构

```
┌─────────────────────────────────────────┐
│           应用层 (Application)           │
├─────────────────────────────────────────┤
│           设备驱动框架                    │
├─────────────────────────────────────────┤
│  文件系统 │ 网络协议栈 │ GUI │ 组件层    │
├─────────────────────────────────────────┤
│           内核层 (Kernel)                │
│  ┌─────────────────────────────────┐    │
│  │ 线程管理 │ 调度器 │ 时钟管理    │    │
│  │ 信号量 │ 互斥量 │ 事件集        │    │
│  │ 邮箱 │ 消息队列 │ 内存管理      │    │
│  │ 定时器 │ 中断管理 │ 空闲线程    │    │
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│           板级支持包 (BSP)               │
├─────────────────────────────────────────┤
│           硬件层 (Hardware)              │
└─────────────────────────────────────────┘
```

## 快速入门

### 获取源码

```bash
# 从官方仓库获取
git clone https://github.com/RT-Thread/rt-thread.git

# 或使用Gitee镜像
git clone https://gitee.com/rtthread/rt-thread.git
```

### 使用Env工具配置

```bash
# 下载Env工具
# https://www.rt-thread.org/page/download.html

# 进入BSP目录
cd rt-thread/bsp/stm32/stm32f407-atk-explorer

# 配置工程
scons --menuconfig

# 生成工程
scons --target=mdk5      # Keil MDK
scons --target=iar       # IAR
scons --target=eclipse   # Eclipse
```

### 最小示例

```c
#include <rtthread.h>

int main(void)
{
    rt_kprintf("Hello RT-Thread!\n");
    return 0;
}
```

## 线程管理

### 创建线程

```c
#include <rtthread.h>

#define THREAD_PRIORITY 25
#define THREAD_STACK_SIZE 512
#define THREAD_TIMESLICE 5

static rt_thread_t tid = RT_NULL;

static void thread_entry(void *parameter)
{
    while (1)
    {
        rt_kprintf("Thread running...\n");
        rt_thread_mdelay(1000);
    }
}

int thread_init(void)
{
    tid = rt_thread_create(
        "thread",              // 线程名称
        thread_entry,          // 线程入口函数
        RT_NULL,               // 参数
        THREAD_STACK_SIZE,     // 栈大小
        THREAD_PRIORITY,       // 优先级
        THREAD_TIMESLICE       // 时间片
    );
    
    if (tid != RT_NULL)
    {
        rt_thread_startup(tid);
    }
    
    return 0;
}
```

### 静态创建线程

```c
static struct rt_thread thread;
static char thread_stack[512];

int thread_static_init(void)
{
    rt_thread_init(
        &thread,               // 线程控制块
        "thread",              // 线程名称
        thread_entry,          // 入口函数
        RT_NULL,               // 参数
        &thread_stack[0],      // 栈起始地址
        sizeof(thread_stack),  // 栈大小
        THREAD_PRIORITY,       // 优先级
        THREAD_TIMESLICE       // 时间片
    );
    
    rt_thread_startup(&thread);
    return 0;
}
```

### 线程操作

```c
// 线程挂起
rt_thread_suspend(tid);

// 线程恢复
rt_thread_resume(tid);

// 线程删除
rt_thread_delete(tid);

// 线程延时
rt_thread_mdelay(100);      // 毫秒延时
rt_thread_delay(100);       // tick延时

// 获取当前线程
rt_thread_t self = rt_thread_self();

// 让出CPU
rt_thread_yield();
```

### 线程优先级

RT-Thread优先级范围：0~255，数值越小优先级越高。

```c
#define PRIORITY_HIGHEST    0
#define PRIORITY_HIGH       10
#define PRIORITY_NORMAL     25
#define PRIORITY_LOW        50
```

## 线程间通信

### 信号量

```c
#include <rtthread.h>

static rt_sem_t sem = RT_NULL;

// 创建信号量
sem = rt_sem_create("sem", 0, RT_IPC_FLAG_PRIO);

// 获取信号量
rt_sem_take(sem, RT_WAITING_FOREVER);

// 释放信号量
rt_sem_release(sem);

// 中断中释放
rt_sem_release(sem);

// 删除信号量
rt_sem_delete(sem);
```

### 互斥量

```c
#include <rtthread.h>

static rt_mutex_t mutex = RT_NULL;

// 创建互斥量
mutex = rt_mutex_create("mutex", RT_IPC_FLAG_PRIO);

// 获取互斥量
if (rt_mutex_take(mutex, RT_WAITING_FOREVER) == RT_EOK)
{
    // 临界区
    rt_mutex_release(mutex);
}

// 删除互斥量
rt_mutex_delete(mutex);
```

### 事件集

```c
#include <rtthread.h>

static rt_event_t event = RT_NULL;

// 创建事件集
event = rt_event_create("event", RT_IPC_FLAG_PRIO);

// 发送事件
rt_event_send(event, 0x01);

// 接收事件
rt_uint32_t e;
rt_event_recv(event, 0x01, RT_EVENT_FLAG_AND | RT_EVENT_FLAG_CLEAR, 
              RT_WAITING_FOREVER, &e);

// 删除事件集
rt_event_delete(event);
```

### 邮箱

```c
#include <rtthread.h>

static rt_mailbox_t mb = RT_NULL;

// 创建邮箱
mb = rt_mb_create("mb", 10, RT_IPC_FLAG_PRIO);

// 发送邮件
rt_uint32_t value = 100;
rt_mb_send(mb, value);

// 接收邮件
rt_uint32_t recv;
rt_mb_recv(mb, &recv, RT_WAITING_FOREVER);

// 删除邮箱
rt_mb_delete(mb);
```

### 消息队列

```c
#include <rtthread.h>

static rt_mq_t mq = RT_NULL;

struct msg_data
{
    rt_uint8_t data[32];
};

// 创建消息队列
mq = rt_mq_create("mq", sizeof(struct msg_data), 10, RT_IPC_FLAG_PRIO);

// 发送消息
struct msg_data msg;
rt_mq_send(mq, &msg, sizeof(msg));

// 接收消息
struct msg_data recv;
rt_mq_recv(mq, &recv, sizeof(recv), RT_WAITING_FOREVER);

// 删除消息队列
rt_mq_delete(mq);
```

## 内存管理

### 动态内存

```c
#include <rtthread.h>

// 分配内存
void *ptr = rt_malloc(1024);

// 重新分配
ptr = rt_realloc(ptr, 2048);

// 释放内存
rt_free(ptr);

// 查看内存使用情况
rt_uint32_t total = 0, used = 0, max_used = 0;
rt_memory_info(&total, &used, &max_used);
rt_kprintf("Total: %d, Used: %d\n", total, used);
```

### 内存池

```c
#include <rtthread.h>

static rt_mp_t mp = RT_NULL;

// 创建内存池
mp = rt_mp_create("mp", 10, 128);   // 10个块，每块128字节

// 分配内存块
void *block = rt_mp_alloc(mp, RT_WAITING_FOREVER);

// 释放内存块
rt_mp_free(block);

// 删除内存池
rt_mp_delete(mp);
```

## 软件定时器

```c
#include <rtthread.h>

static rt_timer_t timer = RT_NULL;

static void timer_callback(void *parameter)
{
    rt_kprintf("Timer expired!\n");
}

// 创建定时器
timer = rt_timer_create(
    "timer",                   // 定时器名称
    timer_callback,            // 回调函数
    RT_NULL,                   // 参数
    1000,                      // 周期（tick）
    RT_TIMER_FLAG_PERIODIC     // 周期定时器
);

// 启动定时器
rt_timer_start(timer);

// 停止定时器
rt_timer_stop(timer);

// 删除定时器
rt_timer_delete(timer);
```

## 设备驱动

### 设备注册与查找

```c
#include <rtthread.h>
#include <rtdevice.h>

// 查找设备
rt_device_t dev = rt_device_find("uart1");

// 打开设备
rt_device_open(dev, RT_DEVICE_OFLAG_RDWR);

// 关闭设备
rt_device_close(dev);
```

### 串口设备

```c
#include <rtthread.h>
#include <rtdevice.h>

#define SAMPLE_UART_NAME "uart1"

static rt_device_t serial;

int uart_init(void)
{
    serial = rt_device_find(SAMPLE_UART_NAME);
    if (serial == RT_NULL)
    {
        rt_kprintf("Device not found!\n");
        return -1;
    }
    
    rt_device_open(serial, RT_DEVICE_OFLAG_RDWR | RT_DEVICE_FLAG_INT_RX);
    return 0;
}

// 发送数据
char buf[] = "Hello";
rt_device_write(serial, 0, buf, sizeof(buf));

// 接收数据（阻塞）
char recv[32];
rt_device_read(serial, 0, recv, sizeof(recv));

// 接收回调
rt_err_t rx_callback(rt_device_t dev, rt_size_t size)
{
    // 有数据到达
    return RT_EOK;
}
rt_device_set_rx_indicate(serial, rx_callback);
```

### GPIO设备

```c
#include <rtthread.h>
#include <rtdevice.h>

#define PIN_LED    0   // LED引脚号

// 设置引脚模式
rt_pin_mode(PIN_LED, PIN_MODE_OUTPUT);

// 设置引脚电平
rt_pin_write(PIN_LED, PIN_HIGH);
rt_pin_write(PIN_LED, PIN_LOW);

// 读取引脚电平
rt_base_t value = rt_pin_read(PIN_LED);

// 中断回调
void irq_callback(void *args)
{
    rt_kprintf("IRQ triggered!\n");
}

// 绑定中断
rt_pin_attach_irq(PIN_LED, PIN_IRQ_MODE_RISING, irq_callback, RT_NULL);
rt_pin_irq_enable(PIN_LED, PIN_IRQ_ENABLE);
```

## 文件系统

### DFS文件系统

```c
#include <dfs_posix.h>

// 挂载文件系统
dfs_mount("sd0", "/", "elm", 0, 0);

// 文件操作
int fd = open("/test.txt", O_WRONLY | O_CREAT);
write(fd, "Hello", 5);
close(fd);

fd = open("/test.txt", O_RDONLY);
char buf[32];
read(fd, buf, sizeof(buf));
close(fd);
```

### 虚拟文件系统

```c
// ROMFS（只读文件系统）
dfs_mount("rom", "/rom", "rom", 0, &romfs_root);

// RAMFS（内存文件系统）
dfs_mount("ram", "/ram", "ram", 0, RT_NULL);

// FATFS（SD卡/U盘）
dfs_mount("sd0", "/sd", "elm", 0, RT_NULL);

// LittleFS（Flash文件系统）
dfs_mount("flash", "/data", "lfs", 0, RT_NULL);
```

## 网络协议栈

### Sal套接字抽象层

```c
#include <sys/socket.h>

// 创建套接字
int sock = socket(AF_INET, SOCK_STREAM, 0);

// 连接服务器
struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(80);
addr.sin_addr.s_addr = inet_addr("192.168.1.1");
connect(sock, (struct sockaddr *)&addr, sizeof(addr));

// 发送数据
send(sock, "GET / HTTP/1.1\r\n", 16, 0);

// 接收数据
char buf[1024];
recv(sock, buf, sizeof(buf), 0);

// 关闭套接字
closesocket(sock);
```

## 常用内核配置

### rt_config.h

```c
// 内核配置
#define RT_THREAD_PRIORITY_MAX    32    // 最大优先级数
#define RT_TICK_PER_SECOND        1000  // tick频率
#define RT_ALIGN_SIZE             4     // 对齐大小

// 内存管理
#define RT_USING_HEAP                    // 使用堆内存
#define RT_USING_SMALL_MEM               // 小内存算法

// IPC机制
#define RT_USING_SEMAPHORE              // 信号量
#define RT_USING_MUTEX                  // 互斥量
#define RT_USING_EVENT                  // 事件集
#define RT_USING_MAILBOX                // 邮箱
#define RT_USING_MESSAGEQUEUE           // 消息队列

// 设备框架
#define RT_USING_DEVICE                 // 设备框架
#define RT_USING_CONSOLE                // 控制台
#define RT_USING_FINSH                  // FinSH shell

// 定时器
#define RT_USING_TIMER                  // 软件定时器
```

## FinSH控制台

FinSH是RT-Thread的命令行控制台。

```c
// 导出命令到FinSH
#include <rtthread.h>

void hello_cmd(int argc, char **argv)
{
    rt_kprintf("Hello RT-Thread!\n");
}
MSH_CMD_EXPORT(hello_cmd, hello command);

// 带参数的命令
void echo_cmd(int argc, char **argv)
{
    if (argc > 1)
    {
        rt_kprintf("%s\n", argv[1]);
    }
}
MSH_CMD_EXPORT(echo_cmd, echo command);
```

## 调试技巧

### 内核对象查看

```bash
# FinSH命令
list_thread    # 列出所有线程
list_sem       # 列出所有信号量
list_mutex     # 列出所有互斥量
list_timer     # 列出所有定时器
list_device    # 列出所有设备
```

### 内存调试

```c
// 开启内存调试
#define RT_USING_MEMTRACE

// 查看内存使用
memtrace_dump();
```

## 参考资料

- [RT-Thread官网](https://www.rt-thread.org/)
- [RT-Thread文档中心](https://www.rt-thread.org/document/site/)
- [RT-Thread编程指南](https://www.rt-thread.org/document/site/tutorial/quick-start/)
- [RT-Thread API参考](https://www.rt-thread.org/document/site/api/)

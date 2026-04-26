# Linux内核模块开发

## 概述

Linux内核模块（Kernel Module）是一种可以动态加载和卸载的内核代码，允许在不重新编译整个内核的情况下扩展内核功能。

## 内核模块特点

1. **动态加载**：运行时加载，无需重启
2. **动态卸载**：可以移除不再需要的模块
3. **节省内存**：按需加载，减少内存占用
4. **开发便捷**：独立编译，便于调试

## 基本模块结构

### 最简单的内核模块

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init hello_init(void)
{
    printk(KERN_INFO "Hello, kernel module loaded!\n");
    return 0;
}

static void __exit hello_exit(void)
{
    printk(KERN_INFO "Goodbye, kernel module unloaded!\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("A simple kernel module");
MODULE_VERSION("1.0");
```

### Makefile

```makefile
obj-m += hello.o

KDIR := /lib/modules/$(shell uname -r)/build

all:
    make -C $(KDIR) M=$(PWD) modules

clean:
    make -C $(KDIR) M=$(PWD) clean
```

## 模块操作

### 加载模块

```bash
# 使用insmod加载
insmod hello.ko

# 使用modprobe加载（自动处理依赖）
modprobe hello

# 加载时传递参数
insmod hello.ko param=100
```

### 卸载模块

```bash
# 使用rmmod卸载
rmmod hello

# 使用modprobe卸载
modprobe -r hello
```

### 查看模块

```bash
# 列出已加载模块
lsmod

# 查看模块信息
modinfo hello.ko

# 查看模块依赖
modprobe --show-depends hello
```

## 模块参数

### 定义参数

```c
#include <linux/moduleparam.h>

static int my_int = 100;
static char *my_str = "default";
static int my_array[10];
static int array_size = 10;

module_param(my_int, int, 0644);
MODULE_PARM_DESC(my_int, "An integer parameter");

module_param(my_str, charp, 0644);
MODULE_PARM_DESC(my_str, "A string parameter");

module_param_array(my_array, int, &array_size, 0644);
MODULE_PARM_DESC(my_array, "An array of integers");
```

### 参数权限

| 权限 | 说明 |
|------|------|
| 0 | 不可见，不可修改 |
| 0444 | 只读 |
| 0644 | root可写，其他只读 |
| 0666 | 所有人可读写 |

## 字符设备驱动

### 注册字符设备

```c
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/device.h>

#define DEVICE_NAME "mydevice"
#define CLASS_NAME "myclass"

static int major_number;
static struct class *my_class = NULL;
static struct device *my_device = NULL;
static struct cdev my_cdev;

static int my_open(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "Device opened\n");
    return 0;
}

static int my_release(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "Device closed\n");
    return 0;
}

static ssize_t my_read(struct file *file, char __user *buf,
                       size_t len, loff_t *offset)
{
    char data[] = "Hello from kernel!\n";
    size_t datalen = strlen(data);
    
    if (*offset >= datalen)
        return 0;
    
    if (len > datalen - *offset)
        len = datalen - *offset;
    
    if (copy_to_user(buf, data + *offset, len))
        return -EFAULT;
    
    *offset += len;
    return len;
}

static ssize_t my_write(struct file *file, const char __user *buf,
                        size_t len, loff_t *offset)
{
    printk(KERN_INFO "Received %zu bytes\n", len);
    return len;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = my_open,
    .release = my_release,
    .read = my_read,
    .write = my_write,
};

static int __init my_init(void)
{
    dev_t dev;
    
    // 分配设备号
    if (alloc_chrdev_region(&dev, 0, 1, DEVICE_NAME) < 0) {
        printk(KERN_ERR "Failed to allocate major number\n");
        return -1;
    }
    major_number = MAJOR(dev);
    
    // 初始化cdev
    cdev_init(&my_cdev, &fops);
    my_cdev.owner = THIS_MODULE;
    
    if (cdev_add(&my_cdev, dev, 1) < 0) {
        unregister_chrdev_region(dev, 1);
        return -1;
    }
    
    // 创建设备类
    my_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(my_class)) {
        cdev_del(&my_cdev);
        unregister_chrdev_region(dev, 1);
        return PTR_ERR(my_class);
    }
    
    // 创建设备节点
    my_device = device_create(my_class, NULL, dev, NULL, DEVICE_NAME);
    if (IS_ERR(my_device)) {
        class_destroy(my_class);
        cdev_del(&my_cdev);
        unregister_chrdev_region(dev, 1);
        return PTR_ERR(my_device);
    }
    
    printk(KERN_INFO "Device registered with major %d\n", major_number);
    return 0;
}

static void __exit my_exit(void)
{
    dev_t dev = MKDEV(major_number, 0);
    
    device_destroy(my_class, dev);
    class_destroy(my_class);
    cdev_del(&my_cdev);
    unregister_chrdev_region(dev, 1);
    
    printk(KERN_INFO "Device unregistered\n");
}

module_init(my_init);
module_exit(my_exit);

MODULE_LICENSE("GPL");
```

## Platform驱动

### 平台设备驱动框架

```c
#include <linux/platform_device.h>

static int my_probe(struct platform_device *pdev)
{
    struct resource *res;
    void __iomem *base;
    
    // 获取内存资源
    res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    if (!res)
        return -ENODEV;
    
    base = devm_ioremap_resource(&pdev->dev, res);
    if (IS_ERR(base))
        return PTR_ERR(base);
    
    // 获取中断
    int irq = platform_get_irq(pdev, 0);
    if (irq < 0)
        return irq;
    
    dev_info(&pdev->dev, "Device probed\n");
    return 0;
}

static int my_remove(struct platform_device *pdev)
{
    dev_info(&pdev->dev, "Device removed\n");
    return 0;
}

static const struct of_device_id my_of_match[] = {
    { .compatible = "vendor,mydevice", },
    { }
};
MODULE_DEVICE_TABLE(of, my_of_match);

static struct platform_driver my_driver = {
    .probe = my_probe,
    .remove = my_remove,
    .driver = {
        .name = "mydriver",
        .of_match_table = my_of_match,
    },
};

module_platform_driver(my_driver);

MODULE_LICENSE("GPL");
```

## 中断处理

### 注册中断

```c
#include <linux/interrupt.h>

static irqreturn_t my_interrupt_handler(int irq, void *dev_id)
{
    // 中断处理代码
    return IRQ_HANDLED;
}

static int my_probe(struct platform_device *pdev)
{
    int irq = platform_get_irq(pdev, 0);
    
    if (request_irq(irq, my_interrupt_handler, 
                    IRQF_TRIGGER_RISING, "mydevice", pdev)) {
        dev_err(&pdev->dev, "Failed to request IRQ\n");
        return -ENODEV;
    }
    
    return 0;
}

static int my_remove(struct platform_device *pdev)
{
    int irq = platform_get_irq(pdev, 0);
    free_irq(irq, pdev);
    return 0;
}
```

### 中断下半部

```c
// Tasklet
static void my_tasklet_func(unsigned long data)
{
    // 延迟处理
}

DECLARE_TASKLET(my_tasklet, my_tasklet_func, 0);

static irqreturn_t my_interrupt_handler(int irq, void *dev_id)
{
    tasklet_schedule(&my_tasklet);
    return IRQ_HANDLED;
}

// Workqueue
static struct work_struct my_work;

static void my_work_func(struct work_struct *work)
{
    // 延迟处理
}

static irqreturn_t my_interrupt_handler(int irq, void *dev_id)
{
    schedule_work(&my_work);
    return IRQ_HANDLED;
}

// 初始化
INIT_WORK(&my_work, my_work_func);
```

## 内存操作

### 内核内存分配

```c
#include <linux/slab.h>
#include <linux/vmalloc.h>

// kmalloc（物理连续，DMA安全）
void *ptr = kmalloc(1024, GFP_KERNEL);
kfree(ptr);

// kzalloc（分配并清零）
void *ptr = kzalloc(1024, GFP_KERNEL);

// vmalloc（虚拟连续，大块内存）
void *ptr = vmalloc(1024 * 1024);
vfree(ptr);

// DMA内存
void *dma_addr;
void *virt = dma_alloc_coherent(dev, size, &dma_addr, GFP_KERNEL);
dma_free_coherent(dev, size, virt, dma_addr);
```

### I/O内存访问

```c
#include <linux/io.h>

void __iomem *base = ioremap(0x40000000, 0x1000);

// 读操作
u32 val = readl(base + REG_OFFSET);

// 写操作
writel(val, base + REG_OFFSET);

iounmap(base);
```

## 用户空间交互

### copy_to_user / copy_from_user

```c
#include <linux/uaccess.h>

static ssize_t my_read(struct file *file, char __user *buf,
                       size_t len, loff_t *offset)
{
    char kbuf[128];
    // ... 填充内核数据
    
    if (copy_to_user(buf, kbuf, len))
        return -EFAULT;
    
    return len;
}

static ssize_t my_write(struct file *file, const char __user *buf,
                        size_t len, loff_t *offset)
{
    char kbuf[128];
    
    if (copy_from_user(kbuf, buf, len))
        return -EFAULT;
    
    // 处理用户数据
    return len;
}
```

## 调试技巧

### printk日志级别

```c
printk(KERN_EMERG "Emergency message\n");
printk(KERN_ALERT "Alert message\n");
printk(KERN_CRIT "Critical message\n");
printk(KERN_ERR "Error message\n");
printk(KERN_WARNING "Warning message\n");
printk(KERN_NOTICE "Notice message\n");
printk(KERN_INFO "Info message\n");
printk(KERN_DEBUG "Debug message\n");
```

### 查看内核日志

```bash
# 查看内核日志
dmesg

# 实时查看
dmesg -w

# 清空日志
dmesg -c
```

## 参考资料

- [Linux内核模块编程指南](https://www.kernel.org/doc/html/latest/driver-api/driver-model/basics.html)
- [Linux设备驱动](https://lwn.net/Kernel/LDD3/)
- [内核文档](https://www.kernel.org/doc/html/latest/)

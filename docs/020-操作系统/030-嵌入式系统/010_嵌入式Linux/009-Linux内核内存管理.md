# Linux内核内存管理

## 概述

Linux内核内存管理是操作系统的核心子系统，负责物理内存分配、虚拟内存管理、内存映射等功能。

## 内存管理架构

```
┌─────────────────────────────────────────┐
│           用户空间 (User Space)          │
├─────────────────────────────────────────┤
│    虚拟内存区域 (VMA)    │   页表        │
├─────────────────────────────────────────┤
│           内核空间 (Kernel Space)        │
├─────────────────────────────────────────┤
│  Slab/Slub/Slob  │  页分配器  │ 内存区域 │
├─────────────────────────────────────────┤
│              物理内存 (RAM)              │
└─────────────────────────────────────────┘
```

## 内存区域（Zone）

### Zone类型

| Zone | 说明 | 典型用途 |
|------|------|----------|
| ZONE_DMA | DMA可访问内存 | ISA DMA设备 |
| ZONE_DMA32 | 32位DMA内存 | 32位DMA设备 |
| ZONE_NORMAL | 普通内存 | 内核直接映射 |
| ZONE_HIGHMEM | 高端内存 | 32位系统大内存 |

### 查看内存区域

```bash
cat /proc/zoneinfo
```

## 页分配器

### 分配函数

```c
#include <linux/gfp.h>

// 分配一个页
struct page *page = alloc_page(GFP_KERNEL);

// 分配多个页
struct page *pages = alloc_pages(GFP_KERNEL, order);  // 2^order页

// 分配虚拟地址连续的内存
void *addr = kmalloc(size, GFP_KERNEL);

// 分配并清零
void *addr = kzalloc(size, GFP_KERNEL);

// 分配页对齐内存
void *addr = vmalloc(size);

// 释放内存
kfree(addr);
vfree(addr);
__free_page(page);
__free_pages(pages, order);
```

### GFP标志

```c
// 常用标志
GFP_KERNEL      // 内核内存分配，可能睡眠
GFP_ATOMIC      // 原子分配，不睡眠
GFP_USER        // 用户空间内存
GFP_DMA         // DMA内存
GFP_HIGHUSER    // 高端用户内存

// 修饰符
__GFP_WAIT      // 允许睡眠
__GFP_HIGH      // 高优先级
__GFP_IO        // 允许IO
__GFP_FS        // 允许文件系统操作
__GFP_NOWARN    // 禁止警告
__GFP_NORETRY   // 失败不重试
```

## Slab分配器

### Slab概念

Slab是一种内核对象缓存机制，用于频繁分配/释放相同大小对象。

```
Slab Cache
├── Per-CPU Slab (当前CPU)
│   ├── partial    部分使用的slab
│   ├── full       完全使用的slab
│   └── empty      空闲slab
└── Node Slab (每个NUMA节点)
```

### 创建Slab缓存

```c
#include <linux/slab.h>

// 创建kmem_cache
struct kmem_cache *my_cache;
my_cache = kmem_cache_create(
    "my_object",          // 名称
    sizeof(struct my_obj),// 对象大小
    0,                    // 对齐
    SLAB_HWCACHE_ALIGN,   // 标志
    NULL                  // 构造函数
);

// 从缓存分配对象
struct my_obj *obj = kmem_cache_alloc(my_cache, GFP_KERNEL);

// 释放对象
kmem_cache_free(my_cache, obj);

// 销毁缓存
kmem_cache_destroy(my_cache);
```

### 常用Slab缓存

```c
// 文件结构
struct file *f = kmem_cache_alloc(filp_cachep, GFP_KERNEL);

// 进程描述符
struct task_struct *tsk = kmem_cache_alloc(task_struct_cachep, GFP_KERNEL);

// dentry
struct dentry *d = kmem_cache_alloc(dentry_cache, GFP_KERNEL);
```

## vmalloc

### vmalloc特点

- 分配虚拟地址连续、物理地址不一定连续的内存
- 适合大块内存分配
- 性能比kmalloc差
- 不能用于DMA

```c
#include <linux/vmalloc.h>

// 分配
void *addr = vmalloc(size);
void *addr = vzalloc(size);  // 分配并清零

// 重分配
void *new_addr = vrealloc(addr, new_size);

// 释放
vfree(addr);

// 映射物理页到vmalloc区域
void *addr = ioremap(phys_addr, size);
iounmap(addr);
```

## 内存映射

### mmap实现

```c
static int my_mmap(struct file *filp, struct vm_area_struct *vma)
{
    // 使用remap_pfn_range映射物理内存
    unsigned long phys = ...;  // 物理地址
    unsigned long size = vma->vm_end - vma->vm_start;
    
    if (remap_pfn_range(vma, vma->vm_start, phys >> PAGE_SHIFT,
                        size, vma->vm_page_prot))
        return -EAGAIN;
    
    return 0;
}

// 使用vm_operations_struct
static const struct vm_operations_struct my_vm_ops = {
    .open = my_vma_open,
    .close = my_vma_close,
    .fault = my_vma_fault,
};

static int my_mmap(struct file *filp, struct vm_area_struct *vma)
{
    vma->vm_ops = &my_vm_ops;
    return 0;
}
```

## DMA内存

### 一致性DMA内存

```c
#include <linux/dma-mapping.h>

// 分配DMA缓冲区
void *vaddr;
dma_addr_t dma_handle;

vaddr = dma_alloc_coherent(dev, size, &dma_handle, GFP_KERNEL);
// 使用vaddr（CPU虚拟地址）和dma_handle（DMA地址）

// 释放
dma_free_coherent(dev, size, vaddr, dma_handle);
```

### 流式DMA映射

```c
// 单次传输
dma_addr_t dma_handle = dma_map_single(dev, vaddr, size, DMA_TO_DEVICE);

// 等待DMA完成
dma_unmap_single(dev, dma_handle, size, DMA_TO_DEVICE);

// 页映射
dma_addr_t dma_handle = dma_map_page(dev, page, offset, size, DMA_FROM_DEVICE);
dma_unmap_page(dev, dma_handle, size, DMA_FROM_DEVICE);

// 同步缓存
dma_sync_single_for_cpu(dev, dma_handle, size, DMA_FROM_DEVICE);
dma_sync_single_for_device(dev, dma_handle, size, DMA_TO_DEVICE);
```

## 内存统计

### 查看内存信息

```bash
# 总体内存信息
cat /proc/meminfo

# 内存区域信息
cat /proc/zoneinfo

# Buddy系统信息
cat /proc/buddyinfo

# Slab信息
cat /proc/slabinfo

# 进程内存
cat /proc/<pid>/maps
cat /proc/<pid>/smaps
```

### 内存统计代码

```c
// 获取空闲内存
unsigned long free_pages = nr_free_pages();
unsigned long free_kb = free_pages * PAGE_SIZE / 1024;

// 获取总内存
unsigned long total_pages = totalram_pages();
unsigned long total_kb = total_pages * PAGE_SIZE / 1024;

// 获取可用内存（估算）
long available = si_mem_available();
```

## 内存调试

### 内存泄漏检测

```c
// 使用kmemleak
CONFIG_DEBUG_KMEMLEAK=y

// 扫描内存泄漏
echo scan > /sys/kernel/debug/kmemleak
cat /sys/kernel/debug/kmemleak

// 清除
echo clear > /sys/kernel/debug/kmemleak
```

### 内存错误检测

```c
// KASAN (Kernel Address Sanitizer)
CONFIG_KASAN=y

// 使用slub调试
CONFIG_SLUB_DEBUG=y
```

## 内存压力

### 内存回收

```c
// 注册内存压力回调
#include <linux/shrinker.h>

static unsigned long my_shrink_count(struct shrinker *shrinker,
                                     struct shrink_control *sc)
{
    // 返回可回收对象数量
    return my_cache_count;
}

static unsigned long my_shrink_scan(struct shrinker *shrinker,
                                    struct shrink_control *sc)
{
    // 回收对象
    // 返回实际回收数量
    return freed;
}

static struct shrinker my_shrinker = {
    .count_objects = my_shrink_count,
    .scan_objects = my_shrink_scan,
    .seeks = DEFAULT_SEEKS,
};

register_shrinker(&my_shrinker);
```

## OOM Killer

### OOM触发条件

当系统内存不足且无法回收足够内存时触发OOM Killer。

```bash
# 查看OOM分数
cat /proc/<pid>/oom_score

# 调整OOM分数（越低越不容易被杀）
echo -500 > /proc/<pid>/oom_score_adj

# 禁止OOM杀死
echo -1000 > /proc/<pid>/oom_score_adj
```

### OOM控制

```c
// 禁用OOM
#include <linux/oom.h>

current->flags |= PF_DUMPCORE;  // 设置标志
```

## 参考资料

- [Linux内存管理文档](https://www.kernel.org/doc/html/latest/admin-guide/mm/index.html)
- [内存管理API](https://www.kernel.org/doc/html/latest/core-api/memory-allocation.html)
- [DMA映射文档](https://www.kernel.org/doc/html/latest/core-api/dma-api.html)

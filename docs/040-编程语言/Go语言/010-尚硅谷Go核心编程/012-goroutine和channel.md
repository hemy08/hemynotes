# goroutine和channel

- [深入理解 Go 调度模型 GPM CSDN博客（csdn.net）](https://blog.csdn.net/weixin_41335923/article/details/124483409)
- [Golang调度器GPM原理与调度全分析 CSDN博客（csdn.net）](https://blog.csdn.net/flynetcn/article/details/126628952)
- [Golang的GPM调度模型 知乎(zhihu.com)](https://zhuanlan.zhihu.com/p/688644598)
- [Golang的协程调度器原理及GMP设计思想 https://github.com/aceld](https://www.yuque.com/aceld/golang/srxd6d#d41f9625)
- [深入golang runtime的调度](https://zboya.github.io/post/go_scheduler/)

并发和并行最开始都是操作系统中的概念，表示的是CPU执行多个任务的方式，但这是两个不同的概念

并发：在操作系统中，是指一个时间段中有几个程序都处于已启动运行到运行完毕之间，且这几个程序都是在同一个处理机上运行

并行：当系统有一个以上CPU时，当一个CPU执行一个进程时，另一个CPU可以执行另一个进程，两个进程互不抢占CPU资源，可以同时进行，这种方式我们称之为并行(Parallel)

**并发其实是一段时间内宏观上多个程序同时运行，而并行是指同一时刻，多个任务真的在同时运行**。

## 一、GPM模型

- [Go语言的GPM模型 简书_(jianshu.com)](https://www.jianshu.com/p/504d9eaf0fd1)

![](https://upload-images.jianshu.io/upload_images/13145841-5d7777384d1fff65.png)


**(G)oroutine**

每个 Goroutine 对应一个 G 结构体，G 存储 Goroutine 的运行堆栈、状态以及任务函数，可重用。G 并非执行体，每个 G 需要绑定到 P 才能被调度执行。

Goroutine是Golang并发执行的轻量级线程。它由Golang运行时管理，而不是操作系统内核。每个Goroutine对应一个G结构体，该结构体存储了Goroutine的状态、栈信息以及待执行的任务函数。Goroutine的栈空间动态伸缩，初始时2KB，随着需要可以增长到1GB。

**(P)rocessor**

表示逻辑处理器， 对 G 来说，P 相当于 CPU 核，G 只有绑定到 P(在 P 的 local runq 中)才能被调度。对 M 来说，P 提供了相关的执行环境(Context)，如内存分配状态(mcache)，任务队列(G)等，P 的数量决定了系统内最大可并行的 G 的数量（前提：物理 CPU 核数 >= P 的数量），P 的数量由用户设置的 GOMAXPROCS 决定，但是不论 GOMAXPROCS 设置为多大，P 的数量最大为 256。

Processor是对处理器（CPU核心）的抽象，表示逻辑处理器。它的主要作用是作为Goroutine和Machine Thread之间的中介，负责调度Goroutines。每个P都维护了一个本地的Goroutine队列，存储着等待执行的Goroutine。每一个P都维护着M的执行上下文，包括内存分配缓存、一些同步原语等。每个M都会与一个P关联起来，并执行该P的任务队列中的Goroutine。Golang运行时在程序启动时可以创建多个P对象，数量通常默认为物理核心数，但可以通过环境变量GOMAXPROCS进行调整。这里的P虽然表示逻辑处理器，但P并不执行任何代码，对G来说，P相当于CPU核，G需要被分配一个P才能被调度。 对M来说，P提供了相关的执行环境(Context)，如内存分配状态(mcache)，任务队列(G)等，只有将P和M绑定才能让P中G得以真实运行起来。

**(M)achine**

OS 线程抽象，代表着真正执行计算的资源，在绑定有效的 P 后，进入 schedule 循环；而 schedule 循环的机制大致是从 Global 队列、P 的 Local 队列以及 wait 队列中获取 G，切换到 G 的执行栈上并执行 G 的函数，调用 goexit 做清理工作并回到 M，如此反复。M 并不保留 G 状态，这是 G 可以跨 M 调度的基础，M 的数量是不定的，由 Go Runtime 调整，为了防止创建过多 OS 线程导致系统调度不过来，目前默认最大限制为 10000 个。

Machine Thread是与操作系统线程直接对应的实体。在Linux上，它对应于pthread。它是实际执行Goroutine的实体。很多人认为GOMAXPROCS可以限制系统线程的数量，但这是错误的，M是按需创建的，和GOMAXPROCS没有直接关系。M在绑定有效的P后，进入调度循环，而且M并不保留G状态，这是G可以跨M调度的基础。当M因为系统调用或锁竞争而阻塞时，它会与P分离，运行时可能会创建新的M（如果系统资源允许）来继续执行其他P的Goroutine队列。

**调度流程**

- 当一个G被创建时，它会被放入P的本地队列，如果P的本地队列已满，则放入全局队列中。
- 调度器选择一个P，并将其与一个M关联（如果M因为阻塞操作而释放了P，运行时会创建新的M或者从M缓存中获取）。
- M执行P的本地队列中的G。如果P的本地队列为空，优先从全局队列获取G，如果全局队列为空时则通过work stealing机制从其他P的本地队列偷取G。
- 当一个G开始执行时，它会使用关联的M执行，直到它执行完成或被阻塞或被sysmon抢占。
- 如果G被阻塞在某个system call操作上，那么不光G会阻塞，执行该G的M也会解绑P(实质是被sysmon抢走了)，与G一起进入sleep状态。如果此时有空闲的M，则P与其绑定继续执行其他G；如果没有空闲M，但仍然有其他G要去执行，那么就会创建一个新M。当阻塞在syscall上的G完成syscall调用后，G会尝试获取一个空闲的P执行，并放入到这个P的本地队列。如果获取不到P，那么这个线程M变成休眠状态，加入到空闲线程中，然后这个G会被放入全局队列中。
- 如果G被阻塞在某个channel操作或I/O操作上时，G会被放置到某个wait队列中，而M会尝试运行下一个runnable的G；如果此时没有runnable的G供M运行，那么M将解绑P，并进入sleep状态。当channel操作完成或I/O available，在wait队列中的G会被唤醒，标记为runnable，放入到某P的队列中，绑定一个M继续执行。

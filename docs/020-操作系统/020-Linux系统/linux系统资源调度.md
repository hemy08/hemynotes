# Linux系统的资源调度

- [Go语言的GPM模型 简书_(jianshu.com)](https://www.jianshu.com/p/504d9eaf0fd1)

Linux操作系统中的资源调度是基于进程的，同一进程中的线程共享这个进程中的所有资源，所以linux中的线程本质上是一种轻量级进程，同样被操作系统进行统一调度。而linux又将线程的实现分为两种：

- 用户级线程
    - 线程切换不需要转换到内核空间，节省了宝贵的内核空间
    - 调度算法可以是进程专用，由用户程序进行指定
    - 用户级线程实现和操作系统无关
    - <span style="color:rgb(255,0,0);font-weight:bold">系统调用阻塞，同一进程中一个线程阻塞和整个进程都阻塞了</span>
    - <span style="color:rgb(255,0,0);font-weight:bold">一个线程只能在一个cpu上获得执行</span>
- 内核级线程
    - 在多处理器上，内核可以调用同一进程中的多个线程同时工作
    - 如果一个进程中的一个线程阻塞了，其他线程仍然可以得到运行
    - 线程的切换代价太大，需要进程进入到内核态并且由内核切换

## 1.1 一对一调度

该模型实现简单，所有用户线程由系统调用，导致上下文切换成本高，用户线程的增加会给操作系统内核带来巨大压力

![](https://upload-images.jianshu.io/upload_images/13145841-32972991bfe6ddd9.png)


## 1.2 一对多

该模型虽然减少了内核线程的数量，但是用户线程无法参与到系统的CPU调度中，且与固定的内核线程绑定，对于用一个内核线程下的用户线程等于是串行，一旦一个用户线程阻塞，其他用户线程会无法调度。

![](https://upload-images.jianshu.io/upload_images/13145841-decb2c961149b11d.png)


## 多对多

模型中用户线程和内核线程非绑定，应用程序和系统共同进行CPU资源的调度，解决了之前模型的缺点，但是实现逻辑复杂。Golang使用的就是基于该模型的调度方案

![](https://upload-images.jianshu.io/upload_images/13145841-c79e4517daf55ac9.png)
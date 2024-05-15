# 003-Flynn分类法

Flynn分类法，也称为Flynn's Taxonomy，是一种用于分类计算机体系结构的框架。它基于指令流和数据流的多倍性特征将计算机系统分为四种基本类型：

[冯·诺依曼 体系结构](https://picx.zhimg.com/70/v2-59c127d4312d7e8c461ac5d2123c465b_1440w.avis?source=172ae18b&biz_tag=Post)


参考：

- [单指令流单数据流_百度百科 (baidu.com)](https://baike.baidu.com/item/%E5%8D%95%E6%8C%87%E4%BB%A4%E6%B5%81%E5%A4%9A%E6%95%B0%E6%8D%AE%E6%B5%81/257612)
- [单指令流多数据流_百度百科 (baidu.com)](https://baike.baidu.com/item/%E5%8D%95%E6%8C%87%E4%BB%A4%E6%B5%81%E5%A4%9A%E6%95%B0%E6%8D%AE%E6%B5%81/257612)
- [多指令流单数据流_百度百科 (baidu.com)](https://baike.baidu.com/item/%E5%A4%9A%E6%8C%87%E4%BB%A4%E6%B5%81%E5%8D%95%E6%95%B0%E6%8D%AE%E6%B5%81)
- [多指令流多数据流_百度百科 (baidu.com)](https://baike.baidu.com/item/%E5%A4%9A%E6%8C%87%E4%BB%A4%E6%B5%81%E5%A4%9A%E6%95%B0%E6%8D%AE%E6%B5%81)
- [指令流和数据流 CSDN](https://blog.csdn.net/weixin_69884785/article/details/130557771)
- [单指令流单数据流,多指令流多数据流 知乎](https://zhuanlan.zhihu.com/p/695889551)

## S1SD

单指令流单数据流机器（SISD Signle Instructions Stream Signle Data Stream) 

SISD机器是一种传统的串行计算机，它的硬件不支持任何形式的并行计算，所有的指令都是串行执行。并且在某个时钟周期内，CPU只能处理一个数据流。因此这种机器被称作单指令流单数据流机器。早期的计算机都是SISD机器。

每个指令部件每次仅译码一条指令，而且在执行时仅为操作部件提供一份数据。这种类型符合冯·诺伊曼结构。

以加法指令为例，单指令单数据（SISD）的CPU对加法指令译码后，执行部件先访问内存，取得第一个操作数；之后再一次访问内存，取得第二个操作数；随后才能进行求和运算。

## SIMD

单指令流多数据流机器（SIMD Signle Instructions Stream Multiple Data Stream)

SIMD是采用一个指令流处理多个数据流。这类机器在数字信号处理、图像处理，以及多媒体信息处理等领域非常有效。

这种计算机系统包含多个重复的运算处理单元，但仅存在唯一的指令部件。在运行过程中，指令部件从存储器中取出指令并译码，然后发往运算处理单元。各运算处理单元按照同一指令流的要求处理各自不同的数据。

以加法指令为例，单指令单数据（SISD）的CPU对加法指令译码后，执行部件先访问内存，取得第一个操作数；之后再一次访问内存，取得第二个操作数；随后才能进行求和运算。而在SIMD型的CPU中，指令译码后几个执行部件同时访问内存，一次性获得所有操作数进行运算。这个特点使SIMD特别适合于多媒体应用等数据密集型运算。

Intel 处理器实现的MMXTM、SSE (Streaming SIMD Extensions)、SSE2及SSE3扩展指令集，都能在单个时钟周期内处理多个数据单元。也就是说人们现在用的单核计算机基本上都厲于SIMD机器。

## MISD

多指令流单数据流机器（MISD Multiple Instructions Stream Signle Data Stream)

MISD是采用多个指令流来处理单个数据流。在实际情况中，采用多指令流处理多数据流才是更有效的方法，因此MISD只是作为理论模型出现，没有投入实际应用。

这种计算机系统的具体代表存在不同的看法。有些文献将指令流水线看成是多指令部件，故将流水线体系结构归并到这类计算机中；有些文献将容错系统也归到这一类。

## MIMD

多指令流多数据流机器（MIMD Multiple Instructions Stream Multiple Data Stream)

实现作业、任务、指令、数据各个级别全面并行执行的计算机系统。这样的系统拥有多个处理机，每个处理机具有独立的程序，每个程序为相应的处理器生成一个指令流，并处理各自不同的数据。分布式计算机系统基本上都属于多指令流多数据流系统。

MIMD机器可以同时执行多个指令流，这些指令流分别对不同数据流进行操作。最新的多核计算平台就属于MIMD的范畴，例如Intel和AMD的双核处理器。

于大多数并行计算机而言，多个处理单元都是根据不同的控制流程执行不同的操作，处理不同的数据，因此，它们被称作是多指令流多数据流计算机，即MIMD（MultipleInstructionMultipleData,MIMD）计算机。
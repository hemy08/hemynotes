# netstat命令详解

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-09-05</span>

Netstat 命令用于显示各种网络相关信息，如网络连接，路由表，接口状态(Interface Statistics)，masquerade 连接，多播成员 (Multicast Memberships) 等。

`netstat -s`命令，与`/proc/net/netstat`文件中内容应该是一致的，但是`/proc/net/netstat`文件的可读性较差，需要格式化才能显示。

## 一、命令格式： `netstat [-acCeFghilMnNoprstuvVwx][-A<网络类型>][--ip]`

### 1）usage

```
usage: netstat [-vWeenNcCF] [<Af>] -r         netstat {-V|--version|-h|--help}
       netstat [-vWnNcaeol] [<Socket> ...]
       netstat { [-vWeenNac] -I[<Iface>] | [-veenNac] -i | [-cnNe] -M | -s [-6tuw] } [delay]

```

### 2）option


```shell
usage: netstat [-vWeenNcCF] [<Af>] -r         netstat {-V|--version|-h|--help}
       netstat [-vWnNcaeol] [<Socket> ...]
       netstat { [-vWeenNac] -I[<Iface>] | [-veenNac] -i | [-cnNe] -M | -s [-6tuw] } [delay]

        -r, --route              display routing table
        -I, --interfaces=<Iface> display interface table for <Iface>
        -i, --interfaces         display interface table
        -g, --groups             display multicast group memberships
        -s, --statistics         display networking statistics (like SNMP)
        -M, --masquerade         display masqueraded connections

        -v, --verbose            be verbose
        -W, --wide               don't truncate IP addresses
        -n, --numeric            don't resolve names
        --numeric-hosts          don't resolve host names
        --numeric-ports          don't resolve port names
        --numeric-users          don't resolve user names
        -N, --symbolic           resolve hardware names
        -e, --extend             display other/more information
        -p, --programs           display PID/Program name for sockets
        -o, --timers             display timers
        -c, --continuous         continuous listing

        -l, --listening          display listening server sockets
        -a, --all                display all sockets (default: connected)
        -F, --fib                display Forwarding Information Base (default)
        -C, --cache              display routing cache instead of FIB
        -Z, --context            display SELinux security context for sockets

  <Socket>={-t|--tcp} {-u|--udp} {-U|--udplite} {-S|--sctp} {-w|--raw}
           {-x|--unix} --ax25 --ipx --netrom
  <AF>=Use '-6|-4' or '-A <af>' or '--<af>'; default: inet
  List of possible address families (which support routing):
    inet (DARPA Internet) inet6 (IPv6) ax25 (AMPR AX.25)
    netrom (AMPR NET/ROM) ipx (Novell IPX) ddp (Appletalk DDP)
    x25 (CCITT X.25)

```

| 选项 | 描述 |
| :- | :-|
| -a或--all | 显示所有连线中的Socket；
| -A<网络类型>或--<网络类型> | 列出该网络类型连线中的相关地址；
| -c或--continuous | 持续列出网络状态；
| -C或--cache | 显示路由器配置的快取信息；
| -e或--extend | 显示网络其他相关信息；
| -F或--fib | 显示FIB；
| -g或--groups | 显示多重广播功能群组组员名单；
| -h或--help | 在线帮助；
| -i或--interfaces | 显示网络界面信息表单；
| -l或--listening | 显示监控中的服务器的Socket；
| -M或--masquerade | 显示伪装的网络连线；
| -n或--numeric | 直接使用ip地址，而不通过域名服务器；
| -N或--netlink或--symbolic | 显示网络硬件外围设备的符号连接名称；
| -o或--timers | 显示计时器；
| -p或--programs | 显示正在使用Socket的程序识别码和程序名称；
| -r或--route | 显示Routing Table；
| -s或--statistice | 显示网络工作信息统计表；
| -t或--tcp | 显示TCP传输协议的连线状况；
| -u或--udp | 显示UDP传输协议的连线状况；
| -v或--verbose | 显示指令执行过程；
| -V或--version | 显示版本信息；
| -w或--raw | 显示RAW传输协议的连线状况；
| -x或--unix | 此参数的效果和指定"-A unix"参数相同；
| --ip或--inet | 此参数的效果和指定"-A inet"参数相同。

## 二、netstat 输出结果解析

netstat的输出结果可以分为两个部分：

- Active Internet connections，称为有源TCP连接，其中"Recv-Q"和"Send-Q"指%0A的是接收队列和发送队列。这些数字一般都应该是0。如果不是则表示软件包正在队列中堆积。这种情况只能在非常少的情况见到。
    - Proto：连接使用的协议
    - Recv-Q：单位是字节，是表示程序总共还有多少字节的数据没有从内核空间的套接字缓存拷贝到用户空间
    - Send-Q：单位是字节，表示远程主机还没有接收到的数据量。发送队列Send-Q不能很快的清零，可能是有应用向外发送数据包过快，或者是对方接收数据包不够快
    - Local Address：本地主机名和端口号
    - Foreign Address：远程主机名和端口号
    - State：链路状态，共有12种状态。

- Active UNIX domain sockets，称为有源Unix域套接口(和网络套接字一样，但是只能用于本机通信，性能可以提高一倍)。
    - Proto：连接使用的协议
    - RefCnt：表示连接到本套接口上的进程号
    - Type：显示套接字的类型
    - State：显示套接字当前的链路状态
    - I-Node：节点编号
    - Path：连接到套接字的其它进程使用的路径名


```shell
[root@izwz91quxhnlkan8kjak5hz proc]# netstat
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 localhost:ddi-tcp-1     localhost:51948         TIME_WAIT  
tcp        0      0 izwz91quxhnlkan:msg-icp 113.110.230.173:srcp    ESTABLISHED
tcp        0      0 izwz91quxhnlkan8k:57000 100.100.30.25:http      ESTABLISHED
...
Active UNIX domain sockets (w/o servers)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  3      [ ]         DGRAM                    7377     /run/systemd/notify
unix  2      [ ]         DGRAM                    7379     /run/systemd/cgroups-agent
unix  2      [ ]         DGRAM                    10206    /run/systemd/shutdownd
...
```

## 三、State链路状态：

- SYN: (同步序列编号,Synchronize Sequence Numbers)该标志仅在三次握手建立TCP连接时有效。表示一个新的TCP连接请求。
- ACK: (确认编号,Acknowledgement Number)是对TCP请求的确认标志,同时提示对端系统已经成功接收所有数据。
- FIN: (结束标志,FINish)用来结束一个TCP回话.但对应端口仍处于开放状态,准备接收后续数据。

| 状态 | 解释 |
| :- | :- |
| LISTEN | 监听TCP连接请求 <br>首先服务端需要打开一个socket进行监听，状态为 LISTEN，侦听来自远方TCP端口的连接请求 |
| SYN_SENT | 客户端发送SYN以请求连接之后，等待匹配的连接请求，此时状态为SYN_SENT <br>客户端通过应用程序调用connect进行active open，于是客户端tcp发送一个SYN以请求建立一个连接，之后状态置为 SYN_SENT，在发送连接请求后等待匹配的连接请求； |
| SYN_RECV | 服务端发出ACK确认客户端的 SYN,同时向客户端发送一个SYN等待对连接请求的确认. 之后状态置为SYN_RECV <br>服务端应发出ACK确认客户端的 SYN，同时自己向客户端发送一个SYN，之后状态置为，在收到和发送一个连接请求后等待对连接请求的确认；|
| ESTABLISHED | 连接已成功建立 <br>代表一个打开的连接，双方可以进行或已经在数据交互了， 代表一个打开的连接，数据可以传送给用户；|
| FIN_WAIT1 | 主动关闭(active close)端应用程序调用close，于是其TCP发出FIN请求主动关闭连接，之后进入FIN_WAIT1状态， 等待远程TCP的连接中断请求，或先前的连接中断请求的确认； |
| CLOSE_WAIT | 被动关闭(passive close)端TCP接到FIN后，就发出ACK以回应FIN请求(它的接收也作为文件结束符传递给上层应用程序)，并进入CLOSE_WAIT， 等待从本地用户发来的连接中断请求；|
| FIN_WAIT2 | 主动关闭端接到ACK后，就进入了 FIN_WAIT2。从远程TCP等待连接中断请求|
| LAST_ACK | 被动关闭端一段时间后，接收到文件结束符的应用程 序将调用CLOSE关闭连接。这导致它的TCP也发送一个 FIN,等待对方的ACK.就进入了LAST-ACK，等待原来发向远程TCP的连接中断请求的确认；|
| TIME_WAIT | 在主动关闭端接收到FIN后，TCP 就发送ACK包，并进入TIME-WAIT状态。等待足够的时间以确保远程TCP接收到连接中断请求的确认|
| CLOSING | 等待远程TCP对连接中断的确认|
| CLOSED | 被动关闭端在接受到ACK包后，就进入了closed的状态，连接结束，没有任何连接状态；|
| UNKNOWN | 未知的Socket状态|


## 四、sockets Type 套接字类型：

套接字(Socket)，就是对网络中不同主机上的应用进程之间进行双向通信的端点的抽象。一个套接字就是网络上进程通信的一端，提供了应用层进程利用网络协议交换数据的机制

| 类型 | 解释 |
| :- | :- |
| SOCK_DGRAM | 此套接字用于数据报(无连接)模式
| SOCK_STREAM | 流模式(连接)套接字
| SOCK_RAW | 此套接字用于RAW模式
| SOCK_RDM | 一种服务可靠性传递信息
| SOCK_SEQPACKET | 连续分组套接字
| SOCK_PACKET | RAW接口使用套接字
| UNKNOWN | 未知类型

## 五、nestat 常用命令：

| 命令 | 解释 |
| :- | :- |
| netstat -a | 列出所有连接的网络状况
| netstat -at | 列出`TCP`协议的连接
| netstat -au | 列出`UDP`协议的连接
| netstat -tnl | 只列出监听中的`TCP`连接
| netstat -tnpl | 只列出监听中的`TCP`连接及其进程编号、进程名称
| netstat -l | 只显示在监听的端口
| netstat -lt | 只显示在所有监听的`TCP`端口
| netstat -lu | 只显示在所有监听的`UDP`端口
| netstat -lx | 只显示在所有监听的`unix`端口
| netstat -p | 显示`PID`和进程名称
| netstat -pt | 显示所有`TCP`端口的`PID`和进程名称
| netstat -s | 显示网络统计信息
| netstat -rn | 显示路由信息
| netstat -i | 显示网络接口
| netstat -atnp &#124; grep ESTABLISHED | 只列出 active 状态的连接，active 状态的套接字连接用 "ESTABLISHED" 字段表示
| netstat -aple &#124; grep ssh | 查看ssh服务是否在运行
| netstat -n &#124; awk '/^tcp/ {++state[$NF]} END {for(key in state) print key,"\t",state[key]}' | 统计TCP各个连接状态的数量


```
[root@izwz91quxhnlkan8kjak5hz proc]# netstat -n | awk '/^tcp/ {++state[$NF]} END {for(key in state) print key,"\t",state[key]}'
ESTABLISHED      3
TIME_WAIT        2
// /proc/net/netstat文件格式化命令：cat /proc/net/netstat |  awk '(f==0) {name=$1; i=2; while ( i<=NF) {n[i] = $i; i++ }; 
// 通过grep匹配某个值，结果netstat命令统计出来的数据与/proc/net/netstat文件中的数据是一致的
f=1; next} (f==1){ i=2; while ( i<=NF){ printf "%s%s = %d\n", name, n[i], $i; i++}; f=0} '
[root@izwz91quxhnlkan8kjak5hz ~]#  cat /proc/net/netstat |  awk '(f==0) {name=$1; i=2; while ( i<=NF) {n[i] = $i; i++ }; f=1; next} (f==1){ i=2; while ( i<=NF){ printf "%s%s = %d\n", name, n[i], $i; i++}; f=0} ' | grep TCPSpuriousRTOs
TcpExt:TCPSpuriousRTOs = 1349
[root@izwz91quxhnlkan8kjak5hz net]# netstat -ts | grep TCPSpuriousRTOs
    TCPSpuriousRTOs: 1349
```


## 六、实例

### 1）列出所有端口 (包括监听和未监听的)

```shell
netstat -a     #列出所有端口
netstat -at    #列出所有tcp端口
netstat -au    #列出所有udp端口  
```

### 2）列出所有处于监听状态的 Sockets


```shell
netstat -l        #只显示监听端口
netstat -lt       #只列出所有监听 tcp 端口
netstat -lu       #只列出所有监听 udp 端口
netstat -lx       #只列出所有监听 UNIX 端口
```

### 3）显示每个协议的统计信息


```shell
netstat -s   #显示所有端口的统计信息
netstat -st   #显示TCP端口的统计信息
netstat -su   #显示UDP端口的统计信息
```

```shell
#**在netstat输出中显示 PID 和进程名称** 
netstat -pt
```

`netstat -p`可以与其它开关一起使用，就可以添加“PID/进程名称”到netstat输出中，这样debugging的时候可以很方便的发现特定端口运行的程序。

### 4）在netstat输出中不显示主机端口和用户名(host, port or user)

当你不想让主机，端口和用户名显示，使用`netstat -n`。将会使用数字代替那些名称。同样可以加速输出，因为不用进行比对查询。

```shell
netstat -an
```

如果只是不想让这三个名称中的一个被显示，使用以下命令:

```shell
netsat -a --numeric-ports
netsat -a --numeric-hosts
netsat -a --numeric-users
```

### 5）持续输出netstat信息


```shell
netstat -c   #每隔一秒输出网络信息
```

### 6）显示系统不支持的地址族(Address Families)


```shell
netstat --verbose
```

在输出的末尾，会有如下的信息：

```shell
netstat: no support for 'AF IPX' on this system.
netstat: no support for 'AF AX25' on this system.
netstat: no support for 'AF X25' on this system.
netstat: no support for 'AF NETROM' on this system.
```

### 7）显示核心路由信息

```shell
netstat -r
```

使用`netstat -rn`显示数字格式，不查询主机名称。

### 8）找出程序运行的端口

并不是所有的进程都能找到，没有权限的会不显示，使用 root 权限查看所有的信息。

```shell
netstat -ap | grep ssh
```

找出运行在指定端口的进程：

```shell
netstat -an | grep :80
```

### 9）通过端口找进程ID

```shell
netstat -anp|grep 8081 | grep LISTEN|awk '{printf $7}'|cut -d/ -f1
```

### 10）显示网络接口列表

```shell
netstat -i
```

显示详细信息，像是ifconfig使用`netstat -ie`。

### 11）IP和TCP分析

查看连接某服务端口最多的的IP地址：

```shell
netstat -ntu | grep :80 | awk '{print $5}' | cut -d: -f1 | awk '{++ip[$1]} END {for(i in ip) print ip[i],"\t",i}' | sort -nr
```

TCP各种状态列表：

```shell
netstat -nt | grep -e 127.0.0.1 -e 0.0.0.0 -e ::: -v | awk '/^tcp/ {++state[$NF]} END {for(i in state) print i,"\t",state[i]}'
```

查看phpcgi进程数，如果接近预设值，说明不够用，需要增加：

```shell
netstat -anpo | grep "php-cgi" | wc -l
```
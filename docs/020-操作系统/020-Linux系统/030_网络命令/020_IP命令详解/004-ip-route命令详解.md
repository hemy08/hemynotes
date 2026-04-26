# ip route命令详解

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-06-27</span>

原文链接 [https://www.kancloud.cn/chunyu/php_basic_knowledge/2137339](https://www.kancloud.cn/chunyu/php_basic_knowledge/2137339)

ip route：用于管理静态路由表。
linux 系统中，可以自定义从 1－252个路由表。其中，linux系统维护了4个路由表：

- 0#表： 系统保留表
- 253#表： defulte table 没特别指定的默认路由都放在改表
- 254#表： main table 没指明路由表的所有路由放在该表
- 255#表： local table 保存本地接口地址，广播地址、NAT地址 由系统维护，用户不得更改

路由表的查看可以通过`ip route list table table_number [table_name]`命令。路由表序号和表名的对应关系在 `/etc/iproute2/rt_tables` 文件中，可手动编辑，路由表添加完毕即时生效。

## ip route 命令格式说明


```
Usage: ip route { list | flush } SELECTOR
       ip route save SELECTOR
       ip route restore
       ip route showdump
       ip route get ADDRESS [ from ADDRESS iif STRING ]
                            [ oif STRING ]  [ tos TOS ]
                            [ mark NUMBER ]
       ip route { add | del | change | append | replace } ROUTE
SELECTOR := [ root PREFIX ] [ match PREFIX ] [ exact PREFIX ]
            [ table TABLE_ID ] [ proto RTPROTO ]
            [ type TYPE ] [ scope SCOPE ]
ROUTE := NODE_SPEC [ INFO_SPEC ]
NODE_SPEC := [ TYPE ] PREFIX [ tos TOS ]
             [ table TABLE_ID ] [ proto RTPROTO ]
             [ scope SCOPE ] [ metric METRIC ]
INFO_SPEC := NH OPTIONS FLAGS [ nexthop NH ]...
NH := [ via ADDRESS ] [ dev STRING ] [ weight NUMBER ] NHFLAGS
OPTIONS := FLAGS [ mtu NUMBER ] [ advmss NUMBER ]
           [ rtt TIME ] [ rttvar TIME ] [reordering NUMBER ]
           [ window NUMBER ] [ cwnd NUMBER ] [ initcwnd NUMBER ]
           [ ssthresh NUMBER ] [ realms REALM ] [ src ADDRESS ]
           [ rto_min TIME ] [ hoplimit NUMBER ] [ initrwnd NUMBER ]
           [ features FEATURES ] [ quickack BOOL ] [ congctl NAME ]
           [ expires TIME ]
TYPE := { unicast | local | broadcast | multicast | throw |
          unreachable | prohibit | blackhole | nat }
TABLE_ID := [ local | main | default | all | NUMBER ]
SCOPE := [ host | link | global | NUMBER ]
NHFLAGS := [ onlink | pervasive ]
RTPROTO := [ kernel | boot | static | NUMBER ]
TIME := NUMBER[s|ms]
BOOL := [1|0]
FEATURES := ecn
```

## ip route add/change/replace

**option：**

- to TYPE PREFIX (default)：路由的目标前缀。如果省略TYPE，则ip采用unicast类型。上面列出了其他类型的值。前缀是一个IP或IPv6地址，后跟斜杠和前缀长度。如果前缀的长度丢失，ip将采用全长主机路由。还有一个特殊的前缀默认值-相当于IP 0/0或IPv6:：/0。
- tos TOS：服务类型（TOS）密钥。这个密钥没有相关的掩码，最长的匹配被理解为：首先，比较路由和包的TOS。如果它们不相等，则分组仍然可以匹配具有零TOS的路由。TOS是8位十六进制数或/etc/iproute2/rt_dsfield中的标识符。
- metric ：跳数，该条路由记录的质量，一般情况下，如果有多条到达相同目的地的路由记录，路由器会采用metric值小的那条路由
- table TABLEID：要将此路由添加到的表。TABLEID可以是文件/etc/iproute2/rt_tables中的数字或字符串。如果省略此参数，ip将采用主表，但本地、广播和nat路由除外，默认情况下，这些路由将放入本地表中
- dev NAME：输出设备名称
- via ADDRESS：下一跳路由器的地址。 实际上，此字段的含义取决于路由类型。 对于普通的单播路由，它要么是真正的下一跳路由器，要么是以BSD兼容模式安装的直接路由，它可以是接口的本地地址。 对于NAT路由，它是已转换IP目标块的第一个地址
- src ADDRESS：发送到路由前缀所覆盖的目的地时首选的源地址
- realm REALMID：此路由被分配到的领域。REALMID可以是/etc/iproute2/rt_realms文件中的数字或字符串。
- mtu MTU/mtu lock MTU：到达目的地的路径上的MTU。 如果未使用修饰符锁定，则由于路径MTU发现，内核可能会更新MTU。 如果使用了修饰符锁定，则将不尝试任何路径MTU发现，在IPv4情况下，所有数据包将在没有DF位的情况下发送，或者将其分片到IPv6的MTU
- window NUMBER：TCP播发到这些目的地的最大窗口，以字节为单位。它限制了允许TCP对等方发送给我们的最大数据突发
- rtt TIME：初始RTT（“往返时间”）估算值。 如果未指定后缀，则这些单位是直接传递到路由代码的原始值，以保持与先前版本的兼容性。 否则，如果使用后缀s，sec或secs来指定秒数，而使用ms，msec或msecs的后缀来指定毫秒。
- rttvar TIME (2.3.15+ only)：初始RTT方差估算值。 与上面的rtt一样指定值
- rto_min TIME (2.6.23+ only)：与此目标通信时要使用的最小TCP重新传输超时。值的指定与上面的rtt相同
- ssthresh NUMBER (2.3.15+ only)：初始慢启动阈值的估计值
- cwnd NUMBER (2.3.15+ only)：锁定标志，如果不使用锁定标志，则忽略该选项
- initcwnd NUMBER (2.5.70+ only)：到此目标的连接的初始拥塞窗口大小。 实际窗口大小是该值乘以相同连接的MSS（``最大段大小''）。 默认值为零，表示使用RFC2414中指定的值。
- initrwnd NUMBER (2.6.33+ only)：到此目标的连接的初始接收窗口大小。 实际窗口大小是此值乘以连接的MSS。 默认值为零，表示使用慢启动值。
- features FEATURES (3.18+only)：启用或禁用每路由功能。此时唯一可用的特性是ecn，它可以在启动到给定目标网络的连接时启用显式拥塞通知。当响应来自给定网络的连接请求时，即使net.ipv4.tcp_ecn sysctl设置为0
- congctl NAME/congctl lock NAME (3.20+ only)：仅针对给定的目的地设置特定的TCP拥塞控制算法。 如果未指定，Linux将保留当前的全局默认TCP拥塞控制算法或应用程序中的一种。 如果未使用修饰符锁定，则应用程序仍可能会覆盖该目的地的建议拥塞控制算法。 如果使用了修饰符锁，则不允许应用程序覆盖该目的地的指定拥塞控制算法，因此将强制/保证使用建议的算法
- advmss NUMBER (2.3.15+ only)：在建立TCP连接时向这些目标播发的MSS（“最大段大小”）。如果没有给定，Linux将使用从第一跳设备MTU计算的默认值
- reordering NUMBER (2.3.15+ only)：到此目的地的路径上的最大重新排序。 如果未给出，则Linux使用通过sysctl变量net/ipv4/tcp_reordering选择的值
- nexthop NEXTHOP：多路径路由的下一跳。 NEXTHOP是一个复杂值，其语法类似于顶级参数列表：
    - via ADDRESS：下一跳路由
    - dev NAME：输出设备名称
    - weight NUMBER：是多路径路由的此元素的权重，反映其相对带宽或质量
- scope SCOPE_VAL：路由前缀所覆盖的目的地范围。 SCOPE_VAL可以是数字/etc/iproute2/rt_scopes中的字符串。 如果省略此参数，则ip假定所有网关单播路由的作用域是全局范围，直接单播和广播路由的作用域链接以及本地路由的作用域主机
- protocol RTPROTO：该路由的路由协议标识符。 RTPROTO可以是文件/ etc / iproute2 / rt_protos中的数字或字符串。如果未提供路由协议ID，则ip会采用协议引导方式（即假定路由是由不了解自己在做什么的人添加的）。 几个协议值具有固定的解释。
    - redirect： 路由是由于ICMP重定向而安装的
    - kernel：路由是在自动配置期间由内核安装的
    - boot：路由是在启动过程中安装的。如果路由守护进程启动，它将清除所有这些守护进程
    - static：该路由由管理员安装，以覆盖动态路由。 路由守护程序将尊重它们，甚至可能将它们通告给其对等端。
    - ra：路由是通过路由器发现协议安装的
    

| 命令 | 解释 |
| :- | :- |
| ip route add default via 192.168.1.1 | 设置系统默认路由 |
| ip route add 192.168.4.0/24 via 192.168.0.254 dev eth0 | 设置192.168.4.0网段的网关为192.168.0.254,数据走eth0接口 |
| ip route add default via 192.168.0.254 dev eth0 | 设置默认网关为192.168.0.254 |
| ip route add default via 192.168.1.1 table 1 | 在一号表中添加默认路由为192.168.1.1 |
| ip route add 192.168.0.0/24 via 192.168.1.2 table 1 | 在一号表中添加一条到192.168.0.0网段的路由为192.168.1.2 |
| ip route add prohibit 209.10.26.51 | 设置请求的目的地不可达的路由 |
| ip route add prohibit 209.10.26.51 from 192.168.99.35 | 假设您不想阻止所有用户访问此特定主机，则可以使用该from选项，阻止了源IP 192.168.99.35到达209.10.26.51 |
| ip route change default via 192.168.99.113 dev eth0 | 更改默认路由。此操作等同于先删除，后新增 |


## ip route get

此命令获取到目标的单个路由，并按照内核所看到的方式打印其内容。
此操作不等同于ip route show。 ip routeshow会显示现有路线，而get解析它们并在必要时创建新克隆。基本上，get相当于沿着此路径发送数据包。如果没有给出iif参数，内核将创建一个路由，以将数据包输出到请求的目的地。这相当于用后续的ip路由ls缓存ping目标，但是实际上没有发送任何数据包。使用iif参数，内核假装一个数据包从这个接口到达，并搜索一条路径来转发数据包

**option：**

- to ADDRESS (default)：目的地址
- from ADDRESS：源地址
- tos TOS：服务类型
- iif NAME：此数据包预期从中到达的设备
- oif NAME：强制将此数据包路由到的输出设备
- connected：如果未给出源地址（选项from），则重新查找源设置为从第一次查找收到的首选地址的路由。 如果使用策略路由，则可能是其他路由

| 查看命令 | 解释 |
| :- | :- |
| ip route get 169.254.0.0/16 | 获取到目标的单个路由，并按照内核所看到的方式打印其内容 |

## ip route delete

| 查看命令 | 解释 |
| :- | :- |
| ip route del 192.168.4.0/24 | 删除192.168.4.0网段的网关 |
| ip route del default | 删除默认路由 |
| ip route delete 192.168.1.0/24 dev eth0 | 删除路由 |


## ip route save

将路由表信息保存到标准输出。该命令的行为类似于ip route show，除了输出是适合传递给ip route restore的原始数据外。

## ip route restore

从stdin恢复路由表信息 该命令希望读取从ip route save返回的数据流。 它将尝试完全还原保存时的路由表信息，因此必须先完成流中信息的任何转换（例如设备索引）。 任何现有路线均保持不变。 表中已经存在的数据流中指定的任何路由都将被忽略。
ip route restore

## ip route flush

该flush选项与ip route一起使用时，将清空路由表或删除特定目标的路由

| 命令 | 解释 |
| :- | :- |
| ip route flush 10.38.0.0/16 | 删除特定路由 |
| ip route flush table main | 清空路由表 |

## Route type 解释:

- unicast：由路由前缀覆盖的目的地址的真实路径
- unreachable：目的路由无法到达。丢弃数据包并生成ICMP消息主机不可访问。本地发件人收到一个EHOSTUNREACH错误。
- blackhole：目的路由无法到达。数据包被悄悄丢弃。本地发件人收到EINVAL错误。
- prohibit：目的路由无法到达。数据包将被丢弃，并生成管理上禁止的ICMP消息通信。 本地发件人收到EACCES错误。
- local：目的地已分配给此主机。数据包被环回并在本地传递
- broadcast：目的路由是广播地址。数据包作为链接广播发送
- throw：与策略规则一起使用的特殊控制路径。 如果选择了这样的路由，则会在未找到路由的情况下终止此表中的查找。 如果没有策略路由，则等同于路由表中没有路由。 数据包被丢弃，并生成ICMP消息net unreachable。 本地发件人收到ENETUNREACH错误
- nat：一条特殊的NAT路由。 前缀所覆盖的目的地被认为是虚拟（或外部）地址，在转发之前需要将其转换为真实（或内部）地址。 使用属性via选择要转换为的地址
- anycast：未分配给此主机的路由地址，它们主要等效于本地，只是有一个区别：这些地址用作任何数据包的源地址时都是无效的。
- multicast：一种用于多播路由的特殊类型。 它在常规路由表中不存在。

## 运行实例：


```
// 查看本地路由表
// 此输出中的第一个字段告诉我们该路由是针对该计算机本地托管的广播地址还是IP地址或范围。
//随后的字段会通知我们目标可通过哪个设备到达，并且特别是（在此表中）内核已添加了这些路由，作为建立IP层接口的一部分
[root@izwz91quxhnlkan8kjak5hz net]# ip route show table local
broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1 
local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1 
local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1 
broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1 

// 添加请求目的不可达的路由
[root@masq-gw]# ip route add prohibit 209.10.26.51
[root@tristan]# ssh 209.10.26.51
ssh: connect to address 209.10.26.51 port 22: No route to host
[root@masq-gw]# tcpdump -nnq -i eth2
tcpdump: listening on eth2
22:13:13.740406 192.168.99.35.51973 &gt; 209.10.26.51.22: tcp 0 (DF)
22:13:13.740714 192.168.99.254 &gt; 192.168.99.35: icmp: host 209.10.26.51 unreachable - admin prohibited filter [tos 0xc0]
```
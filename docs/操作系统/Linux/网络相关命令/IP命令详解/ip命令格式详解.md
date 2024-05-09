# ip命令格式详解

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-06-27</span>

原文链接 [https://www.kancloud.cn/chunyu/php_basic_knowledge/2137335](https://www.kancloud.cn/chunyu/php_basic_knowledge/2137335)

## 命令格式： ip [ OPTIONS ] OBJECT { COMMAND | help }


```
OBJECT := { link | address | addrlabel | route | rule | neigh | ntable |
                   tunnel | tuntap | maddress | mroute | mrule | monitor | xfrm |
                   netns | l2tp | macsec | tcp_metrics | token }
OPTIONS := { -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] |
            -h[uman-readable] | -iec |
            -f[amily] { inet | inet6 | ipx | dnet | bridge | link } |
            -4 | -6 | -I | -D | -B | -0 |
            -l[oops] { maximum-addr-flush-attempts } |
            -o[neline] | -t[imestamp] | -ts[hort] | -b[atch] [filename] |
            -rc[vbuf] [size] | -n[etns] name | -a[ll] }
```


### object：

- link：网络设备
- address：设备上的协议（IP或IPv6）地址
- addrlabel：协议地址选择的标签配置
- route：路由表条目
- rule：路由策略数据库中的规则

### option：

- -h：输出人类可读的统计信息和后缀
- -b：从提供的文件或标准输入中读取命令并调用它们。第一次故障将导致ip终止
- -force：不要在批处理模式下终止ip。如果在执行命令期间出现任何错误，应用程序返回代码将为非零
- -s：输出更多信息。如果该选项出现两次或更多，则信息量会增加。通常，信息是统计信息或一些时间值
- -d：输出详细信息
- -l：指定在放弃之前“ ip地址刷新”逻辑将尝试的最大循环数。 默认值为10。0表示循环，直到删除所有地址
- -f：指定要使用的协议族。 协议系列标识符可以是inet，inet6，bridge，ipx，dnet或链接之一。 如果不存在此选项，则从其他参数中猜测协议族。 如果剩下的命令行没有提供足够的信息来猜测家族，ip会退回到默认值，通常是inet或任意值。 链接是一个特殊的系列标识符，表示不涉及网络协议。
- -4：指定使用的网络层协议是IPv4协议
- -6：指定使用的网络层协议是IPv6协议
- -B：指定使用的网桥
- -o：输出信息每条记录输出一行，即使内容较多也不换行显示
- -r：显示主机时，不使用IP地址，而使用主机的域名
- -n：将ip切换到指定的网络命名空间NETNS。实际上，它只是将命令`ip netns exec NETNS ip [ OPTIONS ] OBJECT { COMMAND | help }` 简化成`ip -n[etns] NETNS [ OPTIONS ] OBJECT { COMMAND | help }`
- -a：对所有对象执行指定的命令，这取决于命令是否支持此选项
- -t：使用监视器选项时显示当前时间
- -ts：与-timestamp类似，但使用较短的格式
- -rs：设置netlink套接字接收缓冲区的大小，默认为1MB
- -iec：以IEC单位打印人类可读率（例如1Ki = 1024）
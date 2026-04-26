# nslookup命令详解

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-06-27</span>

nslookup命令主要用来查询域名的DNS信息。

nslookup拥有“交互模式”和“非交互模式”。在“交互模式”下，用户可以向域名服务器查询各类主机、域名的信息，或者输出域名中的主机列表。而在“非交互模式”下，用户可以针对一个主机或域名来查询对应的信息.

**交互模式：** 仅输入nslookup命令，不加任何参数，即可直接进入交互模式，此时nslookup会连接到默认的域名服务器（即/etc/resolv.conf的第一个dns地址）。或者输入nslookup -nameserver/ip。
**非交互模式：** 直接输入nslookup 域名。
**命令格式：** nslookup [参数] [域名]

**option：**

- sil ：不显示任何警告信息
- exit：退出命令
- server：指定解析域名的服务器地址
- set type=soa：设置查询域名授权起始信息
- set type=a：设置查询域名A记录
- set type=mx：设置查询域名邮件交换记录

## 安装：

yum search nslookup没找到对应的安装包

使用命令`yum  provides  */nslookup`   就可以找到提供nslookup命令的软件包了：bind-utils

安装命令：`yum install -y bind-utils`


```shell
[root@izwz91quxhnlkan8kjak5hz ~]# yum  provides  */nslookup
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile
base/7/x86_64/filelists_db                                                                                                                                                                                                         | 7.2 MB  00:00:00     
epel/x86_64/filelists_db                                                                                                                                                                                                           |  12 MB  00:00:00     
extras/7/x86_64/filelists_db                                                                                                                                                                                                       | 224 kB  00:00:00     
updates/7/x86_64/filelists_db                                                                                                                                                                                                      | 2.1 MB  00:00:00     
1:bash-completion-extras-2.1-11.el7.noarch : Additional programmable completions for Bash
源    ：epel
匹配来源：
文件名    ：/usr/share/bash-completion/completions/nslookup

32:bind-utils-9.11.4-26.P2.el7.x86_64 : Utilities for querying DNS name servers
源    ：base
匹配来源：
文件名    ：/usr/bin/nslookup

32:bind-utils-9.11.4-26.P2.el7_9.2.x86_64 : Utilities for querying DNS name servers
源    ：updates
匹配来源：
文件名    ：/usr/bin/nslookup

zsh-5.0.2-34.el7_8.2.x86_64 : Powerful interactive shell
源    ：base
匹配来源：
文件名    ：/usr/share/zsh/5.0.2/functions/nslookup
```

## 实例


```
// 交互模式下，查看www.baidu.com的域名DNS信息
[root@izwz91quxhnlkan8kjak5hz ~]# nslookup
> set type=soa
> www.baidu.com
Server:         100.100.2.138
Address:        100.100.2.138#53

Non-authoritative answer:
www.baidu.com   canonical name = www.a.shifen.com.

Authoritative answers can be found from:
a.shifen.com
        origin = ns1.a.shifen.com
        mail addr = baidu_dns_master.baidu.com
        serial = 2101090002
        refresh = 5
        retry = 5
        expire = 2592000
        minimum = 3600
> server www.baidu.com
Default server: www.baidu.com
Address: 14.215.177.39#53
Default server: www.baidu.com
Address: 14.215.177.38#53
> 
//非交互模式下，查看www.baidu.com的域名DNS信息
[root@izwz91quxhnlkan8kjak5hz ~]# nslookup www.baidu.com
Server:         100.100.2.138
Address:        100.100.2.138#53

Non-authoritative answer:
www.baidu.com   canonical name = www.a.shifen.com.
Name:   www.a.shifen.com
Address: 14.215.177.38
Name:   www.a.shifen.com
Address: 14.215.177.39

[root@izwz91quxhnlkan8kjak5hz ~]# 
```
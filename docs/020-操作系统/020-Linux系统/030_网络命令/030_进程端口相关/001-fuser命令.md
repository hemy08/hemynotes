# fuser命令

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-09-05</span>

fuser 命令显示在 Linux 中使用指定文件或文件系统的进程的 PID。

可以按如下方式安装它：

```shell
$ sudo apt-get install psmisc [在Debian、Ubuntu和Mint上] 
$ sudo yum install psmisc [在RHEL/CentOS/Fedora和Rocky Linux/AlmaLinux上] 
$ sudo emerge -a sys-apps/psmisc [在Gentoo Linux上] 
$ sudo pacman -S psmisc [在Arch Linux上] 
$ sudo zypper install psmisc [在OpenSUSE上]    
```

您可以通过运行以下命令（指定端口）找到在特定端口上侦听的进程/服务。

```shell
$ fuser 80/tcp
```

然后像这样使用ps 命令使用 PID号查找进程名称。

```shell
$ ps -p 2053 -o comm=
$ ps -p 2381 -o comm=
```

## 一、help


```shell
Usage: fuser [-fIMuvw] [-a|-s] [-4|-6] [-c|-m|-n SPACE]
             [-k [-i] [-SIGNAL]] NAME...
       fuser -l
       fuser -V
Show which processes use the named files, sockets, or filesystems.

  -a,--all              display unused files too
  -i,--interactive      ask before killing (ignored without -k)
  -I,--inode            use always inodes to compare files
  -k,--kill             kill processes accessing the named file
  -l,--list-signals     list available signal names
  -m,--mount            show all processes using the named filesystems or
                        block device
  -M,--ismountpoint     fulfill request only if NAME is a mount point
  -n,--namespace SPACE  search in this name space (file, udp, or tcp)
  -s,--silent           silent operation
  -SIGNAL               send this signal instead of SIGKILL
  -u,--user             display user IDs
  -v,--verbose          verbose output
  -w,--writeonly        kill only processes with write access
  -V,--version          display version information
  -4,--ipv4             search IPv4 sockets only
  -6,--ipv6             search IPv6 sockets only
  -                     reset options

  udp/tcp names: [local_port][,[rmt_host][,[rmt_port]]]

```
# tcpdump工具使用

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-06-27</span>

## 示例

### 1、通用抓包命令

```shell
tcpdump -v -n -i any -s 0 -w {文件名}
```


### 2、指定目标地址，本端网卡


```shell
tcpdump -v -n -i [网卡接口] -s 0 -w /opt/eSight.cap host [对端IP]
```



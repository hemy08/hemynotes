# curl命令参数

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-06-26</span>

| 参数 | 描述 |
|  -------- |  -------- |
| -a | --`append` 上传文件时，附加到目标文件 | 
| -A | --`user-agent <string>`设置用户代理发送给服务器 <br>--`anyauth` 可以使用“任何”身份验证方法 | 
| -b | --`cookie <name=string/file> `cookie字符串或文件读取位置 <br>--`basic` 使用HTTP基本验证 | 
| -B | --`use-ascii` 使用ASCII <br>文本传输 | 
| -c | --`cookie-jar <file>` 操作结束后把cookie写入到这个文件中 | 
| -C | --`continue-at <offset> `断点续转 | 
| -d | --`data <data>` HTTP POST方式传送数据 <br>--`data-ascii <data>` 以ascii的方式post数据 <br>--`data-binary <data>` 以二进制的方式post数据 <br>--`negotiate` 使用HTTP身份验证 <br>--`digest` 使用数字身份验证 <br>--`disable-eprt` 禁止使用EPRT或LPRT <br>--`disable-epsv` 禁止使用EPSV | 
| -D | --`dump-header <file>`把header信息写入到该文件中 <br>--`egd-file <file>`为随机数据(SSL)设置EGD socket路径 <br>--`tcp-nodelay` 使用TCP_NODELAY选项 | 
| -e | --`referer` 来源网址 | 
| -E | --`cert <cert[:passwd]>`客户端证书文件和密码 (SSL) <br>--`cert-type <type>`证书文件类型 (DER/PEM/ENG) (SSL) <br>--`key <key>`私钥文件名 (SSL) <br>--`key-type <type>`私钥文件类型 (DER/PEM/ENG) (SSL) <br>--`pass <pass>`私钥密码 (SSL) <br>--`engine <eng>`加密引擎使用 (SSL). "--engine list" for list <br>--`cacert <file>`CA证书 (SSL) <br>--`capath <directory>`CA目录 (made using c_rehash) to verify peer against (SSL) <br>--`ciphers <list> `SSL密码 <br>--`compressed` 要求返回是压缩的形势 (using deflate or gzip) <br>--`connect-timeout <seconds>`设置最大请求时间 <br>--`create-dirs` 建立本地目录的目录层次结构 <br>--`crlf` 上传是把LF转变成CRLF | 
| -f | --`fail` 连接失败时不显示http错误 <br>--`ftp-create-dirs` 如果远程目录不存在，创建远程目录 <br>--`ftp-method` [multicwd/nocwd/singlecwd] 控制CWD的使用 <br>--`ftp-pasv` 使用 PASV/EPSV 代替端口 <br>--`ftp-skip-pasv-ip` 使用PASV的时候,忽略该IP地址 <br>--`ftp-ssl` 尝试用 SSL/TLS 来进行ftp数据传输 <br>--`ftp-ssl-reqd` 要求用 SSL/TLS 来进行ftp数据传输 | 
| -F | --`form <name=content>`模拟http表单提交数据 <br>--`form-string <name=string>`模拟http表单提交数据 | 
| -g | --`globoff` 禁用网址序列和范围使用{}和[] | 
| -G | --`get` 以get的方式来发送数据 | 
| -h | --`help` 帮助 | 
| -H | --`header <line>`自定义头信息传递给服务器 <br>--`ignore-content-length` 忽略的HTTP头信息的长度 | 
| -i | --`include` 输出时包括protocol头信息 | 
| -I | --`head` 只显示文档信息 | 
| -j | --`junk-session-cookies`忽略会话Cookie <br>--界面`<interface>`指定网络接口/地址使用 <br>--`krb4 <level>` 启用与指定的安全级别krb4 | 
| -j | --`junk-session-cookies` 读取文件进忽略session cookie <br>--`interface <interface>`使用指定网络接口/地址 <br>--`krb4 <level>`使用指定安全级别的krb4 | 
| -k | --`insecure` 允许不使用证书到SSL站点 | 
| -K | --`config` 指定的配置文件读取 | 
| -l | --`list-only` 列出ftp目录下的文件名称 <br>--`limit-rate <rate>`设置传输速度 <br>--`local-port <NUM>`强制使用本地端口号 | 
| -m | --`max-time <seconds>`设置最大传输时间 <br>--`max-redirs <num>`设置最大读取的目录数 <br>--`max-filesize <bytes>` 设置最大下载的文件总量 | 
| -M | --`manual` 显示全手动 | 
| -n | --`netrc` 从netrc文件中读取用户名和密码 <br>--`netrc-optional` 使用 .netrc 或者 URL来覆盖-n <br>--`ntlm` 使用 HTTP NTLM 身份验证 | 
| -N | --`no-buffer` 禁用缓冲输出 | 
| -o | --`output` 把输出写到该文件中 | 
| -O | --`remote-name` 把输出写到该文件中，保留远程文件的文件名 | 
| -p | --`proxytunnel` 使用HTTP代理 <br>--`proxy-anyaut`h 选择任一代理身份验证方法 <br>--`proxy-basic` 在代理上使用基本身份验证 <br>--`proxy-digest` 在代理上使用数字身份验证 <br>--`proxy-ntlm` 在代理上使用ntlm身份验证 | 
| -P | --`ftp-port <address>` 使用端口地址，而不是使用PASV | 
| -Q | --`quote <cmd>`文件传输前，发送命令到服务器 | 
| -r | --`range <range>`检索来自HTTP <br>1.1或FTP服务器字节范围  <br>--`range-file` 读取（SSL）的随机文件 | 
| -R | --`remote-time` 在本地生成文件时，保留远程文件时间 <br>--`retry <num>`传输出现问题时，重试的次数 <br>--`retry-delay <seconds>`传输出现问题时，设置重试间隔时间 <br>--`retry-max-time <seconds>`传输出现问题时，设置最大重试时间 | 
| -s | --`silent`静音模式。不输出任何东西 | 
| -S | --`show-error` 显示错误 <br>--`socks4 <host[:port]>` 用socks4代理给定主机和端口 <br>--`socks5 <host[:port]>` 用socks5代理给定主机和端口 <br>--`stderr <file>`| 
| -t | --`telnet-option <OPT=val>`Telnet选项设置 <br>--`trace <file>`对指定文件进行debug <br>--`trace-ascii <file> Like` --跟踪但没有hex输出 <br>--`trace-time` 跟踪/详细输出时，添加时间戳 | 
| -T | --`upload-file <file>`上传文件 <br>--`url <URL>`Spet URL to work with | 
| -u | --`user <user[:password]>`设置服务器的用户和密码 | 
| -U | --`proxy-user <user[:password]>`设置代理用户名和密码 | 
| -v | --`verbose` | 
| -V | --`version` 显示版本信息 | 
| -w | --`write-out` [format]什么输出完成后 | 
| -x | --`proxy <host[:port]>`在给定的端口上使用HTTP代理 | 
| -X | --`request <command>`指定什么命令 | 
| -y | --`speed-time` 放弃限速所要的时间。默认为30 | 
| -Y | --`speed-limit` 停止传输速度的限制，速度时间'秒 | 
| -z | --`time-cond` 传送时间设置 | 
| -0 | --`http1.0` 使用HTTP 1.0 | 
| -1 | --`tlsv1` 使用TLSv1（SSL） | 
| -2 | --`sslv2` 使用SSLv2的（SSL） | 
| -3 | --`sslv3` 使用的SSLv3（SSL） <br>--`3p-quote` like -Q for the source URL for 3rd party transfer <br>--`3p-url` 使用url，进行第三方传送 <br>--`3p-user` 使用用户名和密码，进行第三方传送 | 
| -4 | --`ipv4` 使用IP4 | 
| -6 | --`ipv6` 使用IP6 | 
| -# | --`progress-bar` 用进度条显示当前的传送状态 | 
| -a | --`append` 上传文件时，附加到目标文件 | 
| -A | --`user-agent <string>` 设置用户代理发送给服务器 <br>--anyauth 可以使用“任何”身份验证方法 | 
| -b | --`cookie <name=string/file>`cookie字符串或文件读取位置 <br>--basic 使用HTTP基本验证 | 
|  |  | 
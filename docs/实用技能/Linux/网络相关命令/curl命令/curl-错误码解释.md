# curl 命令错误码解释

<details>
<summary style="color:rgb(0,0,255)"><b>libcurl 代码库对错误码的定义</b></summary>
<blockcode><pre><code>

```
typedef enum {
  CURLE_OK = 0,
  CURLE_UNSUPPORTED_PROTOCOL,    /* 1 */
  CURLE_FAILED_INIT,             /* 2 */
  CURLE_URL_MALFORMAT,           /* 3 */
  CURLE_NOT_BUILT_IN,            /* 4 - [was obsoleted in August 2007 for
                                    7.17.0, reused in April 2011 for 7.21.5] */
  CURLE_COULDNT_RESOLVE_PROXY,   /* 5 */
  CURLE_COULDNT_RESOLVE_HOST,    /* 6 */
  CURLE_COULDNT_CONNECT,         /* 7 */
  CURLE_WEIRD_SERVER_REPLY,      /* 8 */
  CURLE_REMOTE_ACCESS_DENIED,    /* 9 a service was denied by the server
                                    due to lack of access - when login fails
                                    this is not returned. */
  CURLE_FTP_ACCEPT_FAILED,       /* 10 - [was obsoleted in April 2006 for
                                    7.15.4, reused in Dec 2011 for 7.24.0]*/
  CURLE_FTP_WEIRD_PASS_REPLY,    /* 11 */
  CURLE_FTP_ACCEPT_TIMEOUT,      /* 12 - timeout occurred accepting server
                                    [was obsoleted in August 2007 for 7.17.0,
                                    reused in Dec 2011 for 7.24.0]*/
  CURLE_FTP_WEIRD_PASV_REPLY,    /* 13 */
  CURLE_FTP_WEIRD_227_FORMAT,    /* 14 */
  CURLE_FTP_CANT_GET_HOST,       /* 15 */
  CURLE_HTTP2,                   /* 16 - A problem in the http2 framing layer.
                                    [was obsoleted in August 2007 for 7.17.0,
                                    reused in July 2014 for 7.38.0] */
  CURLE_FTP_COULDNT_SET_TYPE,    /* 17 */
  CURLE_PARTIAL_FILE,            /* 18 */
  CURLE_FTP_COULDNT_RETR_FILE,   /* 19 */
  CURLE_OBSOLETE20,              /* 20 - NOT USED */
  CURLE_QUOTE_ERROR,             /* 21 - quote command failure */
  CURLE_HTTP_RETURNED_ERROR,     /* 22 */
  CURLE_WRITE_ERROR,             /* 23 */
  CURLE_OBSOLETE24,              /* 24 - NOT USED */
  CURLE_UPLOAD_FAILED,           /* 25 - failed upload "command" */
  CURLE_READ_ERROR,              /* 26 - couldn't open/read from file */
  CURLE_OUT_OF_MEMORY,           /* 27 */
  /* Note: CURLE_OUT_OF_MEMORY may sometimes indicate a conversion error
           instead of a memory allocation error if CURL_DOES_CONVERSIONS
           is defined
  */
  CURLE_OPERATION_TIMEDOUT,      /* 28 - the timeout time was reached */
  CURLE_OBSOLETE29,              /* 29 - NOT USED */
  CURLE_FTP_PORT_FAILED,         /* 30 - FTP PORT operation failed */
  CURLE_FTP_COULDNT_USE_REST,    /* 31 - the REST command failed */
  CURLE_OBSOLETE32,              /* 32 - NOT USED */
  CURLE_RANGE_ERROR,             /* 33 - RANGE "command" didn't work */
  CURLE_HTTP_POST_ERROR,         /* 34 */
  CURLE_SSL_CONNECT_ERROR,       /* 35 - wrong when connecting with SSL */
  CURLE_BAD_DOWNLOAD_RESUME,     /* 36 - couldn't resume download */
  CURLE_FILE_COULDNT_READ_FILE,  /* 37 */
  CURLE_LDAP_CANNOT_BIND,        /* 38 */
  CURLE_LDAP_SEARCH_FAILED,      /* 39 */
  CURLE_OBSOLETE40,              /* 40 - NOT USED */
  CURLE_FUNCTION_NOT_FOUND,      /* 41 - NOT USED starting with 7.53.0 */
  CURLE_ABORTED_BY_CALLBACK,     /* 42 */
  CURLE_BAD_FUNCTION_ARGUMENT,   /* 43 */
  CURLE_OBSOLETE44,              /* 44 - NOT USED */
  CURLE_INTERFACE_FAILED,        /* 45 - CURLOPT_INTERFACE failed */
  CURLE_OBSOLETE46,              /* 46 - NOT USED */
  CURLE_TOO_MANY_REDIRECTS,      /* 47 - catch endless re-direct loops */
  CURLE_UNKNOWN_OPTION,          /* 48 - User specified an unknown option */
  CURLE_SETOPT_OPTION_SYNTAX,    /* 49 - Malformed setopt option */
  CURLE_OBSOLETE50,              /* 50 - NOT USED */
  CURLE_OBSOLETE51,              /* 51 - NOT USED */
  CURLE_GOT_NOTHING,             /* 52 - when this is a specific error */
  CURLE_SSL_ENGINE_NOTFOUND,     /* 53 - SSL crypto engine not found */
  CURLE_SSL_ENGINE_SETFAILED,    /* 54 - can not set SSL crypto engine as
                                    default */
  CURLE_SEND_ERROR,              /* 55 - failed sending network data */
  CURLE_RECV_ERROR,              /* 56 - failure in receiving network data */
  CURLE_OBSOLETE57,              /* 57 - NOT IN USE */
  CURLE_SSL_CERTPROBLEM,         /* 58 - problem with the local certificate */
  CURLE_SSL_CIPHER,              /* 59 - couldn't use specified cipher */
  CURLE_PEER_FAILED_VERIFICATION, /* 60 - peer's certificate or fingerprint
                                     wasn't verified fine */
  CURLE_BAD_CONTENT_ENCODING,    /* 61 - Unrecognized/bad encoding */
  CURLE_LDAP_INVALID_URL,        /* 62 - Invalid LDAP URL */
  CURLE_FILESIZE_EXCEEDED,       /* 63 - Maximum file size exceeded */
  CURLE_USE_SSL_FAILED,          /* 64 - Requested FTP SSL level failed */
  CURLE_SEND_FAIL_REWIND,        /* 65 - Sending the data requires a rewind
                                    that failed */
  CURLE_SSL_ENGINE_INITFAILED,   /* 66 - failed to initialise ENGINE */
  CURLE_LOGIN_DENIED,            /* 67 - user, password or similar was not
                                    accepted and we failed to login */
  CURLE_TFTP_NOTFOUND,           /* 68 - file not found on server */
  CURLE_TFTP_PERM,               /* 69 - permission problem on server */
  CURLE_REMOTE_DISK_FULL,        /* 70 - out of disk space on server */
  CURLE_TFTP_ILLEGAL,            /* 71 - Illegal TFTP operation */
  CURLE_TFTP_UNKNOWNID,          /* 72 - Unknown transfer ID */
  CURLE_REMOTE_FILE_EXISTS,      /* 73 - File already exists */
  CURLE_TFTP_NOSUCHUSER,         /* 74 - No such user */
  CURLE_CONV_FAILED,             /* 75 - conversion failed */
  CURLE_CONV_REQD,               /* 76 - caller must register conversion
                                    callbacks using curl_easy_setopt options
                                    CURLOPT_CONV_FROM_NETWORK_FUNCTION,
                                    CURLOPT_CONV_TO_NETWORK_FUNCTION, and
                                    CURLOPT_CONV_FROM_UTF8_FUNCTION */
  CURLE_SSL_CACERT_BADFILE,      /* 77 - could not load CACERT file, missing
                                    or wrong format */
  CURLE_REMOTE_FILE_NOT_FOUND,   /* 78 - remote file not found */
  CURLE_SSH,                     /* 79 - error from the SSH layer, somewhat
                                    generic so the error message will be of
                                    interest when this has happened */

  CURLE_SSL_SHUTDOWN_FAILED,     /* 80 - Failed to shut down the SSL
                                    connection */
  CURLE_AGAIN,                   /* 81 - socket is not ready for send/recv,
                                    wait till it's ready and try again (Added
                                    in 7.18.2) */
  CURLE_SSL_CRL_BADFILE,         /* 82 - could not load CRL file, missing or
                                    wrong format (Added in 7.19.0) */
  CURLE_SSL_ISSUER_ERROR,        /* 83 - Issuer check failed.  (Added in
                                    7.19.0) */
  CURLE_FTP_PRET_FAILED,         /* 84 - a PRET command failed */
  CURLE_RTSP_CSEQ_ERROR,         /* 85 - mismatch of RTSP CSeq numbers */
  CURLE_RTSP_SESSION_ERROR,      /* 86 - mismatch of RTSP Session Ids */
  CURLE_FTP_BAD_FILE_LIST,       /* 87 - unable to parse FTP file list */
  CURLE_CHUNK_FAILED,            /* 88 - chunk callback reported error */
  CURLE_NO_CONNECTION_AVAILABLE, /* 89 - No connection available, the
                                    session will be queued */
  CURLE_SSL_PINNEDPUBKEYNOTMATCH, /* 90 - specified pinned public key did not
                                     match */
  CURLE_SSL_INVALIDCERTSTATUS,   /* 91 - invalid certificate status */
  CURLE_HTTP2_STREAM,            /* 92 - stream error in HTTP/2 framing layer
                                    */
  CURLE_RECURSIVE_API_CALL,      /* 93 - an api function was called from
                                    inside a callback */
  CURLE_AUTH_ERROR,              /* 94 - an authentication function returned an
                                    error */
  CURLE_HTTP3,                   /* 95 - An HTTP/3 layer problem */
  CURLE_QUIC_CONNECT_ERROR,      /* 96 - QUIC connection error */
  CURLE_PROXY,                   /* 97 - proxy handshake error */
  CURLE_SSL_CLIENTCERT,          /* 98 - client-side certificate required */
  CURL_LAST /* never use! */
} CURLcode;
```

</code></pre></blockcode></details>


| <div style="width:50pt;font-size:15pt"><center>状态码</div> | <div style="font-size:15pt"><center>状态原因</div> | <div style="font-size:15pt"><center>解释</div> | 
|  -- | -- | -- |
| 0 | 正常访问 |  | 
| 1 | 错误的协议 | 未支持的协议。此版cURL 不支持这一协议。 | 
| 2 | 初始化代码失败 | 初始化失败。 | 
| 3 | URL格式不正确 | URL 格式错误。语法不正确。 | 
| 4 | 请求协议错误 |  | 
| 5 | 无法解析代理 | 无法解析代理。无法解析给定代理主机。 | 
| 6 | 无法解析主机地址 | 无法解析主机。无法解析给定的远程主机。 | 
| 7 | 无法连接到主机 | 无法连接到主机。 | 
| 8 | 远程服务器不可用 | FTP 非正常的服务器应答。cURL 无法解析服务器发送的数据。 | 
| 9 | 访问资源错误 | FTP 访问被拒绝。服务器拒绝登入或无法获取您想要的特定资源或目录。最有可 | 
| 11 | FTP密码错误 | FTP 非正常的PASS 回复。cURL 无法解析发送到PASS 请求的应答。 | 
| 13 | 结果错误 | FTP 非正常的的PASV 应答，cURL 无法解析发送到PASV 请求的应答。 | 
| 14 | FTP回应PASV命令 | FTP 非正常的227格式。cURL 无法解析服务器发送的227行。 | 
| 15 | 内部故障 | FTP 无法连接到主机。无法解析在227行中获取的主机IP。 | 
| 17 | 设置传输模式为二进制 | FTP 无法设定为二进制传输。无法改变传输方式到二进制。 | 
| 18 | 文件传输短或大于预期 | 部分文件。只有部分文件被传输。 | 
| 19 | RETR命令传输完成 | FTP 不能下载/访问给定的文件， RETR (或类似)命令失败。 | 
| 21 | 命令成功完成 | FTP quote 错误。quote 命令从服务器返回错误。 | 
| 22 | 返回正常 | HTTP 找不到网页。找不到所请求的URL 或返回另一个HTTP 400或以上错误。 | 
| 23 | 数据写入失败 | 写入错误。cURL 无法向本地文件系统或类似目的写入数据。 | 
| 25 | 无法启动上传 | FTP 无法STOR 文件。服务器拒绝了用于FTP 上传的STOR 操作。 | 
| 26 | 回调错误 | 读错误。各类读取问题。 | 
| 27 | 内存分配请求失败 | 内存不足。内存分配请求失败。 | 
| 28 | 访问超时 | 操作超时。到达指定的超时期限条件。 | 
| 30 | FTP端口错误 | FTP PORT 失败。PORT 命令失败。并非所有的FTP 服务器支持PORT 命令，请 | 
| 31 | FTP错误 | FTP 无法使用REST 命令。REST 命令失败。此命令用来恢复的FTP 传输。 | 
| 33 | 不支持请求 | HTTP range 错误。range "命令"不起作用。 | 
| 34 | 内部发生错误 | HTTP POST 错误。内部POST 请求产生错误。 | 
| 35 | SSL/TLS握手失败 | SSL 连接错误。SSL 握手失败。 | 
| 36 | 下载无法恢复 | FTP 续传损坏。不能继续早些时候被中止的下载。 | 
| 37 | 文件权限错误 | 文件无法读取。无法打开文件。权限问题？ | 
| 38 | LDAP可没有约束力 | LDAP 无法绑定。LDAP 绑定(bind)操作失败。 | 
| 39 | LDAP搜索失败 | LDAP 搜索失败。 | 
| 41 | 函数没有找到 | 功能无法找到。无法找到必要的LDAP 功能。 | 
| 42 | 中止的回调 | 由回调终止。应用程序告知cURL 终止运作。 | 
| 43 | 内部错误 | 内部错误。由一个不正确参数调用了功能。 | 
| 45 | 接口错误 | 接口错误。指定的外发接口无法使用。 | 
| 47 | 过多的重定向 | 过多的重定向。cURL 达到了跟随重定向设定的最大限额跟 | 
| 48 | 无法识别选项 | 指定了未知TELNET 选项。 | 
| 49 | TELNET格式错误 | 不合式的telnet 选项。 | 
| 51 | 远程服务器的SSL证书 | peer 的SSL 证书或SSH 的MD5指纹没有确定。 | 
| 52 | 服务器无返回内容 | 服务器无任何应答，该情况在此处被认为是一个错误。 | 
| 53 | 加密引擎未找到 | 找不到SSL 加密引擎。 | 
| 54 | 设定默认SSL加密失败 | 无法将SSL 加密引擎设置为默认。 | 
| 55 | 无法发送网络数据 | 发送网络数据失败。 | 
| 56 | 衰竭接收网络数据 | 在接收网络数据时失败。 | 
| 57 |  | 当前未使用 | 
| 58 | 本地客户端证书 | 本地证书有问题。 | 
| 59 | 无法使用密码 | 无法使用指定的SSL 密码。 | 
| 60 | 凭证无法验证 | peer 证书无法被已知的CA 证书验证。 | 
| 61 | 无法识别的传输编码 | 无法辨识的传输编码。 | 
| 62 | 无效的LDAP URL | 无效的LDAP URL。 | 
| 63 | 文件超过最大大小 | 超过最大文件尺寸。 | 
| 64 | FTP失败 | 要求的FTP 的SSL 水平失败。 | 
| 65 | 倒带操作失败 | 发送此数据需要的回卷(rewind)失败。 | 
| 66 | SSL引擎失败 | 初始化SSL 引擎失败。 | 
| 67 | 服务器拒绝登录 | 用户名、密码或类似的信息未被接受，cURL 登录失败。 | 
| 68 | 未找到文件 | 在TFTP 服务器上找不到文件。 | 
| 69 | 无权限 | TFTP 服务器权限有问题。 | 
| 70 | 超出服务器磁盘空间 | TFTP 服务器磁盘空间不足。 | 
| 71 | 非法TFTP操作 | 非法的TFTP 操作。 | 
| 72 | 未知TFTP传输的ID | 未知TFTP 传输编号(ID)。 | 
| 73 | 文件已经存在 | 文件已存在(TFTP) 。 | 
| 74 | 错误TFTP服务器 | 无此用户(TFTP) 。 | 
| 75 | 字符转换失败 | 字符转换失败。 | 
| 76 | 必须记录回调 | 需要字符转换功能。 | 
| 77 | CA证书权限 | 读SSL 证书出现问题(路径？访问权限？ ) 。 | 
| 78 | URL中引用资源不存在 | URL 中引用的资源不存在。 | 
| 79 | 错误发生在SSH会话 | SSH 会话期间发生一个未知错误。 | 
| 80 | 无法关闭SSL连接 | 未能关闭SSL 连接。 | 
| 81 | 服务未准备 |  | 
| 82 | 无法载入CRL文件 | 无法加载CRL 文件，丢失或格式不正确(在7.19.0版中增加) 。 | 
| 83 | 发行人检查失败 | 签发检查失败(在7.19.0版中增加) 。 | 
| 84 | PRET命令失败。 | FTP服务器根本不理解PRET命令或不支持给定的参数。使用CURLOPT_CUSTOMREQUEST时要小心，在PASV之前也会使用PRET CMD发送自定义LIST命令。 |
| 85 | RTSP CSeq号码不匹配。 |  |
| 86 | RTSP会话标识符不匹配。 |  |
| 87 | 无法解析FTP文件列表（在FTP通配符下载期间）。 |  |
| 88 | 块回调报告错误。 |  |
| 89 | 没有可用的连接，会话将排队 | 仅供内部使用，libcurl永远不会返回） |
| 90 | 无法匹配CURLOPT_PINNEDPUBLICKEY指定的固定密钥。 |  |
| 91 | 当询问CURLOPT_SSL_VERIFYSTATUS时，状态返回失败。 |  |
| 92 | HTTP / 2成帧层中的流错误。 |  |
| 93 | 从回调内部调用API函数。 |  |
| 94 | 身份验证函数返回错误 |  |
| 95 | 一个HTTP/3层的问题 |  |
| 96 | QUIC连接错误 |  |
| 97 | 代理握手错误 |  |
| 98 | 需要客户端证书 |  |
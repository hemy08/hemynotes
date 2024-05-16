# openssl生成证书步骤

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2017-06-27</span>

生成一个私钥，用于生成CA证书：


```
openssl genrsa -out ca.key 2048
```

生成CA证书：


```
openssl req -x509 -new -nodes -key ./ca.key -subj "/CN=guoxze.com" -days 100 -out ca.crt
```

生成服务端证书的步骤如下：

生成一个私钥：


```
openssl genrsa -out server.key 2048
```

生成服务端证书CSR签名请求：


```
openssl req -new -key ./server.key -subj "/CN=server" -out server.csr
```

使用CA证书签发服务端证书：


```
openssl x509 -req -in ./server.csr -CA ./ca.crt -CAkey ./ca.key -CAcreateserial -out server.crt -days 100
```

// 生成客户端证书


```
openssl genrsa -out client.key 2048

openssl req -new -key ./client.key -subj "/CN=client" -out client.csr

openssl x509 -req -in ./client.csr -CA ./ca.crt -CAkey ./ca.key -CAcreateserial -out client.crt -days 100
```


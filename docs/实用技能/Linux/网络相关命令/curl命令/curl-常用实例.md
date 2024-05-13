# 常用curl实例

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2021-07-31</span>

### 1. 抓取页面内容到一个文件中

```
[root@krlcgcms01 mytest]# curl -o home.html  http://blog.51yip.com 
[root@krlcgcms01 mytest]# curl -o home.html  http://blog.51yip.com
```

### 2. 用-O（大写的）

用-O（大写的），后面的url要具体到某个文件，不然抓不下来。我们还可以用正则来抓取东西

```
[root@krlcgcms01 mytest]# curl -O 
[root@krlcgcms01 mytest]# curl -O
```

### 3. 保存cookie信息

模拟表单信息，模拟登录，保存cookie信息

```
[root@krlcgcms01 mytest]# curl -c ./cookie_c.txt -F log=aaaa -F pwd=****** http://blog.51yip.com/wp-login.PHP 
[root@krlcgcms01 mytest]# curl -c ./cookie_c.txt -F log=aaaa -F pwd=****** http://blog.51yip.com/wp-login.php
```

### 4. 保存头信息

模拟表单信息，模拟登录，保存头信息

```
[root@krlcgcms01 mytest]# curl -D ./cookie_D.txt -F log=aaaa -F pwd=****** http://blog.51yip.com/wp-login.php 
[root@krlcgcms01 mytest]# curl -D ./cookie_D.txt -F log=aaaa -F pwd=****** http://blog.51yip.com/wp-login.php
```

-c\(小写\)产生的cookie和-D里面的cookie是不一样的。

### 5. 使用cookie文件

```
[root@krlcgcms01 mytest]# curl -b ./cookie_c.txt  http://blog.51yip.com/wp-admin 
[root@krlcgcms01 mytest]# curl -b ./cookie_c.txt  http://blog.51yip.com/wp-admin
```

### 6. 断点续传，-C(大写的)

```
[root@krlcgcms01 mytest]# curl -C -O
```

### 7. 传送数据

传送数据,最好用登录页面测试，因为你传值过去后，curl回抓数据，你可以看到你传值有没有成功

```
[root@krlcgcms01 mytest]# curl -d log=aaaa  http://blog.51yip.com/wp-login.php 
[root@krlcgcms01 mytest]# curl -d log=aaaa  http://blog.51yip.com/wp-login.php
```

### 8. 显示抓取错误

下面这个例子，很清楚的表明了。

```
[root@krlcgcms01 mytest]# curl -f http://blog.51yip.com/asdf 
curl: (22) The requested URL returned error: 404 
[root@krlcgcms01 mytest]# curl http://blog.51yip.com/asdf 
<HTML><HEAD><TITLE>404,not found</TITLE> 
。。。。。。。。。。。。 
[root@krlcgcms01 mytest]# curl -f http://blog.51yip.com/asdf 
curl: (22) The requested URL returned error: 404 
[root@krlcgcms01 mytest]# curl http://blog.51yip.com/asdf 
<HTML><HEAD><TITLE>404,not found</TITLE> 
。。。。。。。。。。。。
```

### 9. 伪造来源地址

有的网站会判断，请求来源地址。

```
[root@krlcgcms01 mytest]# curl -e http://localhost http://blog.51yip.com/wp-login.php 
[root@krlcgcms01 mytest]# curl -e http://localhost http://blog.51yip.com/wp-login.php
```

### 10. 用代理

当我们经常用curl去搞人家东西的时候，人家会把你的IP给屏蔽掉的,这个时候,我们可以用代理

```
[root@krlcgcms01 mytest]# curl -x 24.10.28.84:32779 -o home.html http://blog.51yip.com 
[root@krlcgcms01 mytest]# curl -x 24.10.28.84:32779 -o home.html http://blog.51yip.com
```

### 11. 分段下载

比较大的东西，我们可以分段下载

```
[root@krlcgcms01 mytest]# curl -r 0-100 -o img.part1 http://blog.51yip.com/wp- 
content/uploads/2010/09/compare_varnish.jpg 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
100   101  100   101    0     0    105      0 --:--:-- --:--:-- --:--:--     0 
[root@krlcgcms01 mytest]# curl -r 100-200 -o img.part2 http://blog.51yip.com/wp- 
content/uploads/2010/09/compare_varnish.jpg 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
100   101  100   101    0     0     57      0  0:00:01  0:00:01 --:--:--     0 
[root@krlcgcms01 mytest]# curl -r 200- -o img.part3 http://blog.51yip.com/wp- 
content/uploads/2010/09/compare_varnish.jpg 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
100  104k  100  104k    0     0  52793      0  0:00:02  0:00:02 --:--:-- 88961 
[root@krlcgcms01 mytest]# ls |grep part | xargs du -sh 
4.0K    one.part1 
112K    three.part3 
4.0K    two.part2 
[root@krlcgcms01 mytest]# curl -r 0-100 -o img.part1 http://blog.51yip.com/wp- 
content/uploads/2010/09/compare_varnish.jpg 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
100   101  100   101    0     0    105      0 --:--:-- --:--:-- --:--:--     0 
[root@krlcgcms01 mytest]# curl -r 100-200 -o img.part2 http://blog.51yip.com/wp- 
content/uploads/2010/09/compare_varnish.jpg 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
100   101  100   101    0     0     57      0  0:00:01  0:00:01 --:--:--     0 
[root@krlcgcms01 mytest]# curl -r 200- -o img.part3 http://blog.51yip.com/wp- 
content/uploads/2010/09/compare_varnish.jpg 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
100  104k  100  104k    0     0  52793      0  0:00:02  0:00:02 --:--:-- 88961 
[root@krlcgcms01 mytest]# ls |grep part | xargs du -sh 
4.0K    one.part1 
112K    three.part3 
4.0K    two.part2
```

用的时候，把他们cat一下就OK了,cat img.part\* \>img.jpg

### 12. 不会显示下载进度信息

```
[root@krlcgcms01 mytest]# curl -s -o aaa.jpg 
```

### 13. 显示下载进度条

```
[root@krlcgcms01 mytest]# curl -# -O  
######################################################################## 100.0%
```

### 14. 通过ftp下载文件

```
[zhangy@BlackGhost ~]$ curl -u 用户名:密码 -O http://blog.51yip.com/demo/curtain/bbstudy_files/style.css 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
101  1934  101  1934    0     0   3184      0 --:--:-- --:--:-- --:--:--  7136 
[zhangy@BlackGhost ~]$ curl -u 用户名:密码 -O http://blog.51yip.com/demo/curtain/bbstudy_files/style.css 
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current 
Dload  Upload   Total   Spent    Left  Speed 
101  1934  101  1934    0     0   3184      0 --:--:-- --:--:-- --:--:--  7136
```

或者用下面的方式


```
[zhangy@BlackGhost ~]$ curl -O ftp://用户名:密码@ip:port/demo/curtain/bbstudy_files/style.css 
[zhangy@BlackGhost ~]$ curl -O ftp://用户名:密码@ip:port/demo/curtain/bbstudy_files/style.css
```

### 15. 通过ftp上传

```
[zhangy@BlackGhost ~]$ curl -T test.sql ftp://用户名:密码@ip:port/demo/curtain/bbstudy_files/ 
[zhangy@BlackGhost ~]$ curl -T test.sql ftp://用户名:密码@ip:port/demo/curtain/bbstudy_files/
```

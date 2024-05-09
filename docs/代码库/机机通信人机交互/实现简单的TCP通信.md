# 实现TCP通信客户端和服务端

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-08-29</span>

## 一、Server端实现

=== "Go语言"
 
    ```Go
    //Server.go
    package main
    
    import (
        "fmt"
        "net"
        "os"
    )
    
    func main(){
        //服务端在本机8888端口建立tcp监听
        listener,err :=net.Listen("tcp","127.0.0.1:8888")
        ServerHandleError(err,"net.listen")
    
        for {
            //循环接入所有客户端得到专线连接
            conn,e := listener.Accept()
            ServerHandleError(e,"listener.accept")
            //开辟独立协程与该客聊天
            go ChatWith(conn)
        }
    }
    
    func ServerHandleError(err error,when string) {
        if err != nil {
            fmt.Println(err, when)
            os.Exit(1)
        }
    }
    
    //在conn网络专线中与客户端对话
    func ChatWith(conn net.Conn){
        //创建消息缓冲区
        buffer := make([]byte, 1024)
        for {
            ///---一个完整的消息回合
            //读取客户端发来的消息放入缓冲区
            n,err := conn.Read(buffer)
            ServerHandleError(err,"conn.read buffer")
    
            //转化为字符串输出
            clientMsg := string(buffer[0:n])
            fmt.Printf("收到消息",conn.RemoteAddr(),clientMsg)
    
            //回复客户端消息
            if clientMsg != "im off" {
                conn.Write([]byte("已读:"+clientMsg))
            } else {
                conn.Write([]byte("bye"))
                break
            }
        }
        conn.Close()
        fmt.Printf("客户端断开连接",conn.RemoteAddr())
    }
    ```

=== "C语言"

    ```c
    #include <stdio.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <errno.h>
    #include <unistd.h>
    #include <string.h>
    #include <sys/types.h>
    #include <arpa/inet.h>
    #include <netinet/in.h>

    #define _PORT_ 9999
    #define _BACKLOG_ 10

    int main()
    {
        int sock=socket(AF_INET,SOCK_STREAM,0);
        if(sock<0)
        {
            printf("socket()\n");
        }
        struct sockaddr_in server_socket;
        struct sockaddr_in socket;
        bzero(&server_socket,sizeof(server_socket));
        server_socket.sin_family=AF_INET;
        server_socket.sin_addr.s_addr=htonl(INADDR_ANY);
        server_socket.sin_port=htons(_PORT_);
        if(bind(sock,(struct sockaddr*)&server_socket,sizeof(struct sockaddr_in))<0)
        {
            printf("bind()\n");
            close(sock);
            return 1;
        }
        if(listen(sock,_BACKLOG_)<0)
        {
            printf("listen()\n");
            close(sock);
            return 2;
        }
        printf("success\n");
        for(;;)
        {
            socklen_t len=0;
            int client_sock=accept(sock,(struct sockaddr*)&socket,&len);
            if(client_sock<0)
            {
                printf("accept()\n");
                return 3;
            }
            char buf_ip[INET_ADDRSTRLEN];
            memset(buf_ip,'\0',sizeof(buf_ip));
            inet_ntop(AF_INET,&socket.sin_addr,buf_ip,sizeof(buf_ip));
            printf("get connect\n");
            
            while(1)
            {
                char buf[1024];
                memset(buf,'\0',sizeof(buf));
                read(client_sock,buf,sizeof(buf));
                
                printf("client:# %s\n",buf);
                printf("server:$ ");
                
                memset(buf,'\0',sizeof(buf));
                fgets(buf,sizeof(buf),stdin);
                buf[strlen(buf)-1]='\0';
                if(strncasecmp(buf,"quit",4)==0)
                {
                    printf("quit\n");
                    break;
                }
                write(client_sock,buf,strlen(buf)+1);
                printf("wait...\n");
            }
            close(client_sock);
        }
        close(sock);
        return 0;
    }
    ```

## 二、Client端实现

=== "Go语言"

    ```go
    //Client.go
    package main
    
    import (
        "bufio"
        "fmt"
        "net"
        "os"
    )
    
    func ClientHandleError(err error, when string){
        if err != nil {
            fmt.Println(err, when)
            os.Exit(1)
        }
    }
    
    func main(){
        //拨号远程地址，简历tcp连接
        conn, err := net.Dial("tcp","127.0.0.1:8888")
        ClientHandleError(err, "client conn error")
    
        //预先准备消息缓冲区
        buffer := make([]byte,1024)
    
        //准备命令行标准输入
        reader := bufio.NewReader(os.Stdin)
        
        for {
            lineBytes,_,_ := reader.ReadLine()
            conn.Write(lineBytes)
            n,err := conn.Read(buffer)
            ClientHandleError(err, "client read error")
            
            serverMsg := string(buffer[0:n])
            fmt.Printf("服务端msg",serverMsg)
            if serverMsg == "bye" {
                break
            }
        }
    }
    ```


=== "C语言"

    ```c
    #include <strings.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stdio.h>
    #include <sys/types.h>          /* See NOTES */
    #include <sys/socket.h>
    #include <netinet/ip.h>
    #include <unistd.h>
    #include <arpa/inet.h>
    #include <pthread.h>
    
    void *recv_data(void *arg)
    {
        int sockfd = *(int *)arg;
        char s[64] = {0};
        while(1)
        {
            int ret = read(sockfd, s, 64);
            if(ret < 0)
            {
                perror("read");
                return NULL;
            }
            printf("%s\n", s);
            memset(s, 0, 64);
        }
    }
    
    int main(int argc, char *argv[])
    {
        int sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if(sockfd == -1)
        {
            perror("socket");
            return -1;
        }
        
        pthread_t pid;
        pthread_create(&pid, NULL, recv_data, (void *)&sockfd);
        pthread_detach(pid);
    
        struct sockaddr_in ser;
        ser.sin_family = AF_INET;
        ser.sin_port = htons(11111);
        //ser.sin_addr.s_addr = inet_addr("0.0.0.0");
        ser.sin_addr.s_addr = htonl(INADDR_ANY);
        
        int ret = connect(sockfd, (struct sockaddr *)&ser, sizeof(ser));
        if(ret == -1)
        {
            perror("connect");
            return -1;
        }
        
        char buf[64];
        while(1)
        {
            fgets(buf, 64, stdin);
            buf[strlen(buf)-1] = '\0';
            write(sockfd, buf, 64);
            
            if(strcmp(buf, "time") == 0)
            {
                char data[64];
                read(sockfd, data, 64);
                printf(">>:%s\n", data);
                memset(buf, 0, 64);
                memset(data, 0, 64); 
            } else if(strncmp(buf, "get", 3) == 0) {
                char str[64];
                while(read(sockfd, str, 64) != 0) {
                    if(strcmp(str, "over") == 0) {
                        memset(str, 0, 64);        
                        break;
                    }
                    printf(">>:%s\n", str);
                    memset(buf, 0, 64);
                    memset(str, 0, 64); 
                }
            } else {	
                char arr[64] = {0};
                read(sockfd, arr, 64);
                printf(">>:%s\n", arr);
                memset(buf, 0, 64);
                memset(arr, 0, 64); 
            }
        }
        close(sockfd);
        return 0;
    }
    ```

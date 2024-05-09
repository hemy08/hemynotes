# 各类语言的HelloWorld实现

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-08-29</span>

!!! Example "脚本语言实现Hello world"

    === "NodeJs"
        ```js
        console.log("Hello World");
        ```

    === "Python"
        ```python
        #!/usr/bin/python3

        print("Hello, World!")
        ```

    === "Ruby"
        ```ruby
        #!/usr/bin/ruby
        puts "Hello World!";
        ```
!!! Example "后端开发语言实现HelloWorld"

    === "C"
        ```c
        #include <stdio.h>
        
        int main()
        {
            /* 我的第一个 C 程序 */
            printf("Hello, World! \n");
        
            return 0;
        }
        ```

    === "C++"
        ```cpp
        #include <iostream>
        using namespace std;
        int main()
        {
            cout << "Hello, world!" << endl;
            return 0;
        }
        ```

    === "Go"
        ```go
        package main

        import "fmt"

        func main() {
            fmt.Println("Hello, World!")
        }
        ```

    === "Java"
        ```java
        public class HelloWorld {
            public static void main(String []args) {
            System.out.println("Hello World");
            }
        }
        ```

    === "Rust"
        ```rust
        fn main() {
            println!("Hello World!");
        }
        ```

    === "Lua"
        ```Lua
        print("Hello World!")
        ```

    === "C#"
        ```csharp
        using System;
        namespace HelloWorldApplication
        {
            class HelloWorld
            {
                static void Main(string[] args)
                {
                    /* 我的第一个 C# 程序*/
                    Console.WriteLine("Hello World!");
                    Console.ReadKey();
                }
            }
        }
        ```

    === "R语言"
        ```r
        myString <- "Hello, World!"

        print ( myString )
        ```

    === "Perl"
        ```Perl
        #!/usr/bin/perl 
        
        print "Hello, World!\n";
        ```

    === "scala"
        ```scala
        object HelloWorld {
            def main(args: Array[String]): Unit = {
                println("Hello, world!")
            }
        }
        ```

!!! Example "前端语言实现Hello World"

    === "HTML"
        ```html
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>菜鸟教程(runoob.com)</title>
        </head>
        <body>

        <h1>Hello world</h1>
        <p>我的第一个段落。</p>

        </body>
        </html>
        ```

    === "javascript"
        ```javascript
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>菜鸟教程(runoob.com)</title>
        <script>
        function displayDate(){
            document.getElementById("demo").innerHTML=Date();
        }
        </script>
        </head>
        <body>

        <h1>我的第一个 JavaScript 程序</h1>
        <p id="demo">这是一个段落</p>

        <button type="button" onclick="displayDate()">显示日期</button>

        </body>
        </html>
        ```

    === "VUE3"
        ```vue3
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
        <script src="https://cdn.staticfile.org/vue/3.2.36/vue.global.min.js"></script>
        </head>
        <body>
        <div id="hello-vue" class="demo">
        {{ message }}
        </div>

        <script>
        const HelloVueApp = {
        data() {
            return {
            message: 'Hello Vue!!'
            }
        }
        }

        Vue.createApp(HelloVueApp).mount('#hello-vue')
        </script>
        </body>
        </html>
        ```

    === "jQuery"
        ```html
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8"> 
        <title>菜鸟教程(runoob.com)</title> 
        <script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js">
        </script>
        <script>
        $(document).ready(function(){
        $("p").click(function(){
            $(this).hide();
        });
        });
        </script>
        </head>
        <body>
        <p>如果你点我，我就会消失。</p>
        <p>继续点我!</p>
        <p>接着点我!</p>
        </body>
        </html>
        ```


## 一、脚本语言

### 1）NodeJs

简单的说 Node.js 就是运行在服务端的 JavaScript。

Node.js 是一个基于 Chrome JavaScript 运行时建立的一个平台。

Node.js 是一个事件驱动 I/O 服务端 JavaScript 环境，基于 Google 的 V8 引擎，V8 引擎执行 Javascript 的速度非常快，性能非常好。

```js
console.log("Hello World");
```

### 2）Python

Python 是一个高层次的结合了解释性、编译性、互动性和面向对象的脚本语言。

Python 的设计具有很强的可读性，相比其他语言经常使用英文关键字，其他语言的一些标点符号，它具有比其他语言更有特色语法结构。

```python
#!/usr/bin/python3

print("Hello, World!")
```

### 3）Ruby

Ruby 是一种开源的面向对象程序设计的服务器端脚本语言，在 20 世纪 90 年代中期由日本的松本行弘（`まつもとゆきひろ/Yukihiro Matsumoto`）设计并开发。在 Ruby 社区，松本也被称为马茨（Matz）。Ruby 可运行于多种平台，如 Windows、MAC OS 和 UNIX 的各种版本。

```ruby
#!/usr/bin/ruby
puts "Hello World!";
```


## 二、后端语言

### 1）C语言

C 语言是一种通用的、面向过程式的计算机程序设计语言。1972 年，为了移植与开发 UNIX 操作系统，丹尼斯·里奇在贝尔电话实验室设计开发了 C 语言。

C 语言是一种广泛使用的计算机语言，它与 Java 编程语言一样普及，二者在现代软件程序员之间都得到广泛使用。

```c
#include <stdio.h>
 
int main()
{
    /* 我的第一个 C 程序 */
    printf("Hello, World! \n");
 
    return 0;
}
```

### 2）C++语言

C++ 是一种高级语言，它是由 Bjarne Stroustrup 于 1979 年在贝尔实验室开始设计开发的。C++ 进一步扩充和完善了 C 语言，是一种面向对象的程序设计语言。C++ 可运行于多种平台上，如 Windows、MAC 操作系统以及 UNIX 的各种版本。

```cpp
#include <iostream>
using namespace std;
int main()
{
    cout << "Hello, world!" << endl;
    return 0;
}
```

### 3）Golang语言

Go 是一个开源的编程语言，它能让构造简单、可靠且高效的软件变得容易。


```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```


### 4）java语言

Java 是由 Sun Microsystems 公司于 1995 年 5 月推出的高级程序设计语言。

Java 可运行于多个平台，如 Windows, Mac OS 及其他多种 UNIX 版本的系统。

```java
public class HelloWorld {
    public static void main(String []args) {
       System.out.println("Hello World");
    }
}
```

### 5）Rust语言

Rust 语言是一种高效、可靠的通用高级语言。其高效不仅限于开发效率，它的执行效率也是令人称赞的，是一种少有的兼顾开发效率和执行效率的语言。

```rust
fn main() {
    println!("Hello World!");
}
```


### 6）lua语言

Lua 是一种轻量小巧的脚本语言，用标准C语言编写并以源代码形式开放， 其设计目的是为了嵌入应用程序中，从而为应用程序提供灵活的扩展和定制功能。


```Lua
print("Hello World!")
```


### 7）C\#

C# 是一个简单的、现代的、通用的、面向对象的编程语言，它是由微软（Microsoft）开发的。

本教程将告诉您基础的 C# 编程，同时将向您讲解 C# 编程语言相关的各种先进理念。

```csharp
using System;
namespace HelloWorldApplication
{
    class HelloWorld
    {
        static void Main(string[] args)
        {
            /* 我的第一个 C# 程序*/
            Console.WriteLine("Hello World!");
            Console.ReadKey();
        }
    }
}
```

### 8）R语言

R 语言是为数学研究工作者设计的一种数学编程语言，主要用于统计分析、绘图、数据挖掘。

```r
myString <- "Hello, World!"

print ( myString )
```

### 9）Perl语言

Perl 是 Practical Extraction and Report Language 的缩写，可翻译为 "实用报表提取语言"。

Perl 是高级、通用、直译式、动态的程序语言。

Perl 最初的设计者为拉里·沃尔（Larry Wall），于1987年12月18日发表。

Perl 借用了C、sed、awk、shell脚本以及很多其他编程语言的特性。

Perl 最重要的特性是Perl内部集成了正则表达式的功能，以及巨大的第三方代码库CPAN。


```Perl
#!/usr/bin/perl 
 
print "Hello, World!\n";
```

### 10）Scala语言

Scala 是一门多范式（multi-paradigm）的编程语言，设计初衷是要集成面向对象编程和函数式编程的各种特性。

Scala 运行在 Java 虚拟机上，并兼容现有的 Java 程序。

Scala 源代码被编译成 Java 字节码，所以它可以运行于 JVM 之上，并可以调用现有的 Java 类库

```scala
object HelloWorld {
    def main(args: Array[String]): Unit = {
        println("Hello, world!")
    }
}
```


## 三、网页web

### 1）HTML语言

超文本标记语言（英语：HyperText Markup Language，简称：HTML）是一种用于创建网页的标准标记语言。

您可以使用 HTML 来建立自己的 WEB 站点，HTML 运行在浏览器上，由浏览器来解析。

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>菜鸟教程(runoob.com)</title>
</head>
<body>

<h1>Hello world</h1>
<p>我的第一个段落。</p>

</body>
</html>
```


### 2）javascript

```javascript
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>菜鸟教程(runoob.com)</title>
<script>
function displayDate(){
	document.getElementById("demo").innerHTML=Date();
}
</script>
</head>
<body>

<h1>我的第一个 JavaScript 程序</h1>
<p id="demo">这是一个段落</p>

<button type="button" onclick="displayDate()">显示日期</button>

</body>
</html>
```

### 3）vue3

Vue.js（读音 /vjuː/, 类似于 view） 是一套构建用户界面的渐进式框架。

Vue 只关注视图层， 采用自底向上增量开发的设计。

Vue 的目标是通过尽可能简单的 API 实现响应的数据绑定和组合的视图组件。

```vue3
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
<script src="https://cdn.staticfile.org/vue/3.2.36/vue.global.min.js"></script>
</head>
<body>
<div id="hello-vue" class="demo">
  {{ message }}
</div>

<script>
const HelloVueApp = {
  data() {
    return {
      message: 'Hello Vue!!'
    }
  }
}

Vue.createApp(HelloVueApp).mount('#hello-vue')
</script>
</body>
</html>
```

### 4）jQuery

jQuery 是一个 JavaScript 库。

jQuery 极大地简化了 JavaScript 编程。

jQuery 很容易学习。

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"> 
<title>菜鸟教程(runoob.com)</title> 
<script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js">
</script>
<script>
$(document).ready(function(){
  $("p").click(function(){
    $(this).hide();
  });
});
</script>
</head>
<body>
<p>如果你点我，我就会消失。</p>
<p>继续点我!</p>
<p>接着点我!</p>
</body>
</html>
```
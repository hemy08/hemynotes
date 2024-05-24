# go 与 C 进行交互

工具 cgo 提供了对 FFI（外部函数接口）的支持，能够使用 Go 代码安全地调用 C 语言库，你可以访问 cgo 文档主页：http://golang.org/cmd/cgo。cgo 会替代 Go 编译器来产生可以组合在同一个包中的 Go 和 C 代码。在实际开发中一般使用 cgo 创建单独的 C 代码包。

如果你想要在你的 Go 程序中使用 cgo，则必须在单独的一行使用 import "C" 来导入，一般来说你可能还需要 import "unsafe"。

然后，你可以在 import "C" 之前使用注释（单行或多行注释均可）的形式导入 C 语言库（甚至有效的 C 语言代码），它们之间没有空行，例如：

```cgo
// #include <stdio.h>
// #include <stdlib.h>
import "C"
```

名称 "C" 并不属于标准库的一部分，这只是 cgo 集成的一个特殊名称用于引用 C 的命名空间。在这个命名空间里所包含的 C 类型都可以被使用，例如 C.uint、C.long 等等，还有 libc 中的函数 C.random() 等也可以被调用。

当你想要使用某个类型作为 C 中函数的参数时，必须将其转换为 C 中的类型，反之亦然，例如：

```go
var i int
C.uint(i)       // 从 Go 中的 int 转换为 C 中的无符号 int
int(C.random()) // 从 C 中 random() 函数返回的 long 转换为 Go 中的 int
```

下面的 2 个 Go 函数 ``Random()`` 和 ``Seed()`` 分别调用了 C 中的 ``C.random()`` 和 ``C.srandom()``。

```go
package rand

// #include <stdlib.h>
import "C"

func Random() int {
    return int(C.random())
}

func Seed(i int) {
    C.srandom(C.uint(i))
}
```

C 当中并没有明确的字符串类型，如果你想要将一个 string 类型的变量从 Go 转换到 C 时，可以使用 ``C.CString(s)``；同样，可以使用 ``C.GoString(cs)`` 从 C 转换到 Go 中的 string 类型。

Go 的内存管理机制无法管理通过 C 代码分配的内存。

开发人员需要通过手动调用 ``C.free`` 来释放变量的内存：

```go
defer C.free(unsafe.Pointer(Cvariable))
```

这一行最好紧跟在使用 C 代码创建某个变量之后，这样就不会忘记释放内存了。下面的代码展示了如何使用 cgo 创建变量、使用并释放其内存：

```go
package print

// #include <stdio.h>
// #include <stdlib.h>
import "C"
import "unsafe"

func Print(s string) {
    cs := C.CString(s)
    defer C.free(unsafe.Pointer(cs))
    C.fputs(cs, (*C.FILE)(C.stdout))
}
```

#### **构建 cgo 包**

你可以在使用Makefile 文件（因为我们使用了一个独立的包），除了使用变量 GOFILES 之外，还需要使用变量 CGOFILES 来列出需要使用 cgo 编译的文件列表。例如，示例 3.2 中的代码就可以使用包含以下内容的 Makefile 文件来编译，你可以使用 gomake 或 make：

```shell
include $(GOROOT)/src/Make.inc
TARG=rand
CGOFILES=\
c1.go\
include $(GOROOT)/src/Make.pkg
```

# Make构建系统

## 概述

Make是经典的构建自动化工具，通过Makefile定义构建规则和依赖关系。

## 基本语法

### 简单Makefile

```makefile
# 目标: 依赖
#    命令（必须用Tab缩进）

program: main.c func.c
    gcc main.c func.c -o program
```

### 变量

```makefile
# 定义变量
CC = gcc
CFLAGS = -Wall -O2
LDFLAGS = -lm

# 使用变量
program: main.c
    $(CC) $(CFLAGS) main.c $(LDFLAGS) -o program

# 自动变量
# $@ - 目标名
# $< - 第一个依赖
# $^ - 所有依赖
# $* - 不含扩展名的目标

%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@
```

### 常用变量

```makefile
# 预定义变量
CC          # C编译器（默认cc）
CXX         # C++编译器（默认g++）
CFLAGS      # C编译选项
CXXFLAGS    # C++编译选项
LDFLAGS     # 链接选项
LDLIBS      # 链接库

# 赋值方式
VAR = value     # 递归展开
VAR := value    # 简单展开
VAR ?= value    # 条件赋值（未定义时）
VAR += value    # 追加
```

## 模式规则

```makefile
# 通配符规则
%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

# 多模式规则
%.o: %.c %.h
    $(CC) $(CFLAGS) -c $< -o $@
```

## 自动依赖

```makefile
# 生成依赖文件
%.d: %.c
    $(CC) -MM $< > $@

# 包含依赖文件
-include $(SRCS:.c=.d)
```

## 完整示例

### C项目Makefile

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -O2 -g
LDFLAGS = -lm -lpthread

SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
TARGET = $(BIN_DIR)/program

.PHONY: all clean dirs

all: dirs $(TARGET)

dirs:
    mkdir -p $(OBJ_DIR) $(BIN_DIR)

$(TARGET): $(OBJS)
    $(CC) $(OBJS) $(LDFLAGS) -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
    $(CC) $(CFLAGS) -c $< -o $@

clean:
    rm -rf $(OBJ_DIR) $(BIN_DIR)
```

### C++项目Makefile

```makefile
CXX = g++
CXXFLAGS = -std=c++17 -Wall -O2
LDFLAGS = -lstdc++fs

SRCS = $(wildcard src/*.cpp)
OBJS = $(SRCS:.cpp=.o)
TARGET = program

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
    $(CXX) $(OBJS) $(LDFLAGS) -o $@

%.o: %.cpp
    $(CXX) $(CXXFLAGS) -c $< -o $@

clean:
    rm -f $(OBJS) $(TARGET)
```

### 交叉编译Makefile

```makefile
# 交叉编译工具链
CROSS_COMPILE = arm-linux-gnueabihf-
CC = $(CROSS_COMPILE)gcc
CXX = $(CROSS_COMPILE)g++
AR = $(CROSS_COMPILE)ar
STRIP = $(CROSS_COMPILE)strip

CFLAGS = -Wall -O2
LDFLAGS = -lm

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
TARGET = program

all: $(TARGET)

$(TARGET): $(OBJS)
    $(CC) $(OBJS) $(LDFLAGS) -o $@
    $(STRIP) $@

%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

clean:
    rm -f $(OBJS) $(TARGET)
```

## 条件判断

```makefile
# 条件判断
ifdef DEBUG
    CFLAGS += -g -DDEBUG
else
    CFLAGS += -O2
endif

# 平台判断
ifeq ($(shell uname),Linux)
    LDFLAGS += -lrt
endif

# 比较字符串
ifeq ($(CC),gcc)
    CFLAGS += -fgnu89-inline
endif

ifneq ($(CC),clang)
    # 不是clang
endif
```

## 函数

```makefile
# wildcard - 通配符
SRCS = $(wildcard src/*.c)

# patsubst - 模式替换
OBJS = $(patsubst %.c,%.o,$(SRCS))

# subst - 字符串替换
VAR = $(subst a,b,abc)    # bbc

# strip - 去除空格
VAR = $(strip  a  b  c )

# shell - 执行命令
DATE = $(shell date)

# filter/filter-out - 过滤
SRCS = $(filter %.c,$(FILES))
HDRS = $(filter-out %.c,$(FILES))

# dir/notdir - 目录/文件名
DIR = $(dir src/file.c)    # src/
FILE = $(notdir src/file.c)    # file.c

# basename/suffix - 基名/扩展名
BASE = $(basename file.c)    # file
EXT = $(suffix file.c)    # .c

# addprefix/addsuffix - 添加前缀/后缀
OBJS = $(addprefix obj/,$(OBJS))
SRCS = $(addsuffix .c,$(NAMES))
```

## 多目录项目

```makefile
# 目录结构
# project/
# ├── src/
# │   ├── main.c
# │   └── lib/
# │       └── func.c
# ├── include/
# └── build/

SRC_DIRS = src src/lib
INC_DIRS = include

SRCS = $(foreach dir,$(SRC_DIRS),$(wildcard $(dir)/*.c))
OBJS = $(patsubst %.c,build/%.o,$(notdir $(SRCS)))
INCS = $(addprefix -I,$(INC_DIRS))

CFLAGS = -Wall -O2 $(INCS)
TARGET = build/program

.PHONY: all clean

all: dirs $(TARGET)

dirs:
    mkdir -p build

$(TARGET): $(OBJS)
    $(CC) $(OBJS) -o $@

build/%.o: src/%.c
    $(CC) $(CFLAGS) -c $< -o $@

build/%.o: src/lib/%.c
    $(CC) $(CFLAGS) -c $< -o $@

clean:
    rm -rf build
```

## 静态库和共享库

```makefile
# 静态库
libmylib.a: func1.o func2.o
    ar rcs $@ $^

# 共享库
libmylib.so: func1.c func2.c
    $(CC) -shared -fPIC -o $@ $^
```

## 常用目标

```makefile
.PHONY: all clean install uninstall test

all: program

clean:
    rm -f $(OBJS) $(TARGET)

install: program
    install -m 755 program /usr/local/bin/

uninstall:
    rm -f /usr/local/bin/program

test: program
    ./program --test
```

## 调试Makefile

```bash
# 显示执行的命令
make -n

# 显示变量值
make print-VAR

# 调试模式
make -d

# 忽略错误
make -i

# 强制重建
make -B
```

## 参考资料

- [GNU Make手册](https://www.gnu.org/software/make/manual/)
- [Make教程](https://makefiletutorial.com/)

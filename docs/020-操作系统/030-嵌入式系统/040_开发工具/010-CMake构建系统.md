# CMake构建系统

## 概述

CMake是跨平台的构建系统生成器，可以生成各种平台的原生构建文件（Makefile、Visual Studio项目等）。

## 基本语法

### 最小CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject VERSION 1.0 LANGUAGES C CXX)

add_executable(myapp main.c)
```

### 变量

```cmake
# 设置变量
set(SOURCES main.c func.c)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# 使用变量
add_executable(myapp ${SOURCES})

# 列表操作
list(APPEND SOURCES extra.c)
list(REMOVE_ITEM SOURCES unused.c)

# 条件赋值
set(VAR "default" CACHE STRING "Description")
```

## 编译配置

### 编译选项

```cmake
# 编译选项
target_compile_options(myapp PRIVATE -Wall -Wextra)
target_compile_options(myapp PRIVATE $<$<CONFIG:Debug>:-g>)
target_compile_options(myapp PRIVATE $<$<CONFIG:Release>:-O3>)

# 定义宏
target_compile_definitions(myapp PRIVATE DEBUG=1)
target_compile_definitions(myapp PRIVATE $<$<CONFIG:Debug>:DEBUG>)

# 包含目录
target_include_directories(myapp PRIVATE ${CMAKE_SOURCE_DIR}/include)
```

### 链接库

```cmake
# 链接库
target_link_libraries(myapp PRIVATE m pthread)

# 链接选项
target_link_options(myapp PRIVATE -Wl,--as-needed)
```

## 项目结构

### 多目录项目

```
project/
├── CMakeLists.txt
├── src/
│   ├── main.c
│   └── lib/
│       ├── func.c
│       └── func.h
└── include/
```

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(SOURCES
    src/main.c
    src/lib/func.c
)

add_executable(myapp ${SOURCES})

target_include_directories(myapp PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src/lib
)
```

### 子目录项目

```cmake
# 根目录 CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyProject)

add_subdirectory(src)
add_subdirectory(lib)
```

```cmake
# src/CMakeLists.txt
add_executable(myapp main.c)
target_link_libraries(myapp PRIVATE mylib)
```

```cmake
# lib/CMakeLists.txt
add_library(mylib func.c)
target_include_directories(mylib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
```

## 库管理

### 创建库

```cmake
# 静态库
add_library(mylib STATIC lib.c)

# 共享库
add_library(mylib SHARED lib.c)

# 默认（通常为静态库）
add_library(mylib lib.c)

# 目标属性
set_target_properties(mylib PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    OUTPUT_NAME mylib
)
```

### 查找库

```cmake
# 查找库
find_library(MATH_LIB m)

# 查找包
find_package(OpenSSL REQUIRED)
find_package(ZLIB)

if(ZLIB_FOUND)
    target_link_libraries(myapp PRIVATE ZLIB::ZLIB)
endif()

# 查找程序
find_program(GIT git)
```

## 条件判断

```cmake
# if判断
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_definitions(myapp PRIVATE DEBUG)
endif()

# 选项
option(ENABLE_FEATURE "Enable feature" ON)

if(ENABLE_FEATURE)
    target_compile_definitions(myapp PRIVATE FEATURE_ENABLED)
endif()

# 平台判断
if(WIN32)
    # Windows
elseif(UNIX)
    # Unix/Linux
elseif(APPLE)
    # macOS
endif()

# 编译器判断
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    # GCC
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    # Clang
endif()
```

## 函数和宏

### 函数

```cmake
function(add_my_executable name)
    add_executable(${name} ${ARGN})
    target_compile_options(${name} PRIVATE -Wall)
endfunction()

add_my_executable(myapp main.c func.c)
```

### 宏

```cmake
macro(set_if_not_defined var value)
    if(NOT DEFINED ${var})
        set(${var} ${value})
    endif()
endmacro()
```

## 安装和打包

### 安装规则

```cmake
# 安装可执行文件
install(TARGETS myapp RUNTIME DESTINATION bin)

# 安装库
install(TARGETS mylib
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# 安装头文件
install(FILES include/myheader.h DESTINATION include)

# 安装目录
install(DIRECTORY include/ DESTINATION include)
```

### CPack打包

```cmake
# 启用CPack
set(CPACK_PACKAGE_NAME "MyApp")
set(CPACK_PACKAGE_VERSION "1.0.0")
set(CPACK_PACKAGE_DESCRIPTION "My Application")
set(CPACK_GENERATOR "DEB;RPM;TGZ")

include(CPack)
```

## 测试

### 启用测试

```cmake
enable_testing()

add_executable(test_app test.c)
add_test(NAME MyTest COMMAND test_app)

# 设置测试属性
set_tests_properties(MyTest PROPERTIES
    TIMEOUT 60
    WILL_FAIL false
)
```

## 外部项目

### FetchContent

```cmake
include(FetchContent)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG release-1.12.0
)

FetchContent_MakeAvailable(googletest)

target_link_libraries(myapp PRIVATE gtest_main)
```

### ExternalProject

```cmake
include(ExternalProject)

ExternalProject_Add(external_lib
    GIT_REPOSITORY https://github.com/user/lib.git
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/install
)
```

## 交叉编译

### 工具链文件

```cmake
# toolchain-arm.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)

set(CMAKE_FIND_ROOT_PATH /path/to/sysroot)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

```bash
# 使用工具链文件
cmake -DCMAKE_TOOLCHAIN_FILE=toolchain-arm.cmake ..
```

## 常用命令

```bash
# 配置
cmake -B build
cmake -B build -DCMAKE_BUILD_TYPE=Release

# 构建
cmake --build build
cmake --build build --target myapp
cmake --build build -j4

# 安装
cmake --install build
cmake --install build --prefix /usr/local

# 清理
cmake --build build --target clean
```

## 参考资料

- [CMake官方文档](https://cmake.org/documentation/)
- [CMake教程](https://cmake.org/cmake/help/latest/guide/tutorial/)
- [Modern CMake](https://cliutils.gitlab.io/modern-cmake/)

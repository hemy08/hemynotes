# DLL操作API

## 概述

动态链接库（Dynamic Link Library，DLL）是Windows操作系统中实现代码共享和模块化的重要机制。Windows提供了丰富的API用于加载、使用和卸载DLL。

## DLL加载

### LoadLibrary - 加载DLL

!!! note "LoadLibrary函数"
    将指定的DLL模块加载到调用进程的地址空间中。

```cpp
HMODULE LoadLibrary(
    LPCTSTR lpLibFileName  // DLL文件名
);
```

**返回值**：
- 成功：返回模块句柄
- 失败：返回NULL，使用GetLastError获取错误码

**示例**：
```cpp
#include <windows.h>
#include <stdio.h>

int main() {
    HMODULE hDll = LoadLibrary(L"user32.dll");
    if (hDll == NULL) {
        printf("LoadLibrary failed: %d\n", GetLastError());
        return -1;
    }
    
    printf("DLL loaded at: %p\n", hDll);
    
    FreeLibrary(hDll);
    return 0;
}
```

### LoadLibraryEx - 扩展加载DLL

```cpp
HMODULE LoadLibraryEx(
    LPCTSTR  lpLibFileName,     // DLL文件名
    HANDLE   hReservedReserved, // 保留，必须为NULL
    DWORD    dwFlags            // 加载选项
);
```

**加载标志**：

| 标志 | 说明 |
|------|------|
| `DONT_RESOLVE_DLL_REFERENCES` | 不解析DLL引用 |
| `LOAD_LIBRARY_AS_DATAFILE` | 作为数据文件加载 |
| `LOAD_LIBRARY_AS_DATAFILE_EXCLUSIVE` | 独占数据文件加载 |
| `LOAD_LIBRARY_AS_IMAGE_RESOURCE` | 作为映像资源加载 |
| `LOAD_LIBRARY_SEARCH_APPLICATION_DIR` | 在应用目录搜索 |
| `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS` | 使用默认搜索目录 |
| `LOAD_LIBRARY_SEARCH_SYSTEM32` | 只在System32搜索 |
| `LOAD_LIBRARY_SEARCH_USER_DIRS` | 在用户目录搜索 |
| `LOAD_WITH_ALTERED_SEARCH_PATH` | 使用替代搜索路径 |

**示例**：
```cpp
HMODULE hDll = LoadLibraryEx(L"mylib.dll", NULL, LOAD_LIBRARY_SEARCH_DEFAULT_DIRS);
```

### FreeLibrary - 卸载DLL

```cpp
BOOL FreeLibrary(
    HMODULE hLibModule  // DLL模块句柄
);
```

**示例**：
```cpp
FreeLibrary(hDll);
```

### FreeLibraryAndExitThread - 卸载DLL并退出线程

```cpp
VOID FreeLibraryAndExitThread(
    HMODULE hLibModule,
    DWORD   dwExitCode
);
```

**用途**：用于DLL中的线程，确保线程退出后再卸载DLL。

## 获取函数地址

### GetProcAddress - 获取导出函数地址

```cpp
FARPROC GetProcAddress(
    HMODULE hModule,    // DLL模块句柄
    LPCSTR  lpProcName  // 函数名或序号
);
```

**返回值**：
- 成功：返回函数地址
- 失败：返回NULL

**示例**：
```cpp
#include <windows.h>
#include <stdio.h>

int main() {
    HMODULE hDll = LoadLibrary(L"user32.dll");
    if (hDll == NULL) {
        printf("LoadLibrary failed: %d\n", GetLastError());
        return -1;
    }
    
    // 获取MessageBox函数地址
    typedef int (WINAPI* MessageBoxFunc)(HWND, LPCWSTR, LPCWSTR, UINT);
    MessageBoxFunc pMessageBox = (MessageBoxFunc)GetProcAddress(hDll, "MessageBoxW");
    
    if (pMessageBox != NULL) {
        pMessageBox(NULL, L"Hello from DLL!", L"Test", MB_OK);
    } else {
        printf("GetProcAddress failed: %d\n", GetLastError());
    }
    
    FreeLibrary(hDll);
    return 0;
}
```

### 通过序号获取函数

```cpp
FARPROC proc = GetProcAddress(hDll, (LPCSTR)MAKEINTRESOURCE(1));
```

## 模块信息

### GetModuleHandle - 获取已加载模块句柄

```cpp
HMODULE GetModuleHandle(
    LPCTSTR lpModuleName  // 模块名（NULL表示当前模块）
);
```

**示例**：
```cpp
HMODULE hExe = GetModuleHandle(NULL);  // 当前程序句柄
HMODULE hDll = GetModuleHandle(L"user32.dll");
```

### GetModuleHandleEx - 扩展获取模块句柄

```cpp
BOOL GetModuleHandleEx(
    DWORD   dwFlags,
    LPCTSTR lpModuleName,
    HMODULE *phModule
);
```

**标志**：
- `GET_MODULE_HANDLE_EX_FLAG_PIN`：固定模块，不卸载
- `GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT`：不增加引用计数
- `GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS`：从地址获取模块

### GetModuleFileName - 获取模块路径

```cpp
DWORD GetModuleFileName(
    HMODULE hModule,    // 模块句柄
    LPTSTR  lpFilename, // 路径缓冲区
    DWORD   nSize       // 缓冲区大小
);
```

**示例**：
```cpp
TCHAR path[MAX_PATH];
GetModuleFileName(NULL, path, MAX_PATH);  // 当前程序路径
GetModuleFileName(hDll, path, MAX_PATH);  // DLL路径
```

### GetModuleBaseName - 获取模块基名

```cpp
DWORD GetModuleBaseName(
    HANDLE  hProcess,
    HMODULE hModule,
    LPTSTR  lpBaseName,
    DWORD   nSize
);
```

### GetModuleInformation - 获取模块信息

```cpp
BOOL GetModuleInformation(
    HANDLE       hProcess,
    HMODULE      hModule,
    LPMODULEINFO lpmodinfo,
    DWORD        cb
);
```

## DLL入口点

### DllMain - DLL入口函数

```cpp
BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,      // DLL模块句柄
    DWORD     fdwReason,     // 调用原因
    LPVOID    lpvReserved    // 保留
);
```

**调用原因**：
- `DLL_PROCESS_ATTACH`：进程附加
- `DLL_PROCESS_DETACH`：进程分离
- `DLL_THREAD_ATTACH`：线程附加
- `DLL_THREAD_DETACH`：线程分离

**示例**：
```cpp
#include <windows.h>

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            // 初始化代码
            DisableThreadLibraryCalls(hinstDLL);
            break;
            
        case DLL_PROCESS_DETACH:
            // 清理代码
            break;
    }
    return TRUE;
}
```

## 延迟加载DLL

### 手动加载延迟DLL

```cpp
HMODULE __HrLoadAllImportsForDll(LPCSTR szDll);
```

### 检查延迟加载异常

```cpp
FARPROC __DelayLoadHelper2(PCImgDelayDescr pidd, FARPROC* ppfn);
```

## 导出函数

### 导出函数声明

```cpp
// 方式1：使用__declspec(dllexport)
__declspec(dllexport) int Add(int a, int b) {
    return a + b;
}

// 方式2：使用DEF文件
// 在.def文件中：
// EXPORTS
//     Add
//     Subtract
```

### 导出C++函数

```cpp
extern "C" __declspec(dllexport) int Add(int a, int b) {
    return a + b;
}
```

### 导出类

```cpp
class __declspec(dllexport) MyClass {
public:
    int GetValue();
    void SetValue(int value);
private:
    int m_value;
};
```

## 模块定义文件(.def)

```
LIBRARY MyLibrary
EXPORTS
    Add         @1
    Subtract    @2
    Multiply    @3
    Divide      @4
```

## 完整DLL示例

### DLL实现

```cpp
// MyMath.cpp
#include <windows.h>

extern "C" {
    __declspec(dllexport) int Add(int a, int b) {
        return a + b;
    }
    
    __declspec(dllexport) int Subtract(int a, int b) {
        return a - b;
    }
    
    __declspec(dllexport) int Multiply(int a, int b) {
        return a * b;
    }
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            DisableThreadLibraryCalls(hinstDLL);
            break;
    }
    return TRUE;
}
```

### 使用DLL

```cpp
#include <windows.h>
#include <stdio.h>

typedef int (*MathFunc)(int, int);

int main() {
    HMODULE hDll = LoadLibrary(L"MyMath.dll");
    if (hDll == NULL) {
        printf("Failed to load DLL: %d\n", GetLastError());
        return -1;
    }
    
    MathFunc pAdd = (MathFunc)GetProcAddress(hDll, "Add");
    MathFunc pSubtract = (MathFunc)GetProcAddress(hDll, "Subtract");
    MathFunc pMultiply = (MathFunc)GetProcAddress(hDll, "Multiply");
    
    if (pAdd && pSubtract && pMultiply) {
        printf("5 + 3 = %d\n", pAdd(5, 3));
        printf("5 - 3 = %d\n", pSubtract(5, 3));
        printf("5 * 3 = %d\n", pMultiply(5, 3));
    }
    
    FreeLibrary(hDll);
    return 0;
}
```

## 隐式链接

### 使用.lib文件

```cpp
// MyMath.h
#pragma once
#ifdef MYMATH_EXPORTS
#define MYMATH_API __declspec(dllexport)
#else
#define MYMATH_API __declspec(dllimport)
#endif

extern "C" {
    MYMATH_API int Add(int a, int b);
    MYMATH_API int Subtract(int a, int b);
}

// 使用
#include "MyMath.h"
#pragma comment(lib, "MyMath.lib")

int main() {
    int result = Add(5, 3);
    return 0;
}
```

## 资源DLL

### 创建资源DLL

```cpp
// 资源DLL只需要包含资源，不需要代码
// 在.rc文件中定义资源
```

### 加载资源DLL

```cpp
HMODULE hResDll = LoadLibraryEx(L"ResourceDll.dll", NULL, LOAD_LIBRARY_AS_DATAFILE);
if (hResDll) {
    // 加载资源
    HBITMAP hBitmap = LoadBitmap(hResDll, MAKEINTRESOURCE(IDB_MYBITMAP));
    // ...
    FreeLibrary(hResDll);
}
```

## DLL搜索顺序

1. 应用程序加载的目录
2. 系统目录（System32）
3. 16位系统目录（System）
4. Windows目录
5. 当前目录
6. PATH环境变量中的目录

### 使用SetDllDirectory修改搜索路径

```cpp
BOOL SetDllDirectory(
    LPCTSTR lpPathName
);
```

### 使用AddDllDirectory添加搜索路径

```cpp
DLL_DIRECTORY_COOKIE AddDllDirectory(
    PCWSTR Path
);
```

## 参考资料

- [动态链接库 - Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/win32/dlls/dynamic-link-libraries)
- [LoadLibrary函数 - Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya)
- [GetProcAddress函数 - Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/win32/api/libloaderapi/nf-libloaderapi-getprocaddress)
- [DllMain函数 - Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/win32/dlls/dllmain)

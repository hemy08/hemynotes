# python实现批量重命名

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-08-29</span>

```python

# encoding=utf-8
import os

path = ""

fileList = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）

count = 1

for file in fileList:
    print(file)
for file in fileList:  # 遍历所有文件
    oldName = os.path.join(path, file)  # 原来的文件路径
    print(oldName)

    if os.path.isdir(oldName):  # 如果是文件夹则跳过
        continue

    filename = os.path.splitext(file)[0]  # 文件名

    filetype = os.path.splitext(file)[1]  # 文件扩展名

    if filetype != ".md":
        continue

    newName = os.path.join(path, str(count).zfill(2) + '-' + filename + filetype)  # 用字符串函数zfill 以0补全所需位数
    print(newName)
    os.rename(oldName, newName)  # 重命名
    count += 1


```

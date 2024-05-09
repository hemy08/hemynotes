# cp命令

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-07-31</span>

cp命令的作用：文件复制

## cp命令的常用选项

- -a：此参数的效果和同时指定"-dpR"参数相同；
- -d：当复制符号连接时，把目标文件或目录也建立为符号连接，并指向与源文件或目录连接的原始文件或目录；
- -f：强行复制文件或目录，不论目标文件或目录是否已存在；
- -i：覆盖既有文件之前先询问用户；
- -l：对源文件建立硬连接，而非复制文件；
- -p：保留源文件或目录的属性；
- -R/r：递归处理，将指定目录下的所有文件与子目录一并处理；
- -s：对源文件建立符号连接，而非复制文件；
- -u：使用这项参数后只会在源文件的更改时间较目标文件更新时或是名称相互对应的目标文件并不存在时，才复制文件；
- -S：在备份文件时，用指定的后缀“SUFFIX”代替文件的默认后缀；
- -b：覆盖已存在的文件目标前将目标文件备份；
- -v：详细显示命令执行的操作。

## 使用 cp 命令复制文件

- 复制文件：cp file.txt file.txt.bak
- 复制文件并保持原有文件权限：cp -p file.txt file.txt.bak
- 复制文件到指定目录下：cp file.txt /tmp/test_shell/dir1
- 复制文件并指定文件目录：cp file.txt /tmp/test_shell/dir1/file.txt.bak
- 复制文件并忽略重复文件提示：cp -f file.txt file.txt.bak

遇到的问题：如果使用 -f 选项后，复制重复文件时，还是有提示，则是alias别名的问题

```
[root@linux test_shell]# alias
alias cp='cp -i'
```
解决方法：删除或修改cp别名

```
[root@linux test_shell]# unalias cp
```


## 使用 cp 命令复制目录

复制目录(包括其所有文件和子目录)：cp -r dir1 dir2
只复制目录下的所有文件和子目录：cp -RT dir1 dir2
只复制目录下的所有文件：cp dir1/* dir3
# rsync命令

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2021-07-31</span>

**rsync命令**是一个远程数据同步工具，可通过LAN/WAN快速同步多台主机间的文件。rsync使用所谓的“rsync算法”来使本地和远程两个主机之间的文件达到同步，这个算法只传送两个文件的不同部分，而不是每次都整份传送，因此速度相当快。 rsync是一个功能非常强大的工具，其命令也有很多功能特色选项，我们下面就对它的选项一一进行分析说明。

## 语法

```
rsync [OPTION]... SRC DEST
rsync [OPTION]... SRC [USER@]host:DEST
rsync [OPTION]... [USER@]HOST:SRC DEST
rsync [OPTION]... [USER@]HOST::SRC DEST
rsync [OPTION]... SRC [USER@]HOST::DEST
rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]
```

对应于以上六种命令格式，rsync有六种不同的工作模式：

1. 拷贝本地文件。当SRC和DES路径信息都不包含有单个冒号":"分隔符时就启动这种工作模式。如：rsync -a /data /backup
2. 使用一个远程shell程序\(如rsh、ssh\)来实现将本地机器的内容拷贝到远程机器。当DST路径地址包含单个冒号":"分隔符时启动该模式。如：rsync -avz \*.c foo:src
3. 使用一个远程shell程序\(如rsh、ssh\)来实现将远程机器的内容拷贝到本地机器。当SRC地址路径包含单个冒号":"分隔符时启动该模式。如：rsync -avz foo:src/bar /data
4. 从远程rsync服务器中拷贝文件到本地机。当SRC路径信息包含"::"分隔符时启动该模式。如：rsync -av root@192.168.78.192::www /databack
5. 从本地机器拷贝文件到远程rsync服务器中。当DST路径信息包含"::"分隔符时启动该模式。如：rsync -av /databack root@192.168.78.192::www
6. 列远程机的文件列表。这类似于rsync传输，不过只要在命令中省略掉本地机信息即可。如：rsync -v rsync://192.168.78.192/www

## Option选项

```
-v, --verbose 详细模式输出。 
-q, --quiet 精简输出模式。 
-c, --checksum 打开校验开关，强制对文件传输进行校验。 
-a, --archive 归档模式，表示以递归方式传输文件，并保持所有文件属性，等于-rlptgoD。 
-r, --recursive 对子目录以递归模式处理。 
-R, --relative 使用相对路径信息。 
-b, --backup 创建备份，也就是对于目的已经存在有同样的文件名时，将老的文件重新命名为~filename。可以使用--suffix选项来指定不同的备份文件前缀。 
    --backup-dir 将备份文件(如~filename)存放在在目录下。 
-suffix=SUFFIX 定义备份文件前缀。 
-u, --update 仅仅进行更新，也就是跳过所有已经存在于DST，并且文件时间晚于要备份的文件，不覆盖更新的文件。 
-l, --links 保留软链结。 
-L, --copy-links 想对待常规文件一样处理软链结。 
    --copy-unsafe-links 仅仅拷贝指向SRC路径目录树以外的链结。 
    --safe-links 忽略指向SRC路径目录树以外的链结。 
-H, --hard-links 保留硬链结。 
-p, --perms 保持文件权限。 
-o, --owner 保持文件属主信息。 
-g, --group 保持文件属组信息。 
-D, --devices 保持设备文件信息。 
-t, --times 保持文件时间信息。 
-S, --sparse 对稀疏文件进行特殊处理以节省DST的空间。 
-n, --dry-run现实哪些文件将被传输。 
-w, --whole-file 拷贝文件，不进行增量检测。 
-x, --one-file-system 不要跨越文件系统边界。 
-B, --block-size=SIZE 检验算法使用的块尺寸，默认是700字节。 
-e, --rsh=command 指定使用rsh、ssh方式进行数据同步。 
    --rsync-path=PATH 指定远程服务器上的rsync命令所在路径信息。 
-C, --cvs-exclude 使用和CVS一样的方法自动忽略文件，用来排除那些不希望传输的文件。 
    --existing 仅仅更新那些已经存在于DST的文件，而不备份那些新创建的文件。 
    --delete 删除那些DST中SRC没有的文件。 
    --delete-excluded 同样删除接收端那些被该选项指定排除的文件。 
    --delete-after 传输结束以后再删除。 
    --ignore-errors 及时出现IO错误也进行删除。 
    --max-delete=NUM 最多删除NUM个文件。 
    --partial 保留那些因故没有完全传输的文件，以是加快随后的再次传输。 
    --force 强制删除目录，即使不为空。 
    --numeric-ids 不将数字的用户和组id匹配为用户名和组名。 
    --timeout=time ip超时时间，单位为秒。 
-I, --ignore-times 不跳过那些有同样的时间和长度的文件。 
    --size-only 当决定是否要备份文件时，仅仅察看文件大小而不考虑文件时间。 
    --modify-window=NUM 决定文件是否时间相同时使用的时间戳窗口，默认为0。 
-T  --temp-dir=DIR 在DIR中创建临时文件。 
    --compare-dest=DIR 同样比较DIR中的文件来决定是否需要备份。 
-P 等同于 --partial。 
    --progress 显示备份过程。 
-z, --compress 对备份的文件在传输时进行压缩处理。 
    --exclude=PATTERN 指定排除不需要传输的文件模式。 
    --include=PATTERN 指定不排除而需要传输的文件模式。 
    --exclude-from=FILE 排除FILE中指定模式的文件。 
    --include-from=FILE 不排除FILE指定模式匹配的文件。 
    --version 打印版本信息。 
    --address 绑定到特定的地址。 
    --config=FILE 指定其他的配置文件，不使用默认的rsyncd.conf文件。 
    --port=PORT 指定其他的rsync服务端口。 
    --blocking-io 对远程shell使用阻塞IO。 
-stats 给出某些文件的传输状态。 
    --progress 在传输时现实传输过程。 
    --log-format=formAT 指定日志文件格式。 
    --password-file=FILE 从FILE中得到密码。 
    --bwlimit=KBPS 限制I/O带宽，KBytes per second。 
-h, --help 显示帮助信息。
```

## 实例

1. SSH方式

   首先在服务端启动ssh服务：

   ```
   servicesshd start
   ```
2. 使用rsync进行同步

   接下来就可以在客户端使用rsync命令来备份服务端上的数据了，SSH方式是通过系统用户来进行备份的，如下：

   ```
   rsync -vzrtopg --progress -e ssh --delete work@xx.xx.xx.xx:/www/* /databack/experiment/rsync 
   work@xx.xx.xx.xx's password: 
   receiving file list ... 
   5 files to consider 
   test/ 
   a 
   0 100% 0.00kB/s 527:35:41 (1, 20.0% of 5) 
   b 
   67 100% 65.43kB/s 0:00:00 (2, 40.0% of 5) 
   c 
   0 100% 0.00kB/s 527:35:41 (3, 60.0% of 5) 
   dd 
   100663296 100% 42.22MB/s 0:00:02 (4, 80.0% of 5) 
   sent 96 bytes received 98190 bytes 11563.06 bytes/sec 
   total size is 100663363 speedup is 1024.19
   ```

   上面的信息描述了整个的备份过程，以及总共备份数据的大小。
3. 后台服务方式

   启动rsync服务，编辑/etc/xinetd.d/rsync文件，将其中的disable=yes改为disable=no，并重启xinetd服务，如下：

   ```
   vi /etc/xinetd.d/rsync 

   #default: off 
   # description: The rsync server is a good addition to an ftp server, as it \ 
   # allows crc checksumming etc. 
   service rsync { 
   disable = no 
   socket_type = stream 
   wait = no 
   user = root 
   server = /usr/bin/rsync 
   server_args = --daemon 
   log_on_failure += USERID 
   }
   ```
   .
   ```
   /etc/init.d/xinetd restart  
   停止 xinetd： [确定]  
   启动 xinetd： [确定]
   ```

   创建配置文件，默认安装好rsync程序后，并不会自动创建rsync的主配置文件，需要手工来创建，其主配置文件为“/etc/rsyncd.conf”，创建该文件并插入如下内容：

   ```
   vi /etc/rsyncd.conf  

   uid=root  
   gid=root  
   max connections=4  
   log file=/var/log/rsyncd.log  
   pid file=/var/run/rsyncd.pid  
   lock file=/var/run/rsyncd.lock  
   secrets file=/etc/rsyncd.passwd 
   hosts deny=xx.xx.xx.0/22  

   [www]  
   comment= backup web  
   path=/www  
   read only = no  
   exclude=test  
   auth users=work
   ```

   创建密码文件，采用这种方式不能使用系统用户对客户端进行认证，所以需要创建一个密码文件，其格式为“username:password”，用户名可以和密码可以随便定义，最好不要和系统帐户一致，同时要把创建的密码文件权限设置为600，这在前面的模块参数做了详细介绍。

   ```
   echo "work:xxxxx" > /etc/rsyncd.passwd  
   chmod 600 /etc/rsyncd.passwd
   ```

   备份，完成以上工作，现在就可以对数据进行备份了，如下：

   ```
   rsync -avz --progress --delete work@xx.xx.xx.xx::www /databack/experiment/rsync 

   Password: 
   receiving file list ... 
   6 files to consider 
   ./ files... 
   a 
   0 100% 0.00kB/s 528:20:41 (1, 50.0% of 6) 
   b 
   67 100% 65.43kB/s 0:00:00 (2, 66.7% of 6) 
   c 
   0 100% 0.00kB/s 528:20:41 (3, 83.3% of 6) 
   dd 
   100663296 100% 37.49MB/s 0:00:02 (4, 100.0% of 6) 
   sent 172 bytes received 98276 bytes 17899.64 bytes/sec 
   total size is 150995011 speedup is 1533.75
   ```

   恢复，当服务器的数据出现问题时，那么这时就需要通过客户端的数据对服务端进行恢复，但前提是服务端允许客户端有写入权限，否则也不能在客户端直接对服务端进行恢复，使用rsync对数据进行恢复的方法如下：

   ```
   rsync -avz --progress /databack/experiment/rsync/ work@xx.xx.xx.xx::www 

   Password: 
   building file list ... 
   6 files to consider 
   ./ 
   a 
   b 
   67 100% 0.00kB/s 0:00:00 (2, 66.7% of 6) 
   c 
   sent 258 bytes received 76 bytes 95.43 bytes/sec 
   total size is 150995011 speedup is 452080.87
   ```

## 在linux上rsync -h的结果

```
rsync  version 3.0.9  protocol version 30 
Copyright (C) 1996-2011 by Andrew Tridgell, Wayne Davison, and others. 
Web site: http://rsync.samba.org/ 
Capabilities: 
    64-bit files, 64-bit inums, 64-bit timestamps, 64-bit long ints, 
    socketpairs, hardlinks, symlinks, IPv6, batchfiles, inplace, 
    append, ACLs, xattrs, iconv, symtimes 

rsync comes with ABSOLUTELY NO WARRANTY.  This is free software, and you 
are welcome to redistribute it under certain conditions.  See the GNU 
General Public Licence for details. 

rsync is a file transfer program capable of efficient remote update 
via a fast differencing algorithm. 

Usage: rsync [OPTION]... SRC [SRC]... DEST 
  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST 
  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST 
  or   rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST 
  or   rsync [OPTION]... [USER@]HOST:SRC [DEST] 
  or   rsync [OPTION]... [USER@]HOST::SRC [DEST] 
  or   rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST] 
The ':' usages connect via remote shell, while '::' & 'rsync://' usages connect 
to an rsync daemon, and require SRC or DEST to start with a module name. 

Options 
 -v, --verbose               increase verbosity 
 -q, --quiet                 suppress non-error messages 
     --no-motd               suppress daemon-mode MOTD (see manpage caveat) 
 -c, --checksum              skip based on checksum, not mod-time & size 
 -a, --archive               archive mode; equals -rlptgoD (no -H,-A,-X) 
     --no-OPTION             turn off an implied OPTION (e.g. --no-D) 
 -r, --recursive             recurse into directories 
 -R, --relative              use relative path names 
     --no-implied-dirs       don't send implied dirs with --relative 
 -b, --backup                make backups (see --suffix & --backup-dir) 
     --backup-dir=DIR        make backups into hierarchy based in DIR 
     --suffix=SUFFIX         set backup suffix (default ~ w/o --backup-dir) 
 -u, --update                skip files that are newer on the receiver 
     --inplace               update destination files in-place (SEE MAN PAGE) 
     --append                append data onto shorter files 
     --append-verify         like --append, but with old data in file checksum 
 -d, --dirs                  transfer directories without recursing 
 -l, --links                 copy symlinks as symlinks 
 -L, --copy-links            transform symlink into referent file/dir 
     --copy-unsafe-links     only "unsafe" symlinks are transformed 
     --safe-links            ignore symlinks that point outside the source tree 
 -k, --copy-dirlinks         transform symlink to a dir into referent dir 
 -K, --keep-dirlinks         treat symlinked dir on receiver as dir 
 -H, --hard-links            preserve hard links 
 -p, --perms                 preserve permissions 
 -E, --executability         preserve the file's executability 
     --chmod=CHMOD           affect file and/or directory permissions 
 -A, --acls                  preserve ACLs (implies --perms) 
 -X, --xattrs                preserve extended attributes 
 -o, --owner                 preserve owner (super-user only) 
 -g, --group                 preserve group 
     --devices               preserve device files (super-user only) 
     --copy-devices          copy device contents as regular file 
     --specials              preserve special files 
 -D                          same as --devices --specials 
 -t, --times                 preserve modification times 
 -O, --omit-dir-times        omit directories from --times 
     --super                 receiver attempts super-user activities 
     --fake-super            store/recover privileged attrs using xattrs 
 -S, --sparse                handle sparse files efficiently 
 -n, --dry-run               perform a trial run with no changes made 
 -W, --whole-file            copy files whole (without delta-xfer algorithm) 
 -x, --one-file-system       don't cross filesystem boundaries 
 -B, --block-size=SIZE       force a fixed checksum block-size 
 -e, --rsh=COMMAND           specify the remote shell to use 
     --rsync-path=PROGRAM    specify the rsync to run on the remote machine 
     --existing              skip creating new files on receiver 
     --ignore-existing       skip updating files that already exist on receiver 
     --remove-source-files   sender removes synchronized files (non-dirs) 
     --del                   an alias for --delete-during 
     --delete                delete extraneous files from destination dirs 
     --delete-before         receiver deletes before transfer, not during 
     --delete-during         receiver deletes during the transfer 
     --delete-delay          find deletions during, delete after 
     --delete-after          receiver deletes after transfer, not during 
     --delete-excluded       also delete excluded files from destination dirs 
     --ignore-errors         delete even if there are I/O errors 
     --force                 force deletion of directories even if not empty 
     --max-delete=NUM        don't delete more than NUM files 
     --max-size=SIZE         don't transfer any file larger than SIZE 
     --min-size=SIZE         don't transfer any file smaller than SIZE 
     --partial               keep partially transferred files 
     --partial-dir=DIR       put a partially transferred file into DIR 
     --delay-updates         put all updated files into place at transfer's end 
 -m, --prune-empty-dirs      prune empty directory chains from the file-list 
     --numeric-ids           don't map uid/gid values by user/group name 
     --timeout=SECONDS       set I/O timeout in seconds 
     --contimeout=SECONDS    set daemon connection timeout in seconds 
 -I, --ignore-times          don't skip files that match in size and mod-time 
     --size-only             skip files that match in size 
     --modify-window=NUM     compare mod-times with reduced accuracy 
 -T, --temp-dir=DIR          create temporary files in directory DIR 
 -y, --fuzzy                 find similar file for basis if no dest file 
     --compare-dest=DIR      also compare destination files relative to DIR 
     --copy-dest=DIR         ... and include copies of unchanged files 
     --link-dest=DIR         hardlink to files in DIR when unchanged 
 -z, --compress              compress file data during the transfer 
     --compress-level=NUM    explicitly set compression level 
     --skip-compress=LIST    skip compressing files with a suffix in LIST 
 -C, --cvs-exclude           auto-ignore files the same way CVS does 
 -f, --filter=RULE           add a file-filtering RULE 
 -F                          same as --filter='dir-merge /.rsync-filter' 
                             repeated: --filter='- .rsync-filter' 
     --exclude=PATTERN       exclude files matching PATTERN 
     --exclude-from=FILE     read exclude patterns from FILE 
     --include=PATTERN       don't exclude files matching PATTERN 
     --include-from=FILE     read include patterns from FILE 
     --files-from=FILE       read list of source-file names from FILE 
 -0, --from0                 all *-from/filter files are delimited by 0s 
 -s, --protect-args          no space-splitting; only wildcard special-chars 
     --address=ADDRESS       bind address for outgoing socket to daemon 
     --port=PORT             specify double-colon alternate port number 
     --sockopts=OPTIONS      specify custom TCP options 
     --blocking-io           use blocking I/O for the remote shell 
     --stats                 give some file-transfer stats 
 -8, --8-bit-output          leave high-bit chars unescaped in output 
 -h, --human-readable        output numbers in a human-readable format 
     --progress              show progress during transfer 
 -P                          same as --partial --progress 
 -i, --itemize-changes       output a change-summary for all updates 
     --out-format=FORMAT     output updates using the specified FORMAT 
     --log-file=FILE         log what we're doing to the specified FILE 
     --log-file-format=FMT   log updates using the specified FMT 
     --password-file=FILE    read daemon-access password from FILE 
     --list-only             list the files instead of copying them 
     --bwlimit=KBPS          limit I/O bandwidth; KBytes per second 
     --write-batch=FILE      write a batched update to FILE 
     --only-write-batch=FILE like --write-batch but w/o updating destination 
     --read-batch=FILE       read a batched update from FILE 
     --protocol=NUM          force an older protocol version to be used 
     --iconv=CONVERT_SPEC    request charset conversion of filenames 
     --checksum-seed=NUM     set block/file checksum seed (advanced) 
 -4, --ipv4                  prefer IPv4 
 -6, --ipv6                  prefer IPv6 
     --version               print version number 
(-h) --help                  show this help (-h is --help only if used alone) 

Use "rsync --daemon --help" to see the daemon-mode command-line options. 
Please see the rsync(1) and rsyncd.conf(5) man pages for full documentation. 
See http://rsync.samba.org/ for updates, bug reports, and answers
```

rsync是一个工具，而不仅仅是一个命令，可以在[http://rsync.samba.org/](http://rsync.samba.org/)去看。

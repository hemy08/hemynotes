#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# 读取文件
file_path = "002-二叉搜索树.md"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 第1部分：查找路径可视化（已完成）
search_part1_old = r'''#### 查找路径可视化


在以下 BST 中查找值 6:

```mermaid
graph TB
    A\(\(8\)\) --> BA\(\(3\)\)
    A --> BB\(\(10\)\)
    BA --> BAA\(\(1\)\)
    BA --> BAB\(\(6\)\)
    BB --> BBA\(\(null\)\)
    BB --> BBB\(\(14\)\)
    BAB --> BABA\(\(4\)\)
    BAB --> BABB\(\(7\)\)
    BBB --> BBBA\(\(13\)\)
    BBB --> BBBB\(\(null\)\)
```

查找路径:
```
─────────────────────────────────────────────────────────────────
步骤   当前节点   比较           决策
─────────────────────────────────────────────────────────────────
 1       8      6 < 8         向左走
 2       3      6 > 3         向右走
 3       6      6 == 6        找到！
─────────────────────────────────────────────────────────────────

查找路径: 8 → 3 → 6
比较次数: 3
```'''

search_part1_new = '''#### 查找路径可视化

在以下 BST 中查找值 6:

<div style="background-color: #F5F5F5; border-radius: 8px; padding: 20px; margin: 10px 0;">
<p style="text-align: center; margin: 0 0 15px 0; font-weight: bold; font-size: 16px;">BST 树结构（查找值 6）</p>
<div style="text-align: center; font-family: monospace;">
<div style="margin-bottom: 8px;">
<span style="display: inline-block; width: 40px; height: 40px; line-height: 40px; background-color: #E3F2FD; border: 3px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold; color: #2196F3;">8</span>
</div>
<div style="color: #999; margin: 5px 0;">│</div>
<div style="margin-bottom: 8px;">
<span style="display: inline-block; width: 38px; height: 38px; line-height: 38px; background-color: #E3F2FD; border: 3px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold; color: #2196F3; margin-right: 40px;">3</span>
<span style="display: inline-block; width: 38px; height: 38px; line-height: 38px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; color: #666;">10</span>
</div>
<div style="color: #999; margin: 5px 0; margin-left: -40px;">│</div>
<div style="margin-bottom: 8px;">
<span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 10px; color: #666;">1</span>
<span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E8F5E9; border: 3px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; color: #4CAF50; margin-right: 30px;">6</span>
<span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 10px; color: #666;">null</span>
<span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; color: #666;">14</span>
</div>
<div style="color: #999; margin: 5px 0; margin-left: 20px;">│</div>
<div style="margin-bottom: 8px; margin-left: 20px;">
<span style="display: inline-block; width: 32px; height: 32px; line-height: 32px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 10px; color: #666;">4</span>
<span style="display: inline-block; width: 32px; height: 32px; line-height: 32px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 30px; color: #666;">7</span>
<span style="display: inline-block; width: 32px; height: 32px; line-height: 32px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 10px; color: #666;">13</span>
<span style="display: inline-block; width: 32px; height: 32px; line-height: 32px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; color: #666;">null</span>
</div>
</div>
<div style="margin-top: 15px; padding: 10px; background-color: #fff; border-radius: 5px; font-size: 13px;">
<p style="margin: 0; font-weight: bold; color: #2196F3;">图例说明:</p>
<p style="margin: 3px 0 0 0; color: #666;"><span style="display: inline-block; width: 12px; height: 12px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; margin-right: 5px;"></span> 蓝色：访问路径上的节点</p>
<p style="margin: 3px 0 0 0; color: #666;"><span style="display: inline-block; width: 12px; height: 12px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; margin-right: 5px;"></span> 绿色：找到的目标节点</p>
</div>
</div>

<div style="background-color: #fff; border: 1px solid #E0E0E0; border-radius: 8px; padding: 15px; margin: 10px 0;">
<p style="margin: 0 0 10px 0; font-weight: bold; font-size: 15px;">查找步骤</p>
<table style="width: 100%; border-collapse: collapse; font-size: 14px;">
<thead>
<tr style="background-color: #F5F5F5;">
<th style="padding: 10px; text-align: center; border: 1px solid #E0E0E0;">步骤</th>
<th style="padding: 10px; text-align: center; border: 1px solid #E0E0E0;">当前节点</th>
<th style="padding: 10px; text-align: center; border: 1px solid #E0E0E0;">比较</th>
<th style="padding: 10px; text-align: center; border: 1px solid #E0E0E0;">决策</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; background-color: #E3F2FD;">1</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; font-weight: bold; color: #2196F3;">8</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; font-family: monospace;">6 &lt; 8</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0;">向左走</td>
</tr>
<tr>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; background-color: #E3F2FD;">2</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; font-weight: bold; color: #2196F3;">3</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; font-family: monospace;">6 &gt; 3</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0;">向右走</td>
</tr>
<tr>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; background-color: #E8F5E9;">3</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; font-weight: bold; color: #4CAF50;">6</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; font-family: monospace;">6 == 6</td>
<td style="padding: 10px; text-align: center; border: 1px solid #E0E0E0; font-weight: bold; color: #4CAF50;">找到！</td>
</tr>
</tbody>
</table>
</div>

<div style="background-color: #E8F5E9; border-left: 4px solid #4CAF50; padding: 12px; margin: 10px 0;">
<p style="margin: 0; font-weight: bold; color: #4CAF50;">查找成功</p>
<p style="margin: 5px 0 0 0; color: #666;">查找路径: <strong>8 → 3 → 6</strong> | 比较次数: <strong>3</strong></p>
</div>'''

print("文件修改脚本已创建")
print("请手动执行修改")

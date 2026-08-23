# 二叉搜索树文档优化修改方案

## 修改概述

本文档详细说明了二叉搜索树文档的四个部分优化方案，将ASCII图形转换为HTML可视化展示。

---

## 第1部分：查找路径可视化（第156-180行）

### 修改位置
- 文件：`002-二叉搜索树.md`
- 行号：156-180
- 标题：**查找路径可视化：**

### 原始内容（需要替换）
```markdown
**查找路径可视化：**

```
在以下 BST 中查找值 6:

              8
            /   \
           3     10
          / \      \
         1   6      14
            / \    /
           4   7  13

查找路径:
─────────────────────────────────────────────────────────────────
步骤   当前节点   比较           决策
─────────────────────────────────────────────────────────────────
 1       8      6 < 8         向左走
 2       3      6 > 3         向右走
 3       6      6 == 6        找到！
─────────────────────────────────────────────────────────────────

查找路径: 8 → 3 → 6
比较次数: 3
```
```

### 新内容（HTML可视化）

**查找路径可视化：**

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
</div>


### 修改要点
1. ✅ 使用HTML+CSS绘制树结构
2. ✅ 蓝色（#E3F2FD/#2196F3）标记访问路径节点：8、3
3. ✅ 绿色（#E8F5E9/#4CAF50）标记找到的目标节点：6
4. ✅ 使用表格展示查找步骤
5. ✅ 保留原有的mermaid流程图

---

## 第2部分：插入过程可视化（第215-250行）

### 修改位置
- 文件：`002-二叉搜索树.md`
- 行号：215-250
- 标题：**插入过程可视化：**

### 原始内容（需要替换）
```markdown
**插入过程可视化：**

```
在以下 BST 中插入值 5:

初始 BST:
              8
            /   \
           3     10
          / \      \
         1   6      14
            / \    /
           4   7  13

插入路径:
─────────────────────────────────────────────────────────────────
步骤   当前节点   比较        决策
─────────────────────────────────────────────────────────────────
 1       8      5 < 8      向左走
 2       3      5 > 3      向右走
 3       6      5 < 6      向左走
 4       4      5 > 4      向右走
 5      NULL    -          在此插入 5
─────────────────────────────────────────────────────────────────

插入后的 BST:
              8
            /   \
           3     10
          / \      \
         1   6      14
            / \    /
           4   7  13
            \
             5  ← 新插入的节点
```
```

### 新内容（HTML可视化）
详见下文...

### 修改要点
1. ✅ 使用HTML绘制初始BST
2. ✅ 使用HTML绘制插入后的BST
3. ✅ 用表格展示插入路径步骤
4. ✅ 绿色/橙色（#FFF3E0/#FF9800）高亮新节点5

---

## 第3部分：三种删除情况详解（第271-342行）

### 修改位置
- 文件：`002-二叉搜索树.md`
- 行号：271-342
- 标题：**三种删除情况详解：**

### 修改方案
将单个代码块拆分为三个 Material MkDocs 标签页：

```markdown
**三种删除情况详解：**

=== "情况1: 删除叶子节点"
    
    删除节点 1：
    
    <div style="display: flex; gap: 20px;">
    <div style="flex: 1; background-color: #F5F5F5; padding: 15px; border-radius: 8px;">
    <p style="margin: 0 0 10px 0; font-weight: bold;">删除前：</p>
    <div style="text-align: center; font-family: monospace;">
    <div style="margin-bottom: 5px;">
    <span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold;">3</span>
    </div>
    <div style="color: #999;">│</div>
    <div>
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #FFEBEE; border: 2px solid #F44336; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 20px;">1</span>
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">4</span>
    </div>
    </div>
    </div>
    <div style="flex: 1; background-color: #F5F5F5; padding: 15px; border-radius: 8px;">
    <p style="margin: 0 0 10px 0; font-weight: bold;">删除后：</p>
    <div style="text-align: center; font-family: monospace;">
    <div style="margin-bottom: 5px;">
    <span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold;">3</span>
    </div>
    <div style="color: #999;">│</div>
    <div>
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">4</span>
    </div>
    </div>
    </div>
    </div>
    
    <div style="background: #E8F5E9; padding: 10px; border-radius: 4px; margin-top: 15px;">
    ✅ 操作：直接删除节点 1
    </div>

=== "情况2: 删除只有一个子节点"
    
    删除节点 3（只有右子节点）：
    
    <div style="display: flex; gap: 20px;">
    <div style="flex: 1; background-color: #F5F5F5; padding: 15px; border-radius: 8px;">
    <p style="margin: 0 0 10px 0; font-weight: bold;">删除前：</p>
    <div style="text-align: center; font-family: monospace;">
    <div style="margin-bottom: 5px;">
    <span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #FFEBEE; border: 2px solid #F44336; border-radius: 50%; text-align: center; font-weight: bold;">3</span>
    </div>
    <div style="color: #999;">│</div>
    <div style="margin-bottom: 5px;">
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #FFF3E0; border: 2px solid #FF9800; border-radius: 50%; text-align: center; font-weight: bold;">4</span>
    </div>
    <div style="color: #999;">│</div>
    <div>
    <span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">5</span>
    </div>
    </div>
    </div>
    <div style="flex: 1; background-color: #F5F5F5; padding: 15px; border-radius: 8px;">
    <p style="margin: 0 0 10px 0; font-weight: bold;">删除后：</p>
    <div style="text-align: center; font-family: monospace;">
    <div style="margin-bottom: 5px;">
    <span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #FFF3E0; border: 2px solid #FF9800; border-radius: 50%; text-align: center; font-weight: bold;">4</span>
    </div>
    <div style="color: #999;">│</div>
    <div>
    <span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">5</span>
    </div>
    </div>
    </div>
    </div>
    
    <div style="background: #FFF3E0; padding: 10px; border-radius: 4px; margin-top: 15px;">
    ⚙️ 操作：用子节点 4 替换节点 3
    </div>

=== "情况3: 删除有两个子节点"
    
    删除节点 3（有两个子节点）：
    
    **步骤1**: 找到中序后继（右子树最小值）
    <div style="background: #E3F2FD; padding: 10px; border-radius: 4px; margin: 10px 0;">
    在右子树中找最左节点 → 节点 4
    </div>
    
    **步骤2**: 用后继值替换被删除节点
    <div style="background: #FFF3E0; padding: 10px; border-radius: 4px; margin: 10px 0;">
    节点 3 的值变为 4
    </div>
    
    **步骤3**: 删除后继节点（节点 4）
    <div style="background: #E8F5E9; padding: 10px; border-radius: 4px; margin: 10px 0;">
    后继节点是叶子或只有右子节点
    </div>
    
    <div style="display: flex; gap: 20px;">
    <div style="flex: 1; background-color: #F5F5F5; padding: 15px; border-radius: 8px;">
    <p style="margin: 0 0 10px 0; font-weight: bold;">删除前：</p>
    <div style="text-align: center; font-family: monospace;">
    <div style="margin-bottom: 5px;">
    <span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #FFEBEE; border: 2px solid #F44336; border-radius: 50%; text-align: center; font-weight: bold;">3</span>
    </div>
    <div style="color: #999;">│</div>
    <div>
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 20px;">1</span>
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold;">5</span>
    </div>
    <div style="color: #999; margin-left: 35px;">│</div>
    <div style="margin-left: 35px;">
    <span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #FFF3E0; border: 2px solid #FF9800; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 10px;">4</span>
    <span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">6</span>
    </div>
    </div>
    </div>
    <div style="flex: 1; background-color: #F5F5F5; padding: 15px; border-radius: 8px;">
    <p style="margin: 0 0 10px 0; font-weight: bold;">删除后：</p>
    <div style="text-align: center; font-family: monospace;">
    <div style="margin-bottom: 5px;">
    <span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #FFF3E0; border: 2px solid #FF9800; border-radius: 50%; text-align: center; font-weight: bold;">4</span>
    </div>
    <div style="color: #999;">│</div>
    <div>
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 20px;">1</span>
    <span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold;">5</span>
    </div>
    <div style="color: #999; margin-left: 35px;">│</div>
    <div style="margin-left: 35px;">
    <span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">6</span>
    </div>
    </div>
    </div>
    </div>
    
    <div style="background: #E3F2FD; padding: 10px; border-radius: 4px; margin-top: 15px;">
    🔄 操作：3 替换为 4，然后删除原来的 4
    </div>
```

### 修改要点
1. ✅ 使用Material MkDocs标签页语法（=== "标签名"）
2. ✅ 每种情况独立一个标签页
3. ✅ 使用HTML绘制删除前后的树结构对比
4. ✅ 使用颜色标记：
   - 红色（#FFEBEE/#F44336）：被删除的节点
   - 橙色（#FFF3E0/#FF9800）：替换节点
   - 蓝色（#E3F2FD/#2196F3）：中序后继查找路径
5. ✅ 缩进统一使用4个空格

---

## 第4部分：完整操作演示（约第375-481行）

### 修改位置
- 文件：`002-二叉搜索树.md`
- 行号：约375-481
- 标题：### 完整操作演示

### 修改方案
将ASCII演示转换为HTML步骤卡片：

```markdown
### 完整操作演示

操作序列: 插入 5, 3, 7, 1, 4, 6, 8, 删除 3

<div style="display: grid; gap: 15px;">

<div style="background: #F5F5F5; padding: 15px; border-radius: 8px; border-left: 4px solid #9E9E9E;">
<strong>步骤1: 初始状态</strong>
<pre style="margin: 10px 0 0 0; color: #666;">空树 (NULL)</pre>
</div>

<div style="background: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;">
<strong>步骤2: insert(5)</strong>
<div style="text-align: center; margin: 10px 0;">
<span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; color: white;">5</span>
</div>
</div>

<div style="background: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;">
<strong>步骤3: insert(3)</strong>
<p style="margin: 5px 0; color: #666; font-size: 13px;">3 &lt; 5, 插入左子树</p>
<div style="text-align: center; margin: 10px 0; font-family: monospace;">
<div><span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold;">5</span></div>
<div style="color: #999;">│</div>
<div><span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; color: white;">3</span></div>
</div>
</div>

<div style="background: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;">
<strong>步骤4: insert(7)</strong>
<p style="margin: 5px 0; color: #666; font-size: 13px;">7 &gt; 5, 插入右子树</p>
<div style="text-align: center; margin: 10px 0; font-family: monospace;">
<div><span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold;">5</span></div>
<div style="color: #999;">│</div>
<div>
<span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 20px;">3</span>
<span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; color: white;">7</span>
</div>
</div>
</div>

... (继续添加步骤5-9) ...

<div style="background: #FFEBEE; padding: 15px; border-radius: 8px; border-left: 4px solid #F44336;">
<strong>步骤9: delete(3)</strong>
<p style="margin: 5px 0; color: #666; font-size: 13px;">节点 3 有两个子节点，找中序后继 4</p>
<div style="text-align: center; margin: 10px 0; font-family: monospace;">
<div><span style="display: inline-block; width: 35px; height: 35px; line-height: 35px; background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 50%; text-align: center; font-weight: bold;">5</span></div>
<div style="color: #999;">│</div>
<div>
<span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #FFF3E0; border: 2px solid #FF9800; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 20px;">4</span>
<span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">7</span>
</div>
<div style="color: #999; margin-left: -35px;">│</div>
<div style="margin-left: -35px;">
<span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 10px;">1</span>
<span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold; margin-right: 10px;">6</span>
<span style="display: inline-block; width: 28px; height: 28px; line-height: 28px; background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 50%; text-align: center; font-weight: bold;">8</span>
</div>
</div>
</div>

<div style="background: #E3F2FD; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;">
<strong>最终结果</strong>
<p style="margin: 5px 0; color: #666; font-size: 13px;">中序遍历: 1, 4, 5, 6, 7, 8 (升序)</p>
<div style="text-align: center; margin: 10px 0; font-family: monospace;">
(最终树结构)
</div>
</div>

</div>
```

### 修改要点
1. ✅ 使用HTML步骤卡片，每个操作一个卡片
2. ✅ 使用颜色区分操作类型：
   - 绿色（#E8F5E9/#4CAF50）：插入操作
   - 红色（#FFEBEE/#F44336）：删除操作
   - 蓝色（#E3F2FD/#2196F3）：最终结果
3. ✅ 每个卡片包含操作说明和树结构展示
4. ✅ 最后展示最终结果和中序遍历

---

## 设计规范总结

### 颜色方案
- **蓝色系** `#E3F2FD` / `#2196F3` - 访问过的节点、信息
- **绿色系** `#E8F5E9` / `#4CAF50` - 找到、新插入、成功
- **橙色系** `#FFF3E0` / `#FF9800` - 当前操作、替换
- **红色系** `#FFEBEE` / `#F44336` - 删除、问题
- **灰色系** `#F5F5F5` / `#9E9E9E` - 容器背景、初始状态

### 样式规范
- **容器背景**: `#F5F5F5`
- **圆角**: `8px`（大容器）、`5px`（小元素）
- **内边距**: `15-20px`（容器）、`10-12px`（提示框）
- **字体**: 
  - `monospace` 用于树结构代码
  - `sans-serif` 用于说明文字
  - 字号：16px（标题）、14px（正文）、13px（说明）

### HTML规范
- ✅ `</p>`标签后不要留空行
- ✅ 所有style属性使用双引号
- ✅ 缩进统一使用2个空格（HTML）
- ✅ 标签页缩进使用4个空格（Markdown）

---

## 执行步骤

1. **备份原文件**
   ```bash
   cp 002-二叉搜索树.md 002-二叉搜索树.md.backup
   ```

2. **逐个修改四个部分**
   - 第1部分：查找路径可视化（第156-180行）
   - 第2部分：插入过程可视化（第215-250行）
   - 第3部分：三种删除情况详解（第271-342行）
   - 第4部分：完整操作演示（第375-481行）

3. **验证修改**
   - 检查HTML代码格式正确
   - 确认`</p>`后无空行
   - 验证===标签页语法正确
   - 测试在MkDocs中渲染效果

4. **提交修改**
   ```bash
   git add 002-二叉搜索树.md
   git commit -m "优化二叉搜索树文档可视化展示"
   ```

---

## 修改完成后的效果

### 第1部分效果
- HTML绘制的树结构，蓝色标记访问路径，绿色标记目标节点
- 表格展示查找步骤，清晰明了
- 保留mermaid流程图，在表格后面

### 第2部分效果
- 初始BST和插入后BST对比展示
- 表格展示插入路径步骤
- 橙色高亮新插入的节点

### 第3部分效果
- 三个标签页分别展示三种删除情况
- 每种情况都有删除前后的对比
- 使用不同颜色标记不同角色节点

### 第4部分效果
- 9个步骤卡片，展示完整操作过程
- 绿色标记插入，红色标记删除
- 最后展示最终结果和中序遍历

---

## 总结

通过将ASCII图形转换为HTML可视化展示，文档的可读性和美观度得到显著提升。新的展示方式：

1. ✅ 使用颜色编码，直观展示节点状态
2. ✅ 使用表格，清晰展示操作步骤
3. ✅ 使用标签页，分类展示不同情况
4. ✅ 使用步骤卡片，逐步展示操作过程
5. ✅ 保持文档其他内容不变
6. ✅ 符合用户偏好和设计规范

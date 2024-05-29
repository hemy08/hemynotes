# Body区域划分

## 一、预览

body区域准备划分两部分，左侧做出文件管理器页面，右侧是编辑区域，对于Markdown编辑来说，可以平方做预览区域。

![](images/20240529193806.png)

## 二、实现思路

在app.vue中进行处理，利用template，以及html相关的语言配置，先上学分为两部分，上面部分作为工作区域，下面部分作为状态栏。

工作区域划分两部分，文件管理器页面和编辑区域。

项目栏：包含文件资源管理器、文章大纲、绘图工具、PlantUML、Mermaid

- 文件资源管理器，中间区域显示文档信息，文件列表tree，编辑区域嵌入Markdown编辑器，并增加预览功能（可选）
- 文章大纲，中间区域显示Markdown-toc
- 绘图工具，中间区域显示简单的绘图工具，这个看看有没有比较成熟的绘图插件，右侧区域作为绘图区域
- PlantUML，中间区域显示PlantUML支持的绘图，点击后，在右侧区域显示语言原码，并且增加预览区域（可选）
- Mermaid，同上

状态栏暂时没想好显示啥，先保留：文件绝对路径、字数等信息

## 三、实现

在app.vue中进行处理，利用template，以及html相关的语言配置，先上学分为两部分，上面部分作为工作区域，下面部分作为状态栏。

<details>
<summary style="color:rgb(0,0,255);font-weight:bold">app.vue 参考</summary>
<blockcode><pre><code>
```vue
<template>
  <div id="editor-container">
    <!-- 应用工具栏和下发区域分割部分，2px高度，宽度与app一致 -->
    <div id="file-bar"></div>
    <!-- 整个工作区域 -->
    <div id="workspace-area" class="workspace-area">
      <!-- 左侧区域导航，固定宽度，放置图标，鼠标悬停显示详细信息 -->
      <div id="navi-tab" class="navi-tab">0</div>
      <!-- 中间资源管理显示区域，宽度可以调节 -->
      <div id="resource-area" class="resource-area">1</div>
      <!-- 资源管理器和编辑区域的宽度调节条 -->
      <div id="resizer-main" class="resizer-main">1</div>
      <!-- 右侧编辑区域 -->
      <div id="edit-area" class="edit-area">2222</div>
    </div>
    <!-- 状态栏区域，高度10px，宽度与app一致 -->
    <div id="status-bar" class="status-bar">0字节dsfdsafsdfasdfasdfasdfasdfasdfaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</div>
  </div>
</template>
```
</code></pre></blockcode></details>

区域的大小调节，可以自己根据需要进行调节
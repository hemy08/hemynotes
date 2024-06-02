# 引入markdown解析器

## 一、解析器选择

这里准备引入`markdown-it`、`markdown-it-vue`、`remarkable`、`marked`、`commonmark`几个，然后看看那个渲染的效果好一些，如果可以，想做成可选功能，由用户去选择使用哪个解析器。

### 1）安装--save

```
npm install --registry=https://registry.npmmirror.com --loglevel verbose markdown-it --save
npm install --registry=https://registry.npmmirror.com --loglevel verbose markdown-it-vue --save
npm install --registry=https://registry.npmmirror.com --loglevel verbose remarkable --save
npm install --registry=https://registry.npmmirror.com --loglevel verbose marked --save
npm install --registry=https://registry.npmmirror.com --loglevel verbose commonmark --save
```

安装完毕之后，`package.json`的`dependencies`会增加如下项目：

![](./images/1717032943720_image.png)

### 1）安装--save-dev（建议）

```
npm install --registry=https://registry.npmmirror.com --loglevel verbose markdown-it --save-dev
npm install --registry=https://registry.npmmirror.com --loglevel verbose markdown-it-vue --save-dev
npm install --registry=https://registry.npmmirror.com --loglevel verbose remarkable --save-dev
npm install --registry=https://registry.npmmirror.com --loglevel verbose marked --save-dev
npm install --registry=https://registry.npmmirror.com --loglevel verbose commonmark --save-dev
```

安装完毕之后，`package.json`的`devDependencies`会增加如下项目：

![](./images/1717033140779_image.png)


## 二、markdown-it解析器

这里的解析器使用的是markdown-it，在MdPreview组件中进行渲染，从外部传入content内容。

<details>
<summary style="color:rgb(0,0,255);font-weight:bold">MdPreview 参考</summary>
<blockcode><pre><code>
```vue
<template>
  <div v-html="renderedMarkdownContent"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, defineProps, watchEffect } from 'vue'
import MarkdownIt from 'markdown-it'
const props = defineProps({
  code: {
    type: String,
    default: ''
  }
})
const renderedMarkdownContent = ref('')
const md = MarkdownIt()
// 组件挂载时，进行初始渲染
onMounted(() => {
  updateMarkdown()
})
// 监听 props.code 的变化，并在变化时更新 Markdown
watchEffect(() => {
  updateMarkdown()
})
// 定义一个函数来更新 Markdown 的渲染
function updateMarkdown() {
  renderedMarkdownContent.value = md.render(props.code)
}
</script>
<style scoped></style>
```
</code></pre></blockcode></details>


### 三、效果

![](images/20240530225549.png)

解析器还不是很完善，可能需要加载一些其他的js，这个后续再慢慢研究，先把框架搞出来。

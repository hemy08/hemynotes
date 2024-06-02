# 支持mermaid渲染

## 一、markdown-it-mermaid

markdown-it-mermaid 这个是js开发的markdown-it插件，支持mermaid渲染。

试用了下，好像并不能进行渲染，因为本人使用的是Electron + Vue + Typescript开发的工具，发现并没有现成的支持markdown-it的插件。

个人的想法是：从编辑器获取mermaid部分字符，然后先渲染成html脚本，取其中的svg部分，再拿给markdown-it进行渲染。

或者可以直接自己开发一个内部的支持mermaid渲染的markdown-it的插件。

## 二、实现

后续补充
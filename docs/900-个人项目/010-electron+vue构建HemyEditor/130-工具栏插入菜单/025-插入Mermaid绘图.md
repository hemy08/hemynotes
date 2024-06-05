# 插入mermaid绘图

## 菜单栏

菜单栏的实现比较简单，就是向编辑区域插入文本块，文本块的内容就是对应的流程参考。

这里每个流程图都从官网拷贝了一个简单的示意图

以flowchart为例，定义一个模板文件flowchart.ts：

```typescript
export const flowchart =
  '```mermaid\n' +
  'flowchart TB\n' +
  '    c1-->a2\n' +
  '    subgraph one\n' +
  '    a1-->a2\n' +
  '    end\n' +
  '    subgraph two\n' +
  '    b1-->b2\n' +
  '    end\n' +
  '    subgraph three\n' +
  '    c1-->c2\n' +
  '    end\n' +
  '```'
```

再定义一个mermaid.ts：

```typescript
import { flowchart } from './flowchart'

export {
    flowchart
}
```

其他的参考这个实现就行，在插入的时候，只导出mermaid.ts即可。

## 预览区渲染

渲染的话可能也有点麻烦，因为是用的Typescript，和vue，貌似没有比较成熟的插件，可以考虑进行内置处理。
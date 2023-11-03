# <center> HEMY NOTES BOOKS  </center>

-----------------

## 一、配置pages\_config.json

这个是自定义的配置文件，在python脚本中会读取，文件名不可更改。

**<font color="red">注意文件必须是UTF-8编码的。</font>**

![](./images/1690959910792_image.png)


#### 1) site\_name

网站名称，可以中文或者英文。这个是显示在文档的上方的。

![site_name](images/site_name.png)

#### 2) site\_description

网站描述，当鼠标停留在图标上的时候，会显示出来。

![site_description](images/site_description.png)


#### 3) repo\_url

pages仓库地址，这个在文档右上方显示，是个按钮，鼠标点击可以跳转到仓库。

![repo_url](images/repo_url.png)

#### 4) copyright

copyright声明，这个是显示在网页的左下方的。

![copyright](images/copyright.png)

#### 5) ignore\_dirs

忽略的文件夹列表，多个目录以英文的分号（“;”）分隔。目的是在生成mkdocs.yml时，忽略对应的文件夹。

这里要写文件夹的全名。

这里列表配置的文件夹，在生成mkdocs.yml文件时，不会生成在nav中。即不在网站上显示。

#### 6) ignore\_file\_types

要忽略的文件类型，这里是文件后缀，多个类型以英文的分号（“;”）分隔。

在生成mkdocs.yml文件时，遇到这里后缀的文件，会跳过，不会生成在nav中。

#### 7) ignore\_files

要忽略的文件，这里是文件全名，多个文件以英文的分号（“;”）分隔。

这里列表配置的文件，在生成mkdocs.yml文件时，会跳过，不会生成在nav中。

#### 8) chapter infos

**<font color="red">配置章节信息，当前仅包含相对路径，仓库地址以及子文档根目录，相对路径不可重复</font>**

生成的mkdoc.yml会以这里定义的章节顺序，生成nav信息。这里的路径是mkdocs.yml的同级路径。

![](./images/image.png)

#### 9）file name convert

这里配置文件名的转换列表。

**<font color="red">注意文件必须是UTF-8编码的。</font>**

有些文件名、文件夹名称在本地会比较长。这样的名称在生成mkdocs.yml时，如果不做特殊处理，显示出来的文件名会很长，不是很美观。

这个配置文件就是专门干这个事情的，把长文件名转换为短文件名。

![file_name_convert](images/fine_name_convert.png)

如图这种的文件名，我们可以配置转换成短文件名，这样在网页上显示就不会换行了。

#### 10) external links

外部链接，这里是与本地文件作为导航一起显示在导航栏的，所以不建议设置太多。

![](./images/1692966114237_image.png)

如图，这俩再本仓库实际是不存在的

#### 11）extra social
 
友情链接，配置的时候，注意图标的使用。

可以去[https://fontawesome.com/icons](https://fontawesome.com/icons)上进行查询

![](./images/1692965894846_image.png)

#### 12) mkdocs配置 theme、plugins、extra、extra_css、extra_javascript、markdown_extensions

这些都是mkdocs的主题配置。

theme 是配置主题名称，主题的图标、特性等

plugins 是mkdocs插件配置

extra 是扩展配置

extra_css 是扩展css样式配置，可以配置一些mkdocs的样式，比如标题颜色、字体等，网页宽度

extra_javascript 扩展js脚本，比如配置支持mermaid

markdown_extensions markdown扩展配置，比如支持emoji、mermaid

如果实在不会，可以参考本案例实现。


## 二、pages_config.json 参考

<details>
<summary style="color:rgb(0,0,255);font-weight:bold">pages_config.json 参考</summary>
<blockcode><pre><code>
```json
{
    "site name": "HEMY NOTES",
    "site description": "HEMY's Personal Learning Notes",
    "copyright": "Copyright &copy; 2021-2029 JunWei Zhao",
    "HOME": "https://openx.huawei.com/mkdocs/project/1186/hemynotes/docs/site/",
    "repo url": "https://codehub-dg-y.huawei.com/hemyzhao/pages/hemynotes.git",
    "ignore dirs": ".git;.idea;.vscode;images;image;resource;.gitignore;public_resources;figures;public_sys-resources;themes;docs;site;vx_notebook;document",
    "ignore file types": ".git;.png;.gif;.txt;.yml;.yaml;.json",
    "ignore files": "Contents.md;SUMMARY.md;vx.json;.gitignore",
    "chapter infos": {
        "ResourceCollation": "\\ResourceCollation",
        "5GCoreLearning": "\\5GCoreLearning",
        "5GCorePlatform": "\\5GCorePlatform",
        "5GCoreSkill": "\\5GCoreSkill",
        "5GCoreCases": "\\5GCoreCases",
        "ProductMEP": "\\ProductMEP",
        "ProductSFIP": "\\ProductSFIP",
        "DeveloperTest": "\\DeveloperTest",
        "SpecSuggest": "\\SpecSuggest",
        "Appendices": "\\Appendices"
    },
    "file name convert": {
        "00_SFIP 5G 问题定位自查手册": "SFIP_5G问题定位自查手册",
        "01_同时复位3个sfmu-pod之后，第三方app实例丢失": "复位sfmu-pod后App实例丢失",
        "SFIP_问题定位自查手册": "SFIP问题定位自查",
        "00 SFIP 5G特性列表": "5G特性列表",
        "00 运维管理": "运维管理总览",
        "00 工程命令列表": "SFIP 工程命令列表",
        "00 README": "总览",
        "00-README": "总览",
        "00_README": "总览",
        "04_sfmu-pod联动复位-01": "sfmu-pod联动复位",
        "05_down掉SBI上的eth4": "ddns复位回迁时容器复位",
        "00_APPF_FAQ_LIST": "APPF问题定位自查手册",
        "010-ResourceCollation": "各类资源整理",
        "020-5GCoreLearning": "5GCore 学习",
        "030-5GCorePlatform": "5GCore 平台",
        "040-5GCoreSkill": "5GCore 技能",
        "050-5GCoreCases": "5GCore 案例",
        "140-ProductMEP": "5GCore MEP",
        "150-ProductSFIP_5G": "5GCore SFIP",
        "160-ProductSFIP": "SFIP",
        "300-DeveloperTest": "开发者测试",
        "910-SpecSuggest": "规范建议",
        "999-Appendices": "附录",
        "ResourceCollation": "各类资源整理",
        "5GCoreLearning": "5GCore 学习",
        "5GCorePlatform": "5GCore 平台",
        "5GCoreSkill": "5GCore 技能",
        "5GCoreCases": "5GCore 案例",
        "ProductMEP": "MEP",
        "ProductSFIP": "SFIP",
        "DeveloperTest": "开发者测试",
        "SpecSuggest": "规范建议",
        "Appendices": "附录"
    },
    "external links": {
        "SKILL_PAGES": "https://openx.huawei.com/mkdocs/project/1186/hemyskills/docs/site/"
    },
    "theme": {
        "favicon": "themes/images/shuye.png",
        "feature": {
            "tabs": "true"
        },
        "features": [
            "navigation.tracking",
            "navigation.tabs",
            "navigation.indexes",
            "navigation.prune",
            "navigation.top",
            "toc.follow",
            "header.autohide",
            "search.share",
            "search.suggest",
            "search.highlight"
        ],
        "icon": {
            "logo": "material/library",
            "note": "octicons/tag-16",
            "abstract": "octicons/checklist-16",
            "info": "octicons/info-16",
            "tip": "octicons/squirrel-16",
            "success": "octicons/check-16",
            "question": "octicons/question-16",
            "warning": "octicons/alert-16",
            "failure": "octicons/x-circle-16",
            "danger": "octicons/zap-16",
            "bug": "octicons/bug-16",
            "example": "octicons/beaker-16",
            "quote": "octicons/quote-16"
        },
        "language": "zh",
        "name": "material",
        "palette": {
            "scheme": "default"
        }
    },
    "plugins": {
        "search": {
            "lang": [
                "en",
                "ru",
                "zh",
                "ja"
            ],
            "separator": "[\\s\\u200b\\-]"
        }
    },
    "extra": {
        "search": {
            "language": "en, jp"
        },
        "social": [
            {
                "icon": "fontawesome/brands/github",
                "link": "https://codehub-y.huawei.com/hemyzhao/pages/hemyskills/home",
                "name": "hemyskills"
            }, {
                "icon": "fontawesome/solid/paper-plane",
                "link": "junwei.zhao@huawei.com",
                "name": "email"
            }
        ]
    },
    "extra_css": [
        "themes/css/custom.css",
        "themes/css/simpleLightbox.min.css"
    ],
    "extra_javascript": [
        "themes/js/custom.js",
        "themes/js/simpleLightbox.min.js",
        "themes/js/optionalConfig.js",
        "themes/js/mermaidloader.js",
        "themes/js/umlconvert.js",
        "https://unpkg.com/mermaid@10.0.2/dist/mermaid.esm.min.mjs",
        "https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.17.1/flowchart.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/raphael/2.3.0/raphael.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.13.6/underscore-min.js",
        "https://cdn.jsdelivr.net/npm/@mermaid-js/mermaid-mindmap@9.3.0/dist/mermaid-mindmap.esm.min.mjs"
    ],
    "markdown_extensions": [
        "admonition",
        "footnotes",
        "meta",
        "def_list",
        "pymdownx.caret",
        "pymdownx.critic",
        "pymdownx.details",
        "pymdownx.snippets",
        "tables",
        "pymdownx.mark",
        "pymdownx.inlinehilite",
        "pymdownx.smartsymbols",
        "pymdownx.tilde",
        "attr_list",
        "md_in_html",
        {
            "pymdownx.arithmatex": {
                "generic": true
            }
        }, {
            "pymdownx.emoji": {
                "emoji_generator": "!!python/name:materialx.emoji.to_svg",
                "emoji_index": "!!python/name:materialx.emoji.twemoji"
            }
        }, {
            "pymdownx.highlight": {
                "anchor_linenums": true,
                "line_spans": "__span",
                "pygments_lang_class": true
            }
        }, {
            "pymdownx.magiclink": {
                "repo_url_shorthand": true,
                "user": "squidfunk",
                "repo": "mkdocs-material"
            }
        }, {
            "pymdownx.tabbed": {
                "alternate_style": true
            }
        }, {
            "pymdownx.tasklist": {
                "custom_checkbox": true
            }
        }, {
            "codehilite": {
                "guess_lang": false,
                "linenums": false
            }
        }, {
            "toc": {
                "permalink": true
            }
        }, {
            "pymdownx.betterem": {
                "smart_enable": "all"
            }
        }, {
            "pymdownx.emoji": {
                "emoji_generator": "!!python/name:pymdownx.emoji.to_png"
            }
        }, {
            "pymdownx.superfences": {
                "custom_fences": [
                    {
                        "name": "mermaid",
                        "class": "mermaid",
                        "format": "!!python/name:pymdownx.superfences.fence_code_format"
                    }, {
                        "name": "uml-flowchart",
                        "class": "flow",
                        "format": "!!python/name:pymdownx.superfences.fence_code_format"
                    }, {
                        "name": "sequence",
                        "class": "sequence",
                        "format": "!!python/name:pymdownx.superfences.fence_code_format"
                    }
                ],
                "preserve_tabs": true
            }
        }, {
            "pymdownx.highlight": {
                "anchor_linenums": true
            }
        }
    ]
}
```
</code></pre></blockcode></details>
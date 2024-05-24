# mkdocs支持mermaid配置

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-05-31</span>

参考： [https://facelessuser.github.io/pymdown-extensions/extras/mermaid/](https://facelessuser.github.io/pymdown-extensions/extras/mermaid/)


## 配置mkdoc.yaml

首先，需要配置mkdoc.yaml文件。配置插件以及扩展脚本。

<details>
<summary style="color:rgb(0,0,255)"><b>mkdoc.yaml配置mermaid示例</b></summary>
<blockcode><pre><code>
```yaml
theme:
  # 主题需要换成material，看帖子上说的，本人mkdocs一直用的这个主题
  name: material
#
# 扩展配置，我是用脚本生成的yaml，这部分加上不太好处理，就没加，只使能了pymdownx.superfences
markdown_extensions:
  - pymdownx.superfences:
      preserve_tabs: true
      custom_fences:
        # Mermaid diagrams
        - name: mermaid
          class: mermaid
          # 注意这里后面的字符串两边不能有任何符号
          format: !!python/name:pymdownx.superfences.fence_code_format
extra_css:
  - themes/css/custom.css
 
# 扩展脚本，这里得配置下
extra_javascript:
  - themes/stylesheets/custom.js
  # mermaid的配置脚本，字体大小，图表颜色等。
  - themes/js/optionalConfig.js\
  # mermaid的加载脚本，也可以在这里配置mermaid
  - themes/js/mermaidloader.js
  - themes/js/umlconvert.js
  # mermaid渲染
  - https://unpkg.com/mermaid@10.0.2/dist/mermaid.esm.min.mjs
  - https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.17.1/flowchart.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/raphael/2.3.0/raphael.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.13.6/underscore-min.js
  - https://cdn.jsdelivr.net/npm/@mermaid-js/mermaid-mindmap@9.3.0/dist/mermaid-mindmap.esm.min.mjs
```
</code></pre></blockcode></details>


<details>
<summary style="color:rgb(0,0,255)"><b>optionalConfig.js示例</b></summary>
<blockcode><pre><code>
```javascript
<!-- base,dark,forest,neutral,default -->
window.mermaidConfig = {
    startOnLoad: true,
    theme: "default",
    themeVariables: {
        fontSize:"28px"
    },
    flowchart: {
        htmlLabels: false,
        useMaxWidth: false
    },
    er: {
        useMaxWidth: false
    },
    sequence: {
        useMaxWidth: false,
        noteFontWeight: "20px",
        actorFontSize: "28px",
        messageFontSize: "22px"
    },
    journey: {
        useMaxWidth: false
    },
    gitGraph: {
        useMaxWidth: false
    }
}
```
</code></pre></blockcode></details>

<details>
<summary style="color:rgb(0,0,255)"><b>mermaidloader.js示例</b></summary>
<blockcode><pre><code>
```javascript
function _typeof(obj) {
    "@babel/helpers - typeof";
    if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
        _typeof = function _typeof(obj) {
            return typeof obj;
        };
    } else {
        _typeof = function _typeof(obj) {
            return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol": typeof obj;
        };
    }
    return _typeof(obj);
}
 
(function() {
    'use strict';
    
    function _classCallCheck(instance, Constructor) {
        if (! (instance instanceof Constructor)) {
            throw new TypeError("Cannot call a class as a function");
        }
    }
    
    function _inherits(subClass, superClass) {
        if (typeof superClass !== "function" && superClass !== null) {
            throw new TypeError("Super expression must either be null or a function");
        }
        
        subClass.prototype = Object.create(superClass && superClass.prototype, {
            constructor: {
                value: subClass,
                writable: true,
                configurable: true
            }
        });
        if (superClass) _setPrototypeOf(subClass, superClass);
    }
    
    function _getPrototypeOf(o) {
        _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf: function _getPrototypeOf(o) {
            return o.__proto__ || Object.getPrototypeOf(o);
        };
        return _getPrototypeOf(o);
    }
    
    function _setPrototypeOf(o, p) {
        _setPrototypeOf = Object.setPrototypeOf ||
        function _setPrototypeOf(o, p) {
            o.__proto__ = p;
            return o;
        };
        
        return _setPrototypeOf(o, p);
    }
    
    function _isNativeReflectConstruct() {
        if (typeof Reflect === "undefined" || !Reflect.construct) return false;
        if (Reflect.construct.sham) return false;
        if (typeof Proxy === "function") return true;
        
        try {
            Date.prototype.toString.call(Reflect.construct(Date, [],
            function() {}));
            return true;
        } catch(e) {
            return false;
        }
    }
    
    function _construct(Parent, args, Class) {
        if (_isNativeReflectConstruct()) {
            _construct = Reflect.construct;
        } else {
            _construct = function _construct(Parent, args, Class) {
                var a = [null];
                a.push.apply(a, args);
                var Constructor = Function.bind.apply(Parent, a);
                var instance = new Constructor();
                if (Class) _setPrototypeOf(instance, Class.prototype);
                return instance;
            };
        }
        
        return _construct.apply(null, arguments);
    }
    
    function _isNativeFunction(fn) {
        return Function.toString.call(fn).indexOf("[native code]") !== -1;
    }
    
    function _wrapNativeSuper(Class) {
        var _cache = typeof Map === "function" ? new Map() : undefined;
        
        _wrapNativeSuper = function _wrapNativeSuper(Class) {
            if (Class === null || !_isNativeFunction(Class)) return Class;
            
            if (typeof Class !== "function") {
                throw new TypeError("Super expression must either be null or a function");
            }
            
            if (typeof _cache !== "undefined") {
                if (_cache.has(Class)) return _cache.get(Class);
                _cache.set(Class, Wrapper);
            }
            
            function Wrapper() {
                return _construct(Class, arguments, _getPrototypeOf(this).constructor);
            }
            
            Wrapper.prototype = Object.create(Class.prototype, {
                constructor: {
                    value: Wrapper,
                    enumerable: false,
                    writable: true,
                    configurable: true
                }
            });
            return _setPrototypeOf(Wrapper, Class);
        };
        
        return _wrapNativeSuper(Class);
    }
    
    function _assertThisInitialized(self) {
        if (self === void 0) {
            throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
        }
        return self;
    }
    
    function _possibleConstructorReturn(self, call) {
        if (call && (_typeof(call) === "object" || typeof call === "function")) {
            return call;
        }
        return _assertThisInitialized(self);
    }
    
    function _createSuper(Derived) {
        var hasNativeReflectConstruct = _isNativeReflectConstruct();
        
        return function _createSuperInternal() {
            var Super = _getPrototypeOf(Derived),
            result;
            
            if (hasNativeReflectConstruct) {
                var NewTarget = _getPrototypeOf(this).constructor;
                result = Reflect.construct(Super, arguments, NewTarget);
            } else {
                result = Super.apply(this, arguments);
            }
            return _possibleConstructorReturn(this, result);
        };
    }
    /* Notes (as of Mermaid 8.7.0):
   * - Gantt: width is always relative to the parent, if you have a small parent, the chart will be squashed.
   *   Can't help it.
   * - Journey: Suffers from the same issues that Gantt does.
   * - Pie: These charts have no default height or width. Good luck pinning them down to a reasonable size.
   * - Git: The render portion is agnostic to the size of the parent element. But padding of the SVG is relative
   *   to the parent element. You will never find a happy size.
   */
   
    /**
   * Targets special code or div blocks and converts them to UML.
   * @param {string} className is the name of the class to target.
   * @return {void}
   */
   
    var uml = function uml(className) {
        // Custom element to encapsulate Mermaid content.
        var MermaidDiv =
        /*#__PURE__*/
        function(_HTMLElement) {
            _inherits(MermaidDiv, _HTMLElement);
            var _super = _createSuper(MermaidDiv);
            /**
            * Creates a special Mermaid div shadow DOM.
            * Works around issues of shared IDs.
            * @return {void}
            */
            
            function MermaidDiv() {
                var _this;
                _classCallCheck(this, MermaidDiv);
                _this = _super.call(this); // Create the Shadow DOM and attach style
                var shadow = _this.attachShadow({
                    mode: "open"
                });
                
                var style = document.createElement("style");
                style.textContent = "\n      :host {\n        display: block;\n        line-height: initial;\n        font-size: 16px;\n      }\n      div.mermaid {\n        margin: 0;\n        overflow: visible;\n      }";
                shadow.appendChild(style);
                return _this;
            }
            
            return MermaidDiv;
        } (
        /*#__PURE__*/
        _wrapNativeSuper(HTMLElement));
        
        if (typeof customElements.get("mermaid-div") === "undefined") {
            customElements.define("mermaid-div", MermaidDiv);
        }
        
        var getFromCode = function getFromCode(parent) {
            // Handles <pre><code> text extraction.
            var text = "";
            for (var j = 0; j < parent.childNodes.length; j++) {
                var subEl = parent.childNodes[j];
                if (subEl.tagName.toLowerCase() === "code") {
                    for (var k = 0; k < subEl.childNodes.length; k++) {
                        var child = subEl.childNodes[k];
                        var whitespace = /^\s*$/;
                        if (child.nodeName === "#text" && !whitespace.test(child.nodeValue)) {
                            text = child.nodeValue;
                            break;
                        }
                    }
                }
            }
            
            return text;
        }; // We use this to determine if we want the dark or light theme.
        // This is specific for our MkDocs Material environment.
        // You should load your configs based on your own environment's needs.
        var defaultConfig = {
            startOnLoad: true,
            theme: "default",
            flowchart: {
                htmlLabels: false
            },
            er: {
                useMaxWidth: false
            },
            sequence: {
                useMaxWidth: false,
                noteFontWeight: "20px",
                actorFontSize: "20px",
                messageFontSize: "22px"
            }
        };
        mermaid.mermaidAPI.globalReset(); // Non Material themes should just use "default"
        var scheme = null;
        
        try {
            scheme = document.querySelector("[data-md-color-scheme]").getAttribute("data-md-color-scheme");
        } catch(err) {
            scheme = "default";
        }
        
        var config = typeof mermaidConfig === "undefined" ? defaultConfig: mermaidConfig[scheme] || mermaidConfig["default"] || defaultConfig;
        mermaid.initialize(config); // Find all of our Mermaid sources and render them.
        var blocks = document.querySelectorAll("pre.".concat(className, ", mermaid-div"));
        var surrogate = document.querySelector("html");
        var _loop = function _loop(i) {
            var block = blocks[i];
            var parentEl = block.tagName.toLowerCase() === "mermaid-div" ? block.shadowRoot.querySelector("pre.".concat(className)) : block; // Create a temporary element with the typeset and size we desire.
            // Insert it at the end of our parent to render the SVG.
            var temp = document.createElement("div");
            temp.style.visibility = "hidden";
            temp.style.display = "display";
            temp.style.padding = "0";
            temp.style.margin = "0";
            temp.style.lineHeight = "initial";
            temp.style.fontSize = "20px";
            surrogate.appendChild(temp);
            
            try {
                mermaid.mermaidAPI.render("_mermaind_".concat(i), getFromCode(parentEl),
                function(content) {
                    var el = document.createElement("div");
                    el.className = className;
                    el.innerHTML = content; // Insert the render where we want it and remove the original text source.
                    // Mermaid will clean up the temporary element.
                    var shadow = document.createElement("mermaid-div");
                    shadow.shadowRoot.appendChild(el);
                    block.parentNode.insertBefore(shadow, block);
                    parentEl.style.display = "none";
                    shadow.shadowRoot.appendChild(parentEl);
                    
                    if (parentEl !== block) {
                        block.parentNode.removeChild(block);
                    }
                },
                temp);
            } catch(err) {} // eslint-disable-line no-empty
            if (surrogate.contains(temp)) {
                surrogate.removeChild(temp);
            }
        };
        
        for (var i = 0; i < blocks.length; i++) {
            _loop(i);
        }
    };
    
    (function() {
        var onReady = function onReady(fn) {
            document.addEventListener("DOMContentLoaded", fn);
            document.addEventListener("DOMContentSwitch", fn);
        };
        
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === "attributes") {
                    var scheme = mutation.target.getAttribute("data-md-color-scheme");
                    if (!scheme) {
                        scheme = "default";
                    }
                    localStorage.setItem("data-md-color-scheme", scheme);
                    if (typeof mermaid !== "undefined") {
                        uml("mermaid");
                    }
                }
            });
        });
        onReady(function() {
            observer.observe(document.querySelector("body"), {
                attributeFilter: ["data-md-color-scheme"]
            });
            if (typeof mermaid !== "undefined") {
                uml("mermaid");
            }
        });
    })();
})();
```
</code></pre></blockcode></details>

<details>
<summary style="color:rgb(0,0,255)"><b>umlconvert.js示例</b></summary>
<blockcode><pre><code>
```javascript
(function (document) {
    function convertUML(className, converter, settings) {
        var charts = document.querySelectorAll("pre." + className + ',div.' + className),
            arr = [],
            i, j, maxItem, diagaram, text, curNode,
            isPre;
 
        // Is there a settings object?
        if (settings === void 0) {
            settings = {};
        }
 
        // Make sure we are dealing with an array
        for(i = 0, maxItem = charts.length; i < maxItem; i++) arr.push(charts[i]);
 
        // Find the UML source element and get the text
        for (i = 0, maxItem = arr.length; i < maxItem; i++) {
            isPre = arr[i].tagName.toLowerCase() == 'pre';
            if (isPre) {
                // Handles <pre><code>
                childEl = arr[i].firstChild;
                parentEl = childEl.parentNode;
                text = "";
                for (j = 0; j < childEl.childNodes.length; j++) {
                    curNode = childEl.childNodes[j];
                    whitespace = /^\s*$/;
                    if (curNode.nodeName === "#text" && !(whitespace.test(curNode.nodeValue))) {
                        text = curNode.nodeValue;
                        break;
                    }
                }
                // Do UML conversion and replace source
                el = document.createElement('div');
                el.className = className;
                parentEl.parentNode.insertBefore(el, parentEl);
                parentEl.parentNode.removeChild(parentEl);
            } else {
                // Handles <div>
                el = arr[i];
                text = el.textContent || el.innerText;
                if (el.innerText){
                    el.innerText = '';
                } else {
                    el.textContent = '';
                }
            }
            diagram = converter.parse(text);
            diagram.drawSVG(el, settings);
        }
    };
 
    function onReady(fn) {
        if (document.addEventListener) {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            document.attachEvent('onreadystatechange', function() {
                if (document.readyState === 'interactive')
                    fn();
            });
        }
    }
 
    onReady(function(){
        convertUML('uml-flowchart', flowchart);
        convertUML('uml-sequence-diagram', Diagram, {theme: 'simple'});
    });
})(document);
```
</code></pre></blockcode></details>

## mkdocs文档编写


[流程图绘制](004-流程图绘制.md)

[mermaid 语法](http://www.manongjc.com/detail/52-gwmipkfyzvebaax.html)

[mermaid.js](https://mermaid.js.org/intro/)

[https://cdnjs.com/](https://cdnjs.com/libraries/mermaid)

[Mermaid画图教程](https://blog.csdn.net/weixin_44360592/article/details/109526990)
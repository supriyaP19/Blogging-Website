!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t(require("lodash"));else if("function"==typeof define&&define.amd)define(["lodash"],t);else{var n="object"==typeof exports?t(require("lodash")):t(e.lodash);for(var r in n)("object"==typeof exports?exports:e)[r]=n[r]}}(this,function(e){return function(e){var t={};function n(r){if(t[r])return t[r].exports;var i=t[r]={i:r,l:!1,exports:{}};return e[r].call(i.exports,i,i.exports,n),i.l=!0,i.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)n.d(r,i,function(t){return e[t]}.bind(null,i));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=105)}({0:function(t,n){t.exports=e},105:function(e,t,n){"use strict";var r=n(106);e.exports={siteButtonLayout:r}},106:function(e,t,n){"use strict";var r=n(0),i=new WeakMap,a=function(e){var t=e.getAttribute("id"),n=e.querySelector("#"+t+"label"),a=function(e){return{data:function(t){return e.dataset[t]},attr:function(t){return e.getAttribute(t)}}}(e),o=a.data("width"),u=a.data("height"),l=i.get(e)||{},d=l.prevWidth,f=l.prevMinWidth,c=l.prevText,s=n.offsetHeight,p=n.offsetWidth,g=n.innerHTML,m=a.data("shouldUseFlex"),h=window.getComputedStyle(e),v=window.getComputedStyle(n),b=function(e){return e.minHeight&&Boolean(parseInt(e.minHeight,10))}(h)?parseInt(h.minHeight,10):s,y=m?p:p+function(e){return parseInt(e.marginRight,10)+parseInt(e.marginLeft,10)}(v),x=a.data("shouldPreventWidthMeasurement"),j=o,w=u,M=Math.max(w,b),S=j;x||(S=function(e){return e!==c}(g)&&function(e){return e<f}(y)&&d===f&&p>0?y:Math.max(S,y));var P={align:a.attr("data-align"),margin:parseInt(a.attr("data-margin"),10),text:g,label:{verticalPadding:function(e){return parseInt(e.paddingTop,10)+parseInt(e.paddingBottom,10)}(v)}},I=p+P.margin>S;if("center"!==P.align){var O=m?"margin":"margin-"+P.align;P.label[O]=I?S-p:P.margin}var T={height:M,minHeight:b};x||(T.width=S);return i.set(e,{prevText:P.text,prevMinWidth:y,prevWidth:S}),[{node:e,type:"css",changes:T},{node:n,type:"css",changes:function(){var e=void 0;if(m){e={};var t=P.align;return"center"!==t&&P.label.margin&&(e["margin-"+t]=P.label.margin),e}return e={"line-height":M-P.label.verticalPadding+"px"},r.reduce(["margin-left","margin-right"],function(e,t){return r.isUndefined(P.label[t])||(e[t]=P.label[t]),e},e)}()}]};a.compType="wysiwyg.viewer.components.SiteButton",e.exports=a}})});
//# sourceMappingURL=santa-components-layout.prod.js.map
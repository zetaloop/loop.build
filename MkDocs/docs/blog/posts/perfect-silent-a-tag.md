---
date:
  created: 2024-06-06 14:57:02
categories:
  - 网页
  - HTML
  - JS
---

# 一个完美的非跳转 a 标签

有时候我们就是需要一个划上去有悬浮信息的 `<a>` 标签，但是又不能让他真的可以点击。<br>
一种常见的做法是 `<a href="javascript:void(0);">`，这样会显示一个 `javascript:void(0);` 的链接，不好看。<br>
还有一种做法是，`<a href="#">` + 阻止 `click` 事件默认行为，这样会在地址栏留下 `#`，也不好看。

本文介绍一种不会在地址栏或链接栏留下任何痕迹的 `<a>` 标签写法。
<!-- more -->
## 首先
让我们在这儿放一个链接：<br>
[这是一个正常的链接 `<a href="https://github.com/zetaloop">`](https://github.com/zetaloop "点击跳转到 GitHub")

但是，有时候我们只需要它有一个悬停提示，但是不需要真正可以跳转。对比以下常见方案：<br>
[这是一个非跳转链接 `<a href="javascript:void(0);">`](javascript:void(0); "点了啥也不做，但是悬停会在左下角显示 <code>javascript:void(0);</code>，并且这个定制悬浮栏会卡住")<br>
[这是一个非跳转链接 `<a href="#">`](# "点了会在地址栏留下 <code>#</code>，并且页面会跳到顶部") (1)
{ .annotate }

1.  如果要加上阻止 `click` 事件默认行为：
    1. `#!html <a href="#" onlick="return false;">`
       似乎无效
    2. `#!js addEventListener("click", e => e.preventDefault());`
       会导致悬浮栏失效，以及一些奇怪的 bug

    Markdown 中不便编写 JS 代码，这里暂不演示。

上面的方案多少都有些缺憾，我们需要一个完美的方案。

## 完美的呢？
```html
<a class="silent">这是一个完美的链接</a>
```
```js
document.querySelectorAll(".silent").forEach(link => {
  link.style.cursor = "auto";  // 把光标形状改为默认（原本是👆），提示用户这个不能点
  link.addEventListener("click", function (e) {
    e.stopImmediatePropagation();  // 立即阻止点击事件
  });
});
```
[这是一个完美的非跳转链接]("它只有悬停提示而没有点击功能")

## 更多实例

#### Software <!-- [md:version]("2020/20/20 v1.2.3<br>增加了三个特性") v1.2.3 --> <!-- [md:autoupdate]("自动更新") --> { data-toc-label="" }

<code>&nbsp;<!-- [md:locked]("被骗啦") -->&nbsp;滑动解锁->&nbsp;</code>

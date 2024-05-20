---
date:
    created: 2024-05-21 04:15:46
authors:
    - fox
categories:
    - 汉化
    - Python
    - Python IDLE
    - Bug
    - Hack
---

# IDLE 的逆天 Bug

## 前言

这几天正在做 IDLE 的汉化，打算弄一个 `pip install idle_cn` 就可以自动改成中文的模块，方便教学使用。（高中那会儿教 Python 都是用这个 IDLE）

做的时候发现一个非常奇怪的 Bug，在编辑器中，以中文输入法状态下输入某些字母，不仅文字会消失，而且会触发奇奇怪怪的功能。_（准确来说这么几年过来都有这个 Bug，老师同学一直没办法）_

<!-- more -->

## 开局

具体来说，这四个按键，按了会触发别的功能。

```plain title="就这四个"
R -> 搜索
T -> 运行
Y -> Alt
P -> 打开在线文档
```

简单搜寻无果，遂直接全局监控按键事件。

```python3 title="editor.py"
self.text.bind('<KeyPress>', lambda event: print(f'Press {event.keysym}'))
self.text.bind('<KeyRelease>', lambda event: print(f'Release {event.keysym}'))
```

```title="按下 Y，输出结果..."
Press ??
Release y
Press ??
Press F10
Release F10
```

WTF？？？<br>
先撇开那两个 `??` 不说，这个 `F10` 是哪来的？

## 接着

接着，我把 A~Z 试了个遍，得出结论：

它基本上是把 A~Z 往奇奇怪怪的按键映射了一次，可能是 Tkinter 对输入法发送的什么数据误读了吧...

|  Key  |  Side Effect  |
| :---: | :-----------: |
|  A~I  |      1~9      |
|   J   | asterisk (\*) |
|   K   |   plus (+)    |
|   L   |      ??       |
|   M   |   minus (-)   |
|   N   |  period (.)   |
|   O   |      无       |
|  P~Z  |    F1~F11     |

还挺有规律，这几个按键也和刚才的现象对得上。

R 是 F3，查找下一个<br>
T 是 F5，运行代码<br>
Y 是 F10，和单按 Alt 的效果一样，是工具栏<br>
P 是 F1，打开帮助

问题是找到了，可是怎么解决呢？

## 失败的第一次尝试

一开始我想直接拦截掉这些额外的 Fn 事件。

```python3 title="editor.py (其实找对地方来改也花了不少时间)"
def ignore_fn(event):
    return 'break'

self.text.bind('<Key-F5>', ignore_fn)
...
```
但是，直接拦截 Fn 事件却会导致这个字母也打不出来，而且原先的 Fn 功能也没了。<br>
况且有几个事件还捕捉不到 KeyPress，想拦截也拦截不到。

## 最终曲线救国

最终还是用了一个极度扭曲的方案：

```python3 title="editor.py -- def apply_bindings(...)"
...
if sys.platform.startswith('win'): # Fix Chinese input bug
    import time
    last_special_key_time = 0
    false_key_map = {
        # '1': 'a',
        # '2': 'b',
        # '3': 'c',
        # '4': 'd',
        # '5': 'e',
        # '6': 'f',
        # '7': 'g',
        # '8': 'h',
        # '9': 'i',
        # 'asterisk': 'j',
        # 'plus': 'k',
        # '??': 'l',  # Unknown key
        # 'minus': 'm',
        # 'period': 'n',
        # '': 'o',  # Nothing to map
        'F1': 'p',
        'F2': 'q',
        'F3': 'r',
        'F4': 's',
        'F5': 't',
        'F6': 'u',
        'F7': 'v',
        'F8': 'w',
        'F9': 'x',
        'F10': 'y',
        'F11': 'z'
    }
    def handle_special_key(event):
        # print(f'Press {event.keysym}')
        nonlocal last_special_key_time
        nonlocal f_key_events_map
        if event.keysym == '??':
            last_special_key_time = time.time()
            # print(f'Pressed ??, time: {last_special_key_time}')
        elif event.keysym in false_key_map:
            if time.time() - last_special_key_time < 0.3:
                text.event_generate(f'<KeyPress-{false_key_map[event.keysym]}>')
                return 'break'
            else:
                # print(f_key_events_map, f'Press {event.keysym}')
                if event.keysym in f_key_events_map:
                    text.event_generate(f_key_events_map[event.keysym])
    # text.bind('<KeyPress>', handle_special_key)
    # self.text.bind('<KeyPress>', lambda event: print(f'Press {event.keysym}'))
    # self.text.bind('<KeyRelease>', lambda event: print(f'Release {event.keysym}'))
    # self.text.bind('<Key>', lambda event: print(f'Key {event.keysym}'))

for event, keylist in keydefs.items():
    if keylist:
        if any(key.startswith('<Key-F') for key in keylist):
            f_key_events_map.update({key[5:-1]: event for key in keylist if key.startswith('<Key-F')})
            keylist = [key for key in keylist if not key.startswith('<Key-F')]
        if keylist:
            text.event_add(event, *keylist)
...
```

我们在所有快捷键注册的地方做个拦截，如果快捷键包含 Fn Keys，我们就把它拿走，自己手动触发。<br>
如果它没有去注册掉 Fn 快捷键去触发事件，那我们就能够捕捉到所有 Fn 的 KeyPress。

每次在中文输入法下完成一次输入，会触发一个 `??`，这时候我们记下时间。<br>
如果按下了 Fn，要是处在完成输入的 0.3s 内，我们就认定它是输入法 Bug，拦截下来，替换成点击字母。<br>
（中文字不会触发 Fn，只有中文输入法下输入英文才会触发对应的 Fn）<br>
如果检测到按下 Fn，但是不在时间内，我们认定它是正常的 Fn 按键，帮它手动触发对应的事件。

别骂了别骂了我知道这个方案超级丑，但是至少它能跑啊（x

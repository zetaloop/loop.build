---
date:
  created: 2024-11-27 19:24:31
categories:
  - 汉化
  - 开发
  - Node.js
---

# Node.js 解决 Dugite 库安装失败

解决安装 dugite 库时，出现 fetch failed 报错无法下载 git 导致安装失败。

问题起源：汉化 GitHub Desktop 时，尝试更新依赖失败。
<!-- more -->
环境：Windows 11 22635.4515；Node.js v20.17.0；全局代理（似乎未生效？）。

## 报错内容

运行 `npm install --force` 后，报错提示 Dugite 无法下载对应的 git 二进制文件。

``` plain title="报错输出" hl_lines="1 33-48"
D:\GitHub\desktop>npm install --force
npm warn using --force Recommended protections disabled.
npm warn ERESOLVE overriding peer dependency
npm warn While resolving: parallel-webpack@2.6.0
npm warn Found: webpack@5.94.0
npm warn node_modules/webpack
npm warn   webpack@"^5.94.0" from the root project
npm warn   11 more (@types/webpack, @types/webpack-bundle-analyzer, ...)
npm warn
npm warn Could not resolve dependency:
npm warn peer webpack@"^1.12.9 || ^2.2.0 || ^3.x || ^4.x" from parallel-webpack@2.6.0
npm warn node_modules/parallel-webpack
npm warn   parallel-webpack@"^2.6.0" from the root project
npm warn
npm warn Conflicting peer dependency: webpack@4.47.0
npm warn node_modules/webpack
npm warn   peer webpack@"^1.12.9 || ^2.2.0 || ^3.x || ^4.x" from parallel-webpack@2.6.0
npm warn   node_modules/parallel-webpack
npm warn     parallel-webpack@"^2.6.0" from the root project

> postinstall
> ts-node -P script/tsconfig.json script/post-install.ts

yarn install v1.21.1
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Rebuilding all packages...
[1/7] ⠠ desktop-notifications
[7/7] ⠐ windows-argv-parser
[3/7] ⠐ dugite
[6/7] ⠐ registry-js
error D:\GitHub\desktop\app\node_modules\dugite: Command failed.
Exit code: 1
Command: node ./script/download-git.js
Arguments:
Directory: D:\GitHub\desktop\app\node_modules\dugite
Output:
Unable to download archive, aborting... TypeError: fetch failed
    at node:internal/deps/undici/undici:13185:13
    at process.processTicksAndRejections (node:internal/process/task_queues:105:5)
    at async downloadAndUnpack (D:\GitHub\desktop\app\node_modules\dugite\script\download-git.js:69:15)
    at async run (D:\GitHub\desktop\app\node_modules\dugite\script\download-git.js:129:5) {
  [cause]: ConnectTimeoutError: Connect Timeout Error
      at onConnectTimeout (node:internal/deps/undici/undici:2331:28)
      at node:internal/deps/undici/undici:2283:50
      at Immediate._onImmediate (node:internal/deps/undici/undici:2313:37)
      at process.processImmediate (node:internal/timers:491:21) {




npm error code 1
npm error path D:\GitHub\desktop
npm error command failed
npm error command C:\Windows\system32\cmd.exe /d /s /c ts-node -P script/tsconfig.json script/post-install.ts
npm error A complete log of this run can be found in: C:\Users\*******\AppData\Local\npm-cache\_logs\2024-11-27T10_35_39_161Z-debug-0.log
```

## 阅读源码

根据报错，出错代码位置为 `D:\GitHub\desktop\app\node_modules\dugite\script\download-git.js` 第 69 行。
``` js title="dugite\script\download-git.js" linenums="67" hl_lines="3-7"
...
const downloadAndUnpack = async url => {
  const res = await fetch(url, {
    headers: {
      Accept: 'application/octet-stream',
      'User-Agent': 'dugite',
    },
  }).catch(e => {
    console.log('Unable to download archive, aborting...', e)
    process.exit(1)
  })
...
```
上述 URL 来自 `embedded-git.json` 文件，其定义了各平台的 git 二进制文件下载地址。
``` json title="dugite\script\embedded-git.json" hl_lines="4"
{
  "win32-x64": {
    "name": "dugite-native-v2.45.1-e87d290-windows-x64.tar.gz",
    "url": "https://github.com/desktop/dugite-native/releases/download/v2.45.1/dugite-native-v2.45.1-e87d290-windows-x64.tar.gz",
    "checksum": "6a79708447291d8b95db9f523f949389d63fca1a25b72520d1a0b9a8d7ede3e1"
  },
  "win32-ia32": {
    "name": "dugite-native-v2.45.1-e87d290-windows-x86.tar.gz",
    "url": "https://github.com/desktop/dugite-native/releases/download/v2.45.1/dugite-native-v2.45.1-e87d290-windows-x86.tar.gz",
    "checksum": "99dafc60fdeb646988c7d6f54c74a557f877b28624ed82e4201460b7d2394d49"
  },
  "darwin-x64": {
    "name": "dugite-native-v2.45.1-e87d290-macOS-x64.tar.gz",
    "url": "https://github.com/desktop/dugite-native/releases/download/v2.45.1/dugite-native-v2.45.1-e87d290-macOS-x64.tar.gz",
    "checksum": "2a3c0b52e98a8423fe54722dd4dce905fce2d1d3014452e26df01f84c5033c3f"
  },
...
```
该文件下载之后默认会被保存到临时目录，对于 Windows 就是 `%TEMP%`。
``` js title="dugite\script\config.js" linenums="44" hl_lines="11 19"
...
  if (config.source !== '') {
    // compute the filename from the download source
    const url = URL.parse(config.source)
    const pathName = url.pathname
    const index = pathName.lastIndexOf('/')
    config.fileName = pathName.substr(index + 1)

    const cacheDirEnv = process.env.DUGITE_CACHE_DIR

    const cacheDir = cacheDirEnv ? path.resolve(cacheDirEnv) : os.tmpdir()

    try {
      fs.statSync(cacheDir)
    } catch (e) {
      fs.mkdirSync(cacheDir)
    }

    config.tempFile = path.join(cacheDir, config.fileName)
  }
...
```
并且如果文件已存在，就不会重复下载。
``` js title="dugite\script\download-git.js" linenums="119" hl_lines="4-9"
...
  const tempFile = config.tempFile

  if (await pathExists(tempFile)) {
    await verifyFile(tempFile).catch(e => {
      console.log('Unable to verify cached archive, removing...', e)
      return rm(tempFile)
    })
    await unpackFile(tempFile)
  } else {
    await downloadAndUnpack(config.source)
  }
})()
```
因此只需要帮 Dugite 把文件下载好，用对应名称放到临时目录即可解决问题。

## 解决方案

1. 手动下载对应的 git 二进制文件 `dugite-native-v2.45.1-e87d290-windows-x64.tar.gz`。
2. 丢到临时目录里 `C:\Users\%username%\AppData\Local\Temp\`。
3. 再次安装。

嗯，就好了。
我还以为会有些复杂的，因为上次好像还有另外哪个库下载失败，那个是改代码加了代理功能才好（全局代理也可解）。

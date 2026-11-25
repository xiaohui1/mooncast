<p align="center">
  <img src="assets/logo.svg" width="92" height="92" alt="月映 · MoonCast" />
</p>

<h1 align="center">月映 · MoonCast</h1>

<p align="center">
  <b>私人夸克云影院 — 极速搜片验活 · 302 蓝光直连 · 双源刮削 · 文件夹级追更</b>
</p>

<p align="center">
  <a href="https://github.com/xiaohui1/mooncast/releases">📦 下载安装包</a> ·
  <a href="docs/DEPLOY.md">🚀 部署指南</a> ·
  <a href="docs/FAQ.md">❓ 常见问题</a> ·
  <a href="CHANGELOG.md">📝 更新日志</a>
</p>

> **声明**：本仓库仅用于分发编译成品（Docker 镜像、飞牛 fnOS `.fpk` 安装包、独立二进制）、部署文档与运维技能，**不包含源代码**；项目本身不内置任何影视资源，所有搜索结果均来自公开网络聚合与用户个人网盘凭证。

---

## 核心特性

* **极速搜片与并发验活**：内置聚合引擎，自动多线程并发检测夸克分享链接有效性，实时剔除失效/取消链接；支持按文件夹树形展开选集与一键复制分享链接（自动拼接提取码）。
* **4K 蓝光 302 直连 & 全功能 Web 播放器**：
  * MP4 与外部播放器（IINA / Infuse / PotPlayer）走纯 302 直连，MKV 转码流自动适配网页 HLS；
  * 内置清晰度、选集、倍速（`0.5x~3x`）、多轨字幕（云端同目录字幕 + 内嵌轨 + 本地上传）、片头片尾跳过、60fps 拖拽进度条、真·全屏与自适应移动端。
* **12h / 500GB 临时缓存池 & 断源智能换源**：
  * 临时预览关闭不卡顿、缓存期内同源秒开复用、超限异步淘汰；
  * 首页与历史记录支持无感续播，原分享失效时自动推荐已验活新源并自动对齐同集数、同秒数续播。
* **防和谐原名收藏 + 文件夹级追更**：
  * 夸克网盘内原样保留分享方的防和谐混淆目录名与原文件名，绝不改名触发风控；
  * 正式海报、剧名、简介通过本地数据库映射；追更支持锁定具体子文件夹并可视化配置每天/每周定时刷新。
* **TMDB + 豆瓣双源刮削 & 手动匹配**：国内环境直连豆瓣自动兜底，同时支持 TMDB 主源与可视化手动匹配元数据。
* **多用户隔离 & 后台一键系统更新**：支持游客防风控限流配置、管理员扫码绑定夸克 Cookie / QuarkTV 4K，以及后台多节点测速与系统更新检测。

---

## 快速部署

### 方式一：Docker 一键部署（推荐，单目录 `/data` 持久化）

```yaml
services:
  mooncast:
    image: ghcr.io/xiaohui1/mooncast:latest
    container_name: mooncast
    restart: unless-stopped
    ports:
      - "5220:5220"
    environment:
      - TZ=Asia/Shanghai
      - MOONCAST_DATA=/data
    volumes:
      - ./data:/data
```

或直接前往 [Releases](https://github.com/xiaohui1/mooncast/releases) 下载 `mooncast-vX.Y.Z-docker-kit.zip` 解压后执行：

```bash
docker compose up -d
```

### 方式二：飞牛 fnOS 原生安装包（`.fpk`）

1. 前往 [Releases](https://github.com/xiaohui1/mooncast/releases) 下载对应架构安装包：
   * x86_64 机型：`mooncast_X.Y.Z_x86.fpk`
   * ARM64 机型：`mooncast_X.Y.Z_arm.fpk`
2. 打开飞牛应用中心 → **手动安装** → 上传 `.fpk` 完成安装（默认端口 `5220`）。

---

## 首次使用说明

1. 启动后访问 `http://<你的设备IP>:5220`。
2. 首次启动会在挂载目录 `/data/init_credentials.txt` 生成初始管理员账号与随机密码（日志中也会输出）。
3. 登录后进入顶部 **「管理」** 页面：
   * 扫码登录更新 **夸克 Web Cookie** 与 **QuarkTV 4K 凭证**；
   * 其余路径、游客限流、临时缓存与刮削源均有开箱即用的默认配置，可按需微调。

---

## 文档导航

* [完整部署与升级指南（Docker / 飞牛 / 反代）](docs/DEPLOY.md)
* [常见问题与防风控说明](docs/FAQ.md)
* [版本更新日志](CHANGELOG.md)
* [AI 自动部署技能](skills/mooncast-deploy/SKILL.md)

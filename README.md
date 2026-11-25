# 月映 · MoonCast

私人夸克云影院 — PanSou 并发验活搜片 · 12h/500GB 临时缓存池 · 302 极速直连 · 豆瓣/TMDB 双源海报刮削 · 文件夹级自动追更 · 多用户隔离。

> 本仓库仅提供成品安装包（Docker 镜像 / 飞牛 fnOS `.fpk` / 独立二进制）、使用文档与部署技能；**不包含源代码**。

## 快速下载
- **GitHub Releases**：前往 [Releases 页面](https://github.com/xiaohui1/mooncast/releases) 下载对应平台成品
- **Docker 镜像**：`ghcr.io/xiaohui1/mooncast:latest`（支持 `linux/amd64`、`linux/arm64`）

## Docker 一键部署（单目录 `/data` 持久化）

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

启动后访问 `http://<你的IP>:5220`，首次启动会在 `./data/init_credentials.txt` 生成初始管理员账号密码。

## 飞牛 fnOS 安装
前往 [Releases](https://github.com/xiaohui1/mooncast/releases) 下载对应架构的 `.fpk` 安装包（x86_64 下载 `*_x86.fpk`，ARM64 下载 `*_arm.fpk`），在飞牛应用中心「手动安装」上传即可。

## 更多文档
- [部署与使用指南](./docs/DEPLOY.md)
- [更新日志](./CHANGELOG.md)
- [AI 自动部署技能](./skills/mooncast-deploy/SKILL.md)

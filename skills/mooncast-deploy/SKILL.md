---
name: mooncast-deploy
description: 部署或升级 月映 · MoonCast（Docker / 飞牛 fnOS）：拉取 ghcr.io/xiaohui1/mooncast 或下载 Releases 安装包并验证健康状态。
---

# 月映 · MoonCast 部署与升级技能

## Docker 部署与升级
1. 确保宿主机挂载单一数据卷 `-v ./data:/data`（包含 SQLite 数据库、海报缓存、PanSou 缓存与运行日志）。
2. 拉取最新镜像并重启：
   ```bash
   docker compose pull && docker compose up -d
   ```
3. 验证健康接口：`curl -fsS http://127.0.0.1:5220/api/v1/health` 返回 `"status":"ok"`。

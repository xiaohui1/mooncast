# 月映 · MoonCast 部署与使用指南

## 1. Docker 部署与升级
1. 从 [Releases](https://github.com/xiaohui1/mooncast/releases) 下载 `mooncast-vX.Y.Z-docker-kit.zip` 并解压；
2. 执行 `docker compose up -d` 启动服务；
3. 后续升级只需执行包内 `./auto-update.sh`（或 `docker compose pull && docker compose up -d`），全部数据库、海报与日志均保存在 `./data` 目录不会丢失。

## 2. 飞牛 fnOS 原生安装
1. 根据 NAS CPU 架构下载 `mooncast_X.Y.Z_x86.fpk` 或 `mooncast_X.Y.Z_arm.fpk`；
2. 打开飞牛应用中心 → 手动安装 → 上传 `.fpk`；
3. 默认端口 `5220`，支持在管理员控制中心内直接通过「系统更新」检测最新版本。

## 3. 首次使用配置
1. 使用初始管理员账号登录（查看挂载目录 `/data/init_credentials.txt`）；
2. 进入「管理 → 夸克账号与 TV 授权」扫码绑定夸克 Cookie 与 QuarkTV 4K 凭证；
3. 刮削默认支持国内豆瓣直连与 TMDB 主源自动切换，无需代理即可正常刮削海报与简介。

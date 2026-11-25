# 月映 · MoonCast 完整部署与升级指南

## 1. Docker 部署与升级

### 1.1 目录结构（单卷映射）
只需映射一个宿主机目录到容器 `/data`，以下全部持久化数据均自动保存在该目录内：
* `mooncast.db`：SQLite 数据库（用户、影库、追更、历史、设置）
* `posters/`：本地海报与封面缓存
* `search-cache/`：内置搜索索引缓存
* `logs/`：按天分类的运行与播放诊断日志
* `init_credentials.txt`：首次启动生成的初始管理员账密

### 1.2 启动命令
```bash
mkdir -p mooncast && cd mooncast
# 下载最新 docker-kit.zip 或自建 docker-compose.yml
docker compose up -d
```

### 1.3 日常升级
```bash
./auto-update.sh
# 或手动执行：
docker compose pull && docker compose up -d
```

---

## 2. 飞牛 fnOS 原生安装

1. 在 [Releases](https://github.com/xiaohui1/mooncast/releases) 下载对应架构的 `.fpk` 文件；
2. 飞牛应用中心 → 右上角/左下角「手动安装」→ 上传 `.fpk`；
3. 安装后点击桌面图标或访问 `http://<NAS_IP>:5220`；
4. 后续有新版时，可在应用内「管理 → 系统更新」查看更新日志与发布页，或上传新版 `.fpk` 覆盖升级。

---

## 3. 环境变量参考

| 变量名 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `MOONCAST_DATA` | `/data` | 持久化数据根目录 |
| `MOONCAST_LISTEN` | `:5220` | HTTP 服务监听地址与端口 |
| `TZ` | `Asia/Shanghai` | 时区设置（影响按天日志与定时追更时间） |

---

## 4. 容器内配置代理说明（直接填 `127.0.0.1` 即可）

* 官方 `docker-compose.yml` 采用标准 `bridge` 端口映射（`5220:5220`，在飞牛/群晖 Docker 面板中可直接点击端口打开页面），同时预置了 `extra_hosts: ["host.docker.internal:host-gateway"]`。
* 月映后端会自动识别容器环境：您在后台设置页直接填写宿主机本地代理（如 **`http://127.0.0.1:7890`**），程序会自动将其路由至宿主机网关端口，**无需手动改写为 `host.docker.internal`**。

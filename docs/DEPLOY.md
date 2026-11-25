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

## 4. 容器内配置代理说明（`127.0.0.1` vs 桥接模式）

* **推荐（默认 `network_mode: host`）**：
  * 官方 `docker-compose.yml` 默认使用 `network_mode: host` 共享宿主机网络，此时在后台设置页可直接填写宿主机本地代理地址，例如 **`http://127.0.0.1:7890`**。
  * 若同一台设备上还运行了其他服务占用 `5220` 端口，可在 `environment` 中修改 `MOONCAST_LISTEN=:5221` 切换端口。
* **如果改用桥接模式（`ports: "5220:5220"`）**：
  * 桥接容器内的 `127.0.0.1` 指向容器自身而非宿主机，需在 `docker-compose.yml` 添加 `extra_hosts: ["host.docker.internal:host-gateway"]`，并在后台代理填写 `http://host.docker.internal:7890` 或宿主机局域网 IP。

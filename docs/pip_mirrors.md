# Python pip 镜像源配置指南

## 已配置的镜像源
当前已配置为：**清华大学镜像源** (`https://pypi.tuna.tsinghua.edu.cn/simple/`)

## 常用国内镜像源

### 1. 清华大学镜像源（推荐）
```bash
python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. 阿里云镜像源
```bash
python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

### 3. 中国科技大学镜像源
```bash
python3 -m pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
```

### 4. 豆瓣镜像源
```bash
python3 -m pip config set global.index-url https://pypi.douban.com/simple/
```

### 5. 华为云镜像源
```bash
python3 -m pip config set global.index-url https://repo.huaweicloud.com/repository/pypi/simple/
```

## 配置文件位置
- 用户级配置：`~/.config/pip/pip.conf`
- 系统级配置：`/etc/pip.conf`

## 手动编辑配置文件
如果命令行配置不生效，可以手动编辑配置文件：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/
trusted-host = pypi.tuna.tsinghua.edu.cn

[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```

## 验证配置
```bash
python3 -m pip config list
```

## 临时使用镜像源
如果只想临时使用某个镜像源：
```bash
python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ 包名
```

## 恢复默认源
```bash
python3 -m pip config unset global.index-url
``` 
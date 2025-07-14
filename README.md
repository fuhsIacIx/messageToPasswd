# 密码生成器

一个基于Python的安全密码生成工具，支持交互式和命令行两种使用模式。

## 功能特点

- 支持中文和ASCII账户名称
- 使用密钥增强密码安全性
- 可配置密码长度和字符类型
- 提供密钥管理功能
- 支持拼音转换(中文账户名)
- 完全中文化界面

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 交互模式

```bash
python main.py
```

进入交互式菜单：
1. 生成密码
2. 退出

### 命令行模式

```bash
python main.py [选项]
```

可用选项：
- `-V, --version`       显示版本信息
- `-h, --help`          显示帮助信息
- `--ant`               生成随机密码(不加此选项则生成确定性密码)
- `-a, --account TEXT`  账户名称(支持ASCII或中文)
- `-l, --length INT`    密码长度(8-64)
- `-k, --key NAME`      指定使用的密钥
- `--new-key`           生成新密钥
- `--key-name NAME`     新密钥名称
- `--key-length INT`    新密钥长度(16-256)

## 运行示例

1. 交互式生成密码：
```bash
python main.py
```

2. 命令行生成密码：
```bash
python main.py -a 我的账户 -l 16
```

3. 生成新密钥：
```bash
python main.py --new-key --key-name mykey --key-length 64
```

## 注意事项

- 密钥文件保存在`keys/`目录下
- 建议定期更换密钥增强安全性
- 中文账户名会自动转换为拼音作为密码生成种子

# NoneBot Plugin Set Essence Msg

<p align="center">
  <a href="https://v2.nonebot.dev/">
    <img
      src="https://v2.nonebot.dev/logo.png"
      width="200"
      height="200"
      alt="nonebot"
    >
  </a>
</p>

<div align="center">

## ✨ QQ 群精华消息管理插件 ✨

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/yourname/nonebot-plugin-set-essence-msg/main/LICENSE">
    <img
      src="https://img.shields.io/github/license/yourname/nonebot-plugin-set-essence-msg"
      alt="license"
    >
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-set-essence-msg">
    <img
      src="https://img.shields.io/pypi/v/nonebot-plugin-set-essence-msg"
      alt="pypi"
    >
  </a>
  <a href="https://www.python.org/downloads/">
    <img
      src="https://img.shields.io/badge/python-3.9+-blue"
      alt="python"
    >
  </a>
  <a href="https://v2.nonebot.dev/">
    <img
      src="https://img.shields.io/badge/nonebot-2.0+-red"
      alt="nonebot"
    >
  </a>
</p>

______________________________________________________________________

## 📖 介绍

本插件为 NoneBot2 提供 QQ 群精华消息管理功能，支持：

- ✅ 设置精华消息
- ✅ 移除精华消息

基于 OneBot V11 协议实现， 支持 NapCat。

由AI驱动

______________________________________________________________________

## 📦 安装

### 使用 nb-cli（推荐）

```bash
nb plugin install nonebot-plugin-set-essence-msg
```

### 使用 pip

```bash
pip install nonebot-plugin-set-essence-msg
```

______________________________________________________________________

## 🚀 使用说明

### 前置要求

- 机器人账号必须是群管理员或群主
- OneBot 协议端需支持精华消息相关 API
- NapCat 已支持

______________________________________________________________________

## 📚 命令列表

### 设置精华

- 命令：`设精`
- 别名：`加精`、`设为精华`
- 权限：群管理员
- 说明：引用要设置的消息后发送命令

### 移除精华

- 命令：`移精`
- 别名：`删精`、`取消精华`、`移除精华`
- 权限：群管理员
- 说明：引用已设置为精华的消息后发送命令

______________________________________________________________________

## 🧪 使用示例

### 设置精华消息

1. 在群聊中找到要设为精华的消息
1. 引用（回复）该消息
1. 发送：

```text
设精
```

或：

```text
加精
```

机器人回复：

```text
✅ 已设为精华消息
消息ID: 1684290360
```

______________________________________________________________________

### 移除精华消息

1. 引用已被设为精华的消息
1. 发送：

```text
删精
```

或：

```text
取消精华
```

机器人回复：

```text
✅ 已移除精华消息
消息ID: 1684290360
```

______________________________________________________________________

## ⚙️ 配置

ESSENCE_COOLDOWN=60 # 冷却时间，单位秒，默认为60，设为0关闭冷却，对超级用户、群主、管理员不生效
ESSENCE_ENABLED_GROUPS=\[123456, 789012\] # 启用插件的群号列表，包含0表示所有群都启用

______________________________________________________________________

## 📄 许可证

本项目采用 MIT 许可证。

______________________________________________________________________

## 🙏 致谢

- NoneBot2 - 强大的机器人框架
- OneBot - 聊天机器人应用接口标准

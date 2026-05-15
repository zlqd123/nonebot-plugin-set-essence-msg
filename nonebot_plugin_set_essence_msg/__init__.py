import asyncio
from collections import defaultdict

from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.exception import FinishedException
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from .config import Config

# 插件元数据
__plugin_meta__ = PluginMetadata(
    name="精华消息管理",
    description="设置和移除群聊精华消息",
    usage="引用消息后回复：设精/加精 或 移精/删精/取消精华",
    type="application",
    homepage="https://github.com/zlqd123/nonebot-plugin-set-essence-msg",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

# 全局冷却存储
_cooldown_store: dict[str, dict[str, float]] = defaultdict(dict)

# 获取配置
driver = get_driver()
plugin_config = Config(**driver.config.dict())


def is_group_enabled(group_id: int) -> bool:
    """检查群聊是否启用插件"""
    enabled_groups = plugin_config.essence_enabled_groups
    if 0 in enabled_groups:
        return True
    return group_id in enabled_groups


def is_privileged_user(event: GroupMessageEvent) -> bool:
    """检查是否为特权用户（无冷却限制）"""
    # 检查是否为群管理员或群主
    if event.sender.role in ["admin", "owner"]:
        return True

    # 检查是否为机器人超级用户
    try:
        superusers: set[str] = getattr(driver.config, "superusers", set())
        if str(event.user_id) in superusers:
            return True
    except Exception:
        pass

    return False


def is_on_cooldown(key: str, cooldown_seconds: int) -> tuple[bool, float]:
    """检查是否在冷却中"""
    store = _cooldown_store.get(key, {})
    if not store:
        return False, 0

    current_time = asyncio.get_event_loop().time()
    expire_time = store.get(key, 0)

    if current_time < expire_time:
        return True, expire_time - current_time
    return False, 0


def set_cooldown(key: str, cooldown_seconds: int) -> None:
    """设置冷却时间"""
    current_time = asyncio.get_event_loop().time()
    _cooldown_store[key][key] = current_time + cooldown_seconds


def clean_expired_cooldown() -> None:
    """清理过期冷却记录"""
    current_time = asyncio.get_event_loop().time()
    for cmd_key in list(_cooldown_store.keys()):
        store = _cooldown_store[cmd_key]
        for user_key in list(store.keys()):
            if store[user_key] <= current_time:
                del store[user_key]
        if not store:
            del _cooldown_store[cmd_key]


def get_reply_msg_id(event: GroupMessageEvent) -> int | None:
    """获取被回复的消息ID"""
    if event.reply:
        try:
            return int(event.reply.message_id)
        except (ValueError, TypeError):
            pass

    for seg in event.message:
        if seg.type == "reply":
            try:
                return int(seg.data.get("id", 0))
            except (ValueError, TypeError):
                pass
    return None


# 创建命令响应器
set_cmd = on_command("设精", aliases={"加精", "设为精华"}, priority=10, block=True)

remove_cmd = on_command(
    "移精", aliases={"删精", "取消精华", "移除精华"}, priority=10, block=True
)


@set_cmd.handle()
async def handle_set(bot: Bot, event: GroupMessageEvent):
    # 检查群聊是否启用
    if not is_group_enabled(event.group_id):
        await set_cmd.finish("❌ 本群未启用精华管理功能")
        return

    is_privileged = is_privileged_user(event)
    cooldown = plugin_config.essence_cooldown

    # 非特权用户需要检查冷却
    if not is_privileged and cooldown > 0:
        user_key = f"set_essence:{event.group_id}:{event.user_id}"

        on_cooldown, remaining = is_on_cooldown(user_key, cooldown)
        if on_cooldown:
            await set_cmd.finish(f"⏰ 操作冷却中，请 {remaining:.0f} 秒后再试")
            return

    msg_id = get_reply_msg_id(event)
    if not msg_id:
        await set_cmd.finish("❌ 请引用一条消息")

    try:
        await bot.call_api("set_essence_msg", message_id=msg_id)

        # 记录日志
        if event.sender.role in ["admin", "owner"]:
            user_type = "管理员"
        elif is_privileged:
            user_type = "超级用户"
        else:
            user_type = "成员"

        logger.info(
            f"设精成功: group={event.group_id}, msg={msg_id}, "
            f"op={event.user_id}({user_type})"
        )

        # 非特权用户设置冷却
        if not is_privileged and cooldown > 0:
            set_cooldown(user_key, cooldown)
            clean_expired_cooldown()
            await set_cmd.finish(f"✅ 已设为精华\nID: {msg_id}")
        else:
            await set_cmd.finish(f"✅ 已设为精华\nID: {msg_id}")

    except FinishedException:
        raise
    except Exception as e:
        error_msg = str(e)
        if "权限不足" in error_msg or "10005" in error_msg:
            await set_cmd.finish("❌ 权限不足，请确认机器人有管理员权限")
        else:
            await set_cmd.finish(f"❌ 设置失败: {error_msg}")


@remove_cmd.handle()
async def handle_remove(bot: Bot, event: GroupMessageEvent):
    # 检查群聊是否启用
    if not is_group_enabled(event.group_id):
        await remove_cmd.finish("❌ 本群未启用精华管理功能")
        return

    is_privileged = is_privileged_user(event)
    cooldown = plugin_config.essence_cooldown

    # 非特权用户需要检查冷却
    if not is_privileged and cooldown > 0:
        user_key = f"remove_essence:{event.group_id}:{event.user_id}"

        on_cooldown, remaining = is_on_cooldown(user_key, cooldown)
        if on_cooldown:
            await remove_cmd.finish(f"⏰ 操作冷却中，请 {remaining:.0f} 秒后再试")
            return

    msg_id = get_reply_msg_id(event)
    if not msg_id:
        await remove_cmd.finish("❌ 请引用一条精华消息")

    try:
        await bot.call_api("delete_essence_msg", message_id=msg_id)

        # 记录日志
        if event.sender.role in ["admin", "owner"]:
            user_type = "管理员"
        elif is_privileged:
            user_type = "超级用户"
        else:
            user_type = "成员"

        logger.info(
            f"移精成功: group={event.group_id}, msg={msg_id}, "
            f"op={event.user_id}({user_type})"
        )

        # 非特权用户设置冷却
        if not is_privileged and cooldown > 0:
            set_cooldown(user_key, cooldown)
            clean_expired_cooldown()
            await remove_cmd.finish(f"✅ 已移除精华\nID: {msg_id}")
        else:
            await remove_cmd.finish(f"✅ 已移除精华\nID: {msg_id}")

    except FinishedException:
        raise
    except Exception as e:
        error_msg = str(e)
        if "权限不足" in error_msg:
            await remove_cmd.finish("❌ 权限不足，请确认机器人有管理员权限")
        else:
            await remove_cmd.finish(f"❌ 移除失败: {error_msg}")


logger.info(
    f"精华消息插件已加载\n"
    f"配置: 冷却时间={plugin_config.essence_cooldown}秒, "
    f"启用群组={plugin_config.essence_enabled_groups}"
)

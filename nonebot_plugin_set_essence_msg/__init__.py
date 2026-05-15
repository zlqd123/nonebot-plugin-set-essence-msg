from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
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
    homepage="https://github.com/zlqd123/nonebot-plugin-essence-message",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

# 获取被回复消息ID的辅助函数（简化版）
def _get_reply_msg_id(event: MessageEvent) -> int | None:
    if event.reply:
        return int(event.reply.message_id)
    for seg in event.message:
        if seg.type == "reply":
            return int(seg.data.get("id"))
    return None

# 命令响应器（使用规范命名，添加必要别名）
set_cmd = on_command("设精", aliases={"加精", "设为精华"}, permission=GROUP_ADMIN | GROUP_OWNER, priority=10, block=True)
remove_cmd = on_command("移精", aliases={"删精", "取消精华", "移除精华"}, permission=GROUP_ADMIN | GROUP_OWNER, priority=10, block=True)

logger.info("精华消息插件已加载")

@set_cmd.handle()
async def _handle_set(bot: Bot, event: MessageEvent):
    msg_id = _get_reply_msg_id(event)
    if not msg_id:
        await set_cmd.finish("❌ 请引用一条消息")
    try:
        await bot.call_api("set_essence_msg", message_id=msg_id)
        logger.info(f"设精成功: group={event.group_id}, msg={msg_id}, op={event.user_id}")
        await set_cmd.finish(f"✅ 已设为精华\nID: {msg_id}")
    except FinishedException:
        raise
    except Exception as e:
        await set_cmd.finish(f"❌ 失败: {e}")

@remove_cmd.handle()
async def _handle_remove(bot: Bot, event: MessageEvent):
    msg_id = _get_reply_msg_id(event)
    if not msg_id:
        await remove_cmd.finish("❌ 请引用一条精华消息")
    try:
        await bot.call_api("delete_essence_msg", message_id=msg_id)
        logger.info(f"移精成功: group={event.group_id}, msg={msg_id}, op={event.user_id}")
        await remove_cmd.finish(f"✅ 已移除精华\nID: {msg_id}")
    except FinishedException:
        raise
    except Exception as e:
        await remove_cmd.finish(f"❌ 失败: {e}")
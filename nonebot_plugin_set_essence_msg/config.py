from nonebot import get_driver
from pydantic import BaseModel, Field


class Config(BaseModel):
    """插件配置类"""

    essence_cooldown: int = Field(
        default=60, description="冷却时间(秒),0 表示关闭冷却", ge=0
    )

    essence_enabled_groups: set[int] = Field(
        default_factory=set, description="启用插件的群号列表，包含 0 表示所有群都启用"
    )


# 获取配置
driver = get_driver()
plugin_config = Config(**driver.config.dict())

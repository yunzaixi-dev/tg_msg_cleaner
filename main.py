import os
import asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import User

async def main():
    """主函数，用于连接 Telegram 并列出所有群聊。"""
    load_dotenv()

    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    session_name = os.getenv('SESSION_NAME', 'my_session')

    if not all([api_id, api_hash]):
        print("错误：请确保 .env 文件中已设置 API_ID 和 API_HASH。")
        return

    try:
        api_id = int(api_id)
    except ValueError:
        print("错误：API_ID 格式不正确，应为纯数字。")
        return

    async with TelegramClient(session_name, api_id, api_hash) as client:
        print("成功连接到 Telegram。正在获取群聊列表...")

        print("\n--- 您的群聊列表 ---")
        count = 0
        try:
            async for dialog in client.iter_dialogs():
                # 筛选出普通群组和超级群组 (megagroup)
                if dialog.is_group or (dialog.is_channel and dialog.entity.megagroup):
                    print(f"- {dialog.name}")
                    count += 1
        except Exception as e:
            print(f"获取群聊时出错: {e}")

        print(f"\n--- 共找到 {count} 个群聊 ---")


if __name__ == "__main__":
    asyncio.run(main())


import os
import asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import User

async def main():
    """主函数，用于连接 Telegram 并列出指定群组中我的所有发言。"""
    load_dotenv()

    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    session_name = os.getenv('SESSION_NAME', 'my_session')
    group_name = os.getenv('GROUP_NAME')

    if not all([api_id, api_hash, group_name]):
        print("错误：请确保 .env 文件中已设置 API_ID, API_HASH, 和 GROUP_NAME。")
        return

    try:
        api_id = int(api_id)
    except ValueError:
        print("错误：API_ID 格式不正确，应为纯数字。")
        return

    async with TelegramClient(session_name, api_id, api_hash) as client:
        print("成功连接到 Telegram。")

        target_group = None
        try:
            async for dialog in client.iter_dialogs():
                if dialog.name == group_name:
                    target_group = dialog.entity
                    break
        except Exception as e:
            print(f"查找群组时出错: {e}")
            return

        if not target_group:
            print(f"错误：找不到名为 '{group_name}' 的群组。请检查名称是否正确。")
            return

        print(f"成功找到群组: '{group_name}'。开始查找您的发言...")

        message_count = 0
        print(f"\n--- 您在 '{group_name}' 的发言 ---")
        try:
            async for message in client.iter_messages(target_group, from_user='me'):
                timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}] {message.text}")
                message_count += 1
        except Exception as e:
            print(f"查找消息时发生错误: {e}")

        print(f"\n--- 共找到 {message_count} 条您发送的消息 ---")


if __name__ == "__main__":
    asyncio.run(main())


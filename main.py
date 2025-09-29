import os
import asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import User

async def main():
    """主函数，用于连接 Telegram 并删除指定群组中的消息。"""
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

        me = await client.get_me()
        print(f"当前用户: {me.username}")

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

        print(f"成功找到群组: '{group_name}'。开始查找并删除您的消息...")

        deleted_count = 0
        try:
            async for message in client.iter_messages(target_group, from_user='me'):
                print(f"正在删除消息 ID: {message.id} - 内容: '{message.text[:30]}...' ")
                await message.delete()
                deleted_count += 1
                await asyncio.sleep(1)  # 避免 API 请求过于频繁

            print(f"\n操作完成！共删除了 {deleted_count} 条您发送的消息。")

        except Exception as e:
            print(f"删除消息时发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())


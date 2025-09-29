import os
import asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import User

import csv

async def main():
    """主函数，用于连接 Telegram，将指定群组中我的所有发言保存到 CSV 文件。"""
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

        print(f"成功找到群组: '{group_name}'。开始查找您的发言并保存到 CSV 文件...")

        csv_filename = f"{group_name.replace('/', '_')}_messages.csv"
        message_count = 0

        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['timestamp', 'message_id', 'content'])

                async for message in client.iter_messages(target_group, from_user='me'):
                    timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')
                    # 仅处理文本消息，您可以根据需要扩展
                    content = message.text if message.text else "(非文本消息)"
                    print(f"正在存档消息 ID: {message.id}")
                    csv_writer.writerow([timestamp, message.id, content])
                    message_count += 1
            
            print(f"\n存档完成！共保存 {message_count} 条消息到文件 '{csv_filename}'。")

        except Exception as e:
            print(f"处理消息时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())


import sys
from pyrogram.types import Message
from pyrogram import enums
from time import time
from os import system, name as os_name
from typing import Tuple, Optional


def wait_for_exit():
    """Wait for user input before exiting."""
    try:
        input("Press enter to exit...")
    except KeyboardInterrupt:
        pass
    finally:
        sys.exit(0)


_speed_data = {}


def display_progress(current: int, total: int, uid: str):
    """Display download progress with speed."""
    now = time()
    
    if uid in _speed_data:
        elapsed = now - _speed_data[uid]["time"]
        speed = (current - _speed_data[uid]["bytes"]) / elapsed if elapsed > 0 else 0
    else:
        speed = 0
    
    _speed_data[uid] = {"time": now, "bytes": current}
    
    percent = (current * 100) / total if total > 0 else 0
    filled = int(50 * current / total) if total > 0 else 0
    bar = f"[{'#' * filled}{' ' * (50 - filled)}]"
    
    sys.stdout.write(f"\r{bar} {percent:.1f}% - {format_file_size(speed)}/s - {format_file_size(current)}")
    sys.stdout.flush()


def get_media_from_message(message: Message) -> Optional[enums.MessageMediaType]:
    """Extract media from message."""
    if not isinstance(message, Message):
        return None
        
    media_attrs = ("audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note")
    for attr in media_attrs:
        media = getattr(message, attr, None)
        if media:
            return media
    return None


def format_file_size(bytes_size: int, precision: int = 2) -> str:
    """Convert bytes to human readable format."""
    if bytes_size == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.{precision}f} {units[unit_index]}"


def parse_link(link: str) -> Tuple[str, int, int]:
    """Parse Telegram link to extract chat ID and message range."""
    if not link.startswith("https://t.me/"):
        raise ValueError("Invalid Telegram link")
    
    parts = link.split("/")
    msg_part = parts[-1].replace("?single", "").split("-")
    start_id = int(msg_part[0])
    end_id = int(msg_part[1]) if len(msg_part) > 1 else start_id
    
    chat_id = int("-100" + parts[4]) if "/c/" in link else parts[3]
    return chat_id, start_id, end_id


def get_filename(media, message: Message) -> str:
    """Get default filename for media."""
    if media and hasattr(media, 'file_name') and media.file_name:
        return media.file_name
    return f"{str(message.chat.id)[-10:]}-{message.id}" + (f"-{media.file_unique_id}" if media else ".txt")


def print_banner():

    system("cls" if os_name == "nt" else "clear")
    print("""
    8888888b.   .d8888b.  8888888b.  
    888   Y88b d88P  Y88b 888  "Y88b 
    888    888 888    888 888    888 
    888   d88P 888        888    888 
    8888888P"  888        888    888 
    888 T88b   888    888 888    888 
    888  T88b  Y88b  d88P 888  .d88P 
    888   T88b  "Y8888P"  8888888P"  

	Restricted Content Downloader v1.0
""")
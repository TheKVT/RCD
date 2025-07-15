from pyrogram import Client
from pyrogram.types import User, Message
from typing import  Optional
from utils import *
from uuid import uuid4
import argparse
import configparser
import sys


def parse_command_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Restricted Content Downloader')
    parser.add_argument('-F', '--filename', help='Custom filename for downloaded files')
    parser.add_argument('-D', '--dry-run', action='store_true', help='Show what would be downloaded')
    parser.add_argument('-I', '--index', action='store_true', help='Add message ID as index to filename')
    parser.add_argument('link', nargs='?', help='Telegram message/post link')
    return parser.parse_args()

def get_credentials() -> Tuple[str, str, str]:
    """Get API credentials and session string from config.ini."""
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        
        if 'Credentials' in config:
            api_id = config['Credentials'].get('api_id')
            api_hash = config['Credentials'].get('api_hash')
            session_string = config['Credentials'].get('session_string')
            
            if all([api_id, api_hash, session_string]):
                return api_id, api_hash, session_string
            else:
                print(f"Missing required credentials in {CONFIG_FILE}")
                wait_for_exit()
                
    except Exception as e:
        print(f"Error reading config: {e}")
        wait_for_exit()

    # Login process
    print(f"{CONFIG_FILE} not found or invalid. Starting login...")
    if input("Login? (y/n): ").lower() != "y":
        wait_for_exit()

    api_id = input("API ID: ").strip()
    api_hash = input("API HASH: ").strip()

    if input("Have session string? (y/n): ").lower() == "y":
        session_string = input("SESSION STRING: ").strip()
    else:
        print("Creating session...")
        with Client("temp", api_id=api_id, api_hash=api_hash, in_memory=True) as temp:
            session_string = temp.export_session_string()
        print("Session created!")

    with open(CONFIG_FILE, "w") as f:
        f.write(f"{api_id}\n{api_hash}\n{session_string}")
    
    return api_id, api_hash, session_string

def add_index_to_filename(filename: str, msg_id: int) -> str:
    """Add message ID as index to filename."""
    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
        return f"{name}.{msg_id}.{ext}"
    else:
        return f"{filename}.{msg_id}"

def download_message(client: Client, chat_id: str, msg_id: int, custom_filename: Optional[str], dry_run: bool, add_index: bool) -> bool:
    """Download content from a single message."""
    try:
        msg: Message = client.get_messages(chat_id, msg_id)
        if msg.empty:
            print(f"Message {chat_id}/{msg_id} not found - skipping")
            return False

        media = get_media_from_message(msg)
        filename = get_filename(media, msg)
        
        # Add index to filename if requested
        if add_index:
            filename = add_index_to_filename(filename, msg_id)
        
        if dry_run:
            size = format_file_size(media.file_size) if media else "00.00"
            print(f"Would save: {filename} ({size})")
            return True
        
        if media:
            print("Downloading media...")
            final_filename = custom_filename
            if custom_filename and media.file_name:
                ext = media.file_name.split('.')[-1]
                if '.' not in custom_filename:
                    final_filename = f"{custom_filename}.{ext}"
                
                # Add index to custom filename if requested
                if add_index:
                    final_filename = add_index_to_filename(final_filename, msg_id)
            elif add_index and not custom_filename:
                final_filename = filename
            
            file_path = client.download_media(
                msg, 
                progress=display_progress, 
                progress_args=(uuid4(),), 
                file_name=final_filename if custom_filename or add_index else filename
            )
            print(f"\nSaved: {file_path}")
        else:
            # Text message
            with open(f"downloads/{filename}", "w", encoding="utf-8") as f:
                f.write(msg.text or "")
            print(f"Saved text: downloads/{filename}")
        
        return True
        
    except Exception as e:
        print(f"Error downloading {msg_id}: {e}")
        return False


def process_link(client: Client, link: str, custom_filename: Optional[str], dry_run: bool, add_index: bool):
    """Process Telegram link and download messages."""
    try:
        chat_id, start_id, end_id = parse_link(link)
    except Exception as e:
        print(f"Link parsing error: {e}")
        return

    total = end_id - start_id + 1
    success_count = 0
    
    for msg_id in range(start_id, end_id + 1):
        # Get message info for display
        try:
            msg: Message = client.get_messages(chat_id, msg_id)
            if not msg.empty:
                media = get_media_from_message(msg)
                if media:
                    display_filename = get_filename(media, msg)
                    if add_index:
                        display_filename = add_index_to_filename(display_filename, msg_id)
                    print(f"{display_filename} - {media.__class__.__name__} - {format_file_size(media.file_size)} ({msg_id - start_id + 1}/{total})")
                else:
                    print(f"Text message ({msg_id - start_id + 1}/{total})")
        except:
            pass
        
        if download_message(client, chat_id, msg_id, custom_filename, dry_run, add_index):
            success_count += 1
        print()
    
    print(f"Completed: {success_count}/{total} messages")



def main():
    """Main function."""
    args = parse_command_arguments()
    
    try:
        api_id, api_hash, session_string = get_credentials()
        client = Client("RCD", api_id=api_id, api_hash=api_hash, session_string=session_string, in_memory=True)
        
        print("Logging in...")
        if not client:
            print(f"Try deleting {CONFIG_FILE}")
            return

        with client:
            user = client.get_me()
            name = user.first_name + (f" {user.last_name}" if user.last_name else "")
            username = f" - @{user.username}" if user.username else ""
            print(f"Logged in as: {name}{username} ({user.id})")
            if not args.link:
                print("No link provided. Use -h for help.")
                sys.exit(1)
            process_link(client, args.link, args.filename, args.dry_run, args.index)
    finally:
        wait_for_exit()


if __name__ == "__main__":
    main()
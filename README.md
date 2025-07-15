# RCD - Restricted Content Downloader

A powerful Python tool for downloading media and content from Telegram channels, groups, and private messages - even when content is restricted.

## ✨ Features

- **Download All Media Types**: Photos, videos, audio, documents, stickers, animations, voice notes, and video notes
- **Batch Downloads**: Download multiple messages at once using message ranges
- **Restricted Content**: Bypass download restrictions on protected content
- **Flexible Naming**: Custom filenames with optional message ID indexing
- **Progress Tracking**: Real-time download progress with speed indicators
- **Dry Run Mode**: Preview what would be downloaded without actually downloading
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Session Management**: Secure session handling with automatic login

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/rcd.git
cd rcd

# Install dependencies
python -m pip install -r requirements.txt

# Run directly
python rcd.py [options] <telegram_link>


## 📋 Requirements

- Python 3.12+
- Telegram API credentials (API ID and API Hash from [my.telegram.org](https://my.telegram.org))
- Active Telegram account

## 🔧 Configuration

### First Time Setup

1. **Get API Credentials**:
   - Go to [my.telegram.org](https://my.telegram.org)
   - Log in with your phone number
   - Go to "API Development Tools"
   - Create a new application
   - Note your `API ID` and `API Hash`

2. **Run the Tool**:
   ```bash
   python rcd.py https://t.me/channel/123
   ```

3. **Enter Credentials**:
   - API ID: `12345678`
   - API Hash: `abcdef1234567890abcdef1234567890`
   - Phone number: `+1234567890` (with country code)

4. **Configuration File**:
   - Credentials are saved in `config.ini`
   - Delete this file to re-login with different credentials

### Manual Configuration

Create a `config.ini` file:
```ini
[Credentials]
api_id = 12345678
api_hash = abcdef1234567890abcdef1234567890
session_string = your_session_string_here
```

## 📖 Usage

### Basic Usage

```bash
# Download a single message
python rcd.py https://t.me/channel/123

# Download a range of messages
python rcd.py https://t.me/channel/123-125

# Download from private channel
python rcd.py https://t.me/c/1234567890/100
```

### Advanced Options

```bash
# Help message
python rcd.py -h

# Custom filename
python rcd.py https://t.me/channel/123 -F "my_video"

# Add message ID prefix to filename
python rcd.py https://t.me/channel/123 --index

# Dry run (preview only)
python rcd.py https://t.me/channel/123 --dry-run

# Custom config file
python rcd.py https://t.me/channel/123 -C /path/to/config.ini

# Combine options
python rcd.py https://t.me/channel/123-125 -F "batch_download" --index --dry-run
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `link` | Telegram message/post link (required) |
| `-F, --filename` | Custom filename for downloaded files |
| `-D, --dry-run` | Show what would be downloaded without downloading |
| `-I, --index` | Add message ID as prefix to filename |
| `-C, --config` | Path to config file (default: config.ini) |
| `-h, --help` | Show help message |

## 🔗 Supported Link Formats

- **Public Channels**: `https://t.me/channel_name/123`
- **Private Channels**: `https://t.me/c/1234567890/123`
- **Message Ranges**: `https://t.me/channel_name/123-125`
- **Single Messages**: `https://t.me/channel_name/123`


## 🔒 Security & Privacy

- **Local Storage**: All credentials are stored locally in `config.ini`
- **Session Management**: Uses secure session strings instead of storing passwords
- **No Data Collection**: No user data is sent to external servers
- **Open Source**: Full source code available for inspection


### Legal Considerations
- Only download content you have permission to access
- Respect copyright and intellectual property rights
- Follow Telegram's Terms of Service
- Be aware of local laws regarding content downloading

### Troubleshooting

#### Login Issues
```bash
# Delete config and try again
rm config.ini
python rcd.py https://t.me/channel/123
```

#### Session Expired
```bash
# Remove session and re-login
rm config.ini
python rcd.py https://t.me/channel/123
```

#### Permission Denied
```bash
# Make sure you have access to the channel/group
# Check if the link is correct
# Verify you're logged in with the right account
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## 🔄 Changelog

### v1.0.0
- Initial release
- Basic download functionality
- Session management
- Progress tracking
- Dry run mode
- Custom filename support
- Message ID indexing

**⭐ Star this repository if you find it useful!**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
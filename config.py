# Configuration Settings for TikTok Account Manager

# Chrome options
CHROME_OPTIONS = {
    'headless': True,
    'disable_gpu': True,
    'no_sandbox': True
}

# TikTok settings
TIKTOK_URLS = [
    'https://www.tiktok.com/@username1',
    'https://www.tiktok.com/@username2',
]

# Delays (in seconds)
DELAY_SETTINGS = {
    'short_delay': 2,
    'medium_delay': 5,
    'long_delay': 10,
}

# Video settings
VIDEO_SETTINGS = {
    'resolution': '1080p',
    'fps': 30,
    'codec': 'h264'
}

# Folder paths
FOLDER_PATHS = {
    'download': './downloads/',
    'output': './output/video/',
    'logs': './logs/'
}
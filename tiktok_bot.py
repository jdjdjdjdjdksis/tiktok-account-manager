import time
import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
from config import *

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/tiktok_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TikTokBot:
    def __init__(self, account_email, account_password, user_data_dir=None):
        """Khởi tạo TikTok Bot với một tài khoản"""
        self.account_email = account_email
        self.account_password = account_password
        self.user_data_dir = user_data_dir or f"./chrome_profiles/{{account_email.split('@')[0]}}"
        self.driver = None
        self.logger = logger
        
    def initialize_driver(self):
        """Tạo Chrome webdriver với profile riêng"""
        try:
            options = webdriver.ChromeOptions()
            
            # User data directory để lưu cookies và session
            options.add_argument(f'--user-data-dir={{self.user_data_dir}}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Headless mode (tùy chọn)
            # options.add_argument('--headless')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_window_size(1920, 1080)
            
            self.logger.info(f"✓ Chrome driver initialized for {{self.account_email}}")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Failed to initialize driver: {{str(e)}}")
            return False
    
    def login(self):
        """Đăng nhập vào TikTok"""
        try:
            self.logger.info(f"🔑 Logging in: {{self.account_email}}")
            self.driver.get(TIKTOK_LOGIN_URL)
            time.sleep(DELAY_LONG)
            
            # Chờ nút login xuất hiện
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Log in')]"))
            )
            login_button[0].click()
            time.sleep(DELAY_MEDIUM)
            
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(self.account_email)
            time.sleep(DELAY_SHORT)
            
            # Nhập password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.account_password)
            time.sleep(DELAY_SHORT)
            
            # Click login
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            time.sleep(DELAY_LONG)
            
            # Chờ trang home load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/']"))
            )
            
            self.logger.info(f"✓ Successfully logged in: {{self.account_email}}")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Login failed: {{str(e)}}")
            return False
    
    def logout(self):
        """Đăng xuất khỏi TikTok"""
        try:
            self.logger.info(f"🚪 Logging out: {{self.account_email}}")
            
            # Click vào profile icon
            profile_icon = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href*='/user/']"))
            )
            profile_icon.click()
            time.sleep(DELAY_MEDIUM)
            
            # Click logout
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Log out')]"))
            )
            logout_button.click()
            time.sleep(DELAY_MEDIUM)
            
            self.logger.info(f"✓ Successfully logged out: {{self.account_email}}")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Logout failed: {{str(e)}}")
            return False
    
    def scroll_feed(self, scroll_count=SCROLL_COUNT):
        """Lướt video tự động"""
        try:
            self.logger.info(f"📱 Scrolling feed ({{scroll_count}} videos)")
            self.driver.get(TIKTOK_HOME_URL)
            time.sleep(DELAY_LONG)
            
            for i in range(scroll_count):
                # Scroll down
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                
                self.logger.info(f"   Scrolled {{i+1}}/{{scroll_count}} videos")
            
            self.logger.info(f"✓ Feed scrolling completed")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Feed scrolling failed: {{str(e)}}")
            return False
    
    def upload_video(self, video_path, caption="", hashtags=""):
        """Đăng video lên TikTok"""
        try:
            if not os.path.exists(video_path):
                self.logger.error(f"✗ Video file not found: {{video_path}}")
                return False
            
            self.logger.info(f"📹 Uploading video: {{video_path}}")
            self.driver.get(TIKTOK_UPLOAD_URL)
            time.sleep(DELAY_LONG)
            
            # Click upload area
            upload_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            
            # Send video file
            upload_area.send_keys(os.path.abspath(video_path))
            time.sleep(DELAY_LONG)
            
            # Nhập caption
            if caption:
                caption_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder*='caption']"))
                )
                caption_input.send_keys(caption)
                time.sleep(DELAY_SHORT)
            
            # Nhập hashtags
            if hashtags:
                hashtag_input = self.driver.find_element(By.XPATH, "//input[@placeholder*='hashtag']")
                hashtag_input.send_keys(hashtags)
                time.sleep(DELAY_SHORT)
            
            # Click post button
            post_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Post')]"))
            )
            post_button.click()
            time.sleep(DELAY_LONG)
            
            self.logger.info(f"✓ Video uploaded successfully: {{video_path}}")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Video upload failed: {{str(e)}}")
            return False
    
    def close(self):
        """Đóng browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info(f"✓ Browser closed for {{self.account_email}}")

class AccountManager:
    def __init__(self, accounts_file=ACCOUNTS_FILE):
        """Quản lý nhiều tài khoản"""
        self.accounts_file = accounts_file
        self.accounts = self.load_accounts()
        self.bots = {}
        
    def load_accounts(self):
        """Load danh sách tài khoản từ file JSON"""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"✗ Failed to load accounts: {{str(e)}}")
            return {}
    
    def save_accounts(self):
        """Lưu danh sách tài khoản"""
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(self.accounts, f, indent=2, ensure_ascii=False)
            logger.info(f"✓ Accounts saved")
        except Exception as e:
            logger.error(f"✗ Failed to save accounts: {{str(e)}}")
    
    def add_account(self, email, password):
        """Thêm tài khoản mới"""
        self.accounts[email] = {'password': password}
        self.save_accounts()
        logger.info(f"✓ Account added: {{email}}")
    
    def remove_account(self, email):
        """Xóa tài khoản"""
        if email in self.accounts:
            del self.accounts[email]
            self.save_accounts()
            logger.info(f"✓ Account removed: {{email}}")
    
    def initialize_all_bots(self):
        """Khởi tạo tất cả bots"""
        for email, data in self.accounts.items():
            bot = TikTokBot(email, data['password'])
            if bot.initialize_driver():
                self.bots[email] = bot
    
    def login_all(self):
        """Đăng nhập tất cả tài khoản"""
        for email, bot in self.bots.items():
            bot.login()
            time.sleep(DELAY_LONG)
    
    def logout_all(self):
        """Đăng xuất tất cả tài khoản"""
        for email, bot in self.bots.items():
            bot.logout()
            time.sleep(DELAY_LONG)
    
    def scroll_all(self, count=SCROLL_COUNT):
        """Lướt video cho tất cả tài khoản"""
        for email, bot in self.bots.items():
            logger.info(f"🔄 Processing account: {{email}}")
            bot.scroll_feed(count)
            time.sleep(DELAY_LONG)
    
    def upload_to_all(self, video_path, caption="", hashtags=""):
        """Đăng video lên tất cả tài khoản"""
        for email, bot in self.bots.items():
            logger.info(f"🔄 Processing account: {{email}}")
            bot.upload_video(video_path, caption, hashtags)
            time.sleep(DELAY_LONG)
    
    def close_all(self):
        """Đóng tất cả browsers"""
        for email, bot in self.bots.items():
            bot.close()

if __name__ == "__main__":
    # Ví dụ sử dụng
    manager = AccountManager()
    manager.add_account("account1@email.com", "password123")
    manager.add_account("account2@email.com", "password456")
    
    manager.initialize_all_bots()
    manager.login_all()
    
    # Lướt video
    manager.scroll_all(5)
    
    # Đăng video
    # manager.upload_to_all("videos/video1.mp4", "Check this out! #tiktok", "#viral #trending")
    
    manager.logout_all()
    manager.close_all()
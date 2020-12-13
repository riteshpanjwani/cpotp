import os
import time
from pathlib import Path

import nltk
nltk_data_path = 'nltk_data/tokenizers/punkt' if os.name == 'posix' else 'AppData/Roaming/nltk_data/tokenizers/punkt'
if not os.path.exists(Path.home() / nltk_data_path):
    nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
import pyderman
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from cpotp._version import __version__


GOOGLE_MESSAGES_URL = "https://messages.google.com/web"
if not ('CHROME_USER_DATA_DIR' in os.environ and os.path.exists(Path(os.environ['CHROME_USER_DATA_DIR']))):
    print('''
        Please set CHROME_USER_DATA_DIR environment variable.
        Run chrome://version in Chrome/Edge/Chromium browser new tab
        and set this environment variable to path given in "Profile Path"
        except the "/Default" part.
        Example: export CHROME_USER_DATA_DIR=/home/riteshp/.config/google-chrome
    ''')


class CpOTP:
    def __init__(self):
        self._driver_path = pyderman.install(browser=pyderman.chrome)
        self._driver = self._init_driver()
        self._wait = WebDriverWait(self._driver, 10)

    def _init_driver(self):
        options = Options()
        options.add_argument("--enable-javascript")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        clean_user_data_dir = os.environ['CHROME_USER_DATA_DIR'].replace('/Default', '').strip().rstrip('/')
        options.add_argument(
            f"--user-data-dir={str(Path(clean_user_data_dir) / 'cpotp')}"
        )
        self._driver = webdriver.Chrome(self._driver_path, options=options)
        return self._driver

    def _login(self):
        toggle = self._wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
        self._driver.execute_script("arguments[0].click();", toggle)
        WebDriverWait(self._driver, 300).until(EC.url_contains('conversations'))

    def _grab_last_sms(self):
        elems = self._wait.until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, "//div[contains(@class,'conv-container')]/mws-conversation-list-item"))
        )
        if elems:
            msg_elem = elems[0].find_element(By.TAG_NAME, 'a')
            self._driver.execute_script("arguments[0].click();", msg_elem)
            txt_elems = self._wait.until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class,'text-msg')]"))
            )
            if txt_elems:
                return txt_elems[-1].text

    def _extract_otp(self, sms):
        window_size = 3
        tokens = [word.lower().strip() for sent in sent_tokenize(sms) for word in word_tokenize(sent)]
        for idx, word in enumerate(tokens):
            if word == 'otp' or word == 'code':
                context_tokens = tokens[idx+1:idx+window_size+1] + tokens[idx-window_size:idx]
                for context_token in context_tokens:
                    if context_token.isdigit():
                        return context_token
        return ''

    def get_otp(self):
        try:
            self._driver.get(GOOGLE_MESSAGES_URL)
            time.sleep(1)
            if 'conversations' not in self._driver.current_url:
                self._login()
                
            sms = self._grab_last_sms()
            otp = self._extract_otp(sms)
            if otp == '':
                print('OTP not found in the last received sms.')
            else:
                pyperclip.copy(otp)
                print('OTP has been copied to the clipboard.')           
        except Exception as e:
            print(str(e))
        finally:
            self._driver.quit()

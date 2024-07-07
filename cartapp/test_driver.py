# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 配置 Chrome 選項
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("detach", True)

# 安裝 ChromeDriver 並啟動瀏覽器
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 這裡可以寫你的測試代碼
driver.get("https://www.google.com")

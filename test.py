
from time import sleep
from DrissionPage import ChromiumPage
p = ChromiumPage()
p.get('https://dexscreener.com/moonshot')

sleep(5)
html_content = p.html

print(html_content)
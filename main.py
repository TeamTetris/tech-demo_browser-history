from chrome_browser import Chrome

chrome = Chrome()

if not chrome.is_installed():
    print("google chrome is not installed")
    exit(0)

for row in chrome.history():
    print(row)

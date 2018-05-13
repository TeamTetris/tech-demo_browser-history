from chrome_browser import Chrome
from firefox_browser import Firefox

chrome = Chrome()
if chrome.is_installed():
    print("====== history in google chrome ======")

    for (domain, visits) in chrome.history():
        print(domain + "\t" + str(visits) + " times visited")

else:
    print("google chrome is not installed")

firefox = Firefox()
if firefox.is_installed():
    print("====== history in mozilla firefox ======")

    for (domain, visits) in firefox.history():
        print(domain + "\t" + str(visits) + " times visited")

else:
    print("mozilla firefox is not installed")


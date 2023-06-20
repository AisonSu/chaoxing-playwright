from playwright.sync_api import sync_playwright, Playwright


def attachBrowser():
    instance = sync_playwright().start()
    browser = instance.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]
    return page

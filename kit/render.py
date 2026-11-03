import sys
from playwright.sync_api import sync_playwright
src, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width":1080,"height":1350})
    pg.goto("file://"+src); pg.wait_for_timeout(500)
    for i in range(1,n+1):
        pg.locator(f"#s{i}").screenshot(path=f"{out}/slide{i}.jpg", type="jpeg", quality=92)
    b.close()

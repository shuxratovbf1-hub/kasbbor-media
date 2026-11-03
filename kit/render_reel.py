import sys, subprocess
from playwright.sync_api import sync_playwright
# usage: render_reel.py page.html duration out.mp4 [frames_at_seconds...]
src, dur, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
stills = [float(x) for x in sys.argv[4:]]
fps = 30
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + src); pg.wait_for_timeout(600)
    if stills:
        for s in stills:
            pg.evaluate(f"draw({s})")
            pg.screenshot(path=f"{out}_t{s}.jpg", type="jpeg", quality=85)
        b.close(); sys.exit(0)
    tmp = out[:-4] + ".tmp.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
    n = int(dur * fps)
    for i in range(n):
        pg.evaluate(f"draw({i / fps})")
        ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
    ff.stdin.close(); rc = ff.wait(); b.close()
    if rc == 0:
        import os; os.replace(tmp, out)
    sys.exit(rc)

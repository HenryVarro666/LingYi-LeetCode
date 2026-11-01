"""Make a GIF next to every mp4 (GitHub's web UI shows GIFs but cannot play mp4).

python pipeline/gifs.py ROOT [--jobs 4] [--budget 150] [--width 1280] [--fps 5]
Skips videos whose .gif already exists; stops starting new jobs after --budget seconds (re-run to continue).
1280 px wide, 5 fps, 128-colour palette with frame differencing: about 1.5-2x the mp4 size, code stays readable.
"""
import argparse
import glob
import os
import subprocess
import time
from shlex import quote as shq

ap = argparse.ArgumentParser()
ap.add_argument('root')
ap.add_argument('--jobs', type=int, default=4)
ap.add_argument('--budget', type=float, default=150)
ap.add_argument('--width', type=int, default=1280)
ap.add_argument('--fps', type=int, default=5)
ap.add_argument('--tmp', default=None, help='where palette files go (default ROOT/_work/tmp); reused per worker, never deleted')
a = ap.parse_args()

# two passes (palette first, then encode) so ffmpeg never buffers the whole video in memory
SCALE = f'fps={a.fps},scale={a.width}:-1:flags=lanczos'
PAL = SCALE + ',palettegen=max_colors=128:stats_mode=diff'
USE = SCALE + '[x];[x][1:v]paletteuse=dither=none:diff_mode=rectangle'

todo = []
for pat in ('题解/*/*/*.mp4', '分类概念视频/*.mp4'):
    for mp4 in sorted(glob.glob(os.path.join(a.root, pat))):
        if mp4.endswith('.part.mp4'):
            continue
        if not os.path.exists(mp4[:-4] + '.gif'):
            todo.append(mp4)

TMP = a.tmp or os.path.join(a.root, '_work', 'tmp')
os.makedirs(TMP, exist_ok=True)
t0 = time.time()
running, done, fails = [], 0, 0
free = list(range(a.jobs))
while todo or running:
    while todo and len(running) < a.jobs and time.time() - t0 < a.budget:
        mp4 = todo.pop(0)
        slot = free.pop()
        part = mp4[:-4] + '.part.gif'  # written in place, then renamed (the folder may not allow deleting files)
        pal = os.path.join(TMP, f'palette_{slot}.png')
        cmd = (f"ffmpeg -v error -y -i {shq(mp4)} -vf {shq(PAL)} {shq(pal)} && "
               f"ffmpeg -v error -y -i {shq(mp4)} -i {shq(pal)} -lavfi {shq(USE)} -loop 0 -f gif {shq(part)}")
        p = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        running.append((p, mp4, part, slot))
    if not running:
        break
    time.sleep(0.2)
    for r in running[:]:
        p, mp4, part, slot = r
        if p.poll() is not None:
            running.remove(r)
            free.append(slot)
            if p.returncode == 0 and os.path.exists(part) and os.path.getsize(part) > 0:
                os.replace(part, mp4[:-4] + '.gif')
                done += 1
            else:
                fails += 1
                print('FAIL', os.path.relpath(mp4, a.root), (p.stderr.read() or '')[-200:])
print(f'gif made {done}; failed {fails}; remaining {len(todo)}; {time.time() - t0:.0f}s')

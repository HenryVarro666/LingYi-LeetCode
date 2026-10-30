"""Render every config under configs/ to out/<dir>/<name>.mp4 (skips existing).

python batch.py [--jobs 2] [--dirs ling,yiduobo,concept] [--force] [--only ling/0011,yiduobo/0042]
"""
import argparse
import concurrent.futures as cf
import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def render(cfg, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + '.part.mp4'
    t = time.time()
    p = subprocess.run([sys.executable, os.path.join(HERE, 'make.py'), cfg, tmp], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONHASHSEED='0'))
    if p.returncode == 0 and os.path.exists(tmp):
        os.replace(tmp, out)
        return cfg, True, f'{time.time() - t:.0f}s'
    return cfg, False, (p.stderr or p.stdout)[-800:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--dirs', default='ling,yiduobo,concept')
    ap.add_argument('--only', default='')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--reverse', action='store_true')
    ap.add_argument('--out', default=os.path.join(HERE, 'out'))
    a = ap.parse_args()
    todo = []
    for d in a.dirs.split(','):
        for cfg in sorted(glob.glob(os.path.join(HERE, 'configs', d, '*.py'))):
            name = os.path.splitext(os.path.basename(cfg))[0]
            key = f'{d}/{name}'
            if a.only and key not in a.only.split(','):
                continue
            out = os.path.join(a.out, d, name + '.mp4')
            if os.path.exists(out) and not a.force:
                continue
            todo.append((cfg, out))
    if a.reverse:
        todo.reverse()
    print(f'{len(todo)} to render', flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for cfg, ok, info in ex.map(lambda x: render(*x), todo):
            print(('OK  ' if ok else 'FAIL'), os.path.relpath(cfg, HERE), info if ok else '\n' + info, flush=True)


if __name__ == '__main__':
    main()

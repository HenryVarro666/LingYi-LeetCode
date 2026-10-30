"""Pack the engine (Mac -> cloud) or the new configs (cloud -> Mac) into a time-stamped tgz.

python pipeline/pack.py engine DIR     # whole engine (code + all configs) -> DIR/engine_<ts>.tgz   (run on the Mac)
python pipeline/pack.py configs DIR    # configs/{ling_all,yiduobo_all,skipped,failed} -> DIR/sync_<ts>.tgz (run in the cloud)
Prints the path of the archive.  Time-stamped names avoid stale copies when files are synced between machines.
"""
import os
import sys
import tarfile
import time

ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
what, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
ts = int(time.time())
SKIP_DIRS = {'__pycache__', 'out', 'preview'}


def add(tf, rel):
    p = os.path.join(ENGINE, rel)
    if not os.path.exists(p):
        return
    if os.path.isdir(p):
        for name in sorted(os.listdir(p)):
            if name in SKIP_DIRS or name.endswith(('.pyc', '.mp4')):
                continue
            add(tf, os.path.join(rel, name))
    else:
        tf.add(p, arcname=rel)


if what == 'engine':
    path = os.path.join(out_dir, f'engine_{ts}.tgz')
    with tarfile.open(path, 'w:gz') as tf:
        for name in sorted(os.listdir(ENGINE)):
            if name not in SKIP_DIRS and not name.endswith('.pyc'):
                add(tf, name)
else:
    path = os.path.join(out_dir, f'sync_{ts}.tgz')
    with tarfile.open(path, 'w:gz') as tf:
        for d in ('configs/ling_all', 'configs/yiduobo_all', 'configs/skipped', 'configs/failed'):
            add(tf, d)
print(path)

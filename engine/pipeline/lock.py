"""Run lock for scheduled batches (stored in LC_Video/_work/lock.json; files there can't be deleted, so we overwrite).

python pipeline/lock.py acquire NAME   -> prints ACQUIRED, or LOCKED <info> if another run heartbeated < 90 min ago
python pipeline/lock.py touch          -> refresh the heartbeat
python pipeline/lock.py release
"""
import json
import os
import sys
import time

P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '_work', 'lock.json')
STALE = 90 * 60


def load():
    try:
        return json.load(open(P))
    except Exception:
        return {}


cmd = sys.argv[1]
L = load()
now = time.time()
if cmd == 'acquire':
    if L.get('active') and now - L.get('t', 0) < STALE:
        print('LOCKED', L.get('by'), f"heartbeat {int((now - L['t']) / 60)} min ago")
    else:
        json.dump({'active': True, 't': now, 'started': now, 'by': sys.argv[2] if len(sys.argv) > 2 else '?'}, open(P, 'w'))
        print('ACQUIRED')
elif cmd == 'touch':
    L.update(active=True, t=now)
    json.dump(L, open(P, 'w'))
    print('touched')
elif cmd == 'release':
    L.update(active=False, t=now)
    json.dump(L, open(P, 'w'))
    print('released')

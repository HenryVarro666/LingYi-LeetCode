"""All remaining solutions (configs/ling_all, configs/yiduobo_all) -> LC_Video/题解/<bucket>/<NNNN 题名>/....mp4

python allsets.py next N [--skip-claimed FILE]   # next N problem keys (study-path order) that still need a config
python allsets.py status ROOT                    # counts: configs written / skipped / rendered
python allsets.py failed                         # quarantined configs still waiting for a fix
python allsets.py recheck-failed                 # re-check them; ones that pass now are restored (.fixed marker)
python allsets.py check KEYS [--quarantine]      # run --steps on configs of these keys (comma list, 'all-new',
                                                 #   or 'unrendered --root ROOT' = configs whose video is still missing);
                                                 # --quarantine moves failing configs to configs/failed/ (retried in a final repair pass)
python allsets.py render ROOT --jobs 4 --budget 150 [--only k1,k2]   # render configs whose video is missing
"""
import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import repo  # noqa: E402

SKIPDIR = os.path.join(HERE, 'configs', 'skipped')
# the Mac renders with Python 3.12 (~/py312), so checks in the cloud use a 3.12 interpreter when one is set up (/opt/py312)
PY = os.environ.get('LCV_PY') or ('/opt/py312/bin/python' if os.path.exists('/opt/py312/bin/python') else sys.executable)


def cfg_path(author, key):
    return os.path.join(HERE, 'configs', f'{author}_all', key + '.py')


def skip_path(author, key):
    return os.path.join(SKIPDIR, f'{author}_all', key + '.txt')


def failed_path(author, key):
    return os.path.join(HERE, 'configs', 'failed', f'{author}_all', key + '.py')


def pending(it):
    """authors of this problem that have no config, no skip note and no quarantined (failed) config"""
    return [a for a in it['todo'] if not any(os.path.exists(f(a, it['key'])) for f in (cfg_path, skip_path, failed_path))]


def nxt(n, exclude=()):
    out = []
    for it in repo.items():
        if it['key'] in exclude:
            continue
        if pending(it):
            out.append(it['key'])
            if len(out) >= n:
                break
    return out


def all_new_configs():
    """configs in configs/{ling,yiduobo}_all, minus ones quarantined in configs/failed/ (unless marked .fixed)"""
    out = []
    for a in ('ling', 'yiduobo'):
        for c in sorted(glob.glob(os.path.join(HERE, 'configs', f'{a}_all', '*.py'))):
            key = os.path.splitext(os.path.basename(c))[0]
            if os.path.exists(failed_path(a, key)) and not is_fixed(a, key):
                continue
            out.append(c)
    return out


def final_path(cfg):
    a = os.path.basename(os.path.dirname(cfg)).replace('_all', '')
    key = os.path.splitext(os.path.basename(cfg))[0]
    return repo.video(repo.by_key()[key], a)


def is_fixed(author, key):
    """a quarantined config counts as fixed once configs/failed/<author>_all/KEY.fixed exists (written by the repair)"""
    return os.path.exists(failed_path(author, key)[:-3] + '.fixed')


def unresolved_failed():
    """quarantined configs still waiting for a fix (no .fixed marker, no skip note)"""
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, 'configs', 'failed', '*_all', '*.py'))):
        a = os.path.basename(os.path.dirname(f)).replace('_all', '')
        key = os.path.splitext(os.path.basename(f))[0]
        if is_fixed(a, key) or os.path.exists(skip_path(a, key)):
            continue
        out.append(f)
    return out


def recheck_failed():
    """re-run --steps on quarantined configs; those that pass now (e.g. after the Python upgrade) go back into
    configs/*_all with a .fixed marker"""
    import shutil
    for f in unresolved_failed():
        p = subprocess.run([PY, os.path.join(HERE, 'make.py'), f, '--steps'], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONHASHSEED='0'), timeout=120)
        ok = p.returncode == 0 and 'estimated duration' in (p.stdout or '')
        a = os.path.basename(os.path.dirname(f)).replace('_all', '')
        key = os.path.splitext(os.path.basename(f))[0]
        if ok:
            shutil.copyfile(f, cfg_path(a, key))
            open(f[:-3] + '.fixed', 'w').write('passes after recheck\n')
        print('RESTORED' if ok else 'STILL FAILS', os.path.relpath(f, HERE))


def status(root=None):
    its = repo.items()
    need = sum(len(it['todo']) for it in its)
    cfgs = all_new_configs()
    skipped = glob.glob(os.path.join(SKIPDIR, '*', '*.txt'))
    failed = unresolved_failed()
    rendered = sum(os.path.exists(os.path.join(root, final_path(c))) for c in cfgs) if root else '?'
    left = sum(len(pending(it)) for it in its)
    print(f'videos to make (new): {need}; configs written: {len(cfgs)}; skipped: {len(skipped)}; '
          f'rendered: {rendered}; failed(quarantined): {len(failed)}; still pending: {left}')


def check(keys, quarantine=False, root=None):
    cfgs = all_new_configs()
    if keys == ['unrendered']:
        cfgs = [c for c in cfgs if not os.path.exists(os.path.join(root, final_path(c)))]
    elif keys != ['all-new']:
        cfgs = [c for c in cfgs if os.path.splitext(os.path.basename(c))[0] in keys]
    bad = []
    for c in cfgs:
        try:
            p = subprocess.run([PY, os.path.join(HERE, 'make.py'), c, '--steps'], capture_output=True, text=True,
                               env=dict(os.environ, PYTHONHASHSEED='0'), timeout=120)
        except subprocess.TimeoutExpired:
            bad.append((os.path.relpath(c, HERE), 'timeout'))
            continue
        tail = (p.stdout or '').strip().split('\n')[-1]
        if p.returncode != 0 or 'estimated duration' not in tail:
            bad.append((os.path.relpath(c, HERE), (p.stderr or p.stdout)[-300:]))
        else:
            print('OK  ', os.path.relpath(c, HERE), tail.split(':')[-1].strip())
    for c, e in bad:
        print('FAIL', c, e.replace('\n', ' | '))
        if quarantine:
            dst = os.path.join(HERE, 'configs', 'failed', os.path.relpath(os.path.join(HERE, c), os.path.join(HERE, 'configs')))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.replace(os.path.join(HERE, c), dst)
            if os.path.exists(dst[:-3] + '.fixed'):  # failed again after a "fix": the old marker no longer applies
                os.replace(dst[:-3] + '.fixed', dst[:-3] + '.fixed.old')
            open(dst[:-3] + '.err.txt', 'w').write(e)
            print('  -> moved to', os.path.relpath(dst, HERE))
    print(f'{len(cfgs) - len(bad)} ok, {len(bad)} failed')


def render(root, jobs=4, budget=150, only=None):
    t0 = time.time()
    todo = [c for c in all_new_configs() if not os.path.exists(os.path.join(root, final_path(c)))]
    if only:
        todo = [c for c in todo if os.path.splitext(os.path.basename(c))[0] in only]
    running, done, fails = [], 0, []
    while todo or running:
        while todo and len(running) < jobs and time.time() - t0 < budget:
            c = todo.pop(0)
            out = os.path.join(root, final_path(c))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            part = out[:-4] + '.part.mp4'
            p = subprocess.Popen([sys.executable, os.path.join(HERE, 'make.py'), c, part], stdout=subprocess.DEVNULL,
                                 stderr=subprocess.PIPE, text=True, env=dict(os.environ, PYTHONHASHSEED='0'))
            running.append((p, c, part, out))
        if not running:
            break
        time.sleep(0.3)
        for r in running[:]:
            p, c, part, out = r
            if p.poll() is not None:
                running.remove(r)
                if p.returncode == 0 and os.path.exists(part):
                    os.replace(part, out)
                    done += 1
                else:
                    fails.append(os.path.relpath(c, HERE))
                    print('FAIL', os.path.relpath(c, HERE), (p.stderr.read() or '')[-300:].replace('\n', ' | '))
    print(f'rendered {done}; failed {len(fails)}; remaining {len(todo)}; {time.time() - t0:.0f}s')


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    g = lambda k, f=str, d=None: f(args[args.index(k) + 1]) if k in args else d  # noqa: E731
    if cmd == 'next':
        ex = set(open(g('--skip-claimed')).read().split()) if '--skip-claimed' in args and os.path.exists(g('--skip-claimed')) else set()
        print(' '.join(nxt(int(args[0]), ex)))
    elif cmd == 'recheck-failed':
        recheck_failed()
    elif cmd == 'failed':
        for f in unresolved_failed():
            print(os.path.relpath(f, HERE))
    elif cmd == 'status':
        status(args[0] if args else None)
    elif cmd == 'check':
        check(args[0].split(',') if args and not args[0].startswith('--') else ['all-new'], '--quarantine' in args,
              g('--root'))
    elif cmd == 'render':
        render(args[0], g('--jobs', int, 4), g('--budget', float, 150), g('--only', lambda s: s.split(',')))

"""Build a LeetCode explainer video from a config file.

usage:
  python make.py CONFIG.py OUT.mp4            render
  python make.py CONFIG.py --steps            print the step list (line, caption) — fast sanity check
  python make.py CONFIG.py --preview 0,5,-1   save PNG frames of chosen keyframes to ./preview/
"""
import ast
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tracer  # noqa: E402
from engine import Video, Code, T, draw_vars  # noqa: E402
from common import Builder, read_time  # noqa: E402
import views as V  # noqa: E402

ACCENTS = {'灵茶山艾府': (255, 166, 87), 'yiduobo': (45, 212, 191), '概念讲解': (188, 140, 255)}
SHORT = {'灵茶山艾府': '灵神', 'yiduobo': 'yiduobo'}


def load_config(path):
    spec = importlib.util.spec_from_file_location('cfg', path)
    mod = importlib.util.module_from_spec(spec)
    mod.__dict__.update(tracer.base_namespace())
    spec.loader.exec_module(mod)
    return mod.CONFIG


# ------------------------------------------------------------------ captions
def _depth_label(frames):
    names = [f['name'] for f in frames]
    if not names:
        return ''
    rec = max(names.count(x) for x in set(names))
    if rec > 1:
        return f' · 递归深度 {rec}'
    if len(names) > 1:
        return f' · 在 {names[-1]}() 中'
    return ''


def merged(frames):
    S = {}
    for fr in frames:  # outermost first, inner overrides
        S.update(fr['locals'])
    return S


def _split_comment(src):
    s = src.strip()
    in_str = None
    for i, ch in enumerate(s):
        if in_str:
            if ch == in_str:
                in_str = None
        elif ch in '\'"':
            in_str = ch
        elif ch == '#':
            return s[:i].rstrip(), s[i + 1:].strip()
    return s, ''


def _sig(x):
    if x is None:
        return None
    return (getattr(x, '_uid', None), getattr(x, 'val', None),
            *[getattr(getattr(x, a, None), '_uid', None) for a in ('next', 'left', 'right', 'random')])


def _describe_changes(B, S, limit=3):
    out = []
    for k, v in S.items():
        if k.startswith('_'):
            continue
        if k not in B:
            out.append(f'`{k} = {V.fmt_var(v, 18)}`')
            continue
        bv = B[k]
        same = V.eq(bv, v)
        if isinstance(v, (tracer.ListNode, tracer.TreeNode, tracer.Node)) or isinstance(bv, (tracer.ListNode, tracer.TreeNode, tracer.Node)):
            same = _sig(bv) == _sig(v)
            if same:
                continue
            if getattr(bv, '_uid', 0) == getattr(v, '_uid', 0):
                for attr in ('next', 'left', 'right', 'random', 'val'):
                    a, b2 = getattr(bv, attr, None), getattr(v, attr, None)
                    if (getattr(a, '_uid', a) if attr != 'val' else a) != (getattr(b2, '_uid', b2) if attr != 'val' else b2):
                        out.append(f'`{k}.{attr} = {V.fmt_var(b2, 18)}`')
                continue
        if same:
            continue
        if isinstance(v, list) and isinstance(bv, list):
            if len(v) == len(bv) + 1 and v[:-1] == bv:
                out.append(f'`{k}` 末尾加入 `{V.fmt(v[-1], 10)}`')
            elif len(v) + 1 == len(bv) and v == bv[:-1]:
                out.append(f'`{k}` 弹出末尾 `{V.fmt(bv[-1], 10)}`')
            elif len(v) == len(bv):
                idx = [i for i in range(len(v)) if v[i] != bv[i]]
                if len(idx) <= 2:
                    out += [f'`{k}[{i}] = {V.fmt(v[i], 10)}`' for i in idx]
                else:
                    out.append(f'`{k}` 更新')
            else:
                out.append(f'`{k} = {V.fmt_var(v, 18)}`')
        elif isinstance(v, dict) and isinstance(bv, dict):
            ch = [kk for kk in v if kk not in bv or not V.eq(bv[kk], v[kk])]
            rm = [kk for kk in bv if kk not in v]
            out += [f'`{k}[{V.fmt_var(kk, 8)}] = {V.fmt(v[kk], 10)}`' for kk in ch[:2]]
            out += [f'删除 `{k}[{V.fmt_var(kk, 8)}]`' for kk in rm[:1]]
        elif isinstance(v, (set, frozenset)) and isinstance(bv, (set, frozenset)):
            out += [f'`{k}` 加入 `{V.fmt(x, 8)}`' for x in list(v - bv)[:2]]
            out += [f'`{k}` 移除 `{V.fmt(x, 8)}`' for x in list(bv - v)[:2]]
        else:
            out.append(f'`{k} = {V.fmt_var(v, 18)}`')
        if len(out) >= limit:
            break
    return out[:limit]


def _cond_detail(cond, B):
    try:
        node = ast.parse(cond, mode='eval').body
    except SyntaxError:
        return ''
    if isinstance(node, ast.Compare) and len(node.ops) == 1:
        lhs = V.ev(ast.unparse(node.left), B)
        rhs = V.ev(ast.unparse(node.comparators[0]), B)
        if lhs is not None and rhs is not None:
            op = ast.unparse(node).replace(ast.unparse(node.left), '', 1).replace(ast.unparse(node.comparators[0]), '').strip()
            return f'（`{V.fmt(lhs, 10)} {op} {V.fmt(rhs, 10)}`）'
    return ''


def default_caption(src, S, B, ret, kind):
    stmt, comment = _split_comment(src)
    pre = f'{comment}：' if comment else ''
    if kind == 'call':
        return pre + f'调用 → 进入新的一层：`{src.strip()[:60]}`'
    m = re.match(r'(if|elif|while)\s+(.*):\s*$', stmt)
    if m:
        cond = m.group(2)
        import copy as _copy
        try:
            B = _copy.deepcopy(B)  # conditions like `st.pop() != x` must not mutate the snapshot
        except Exception:
            return pre + f'判断 `{cond}`'
        r = V.ev(cond, B)
        if r is None and not isinstance(r, bool):
            return pre + f'判断 `{cond}`'
        word = '成立' if r else '不成立'
        tail = ' → 进入循环体' if (m.group(1) == 'while' and r) else (' → 循环结束' if m.group(1) == 'while' else '')
        return pre + f'判断 `{cond}`{_cond_detail(cond, B)} → =={word}=={tail}'
    if stmt.startswith('else'):
        return pre + '前面的条件不成立 → 走 `else`'
    if stmt.startswith('for ') or stmt.startswith('async for'):
        ch = _describe_changes(B, S)
        return pre + ('for 循环取下一个：' + '，'.join(ch) if ch else 'for 循环结束（没有下一个元素了）')
    if stmt.startswith('return'):
        return pre + f'返回 `{V.fmt_var(ret, 40)}`'
    ch = _describe_changes(B, S)
    if ch:
        return pre + f'执行 `{stmt[:48]}` → ' + '，'.join(ch)
    return pre + f'执行 `{stmt[:60]}`'


def render_caption(tmpl, S, B, ret):
    if callable(tmpl):
        es, eb = V._Env(S), V._Env(B)
        es['fmt'] = eb['fmt'] = V.fmt
        return tmpl(es, eb, ret)
    env = V._Env(S)
    env['B'] = V._Env(B)
    env['ret'] = ret
    env['fmt'] = V.fmt
    return eval('f' + repr(tmpl), {'__builtins__': __builtins__, 'inf': float('inf')}, env)


# ------------------------------------------------------------------ steps
def build_steps(cfg, code_lines, events):
    caps = cfg.get('captions', {})
    skip = cfg.get('skip', [])
    steps = []
    for i, e in enumerate(events):
        if e['kind'] != 'line':
            continue
        src = code_lines[e['line'] - 1] if e['line'] - 1 < len(code_lines) else ''
        st_src = src.strip()
        if st_src.startswith(('def ', 'class ', '@')) or not st_src or st_src.startswith('#'):
            continue
        if any((isinstance(sk, int) and sk == e['line']) or (isinstance(sk, str) and sk in src) for sk in skip):
            continue
        nxt = events[i + 1] if i + 1 < len(events) else None
        if nxt is not None and nxt['kind'] == 'line' and nxt['line'] == e['line'] and len(nxt['frames']) == len(e['frames']) \
                and nxt.get('thread') == e.get('thread'):
            continue  # inlined comprehension (py3.12+) or one-line loop: keep only the last event of the run
        after = events[i + 1] if i + 1 < len(events) else e
        B = merged(e['frames'])
        S = merged(after['frames'])
        ret = after['ret'] if after['kind'] == 'return' and len(after['frames']) == len(e['frames']) else None
        kind = 'call' if len(after['frames']) > len(e['frames']) else 'line'
        S['_line'] = B['_line'] = e['line']
        S['_thread'] = B['_thread'] = e.get('thread')
        S['_inner'] = after['frames'][-1]['locals'] if after['frames'] else {}
        B['_inner'] = e['frames'][-1]['locals'] if e['frames'] else {}
        cap = None
        for key, tmpl in caps.items():
            hit = (isinstance(key, int) and key == e['line']) or (isinstance(key, str) and key in src)
            if hit:
                try:
                    cap = render_caption(tmpl, S, B, ret)
                except Exception as ex:  # noqa: F841
                    cap = None
                break
        if cap is None:
            cap = default_caption(src, S, B, ret, kind)
        S['_line'] = e['line']
        B['_line'] = e['line']
        S['_thread'] = B['_thread'] = e.get('thread')
        S['_inner'] = after['frames'][-1]['locals'] if after['frames'] else {}
        B['_inner'] = e['frames'][-1]['locals'] if e['frames'] else {}
        steps.append(dict(line=e['line'], S=S, B=B, frames=after['frames'], cap=cap, depth=len(e['frames'])))
    return steps


def compress(steps, max_steps):
    if len(steps) <= max_steps:
        return steps
    tail = min(12, max_steps // 4)
    head = max_steps - tail
    gap = len(steps) - head - tail
    mid = dict(steps[head - 1])
    mid = dict(mid, cap=f'…… 中间 {gap} 步同理，快进 ……', ff=True)
    return steps[:head] + [mid] + steps[-tail:]


# ------------------------------------------------------------------ video
def make_video(cfg):
    author = cfg.get('author', '灵茶山艾府')
    accent = tuple(cfg.get('accent', ACCENTS.get(author, (255, 166, 87))))
    code_src = cfg['code'].strip('\n')
    code = Code(code_src) if cfg.get('show_code', True) else None
    code_lines = code_src.split('\n')
    specs = cfg.get('views', [])

    tracer._origin.clear()
    tracer._input_rows = __import__('itertools').count(0)
    tracer._SNAP_MAXLEN = cfg.get('snap_maxlen')
    result, events, ns = tracer.run(code_src, cfg['call'], max_events=cfg.get('max_events', 6000), setup=cfg.get('setup', ''),
                                    threads=cfg.get('threads', False), trace_limit=cfg.get('trace_limit'))
    check = cfg.get('check')
    if 'expect' in cfg:
        got = cfg['result_fn'](result) if cfg.get('result_fn') else result
        if got != cfg['expect']:
            raise AssertionError(f'result {got!r} != expect {cfg["expect"]!r}')
    if check and not check(result):
        raise AssertionError(f'check failed on result {result!r}')

    steps = build_steps(cfg, code_lines, events)
    if ns.get('__truncated__') and steps:  # trace_limit reached: the rest ran untraced
        steps.append(dict(steps[-1], cap=cfg.get('truncated_caption', '…… 后面的循环同理，快进到结束 ……'), ff=True))
    steps = compress(steps, cfg.get('max_steps', 70))
    ctx = {'accent': accent, 'll_pos': V.linked_positions([s['S'] for s in steps])}

    vb = (40, 130, 1060, 780)

    def draw_viz(cv, st, box):
        x0, y0, x1, y1 = box[0], vb[1], box[2], vb[3]
        hs = [V.VIEWS[sp['type']][1](sp) for sp in specs]
        avail = (y1 - y0) - 16
        scale = min(1.0, avail / max(1, sum(hs)))
        y = y0 + 12
        for vi, (sp, h) in enumerate(zip(specs, hs)):
            hh = h * scale
            V.VIEWS[sp['type']][0](cv, sp, st, (x0, y, x1, y + hh), vi, ctx)
            y += hh

    tags = [cfg.get('category', '')] + list(cfg.get('tags', []))
    v = Video(cfg['num'] if cfg.get('num') is not None else '', cfg['title'], author, accent, [t for t in tags if t],
              code, draw_viz, cfg.get('difficulty', ''))
    if cfg.get('badge'):
        v.author = cfg['badge'].replace(' 题解', '')
    b = Builder(v, {})
    cards = cfg.get('cards', {})
    kind = cfg.get('kind', 'problem')
    short = SHORT.get(author, author)
    big = f"{cfg['num']}. {cfg['title']}" if cfg.get('num') is not None else cfg['title']
    title_lines = [x for x in [cards.get('one_liner') and f"一句话：{cards['one_liner']}",
                               cards.get('complexity') and f"复杂度：{cards['complexity']}"] if x]
    sub = f"{author} · {cfg.get('technique', cfg.get('category', ''))}"
    if kind == 'concept':
        try:
            import json as _json
            items = _json.load(open(os.path.join(HERE, 'hot100.json'), encoding='utf-8'))
            ncat = sum(1 for it in items if it['cat'] == cfg.get('category'))
            sub = f"Hot100 · {cfg.get('category')} · 本类 {ncat} 道题的通用思想与模板"
        except Exception:
            pass
    b.card({'kind': 'title', 'big': big, 'sub': sub,
            'lines': title_lines}, '① 开场')
    if cards.get('problem'):
        b.card({'heading': cards.get('problem_heading', '题意'), 'lines': cards['problem']}, '① 题目')
    for extra in cards.get('before', []):
        b.card(extra, extra.get('chapter', '② 概念'))
    if cards.get('quote') or cards.get('idea'):
        b.card({'heading': cards.get('idea_heading', f'{short}的思路'), 'quote': cards.get('quote'),
                'src': cards.get('quote_src', f'—— {author}题解原文'), 'lines': cards.get('idea', [])}, '② 思路')

    n = len(steps)
    b.s.update({'_chapter': '③ 逐步演示'})
    for k, s in enumerate(steps):
        st = {'hl': s['line'] - 1, '_S': s['S'], '_B': s['B'], '_frames': s['frames'], '_cap': s['cap'],
              '_step': f"步骤 {k + 1}/{n}" + _depth_label(s['frames'])}
        watch = []
        for w in cfg.get('watch', []):
            if isinstance(w, str):
                w = (w, w)
            val = V.ev(w[1], s['S'])
            if val is None and w[1] not in s['S']:
                continue
            watch.append((w[0], V.fmt_var(val, 24)) + ((V.col(w[2]),) if len(w) > 2 else ()))
        st['_vars'] = watch
        for vi, sp in enumerate(specs):
            for name, val in V.ptr_values(sp, s['S']).items():
                st[f'p{vi}:{name}'] = float(val)
        # drop stale pointer keys from previous state
        for key in [kk for kk in b.s if kk.startswith('p') and ':' in kk and kk not in st]:
            del b.s[key]
        fast = 0.7 if k > 24 else 1.0
        cap_hold = read_time(s['cap'], lo=0.7, hi=3.2, cps=15) * fast
        if s.get('ff'):
            cap_hold = 1.4
        b.step(hold=cap_hold, trans=0.3, **st)
    b.s['_step'] = '结束'
    if cards.get('result'):
        b.step(hold=read_time(cards['result'], lo=1.5, hi=4.0), trans=0.3, _cap=cards['result'])
    else:
        b.step(hold=1.8, trans=0.3, _cap=f'运行结束，返回 `{V.fmt_var(result, 40)}`' + (' ✓ 与示例答案一致' if 'expect' in cfg else ''))
    for extra in cards.get('after', []):
        b.card(extra, extra.get('chapter', '④ 拓展'))
    if cards.get('summary'):
        b.card({'heading': cards.get('summary_heading', '小结 & 易错点'), 'lines': cards['summary']}, '④ 小结')
    return v, steps, result


def main():
    cfg_path = sys.argv[1]
    cfg = load_config(cfg_path)
    v, steps, result = make_video(cfg)
    if '--steps' in sys.argv:
        print(f'result = {result!r}; {len(steps)} steps; {len(v.keys)} keyframes')
        for k, s in enumerate(steps):
            print(f'{k:3d} L{s["line"]:<3d} {s["cap"]}')
        tot = sum(h + t for _, h, t in v.keys)
        print(f'estimated duration: {tot:.0f}s')
        return
    if '--preview' in sys.argv:
        idx = sys.argv[sys.argv.index('--preview') + 1]
        out = os.path.join(os.getcwd(), 'preview')
        os.makedirs(out, exist_ok=True)
        base = os.path.splitext(os.path.basename(cfg_path))[0]
        for i in [int(x) for x in idx.split(',')]:
            i = i if i >= 0 else len(v.keys) + i
            p = f'{out}/{base}_{cfg.get("author", "")}_{i}.png'
            v.frame(v.keys[i][0]).convert('RGB').save(p)
            print(p)
        return
    out = sys.argv[2]
    dur = v.render(out)
    print(f'{out}  {dur:.0f}s')


if __name__ == '__main__':
    main()

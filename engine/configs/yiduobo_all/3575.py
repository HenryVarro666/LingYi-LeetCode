VALS = [3, 22, 5, 12, 4]
PAR = [-1, 0, 1, 1, 0]
KIDS = [[] for _ in PAR]
for _i in range(1, len(PAR)):
    KIDS[PAR[_i]].append(_i)


def _digits(v):
    s = set()
    for ch in str(v):
        if ch in s:
            return None
        s.add(ch)
    return ''.join(sorted(s))


def _ms(mask):
    return '{' + ','.join(str(d) for d in range(10) if mask >> d & 1) + '}' if mask else '{}'


_POS = {}


def _layout():
    cnt = [0]
    def go(u, d):
        if not KIDS[u]:
            xs = cnt[0]
            cnt[0] += 1
        else:
            xs = sum(go(c, d + 1) for c in KIDS[u]) / len(KIDS[u])
        _POS[u] = (xs, d)
        return xs
    go(0, 0)
    return cnt[0]


_NL = _layout()


def _maxscore(u):
    nodes, st = [], [u]
    while st:
        w = st.pop()
        nodes.append(w)
        st.extend(KIDS[w])
    best = 0
    items = [(w, sum(1 << int(c) for c in set(str(VALS[w])))) for w in nodes if _digits(VALS[w]) is not None]
    for m in range(1 << len(items)):
        used, tot, ok = 0, 0, True
        for k, (w, mk) in enumerate(items):
            if m >> k & 1:
                if used & mk:
                    ok = False
                    break
                used |= mk
                tot += VALS[w]
        if ok:
            best = max(best, tot)
    return best


def _order(u):
    out = []
    for c in KIDS[u]:
        out += _order(c)
    return out + [u]


CUM = {}
_run = 0
for _u in _order(0):
    _run += _maxscore(_u)
    CUM[_u] = _run


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '树（节点里是 vals[i]，黄 = 当前 now，青 = 正在合并的儿子 nxt，红 = 数位重复不能选）', 21, T['muted'], bold=True)
    w, h = x1 - x0 - 120, y1 - y0 - 120
    def P(u):
        xs, d = _POS[u]
        return (x0 + 60 + (xs + 0.5) / _NL * w, y0 + 80 + d * h / 2)
    x = S.get('now')
    y = S.get('nxt')
    for u in range(1, len(PAR)):
        cv.line([P(PAR[u]), P(u)], T['border'], 3)
    for u in range(len(PAR)):
        px, py = P(u)
        bad = _digits(VALS[u]) is None
        fill = T['yellow'] if u == x else T['cyan'] if u == y else T['panel2']
        r = 36
        cv.rect((px - r - 14, py - r, px + r + 14, py + r), fill=fill, outline=T['red'] if bad else T['border'], width=4 if bad else 2, r=r)
        cv.text((px, py - 6), VALS[u], 32, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py + 22), f'#{u} {_ms(sum(1 << int(c) for c in set(str(VALS[u]))))}' if not bad else f'#{u} 重复', 16,
                T['bg'] if fill != T['panel2'] else T['dim'], anchor='mm', mono=True)


def _fmt(k, v):
    return f'{_ms(k)}→{v}'


CONFIG = dict(
    num=3575, title='最大好子树分数', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='树形 DP + 数位状压 · 逐个儿子合并',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 2360'],
    code='''
class Solution(object):
    def goodSubtreeSum(self, vals, par):
        
        n = len(vals)
        g = [[] for _ in range(n)]
        for index, p in enumerate(par[1:], 1):
            g[p].append(index)
        
        global res
        res = 0
        mod = 10 ** 9 + 7
        def dfs(now):
            f = {}

            state = 0
            v = vals[now]
            while v:
                r = v % 10
                v //= 10
                if state & (1 << r) == (1 << r):
                    state = -1
                    break
                state |= (1 << r)
            
            if state != -1:
                f[state] = vals[now]
            
            for nxt in g[now]:
                sub_f = dfs(nxt)
                tmp = copy.deepcopy(f)
                for sub_state, sub_v in sub_f.items():
                    f[sub_state] = max(f.get(sub_state, 0), sub_v)
                    for state, v in tmp.items():
                        if state & sub_state == 0:
                            merge_state = state | sub_state
                            f[merge_state] = max(f.get(merge_state, 0), v + sub_v)

            if f:
                global res
                res += max(f.values())
                if res >= mod:
                    res -= mod
            
            return f
        
        dfs(0)
        return res
''',
    setup='import copy',
    call='Solution().goodSubtreeSum([3, 22, 5, 12, 4], [-1, 0, 1, 1, 0])',
    expect=62,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='f', label='f：now 子树里「数位集合 → 最大分数」', h=170, fmt=_fmt, font=24),
        dict(type='text', fn=lambda S: (f"now = {S['now']}（vals = {VALS[S['now']]}）" if 'now' in S else '') + (f"   `res` = =={CUM[S['now']]}==" if S.get('_line') in (40, 41, 42) else ''), size=28, h=60),
    ],
    watch=[('now', 'now', 'yellow'), ('nxt', 'nxt', 'cyan'), ('state', 'state', 'purple')],
    captions={
        'g[p].append(index)': '`g[{p}]` 记下儿子 `{index}`',
        'res = 0': '`res` 累加每个节点的最大好子集分数',
        'v = vals[now]': lambda S, B, r: f'==节点 {S.now}==，`vals = {VALS[S.now]}`：逐位拆开，`state` 用二进制记数位集合。' + ('数位 ' + str(VALS[S.now]) + ' 里有重复 → `state = -1`，这个点不能选' if _digits(VALS[S.now]) is None else f'数位互不相同 → 集合 `{_ms(sum(1 << int(c) for c in set(str(VALS[S.now]))))}`'),
        'f[state] = vals[now]': lambda S, B, r: f'`state != -1` 可用：`f[{_ms(S.state)}] = {S.vals[S.now]}`',
        'sub_f = dfs(nxt)': lambda S, B, r: (f'进入儿子 `nxt = {S.nxt}`，先递归算它的 `f`' if S['_inner'].get('now') == S.nxt else f'儿子 `{S.nxt}` 返回 `sub_f = {dict(S.sub_f)}`'),
        'f[sub_state] = max': lambda S, B, r: f'情况一：直接用儿子子树的 `{_ms(S.sub_state)}`（分数 `{S.sub_v}`）来更新：`f[{_ms(S.sub_state)}]` = {S.f[S.sub_state]}。合并要用副本 `tmp`，因为 `f` 正在改',
        'if state & sub_state == 0': lambda S, B, r: f'`tmp` 里的 `{_ms(S.state)}` 和儿子的 `{_ms(S.sub_state)}` ' + ('==没有公共数位== → 可以合并' if S.state & S.sub_state == 0 else '有公共数位 → 不能同时选'),
        'f[merge_state] = max': lambda S, B, r: f'情况二：`tmp` 的 `{_ms(S.state)}` 与儿子的 `{_ms(S.sub_state)}` ==没有公共数位== → 合并成 `{_ms(S.merge_state)}`，`{S.v} + {S.sub_v}` = `f[{_ms(S.merge_state)}]` 变成 =={S.f[S.merge_state]}==',
        'res += max(f.values())': lambda S, B, r: f'`maxScore[{S.now}] = {max(S.f.values())}` 累加到 `res`：`res = {CUM[S.now]}`',
        'return res': '全部节点的 maxScore 之和 =={ret}==（没超过 `mod`）',
    },
    skip=[34, 4, 5, 6, 7, 9, 11, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 25, 28, 30, 31, 33, 35, 38, 39, 41, 44],
    max_steps=140,
    cards=dict(
        one_liner='f[状态] = 子树里这些数位被占用时的最大总和，儿子一个个合并进来',
        complexity='时间 `O(n·4^D)`，空间 `O(n·2^D)`，`D = 10`',
        problem=['无向树，根 `0`，节点值 `vals[i]`；子树里选一些节点，十进制数位 0–9 每个数字至多出现一次才是好子集',
                 '`maxScore[u]` 是 `u` 的子树里好子集的最大总和，求所有 `maxScore` 之和',
                 '本视频：`vals=[3,22,5,12,4]`，`par=[-1,0,1,1,0]` → `62`'],
        quote='首先，从题目中关于好子集的定义来看，0到9每个数字只能出现一次，那么完全可以利用状态压缩来表示子集中已经有哪些数字。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[now][state]`：以 `now` 为根的子树，选出节点占用数位为 `state` 时的最大总和',
              '先看 `vals[now]` 自己：逐位拆开，有重复数位就不可用，否则 `f[state] = vals[now]`',
              '再遍历儿子 `nxt`：先用 `sub_f` 更新 `f`，再和 `f` 的副本里 `state & sub_state == 0` 的合并',
              '每个节点的 `max(f.values())` 累加到答案'],
        summary=['时间 `O(n·4^D)`：每条边做一次两层循环；空间 `O(n·2^D)`',
                 '合并必须用 `tmp`（`f` 的副本），否则一边遍历一边改会重复使用同一个儿子',
                 '原文用到 `copy.deepcopy`，运行时在 setup 里补上了 `import copy`，代码本身未改',
                 '对比灵神：灵神用 `defaultdict` + 启发式合并，只把小的一边并进大的；yiduobo 每个儿子整张表合并',
                 '`res` 用 `global` 累加，每次超过 `mod` 就减一次 `mod`'],
    ),
)

def _layout_tree(n, edges, root=0):
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)
    pos, nxt = {}, [0]

    def go(x, fa, d):
        ch = [y for y in g[x] if y != fa]
        if not ch:
            pos[x] = (nxt[0], d)
            nxt[0] += 1
        else:
            for y in ch:
                go(y, x, d + 1)
            pos[x] = (sum(pos[y][0] for y in ch) / len(ch), d)
    go(root, -1, 0)
    return pos, nxt[0], max(d for _, d in pos.values()) + 1


def _draw_tree(cv, box, T, n, edges, fill, sub, ring=None, title='', subcolor='muted', inner=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    pos, w, h = _layout_tree(n, edges)
    sp = min(170, (x1 - x0 - 60) / max(1, w))
    R = max(18, min(28, sp * 0.36))
    dy = min(120, (y1 - y0 - 70 - 2 * R - 40) / max(1, h - 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * w) / 2 + sp / 2
    P = {k: (sx + a * sp, y0 + 60 + R + d * dy) for k, (a, d) in pos.items()}
    for a, b in edges:
        (ax, ay), (bx, by) = P[a], P[b]
        if pos[a][1] > pos[b][1]:
            (ax, ay), (bx, by) = (bx, by), (ax, ay)
        cv.line([(ax, ay), (bx, by)], T['dim'], 3)
    for k, (cx, cy) in P.items():
        c = fill.get(k)
        cv.rect((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'], outline=T['yellow'] if k == ring else T['border'],
                width=5 if k == ring else 3, r=R)
        cv.text((cx, cy), k, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        s = sub.get(k)
        if s not in (None, ''):
            tw = cv.tlen(s, 21, bold=True) + 10
            cv.rect((cx - tw / 2, cy + R + 4, cx + tw / 2, cy + R + 32), fill=T['panel'], r=6)
            cv.text((cx, cy + R + 8), s, 21, T[subcolor], anchor='mt', bold=True)


SNAP = {}
DONE = {}


def trk(fn=None, rec=None, reset=False):
    """caption wrapper: remember which nodes have returned (node -> returned value), keyed by this step's innermost-locals object"""
    def cap(S, B, ret):
        if reset:
            DONE.clear()
        if rec is not None:
            kv = rec(S, B, ret)
            if kv is not None:
                DONE[kv[0]] = kv[1]
        SNAP[id(S['_inner'])] = dict(DONE)
        return fn(S, B, ret) if callable(fn) else None
    return cap


def _done(S):
    return SNAP.get(id(S['_inner']), {})


def fill_caps(code, caps):
    """give every other statement line a tracking (default-text) caption"""
    out = dict(caps)
    for l in code.strip('\n').split('\n'):
        s = l.strip()
        if not s or s.startswith(('def ', 'class ', '#')) or any(k in l for k in out):
            continue
        out[s] = trk()
    return out
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4]]
NUMS = [2, 2, 2, 1, 1]


def _draw(cv, S, B, box, T):
    nums = S.get('nums')
    if nums is None:
        return
    done, inner, tg = _done(S), S['_inner'], S.get('target')
    cur = inner.get('now')
    fill, sub = {}, {}
    for i in range(len(nums)):
        sub[i] = str(nums[i])
        if i in done:
            v = done[i]
            fill[i] = 'green' if v == 0 else ('red' if tg is not None and v > tg else 'orange')
            sub[i] += f' → {v}'
    if cur is not None and cur not in done:
        fill[cur] = 'blue'
        sub[cur] += f'  已凑 {inner.get("val")}'
    _draw_tree(cv, box, T, len(nums), EDGES, fill, sub, ring=cur,
               title='树（蓝 = 正在处理，绿 = 返回 0（自成一块），橙 = 返回不足的和，红 = 超出；下方：点权 → 返回值）')


def _info(S):
    t = S.get('target')
    if t is None:
        return ''
    return f'节点和 `s = {S.get("s")}`，试切成 `parts = {S.get("parts")}` 块 → 每块 `target = {t}`'


CODE = '''
class Solution(object):
    def componentValue(self, nums, edges):

        s = sum(nums)
        n = len(nums)
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        def check(now, fa, v):
            val = nums[now]
            for next in g[now]:
                if next == fa:
                    continue
                
                rest = check(next, now, v)
                if rest + val > v:
                    return rest + val
                else:
                    val += rest
            
            if val == v:
                return 0
            else:
                return val

        for parts in range(n, 1, -1):
            if s % parts == 0:
                target = s // parts
                if check(0, -1, target) == 0:
                    return parts - 1
        
        return 0
'''
CAPS = {
    's = sum(nums)': trk(lambda S, B, r: f'`s = {S.s}`：所有节点值之和，每块的和必须是 `s / 块数`', reset=True),
    'g = {index': trk(lambda S, B, r: '建图：每个节点对应一个邻居集合；`n` 个点最多切成 `n` 块'),
    'val = nums[now]': trk(lambda S, B, r: f'处理节点 `{S.now}`：它所在连通块目前的和 `val = {S.val}`'),
    'for next in g[now]': trk(lambda S, B, r: (f'下一个邻居 `{S.next}`' + ('，是父节点 `fa`，直接跳过' if S.next == S.fa else '，是孩子，递归求它所在块的和')
                                               if S['_inner'].get('next') != B['_inner'].get('next') else f'`{S.now}` 的孩子都处理完了，`val = {S.val}`')),
    'rest = check': trk(lambda S, B, r: f'先递归孩子 `{B.next}`：返回它那一块 ==还没凑满的和==（凑满自成一块则返回 0）'),
    'if rest + val > v': trk(lambda S, B, r: f'`rest + val = {B.rest} + {B.val} = {B.rest + B.val}`，' + ('==超过 target，不可能合法=='
                                                                                  if B.rest + B.val > B.v else '没超过 → 并入当前块（`val += rest`）')),
    'return rest + val': trk(lambda S, B, r: f'超出 `v = {S.v}` → 直接返回 `{r}`（非 0），这个 target 失败', rec=lambda S, B, r: (S.now, r)),
    'val += rest': trk(lambda S, B, r: f'孩子那块没凑满就并进来：`val = {B.val} + {B.rest} = {S.val}`（孩子返回 0 时等于不变）'),
    'return 0': trk(lambda S, B, r: f'凑满了：把这块独立切下来（和父节点断边），返回 `0`', rec=lambda S, B, r: (S.now, 0)),
    'return val': trk(lambda S, B, r: f'`val = {r} < v = {S.v}` 没凑满：把 `{r}` 交给父节点，继续并入它所在的块', rec=lambda S, B, r: (S.now, r)),
    'for parts in range': trk(lambda S, B, r: (f'枚举块数 `parts = {S.parts}`（从大到小，先试删边多的）'
                                               if S['_inner'].get('parts') != B['_inner'].get('parts') else '所有块数都不行')),
    'if s % parts': trk(lambda S, B, r: f'`{S.s} % {S.parts} = {S.s % S.parts}` → ' + ('能整除，每块和相等才有可能' if S.s % S.parts == 0 else '不能整除，==每块和不是整数== → 跳过')),
    'target = s // parts': trk(lambda S, B, r: f'`target = {S.s} // {S.parts} = {S.target}`：每块的节点值之和', reset=True),
    'if check(0, -1, target) == 0': trk(lambda S, B, r: '从根 `0` 向下递归；若返回 `0`，整棵树恰好分成 `parts` 块'),
    'return parts - 1': trk(lambda S, B, r: f'切成 `{S.parts}` 块，要删 `{S.parts} - 1 = {r}` 条边'),
    'return 0': None,
}
CAPS.pop('return 0')
CAPS['return 0'] = trk(lambda S, B, r: f'`val == v = {S.v}`，凑满了：这块独立切下，返回 `0`' if 'now' in S['_inner'] else '没有任何块数可行，返回 `0`',
                       rec=lambda S, B, r: (S['_inner']['now'], 0) if 'now' in S['_inner'] else None)
CONFIG = dict(
    num=2440, title='创建价值相同的连通块', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='枚举块数 + 递归判定可行', tags=['灵神题单·链表树与回溯', '难度分 2460'],
    code=CODE,
    call=f'Solution().componentValue({NUMS}, {EDGES})',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=390),
        dict(type='text', fn=_info, h=50),
        dict(type='calls', h=150),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('val', lambda S: S['_inner'].get('val')), ('target', 'target', 'green'), ('parts', 'parts', 'orange')],
    captions=fill_caps(CODE, CAPS),
    skip=['for x, y in edges', 'g[x].add', 'g[y].add', 'if next == fa', 'continue', 'val += rest', 'if val == v', 'n = len(nums)'],
    max_steps=120,
    cards=dict(
        one_liner='先自底向上凑满一块就切断，凑不满的和交给父节点',
        complexity='时间 `O(n·d)`，`d` 为总和的因子数（至多 240）；空间 `O(n)`',
        problem=['无向树，点权 `nums[i]`；删掉若干条边，让所有连通块的点权和 ==相等==',
                 '求最多能删多少条边',
                 '本视频：`nums=[2,2,2,1,1]`，树 `0-1, 0-2, 1-3, 1-4` → `1`'],
        quote='整棵树所有节点之和最大也只有一百万，而在小于等于一百万的整数中，约数最多的应该是720720，总共也仅有240个约数，也就是说，在这里完全可以枚举最终树被切分成了多少块',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举块数 `parts`，要求 `s % parts == 0`，每块和 `target = s // parts`',
              '叶子 `> target` 无解；`= target` 独立成块；`< target` 必须并入父节点',
              '递归时：孩子返回的和并入当前块，==凑满 target 就返回 0（切断），超出就一路失败向上=='],
        result='`parts = 4` 失败（有一块和超过 2），`parts = 2` 成功：只要切一条边',
        summary=['原文为 Python 2 写法，整数除法 `s / parts` 已改为 `s // parts`，其余代码不变',
                 '时间 `O(n·d)`：每个块数只要 `O(n)` 的 DFS，块数只试总和的因子',
                 '易错：返回 `0` 代表「凑满切断」，返回非 0 且 `> target` 代表失败，但原代码靠逐层把和往上传来表达，不必区分',
                 '对比灵神：他明确用 `-1` 表示失败，并把块数上界收紧到 `total // max(nums)`；yiduobo 从 `n` 开始枚举'],
    ),
)

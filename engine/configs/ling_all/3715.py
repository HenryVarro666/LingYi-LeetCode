N = 6
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]]
NUMS = [2, 8, 3, 2, 12, 27]


def _core(v):
    i = 2
    while i * i <= v:
        while v % (i * i) == 0:
            v //= i * i
        i += 1
    return v


CORES = [_core(v) for v in NUMS]
_ch = {i: [] for i in range(N)}
PAR = {0: -1}
for _a, _b in EDGES:
    _ch[_a].append(_b)
    PAR[_b] = _a
DEPTH = {0: 0}
for _a, _b in EDGES:
    DEPTH[_b] = DEPTH[_a] + 1
_pos, _cnt = {}, [0]


def _lay(u):
    if not _ch[u]:
        _pos[u] = float(_cnt[0])
        _cnt[0] += 1
    else:
        for c in _ch[u]:
            _lay(c)
        _pos[u] = sum(_pos[c] for c in _ch[u]) / len(_ch[u])


_lay(0)
LEAVES = _cnt[0]


def _anc(x):
    r = []
    while x != -1:
        r.append(x)
        x = PAR[x]
    return r


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '树（圆内 = nums，下方 = core；黄 = 当前，绿 = 祖先里 core 相同）', 22, T['muted'], bold=True)
    cur = S.get('x') if '_inner' in S else None
    cur = S['_inner'].get('x') if isinstance(S.get('_inner'), dict) and 'x' in S['_inner'] else cur
    pathset = set(_anc(PAR[cur])) if cur is not None and cur in PAR and PAR[cur] != -1 else set()
    cell = min(190, (x1 - x0 - 120) / max(1, LEAVES - 1)) if LEAVES > 1 else 0
    sx = x0 + 60 + ((x1 - x0 - 120) - cell * (LEAVES - 1)) / 2
    dmax = max(DEPTH.values())
    top = y0 + 80
    dy = min(120, (y1 - top - 90) / max(1, dmax))
    P = {u: (sx + _pos[u] * cell, top + DEPTH[u] * dy) for u in range(N)}
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 3)
    for u in range(N):
        px, py = P[u]
        fill = T['panel2']
        if cur is not None and u == cur:
            fill = T['yellow']
        elif u in pathset and CORES[u] == CORES[cur]:
            fill = T['green']
        elif u in pathset:
            fill = (70, 80, 96)
        cv.rect((px - 40, py - 32, px + 40, py + 32), fill=fill, r=32, outline=T['border'])
        dark = fill in (T['yellow'], T['green'])
        cv.text((px, py), NUMS[u], 30, T['bg'] if dark else T['text'], anchor='mm', bold=True)
        cv.text((px + 46, py + 4), f'core {CORES[u]}', 18, T['cyan'], anchor='lm', mono=True)
        cv.text((px - 46, py + 4), u, 16, T['dim'], anchor='rm', mono=True)


CONFIG = dict(
    num=3715, title='完全平方数的祖先个数总和', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='core 值相同 · 树上 DFS 计数',
    tags=['难度分 2235'],
    setup='''
from math import isqrt
MX = 100_001
core = [0] * MX
for i in range(1, MX):
    if core[i] == 0:
        for j in range(1, isqrt(MX // i) + 1):
            core[i * j * j] = i
''',
    code='''
class Solution:
    def sumOfAncestors(self, n: int, edges: List[List[int]], nums: List[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        cnt = defaultdict(int)
        ans = 0

        def dfs(x: int, fa: int) -> None:
            nonlocal ans
            c = core[nums[x]]
            # 本题 x 的祖先不包括 x 自己
            ans += cnt[c]
            cnt[c] += 1
            for y in g[x]:
                if y != fa:
                    dfs(y, x)
            cnt[c] -= 1  # 恢复现场

        dfs(0, -1)
        return ans
''',
    call='Solution().sumOfAncestors(6, [[0,1],[0,2],[1,3],[1,4],[2,5]], [2,8,3,2,12,27])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=150),
        dict(type='map', var='cnt', label='cnt：路径上各 core 值出现次数', fmt=lambda k, v: f'core {k}: {v}', h=110, font=30),
    ],
    watch=['x', 'c', ('ans', 'ans', 'green')],
    captions={
        'g = [[]': '先把 `edges` 建成邻接表 `g`（无向边，两个方向都存）',
        'cnt = defaultdict': '`cnt[c]`：==当前路径（根到父亲）上== core 值为 `c` 的点有几个',
        'ans = 0': '`ans` 累计答案',
        'c = core[nums[x]]': '`nums[{x}] = {nums[x]}` 的 core 值：`c` = =={c}==，两个数乘积是平方数 ⇔ core 相同',
        'ans += cnt[c]': '路径上已有 `{cnt[c]}` 个祖先 core 也是 `{c}` → 它们都能和 `{x}` 配对：`ans` → =={ans}==',
        'cnt[c] += 1': '`{x}` 自己入路径：`cnt[{c}]` → {cnt[c]}（对 `{x}` 的后代来说，它是祖先）',
        'if y != fa': lambda S, B, r: (f'`{S.y}` 不是父亲 `{S.fa}` → 是孩子，递归下去' if S.y != S.fa else f'`{S.y}` 是父亲，跳过（无向边别走回头路）'),
        'dfs(y, x)': '进入孩子 `{y}`',
        'cnt[c] -= 1': '`{x}` 的子树处理完，==恢复现场==：`cnt[{c}]` → {cnt[c]}，不影响兄弟子树',
        'dfs(0, -1)': '从根 0 开始，没有父亲，`fa = -1`',
        'return ans': '所有点处理完，答案 =={ans}==',
    },
    cards=dict(
        one_liner='乘积是平方数 ⇔ 去掉平方因子后相等',
        complexity='时间 `O(n)`（不计预处理），空间 `O(n)`',
        problem=['以 0 为根的树，点权 `nums[i]`',
                 '数 `t_i` = 祖先里满足 `nums[i] * nums[祖先]` 为完全平方数的个数',
                 '求 `t_1 + ... + t_{n-1}`；示例 `nums=[2,8,2]` 链 → `3`'],
        quote='设 x′ = core(x)，y′ = core(y)，等式简化为 e_p(x′) = e_p(y′)。这意味着 x′ 和 y′ 完全一样，即 core(x) = core(y)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['x·y 是平方数 ⇔ 每个质数的指数之和为偶数 ⇔ 指数奇偶性相同',
              '去掉完全平方因子得到 ==core==：core 相等就能配对',
              '树上做「好数对」：DFS 时用 `cnt` 记路径上 core 的次数，回溯时撤销'],
        summary=['时间 `O(n)`，空间 `O(n)`（预处理 core 筛在 setup 中执行，不逐行演示）',
                 '祖先不含自己：先 `ans += cnt[c]`，再 `cnt[c] += 1`',
                 '递归返回要 `cnt[c] -= 1` 恢复现场，否则兄弟子树会被算进去',
                 '同类：2862 完全子集的最大元素和（同样按 core 分组）'],
    ),
    skip=['for x, y in edges', 'g[x].append', 'g[y].append'],
    max_steps=110,
)

N = 6
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]]
NUMS = [2, 8, 3, 2, 12, 3]


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
    cur = S['_inner'].get('now') if isinstance(S.get('_inner'), dict) else None
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
    author='yiduobo', technique='先去平方因子 · DFS + 哈希计数',
    tags=['难度分 2235'],
    code='''
class Solution(object):
    def sumOfAncestors(self, n, edges, nums):
        
        power = []
        x = 2
        ma = max(nums)
        while x * x <= ma:
            power.append(x * x)
            x += 1

        for index, v in enumerate(nums):
            for p in power:
                if p > v:
                    break
                while v % p == 0:
                    v //= p
            
            nums[index] = v
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        cnt = {}
        global res
        res = 0
        def dfs(now, fa):
            global res
            res += cnt.get(nums[now], 0)
            cnt[nums[now]] = cnt.get(nums[now], 0) + 1
            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                dfs(nxt, now)
            
            cnt[nums[now]] -= 1
        
        dfs(0, -1)
        return res
''',
    call='Solution().sumOfAncestors(6, [[0,1],[0,2],[1,3],[1,4],[2,5]], [2,8,3,2,12,3])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在处理的 index）', index=False, cell=60, h=110,
             color=lambda S, i, v: ('blue' if '_inner' in S and 'now' not in S and S.get('index') == i else None)),
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', h=125),
        dict(type='map', var='cnt', label='cnt：路径上各值出现次数', fmt=lambda k, v: f'{k}: {v}', h=110, font=28),
    ],
    watch=['x', 'v', 'now', ('p', 'p', 'cyan')],
    captions={
        'power = []': '`power`：4、9、16… 不超过最大值的完全平方数，用来当平方因子候选',
                'while x * x <= ma': lambda S, B, r: (f'`x*x = {S.x*S.x} <= max(nums) = {S.ma}`：继续收集平方数' if S.x * S.x <= S.ma else f'`x*x = {S.x*S.x} > {S.ma}`：收集完毕，`power = {S.power}`'),
        'power.append(x * x)': '`power` 加入 `{x*x}`',
        'for p in power': lambda S, B, r: f'试平方数 `p = {S.p}`',
        'if p > v': lambda S, B, r: (f'`{S.p} > {S.v}`：平方数比 `v` 还大，不可能是因子 → `break`' if S.p > S.v else f'`{S.p} <= {S.v}`：还可能整除'),
        'while v % p == 0': lambda S, B, r: (f'`{S.v} % {S.p} == 0`：`{S.p}` 整除，除掉' if S.v % S.p == 0 else f'`{S.v} % {S.p} != 0`：除不动了'),
        'v //= p': '去掉平方因子 `{p}`：`v` → {v}',
        'nums[index] = v': '`nums[{index}]` 变成 =={v}==：乘积是平方数 ⇔ 去掉平方因子后==相等==',
        'g = [[]': '建邻接表 `g`',
        'cnt = {}': '`cnt`：根到当前节点路径上，各值出现的次数',
        'res = 0': '`res` 累计答案',
        'res += cnt.get': '路径上已有 `{cnt.get(nums[now], 0)}` 个祖先的值也是 `{nums[now]}` → 都能和 `{now}` 配对，加进 `res`',
        'cnt[nums[now]] = cnt.get': '`{now}` 自己入路径：`cnt[{nums[now]}]` → {cnt[nums[now]]}',
        'if nxt == fa': lambda S, B, r: (f'`{S.nxt}` 是父亲，跳过' if S.nxt == S.fa else f'`{S.nxt}` 是孩子，往下走'),
        'dfs(nxt, now)': '进入孩子 `{nxt}`',
        'cnt[nums[now]] -= 1': '`{now}` 的子树算完，==回溯==：`cnt[{nums[now]}]` → {cnt[nums[now]]}，不影响别的分支',
        'dfs(0, -1)': '从根 0 开始',
        'return res': '所有节点处理完，答案 =={ret}==',
    },
    skip=['power = []', 'cnt = {}', 'break', 'continue', 'x = 2', 'ma = max', 'for x, y in edges', 'g[x].append', 'g[y].append', 'x += 1', 'power.append'],
    cards=dict(
        one_liner='先把平方因子去掉，剩下的相同才能配成平方数',
        complexity='时间 `O(n√U + n)`，空间 `O(n)`',
        problem=['以 0 为根的树，点权 `nums[i]`',
                 '`t_i` = 祖先里 `nums[i] * nums[祖先]` 为完全平方数的个数',
                 '求 `t_1 + ... + t_{n-1}`；示例 `nums=[2,8,2]` 链 → `3`'],
        quote='对于新得到的nums[i]，若其能与nums[ancestor]相乘得到完全平方数，这里的nums[ancestor]就必须恰好等于nums[i]。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `x * y = t^2` 里去掉平方因子 `p^2`，结果仍是平方数',
              '所以先把每个数的 4、9、16… 因子全除掉，剩下的值相等才行',
              '一趟 DFS：哈希表 `cnt` 记路径上各值的次数，回溯时减 1'],
        summary=['时间 `O(n√U + n)`，空间 `O(n)`',
                 '原文去平方因子是用平方数列表试除（`power`），灵神是用筛法预处理 core',
                 '`global res` 在嵌套函数里累加答案；回溯要把 `cnt` 减回去',
                 '原文代码无需修改即可在 Python 3 运行（已用 `//=` 整除）'],
    ),
    max_steps=110,
)

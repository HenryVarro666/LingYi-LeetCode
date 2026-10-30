def _vals(S):
    f, g, n = S.get('f'), S.get('g'), len(S['nums'])
    if f is None:
        return None
    out = []
    for k in range(n):
        now, l, r, acc = 0, 0, n - 1, 0
        while l < r:
            acc += g[now]
            m = (l + r) // 2
            if k <= m:
                now, r = now * 2 + 1, m
            else:
                now, l = now * 2 + 2, m + 1
        out.append(f[now] + acc)
    return out


def _nodes(n):
    out = []

    def go(o, l, r, d):
        out.append((o, l, r, d))
        if l < r:
            m = (l + r) // 2
            go(o * 2 + 1, l, m, d + 1)
            go(o * 2 + 2, m + 1, r, d + 1)
    go(0, 0, n - 1, 0)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '线段树：f = 这段区间的和，g = 还没下发给孩子的加法标记（0 号节点是根）', 22, T['muted'], bold=True)
    f, g = S.get('f'), S.get('g')
    if f is None or 'nums' not in S:
        return
    n = len(S['nums'])
    nodes = _nodes(n)
    maxd = max(d for *_, d in nodes)
    inn = S.get('_inner', {})
    cur = inn.get('now') if 'now' in inn else None
    rng = (inn['i'], inn['j']) if 'now' in inn and 'i' in inn and 'j' in inn and 'left' in inn else None
    W = x1 - x0 - 40
    cw = min(170, W / n)
    sx = x0 + 20 + (W - cw * n) / 2
    top, bottom = y0 + 80, y1 - 100
    dy = (bottom - top) / max(1, maxd)
    pos = {}
    for o, l, r, d in sorted(nodes, key=lambda t: -t[3]):
        cx = sx + (l + 0.5) * cw if l == r else (pos[o * 2 + 1][0] + pos[o * 2 + 2][0]) / 2
        pos[o] = (cx, top + d * dy)
    bw, bh = min(150, cw - 10), 66
    for o, l, r, d in nodes:
        if l < r:
            for ch in (o * 2 + 1, o * 2 + 2):
                cv.line([(pos[o][0], pos[o][1] + bh / 2), (pos[ch][0], pos[ch][1] - bh / 2)], T['border'], 2)
    for o, l, r, d in nodes:
        cx, cy = pos[o]
        inside = rng is not None and rng[0] <= l and r <= rng[1]
        fill = (30, 70, 45) if inside else T['panel2']
        cv.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), fill=fill,
                outline=T['yellow'] if o == cur else T['border'], width=4 if o == cur else 2, r=8)
        cv.text((cx, cy - 21), f'[{l},{r}]', 18, T['muted'], anchor='mm', mono=True)
        cv.text((cx, cy + 1), f'f={f[o]}', 24, T['green'], anchor='mm', bold=True)
        cv.text((cx, cy + 22), f'g={g[o]}', 18, T['orange'] if g[o] else T['dim'], anchor='mm', mono=True)
    if rng is not None:
        a, b = sx + rng[0] * cw + 6, sx + (rng[1] + 1) * cw - 6
        cv.line([(a, y1 - 40), (b, y1 - 40)], T['green'], 4)
        cv.text(((a + b) / 2, y1 - 32), f'操作区间 [{rng[0]}, {rng[1]}]', 20, T['green'], anchor='mt', bold=True)


def _hit(S, B, ret):
    L, R, i, j, now = S.left, S.right, S.i, S.j, S.now
    hit = L == i and R == j
    if 'v' in S['_inner']:
        pre = f'`f[{now}]` += {S.v}×长度 → =={S.f[now]}==；'
        if hit:
            return pre + f'`[{L}, {R}]` 正是要改的区间 → 记标记 `g[{now}] += {S.v}`，不往下'
        return pre + f'`[{L}, {R}]` 大于 `[{i}, {j}]` → 往下拆'
    if hit:
        return f'`[{L}, {R}]` 正是要查的区间 → 直接返回 `f[{now}] = {S.f[now]}`'
    return f'`[{L}, {R}]` 大于要查的 `[{i}, {j}]` → 往下拆'


def _formula(S):
    if 'index' not in S or 'pre' not in S:
        return '`v[k]` = 以 index 为右端点、左端点为 k 的子数组不同元素数；`square_s` = 它们的平方和'
    left, right = S['pre'].get(S['nums'][S['index']], -1) + 1, S['index']
    inn = S.get('_inner', {})
    if 'now' in inn and 'i' in inn:
        return f'{"修改" if "v" in inn else "查询"}区间 `[{inn["i"]}, {inn["j"]}]`，当前线段树节点 `[{inn["left"]}, {inn["right"]}]`'
    return f'右端点 `index = {right}`，上次出现在 `pre = {left - 1}`：左端点 `[{left}, {right}]` 的 v 都 +1'


CONFIG = dict(
    num=2916, title='子数组不同元素数目的平方和 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举右端点 + 懒更新线段树',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def sumCounts(self, nums):

        n = len(nums)
        f = [0] * (n * 4)
        g = [0] * (n * 4)
        pre = {}
        mod = 10 ** 9 + 7

        def add(f, g, now, left, right, i, j, v):
            f[now] += v * (j - i + 1)
            f[now] %= mod
            if left == i and right == j:
                g[now] += v
                return

            mid = (left + right) // 2
            if j <= mid:
                add(f, g, now + now + 1, left, mid, i, j, v)
            elif i > mid:
                add(f, g, now + now + 2, mid + 1, right, i, j, v)
            else:
                add(f, g, now + now + 1, left, mid, i, mid, v)
                add(f, g, now + now + 2, mid + 1, right, mid + 1, j, v)

        def get(f, now, left, right, i, j):
            if left == i and right == j:
                return f[now]

            mid = (left + right) // 2

            if g[now] > 0:
                add(f, g, now + now + 1, left, mid, left, mid, g[now])
                add(f, g, now + now + 2, mid + 1, right, mid + 1, right, g[now])
                g[now] = 0

            if j <= mid:
                return get(f, now + now + 1, left, mid, i, j)
            elif i > mid:
                return get(f, now + now + 2, mid + 1, right, i, j)
            else:
                return get(f, now + now + 1, left, mid, i, mid) + get(f, now + now + 2, mid + 1, right, mid + 1, j)

        square_s = 0
        res = 0
        for index, v in enumerate(nums):
            left, right = pre.get(v, -1) + 1, index

            s = get(f, 0, 0, n - 1, left, right)
            add(f, g, 0, 0, n - 1, left, right, 1)
            square_s += s * 2 + right - left + 1
            square_s %= mod
            res += square_s
            res %= mod

            pre[v] = index
        
        return res
''',
    call='Solution().sumCounts([1,2,1])',
    expect=15,
    skip=['n = len(nums)', 'f = [0]', 'g = [0]', 'pre = {}', 'mod = 10', 'f[now] %= mod', 'square_s %= mod', 'res %= mod', 'pre[v] = index',
          'mid = (left + right)', 'g[now] += v', 15, 'square_s = 0', 'res = 0', 'elif i > mid', 'g[now] = 0', 'f[now] += v', 'return f[now]', 'return get(f, now + now + 1, left, mid, i, mid)', 'add(f, g, now + now + 1, left, mid, left, mid, g[now])', 'add(f, g, now + now + 2, mid + 1, right, mid + 1, right, g[now])', 'add(f, g, now + now + 1, left, mid, i, mid, v)', 'add(f, g, now + now + 2, mid + 1, right, mid + 1, j, v)',
          'left, mid, i, j, v)', 'mid + 1, right, i, j, v)', 'return get(f, now + now + 1, left, mid, i, j)', 'return get(f, now + now + 2, mid + 1, right, i, j)'],
    views=[
        dict(type='text', fn=_formula, size=24, h=56),
        dict(type='array', var='nums', label='nums（蓝 = 当前 index）', h=165, cell=80,
             color=lambda S, k, v: 'blue' if S.get('index') == k else None),
        dict(type='array', var=_vals, label='v[k]：左端点为 k 的子数组的不同元素数（框 = 本轮 +1 的区间）', h=180, cell=80,
             window=('pre.get(nums[index], -1) + 1', 'index'), index=True),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('index', 'index', 'blue'), ('s(区间和)', 's', 'cyan'), ('square_s', 'square_s', 'yellow'), ('res', 'res', 'green')],
    captions={
        'left, right = pre.get': '`{v}` 上次在 `{left - 1}`（没有记 -1）→ 左端点 `[{left}, {right}]` 的子数组多出新数，v 都 +1',
        's = get(f, 0': '先用线段树查出 `v[{left}..{right}]` 的和 `s`（加一之前）',
        'add(f, g, 0, 0, n - 1, left': '再把 `v[{left}..{right}]` 都 +1（懒更新）',
        'square_s += s * 2': '每个 v 加一，平方多 `2v+1`：`square_s += 2×{s} + {right - left + 1}` → =={square_s}==',
        'res += square_s': '右端点 `{index}` 的平方和 `{square_s}` 累进 `res = {res}`',
        'if left == i and right == j': _hit,
        'if j <= mid': lambda S, B, r: (f'`j = {S.j} <= mid = {S.mid}`：要处理的区间全在左半边' if S.j <= S.mid else (f'`j = {S.j} > mid = {S.mid}` 且 `i = {S.i} > mid`：全在右半边' if S.i > S.mid else f'`i = {S.i} <= mid = {S.mid} < j = {S.j}`：横跨中点，左右各处理一段')),
        'if g[now] > 0': lambda S, B, r: (f'`g[{S.now}] = {S.g[S.now]}` > 0：先下发给两个孩子，`g[{S.now}]` 清零' if S.g[S.now] > 0 else f'`g[{S.now}] = 0`：没有欠账，直接往下查'),
        'return res': '`res = {res}`：所有右端点的平方和累加完',
    },
    cards=dict(
        one_liner='枚举右端点，给一段左端点的 v 区间加一，平方和差值 = 2×区间和 + 长度',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 的每个子数组有「不同元素数」，求所有子数组不同元素数的==平方和==，对 `10^9+7` 取模','`n` 到 `10^5`，只能 `O(n log n)`','示例：`[1,2,1]` → `15`'],
        quote='square_s[index] - square_s[index - 1] = 2 * (v[pre + 1] + v[pre + 2] + ... + v[index]) + index - pre + 1',
        quote_src='—— yiduobo 题解原文',
        idea=['`v[k]` = 以当前右端点结尾、从 `k` 开始的子数组的不同元素数；新数 `nums[index]` 上次在 `pre`','`v[0..pre]` 不变，`v[pre+1..index]` 全部 +1（区间加）','两轮平方和作差，平方项全约掉，只剩 `2×区间和 + 长度` → 区间求和 + 区间加 = 懒更新线段树'],
        summary=['时间 `O(n log n)`，空间 `O(n)`','`pre` 里没有的数用 `-1`，所以左端点是 `pre + 1 = 0`','`add` 把区间和直接更新，`g` 只记标记；`get` 往下走之前才下发','原文为 Python 2 写法，其中 `mid = (left + right) / 2` 已改为 `//`','对比灵神：灵神把「查询 + 加一」合成一个函数且下标从 1 开始；yiduobo 拆成 `get` 和 `add`，下标从 0 开始'],
    ),
)

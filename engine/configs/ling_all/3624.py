def _fen_pic(cv, T, box, tree, old, vals, cur, title, vlabel='值'):
    """树状数组：上排 = 位置 1..m 的值，下面每根条 = tree[i] 管的关键区间 [i-lowbit+1, i]（按 lowbit 分层）；
    黄色 = 当前正在访问的 tree[i]，蓝色 = 它覆盖的位置，黄边 = 这一步刚改过"""
    x0, y0, x1, y1 = box
    m = len(tree) - 1
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    if m < 1:
        return
    cell = min(120, (x1 - x0 - 60) / m)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * m) / 2
    ty = y0 + 34
    nlev = max(i & -i for i in range(1, m + 1)).bit_length()
    rowh = min(60, (y1 - (ty + 76)) / nlev)
    lo = hi = None
    if cur is not None and 1 <= cur <= m:
        hi = cur
        lo = cur - (cur & -cur) + 1
    for i in range(1, m + 1):
        X = sx + (i - 1) * cell
        covered = lo is not None and lo <= i <= hi
        cv.rect((X + 2, ty, X + cell - 2, ty + 42), fill=T['blue'] if covered else T['panel2'], r=6, alpha=200 if covered else 255)
        v = vals[i - 1] if i - 1 < len(vals) else ''
        cv.text((X + cell / 2, ty + 21), v, 24, T['bg'] if covered else T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ty + 48), i, 18, T['dim'], anchor='mt', mono=True)
    by = ty + 72
    for i in range(1, m + 1):
        lb = i & -i
        lv = lb.bit_length() - 1
        xa, xb = sx + (i - lb) * cell + 3, sx + i * cell - 3
        ya = by + lv * rowh
        changed = old is not None and len(old) == len(tree) and old[i] != tree[i]
        if i == cur:
            fill, tc = T['yellow'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((xa, ya, xb, ya + rowh - 5), fill=fill, outline=T['yellow'] if changed else T['border'], width=3 if changed else 1, r=6)
        lab = f't{i}={tree[i]}' if cell * lb > 150 else f'{tree[i]}'
        if lb > 1:
            lab = f't{i}={tree[i]}  [{i - lb + 1},{i}]' if cell * lb > 260 else f't{i}={tree[i]}'
        cv.text(((xa + xb) / 2, ya + (rowh - 5) / 2), lab, 20, tc, anchor='mm', bold=True)


def _lb_text(i):
    return f'`{i}` = `{i:b}`（二进制），lowbit = `{i & -i}`'
def _depth(x):
    r = 0
    while x > 1:
        r += 1
        x = x.bit_count()
    return r


def _rows(S):
    f = S.get('f')
    if not f:
        return None
    try:
        return [t.tree for t in f]
    except Exception:
        return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    rows = _rows(S)
    nums = S.get('nums')
    if rows is None or nums is None:
        cv.text((x0 + 18, y0), '（还没建树）', 24, T['dim'])
        return
    old = _rows(B)
    n = len(nums)
    cell = min(110, (x1 - x0 - 230) / n)
    sx = x0 + 190
    cv.text((x0 + 18, y0), 'nums 的 popcount-depth → 放进对应的树 f[k]（黄 = 当前，蓝 = 这次改过）', 22, T['muted'], bold=True)
    ty = y0 + 40
    cv.text((x0 + 10, ty + 28), 'nums', 22, T['muted'], anchor='lm', bold=True)
    cv.text((x0 + 10, ty + 66), '深度', 22, T['muted'], anchor='lm', bold=True)
    for j, v in enumerate(nums):
        X = sx + j * cell
        cv.rect((X + 3, ty, X + cell - 3, ty + 50), fill=T['panel2'], r=6)
        cv.text((X + cell / 2, ty + 25), v, 26, T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ty + 66), _depth(v), 24, T['cyan'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ty + 94), j + 1, 18, T['dim'], anchor='mm', mono=True)
    ry = ty + 112
    rh = min(58, (y1 - ry) / len(rows))
    cur = S.get('self.tree')
    i = S.get('i')
    for k, t in enumerate(rows):
        Y = ry + k * rh
        mine = cur is not None and cur is t
        cv.text((x0 + 10, Y + (rh - 6) / 2), f'f[{k}]', 24, T['yellow'] if mine else T['muted'], anchor='lm', bold=True, mono=True)
        for p in range(1, len(t)):
            X = sx + (p - 1) * cell
            changed = old is not None and k < len(old) and len(old[k]) == len(t) and old[k][p] != t[p]
            hot = mine and i == p
            cv.rect((X + 3, Y, X + cell - 3, Y + rh - 6), fill=T['yellow'] if hot else T['panel2'],
                    outline=T['blue'] if changed else T['border'], width=3 if changed else 1, r=5)
            cv.text((X + cell / 2, Y + (rh - 6) / 2), t[p], 22, T['bg'] if hot else (T['text'] if t[p] else T['dim']), anchor='mm', bold=True)


def _info(S):
    q = S.get('q')
    if q is None:
        return ''
    if q[0] == 1:
        return f"查询 `[1,{q[1]},{q[2]},{q[3]}]`：下标 {q[1]}~{q[2]} 里深度 = {q[3]} 的有几个？"
    return f"查询 `[2,{q[1]},{q[2]}]`：把 `nums[{q[1]}]` 改成 {q[2]}（深度 {_depth(q[2])}）"


CONFIG = dict(
    num=3624, title='位计数深度为 K 的整数数目 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='6 棵树状数组（按深度分组）',
    tags=['常用数据结构', '树状数组和线段树', '难度分 2086'],
    code='''
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.tree[i]
            i &= i - 1
        return res

    # 计算区间和 a[l] + ... + a[r]
    # 1 <= l <= r <= n
    # 时间复杂度 O(log n)
    def query(self, l: int, r: int) -> int:
        return self.pre(r) - self.pre(l - 1)

pop_depth_list = [0] * 51
for i in range(2, len(pop_depth_list)):
    pop_depth_list[i] = pop_depth_list[i.bit_count()] + 1

def pop_depth(x: int) -> int:
    if x == 1:
        return 0
    return pop_depth_list[x.bit_count()] + 1

class Solution:
    def popcountDepth(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        f = [FenwickTree(n) for _ in range(6)]

        def update(i: int, delta: int) -> None:
            d = pop_depth(nums[i])
            f[d].update(i + 1, delta)

        for i in range(n):
            update(i, 1)  # 添加

        ans = []
        for q in queries:
            if q[0] == 1:
                ans.append(f[q[3]].query(q[1] + 1, q[2] + 1))
            else:
                i = q[1]
                update(i, -1)  # 撤销旧的
                nums[i] = q[2]
                update(i, 1)  # 添加新的
        return ans
''',
    call='Solution().popcountDepth([2, 4], [[1, 0, 1, 1], [2, 1, 1], [1, 0, 1, 0]])',
    expect=[2, 1],
    max_steps=64,
    skip=['self.tree = [0] * (n + 1)', 'n = len(nums)', 'res = 0', 'ans = []', 'while i > 0', 'if x == 1', 'f = [FenwickTree(n)', 'if q[0] == 1', 'i = q[1]'],
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='custom', draw=_draw, h=520),
        dict(type='array', var='ans', label='ans', cell=64, h=110),
    ],
    watch=[('i', 'i', 'blue'), ('d', 'd', 'yellow'), ('x', 'x', 'pink'), ('res', 'res', 'green')],
    captions={
        'for i in range(n)': lambda S, B, r: ('全部放完了' if ('i' in B and B['i'] == S.i) else
                                              (f'深度只有 `0 ~ 5` → 先开好 ==6 棵==树状数组 `f[0..5]`，再把 `nums[{S.i}]` 放进它深度对应的那棵' if S.i == 0
                                               else f'接着放 `nums[{S.i}]`')),
        'd = pop_depth(nums[i])': '`nums[{i}]` = {nums[i]} 的 popcount-depth = =={d}==',
        'f[d].update(i + 1, delta)': lambda S, B, r: f'`f[{S.d}]` 的位置 `{S.i + 1}` 加 `{S.delta}`（数组下标 +1）：深度 {S.d} 的树记上这个位置',
        'if x == 1': '`x = {x}`：深度 0 的只有 1',
        'return 0': '`1` 的深度是 0',
        'return pop_depth_list[x.bit_count()] + 1': '`{x}` 的二进制有 `{x.bit_count()}` 个 1，==一步就变成 ≤ 50 的数==，查表再 +1 → 深度 =={ret}==',
        'while i < len(self.tree)': lambda S, B, r: (f'`i = {S.i}` < {len(S["self.tree"])}：`tree[{S.i}]` 含这个位置 → 要改' if S.i < len(S['self.tree']) else f'`i = {S.i}` 越界：改完了'),
        'self.tree[i] += val': '`tree[{i}]` 管 [{i - (i & -i) + 1}, {i}]，加 `{val}` → =={self.tree[i]}==',
        'i += i & -i': '`i += lowbit` → `{i}`',
        'res = 0': '`res` 累加前缀 `[1, {i}]`',
        'while i > 0': lambda S, B, r: (f'`i = {S.i}` > 0：前缀还没拆完' if S.i > 0 else '`i = 0`：前缀拆完了'),
        'res += self.tree[i]': '`tree[{i}]` 管 [{i - (i & -i) + 1}, {i}]，整段加进 `res` → =={res}==',
        'i &= i - 1': '去掉最低位的 1：`{B.i}` → `{i}`',
        'return res': '前缀和 `{ret}`',
        'return self.pre(r) - self.pre(l - 1)': lambda S, B, r: (f'区间和 = 前缀 [1,{S.r}] − 前缀 [1,{S.l - 1}]' if r is None else f'区间 [{S.l},{S.r}] 里深度对应的个数 = ==`{r}`=='),
        'update(i, 1)': '`update(i, 1)`：把 `nums[{i}]` 按它的深度放进对应的树',
        'for q in queries': '逐个处理查询：`q = {q}`',
        'if q[0] == 1': lambda S, B, r: ('`q[0] == 1`：这是==计算==类型' if S.q[0] == 1 else '`q[0] == 2`：这是==修改==类型'),
        'ans.append(f[q[3]].query': '深度 `{q[3]}` 的个数：问 `f[{q[3]}]` 在区间 [{q[1] + 1}, {q[2] + 1}] 的和（下标 +1）',
        'i = q[1]': '要修改的下标 `i = {i}`',
        'update(i, -1)': '`update(i, -1)`：先==撤销旧的==，从 `nums[{i}]` = {nums[i]} 的旧深度那棵树里减 1',
        'nums[i] = q[2]': '`nums[{i}]` 改成 `{q[2]}`',
        'return ans': '所有计算查询的答案：==`{ret}`==',
    },
    cards=dict(
        one_liner='k 最多 5：按深度开 6 棵树状数组，区间计数变成前缀和相减',
        complexity='时间 `O((n + q) log n)`，空间 `O(n)`',
        problem=['`popcount-depth`：反复取二进制 1 的个数，直到变成 1 的次数；如 `7 → 3 → 2 → 1`，深度 3',
                 '查询 `[1,l,r,k]`：区间里深度恰为 `k` 的个数；`[2,idx,val]`：修改一个数',
                 '示例：`nums=[2,4]`，`[[1,0,1,1],[2,1,1],[1,0,1,0]]` → `[2,1]`'],
        quote='由于 0 ≤ k ≤ 5，用 6 棵树状数组维护。比如 k=3 的树状数组维护的是一个 0-1 数组 a 的前缀和，其中 a[i] = 1 表示 nums[i] 的 popcount-depth 值等于 3。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「区间里深度等于 k 的个数」= 0-1 数组的区间和 → 树状数组',
              '深度只有几种：每种深度一棵树，`f[d]` 里位置 `i` 为 1 表示 `nums[i]` 深度是 `d`',
              '修改 = ==撤销旧的 + 添加新的==：旧深度那棵树减 1，新深度那棵树加 1',
              '优化：`10^15` 的二进制只有 50 位，一步之后 ≤ 50 → 预处理 `≤ 50` 的深度表，查表代替循环'],
        summary=['时间 `O((n + q) log n)`，空间 `O(n)`（6 棵树）',
                 '易错：`nums[i]` 要在撤销之后才能改；撤销用旧值的深度，添加用新值的深度',
                 '`1` 的深度是 0，要单独判断；树状数组下标 +1',
                 '优化前写法：`pop_depth` 每次用 `while` 迭代计算，不写记忆化；结果相同，只是常数更大'],
    ),
)

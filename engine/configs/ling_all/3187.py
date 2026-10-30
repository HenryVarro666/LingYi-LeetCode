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
def _peak(a, i):
    return 1 if 0 < i < len(a) - 1 and a[i - 1] < a[i] > a[i + 1] else 0


def _fw(S):
    o = S.get('self')
    t = getattr(o, 'f', None)
    if t is None:
        t = getattr(S.get('f'), 'f', None)
    return t


def _draw(cv, S, B, box, T):
    t = _fw(S)
    nums = S.get('nums')
    if t is None or nums is None:
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    m = len(t) - 1
    vals = [_peak(nums, i) for i in range(1, m + 1)]
    cur = S.get('i') if S.get('self') is not None else None
    if cur is not None and cur < 1:
        cur = None
    _fen_pic(cv, T, box, t, _fw(B), vals, cur, '上排 = 位置 i 现在是不是峰值（1/0）；条 = 树状数组 f[i]（黄 = 当前）')


def _info(S):
    op = S.get('op')
    if op is None:
        return ''
    i, val = S.get('i'), S.get('val')
    qs = [q for q in (S.get('queries') or []) if q[0] == op]
    if qs:
        k = min(len(S.get('ans') or []), len(qs) - 1) if op == 1 else 0
        i, val = qs[k][1], qs[k][2]
    if op == 1:
        return f"操作 1：子数组 `[{i}, {val}]` 的首尾不算峰值 → 数位置 `{i + 1} ~ {val - 1}` 的峰值"
    return f"操作 2：`nums[{i}]` 改成 {val}，只影响位置 `{i - 1}, {i}, {i + 1}` 的峰值状态"


CONFIG = dict(
    num=3187, title='数组中的峰值', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='峰值记成 0/1，树状数组维护',
    tags=['常用数据结构', '树状数组和线段树', '难度分 2154'],
    code='''
class Fenwick:
    __slots__ = 'f'

    def __init__(self, n: int):
        self.f = [0] * n

    def update(self, i: int, val: int) -> None:
        while i < len(self.f):
            self.f[i] += val
            i += i & -i

    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.f[i]
            i &= i - 1
        return res

    def query(self, l: int, r: int) -> int:
        if r < l:
            return 0
        return self.pre(r) - self.pre(l - 1)

class Solution:
    def countOfPeaks(self, nums, queries):
        n = len(nums)
        f = Fenwick(n - 1)
        def update(i: int, val: int) -> None:
            if nums[i - 1] < nums[i] and nums[i] > nums[i + 1]:
                f.update(i, val)
        for i in range(1, n - 1):
            update(i, 1)

        ans = []
        for op, i, val in queries:
            if op == 1:
                ans.append(f.query(i + 1, val - 1))
                continue
            for j in range(max(i - 1, 1), min(i + 2, n - 1)):
                update(j, -1)
            nums[i] = val
            for j in range(max(i - 1, 1), min(i + 2, n - 1)):
                update(j, 1)
        return ans
''',
    call='Solution().countOfPeaks([1, 3, 2, 1], [[1, 0, 3], [2, 2, 4], [1, 0, 2]])',
    expect=[1, 0],
    max_steps=66,
    skip=['n = len(nums)', 'ans = []', 'continue', 'if r < l', 'res = 0', 'while i > 0'],
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='nums', label='nums（绿 = 当前峰值）', h=150,
             color=lambda S, i, v: 'green' if _peak(S['nums'], i) else None),
        dict(type='array', var='ans', label='ans', cell=64, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('val', 'val', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = Fenwick(n - 1)': '首尾不可能是峰值，只需位置 `1 ~ n-2`：树状数组记录「该位置是不是峰值」（是 = 1）',
        'self.f = [0] * n': '`f` 长度 `{len(self.f)}`，可用下标 `1 ~ {len(self.f) - 1}`（0 号不用）',
        'for i in range(1, n - 1)': lambda S, B, r: ('每个位置都处理过了，树建好' if ('i' in B and B['i'] == S.i) else
                                                       (f'先建树：枚举 `i = 1 ~ n-2`，是峰值就加进树（`i = {S.i}`）' if S.i == 1 else f'下一个位置 `i = {S.i}`')),
        'if nums[i - 1] < nums[i] and nums[i] > nums[i + 1]': lambda S, B, r: (
            f'`nums[{S.i - 1}] = {S.nums[S.i - 1]}`，`nums[{S.i}] = {S.nums[S.i]}`，`nums[{S.i + 1}] = {S.nums[S.i + 1]}`：'
            + ('比两边都大 → ==峰值==' if S.nums[S.i - 1] < S.nums[S.i] > S.nums[S.i + 1] else '不是峰值，不用动树')),
        'f.update(i, val)': '位置 `{i}` 的峰值 ' + '`{val}`：树状数组里这个位置' + '{"加 1" if val > 0 else "减 1"}',
        'update(i, 1)': '`update({i}, 1)`：如果位置 {i} 是峰值，就在树里加 1',
        'for op, i, val in queries': '处理操作 `[{op}, {i}, {val}]`',
        'if op == 1': lambda S, B, r: ('`op == 1`：==查询==峰值个数' if S.op == 1 else '`op == 2`：==修改=='),
        'ans.append(f.query(i + 1, val - 1))': '子数组首尾不算峰值 → 数位置 `[{i + 1}, {val - 1}]` 的峰值个数（区间和）',
        'return self.pre(r) - self.pre(l - 1)': lambda S, B, r: (f'区间和 = 前缀 [1,{S.r}] − 前缀 [1,{S.l - 1}]' if r is None else f'区间 [{S.l}, {S.r}] 里的峰值数 = =={r}=='),
        'while i < len(self.f)': lambda S, B, r: (f'`i = {S.i}` < {len(S["self"].f)}：`f[{S.i}]` 含这个位置 → 要改' if S.i < len(S['self'].f) else f'`i = {S.i}` 越界：改完了'),
        'self.f[i] += val': '`f[{i}]` 管 [{i - (i & -i) + 1}, {i}]，加 `{val}` → =={self.f[i]}==',
        'i += i & -i': '`i += lowbit` → `{i}`',
        'res += self.f[i]': '`f[{i}]` 管 [{i - (i & -i) + 1}, {i}]，加进 `res` → =={res}==',
        'i &= i - 1': '去掉最低位的 1：`{B.i}` → `{i}`',
        'return res': '前缀和 `{ret}`',
        'for j in range(max(i - 1, 1)': lambda S, B, r: ('这几个位置都处理完了' if ('j' in B and B['j'] == S.j) else
                                                        (f'`nums[{S.i}]` 变了，只影响位置 `{max(S.i - 1, 1)} ~ {min(S.i + 1, len(S.nums) - 2)}` 的峰值状态（不超出 `1 ~ n-2`），从 `j = {S.j}` 开始'
                                                         if S.j == max(S.i - 1, 1) else f'下一个位置 `j = {S.j}`')),
        'update(j, -1)': '先把位置 `{j}` 的旧峰值==去掉==（修改前判断）',
        'nums[i] = val': '修改 `nums[{i}] = {val}`',
        'update(j, 1)': '再按新数组把位置 `{j}` 的峰值==加回去==',
        'return ans': '所有查询 1 的答案：==`{ret}`==',
    },
    cards=dict(
        one_liner='峰值记成 1、其余记成 0：区间峰值数 = 区间和，改一个数只影响三个位置',
        complexity='时间 `O((n + q) log n)`，空间 `O(n)`',
        problem=['峰值：严格大于左右邻居的元素；==子数组的首尾不算峰值==',
                 '操作 1：数 `nums[l..r]` 的峰值；操作 2：把 `nums[i]` 改成 `val`',
                 '示例：`nums=[4,1,4,2,1,5]`，`[[2,2,4],[1,0,2],[1,0,4]]` → `[0,1]`；本视频用 `[1,3,2,1]`'],
        quote='如果 1 ≤ i ≤ n-2 且 a[i-1] < a[i] > a[i+1]，那么把 a[i] 视作 1，否则视作 0。如此转换后，操作 1 相当于计算从 l+1 到 r-1 的子数组的元素和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['峰值转成 0/1 数组，操作 1 = 区间 `[l+1, r-1]` 的和 → 树状数组',
              '注意是「子数组」的首尾不算，所以区间要缩成 `[l+1, r-1]`',
              '修改 `a[i]` 只会改变 `i-1, i, i+1` 三个位置的峰值状态',
              '做法：先把这几个位置的旧峰值去掉，改值，再把新峰值加回来'],
        summary=['时间 `O((n + q) log n)`，空间 `O(n)`；初始化也可 `O(n)`',
                 '易错：区间是 `[l+1, r-1]`；`r < l` 时返回 0（子数组太短）',
                 '易错：先 `-1` 去掉旧峰值再改值，顺序不能反',
                 '`j` 的范围要卡在 `1 ~ n-2`，首尾永远不是峰值'],
    ),
)

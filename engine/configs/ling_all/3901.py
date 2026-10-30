def _fit(cv, s, size, maxw, bold=True):
    while size > 13 and cv.tlen(s, size, bold) > maxw:
        size -= 1
    return size


def _seg(cv, T, box, n, lab, kids, cur=(), chg=(), nums=None, num_hl=(), title='', root=1, bound=None):
    """线段树示意图：上排 = 数组（可选），下面每个节点 = 一段区间；黄色 = 当前节点，黄边 = 这一步刚改过，虚框 = 还没算出"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0), title, 22, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 60) / max(n, 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 36
    if nums is not None:
        for i in range(n):
            X = sx + i * cell
            hl = i in num_hl
            cv.rect((X + 2, top, X + cell - 2, top + 40), fill=T['yellow'] if hl else T['panel2'], r=6)
            cv.text((X + cell / 2, top + 20), nums[i] if i < len(nums) else '', 24, T['bg'] if hl else T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, top + 44), i, 16, T['dim'], anchor='mt', mono=True)
        top += 72
    nodes = {}
    def walk(nd, l, r, d):
        nodes[nd] = (l, r, d)
        if l < r:
            m = (l + r) // 2
            a, b = kids(nd)
            walk(a, l, m, d + 1)
            walk(b, m + 1, r, d + 1)
    walk(root, 0, n - 1, 0)
    depth = max(d for _, _, d in nodes.values()) + 1
    rowh = min(112, (y1 - top - 6) / depth)
    bh = min(54, rowh - 30)
    pos = {}
    for nd, (l, r, d) in nodes.items():
        cx = sx + (l + r + 1) / 2 * cell
        pos[nd] = (cx, top + d * rowh)
    for nd, (l, r, d) in nodes.items():
        if l < r:
            for c in kids(nd):
                cv.line([(pos[nd][0], pos[nd][1] + bh + 20), (pos[c][0], pos[c][1])], T['border'], 2)
    for nd, (l, r, d) in nodes.items():
        cx, cy = pos[nd]
        w = min(max(cell * (r - l + 1) - 8, 40), 190 if r > l else 130)
        s = lab(nd)
        is_cur = nd in cur
        changed = nd in chg
        if s is None:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['dim'], width=1, r=8)
            s = ''
        else:
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), fill=T['yellow'] if is_cur else T['panel2'],
                    outline=T['yellow'] if changed else T['border'], width=4 if changed else 1, r=8)
        if is_cur and s == '':
            cv.rect((cx - w / 2, cy, cx + w / 2, cy + bh), outline=T['yellow'], width=4, r=8)
        sz = _fit(cv, s, 24, w - 10)
        cv.text((cx, cy + bh / 2), s, sz, T['bg'] if is_cur and s else T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + bh + 3), f'#{nd} [{l},{r}]', 15, T['dim'], anchor='mt', mono=True)



def _tr(S):
    o = S.get('self')
    if o is not None and hasattr(o, '_tree'):
        return o
    return S.get('t')


def _nums(S):
    for k in ('nums', 'a', 'arr'):
        v = S.get(k)
        if isinstance(v, list):
            return v
    return None


def _draw(cv, S, B, box, T):
    t = _tr(S)
    if t is None or not hasattr(t, '_n') or not hasattr(t, '_tree'):
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    tb = _tr(B)
    old = getattr(tb, '_tree', None) if tb is not None else None
    tree = t._tree
    cur = S['_inner'].get('node')
    chg = set()
    if old is not None and len(old) == len(tree):
        chg = {i for i in range(len(tree)) if old[i] != tree[i]}
    _seg(cv, T, box, t._n, lambda nd: str(tree[nd]) if nd < len(tree) else None, lambda nd: (nd * 2, nd * 2 + 1),
         cur=(cur,) if cur else (), chg=chg, nums=_nums(S) if t._n == len(_nums(S) or []) else None,
         title=f'线段树：每个节点 = 区间内「p 的倍数」的 GCD（0 = 没有倍数，p = {t._target_gcd}）')


def _info(S):
    if 'cnt_p' in S and 't' in S:
        t = S['t']
        return (f"`p = {S['p']}`：p 的倍数有 `{S['cnt_p']}` 个（`n = {S['n']}`），线段树根 = 它们的 GCD = =={t._tree[1]}=="
                + ('，等于 `p`' if t._tree[1] == S['p'] else ''))
    return ''


def _chk(S, B, ret):
    g, p, n, c = S.t.query_all(), S.p, S.n, S.cnt_p
    if g != p:
        return f'倍数的 GCD = `{g}` ≠ `p = {p}`：选更少的数 GCD 只会更大 → ==没有好子序列=='
    if c < n:
        return f'GCD = `p`，且倍数只有 `{c}` < `n = {n}` 个：全选这些就是长度 < n 的好子序列 → ==计数=='
    if n > 6:
        return f'GCD = `p`，但 `n = {n}` > 6：一定能删掉一个数 GCD 仍为 p → ==计数=='
    return f'GCD = `p`，每个数都是倍数且 `n = {n}` ≤ 6：必须删一个，调用 `check` 枚举删哪个'


CONFIG = dict(
    num=3901, title='好子序列查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='线段树维护倍数的 GCD + 特判 n ≤ 6',
    tags=['灵神题单·常用数据结构', '灵神题单·数学算法', '难度分 2545'],
    code='''
# 模板来源 https://leetcode.cn/circle/discuss/mOr1u6/
# 线段树有两个下标，一个是线段树节点的下标，另一个是线段树维护的区间的下标
# 节点的下标：从 1 开始，如果你想改成从 0 开始，需要把左右儿子下标分别改成 node*2+1 和 node*2+2
# 区间的下标：从 0 开始
class SegmentTree:
    def __init__(self, arr, target_gcd: int, default=0):
        # 线段树维护一个长为 n 的数组（下标从 0 到 n-1）
        # arr 可以是 list 或者 int
        # 如果 arr 是 int，视作数组大小，默认值为 default
        if isinstance(arr, int):
            arr = [default] * arr
        n = len(arr)
        self._target_gcd = target_gcd
        self._n = n
        self._tree = [0] * (2 << (n - 1).bit_length())
        self._build(arr, 1, 0, n - 1)

    # 合并左右儿子的 val 到当前节点的 val
    def _maintain(self, node: int) -> None:
        self._tree[node] = gcd(self._tree[node * 2], self._tree[node * 2 + 1])

    # 用 a 初始化线段树
    # 时间复杂度 O(n)
    def _build(self, a: List[int], node: int, l: int, r: int) -> None:
        if l == r:  # 叶子
            # 0 和任何数 g 的 GCD 都是 g，所以设置为 0 不影响所有数的 GCD
            self._tree[node] = a[l] if a[l] % self._target_gcd == 0 else 0  # 初始化叶节点的值
            return
        m = (l + r) // 2
        self._build(a, node * 2, l, m)  # 初始化左子树
        self._build(a, node * 2 + 1, m + 1, r)  # 初始化右子树
        self._maintain(node)

    def _update(self, node: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:  # 叶子（到达目标）
            # 0 和任何数 g 的 GCD 都是 g，所以设置为 0 不影响所有数的 GCD
            self._tree[node] = val if val % self._target_gcd == 0 else 0
            return
        m = (l + r) // 2
        if i <= m:  # i 在左子树
            self._update(node * 2, l, m, i, val)
        else:  # i 在右子树
            self._update(node * 2 + 1, m + 1, r, i, val)
        self._maintain(node)

    def _query(self, node: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql > qr:
            return 0
        if ql <= l and r <= qr:  # 当前子树完全在 [ql, qr] 内
            return self._tree[node]
        m = (l + r) // 2
        if qr <= m:  # [ql, qr] 在左子树
            return self._query(node * 2, l, m, ql, qr)
        if ql > m:  # [ql, qr] 在右子树
            return self._query(node * 2 + 1, m + 1, r, ql, qr)
        l_res = self._query(node * 2, l, m, ql, qr)
        r_res = self._query(node * 2 + 1, m + 1, r, ql, qr)
        return gcd(l_res, r_res)

    # 更新 a[i]
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        self._update(1, 0, self._n - 1, i, val)

    # 返回用 gcd 合并所有 a[i] 的计算结果，其中 i 在闭区间 [ql, qr] 中
    # 时间复杂度 O(log n)
    def query(self, ql: int, qr: int) -> int:
        return self._query(1, 0, self._n - 1, ql, qr)

    def query_all(self) -> int:
        return self._tree[1]

    def check(self, n: int) -> bool:
        return any(gcd(self.query(0, i - 1), self.query(i + 1, n - 1)) == self._target_gcd for i in range(n))

class Solution:
    def countGoodSubseq(self, nums: List[int], p: int, queries: List[List[int]]) -> int:
        n = len(nums)
        cnt_p = sum(x % p == 0 for x in nums)

        t = SegmentTree(nums, p)
        ans = 0

        for i, x in queries:
            if nums[i] % p == 0:
                cnt_p -= 1
            if x % p == 0:
                cnt_p += 1
            nums[i] = x
            t.update(i, x)

            if t.query_all() == p and (cnt_p < n or n > 6 or t.check(n)):
                ans += 1

        return ans
''',
    call='Solution().countGoodSubseq([4, 5, 6], 2, [[1, 8], [1, 5], [2, 3]])',
    expect=2,
    max_steps=110,
    skip=[48, 'self._maintain(node)', 'if ql <= l and r <= qr', 'if qr <= m', 'if ql > m', 'return self._query(node * 2', 'return self._query(1,', 'self._update(1, 0', 28, 38, 'if l == r', 'if ql > qr', 'self._target_gcd = target_gcd', 'self._n = n', 'self._tree = [0]', 'self._build(arr', 'return self._tree[1]',
          'n = len(nums)', 'if isinstance(arr, int)', 'arr = [default]', 'm = (l + r) // 2', 'self._build(a, node * 2, l, m)',
          'self._build(a, node * 2 + 1, m + 1, r)', 'self._update(node * 2, l, m, i, val)', 'self._update(node * 2 + 1, m + 1, r, i, val)'],
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=120),
    ],
    watch=['p', 'cnt_p', 'n', ('ans', 'ans', 'green')],
    captions={
        'cnt_p = sum': '先数一数：`nums` 里有 `{cnt_p}` 个数是 `p = {p}` 的倍数（`n = {n}`）',
        't = SegmentTree(nums, p)': '建线段树：叶子只放 ==p 的倍数==，其余放 `0`（0 和任何数的 GCD 都是它本身，不影响结果）',
        'ans = 0': '`ans` 统计「有好子序列」的查询次数',
        'self._tree[node] = a[l] if': lambda S, B, r: f'叶子 `a[{S.l}] = {S.a[S.l]}`' + (f' 是 `{S.self._target_gcd}` 的倍数 → 存它自己' if S.a[S.l] % S.self._target_gcd == 0 else f' 不是 `{S.self._target_gcd}` 的倍数 → 存 `0`'),
        'self._tree[node] = gcd(': '合并：左儿子 `{self._tree[node*2]}` 和右儿子 `{self._tree[node*2+1]}` 的 GCD → 节点 `{node}` = =={self._tree[node]}==',
        'self._tree[node] = val if': lambda S, B, r: f'叶子改成 `{S.val}`' + (f'：是 `p` 的倍数 → 存它自己' if S.val % S.self._target_gcd == 0 else f'：不是 `p` 的倍数 → 存 `0`'),
        'if i <= m': lambda S, B, r: f'`i = {S.i}` ' + ('≤' if S.i <= S.m else '>') + f' `m = {S.m}`：被改的位置在' + ('左' if S.i <= S.m else '右') + '子树，只往那边走',
        'if nums[i] % p == 0': lambda S, B, r: f'旧值 `nums[{S.i}] = {S.nums[S.i]}` ' + ('是' if S.nums[S.i] % S.p == 0 else '不是') + f' `p = {S.p}` 的倍数' + ('，要从计数里拿掉' if S.nums[S.i] % S.p == 0 else '，计数不变'),
        'cnt_p -= 1': '旧值是倍数，先从计数里拿掉：`cnt_p` → {cnt_p}',
        'if x % p == 0': lambda S, B, r: f'新值 `{S.x}` ' + ('是' if S.x % S.p == 0 else '不是') + f' `p = {S.p}` 的倍数' + ('，要加进计数' if S.x % S.p == 0 else '，计数不变'),
        'cnt_p += 1': '新值是倍数：`cnt_p` → {cnt_p}',
        'nums[i] = x': '`nums[{i}]` 改成 `{x}`',
        't.update(i, x)': '同步线段树：自底向上重算 GCD，`O(log n)`',
        'if t.query_all() == p and': _chk,
        'ans += 1': '这次查询后存在好子序列：`ans` → =={ans}==',
        'return any(': '依次试着不选 `nums[i]`：左边 `[0, i-1]` 的 GCD 与右边 `[i+1, n-1]` 的 GCD 再求 GCD，等于 `p` 就成功',
        'return ans': '一共 `{ans}` 次查询后存在好子序列',
    },
    cards=dict(
        one_liner='只看 p 的倍数：它们的 GCD 等于 p 才有戏，n ≤ 6 时再特判',
        complexity='时间 `O(n log U + q(log n + log U))`，空间 `O(n)`',
        problem=['数组 `nums` 和整数 `p`，单点修改 `q` 次；子序列长度必须 `< n`，GCD 恰好等于 `p` 才算好子序列',
                 '每次修改后判断是否存在好子序列，统计「存在」的次数',
                 '示例：`nums=[4,8,12,16], p=2, queries=[[0,3],[2,6]]` → `1`',
                 '本视频：`[4,5,6]`，`p=2`，三次修改 → `2`'],
        quote='参与 GCD 的数越多，GCD 越小。那么把所有是 p 的倍数的数都选上，如果这些数的 GCD 不等于 p，那么选更少的数，GCD 也无法等于 p。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不是 `p` 的倍数的数一定不能选；==把所有倍数都选上，GCD 最小==，用线段树维护单点修改',
              '倍数 GCD = `p` 且倍数不足 `n` 个：直接成立；倍数恰好 `n` 个就必须删一个',
              '删任何一个数 GCD 都变大，要求至少 `n` 个不同质数；值域 5·10^4 内最多 5 个 → ==`n > 6` 时一定能删==',
              '所以只有 `n ≤ 6` 才枚举删哪个：`check` 用左右两段的 GCD 合并'],
        summary=['时间 `O(n log U + q(log n + log U))`，GCD 沿路径上总共只减半 `O(log)` 次',
                 '叶子用 `0` 表示「不是倍数」：`gcd(0, g) = g`，不影响合并',
                 '易错：`cnt_p` 要在改 `nums[i]` 前先用旧值减、新值加；`n ≤ 6` 才调用 `check`',
                 '思考题（原文）：如果有区间修改操作呢？'],
    ),
)

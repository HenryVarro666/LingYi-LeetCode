_SETUP = '''
MX = 100_001
is_p = [True] * MX
is_p[0] = is_p[1] = False
for i in range(2, MX):
    if is_p[i]:
        for j in range(i * i, MX, i):
            is_p[j] = False

from bisect import insort


class SortedList:  # 最小替代 sortedcontainers.SortedList
    def __init__(self):
        self.a = []

    def add(self, x):
        insort(self.a, x)

    def remove(self, x):
        self.a.remove(x)

    def __getitem__(self, i):
        return self.a[i]

    def __len__(self):
        return len(self.a)

    def __iter__(self):
        return iter(self.a)

    def __repr__(self):
        return repr(self.a)
'''


def _seg(S):
    seg = S.get('self._tree')
    if seg:
        return seg
    t = S.get('t')
    return getattr(t, '_tree', None)


def _leaves(S):
    """每个下标当前真实的 cnt 值（把祖先的 todo 累加起来，不改动树）"""
    seg = _seg(S)
    n = S.get('n')
    if not seg or not n:
        return [0] * (n or 0)
    out = [0] * n

    def go(o, l, r, add):
        if l == r:
            out[l] = seg[o].val + add
            return
        m = (l + r) // 2
        go(o * 2, l, m, add + seg[o].todo)
        go(o * 2 + 1, m + 1, r, add + seg[o].todo)
    try:
        go(1, 0, n - 1, 0)
    except Exception:
        pass
    return out


def _draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    seg = _seg(S)
    n = S.get('n')
    cv.text((x0 + 18, y0 + 4), '线段树：每个节点 val(区间最大) / todo(懒标记)；黄框 = 本步改动', 22, T['muted'], bold=True)
    if not seg or not n or 'queries' not in S and 'nums' not in S:
        return
    Bs = _seg(B)
    pos = {}
    gap = min(100, (y1 - y0 - 110) / max(1, (n - 1).bit_length()))

    def lay(o, l, r, d, lo, hi):
        pos[o] = ((lo + hi) / 2, y0 + 70 + d * gap, l, r, hi - lo)
        if l == r:
            return
        m = (l + r) // 2
        c = (lo + hi) / 2
        lay(o * 2, l, m, d + 1, lo, c)
        lay(o * 2 + 1, m + 1, r, d + 1, c, hi)

    lay(1, 0, n - 1, 0, x0 + 10, x1 - 10)
    for o, (cx, cy, l, r, ww) in pos.items():
        for c in (o * 2, o * 2 + 1):
            if c in pos:
                cv.line([(cx, cy + 28), (pos[c][0], pos[c][1] - 28)], T['border'], 2)
    for o, (cx, cy, l, r, ww) in pos.items():
        nd = seg[o]
        if not hasattr(nd, 'val') or not hasattr(nd, 'todo'):
            continue
        ch = False
        if Bs is not None and o < len(Bs) and hasattr(Bs[o], 'val') and hasattr(Bs[o], 'todo'):
            ch = (Bs[o].val, Bs[o].todo) != (nd.val, nd.todo)
        w = min(140, ww * 0.9)
        cv.rect((cx - w / 2, cy - 28, cx + w / 2, cy + 28), fill=(30, 36, 46),
                outline=T['yellow'] if ch else T['border'], width=4 if ch else 2, r=8)
        cv.text((cx, cy - 24), f'[{l},{r}]', 16, T['dim'], anchor='mt', mono=True)
        cv.text((cx, cy), f'{nd.val} / {nd.todo}', 22, T['text'], anchor='mt', bold=True, mono=True)


def _isp(v):
    return v > 1 and all(v % d for d in range(2, int(v ** 0.5) + 1))


CONFIG = dict(
    num=3569, title='分割数组后不同质数的最大数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='Lazy 线段树（区间加、区间最大）+ 分类讨论',
    tags=['灵神题单', '常用数据结构', '难度分 2697'],
    code='''
class Node:
    __slots__ = 'val', 'todo'

class LazySegmentTree:
    # 懒标记初始值
    _TODO_INIT = 0

    def __init__(self, n: int, init_val=0):
        # 线段树维护一个长为 n 的数组（下标从 0 到 n-1），元素初始值为 init_val
        # init_val 可以是 list 或者 int
        # 如果是 int，那么创建一个 list
        if isinstance(init_val, int):
            init_val = [init_val] * n
        self._n = n
        self._tree = [Node() for _ in range(2 << (n - 1).bit_length())]
        self._build(init_val, 1, 0, n - 1)

    # 合并两个 val
    def _merge_val(self, a: int, b: int) -> int:
        return a if a > b else b

    # 把懒标记作用到 node 子树（本例为区间加）
    def _apply(self, node: int, l: int, r: int, todo: int) -> None:
        cur = self._tree[node]
        # 计算 tree[node] 区间的整体变化
        cur.val += todo
        cur.todo += todo

    # 把当前节点的懒标记下传给左右儿子
    def _spread(self, node: int, l: int, r: int) -> None:
        todo = self._tree[node].todo
        if todo == self._TODO_INIT:  # 没有需要下传的信息
            return
        m = (l + r) // 2
        self._apply(node * 2, l, m, todo)
        self._apply(node * 2 + 1, m + 1, r, todo)
        self._tree[node].todo = self._TODO_INIT  # 下传完毕

    # 合并左右儿子的 val 到当前节点的 val
    def _maintain(self, node: int) -> None:
        self._tree[node].val = self._merge_val(self._tree[node * 2].val, self._tree[node * 2 + 1].val)

    # 用 a 初始化线段树
    # 时间复杂度 O(n)
    def _build(self, a: List[int], node: int, l: int, r: int) -> None:
        self._tree[node].todo = self._TODO_INIT
        if l == r:  # 叶子
            self._tree[node].val = a[l]  # 初始化叶节点的值
            return
        m = (l + r) // 2
        self._build(a, node * 2, l, m)  # 初始化左子树
        self._build(a, node * 2 + 1, m + 1, r)  # 初始化右子树
        self._maintain(node)

    def _update(self, node: int, l: int, r: int, ql: int, qr: int, f: int) -> None:
        if ql <= l and r <= qr:  # 当前子树完全在 [ql, qr] 内
            self._apply(node, l, r, f)
            return
        self._spread(node, l, r)
        m = (l + r) // 2
        if ql <= m:  # 更新左子树
            self._update(node * 2, l, m, ql, qr, f)
        if qr > m:  # 更新右子树
            self._update(node * 2 + 1, m + 1, r, ql, qr, f)
        self._maintain(node)

    def _query(self, node: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:  # 当前子树完全在 [ql, qr] 内
            return self._tree[node].val
        self._spread(node, l, r)
        m = (l + r) // 2
        if qr <= m:  # [ql, qr] 在左子树
            return self._query(node * 2, l, m, ql, qr)
        if ql > m:  # [ql, qr] 在右子树
            return self._query(node * 2 + 1, m + 1, r, ql, qr)
        l_res = self._query(node * 2, l, m, ql, qr)
        r_res = self._query(node * 2 + 1, m + 1, r, ql, qr)
        return self._merge_val(l_res, r_res)

    # 用 f 更新 [ql, qr] 中的每个 a[i]
    # 0 <= ql <= qr <= n-1
    # 时间复杂度 O(log n)
    def update(self, ql: int, qr: int, f: int) -> None:
        self._update(1, 0, self._n - 1, ql, qr, f)

    # 返回用 _merge_val 合并所有 a[i] 的计算结果，其中 i 在闭区间 [ql, qr] 中
    # 0 <= ql <= qr <= n-1
    # 时间复杂度 O(log n)
    def query(self, ql: int, qr: int) -> int:
        return self._query(1, 0, self._n - 1, ql, qr)

class Solution:
    def maximumCount(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        pos = defaultdict(SortedList)
        for i, x in enumerate(nums):
            if is_p[x]:
                pos[x].add(i)

        t = LazySegmentTree(n, 0)
        for sl in pos.values():
            if len(sl) > 1:
                t.update(sl[0], sl[-1], 1)

        def update(sl: SortedList, i: int, delta: int) -> None:
            l, r = sl[0], sl[-1]
            if l == r:
                t.update(min(l, i), max(r, i), delta)
            elif i < l:
                t.update(i, l - 1, delta)
            elif i > r:
                t.update(r + 1, i, delta)

        ans = []
        for i, val in queries:
            old = nums[i]
            nums[i] = val

            # 处理旧值
            if is_p[old]:
                sl = pos[old]
                sl.remove(i)
                if sl:
                    update(sl, i, -1)
                else:
                    del pos[old]

            # 处理新值
            if is_p[val]:
                sl = pos[val]
                if sl:
                    update(sl, i, 1)
                sl.add(i)

            # 整个数组的不同质数个数 + 切一刀的最大额外收益
            ans.append(len(pos) + t.query(0, n - 1))

        return ans
''',
    setup=_SETUP,
    call='Solution().maximumCount([2, 3, 1, 2], [[2, 3], [1, 1]])',
    expect=[4, 3],
    views=[
        dict(type='array', var='nums', label='nums（橙 = 质数）', h=190, cell=80, pointers={'i': 'blue'},
             color=lambda S, i, v: 'orange' if _isp(v) else None),
        dict(type='array', var=_leaves, label='cnt：切在 k 左边带来的额外收益（线段树维护）', h=190, cell=80),
        dict(type='map', var='pos', label='pos：质数 → 出现下标', fmt=lambda k, v: f'{k} → {list(v)}', h=130),
        dict(type='custom', draw=_draw_tree, h=300),
    ],
    watch=['i', 'old', 'val', ('len(pos)', 'len(pos)', 'cyan'), ('ans', 'ans', 'green')],
    skip=['self._TODO_INIT', 'self._n = n', 'init_val', 'self._tree = [Node()', 'self._build(', 'cur = self._tree', 'cur.todo += todo',
          'def _spread', 49, 'self._tree[node].todo = self._TODO_INIT', 'todo = self._tree', 'm = (l + r) // 2', 'a if a > b else b', 'n = len(nums)',
          'pos = defaultdict', 'def update', 'ans = []', 'self._update(1, 0', 'return self._query(1', 'if todo == self._TODO_INIT',
          'self._apply(node * 2', 'self._maintain(node)', 'self._tree[node].val = self._merge_val',
          'if l == r:  # 叶子', 'self._tree[node].val = a[l]', 'self._build(a, node', 'return self._tree[node].val', 'for sl in pos.values()', 'if len(sl) > 1'],
    max_steps=56,
    captions={
        'old = nums[i]': '第 {i} 次修改：`nums[{i}]` 从 `{old}` 改成 `{val}`，先记下旧值',
        'if is_p[old]': lambda S, B, r: (f'旧值 `{S.old}` 是质数 → 它在下标 `{S.i}` 的出现要撤销' if _isp(S.old) else f'旧值 `{S.old}` 不是质数，不影响答案'),
        'sl.remove(i)': '`{old}` 不再出现在下标 `{i}`：从它的有序集合里删掉，现在是 `{list(sl)}`',
        'if sl:': lambda S, B, r: (f'`sl = {list(S.sl)}` 里还有下标：要看 `i = {S.i}` 会不会改变它的 [最左, 最右] 范围' if S.sl else '集合空了：这个质数不再出现，从 `pos` 里删掉'),
        'update(sl, i, -1)': '旧值：把「因为下标 i 才多出来的区间」减 1',
        'update(sl, i, 1)': '新值：把「因为下标 i 才多出来的区间」加 1',
        'l, r = sl[0], sl[-1]': '这个质数当前最左出现 `l = {l}`，最右出现 `r = {r}`（不含 `i` 自己的变化）',
        'if l == r': lambda S, B, r: (f'只有一个下标 `{S.l}`：加/减 `i = {S.i}` 之后，`{S.l}` 和 `{S.i}` 之间整段会多/少一次' if S.l == S.r else f'`l = {S.l} ≠ r = {S.r}`，已经至少有两个下标，再看 `i` 在不在范围外'),
        'elif i < l': lambda S, B, r: (f'`i = {S.i} < l = {S.l}`：最左端往左扩，只有 `[{S.i}, {S.l - 1}]` 受影响' if S.i < S.l else f'`i = {S.i}` 不在 `l = {S.l}` 左边'),
        'elif i > r': lambda S, B, r: (f'`i = {S.i} > r = {S.r}`：最右端往右扩，只有 `[{S.r + 1}, {S.i}]` 受影响' if S.i > S.r else f'`i = {S.i}` 落在 `[{S.l}, {S.r}]` 里面 → ==不用改线段树=='),
        't.update(min(l, i), max(r, i), delta)': '区间 `[{min(l, i)}, {max(r, i)}]` 加 `{delta}`',
        't.update(i, l - 1, delta)': '区间 `[{i}, {l - 1}]` 加 `{delta}`',
        't.update(r + 1, i, delta)': '区间 `[{r + 1}, {i}]` 加 `{delta}`',
        'self._spread(node, l, r)': '这个节点只有一部分在 `[ql, qr]` 里：要往下走，先把它的懒标记推给两个儿子',
        'cur.val += todo': '`val` 和 `todo` 都加 `{todo}`：整块一起加，先记着，不往叶子推',
        'ans.append': lambda S, B, r: f'答案 = 不同质数种数 `len(pos) = {len(S.pos)}` + 整个 cnt 的最大值 `{max(_leaves(S))}`（线段树根节点的 `val`）= =={len(S.pos) + max(_leaves(S))}==',
        'return ans': '每次修改后的答案：`{ans}`',
    },
    cards=dict(
        one_liner='切一刀 = 整体质数种数 + 某个下标的最大额外收益',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['数组 `nums` 依次修改 `q` 次，每次修改后选一个切点，把数组分成非空前后两段',
                 '求两段里「不同质数个数」之和的最大值，每次修改后各答一个',
                 '本视频：`[2,3,1,2]`，查询 `[[2,3],[1,1]]` → `[4,3]`'],
        quote='相加结果等价于如下两部分之和：1. 切一刀之前，整个数组的不同质数之和。2. 切一刀之后，带来的额外收益。考虑一个至少出现两次的质数，其最左边的出现位置 l 和最右边的出现位置 r，如果 l+1≤k≤r，那么分割后，左右两边都有同一个质数，答案可以额外加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['质数 `p` 至少出现两次时，切点落在它最左、最右出现位置之间，就能让 `p` 在两边各算一次',
              '于是 `cnt` 数组里对区间 `[l, r]` 加 1，`cnt` 的最大值就是切一刀的最大额外收益',
              '用有序集合记录每个质数的所有下标，改动时只在两端变化处更新区间（写法二：分类讨论）'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`；答案 = `len(pos)` + 整个 `cnt` 的最大值',
                 '写法二比写法一少更新线段树：只有最左/最右出现位置变化时才加减区间',
                 '`l == r`（原来只有一个）时，加入新下标后区间是 `[min(l,i), max(r,i)]`',
                 '题解里的质数筛放到了 `setup`（预处理，不演示）；`SortedList` 来自 sortedcontainers，这里用最小替代实现',
                 '写法一：每次先撤销旧区间再加新区间，更直观但更新次数更多'],
    ),
)

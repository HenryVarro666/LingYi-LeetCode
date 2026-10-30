_CODE = '''
# 手写 min max 更快
min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a

class Node:
    __slots__ = 'min', 'max', 'todo'

    def __init__(self):
        self.min = self.max = self.todo = 0

class LazySegmentTree:
    def __init__(self, n: int):
        self._n = n
        self._tree = [Node() for _ in range(2 << (n - 1).bit_length())]

    # 把懒标记作用到 node 子树
    def _apply(self, node: int, todo: int) -> None:
        cur = self._tree[node]
        cur.min += todo
        cur.max += todo
        cur.todo += todo

    # 把当前节点的懒标记下传给左右儿子
    def _spread(self, node: int) -> None:
        todo = self._tree[node].todo
        if todo == 0:  # 没有需要下传的信息
            return
        self._apply(node * 2, todo)
        self._apply(node * 2 + 1, todo)
        self._tree[node].todo = 0  # 下传完毕

    # 合并左右儿子的 min max 到当前节点
    def _maintain(self, node: int) -> None:
        l_node = self._tree[node * 2]
        r_node = self._tree[node * 2 + 1]
        self._tree[node].min = min(l_node.min, r_node.min)
        self._tree[node].max = max(l_node.max, r_node.max)

    def _update(self, node: int, l: int, r: int, ql: int, qr: int, f: int) -> None:
        if ql <= l and r <= qr:  # 当前子树完全在 [ql, qr] 内
            self._apply(node, f)
            return
        self._spread(node)
        m = (l + r) // 2
        if ql <= m:  # 更新左子树
            self._update(node * 2, l, m, ql, qr, f)
        if qr > m:  # 更新右子树
            self._update(node * 2 + 1, m + 1, r, ql, qr, f)
        self._maintain(node)

    def _find_first(self, node: int, l: int, r: int, ql: int, qr: int, target: int) -> int:
        if l > qr or r < ql or not self._tree[node].min <= target <= self._tree[node].max:
            return -1
        if l == r:
            return l
        self._spread(node)
        m = (l + r) // 2
        idx = self._find_first(node * 2, l, m, ql, qr, target)
        if idx < 0:
            # 去右子树找
            idx = self._find_first(node * 2 + 1, m + 1, r, ql, qr, target)
        return idx

    # 用 f 更新 [ql, qr] 中的每个 sum[i]
    # 0 <= ql <= qr <= n-1
    # 时间复杂度 O(log n)
    def update(self, ql: int, qr: int, f: int) -> None:
        self._update(1, 0, self._n - 1, ql, qr, f)

    # 查询 [ql, qr] 内第一个等于 target 的元素下标
    # 找不到返回 -1
    # 0 <= ql <= qr <= n-1
    # 时间复杂度 O(log n)
    def find_first(self, ql: int, qr: int, target: int) -> int:
        return self._find_first(1, 0, self._n - 1, ql, qr, target)

class Solution:
    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        t = LazySegmentTree(n + 1)

        last = {}  # nums 的元素上一次出现的位置
        ans = cur_sum = 0
        for i, x in enumerate(nums, 1):
            v = 1 if x % 2 else -1
            j = last.get(x, 0)
            if j == 0:  # 首次遇到 x
                cur_sum += v
                t.update(i, n, v)  # sum[i:] 增加 v
            else:  # 再次遇到 x
                t.update(j, i - 1, -v)  # 撤销之前对 sum[j:i] 的增加
            last[x] = i

            # 把 i-1 优化成 i-1-ans，因为在下标 > i-1-ans 中搜索是没有意义的，不会把答案变大
            j = t.find_first(0, i - 1 - ans, cur_sum)
            if j >= 0:
                ans = i - j  # 如果找到了，那么答案肯定会变大
        return ans
'''
_LN = _CODE.strip('\n').split('\n')
_a = next(i for i, l in enumerate(_LN, 1) if l.startswith('class Node'))
_b = next(i for i, l in enumerate(_LN, 1) if l.startswith('class Solution'))
_keep = {i for i, l in enumerate(_LN, 1) if l.strip() in ('cur.min += todo', 'return l')}
_SKIP = [i for i in range(_a, _b) if i not in _keep and _LN[i - 1].strip()]


def _seg(S):
    seg = S.get('self._tree')
    if seg:
        return seg
    t = S.get('t')
    return getattr(t, '_tree', None)


def _sums(S):
    t = S.get('t')
    seg = _seg(S)
    n = getattr(t, '_n', None) or (len(S['nums']) + 1 if 'nums' in S else 0)
    if not seg or not n:
        return []
    out = [0] * n

    def go(o, l, r, add):
        if l == r:
            out[l] = seg[o].min + add
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
    t = S.get('t')
    n = getattr(t, '_n', None) or getattr(S.get('self'), '_n', None) if S.get('t') or S.get('self') else None
    cv.text((x0 + 18, y0 + 4), '线段树：min / max / todo（黄框 = 本步改动）', 22, T['muted'], bold=True)
    if not seg or not n:
        return
    Bs = _seg(B)
    pos = {}
    depth = (n - 1).bit_length()
    gap = min(90, (y1 - y0 - 100) / max(1, depth))

    def lay(o, l, r, d, lo, hi):
        pos[o] = ((lo + hi) / 2, y0 + 64 + d * gap, l, r, hi - lo)
        if l == r:
            return
        m = (l + r) // 2
        c = (lo + hi) / 2
        lay(o * 2, l, m, d + 1, lo, c)
        lay(o * 2 + 1, m + 1, r, d + 1, c, hi)

    lay(1, 0, n - 1, 0, x0 + 6, x1 - 6)
    for o, (cx, cy, l, r, ww) in pos.items():
        for c in (o * 2, o * 2 + 1):
            if c in pos:
                cv.line([(cx, cy + 24), (pos[c][0], pos[c][1] - 24)], T['border'], 2)
    for o, (cx, cy, l, r, ww) in pos.items():
        nd = seg[o]
        ch = False
        if Bs is not None and o < len(Bs):
            ch = (Bs[o].min, Bs[o].max, Bs[o].todo) != (nd.min, nd.max, nd.todo)
        w = min(120, ww * 0.92)
        cv.rect((cx - w / 2, cy - 24, cx + w / 2, cy + 24), fill=(30, 36, 46),
                outline=T['yellow'] if ch else T['border'], width=4 if ch else 2, r=6)
        cv.text((cx, cy - 22), f'[{l},{r}]', 14, T['dim'], anchor='mt', mono=True)
        cv.text((cx, cy - 4), f'{nd.min},{nd.max}/{nd.todo}', 18, T['text'], anchor='mt', bold=True, mono=True)


def _star(S, k, v):
    """nums[k] 在当前前缀里不是它这个值最近一次出现 → 视作 *"""
    i, last = S.get('i'), S.get('last')
    if i is None or last is None:
        return False
    if k + 1 > i:
        return True
    return k + 1 != i and last.get(v) != k + 1


def _fmt_text(S):
    if 'cur_sum' not in S:
        return '把偶数视作 −1、奇数视作 +1，重复元素只保留最近一次出现'
    return f"当前 `sum[i] = cur_sum` = ==`{S['cur_sum']}`==；在 `sum[0..{S.get('i', 1) - 1 - S.get('ans', 0)}]` 里找最靠左的、值也是 `{S['cur_sum']}` 的位置"


CONFIG = dict(
    num=3721, title='最长平衡子数组 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='Lazy 线段树（区间加 + 找首个等于 target）',
    tags=['灵神题单', '常用数据结构', '难度分 2724'],
    code=_CODE,
    call='Solution().longestBalanced([1, 2, 3, 2])',
    expect=3,
    views=[
        dict(type='text', fn=_fmt_text, size=24, h=70),
        dict(type='array', var='nums', label='nums（灰 = 不是最近一次出现，视作 *）', h=170, cell=80,
             window=(lambda S: 0 if 'i' in S else None, lambda S: S['i'] - 1 if 'i' in S else None),
             dim=lambda S, k, v: _star(S, k, v)),
        dict(type='array', var=_sums, label='sum（前缀和，线段树维护；重复值只算最近一次）', h=170, cell=80,
             color=lambda S, k, v: ('pink' if S.get('j', -1) >= 0 and k == S['j'] and S.get('_line', 0) >= 95 else 'green' if 'cur_sum' in S and v == S['cur_sum'] else None)),
        dict(type='custom', draw=_draw_tree, h=260),
    ],
    watch=['i', 'x', 'v', ('cur_sum', 'cur_sum', 'cyan'), ('j', 'j', 'pink'), ('ans', 'ans', 'green'), ('last', 'last')],
    skip=['min = lambda', 'max = lambda', 'n = len(nums)', 't = LazySegmentTree', 'last = {}'] + _SKIP,
    max_steps=60,
    captions={
        'ans = cur_sum = 0': '`ans` 是答案，`cur_sum` 是当前前缀的 sum 值，都从 0 开始',
        'for i, x in enumerate(nums, 1)': lambda S, B, r: (f'遍历结束，`ans = {S.ans}`' if B.get('i') == S.i else f'`i = {S.i}`（从 1 开始）：处理 `nums[{S.i - 1}] = {S.x}`，前缀长度 {S.i}'),
        'v = 1 if x % 2 else -1': lambda S, B, r: f'`x = {S.x}` 是{"奇" if S.x % 2 else "偶"}数 → `v = {S.v}`（奇 +1，偶 −1）',
        'j = last.get(x, 0)': lambda S, B, r: (f'`{S.x}` 以前没出现过 → `j = 0`' if S.j == 0 else f'`{S.x}` 上次出现在位置 `{S.j}` → `j = {S.j}`'),
        'if j == 0': lambda S, B, r: ('首次遇到 `x`：它要被计入，`[i, n]` 的 sum 全体 `+v`' if S.j == 0 else '`x` 之前出现过：它只能算一次，要把旧位置的那份挪过来'),
        'cur_sum += v': '当前前缀的 `sum[i]` 也跟着变：`cur_sum` → =={cur_sum}==',
        't.update(i, n, v)': '`sum[i..n]` 全部加 `{v}`（从第 {i} 个元素起，每个前缀都包含了新元素 `x`）',
        't.update(j, i - 1, -v)': '`x` 搬到了新位置 `i`：旧位置 `j = {j}` 变成 *，所以撤销 `sum[{j}..{i - 1}]` 里那份 `{v}`',
        'last[x] = i': '记下 `x` 最近一次出现在位置 `{i}`',
        't.find_first(0, i - 1 - ans': lambda S, B, r: f'在 `sum[0..{S.i - 1 - S.ans}]` 里找最左的、等于 `cur_sum = {S.cur_sum}` 的下标（相邻差 ≤ 1，`min ≤ target ≤ max` 就必有）',
        'if j >= 0': lambda S, B, r: (f'找到了 `j = {S.j}`：`sum[{S.j}] = sum[{S.i}]` → 区间 `[{S.j}, {S.i})` 平衡' if S.j >= 0 else '没找到 → 没有比 `ans` 更长的平衡子数组'),
        'ans = i - j': '长度 `i − j = {i} − {j}` = =={ans}==；这里一定比之前的 `ans` 大（因为只在 `[0, i-1-ans]` 里搜）',
        'cur.min += todo': '整块 `min` / `max` / `todo` 都加 `{todo}`，先记着，不往叶子推',
        'return l': '找到了：叶子 `{l}` 的值就是 target',
        'return ans': '最长平衡子数组长度 =={ans}==',
    },
    cards=dict(
        one_liner='只保留每个数最近一次出现，变成「和为 0 的最长子数组」',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['子数组里「不同偶数个数 = 不同奇数个数」就算平衡，求最长平衡子数组的长度',
                 '同一个数出现多次只算一种',
                 '本视频：`[1,2,3,2]` → `3`（子数组 `[2,3,2]`）'],
        quote='从左到右遍历 nums，如果固定子数组右端点为 i，要想让子数组包含某个元素 x，左端点必须 ≤ x 最后一次出现的位置。……那么把除了最近一次的 x 全部不计入，就变成 525 题了！',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇数视作 +1、偶数视作 −1，「相同元素只算一次」靠把旧位置变成 0（*）来实现',
              '首次遇到 `x`：`sum[i:]` 全部加 `v`；再次遇到：撤销 `sum[j:i]` 里旧的那份',
              '`sum` 相邻只差 ≤ 1，所以用 Lazy 线段树维护区间 min / max，判断「target 在不在区间里」就能二分找最左位置'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '搜索范围优化成 `[0, i-1-ans]`：更靠右的位置找到也不会让答案变大',
                 '线段树要开 `n+1` 个叶子，因为前缀和多一项 `sum[0]`',
                 '题解还给了方法二：分块，不依赖 sum 相邻差 ≤ 1，时间 `O(n√n)`',
                 '前置题：525 连续数组（相同元素都算时的做法）'],
    ),
)

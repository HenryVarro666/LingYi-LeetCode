from bisect import bisect_left, bisect_right


def _tarr(S):
    o = S.get('t')
    if o is not None and hasattr(o, 't'):
        return o.t
    return S.get('self.t')


def _fmt(v):
    return '-∞' if v == float('-inf') else str(v)


def _tree(S):
    """list of (node, l, r, depth) for the value-domain segment tree"""
    M = len(S['sorted_nums'])
    out = []

    def go(node, l, r, d):
        out.append((node, l, r, d))
        if l < r:
            m = (l + r) // 2
            go(node * 2, l, m, d + 1)
            go(node * 2 + 1, m + 1, r, d + 1)
    go(1, 0, M - 1, 0)
    return out


def _qrange(S):
    inn = S.get('_inner', {})
    if 'ql' in inn:
        return inn['ql'], inn['qr']
    if 'l' in S and 'r' in S and 'j' in S and 'node' not in inn and S.get('_line') in (42, 43, 44):
        return S['l'], S['r']
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    arr = _tarr(S)
    cv.text((x0 + 18, y0 + 4), '值域线段树：每个节点 = 一段值域（名次区间）里最大的 f', 24, T['muted'], bold=True)
    if arr is None or 'sorted_nums' not in S:
        return
    nodes = _tree(S)
    M = len(S['sorted_nums'])
    maxd = max(d for _, _, _, d in nodes)
    inn = S.get('_inner', {})
    cur = inn.get('node') if 'node' in inn else None
    qr = _qrange(S)
    W = x1 - x0 - 60
    cw = min(150, W / M)
    sx = x0 + 30 + (W - cw * M) / 2
    top, bottom = y0 + 90, y1 - 120
    dy = (bottom - top) / max(1, maxd)
    pos = {}
    for node, l, r, d in sorted(nodes, key=lambda n: -n[3]):
        if l == r:
            cx = sx + (l + 0.5) * cw
        else:
            cx = (pos[node * 2][0] + pos[node * 2 + 1][0]) / 2
        pos[node] = (cx, top + d * dy)
    bw, bh = min(130, cw - 10), 70
    for node, l, r, d in nodes:
        if l < r:
            for ch in (node * 2, node * 2 + 1):
                cv.line([(pos[node][0], pos[node][1] + bh / 2), (pos[ch][0], pos[ch][1] - bh / 2)], T['border'], 2)
    for node, l, r, d in nodes:
        cx, cy = pos[node]
        v = arr[node] if node < len(arr) else float('-inf')
        inside = qr is not None and qr[0] <= l and r <= qr[1]
        fill = (30, 70, 45) if inside else T['panel2']
        out = T['yellow'] if node == cur else T['border']
        cv.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), fill=fill, outline=out, width=4 if node == cur else 2, r=8)
        cv.text((cx, cy - 16), f'[{l},{r}]' if l < r else f'[{l}]', 20, T['muted'], anchor='mm', mono=True)
        cv.text((cx, cy + 14), _fmt(v), 30, T['green'] if v != float('-inf') else T['dim'], anchor='mm', bold=True)
    base = bottom + bh / 2 + 22
    for k, val in enumerate(S['sorted_nums']):
        cx = sx + (k + 0.5) * cw
        hit = qr is not None and qr[0] <= k <= qr[1]
        cv.text((cx, base), val, 26, T['green'] if hit else T['text'], anchor='mm', bold=True)
        cv.text((cx, base + 28), k, 18, T['dim'], anchor='mm', mono=True)
    if qr is not None and qr[0] <= qr[1]:
        a, b = sx + qr[0] * cw + 6, sx + (qr[1] + 1) * cw - 6
        cv.line([(a, base + 50), (b, base + 50)], T['green'], 4)
        cv.text(((a + b) / 2, base + 62), f'查询值域 [{qr[0]}, {qr[1]}]', 20, T['green'], anchor='mt', bold=True)
    cv.text((sx - 10, base), 'sorted_nums', 18, T['dim'], anchor='rm')


def _formula(S):
    inn = S.get('_inner', {})
    if 'j' not in S:
        return '`f[j]` = 跳到 j 的最大次数；线段树按值域保存每个值上的最大 f'
    j = S['j']
    if 'l' in S and 'r' in S and 'node' not in inn:
        lo, hi = S['sorted_nums'][S['l']] if S['l'] < len(S['sorted_nums']) else '?', S['sorted_nums'][S['r']] if 0 <= S['r'] < len(S['sorted_nums']) else '?'
        return f'`nums[{j}] = {S["nums"][j]}`，能从值在 `[{S["nums"][j] - S["target"]}, {S["nums"][j] + S["target"]}]` 的位置跳过来'
    if 'ql' in inn:
        return f'查 [{inn["ql"]}, {inn["qr"]}]：当前节点 `[{inn["l"]}, {inn["r"]}]`'
    return f'更新位置 `{inn["i"]}`：当前节点 `[{inn["l"]}, {inn["r"]}]`' if 'i' in inn else ''


CONFIG = dict(
    num=2770, title='达到末尾下标所需的最大跳跃次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='值域线段树优化 DP',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
# 完整的线段树模板见 https://leetcode.cn/circle/discuss/mOr1u6/
class SegmentTree:
    def __init__(self, n: int) -> None:
        self.t = [-inf] * (2 << (n - 1).bit_length())

    def update(self, node: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:  # 叶子
            self.t[node] = val
            return
        m = (l + r) // 2
        if i <= m:  # i 在左子树
            self.update(node * 2, l, m, i, val)
        else:  # i 在右子树
            self.update(node * 2 + 1, m + 1, r, i, val)
        self.t[node] = max(self.t[node * 2], self.t[node * 2 + 1])

    def query(self, node: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:  # 当前子树完全在 [ql, qr] 内
            return self.t[node]
        m = (l + r) // 2
        if qr <= m:  # [ql, qr] 在左子树
            return self.query(node * 2, l, m, ql, qr)
        if ql > m:  # [ql, qr] 在右子树
            return self.query(node * 2 + 1, m + 1, r, ql, qr)
        return max(self.query(node * 2, l, m, ql, qr), self.query(node * 2 + 1, m + 1, r, ql, qr))

class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        # 去重排序，便于离散化
        sorted_nums = sorted(set(nums))

        n = len(nums)
        m = len(sorted_nums)
        t = SegmentTree(m)  # 值域线段树

        # nums[0] 对应的 f[0] = 0
        t.update(1, 0, m - 1, bisect_left(sorted_nums, nums[0]), 0)

        for j in range(1, n):
            l = bisect_left(sorted_nums, nums[j] - target)       # >= nums[j]-target 的第一个数
            r = bisect_right(sorted_nums, nums[j] + target) - 1  # <= nums[j]+target 的最后一个数
            # t.query 返回满足 nums[j]-target <= nums[i] <= nums[j]+target 的最大的 f[i]
            fj = t.query(1, 0, m - 1, l, r) + 1
            t.update(1, 0, m - 1, bisect_left(sorted_nums, nums[j]), fj)

        return -1 if fj < 0 else fj
''',
    call='Solution().maximumJumps([2,5,3], 1)',
    expect=1,
    views=[
        dict(type='text', fn=_formula, size=24, h=56),
        dict(type='array', var='nums', label='nums（蓝 = 当前 j）', h=175, cell=80, color=lambda S, k, v: 'blue' if k == S.get('j') else None),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('j', 'j', 'blue'), ('fj', 'fj', 'green')],
    captions={
        'sorted_nums = sorted': '值域离散化：去重排序得 `{sorted_nums}`，线段树的"位置"就是这里的名次',
        't = SegmentTree': '建值域线段树：叶子 = `sorted_nums` 里的一个值，每个节点存它那段值域里 ==最大的 f==，初值 `-inf`',
        'sorted_nums, nums[0]': '`f[0] = 0`：把 `nums[0] = {nums[0]}` 对应的叶子设成 0',
        'if l == r': lambda S, B, r: (f'`l == r`（`{S.l} == {S.r}`）→ 到叶子了，直接写入' if S.l == S.r else f'`[{S.l}, {S.r}]` 不是叶子 → 继续往下找位置 `{S.i}`'),
        'if i <= m': lambda S, B, r: (f'位置 `{S.i} <= 中点 {S.m}` → 递归进左半边 `[{S.l}, {S.m}]`' if S.i <= S.m else f'位置 `{S.i} > 中点 {S.m}` → 递归进右半边 `[{S.m + 1}, {S.r}]`'),
        'self.t[node] = val': '叶子 `t[{node}] = {val}`（`-inf` 表示这个值上还没有可跳起点）',
        'self.t[node] = max(self.t[node * 2]': '回溯时更新父节点：`t[{node}]` = 左右孩子较大者 = =={self.t[node]}==',
        'if ql <= l and r <= qr': lambda S, B, r: (f'`[{S.l}, {S.r}]` 完全落在查询区间 `[{S.ql}, {S.qr}]` 内 → ==整块直接用== 它存的最大值' if S.ql <= S.l and S.r <= S.qr else f'`[{S.l}, {S.r}]` 只有一部分在 `[{S.ql}, {S.qr}]` 内 → 继续拆'),
        'return self.t[node]': '这一块的最大 f = =={ret}==（`-inf` 就是这段值域里没有可用起点）',
        'if qr <= m': lambda S, B, r: (f'`qr = {S.qr} <= 中点 {S.m}`：查询区间全在左半边 → 只查左子树' if S.qr <= S.m else f'`qr = {S.qr} > 中点 {S.m}`：右半边也有内容'),
        'if ql > m': lambda S, B, r: (f'`ql = {S.ql} > 中点 {S.m}`：查询区间全在右半边 → 只查右子树' if S.ql > S.m else f'`ql = {S.ql} <= 中点 {S.m}`：区间横跨中点，左右都要查'),
        'return max(self.query': '横跨中点：左右两边各查一次，取 ==较大者==',
        'l = bisect_left': lambda S, B, rt: (lambda lo, hi: f'能跳过来的值在 `[{S.nums[S.j] - S.target}, {S.nums[S.j] + S.target}]` → 换成名次区间 `[{lo}, {hi}]`（即 `sorted_nums[{lo}..{hi}]`）')(bisect_left(S.sorted_nums, S.nums[S.j] - S.target), bisect_right(S.sorted_nums, S.nums[S.j] + S.target) - 1),
        'fj = t.query': '问线段树：值域名次 `[{l}, {r}]` 里最大的 f 是多少？再 `+1` 就是 `f[{j}]`',
        'sorted_nums, nums[j]': '`f[{j}] = {fj}`（`-inf + 1` 还是 `-inf`，表示到不了）→ 写进 `nums[{j}] = {nums[j]}` 的叶子',
        'return -1 if fj < 0': '`fj = {fj}` 就是 `f[n-1]`：为负说明到不了，返回 `-1`；否则它就是答案',
    },
    skip=[9, 10, 20, 'n = len(nums)', 'm = len(sorted_nums)', 'self.update(node * 2', 'return self.query(node * 2', 'r = bisect_right'],
    max_steps=110,
    cards=dict(
        one_liner='f[j] = 值域 [nums[j]±target] 里最大的 f，再加 1',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['从下标 `0` 出发，只能向右跳到 `j`，要求 `|nums[j] − nums[i]| <= target`','求到达最后一个下标的==最大==跳跃次数，到不了返回 `-1`','本视频：`nums = [2,5,3]`，`target = 1` → `1`'],
        quote='遍历到 nums[j] 时，我们需要知道满足 nums[j]-target <= nums[i] <= nums[j]+target 的最大的 f[i]。这可以用一棵值域线段树维护。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`O(n^2)` 的递推是 `f[j] = max(f[i]) + 1`，枚举所有 `i < j`', '合法的 `i` 其实是==值域上的一段==：`nums[i] ∈ [nums[j]−target, nums[j]+target]`','值域线段树按值存 f：区间最大值查询 + 单点更新，各 `O(log n)`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`n=1000` 时 `O(n^2)` 也能过）','先把 `nums` 去重排序离散化，再用 `bisect` 把值域边界换成名次','`-inf + 1` 仍然是负数，所以最后用 `fj < 0` 判断到不了','灵神题解里还有记忆化搜索和 `O(n^2)` 递推两种写法，本视频演示最后的线段树优化','同类题：2407 最长递增子序列 II'],
    ),
)

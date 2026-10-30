ARR = 'mx'
ROOT = 1
CH = lambda o: (2 * o, 2 * o + 1)


def _nodes(u, root, ch):
    out = []

    def go(o, l, r, d):
        out.append((o, l, r, d))
        if l < r:
            m = (l + r) // 2
            a, b = ch(o)
            go(a, l, m, d + 1)
            go(b, m + 1, r, d + 1)
    go(root, 1, u, 0)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    arr = S.get(ARR)
    if arr is None:
        return
    u = max(S['nums'])
    nodes = _nodes(u, ROOT, CH)
    maxd = max(d for _, _, _, d in nodes) + 1
    W = x1 - x0 - 40
    slot = W / u
    dy = min(110, (y1 - y0 - 70) / maxd)
    bh = min(66, dy - 22)
    bw = min(150, slot * 2 - 14) if u > 1 else 140
    bw = max(70, min(bw, 150))
    inner = S.get('_inner') or {}
    kind = None
    qlo = qhi = tgt = None
    cur = None
    if 'p' in inner or 'o' in inner:
        cur = inner.get('p') if 'p' in inner else inner.get('o')
    if ('now' in inner and 'p' in inner) or 'val' in inner:
        kind = 'upd'
        tgt = inner.get('num') if 'num' in inner else inner.get('i')
    elif 'L' in inner or ('left' in inner and 'l' in inner):
        kind = 'qry'
        qlo = inner.get('L') if 'L' in inner else inner.get('left')
        qhi = inner.get('R') if 'R' in inner else inner.get('right')
    cx = {}
    for o, l, r, d in nodes:
        cx[o] = x0 + 20 + ((l - 1) + (r - l + 1) / 2) * slot
    cv.text((x0 + 18, y0 + 4), f'线段树：叶子 = 数值 1..{u}，节点值 = 区间最大 f（黄 = 当前）', 22, T['muted'], bold=True)
    pos = {}
    for o, l, r, d in nodes:
        pos[o] = (cx[o], y0 + 52 + d * dy)
    for o, l, r, d in nodes:
        if l < r:
            for c in CH(o):
                cv.line([(pos[o][0], pos[o][1] + bh), (pos[c][0], pos[c][1])], T['border'], 2)
    for o, l, r, d in nodes:
        X, Y = pos[o]
        fill = (50, 56, 68)
        outline = None
        if kind == 'qry' and qlo is not None and qlo <= l and r <= qhi:
            outline = T['blue']
        if kind == 'upd' and tgt is not None and l <= tgt <= r:
            outline = T['pink']
        if o == cur:
            fill = T['yellow']
        cv.rect((X - bw / 2, Y, X + bw / 2, Y + bh), fill=fill, r=8)
        if outline:
            cv.rect((X - bw / 2, Y, X + bw / 2, Y + bh), outline=outline, width=4, r=8)
        tc = T['bg'] if o == cur else T['text']
        v = arr[o]
        cv.text((X, Y + bh * 0.28), f'[{l},{r}]' if l < r else f'数值 {l}', 18, T['bg'] if o == cur else T['muted'], anchor='mm', bold=True)
        cv.text((X, Y + bh * 0.68), v, 30, tc, anchor='mm', bold=True)
    if kind == 'qry':
        cv.text((x0 + 20, y1 - 30), f'蓝框 = 完全落在 [{qlo},{qhi}] 内的节点', 20, T['blue'], bold=True)
    elif kind == 'upd':
        cv.text((x0 + 20, y1 - 30), f'粉框 = 含数值 {tgt} 的节点（从下往上更新）', 20, T['pink'], bold=True)


def _info(S):
    if 'x' not in S or S.get('k') is None:
        return '`f[v]`：以数值 `v` 结尾的最长子序列长度；线段树维护它的区间最大值'
    x, k = S['x'], S['k']
    lo = max(x - k, 1)
    if x == 1:
        return f'`x = 1`：前面没有更小的数 → `f[1] = 1`'
    return f'`x = {x}`：前一个数只能在 `[{lo}, {x - 1}]`（差 ≤ {k}）→ 区间最大值 + 1'


CONFIG = dict(
    num=2407, title='最长递增子序列 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='值域线段树优化 LIS',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2280'],
    code='''
class Solution:
    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        u = max(nums)
        mx = [0] * (4 * u)

        def modify(o: int, l: int, r: int, i: int, val: int) -> None:
            if l == r:
                mx[o] = val
                return
            m = (l + r) // 2
            if i <= m: modify(o * 2, l, m, i, val)
            else: modify(o * 2 + 1, m + 1, r, i, val)
            mx[o] = max(mx[o * 2], mx[o * 2 + 1])

        # 返回区间 [L,R] 内的最大值
        def query(o: int, l: int, r: int, L: int, R: int) -> int:  # L 和 R 在整个递归过程中均不变，将其大写，视作常量
            if L <= l and r <= R: return mx[o]
            res = 0
            m = (l + r) // 2
            if L <= m: res = query(o * 2, l, m, L, R)
            if R > m: res = max(res, query(o * 2 + 1, m + 1, r, L, R))
            return res

        for x in nums:
            if x == 1:
                modify(1, 1, u, 1, 1)
            else:
                res = 1 + query(1, 1, u, max(x - k, 1), x - 1)
                modify(1, 1, u, x, res)
        return mx[1]
''',
    call='Solution().lengthOfLIS([3,1,2,4], 2)',
    expect=3,
    skip=['m = (l + r) // 2', 'res = 0', 'def modify', 'def query', 'if L <= m', 'else: modify', 9, 'if x == 1', 'if l == r'],
    max_steps=160,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=200, hide=('nums',)),
    ],
    watch=[('x', 'x', 'yellow'), ('k', 'k', 'blue'), ('res', 'res', 'green')],
    captions={
        'u = max(nums)': '值域 `[1, {u}]`：线段树的下标是==数值==，不是 `nums` 的下标',
        'mx = [0] * (4 * u)': '`mx[o]`：线段树节点 `o` 管的数值区间里，最长子序列的最大值；先全是 0',
        'for x in nums': lambda S, B, r: (f'依次处理 `x = {S.x}`：' + ('1 前面没有更小的数，自己就是长度 1' if S.x == 1 else '前一个数只能在 `[x−k, x−1]`，要先查区间最大值') if S.get('x') != B.get('x') or S.get('x') is None else '`nums` 都处理完了'),
        'if x == 1': lambda S, B, r: ('`x = 1`：没有比 1 小的数 → 它自己就是长度 1' if S.x == 1 else f'`x = {S.x} > 1`：要先查区间 `[max(x−k,1), x−1]`'),
        'modify(1, 1, u, 1, 1)': '`f[1] = 1`：`mx` 已更新，根节点 `mx[1] = {mx[1]}`',
        'res = 1 + query': lambda S, B, r: f'`f[{S.x}]` 的前一个数在 `[{max(S.x - S.k, 1)}, {S.x - 1}]`：查这段的最大值，再 `+1`',
        'modify(1, 1, u, x, res)': '区间最大值 + 1 → `f[{x}] = {res}`：单点更新，沿路径向上刷新最大值',
        'if L <= l and r <= R': lambda S, B, r: (f'节点 `[{B.l},{B.r}]` ==完全落在== `[{B.L},{B.R}]` 内 → 直接返回 `mx[{B.o}] = {B.mx[B.o]}`' if B.L <= B.l and B.r <= B.R
                                                else f'节点 `[{B.l},{B.r}]` 只有一部分在 `[{B.L},{B.R}]` 内 → 拆成左右两半'),
        'if L <= m': lambda S, B, r: (f'`L = {B.L} <= m = {(B.l + B.r) // 2}`：左半有交集，去左边查' if B.L <= (B.l + B.r) // 2 else '左半没有交集，跳过'),
        'if R > m': lambda S, B, r: (f'`R = {B.R} > m = {(B.l + B.r) // 2}`：右半也有交集，去右边查，两边取 ==max==' if B.R > (B.l + B.r) // 2 else f'`R = {B.R} <= m`：右半没有交集，只用左半'),
        'return res': '这个节点查到的最大值是 `{ret}`，返回给上一层',
        'if l == r': lambda S, B, r: (f'`l = r = {B.l}`：到叶子（数值 {B.l}）了' if B.l == B.r else f'`[{B.l},{B.r}]` 还不是叶子，继续往下'),
        'mx[o] = val': '到叶子（数值 {l}）：`mx[{o}] = {val}`，`f[{l}]` 更新完毕',
        'if i <= m': lambda S, B, r: (f'`i = {B.i} <= m = {B.m}`：数值在左半 → 往左走' if B.i <= B.m else f'`i = {B.i} > m = {B.m}`：数值在右半 → 往右走'),
        'mx[o] = max(mx[o * 2]': '回溯：`mx[{o}]` = 左右孩子的最大值 = =={mx[o]}==',
        'return mx[1]': '根节点就是整个值域的最大值：答案 =={ret}==',
    },
    cards=dict(
        one_liner='用值域线段树把「区间最大值」做到 O(log U)',
        complexity='时间 `O(n log U)`，空间 `O(U)`',
        problem=['找最长==严格递增==子序列，相邻元素差 ==不超过== `k`',
                 '示例：`[4,2,1,4,3,4,5,8,15], k=3` → `5`',
                 '本视频：`[3,1,2,4], k=2` → `3`'],
        quote='当 $j=\\textit{nums}[i]$ 时，我们可以从 $f[i-1][j\']$ 转移过来，这里 $j-k\\le j\'<j$，取最大值。这非常适合用==线段树==计算。',
        quote_src='—— 灵茶山艾府题解',
        before=[dict(heading='为什么二分不行', lines=[
            '300 题的「贪心 + 二分」不管相邻差',
            '本题多了差值 `≤ k`：必须能==查一段值域的最大值==',
            '于是把 `f` 开在值域上，用线段树做区间最值'])],
        idea=['`f[j]`：以数值 `j` 结尾的最长子序列；`j = nums[i]` 时 `f[j] = 1 + max f[j−k..j−1]`',
              '`f` 只依赖上一轮，第一维直接丢掉，线段树本身就是 `f`',
              '查询区间 `[max(x−k,1), x−1]`，更新单点 `x`，答案是根节点的值'],
        summary=['时间 `O(n log U)`，空间 `O(U)`，`U = max(nums)`',
                 '`x == 1` 要单独处理，否则查询区间 `[1, 0]` 为空',
                 '是严格递增：区间右端取 `x−1`，不含 `x` 自己',
                 '线段树大小 `4u`，下标从 1 开始',
                 '视频里的节点值只在更新时变大：`mx[o]` 取左右孩子最大'],
    ),
)

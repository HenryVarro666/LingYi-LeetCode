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


def _lab(v):
    if v is None:
        return None
    return f'×{v[0]} {v[1]}'


def _leafs(t):
    out = []
    def go(nd, l, r):
        if l == r:
            out.append(t._tree[nd][0] if t._tree[nd] else '')
            return
        m = (l + r) // 2
        go(nd * 2, l, m)
        go(nd * 2 + 1, m + 1, r)
    go(1, 0, t._n - 1)
    return out


def _draw(cv, S, B, box, T):
    t = _tr(S)
    if t is None or not hasattr(t, '_n') or not hasattr(t, '_k') or t._tree[1] is None:
        if t is not None and hasattr(t, '_tree') and hasattr(t, '_k') and hasattr(t, '_n'):
            pass
        else:
            cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
            return
    tb = _tr(B)
    old = getattr(tb, '_tree', None) if tb is not None else None
    tree = t._tree
    inn = S['_inner']
    cur = inn.get('node')
    chg = set()
    if old is not None and len(old) == len(tree):
        chg = {i for i in range(len(tree)) if old[i] is not None and tree[i] is not None and (old[i][0], list(old[i][1])) != (tree[i][0], list(tree[i][1]))}
    hl = ()
    if 'ql' in S:
        hl = range(S['ql'], t._n)
    elif 'start' in S and S.get('_line', 0) >= 70:
        hl = range(S['start'], t._n)
    nums = _leafs(t) if tree[1] is not None else None
    _seg(cv, T, box, t._n, lambda nd: _lab(tree[nd]) if nd < len(tree) else None, lambda nd: (nd * 2, nd * 2 + 1),
         cur=(cur,) if cur else (), chg=chg, nums=nums, num_hl=hl,
         title=f'线段树：节点 = ×mul  cnt（上排 = nums % {t._k}，黄 = 查询区间）')


def _info(S):
    t = _tr(S)
    if t is None or not hasattr(t, '_k'):
        return ''
    r = t._tree[1]
    if r is None:
        return f"`k = {t._k}`：`cnt[x]` = 左端点固定时，前缀乘积 mod k 等于 x 的个数"
    return f"根：整段乘积 mod {t._k} = ×{r[0]}，`cnt = {r[1]}`（`cnt[x]` = 前缀乘积 mod {t._k} 为 x 的前缀数）"


CONFIG = dict(
    num=3525, title='求出数组的 X 值 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='线段树（mul + cnt[x]，合并时左 mul 乘右 cnt）',
    tags=['灵神题单·常用数据结构', '难度分 2645'],
    code='''
# 线段树有两个下标，一个是线段树节点的下标，另一个是线段树维护的区间的下标
# 节点的下标：从 1 开始，如果你想改成从 0 开始，需要把左右儿子下标分别改成 node*2+1 和 node*2+2
# 区间的下标：从 0 开始
class SegmentTree:
    def __init__(self, a: List[int], k: int):
        self._n = n = len(a)
        self._k = k
        self._tree = [None] * (2 << (n - 1).bit_length())
        self._build(a, 1, 0, n - 1)

    # 合并信息
    def _merge_data(self, a: Tuple[int, List[int]], b: Tuple[int, List[int]]) -> Tuple[int, List[int]]:
        cnt = a[1].copy()
        left_mul = a[0]
        for rx, c in enumerate(b[1]):
            cnt[left_mul * rx % self._k] += c
        return left_mul * b[0] % self._k, cnt

    def _new_data(self, val: int) -> Tuple[int, List[int]]:
        mul = val % self._k
        cnt = [0] * self._k
        cnt[mul] = 1
        return mul, cnt

    # 合并左右儿子的信息到当前节点
    def _maintain(self, node: int) -> None:
        self._tree[node] = self._merge_data(self._tree[node * 2], self._tree[node * 2 + 1])

    # 用 a 初始化线段树
    # 时间复杂度 O(n)
    def _build(self, a: List[int], node: int, l: int, r: int) -> None:
        if l == r:  # 叶子
            self._tree[node] = self._new_data(a[l])  # 初始化叶节点的值
            return
        m = (l + r) // 2
        self._build(a, node * 2, l, m)  # 初始化左子树
        self._build(a, node * 2 + 1, m + 1, r)  # 初始化右子树
        self._maintain(node)

    def _update(self, node: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:  # 叶子（到达目标）
            self._tree[node] = self._new_data(val)
            return
        m = (l + r) // 2
        if i <= m:  # i 在左子树
            self._update(node * 2, l, m, i, val)
        else:  # i 在右子树
            self._update(node * 2 + 1, m + 1, r, i, val)
        self._maintain(node)

    def _query(self, node: int, l: int, r: int, ql: int, qr: int) -> Tuple[int, List[int]]:
        if ql <= l and r <= qr:  # 当前子树完全在 [ql, qr] 内
            return self._tree[node]
        m = (l + r) // 2
        if qr <= m:  # [ql, qr] 在左子树
            return self._query(node * 2, l, m, ql, qr)
        if ql > m:  # [ql, qr] 在右子树
            return self._query(node * 2 + 1, m + 1, r, ql, qr)
        l_res = self._query(node * 2, l, m, ql, qr)
        r_res = self._query(node * 2 + 1, m + 1, r, ql, qr)
        return self._merge_data(l_res, r_res)

    # 更新 a[i] 为 _new_data(val)
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        self._update(1, 0, self._n - 1, i, val)

    # 返回用 _merge_data 合并所有 a[i] 的计算结果，其中 i 在闭区间 [ql, qr] 中
    # 时间复杂度 O(log n)
    def query(self, ql: int, qr: int) -> Tuple[int, List[int]]:
        return self._query(1, 0, self._n - 1, ql, qr)

class Solution:
    def resultArray(self, nums: List[int], k: int, queries: List[List[int]]) -> List[int]:
        t = SegmentTree(nums, k)
        n = len(nums)
        ans = []
        for index, value, start, x in queries:
            t.update(index, value)
            _, cnt = t.query(start, n - 1)
            ans.append(cnt[x])
        return ans
''',
    call='Solution().resultArray([1, 2, 3, 4], 3, [[2, 2, 0, 2], [3, 3, 2, 0]])',
    expect=[1, 1],
    max_steps=75,
    skip=[41, 44, 46, 48, 49, 43, 53, 66, 76, 77, 75, 6, 7, 8, 9, 32, 35, 36, 37, 38, 20, 21, 22, 23, 34, 13, 14, 15, 16, 27, 54, 55, 57, 58, 71],
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=100),
    ],
    watch=[('ans', 'ans', 'green')],
    captions={
        33: lambda S, B, r: f"叶子 `[{S.l}]`：`nums[{S.l}] % k` = `{S.a[S.l]} % {S.self._k}` = ==`{S.a[S.l] % S.self._k}`==，只有一个前缀 → `cnt[{S.a[S.l] % S.self._k}] = 1`",
        17: lambda S, B, r: (f"合并：左段整体乘积 `left_mul = {S.left_mul}`；右段每个前缀 `rx` 乘上它后落到 `cnt[{S.left_mul}·rx % k]`，再并上左段的 cnt → 节点 mul = `{r[0]}`，`cnt = {r[1]}`"),
        42: '到达叶子：`nums[{i}]` 换成 `{val}`，重建这个叶子的 `(mul, cnt)`',
        45: lambda S, B, r: f'`i = {S.i}` ' + ('≤' if S.i <= S.m else '>') + f' `m = {S.m}`：在' + ('左' if S.i <= S.m else '右') + '半，往那边走，回溯时重新合并',
        78: lambda S, B, r: ('所有查询处理完了' if B.get('index') == S.index and 'value' in B else f"查询 {S.index}：把 `nums[{S.index}]` 改成 `{S.value}`；问从 `start = {S.start}` 起，前缀乘积 mod k 等于 `{S.x}` 的前缀有几个"),
        79: '先单点修改：线段树更新 `O(log n)` 个节点',
        80: '再查询 `[start, n-1]`：左端点固定，右端点往右延伸，合并几个节点得到这段的 `cnt`',
        52: lambda S, B, r: f"节点 `[{S.l},{S.r}]` 在查询 `[{S.ql},{S.qr}]` 内？" + ('==是==，直接返回它的 `(mul, cnt)`' if S.ql <= S.l and S.r <= S.qr else '否，拆成左右两边'),
        81: '`cnt[{x}]` = =={cnt[x]}==：前缀乘积 mod `k` 等于 `{x}` 的前缀数，就是答案',
        82: '每次查询的答案：`{ans}`',
    },
    cards=dict(
        one_liner='区间合并：右半每个前缀要先乘上左半整体的乘积',
        complexity='时间 `O((n + q log n)k)`，空间 `O(nk)`',
        problem=['正整数数组 `nums` 和 `k`（≤ 5）；只能移除后缀，子数组左端点固定为 `start`',
                 '每条查询先 `nums[index] = value`，再数「保留前缀的乘积 mod k 等于 x」的方案数',
                 '示例：`nums=[1,2,3,4,5], k=3, queries=[[2,2,0,2],...]` → 第一问 `2`',
                 '本视频：`[1,2,3,4]`，`k=3`，两条查询 → `[1,1]`'],
        quote='把右半子数组的元素积乘以 leftMul，就得到了左端点为 l，右端点为 m+1,m+2,…,r 的子数组的元素积，从而统计个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左端点固定 → 问题变成「前缀乘积 mod k 等于 x 的前缀个数」；有修改就用线段树',
              '每个节点存 `mul`（整段乘积 mod k）和 `cnt[x]`（左端点在区间首的前缀里，乘积 mod k = x 的个数）',
              '合并：`cnt` = 左 `cnt` + 右 `cnt` 每项乘上左 `mul` 后累加；`mul` = 左 `mul` × 右 `mul` % k',
              '查询 `[start, n-1]` 就是合并若干节点，取 `cnt[x]`'],
        summary=['时间 `O((n + q log n)k)`，空间 `O(nk)`',
                 '易错：合并时是 `left_mul * rx % k` 落到 `cnt` 的哪一格，不是 `rx` 本身',
                 '叶子的 `mul = val % k`，所以数组元素先模 `k` 再相乘',
                 '要先看懂上一题 3524（统计所有子数组），本题左端点固定，更简单'],
    ),
)

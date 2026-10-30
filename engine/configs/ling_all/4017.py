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
    return f"{v[0]} | {v[1]},{v[2]}" + (' ★' if v[4] else '')


def _arr(S):
    for k in ('nums', 'a'):
        v = S.get(k)
        if isinstance(v, list):
            return v
    return None


def _peaks(a):
    return {j for j in range(1, len(a) - 1) if a[j - 1] < a[j] > a[j + 1]}


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
        chg = {i for i in range(len(tree)) if old[i] is not None and tree[i] is not None and list(old[i]) != list(tree[i])}
    a = _arr(S)
    if a is not None and len(a) != t._n:
        a = None
    _seg(cv, T, box, t._n, lambda nd: _lab(tree[nd]) if nd < len(tree) else None, lambda nd: (nd * 2, nd * 2 + 1),
         cur=(cur,) if cur else (), chg=chg, nums=a, num_hl=_peaks(a) if a else (),
         title='线段树：节点 = cnt｜pre,suf（★ = 区间内有峰顶；黄格 = nums 中的峰顶）')


def _info(S):
    t = _tr(S)
    if t is None or not hasattr(t, '_tree') or t._tree[1] is None:
        return ''
    inn = S['_inner']
    if 'a_cnt' in inn and 'b_cnt' in inn:
        return (f"合并 A=`[{inn['a_cnt']}, pre {inn['a_pre']}, suf {inn['a_suf']}, 长 {inn['a_len']}]` 与 B=`[{inn['b_cnt']}, pre {inn['b_pre']}, suf {inn['b_suf']}, 长 {inn['b_len']}]`")
    return f"根节点：整个数组共有 ==`{t._tree[1][0]}`== 个峰值子数组"


CONFIG = dict(
    num=4017, title='数组中的峰值 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='线段树（cnt / pre / suf / len / has）· 只在峰顶变化时更新',
    tags=['灵神题单·常用数据结构'],
    code='''
# 详细注释见 https://leetcode.cn/circle/discuss/mOr1u6/
class SegmentTree:
    def __init__(self, a: list[int]):
        self._n = n = len(a)
        self._tree = [None] * (2 << (n - 1).bit_length())
        self._build(a, 1, 0, n - 1)

    def _merge_data(self, a: list, b: list) -> list:
        a_cnt, a_pre, a_suf, a_len, a_has = a
        b_cnt, b_pre, b_suf, b_len, b_has = b
        cnt = a_cnt + b_cnt + a_len * b_len - a_suf * b_pre
        pre = a_pre if a_has else a_len + b_pre
        suf = b_suf if b_has else b_len + a_suf
        return [cnt, pre, suf, a_len + b_len, a_has or b_has]

    def _maintain(self, node: int) -> None:
        self._tree[node] = self._merge_data(self._tree[node * 2], self._tree[node * 2 + 1])

    def _build(self, a: List[int], node: int, l: int, r: int) -> None:
        if l == r:  # 叶子
            has_peak = 0 < l < self._n - 1 and a[l - 1] < a[l] > a[l + 1]
            self._tree[node] = [0, 1, 1, 1, has_peak]  # 初始化叶节点的值
            return
        m = (l + r) // 2
        self._build(a, node * 2, l, m)  # 初始化左子树
        self._build(a, node * 2 + 1, m + 1, r)  # 初始化右子树
        self._maintain(node)

    def _update(self, node: int, l: int, r: int, i: int) -> None:
        if l == r:  # 叶子（到达目标）
            d = self._tree[node]
            d[-1] = not d[-1]
            return
        m = (l + r) // 2
        if i <= m:  # i 在左子树
            self._update(node * 2, l, m, i)
        else:  # i 在右子树
            self._update(node * 2 + 1, m + 1, r, i)
        self._maintain(node)

    def _query(self, node: int, l: int, r: int, ql: int, qr: int) -> list:
        if ql <= l and r <= qr:  # 当前子树完全在 [ql, qr] 内
            return self._tree[node]
        m = (l + r) // 2
        if qr <= m:  # [ql, qr] 与右子树无交集，仅需递归左子树
            return self._query(node * 2, l, m, ql, qr)
        if ql > m:  # [ql, qr] 与左子树无交集，仅需递归右子树
            return self._query(node * 2 + 1, m + 1, r, ql, qr)
        # [ql, qr] 与左右子树均有交集，分别递归，然后合并结果
        return self._merge_data(self._query(node * 2, l, m, ql, qr), self._query(node * 2 + 1, m + 1, r, ql, qr))

    def update(self, i: int) -> None:
        self._update(1, 0, self._n - 1, i)

    def query(self, ql: int, qr: int) -> int:
        return self._query(1, 0, self._n - 1, ql, qr)[0]

class Solution:
    def countOfPeaks(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        n = len(nums)
        t = SegmentTree(nums)
        ans = []

        for op, i, v in queries:
            if op == 1:
                ans.append(t.query(i, v))
                continue

            if i > 1:
                old_has = nums[i - 2] < nums[i - 1] > nums[i]
                new_has = nums[i - 2] < nums[i - 1] > v
                if new_has != old_has:
                    t.update(i - 1)

            if 0 < i < n - 1:
                old_has = nums[i - 1] < nums[i] > nums[i + 1]
                new_has = nums[i - 1] < v > nums[i + 1]
                if new_has != old_has:
                    t.update(i)

            if i < n - 2:
                old_has = nums[i] < nums[i + 1] > nums[i + 2]
                new_has = v < nums[i + 1] > nums[i + 2]
                if new_has != old_has:
                    t.update(i + 1)

            nums[i] = v

        return ans
''',
    call='Solution().countOfPeaks([1, 3, 2, 4, 1], [[1, 0, 4], [2, 2, 5], [1, 1, 3]])',
    expect=[5, 1],
    max_steps=75,
    skip=['if ql <= l and r <= qr', 'if op == 1', 'n = len(nums)', 'ans = []', 'if i <= m', 'a_cnt, a_pre', 'b_cnt, b_pre', 'pre = a_pre', 'suf = b_suf', 'return [cnt', 'self._tree[node] = self._merge_data', 'self._tree[node] = [0, 1, 1, 1, has_peak]',
          'm = (l + r)', 'if l == r', 'self._build(a, node', 'self._update(node', 'self._query(node', 'self._maintain(node)', 'self._n = n', 'self._tree = [None]', 'self._build(a, 1',
          'return self._merge_data(self._query', 'if qr <= m', 'if ql > m', 'self._update(1, 0', 'return self._query(1', 'return self._tree[node]', 'd = self._tree[node]', 'return'],
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=100),
    ],
    watch=['n', ('ans', 'ans', 'green')],
    captions={
        'n = len(nums)': '`n = len(nums)`：峰顶只可能出现在下标 `1 ~ n-2`（两端没有两个邻居）',
        't = SegmentTree(nums)': '`n = len(nums)`，峰顶只可能在下标 `1 ~ n-2`。建线段树：叶子只记「这个位置是不是峰顶」，合并时算出 `cnt / pre / suf`',
        'has_peak = 0 < l': lambda S, B, r: f"下标 `{S.l}`：" + (f"`{S.a[S.l - 1]} < {S.a[S.l]} > {S.a[S.l + 1]}` → " + ('==是峰顶==' if S.has_peak else '不是峰顶') if 0 < S.l < len(S.a) - 1 else '在两端，不可能是峰顶'),
        'cnt = a_cnt': '横跨 A、B 的子数组共 `A.len × B.len` = `{a_len}×{b_len}` = {a_len*b_len} 个，不含峰顶的有 `A.suf × B.pre` = `{a_suf}×{b_pre}` = {a_suf*b_pre} 个 → `cnt` = =={cnt}==',
        'for op, i, v in queries': lambda S, B, r: ('所有操作处理完了' if B.get('i') == S.i and B.get('op') == S.op and B.get('v') == S.v else (f"操作 `[1, {S.i}, {S.v}]`：查询 `nums[{S.i}..{S.v}]` 里的峰值子数组个数" if S.op == 1 else f"操作 `[2, {S.i}, {S.v}]`：把 `nums[{S.i}]` 改成 `{S.v}`，检查附近三个位置的峰顶有没有变")),
        'if op == 1': lambda S, B, r: ('类型 1：查询 `nums[l..r]` 内峰值子数组的个数' if S.op == 1 else '类型 2：把 `nums[index]` 改成 `val`，要检查附近三个位置的峰顶有没有变'),
        'ans.append(t.query': '查询 `[{i}, {v}]`：把线段树里覆盖这个区间的几个节点合并，`cnt` 就是答案',
        'if ql <= l and r <= qr': lambda S, B, r: f"节点 `[{S.l},{S.r}]` 在查询 `[{S.ql},{S.qr}]` 内？" + ('==是==，直接用它的信息' if S.ql <= S.l and S.r <= S.qr else '否，拆成左右两边再合并'),
        'continue': '这次查询的答案是 `{ans[-1]}`',
        'if i > 1': '修改 `nums[i]` 会影响 `i-1`、`i`、`i+1` 三个位置是否为峰顶，逐个检查；先看 `i-1`',
        70: '位置 `{i-1}` 修改前：`{nums[i-2]} < {nums[i-1]} > {nums[i]}` → ==`{old_has}`==',
        71: '位置 `{i-1}` 修改后：`{nums[i-2]} < {nums[i-1]} > {v}` → ==`{new_has}`==',
        'if 0 < i < n - 1': '再看位置 `i` 本身（要在 `1 ~ n-2` 内）',
        76: '位置 `{i}` 修改前：`{nums[i-1]} < {nums[i]} > {nums[i+1]}` → ==`{old_has}`==',
        77: '位置 `{i}` 修改后：`{nums[i-1]} < {v} > {nums[i+1]}` → ==`{new_has}`==',
        'if i < n - 2': '最后看位置 `i+1`',
        82: '位置 `{i+1}` 修改前：`{nums[i]} < {nums[i+1]} > {nums[i+2]}` → ==`{old_has}`==',
        83: '位置 `{i+1}` 修改后：`{v} < {nums[i+1]} > {nums[i+2]}` → ==`{new_has}`==',
        'if new_has != old_has': lambda S, B, r: ('峰顶状态变了 → 更新这个叶子' if S.new_has != S.old_has else '峰顶状态没变 → 不用动线段树（优化）'),
        'd[-1] = not d[-1]': '叶子的 `has` 取反 → `{d[-1]}`，然后自底向上重新合并 `cnt / pre / suf`',
        'nums[i] = v': '最后把 `nums[{i}]` 写成 `{v}`（判断峰顶要用旧值，所以放在最后）',
        'return ans': '所有类型 1 查询的答案：`{ans}`',
    },
    cards=dict(
        one_liner='区间合并时：横跨 = 总数 − 不含峰顶的（A.suf × B.pre）',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['数组 `nums`，长度 ≥ 3 且内部有「严格比两邻居大」的下标的子数组叫峰值子数组',
                 '操作 `[1, l, r]`：数 `nums[l..r]` 里完全包含的峰值子数组个数；`[2, i, v]`：单点修改',
                 '示例：`nums=[1,3,2,4], queries=[[1,0,3],[2,1,1],[1,0,3]]` → `[2,0]`',
                 '本视频：`[1,3,2,4,1]`，查询 `[0,4]` → `5`；`nums[2]` 改成 `5` 后查 `[1,3]` → `1`'],
        quote='一共有 A.len · B.len 个横跨 A 和 B 的子数组，其中不含峰顶的子数组，左端点有 A.suf 个，右端点有 B.pre 个（注意峰顶必须严格在子数组内部）',
        quote_src='—— 灵茶山艾府题解',
        idea=['分治：答案 = A.cnt + B.cnt + 横跨的个数；横跨的共 `A.len × B.len` 个，减去==不含峰顶==的 `A.suf × B.pre` 个',
              '每个节点维护 `cnt / pre / suf / len / has`，`pre / suf` 是到第一个 / 最后一个峰顶的长度',
              '改一个数只影响 `i-1, i, i+1` 的峰顶；==状态变了才更新线段树==（优化版）'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`',
                 '易错：峰顶必须严格在子数组内部，所以区间两端的下标永远不是叶子里的峰顶（叶子 `has` 为假）',
                 '优化前：每次修改都对三个位置各 `update` 一次；优化后只在 `has` 变化时才翻转叶子',
                 '`nums[i] = v` 放在最后，因为判断旧峰顶要用旧的 `nums`'],
    ),
)

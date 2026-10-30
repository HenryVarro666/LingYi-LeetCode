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
    return None if v is None else f'{v[0]} · {v[1]} · {v[2]}'


def _draw(cv, S, B, box, T):
    t = _tr(S)
    if t is None or not hasattr(t, '_n') or not hasattr(t, '_s'):
        cv.text((box[0] + 18, box[1]), '（还没建树）', 24, T['dim'])
        return
    tb = _tr(B)
    old = getattr(tb, '_tree', None) if tb is not None else None
    tree = t._tree
    cur = S['_inner'].get('node')
    chg = set()
    if old is not None and len(old) == len(tree):
        chg = {i for i in range(len(tree)) if old[i] != tree[i]}
    hl = ()
    if 'i' in S and isinstance(S['i'], int) and 'val' in S['_inner'] or S.get('_line') == 62:
        hl = (S['i'],)
    _seg(cv, T, box, t._n, lambda nd: _lab(tree[nd]) if nd < len(tree) else None, lambda nd: (nd * 2, nd * 2 + 1),
         cur=(cur,) if cur else (), chg=chg, nums=t._s, num_hl=hl,
         title='线段树：每个节点 = (mx 最长段 · pre 最长前缀 · suf 最长后缀)')


def _info(S):
    t = _tr(S)
    if t is None or not hasattr(t, '_s'):
        return ''
    inn = S['_inner']
    if 'same' in inn and 'm' in inn:
        s = t._s
        m, l, r = inn['m'], inn['l'], inn['r']
        return (f"合并 `[{l},{m}]` 与 `[{m + 1},{r}]`：左末尾 `{s[m]}`，右开头 `{s[m + 1]}` → "
                + ('==相同，可以拼接==' if inn['same'] else '==不同，不能拼接=='))
    return f"当前字符串：`{''.join(t._s)}`，根节点 mx = =={t._tree[1][0] if t._tree[1] else '?'}=="


CONFIG = dict(
    num=2213, title='由单个字符重复的最长子字符串', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='分治思想 + 线段树（mx / pre / suf）',
    tags=['灵神题单·常用数据结构', '难度分 2629'],
    code='''
# 详细注释见 https://leetcode.cn/circle/discuss/mOr1u6/
class SegmentTree:
    def __init__(self, s: list[str]):
        self._n = n = len(s)
        self._s = s
        self._tree = [None] * (2 << (n - 1).bit_length())
        self._build(s, 1, 0, n - 1)

    def _maintain(self, node: int, l: int, m: int, r: int) -> None:
        a_mx, a_pre, a_suf = self._tree[node * 2]
        b_mx, b_pre, b_suf = self._tree[node * 2 + 1]
        same = self._s[m] == self._s[m + 1]  # 左区间的最后一个字符 == 右区间的第一个字符
        self._tree[node] = (
            max(a_mx, b_mx, a_suf + b_pre) if same else max(a_mx, b_mx),
            a_pre + b_pre if same and a_pre == m - l + 1 else a_pre,
            a_suf + b_suf if same and b_suf == r - m else b_suf,
        )

    def _build(self, s: List[str], node: int, l: int, r: int) -> None:
        if l == r:  # 叶子
            self._tree[node] = (1, 1, 1)  # 初始化叶节点的值
            return
        m = (l + r) // 2
        self._build(s, node * 2, l, m)  # 初始化左子树
        self._build(s, node * 2 + 1, m + 1, r)  # 初始化右子树
        self._maintain(node, l, m, r)

    def _update(self, node: int, l: int, r: int, i: int, val: str) -> None:
        if l == r:  # 叶子（到达目标）
            self._s[i] = val
            return
        m = (l + r) // 2
        if i <= m:  # i 在左子树
            self._update(node * 2, l, m, i, val)
        else:  # i 在右子树
            self._update(node * 2 + 1, m + 1, r, i, val)
        self._maintain(node, l, m, r)

    def update(self, i: int, val: str) -> None:
        self._update(1, 0, self._n - 1, i, val)

    def query_all(self) -> int:
        return self._tree[1][0]

class Solution:
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        t = SegmentTree(list(s))
        ans = []
        for i, ch in zip(queryIndices, queryCharacters):
            t.update(i, ch)
            ans.append(t.query_all())
        return ans
''',
    call='Solution().longestRepeating("aabbc", "aa", [2, 3])',
    expect=[3, 4],
    max_steps=70,
    skip=[14, 15, 16, 21, 'self._update(1, 0', 'a_mx, a_pre', 'b_mx, b_pre', 'm = (l + r)', 'if l == r', 'self._build(s, node', 'self._update(node', 'self._maintain(node, l, m, r)',
          'self._n = n', 'self._s = s', 'self._tree = [None]', 'self._build(s, 1', 'return self._tree[1][0]', 'return'],
    views=[
        dict(type='text', fn=_info, h=50),
        dict(type='custom', draw=_draw, h=360),
        dict(type='calls', h=100),
    ],
    watch=[('ans', 'ans', 'green')],
    captions={
        't = SegmentTree': '建线段树：叶子都是 `(1,1,1)`，每个内部节点由左右儿子合并出 `mx / pre / suf`',
        'self._tree[node] = (1, 1, 1)': '叶子：一个字符，最长段、最长前缀、最长后缀都是 ==1==',
        'same = ': lambda S, B, r: f"左区间最后一个字符 `{S.self._s[S.m]}` 与右区间第一个字符 `{S.self._s[S.m + 1]}` " + ('==相同==：两段可以拼在一起' if S.same else '==不同==：不能跨过中点拼接'),
        'self._tree[node] = (': lambda S, B, r: (f"合并得到 `(mx, pre, suf)` = `{S.self._tree[S.node]}`：" + (
            f"跨中点的段长 = 左 suf `{S.a_suf}` + 右 pre `{S.b_pre}` = `{S.a_suf + S.b_pre}`，参与 mx 的比较；pre 只在左半全相同时才延伸，suf 同理"
            if S.same else f"不能拼接：mx = max(左 mx, 右 mx) = `{S.self._tree[S.node][0]}`，pre / suf 直接继承左 / 右")),
        'self._s[i] = val': '叶子：把 `s[{i}]` 改成 `{val}`（叶子的 `(1,1,1)` 不变，变的是它和邻居的「是否相同」）',
        'if i <= m': lambda S, B, r: f'`i = {S.i}` ' + ('≤' if S.i <= S.m else '>') + f' `m = {S.m}`：下标在' + ('左' if S.i <= S.m else '右') + '半，只走这一边，回溯时重新合并',
        'for i, ch in zip': lambda S, B, r: ('查询处理完了' if B.get('i') == S.i and 'ch' in B and B.get('ch') == S.ch else f'取下一条查询：把 `s[{S.i}]` 改成 `{S.ch}`'),
        't.update(i, ch)': '单点更新：从叶子到根，只重新合并路径上 `O(log n)` 个节点',
        'ans.append(t.query_all())': '整个字符串的答案就是根节点的 `mx` = =={t._tree[1][0]}==',
        'return ans': '每次修改后的最长段：`{ans}`',
    },
    cards=dict(
        one_liner='能分治的问题，带修改版就上线段树：每个节点存 mx / pre / suf',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['字符串 `s`，`k` 次修改：把 `s[queryIndices[i]]` 改成 `queryCharacters[i]`',
                 '每次修改后，求「只由单个字符重复」的最长子串长度',
                 '示例：`s="babacc"`，改 3 次 → `[3,3,4]`',
                 '本视频：`s="aabbc"`，改 `s[2]`、`s[3]` 为 `a` → `[3,4]`'],
        quote='如果一个问题可以用分治解决，那么这个问题的带修改版本可以用线段树解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想分治：左右两半 A、B 的答案 = max(A 的答案，B 的答案，跨过中点的段)',
              '跨中点的段 = ==A 的最长后缀 + B 的最长前缀==（前提：A 末尾字符 == B 开头字符）',
              '所以每个区间维护 `mx / pre / suf`；`pre` 只有在 A 整段相同且能接上时才延伸到 B',
              '修改一个字符 = 线段树单点更新，回溯重新合并，根的 `mx` 就是答案'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`',
                 '易错：`pre` 延伸要同时满足「左半整段相同」和「中点两侧字符相同」，`suf` 同理',
                 '叶子永远是 `(1,1,1)`，字符变化体现在 `_s` 里，合并时用 `_s[m] == _s[m+1]` 判断',
                 '同类：3777 / 4017 / 3525 / 3165 / 3410 都是「分治 → 线段树」'],
    ),
)

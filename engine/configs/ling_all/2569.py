_NUMS1 = [1, 0, 1, 0]
_NUMS2 = [1, 2, 3, 4]
_QUERIES = [[1, 0, 1], [2, 1, 0], [3, 0, 0], [1, 1, 1], [2, 5, 0], [3, 0, 0]]
_N3 = sum(1 for q in _QUERIES if q[0] == 3)


def _expect():
    a, b, s, out = list(_NUMS1), list(_NUMS2), sum(_NUMS2), []
    for op, l, r in _QUERIES:
        if op == 1:
            for i in range(l, r + 1):
                a[i] ^= 1
        elif op == 2:
            s += l * sum(a)
        else:
            out.append(s)
    return out


def _skeleton(n):
    out = []

    def go(o, l, r, d):
        out.append((o, l, r, d))
        if l < r:
            m = (l + r) // 2
            go(o * 2, l, m, d + 1)
            go(o * 2 + 1, m + 1, r, d + 1)
    go(1, 0, n - 1, 0)
    return out


def _true_leaves(sk, cnt, flip):
    """每个叶子的真实值 = 叶子里存的值 异或 祖先上还没下放的翻转次数；同时给出是否带「待翻转」"""
    res = {}

    def go(o, l, r, par):
        if l == r:
            res[l] = (cnt[o] ^ par, par)
            return
        m = (l + r) // 2
        p2 = par ^ (1 if flip[o] else 0)
        go(o * 2, l, m, p2)
        go(o * 2 + 1, m + 1, r, p2)
    n = max(r for _, _, r, _ in sk) + 1
    go(1, 0, n - 1, 0)
    return res


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S['nums1'])
    cnt, flip = S['cnt1'], S['flip']
    bc, bf = B.get('cnt1', cnt), B.get('flip', flip)
    sk = _skeleton(n)
    maxd = max(d for *_, d in sk) + 1
    cv.text((x0 + 18, y0 + 4), '线段树：每个节点 = 区间里 1 的个数（橙色「翻转」= 整段待翻转，还没下放）', 22, T['muted'], bold=True)
    slot = (x1 - x0 - 40) / n
    bw, bh = min(slot * 0.9, 130), 66
    dy = min(110, (y1 - y0 - 190 - bh) / max(1, maxd - 1))
    cur = S.get('o')
    inner = S.get('_inner', {})
    if 'L' in inner:
        qr = (inner['L'], inner['R'])
    elif S.get('op') == 1 and 'queries' in S and 'l' in S:
        qr = (S['l'], S['r'])
    else:
        qr = None
    pos = {}
    for o, l, r, d in sk:
        pos[o] = (x0 + 20 + (l + r + 1) / 2 * slot, y0 + 48 + d * dy + bh / 2)
    for o, l, r, d in sk:
        if l < r:
            for c in (o * 2, o * 2 + 1):
                cv.line([(pos[o][0], pos[o][1] + bh / 2), (pos[c][0], pos[c][1] - bh / 2)], T['border'], 3)
    for o, l, r, d in sk:
        X, Y = pos[o]
        outline, width = T['border'], 2
        if cnt[o] != bc[o] or flip[o] != bf[o]:
            outline, width = T['yellow'], 4
        if o == cur:
            outline, width = T['blue'], 4
        cv.rect((X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2), fill=(80, 56, 30) if flip[o] else T['panel2'], outline=outline, width=width, r=10)
        cv.text((X - bw / 2 + 8, Y - bh / 2 + 4), f'[{l},{r}]' if l < r else f'[{l}]', 16, T['muted'], mono=True)
        cv.text((X, Y + 8), cnt[o], 28, T['green'], anchor='mm', bold=True)
        if flip[o]:
            cv.text((X + bw / 2 - 6, Y - bh / 2 + 4), '翻转', 17, T['orange'], anchor='ra', bold=True)
    # 真实 nums1
    leaves = _true_leaves(sk, cnt, flip)
    ya = y1 - 64
    cv.text((x0 + 18, ya - 58), '真实的 nums1（叶子里的值 × 祖先上待下放的翻转）', 19, T['muted'], bold=True)
    cw = min(70, (x1 - x0 - 40) / n)
    for k in range(n):
        v, par = leaves[k]
        X = x0 + 20 + (x1 - x0 - 40 - cw * n) / 2 + k * cw
        inq = qr is not None and qr[0] <= k <= qr[1]
        cv.rect((X + 3, ya - 20, X + cw - 3, ya + 20), fill=T['panel2'], outline=T['yellow'] if inq else (T['orange'] if par else T['border']), width=3 if (inq or par) else 2, r=8)
        cv.text((X + cw / 2, ya), v, 26, T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, ya + 32), k, 15, T['dim'], anchor='mt', mono=True)
    if qr is not None:
        cv.text((x1 - 20, ya - 58), f'黄框 = 本次翻转区间 [{qr[0]}, {qr[1]}]', 19, T['yellow'], anchor='ra', bold=True)


def _hint(S, B):
    if 's' not in S:
        return ''
    return f"`nums2` 总和 `s` = =={S['s']}==；`nums1` 里 1 的个数 = ==`{S['cnt1'][1]}`=="


CONFIG = dict(
    num=2569, title='更新数组后处理求和查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='Lazy 线段树 · 区间翻转 + 维护 1 的个数',
    tags=['灵神题单·常用数据结构', '难度分 2398'],
    code='''
class Solution:
    def handleQuery(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        cnt1 = [0] * (2 << n.bit_length())
        flip = [False] * (2 << n.bit_length())

        # 维护区间 1 的个数
        def maintain(o: int) -> None:
            cnt1[o] = cnt1[o * 2] + cnt1[o * 2 + 1]

        # 执行区间反转
        def do(o: int, l: int, r: int) -> None:
            cnt1[o] = r - l + 1 - cnt1[o]
            flip[o] = not flip[o]

        # 初始化线段树   o,l,r=1,0,n-1
        def build(o: int, l: int, r: int) -> None:
            if l == r:
                cnt1[o] = nums1[l]
                return
            m = (l + r) // 2
            build(o * 2, l, m)
            build(o * 2 + 1, m + 1, r)
            maintain(o)

        # 反转区间 [L,R]   o,l,r=1,0,n-1
        def update(o: int, l: int, r: int, L: int, R: int) -> None:
            if L <= l and r <= R:
                do(o, l, r)
                return
            m = (l + r) // 2
            if flip[o]:
                do(o * 2, l, m)
                do(o * 2 + 1, m + 1, r)
                flip[o] = False
            if m >= L:
                update(o * 2, l, m, L, R)
            if m < R:
                update(o * 2 + 1, m + 1, r, L, R)
            maintain(o)

        build(1, 0, n - 1)
        ans = []
        s = sum(nums2)
        for op, l, r in queries:
            if op == 1:
                update(1, 0, n - 1, l, r)
            elif op == 2:
                s += l * cnt1[1]
            else:
                ans.append(s)
        return ans
''',
    call=f'Solution().handleQuery({_NUMS1!r}, {_NUMS2!r}, {_QUERIES!r})',
    expect=_expect(),
    views=[
        dict(type='text', fn=lambda S: (f"当前操作：`{['', '翻转 nums1[' + str(S.get('l')) + '..' + str(S.get('r')) + ']', 's += ' + str(S.get('l')) + ' × cnt1[1]', '记录 s'][S['op']]}`" if 'op' in S and 'queries' in S else '先建树'), h=50) if False else dict(type='text', fn=_hint, h=50),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('o', 'o', 'blue'), ('L', 'L'), ('R', 'R'), ('s', 's', 'green'), ('ans', 'ans', 'green')],
    skip=['n = len(nums1)', 'if l == r', 20, 30, 'm = (l + r) // 2', 'build(o * 2', 'if m >= L', 'if m < R', 'ans = []', 'if op == 1', 'elif op == 2'],
    max_steps=70,
    captions={
        'cnt1 = [0]': '`cnt1[o]`：节点 `o` 管的区间里 1 的个数',
        'flip = [False]': '`flip[o]`：Lazy 标记——这一整段「要翻转，但还没往下传」',
        'build(1, 0, n - 1)': '从根 `[0, {n - 1}]` 开始建树',
        'cnt1[o] = nums1[l]': '叶子 `[{l}]`：`cnt1[{o}] = nums1[{l}]` = =={nums1[l]}==',
        'maintain(o)': '回溯：用左右儿子合并出节点 `{o}` 的 1 的个数',
        'cnt1[o] = cnt1[o * 2] + cnt1[o * 2 + 1]': '节点 `{o}` = 左儿子 `{cnt1[o * 2]}` + 右儿子 `{cnt1[o * 2 + 1]}` = =={cnt1[o]}==',
        's = sum(nums2)': '`s` = `nums2` 的总和 =={s}==。操作 2 只会让 `s` 增加 `p × 1 的个数`，不用真去改 `nums2`',
        'for op, l, r in queries': lambda S, B, r: ('操作都处理完了' if (B.get('op') == 3 and len(B.get('ans') or []) == _N3) else
                                                    f'取下一个操作 `[{S.op}, {S.l}, {S.r}]`：' + {1: f'翻转 `nums1[{S.l}..{S.r}]`', 2: f'`s` 加上 `{S.l} × 1 的个数`', 3: '记录当前 `s`'}[S.op]),
        'update(1, 0, n - 1, l, r)': '操作 1：翻转 `nums1[{B.l}..{B.r}]`，从根节点开始，`update(1, 0, n - 1, l, r)`',
        'if L <= l and r <= R': '节点 `[{l}, {r}]` vs 翻转区间 `[{L}, {R}]` → =={"整段都在区间内：打个翻转标记就停，不往下" if L <= l and r <= R else "只有一部分在区间内：要继续往下"}==',
        'do(o, l, r)': '整段翻转（`do`）：`1` 的个数变成「区间长 − 原个数」，`flip` 取反',
        'cnt1[o] = r - l + 1 - cnt1[o]': '节点 `{o}`（区间长 `{r - l + 1}`）：1 的个数变成 `{r - l + 1} − {B.cnt1[o]}` = =={cnt1[o]}==',
        'flip[o] = not flip[o]': '`flip[{o}]` 取反 → =={flip[o]}==（先不改子孙，用到再下放）',
        'if flip[o]': '节点 `{o}` 有没下放的翻转标记吗？ → =={"有：要先传给两个儿子，再往下" if flip[o] else "没有，可以直接往下"}==',
        'do(o * 2, l, m)': '标记传给左儿子 `[{l}, {m}]`：它整段翻转',
        'do(o * 2 + 1, m + 1, r)': '标记传给右儿子 `[{m + 1}, {r}]`：它整段翻转',
        'flip[o] = False': '标记已传下去，节点 `{o}` 自己的清掉',
        'update(o * 2, l, m, L, R)': '`[{L}, {R}]` 伸进左半 `[{l}, {m}]` → 递归左儿子',
        'update(o * 2 + 1, m + 1, r, L, R)': '`[{L}, {R}]` 伸进右半 `[{m + 1}, {r}]` → 递归右儿子',
        's += l * cnt1[1]': '操作 2：`s += p × 1 的个数` = `{l} × {cnt1[1]}`，`s` = =={s}==',
        'ans.append(s)': '操作 3：把当前总和 `s` = =={s}== 记进答案',
    },
    cards=dict(
        one_liner='操作 2 只需要「1 的个数」：Lazy 线段树维护它，区间翻转打标记',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['`nums1` 是 0/1 数组，`nums2` 是整数数组，三种操作：',
                 '1：翻转 `nums1[l..r]`；2：`nums2[i] += nums1[i] × p`；3：求 `nums2` 的和',
                 '示例：`[1,0,1]`、`[0,0,0]`，操作 `[[1,1,1],[2,1,0],[3,0,0]]` → `[3]`'],
        quote='假设 nums1 中总共有 c 个 1，那么操作 2 相当于把 nums2 的元素和增加了 c·p。所以只需要维护 nums1 中 1 的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums2` 的和 `s` 单独记，操作 2 就是 `s += p × cnt1[1]`',
              '区间翻转用 Lazy 线段树：整段被盖住就只改个数、打 `flip` 标记，不往下',
              '之后要进入这个节点内部时，先把标记传给两个儿子（`flip[o]` 清零）'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`',
                 '翻转后 1 的个数 = 区间长度 − 原来的个数',
                 '往下走之前先下放标记，回来再 `maintain`，顺序别颠倒',
                 '节点数组开 `2 << n.bit_length()`，足够 4n 级的下标',
                 '`s` 用 Python 大整数，不用取模；操作 2 不用真改 `nums2`'],
    ),
)

def _tree_nodes(n):
    """heap 编号的线段树结构：[(o, l, r, depth)]"""
    out = []

    def go(o, l, r, d):
        out.append((o, l, r, d))
        if l < r:
            m = (l + r) // 2
            go(o * 2, l, m, d + 1)
            go(o * 2 + 1, m + 1, r, d + 1)
    go(1, 0, n - 1, 0)
    return out


def _pending(S, B):
    """追踪到的「执行后」状态停在手写 max 里面，赋值那一行还没生效：这里把它补上"""
    t = [list(v) for v in S['t']]
    ln, o = S.get('_line'), B.get('o')
    inner = B.get('_inner', {})
    try:
        if ln in (14, 15, 16, 17) and 'a' in inner:
            a, b = inner['a'], inner['b']
            f = {14: (0, max(a[0] + b[2], a[1] + b[0])), 15: (1, max(a[0] + b[3], a[1] + b[1])),
                 16: (2, max(a[2] + b[2], a[3] + b[0])), 17: (3, max(a[2] + b[3], a[3] + b[1]))}[ln]
            t[o][f[0]] = f[1]
        elif ln == 22:
            t[o][3] = max(B['nums'][B['l']], 0)
        elif ln == 32:
            t[o][3] = max(B['val'], 0)
    except Exception:
        pass
    return t


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    t, n = _pending(S, B), len(S['nums'])
    bt = B.get('t', t)
    nodes = _tree_nodes(n)
    maxd = max(d for _, _, _, d in nodes) + 1
    cv.text((x0 + 18, y0 + 4), '线段树：每个节点存 f00 f01 / f10 f11（黄 = 刚改动）', 24, T['muted'], bold=True)
    slot = (x1 - x0 - 40) / n
    bw = min(slot * 0.92, 150)
    bh = 92
    dy = min(150, (y1 - y0 - 110 - bh) / max(1, maxd - 1))
    cur = S.get('o')
    inner = S.get('_inner', {})
    kids = set()
    if 'a' in inner and cur:
        kids = {cur * 2, cur * 2 + 1}
    pos = {}
    for o, l, r, d in nodes:
        X = x0 + 20 + (l + r + 1) / 2 * slot
        pos[o] = (X, y0 + 78 + d * dy + bh / 2)
    for o, l, r, d in nodes:
        if l < r:
            for c in (o * 2, o * 2 + 1):
                cv.line([(pos[o][0], pos[o][1] + bh / 2), (pos[c][0], pos[c][1] - bh / 2)], T['border'], 3)
    for o, l, r, d in nodes:
        X, Y = pos[o]
        v = t[o]
        changed = list(v) != list(bt[o])
        outline = T['border']
        width = 2
        fill = T['panel2']
        if changed:
            outline, width = T['yellow'], 4
        if o in kids:
            outline, width = T['cyan'], 4
        if o == cur:
            outline, width = T['blue'], 4
        cv.rect((X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2), fill=fill, outline=outline, width=width, r=10)
        cv.text((X, Y - bh / 2 + 4), f'[{l},{r}]' if l < r else f'[{l}]', 17, T['muted'], anchor='mt', mono=True)
        for k, (dx, dyy) in enumerate(((-1, 0), (1, 0), (-1, 1), (1, 1))):
            col = T['green'] if k == 3 else T['text']
            cv.text((X + dx * bw * 0.24, Y - 1 + dyy * 28), v[k], 22, col, anchor='mm', bold=(k == 3))
    if cur:
        X, Y = pos[cur]
        cv.text((X + bw / 2 + 6, Y - bh / 2 - 2), f'o={cur}', 18, T['blue'], anchor='lb', bold=True)
    cv.text((x0 + 18, y1 - 8), '左上 f00　右上 f01　左下 f10　右下 f11（绿，可选可不选）', 19, T['dim'], anchor='lb')


CONFIG = dict(
    num=3165, title='不包含相邻元素的子序列的最大和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='线段树 · 四个值合并',
    tags=['灵神题单·常用数据结构', '难度分 2697'],
    code='''
class Solution:
    def maximumSumSubsequence(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums)
        # 4 个数分别保存 f00, f01, f10, f11
        t = [[0] * 4 for _ in range(2 << n.bit_length())]

        # 手写 max，效率更高
        def max(a: int, b: int) -> int:
            return b if b > a else a

        # 合并左右儿子
        def maintain(o: int):
            a, b = t[o * 2], t[o * 2 + 1]
            t[o][0] = max(a[0] + b[2], a[1] + b[0])
            t[o][1] = max(a[0] + b[3], a[1] + b[1])
            t[o][2] = max(a[2] + b[2], a[3] + b[0])
            t[o][3] = max(a[2] + b[3], a[3] + b[1])

        # 用 nums 初始化线段树
        def build(o: int, l: int, r: int) -> None:
            if l == r:
                t[o][3] = max(nums[l], 0)
                return
            m = (l + r) // 2
            build(o * 2, l, m)
            build(o * 2 + 1, m + 1, r)
            maintain(o)

        # 把 nums[i] 改成 val
        def update(o: int, l: int, r: int, i: int, val: int) -> None:
            if l == r:
                t[o][3] = max(val, 0)
                return
            m = (l + r) // 2
            if i <= m:
                update(o * 2, l, m, i, val)
            else:
                update(o * 2 + 1, m + 1, r, i, val)
            maintain(o)

        build(1, 0, n - 1)

        ans = 0
        for i, x in queries:
            update(1, 0, n - 1, i, x)
            ans += t[1][3]  # 注意 f11 没有任何限制，也就是整个数组的打家劫舍
        return ans % 1_000_000_007
''',
    call='Solution().maximumSumSubsequence([3, 5, 9], [[1, -2], [0, -3]])',
    expect=21,
    views=[
        dict(type='text', fn=lambda S: f"当前查询：`nums[{S['i']}] = {S['x']}`" if 'x' in S else '先用 nums 建树', h=50),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('o', 'o', 'blue'), ('l', 'l'), ('r', 'r'), ('根 f11', 't[1][3]', 'green'), ('ans', 'ans', 'green')],
    skip=['m = (l + r) // 2', 'a, b = t[o * 2]', 'return b if b > a else a', 'if l == r', 23, 33],
    max_steps=52,
    captions={
        'a[0] + b[2]': '合并左 `{B.a}` 右 `{B.b}`。`f00` 首尾都不选：`max(a.f00+b.f10, a.f01+b.f00)` = =={max(B.a[0] + B.b[2], B.a[1] + B.b[0])}==',
        'a[0] + b[3]': '`f01` 首不选、尾随意：`max(a.f00+b.f11, a.f01+b.f01)` = =={max(B.a[0] + B.b[3], B.a[1] + B.b[1])}==',
        'a[2] + b[2]': '`f10` 首随意、尾不选：`max(a.f10+b.f10, a.f11+b.f00)` = =={max(B.a[2] + B.b[2], B.a[3] + B.b[0])}==',
        'a[2] + b[3]': '`f11` 首尾都随意，就是这一段的打家劫舍：`max(a.f10+b.f11, a.f11+b.f01)` = =={max(B.a[2] + B.b[3], B.a[3] + B.b[1])}==',
        'max(nums[l], 0)': '叶子 `[{l}]`：长度为 1，只有 `f11 = max(nums[{l}], 0)` = =={max(nums[l], 0)}==，其余三个为 0',
        'max(val, 0)': '叶子 `[{l}]` 改成 `{val}`：`f11 = max({val}, 0)` = =={max(val, 0)}==（负数不选）',
        'build(o * 2, l, m)': '先建左半 `[{l}, {m}]`',
        'build(o * 2 + 1, m + 1, r)': '再建右半 `[{m + 1}, {r}]`',
        'build(1, 0, n - 1)': '从根节点 `[0, {n - 1}]` 开始分治建树',
        'maintain(o)': '回到节点 `{o}`：左右儿子都算好了，合并出它的四个值',
        'if i <= m': '修改位置 `{i}` 在{"左" if i <= m else "右"}半 `m = {m}` → 只往{"左" if i <= m else "右"}儿子走',
        'update(o * 2, l, m, i, val)': '往左儿子 `[{l}, {m}]` 递归',
        'update(o * 2 + 1, m + 1, r, i, val)': '往右儿子 `[{m + 1}, {r}]` 递归',
        'update(1, 0, n - 1, i, x)': '单点修改：`nums[{i}] = {x}`，只改一条根到叶子的路径',
        'ans += t[1][3]': '根节点 `f11` = =={t[1][3]}== 就是整个数组的打家劫舍 → `ans` = {ans}',
        'return ans %': '答案累加后取模，返回 `{ret}`',
    },
    cards=dict(
        one_liner='带修改的打家劫舍：分治 + 线段树，节点存四个值',
        complexity='时间 `O(n + q log n)`，空间 `O(n)`',
        problem=['数组 `nums`，每次查询先 `nums[pos] = x`，再求不相邻子序列的最大和（可选空）',
                 '所有查询的答案之和，对 `10^9+7` 取模',
                 '示例：`[3,5,9]`，`[[1,-2],[0,-3]]` → `12 + 9 = 21`'],
        quote='把 nums 从中间切开，分成左右两个子数组……万一同时选了 a 的最后一个数和 b 的第一个数，就不满足题目要求了。怎么办？要么不选 a 的最后一个数，要么不选 b 的第一个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['给每段记 4 个值：首尾各自「一定不选 / 可选可不选」，`f00 f01 f10 f11`',
              '合并左右两段时，==中间相邻的两个数至少有一个被禁选==，两种情况取最大',
              '单点修改 = 改一个叶子，再沿路径回溯重新合并，根的 `f11` 就是答案'],
        summary=['时间 `O(n + q log n)`，空间 `O(n)`',
                 '叶子：`f11 = max(x, 0)`，其余三个为 0（空子序列和为 0）',
                 '四个合并式别记混：左段 a 的「尾」配右段 b 的「首」',
                 '最后才取模；`f11` 没有任何限制，就是整个数组的答案',
                 '套路：能分治的题，带修改版本用线段树'],
    ),
)

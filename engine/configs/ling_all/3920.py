def _box(cv, X, Y, w, h, fill, txt, T, size=30, tc=None, outline=None):
    if fill is not None:
        cv.rect((X, Y, X + w, Y + h), fill=fill, r=8, alpha=210)
    if outline is not None:
        cv.rect((X, Y, X + w, Y + h), outline=outline, width=4, r=8)
    cv.text((X + w / 2, Y + h / 2), txt, size, tc or T['text'], anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    W = x1 - x0 - 40
    cand = S.get('envelopes') or S.get('a') or S.get('candidate')
    g = S.get('g') if S.get('g') is not None else S.get('f')
    cur = None
    if cand is not None and S.get('_') is not None:
        d = S.get('h') if S.get('h') is not None else S.get('delta')
        if (S['_'], d) in cand:
            cur = cand.index((S['_'], d))
    # row 1: nums
    cv.text((x0 + 18, y0 + 4), 'nums：值 x 必须 ≤ 下标 i 才可能成为固定点（绿 = 候选，灰 = 不可能）', 22, T['muted'], bold=True)
    cell = min(100, W / n)
    sx = x0 + 20 + (W - cell * n) / 2
    for i, x in enumerate(nums):
        ok = x <= i
        X = sx + i * cell
        _box(cv, X + 3, y0 + 40, cell - 6, 56, T['green'] if ok else (70, 76, 86), x, T, 30, T['bg'] if ok else T['muted'])
        cv.text((X + cell / 2, y0 + 100), f'i={i}', 18, T['dim'], anchor='mt', mono=True)
        if ok:
            cv.text((X + cell / 2, y0 + 124), f'i-x={i - x}', 19, T['cyan'], anchor='mt', bold=True)
    # row 2: candidate pairs
    y2 = y0 + 205
    if cand is not None:
        sorted_now = cand != [(x, i - x) for i, x in enumerate(nums) if x <= i]
        cv.text((x0 + 18, y2 - 34), ('二元组 (x, i-x)：已按 x 升序、i-x 降序排好' if sorted_now else '二元组 (x, i-x)：收集候选'), 22, T['muted'], bold=True)
        m = len(cand)
        c2 = min(120, W / max(m, 1))
        s2 = x0 + 20 + (W - c2 * m) / 2
        for k, (x, d) in enumerate(cand):
            col = None
            fill = (60, 66, 78)
            if cur is not None:
                if k == cur:
                    fill = T['yellow']
                elif k < cur:
                    fill = (90, 98, 112)
            _box(cv, s2 + k * c2 + 3, y2, c2 - 6, 56, fill, f'({x},{d})', T, 24, T['bg'] if cur == k else T['text'])
    # row 3: g
    y3 = y2 + 140
    if g is not None:
        cv.text((x0 + 18, y3 - 34), '末尾表：i-x 的最长非降子序列（第 k 格 = 长度 k+1 的最小结尾）', 22, T['muted'], bold=True)
        gc = 110
        gs = x0 + 20
        for k, v in enumerate(g):
            _box(cv, gs + k * gc + 3, y3, gc - 6, 56, T['green'], v, T, 30, T['bg'])
            cv.text((gs + k * gc + gc / 2, y3 + 60), k, 18, T['dim'], anchor='mt', mono=True)
        for name, c in (('j', T['pink']), ('left', T['blue']), ('right', T['pink']), ('mid', T['yellow'])):
            p = S.get(name)
            if isinstance(p, int) and cur is not None and 0 <= p <= len(g) and (name != 'j' or True):
                X = gs + p * gc + gc / 2
                cv.tri_up(X, y3 + 88, 9, c)
                cv.text((X, y3 + 100), name, 20, c, anchor='mt', bold=True)


CONFIG = dict(
    num=3920, title='删除元素后最大固定点数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='转成 354 题 · 俄罗斯套娃 LIS',
    tags=['灵神题单·动态规划', '难度分 2264'],
    code='''
class Solution:
    # 354. 俄罗斯套娃信封问题
    def maxEnvelopes(self, envelopes: list[tuple[int, int]]) -> int:
        envelopes.sort(key=lambda e: (e[0], -e[1]))

        g = []
        for _, h in envelopes:
            j = bisect_right(g, h)  # 允许 LIS 相邻元素相等
            if j < len(g):
                g[j] = h
            else:
                g.append(h)
        return len(g)

    def maxFixedPoints(self, nums: list[int]) -> int:
        a = [(x, i - x) for i, x in enumerate(nums) if i >= x]
        return self.maxEnvelopes(a)
''',
    call='Solution().maxFixedPoints([1,0,1,2,2,1,4,3])',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=500),
    ],
    watch=[('h', 'h', 'yellow'), ('j', 'j', 'pink'), ('g', 'g', 'green')],
    captions={
        'a = [(x, i - x)': lambda S, B, r: f'只留 `i ≥ x` 的元素，记成 `(x, i-x)`：共 `{len(S.a)}` 个二元组。`i-x` = 要删掉左边几个数才能到下标 `x`',
        'return self.maxEnvelopes': '转成「套娃信封」：`x` 严格递增、`i-x` 非降，求最长的一组',
        'envelopes.sort': '按 `x` 升序；`x` 相同时 ==`i-x` 降序==，这样同一个 `x` 不会被重复选进非降序列',
        'g = []': '`g[k]`：长为 `k+1` 的非降子序列的最小结尾（只看第二维 `i-x`）',
        'for _, h in envelopes': lambda S, B, r: (f'取下一个二元组，`i-x = {S.h}`' if S.get('h') != B.get('h') or S.get('_') != B.get('_') else '二元组都处理完了'),
        'j = bisect_right': lambda S, B, r: f'`bisect_right(g, {S.h})` = `{S.j}`：第一个 ==大于== `{S.h}` 的位置（相等可以接在后面）',
        'if j < len(g)': lambda S, B, r: (f'`{S.j} < {len(S.g)}`：`g` 里有更大的数 → 替换成更小的 `{S.h}`，以后更容易接' if S.j < len(S.g)
                                         else f'`{S.j} = len(g)`：没有比 `{S.h}` 更大的 → 接在末尾，长度 +1'),
        'g[j] = h': '`g[{j}]` 改成 `{h}`，长度不变，但结尾更小：`g = {g}`',
        'g.append(h)': '`g` 增长一位：当前最长 `{len(g)}`，`g = {g}`',
        'return len(g)': '`len(g) = {ret}`：最多保留这么多个固定点',
    },
    cards=dict(
        one_liner='删除 `i-x` 个数让 x 落到下标 x：问题变成套娃信封',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['可任意删除元素，删后剩余元素左移、下标重排',
                 '`nums[i] == i` 的位置叫固定点，求最多能有几个',
                 '本视频：`[1,0,1,2,2,1,4,3]` → `4`'],
        quote='删除 $x = \\textit{nums}[i]$ 左侧的 $i - x$ 个数，就可以让 $x$ 位于下标 $x$，成为固定点。如果 $i<x$，那么 $x$ 无法成为固定点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['固定点的值递增，且左边被删的个数 `i-x` ==非降==（后面的删的包含前面的）',
              '于是 `(x, i-x)` 就是信封：两维都不减，正是 354 题',
              '按 `x` 升序、`i-x` 降序排序后，只需对 `i-x` 求最长非降子序列'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`bisect_right` 允许相等（非降）；换成 `bisect_left` 就变成严格递增了',
                 '排序后选出的二元组原下标一定递增：`x_i + (i-x_i) < x_j + (j-x_j)`',
                 '`i < x` 的元素一开始就丢掉；代码里的 `maxEnvelopes` 是 354 题的原解'],
    ),
)

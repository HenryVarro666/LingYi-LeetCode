def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    strs = S['strs']
    m = len(strs[0])
    f = S.get('f')
    I, J = S.get('i'), S.get('j')
    live = f is not None and I is not None
    cv.text((x0 + 18, y0 + 4), '每一列 = 各行同位置的字母；蓝 = i 列，粉 = j 列，下方是 f 值', 24, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 40) / m)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * m) / 2
    top = y0 + 60
    rh = 64
    ok = None
    if live and J is not None and J < I:
        ok = all(s[J] <= s[I] for s in strs)
    for c in range(m):
        X = sx + c * cell
        col = None
        if live and c == I:
            col = T['blue']
        elif live and J is not None and c == J and J < I:
            col = T['pink']
        if col:
            cv.rect((X + 2, top - 6, X + cell - 2, top + rh * len(strs) + 6), outline=col, width=4, r=8)
        for r, s in enumerate(strs):
            cv.text((X + cell / 2, top + r * rh + rh / 2), s[c], 38, col or T['text'], anchor='mm', bold=True, mono=True)
        yb = top + rh * len(strs) + 22
        if live:
            v = f[c]
            kept = v > 0 and c < I
            fill = T['green'] if kept else (70, 76, 86)
            cv.rect((X + 8, yb, X + cell - 8, yb + 52), fill=fill, r=8, alpha=200)
            cv.text((X + cell / 2, yb + 26), v, 30, T['bg'] if kept else T['muted'], anchor='mm', bold=True)
        cv.text((X + cell / 2, yb + 62), c, 18, T['dim'], anchor='mt', mono=True)
    if ok is not None:
        msg = f'最近一次比较：第 {J} 列 ≤ 第 {I} 列（每行都满足）→ 能接上' if ok else f'最近一次比较：第 {J} 列有行比第 {I} 列大 → 接不上'
        cv.text((x0 + 20, top + rh * len(strs) + 150), msg, 28, T['green'] if ok else T['orange'], bold=True)


CONFIG = dict(
    num=960, title='删列造序 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多行版 LIS · 枚举选哪个',
    tags=['灵神题单·动态规划', '难度分 2247'],
    code='''
class Solution:
    def minDeletionSize(self, strs: List[str]) -> int:
        m = len(strs[0])
        f = [0] * m
        for i in range(m):
            for j in range(i):
                # 如果 f[j] <= f[i]，就不用跑 O(n) 的 all 了
                if f[j] > f[i] and all(s[j] <= s[i] for s in strs):
                    f[i] = f[j]
            f[i] += 1
        return m - max(f)
''',
    call='Solution().minDeletionSize(["babca","bbazb"])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f', 'f', 'green'), ('f[i]', 'f[i]', 'yellow')],
    captions={
        'm = len': '`m = {m}` 列。反过来想：==最多保留几列==，答案 = `m − 最多保留列数`',
        'f = [0] * m': '`f[i]`：保留的列都以第 `i` 列结尾时，最多保留几列',
        'for i in range': lambda S, B, r: (f'枚举结尾列 `i = {S.i}`' if S.i != B.get('i') else '所有列都算完了'),
        'for j in range': lambda S, B, r: ('没有更靠左的列可选' if S.i == 0 else
            (f'枚举倒数第二列 `j = {S.j}`（`j < i`）' if not (S.j == S.i - 1 and B.get('j') == S.i - 1) else f'`j` 枚举完了：左边最长可接 `{S.f[S.i]}` 列，下一步加上自己')),
        'if f[j] > f[i]': lambda S, B, r: (f'`f[{S.j}] = {S.f[S.j]}`，`f[{S.i}] = {S.f[S.i]}`：' +
            ((f'j 更长，且==每一行 s[{S.j}] ≤ s[{S.i}]== → 能接' if all(t[S.j] <= t[S.i] for t in S.strs)
              else f'j 更长，但有一行 s[{S.j}] > s[{S.i}] → ==接不上==')
             if S.f[S.j] > S.f[S.i] else '不比现有的长，==不用跑 all 了==')),
        'f[i] = f[j]': '每一行都 `s[{j}] ≤ s[{i}]`：第 `{i}` 列能接在 `{j}` 后，`f[{i}] = {f[i]}`',
        'f[i] += 1': '把第 `{i}` 列自己算上：`f[{i}] = {f[i]}`（单独一列也是长度 1）',
        'return m - max': '最多保留 `{max(f)}` 列，删 `{m} − {max(f)}` = =={ret}== 列',
    },
    cards=dict(
        one_liner='把「最多保留几列」当作多行版的最长递增子序列',
        complexity='时间 `O(nm^2)`，空间 `O(m)`',
        problem=['`n` 个等长小写字符串，删去若干列，使==每一行==都按字典序（非降）排列',
                 '求最少删几列',
                 '示例：`["babca","bbazb"]` → `3`（留下第 2、3 列）'],
        quote='定义 $f[i]$ 表示每个子序列都以 $i$ 列结尾时，最多保留的列数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每一列当作 LIS 里的一个数；`j` 能接在 `i` 前 ⇔ ==每一行== `s[j] ≤ s[i]`',
              '和 300 题一样枚举倒数第二列 `j`，用 `f[j] + 1` 更新 `f[i]`',
              '代码先取 `max f[j]`，循环后统一 `+1`；`f[j] ≤ f[i]` 时跳过 `all`'],
        summary=['时间 `O(nm^2)`，空间 `O(m)`',
                 '`n = 1` 就是允许相等的 300 题；多行只是把比较换成 `all`',
                 '答案是 `m - max(f)`，不是 `f[m-1]`：结尾列不一定是最后一列',
                 '相等的字母可以保留，所以用 `<=`'],
    ),
)

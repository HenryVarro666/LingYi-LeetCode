def _cell(cv, X, Y, w, h, txt, T, fill=None, color=None, size=24):
    cv.rect((X, Y, X + w, Y + h), fill=fill or T['panel2'], r=8, outline=T['border'])
    cv.text((X + w / 2, Y + h / 2), txt, size, color or T['text'], anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    N0 = 10
    line = S.get('_line')
    phase2 = 'k' in S and (line or 0) >= 15
    # 第一行：s[k] = k(k+1)(k+2)/6
    cv.text((x0 + 18, y0 + 4), '第一次二分：s[k] = k(k+1)(k+2)/6 = k 层堆满需要的盒子数', 22, T['muted'], bold=True)
    cw = min(80, (x1 - x0 - 60) / N0)
    sx = x0 + 30
    ya = y0 + 110
    l, r = S.get('l'), S.get('r')
    for k in range(1, N0 + 1):
        X = sx + (k - 1) * cw
        v = k * (k + 1) * (k + 2) // 6
        fill = None
        if not phase2 and l is not None and l <= k <= r:
            fill = (52, 64, 84)
        if 'k' in S and k == S['k']:
            fill = T['green']
        _cell(cv, X + 3, ya, cw - 6, 56, v, T, fill=fill, color=T['bg'] if 'k' in S and k == S['k'] else None, size=22)
        cv.text((X + cw / 2, ya + 66), f'k={k}', 16, T['dim'], anchor='mt', mono=True)
    if not phase2 and l is not None:
        for name, idx, c in (('l', l, T['blue']), ('r', r, T['pink'])):
            if 1 <= idx <= N0:
                X = sx + (idx - 1) * cw + cw / 2
                dy = 26 if (name == 'r' and l == r) else 0
                cv.tri_up(X, ya + 100, 9, c)
                cv.text((X, ya + 112 + dy), name, 20, c, anchor='mt', bold=True)
        if 'mid' in S and 1 <= S['mid'] <= N0:
            X = sx + (S['mid'] - 1) * cw
            cv.rect((X + 1, ya - 4, X + cw - 1, ya + 60), outline=T['yellow'], width=4, r=10)
    # 第二行：最下层依次是 cnt[k-1]+1.. 的分布
    yb = ya + 200
    cv.text((x0 + 18, yb - 40), '第二次二分：多出的盒子按 1 个、2 个、3 个… 分段增加地面盒子', 22, T['muted'], bold=True)
    if phase2:
        kk = S['k']
        m = kk
        cw2 = min(150, (x1 - x0 - 60) / m)
        l2, r2 = S.get('l'), S.get('r')
        for q in range(1, m + 1):
            X = sx + (q - 1) * cw2
            v = (1 + q) * q // 2
            fill = (52, 64, 84) if l2 is not None and l2 <= q <= r2 else None
            if line is not None and S.get('l') == S.get('r') and False:
                fill = T['green']
            _cell(cv, X + 4, yb + 6, cw2 - 8, 60, f'{v}', T, fill=fill, size=26)
            cv.text((X + cw2 / 2, yb + 76), f'l={q}：累计 {v} 个', 17, T['dim'], anchor='mt')
        if l2 is not None:
            for name, idx, c in (('l', l2, T['blue']), ('r', r2, T['pink'])):
                if 1 <= idx <= m:
                    X = sx + (idx - 1) * cw2 + cw2 / 2
                    dy = 26 if (name == 'r' and l2 == r2) else 0
                    cv.tri_up(X, yb + 118, 9, c)
                    cv.text((X, yb + 130 + dy), name, 20, c, anchor='mt', bold=True)
        if 'mid' in S and 1 <= S['mid'] <= m and l2 is not None:
            X = sx + (S['mid'] - 1) * cw2
            cv.rect((X + 2, yb + 2, X + cw2 - 2, yb + 70), outline=T['yellow'], width=4, r=10)
        cv.text((x0 + 18, yb + 190), f"放满 k-1 = {S['k'] - 1} 层要 {(S['k'] - 1) * S['k'] * (S['k'] + 1) // 6} 个，多出 n = {S['n']} 个", 24, T['cyan'], bold=True)
    else:
        cv.text((x0 + 30, yb + 20), '先找最小的 k，使 s[k] >= n', 24, T['dim'])


CONFIG = dict(
    num=1739, title='放置盒子', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='两次二分 · 找层数再找多出的地面盒子',
    tags=['灵神题单', '难度分 2198'],
    code='''
class Solution(object):
    def minimumBoxes(self, n):

        l = 1
        r = n
        while l < r:
            mid = (l + r) >> 1
            if mid * (mid + 1) * (mid + 2) // 6 < n:
                l = mid + 1
            else:
                r = mid
        
        k = l
        n -= (k - 1) * k * (k + 1) // 6
        l = 1
        r = k
        while l < r:
            mid = (l + r) >> 1
            if (1 + mid) * mid // 2 < n:
                l = mid + 1
            else:
                r = mid
        
        return (k - 1) * k // 2 + l
''',
    call='Solution().minimumBoxes(10)',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=['n', ('l', 'l', 'blue'), ('r', 'r', 'pink'), 'mid', ('k', 'k', 'green')],
    captions={
        'r = n': '`r = n = {r}`，层数不会超过 n',
        'mid = (l + r) >> 1': lambda S, B, r: (f'试第二段下标 `mid = ({S.l} + {S.r}) >> 1 = {S.mid}`：前 {S.mid} 段一共多出 `{(1 + S.mid) * S.mid // 2}` 个地面盒子' if 'k' in S else f'试 `mid = ({S.l} + {S.r}) >> 1 = {S.mid}` 层，堆满要 `s[{S.mid}] = {S.mid * (S.mid + 1) * (S.mid + 2) // 6}` 个'),
        'if mid * (mid + 1)': lambda S, B, r: (f'`s[{S.mid}] = {S.mid * (S.mid + 1) * (S.mid + 2) // 6} < n = {S.n}`：这么多层还堆不满 n 个 → ==层数不够，向右找==' if S.mid * (S.mid + 1) * (S.mid + 2) // 6 < S.n else f'`s[{S.mid}] = {S.mid * (S.mid + 1) * (S.mid + 2) // 6} >= n = {S.n}`：够了 → ==答案在 mid 或更左==，`r = mid`'),
        'l = mid + 1': lambda S, B, r: (f'前 {S.mid} 段还不够 → `l` 移到 {S.l}' if S._line >= 15 else f'`{S.mid}` 层不够 → `l` 移到 {S.l}'),
        'r = mid': lambda S, B, r: (f'前 {S.mid} 段已覆盖，但可能有更小的 → `r` 收到 {S.r}' if S._line >= 15 else f'`{S.mid}` 层已经够了，但可能还有更小的 → `r` 收到 {S.r}'),
        'k = l': '找到最小的 `k = {k}`：n 个盒子落在 `s[k-1]` 到 `s[k]` 的放置过程中',
        'n -= ': '放满 `k-1 = {k-1}` 层用掉 `s[k-1]` 个，还剩 `n` = =={n}== 个要往地面上补',
        'l = 1': lambda S, B, r: ('第二次二分：多出的盒子按 1 个 cnt+1、2 个 cnt+2、3 个 cnt+3… 分段，在 `[1, k]` 里找落在第几段' if 'k' in S else '第一次二分：在 `[1, n]` 里找「n 个盒子最多堆满到第几层」'),
        'r = k': '`r = k = {r}`：最多分 `k` 段',
        'if (1 + mid) * mid // 2 < n': lambda S, B, r: (f'前 {S.mid} 段共 `(1+{S.mid})*{S.mid}//2 = {(1 + S.mid) * S.mid // 2}` 个 `< {S.n}`：==还没覆盖到 → 向右找==' if (1 + S.mid) * S.mid // 2 < S.n else f'前 {S.mid} 段共 `{(1 + S.mid) * S.mid // 2}` 个 `>= {S.n}`：==已覆盖，答案在 mid 或更左==，`r = mid`'),
        'return': '地面盒子数 = `cnt[k-1] + l = {(k-1)*k//2} + {l}` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='先二分出堆满几层，再二分出多出的盒子落在哪一段',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['立方房间里放 `n` 个单位盒子；盒子放在另一个盒子上时，下面那个盒子四个侧面必须有盒子或墙',
                 '求接触地面的盒子最少有几个',
                 '示例：`n=10 → 6`（本视频用它），`n=3 → 3`'],
        quote='看到数据规模就能想到这是一道找规律的题目，但是我在这里只找到了规律，却不知道怎么证明按这个方式摆放是最优的。',
        quote_src='—— yiduobo 题解原文',
        idea=['k 层堆满：`s[k] = k(k+1)(k+2)/6`，用平方和公式推出，二分找最小的 `k`',
              '从 `k-1` 层堆满变到 `k` 层：地面盒子按 1 个 `cnt+1`、2 个 `cnt+2`… 分布',
              '对多出的盒子再二分，答案 = `cnt[k-1] + l`'],
        summary=['时间 `O(log n)`：两次二分，空间 `O(1)`',
                 '二分要找的是「最小的 k 使 s[k] >= n」，所以 `r = mid`，不是 `mid - 1`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神用循环直接累加（`O(n^(1/3))`），这里用二分'],
    ),
)

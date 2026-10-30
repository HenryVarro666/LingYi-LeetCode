def _draw_fruit(get):
    def _draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        fruits, start, k, lo, hi, note = get(S)
        mxp = max(max(f[0] for f in fruits), start + k)
        n = mxp + 1
        cell = min(90, (x1 - x0 - 60) / n)
        sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
        base = y0 + 300
        amt = {p: a for p, a in fruits}
        vmax = max(amt.values())
        sc = 150 / vmax
        cv.text((x0 + 18, y0 + 4), '数轴：柱高 = 该位置水果数（绿 = 本次路线摘到的，框 = 最远能走到的范围）', 22, T['muted'], bold=True)
        if note:
            cv.text((x0 + 18, y0 + 40), note, 24, T['yellow'])
        # reachable range
        a, b = max(start - k, 0), min(start + k, mxp)
        cv.rect((sx + a * cell, base - 190, sx + (b + 1) * cell, base + 4), outline=T['border'], width=2, r=8)
        for p in range(n):
            X = sx + p * cell
            inwin = lo is not None and lo <= p <= hi
            if p in amt:
                h = amt[p] * sc
                cv.rect((X + 6, base - h, X + cell - 6, base), fill=T['green'] if inwin else (110, 118, 130), r=5)
                cv.text((X + cell / 2, base - h - 4), amt[p], 22, T['text'], anchor='mb', bold=True)
            elif inwin:
                cv.rect((X + 6, base - 4, X + cell - 6, base), fill=T['green'], r=2)
            cv.text((X + cell / 2, base + 8), p, 20, T['dim'], anchor='mt', mono=True)
        X = sx + start * cell + cell / 2
        cv.tri_up(X, base + 52, 11, T['yellow'])
        cv.text((X, base + 66), f'start={start}', 22, T['yellow'], anchor='mt', bold=True)
        if lo is not None:
            XL = sx + lo * cell + cell / 2
            XR = sx + hi * cell + cell / 2
            cv.line([(XL, base + 36), (XR, base + 36)], T['green'], 4)
    return _draw


def _get(S):
    fr, st, k = S['fruits'], S['startPos'], S['k']
    if S.get('_line') in (14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27) and 'left' in S and 'right' in S:
        l, r = S['left'], S['right']
        return fr, st, k, l, r, f"这条路线走过 [{l}, {r}]，水果数 = s[{r}] − s[{l - 1}] = {S.get('cnt', '?')}"
    return fr, st, k, None, None, ''


CONFIG = dict(
    num=2106, title='摘水果', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举折返点 + 前缀和',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2062'],
    code='''
class Solution(object):
    def maxTotalFruits(self, fruits, startPos, k):

        n = max(fruits[-1][0], startPos)
        s = [0] * (n + 1)
        for pos, amount in fruits:
            s[pos] = amount
        
        for index in range(1, n + 1):
            s[index] += s[index - 1]
        
        res = 0
        for left in range(max(0, startPos - k), startPos + 1):
            right = max(startPos, min(left + k - (startPos - left), n))
            cnt = s[right]
            if left > 0:
                cnt -= s[left - 1]
            
            res = max(res, cnt)
        
        for right in range(startPos + 1, min(n, startPos + k) + 1):
            left = min(startPos, max(right - (k - (right - startPos)), 0))
            cnt = s[right]
            if left > 0:
                cnt -= s[left - 1]
            
            res = max(res, cnt)
        
        return res
''',
    call='Solution().maxTotalFruits([[1,3],[3,2],[4,5],[6,1],[7,4]], 4, 4)',
    expect=10,
    views=[dict(type='custom', draw=_draw_fruit(_get), h=440),
           dict(type='array', var='s', h=150, label='s：前缀和（s[i] = 位置 0..i 的水果总数）', cell=70,
                pointers={'left': 'blue', 'right': 'pink'}),],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'cnt', ('res', 'res', 'green')],
    skip=['for pos, amount in fruits', 's[pos] = amount', 'for index in range(1, n + 1)', 's[index] += '],
    captions={
        'n = max': '数轴上最远的位置 `n = {n}`（起点也可能更远）',
        's = [0] * (n + 1)': '按位置放水果、做前缀和：`s[i]` = 位置 `0..i` 的总数，区间和 O(1)',
        'res = 0': '`res` 记录最多摘到的水果',
        'for left in range(max': '情况 1：先向左走到 `left = {left}`（花 `{startPos - left}` 步），再尽力向右',
        'right = max(startPos, min(left': lambda S, B, r: f'向左花了 `{S.startPos - S.left}` 步，剩 `{S.k - (S.startPos - S.left)}` 步向右，最远到 `{S.right}`（不能小于起点，也不能超过 n）',
        'cnt = s[right]': '走过的区间是 `[{left}, {right}]`，先取 `s[{right}]` = {cnt}',
        'if left > 0': '区间和 = `s[right] − s[left−1]`',
        'cnt -= s[left - 1]': '减掉 `s[{left - 1}]`，这条路线摘到 `cnt` = =={cnt}==',
        'res = max': '`res = max({B.res}, {cnt}) = {res}`',
        'for right in range(startPos + 1': '情况 2：先向右走到 `right = {right}`（花 `{right - startPos}` 步），再尽力向左',
        'left = min(startPos': lambda S, B, r: f'向右花了 `{S.right - S.startPos}` 步，剩 `{S.k - (S.right - S.startPos)}` 步向左，最远到 `{S.left}`（不能大于起点，也不能小于 0）',
        'return res': '最多摘到 =={res}== 个水果',
    },
    cards=dict(
        one_liner='只有两种走法：先左后右，或先右后左；枚举折返点',
        complexity='时间 `O(n + k)`（n 为坐标范围），空间 `O(n)`',
        problem=['`fruits[i] = [位置, 数量]`，起点 `startPos`，最多走 `k` 步，水果摘完即消失',
                 '求最多摘到多少水果',
                 '本视频：`[[1,3],[3,2],[4,5],[6,1],[7,4]]`，`startPos=4`，`k=4` → `10`'],
        quote='由于摘掉的水果就没了，因此最终只可能有两种走法，即：1、先向左走到某个位置left，然后再从left开始尽力向右走。……2、先向右走到某个位置right，然后再从right开始尽力向左走',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举折返点，剩下的步数全部用来往回走：能到的另一端是确定的',
              '走过的区间 `[left, right]` 里水果数 = 前缀和之差',
              '坐标范围 ≤ 2×10⁵，直接开数组做前缀和，不需要二分'],
        summary=['时间 `O(n + k)`，空间 `O(n)`，`n` 是坐标范围',
                 '易错：另一端要夹在 `[startPos, n]`（或 `[0, startPos]`）里',
                 '`left > 0` 才能减 `s[left-1]`，否则下标越界',
                 '对比灵神：灵神用滑动窗口只扫水果数组；这里按坐标枚举，用前缀和求区间',
                 '示例换成了更小的输入'],
    ),
)

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
    if 'left' not in S or 's' not in S or 'right' not in S:
        return fr, st, k, None, None, ''
    left, s = S['left'], S['s']
    hi, acc = left - 1, 0
    for j in range(left, len(fr)):
        if acc == s:
            break
        acc += fr[j][1]
        hi = j
    if acc != s and S.get('_line') == 11 and left + 1 < len(fr):
        return fr, st, k, fr[left + 1][0], fr[S['right']][0], f"扔掉位置 {fr[left][0]} 后，窗口水果数 s = {s}"
    if acc != s or left >= len(fr) or hi < left:
        return fr, st, k, None, None, f"窗口内水果 s = {s}"
    return fr, st, k, fr[left][0], fr[hi][0], f"窗口位置 [{fr[left][0]}, {fr[hi][0]}]，水果数 s = {s}"


CONFIG = dict(
    num=2106, title='摘水果', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举最右位置 + 滑动窗口',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2062'],
    code='''
class Solution:
    def maxTotalFruits(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        left = bisect_left(fruits, [startPos - k])  # 向左最远能到 fruits[left][0]
        right = bisect_left(fruits, [startPos + 1])  # 位置 <= startPos 的最大下标 + 1
        ans = s = sum(f[1] for f in fruits[left: right])  # 从 fruits[left][0] 到 startPos 的水果数
        # 枚举最右走到 fruits[right][0]
        while right < len(fruits) and fruits[right][0] <= startPos + k:
            s += fruits[right][1]
            while fruits[right][0] * 2 - fruits[left][0] - startPos > k and \\
                  fruits[right][0] - fruits[left][0] * 2 + startPos > k:
                s -= fruits[left][1]  # fruits[left][0] 太远了
                left += 1
            ans = max(ans, s)  # 更新答案最大值
            right += 1  # 继续枚举下一个最右位置
        return ans
''',
    call='Solution().maxTotalFruits([[1,3],[3,2],[4,5],[6,1],[7,4]], 4, 4)',
    expect=10,
    views=[dict(type='custom', draw=_draw_fruit(_get), h=430),
           dict(type='text', h=80, size=26, fn=lambda S: (
               f"先右后左：`{S['fruits'][S['right']][0]}×2 − {S['fruits'][S['left']][0]} − {S['startPos']}` = {S['fruits'][S['right']][0] * 2 - S['fruits'][S['left']][0] - S['startPos']}；"
               f"先左后右：`{S['fruits'][S['right']][0]} − {S['fruits'][S['left']][0]}×2 + {S['startPos']}` = {S['fruits'][S['right']][0] - S['fruits'][S['left']][0] * 2 + S['startPos']}；k = {S['k']}"
               if 'right' in S and 'left' in S and S['right'] < len(S['fruits']) and S.get('_line') in (8, 9, 10, 11, 12) else '步数 = 走到最右 + 折返，取先右后左、先左后右中较小者'))],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'left = bisect_left': '向左最远走 `k = {k}` 步到位置 `{startPos - k}`，`left` = 第一个位置 `>= {startPos - k}` 的水果 = {left}',
        'right = bisect_left': '`right` = 第一个位置 `> startPos` 的水果下标 = {right}：它左边的都在起点或起点左侧',
        'ans = s = sum': '先只向左走：`left..right-1` 的水果都能摘 → `s = ans = {s}`',
        'while right < len': lambda S, B, r: (f'`fruits[{S.right}][0] = {S.fruits[S.right][0]} <= startPos + k = {S.startPos + S.k}`：最右能走到这 → 枚举它' if S.right < len(S.fruits) and S.fruits[S.right][0] <= S.startPos + S.k
                                              else '最右的水果已超出 `startPos + k`（或没有了）→ 结束枚举'),
        's += fruits[right][1]': '把最右位置 `{fruits[right][0]}` 的 `{fruits[right][1]}` 个水果加进窗口：`s = {s}`',
        'while fruits[right][0] * 2': lambda S, B, r: (f'先右后左要走 `{S.fruits[S.right][0] * 2 - S.fruits[S.left][0] - S.startPos}` 步，`<= k = {S.k}`：走得到 → ==左端合法==' if S.fruits[S.right][0] * 2 - S.fruits[S.left][0] - S.startPos <= S.k
                                                      else f'先右后左要走 `{S.fruits[S.right][0] * 2 - S.fruits[S.left][0] - S.startPos}` 步，`> k = {S.k}`：不行，再看先左后右'),
        'fruits[right][0] - fruits[left][0] * 2 + startPos > k': lambda S, B, r: (f'先左后右要走 `{S.fruits[S.right][0] - S.fruits[S.left][0] * 2 + S.startPos}` 步，`> k = {S.k}`：两种走法都不行 → `fruits[left]` 太远，==收缩左端==' if S.fruits[S.right][0] - S.fruits[S.left][0] * 2 + S.startPos > S.k
                                                                              else f'先左后右要走 `{S.fruits[S.right][0] - S.fruits[S.left][0] * 2 + S.startPos}` 步，`<= k = {S.k}`：走得到 → ==左端合法=='),
        's -= fruits[left][1]': '位置 `{fruits[left][0]}` 的 `{fruits[left][1]}` 个水果摘不到了：`s = {s}`',
        'left += 1': '`left` 右移到 {left}',
        'ans = max': '这个窗口的水果都能在 `k` 步内摘完 → `ans = max({B.ans}, {s}) = {ans}`',
        'right += 1': '`right` 右移，枚举下一个最右位置',
        'return ans': '最多摘到 =={ans}== 个水果',
    },
    cards=dict(
        one_liner='走的范围是一段区间：枚举最右端，左端只增不减',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`fruits[i] = [位置, 数量]`，按位置升序；从 `startPos` 出发，最多走 `k` 步，每走到一个位置摘光水果',
                 '求最多摘到的水果总数',
                 '本视频：`[[1,3],[3,2],[4,5],[6,1],[7,4]]`，`startPos=4`，`k=4` → `10`'],
        quote='反复左右移动会白白浪费移动次数，所以最优方案要么先向右再向左，要么先向左再向右。……如果上面两个式子均大于 k，就说明 fruits[left][0] 太远了，无法到达，需要增大 left。',
        quote_src='—— 灵茶山艾府题解',
        idea=['走过的位置必是一段连续区间，枚举它的右端 `right`',
              '步数 = 走到最右 + 折返到最左，==先右后左、先左后右取小==；都超过 `k` 就扔掉 `left`',
              '`right` 变大时 `left` 不会变小 → 滑动窗口'],
        after=[dict(heading='另一种写法', lines=['题解还有「写法二」：把第一个求和循环并进主循环，', '思路相同，只是多了一些无效计算'])],
        summary=['时间 `O(n)`：`left` 总共最多移动 `n` 次；空间 `O(1)`',
                 '先用二分把 `left` 放到 `startPos − k`，`right` 放到起点右侧第一个',
                 '易错：步数公式要两个都 `> k` 才收缩；`right` 必须 `<= startPos + k`',
                 '本视频的示例换成更能看到收缩的小例子'],
    ),
)

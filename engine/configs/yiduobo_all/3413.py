def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    coins = S['coins']
    lo = min(t[0] for t in coins)
    hi = max(t[1] for t in coins)
    n = hi - lo + 1
    cell = min(86, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys, ch = y0 + 110, 96
    back = 'start' in S
    cv.text((x0 + 18, y0 + 4), ('第二趟（倒序）：选的区间终点对齐 coins[index] 的右端' if back else
            '第一趟（正序）：选的区间起点对齐 coins[index] 的左端') + '，粉框 = 选中的 k 个袋子', 22, T['muted'], bold=True)
    colors = [T['blue'], T['green'], T['purple'], T['cyan'], T['orange']]
    for ti, (a, b, c) in enumerate(coins):
        for p in range(a, b + 1):
            X = sx + (p - lo) * cell
            cv.rect((X + 2, ys, X + cell - 2, ys + ch), fill=colors[ti % 5], alpha=200, r=8)
            cv.text((X + cell / 2, ys + ch / 2), c, 32, T['bg'], anchor='mm', bold=True)
    for p in range(lo, hi + 1):
        X = sx + (p - lo) * cell
        cv.rect((X + 2, ys, X + cell - 2, ys + ch), outline=T['border'], r=8)
        cv.text((X + cell / 2, ys + ch + 8), p, 18, T['dim'], anchor='mt', mono=True)
    if 'index' in S and ('end' in S or back):
        if back:
            a, b = S['start'], coins[S['index']][1]
        else:
            a, b = coins[S['index']][0], S['end']
        a2, b2 = max(a, lo), min(b, hi)
        cv.rect((sx + (a2 - lo) * cell - 3, ys - 8, sx + (b2 - lo + 1) * cell + 3, ys + ch + 8), outline=T['pink'], width=5, r=10)
        cv.text((sx + (a2 - lo) * cell, ys - 14), f'区间 [{a}, {b}]', 22, T['pink'], anchor='lb', bold=True)
        p = S['p']
        if 0 <= p < len(coins):
            L = coins[p]
            cv.line([(sx + (L[0] - lo) * cell + 4, ys + ch + 44), (sx + (L[1] - lo + 1) * cell - 4, ys + ch + 44)], T['yellow'], 6)
            cv.text(((sx + (L[0] - lo) * cell + sx + (L[1] - lo + 1) * cell) / 2, ys + ch + 52), 'p 所在区间', 20, T['yellow'], anchor='mt', bold=True)


def _txt(S, B):
    if 'cnt' not in S or 'index' not in S:
        return '对齐某个区间的端点，用窗口算出能收集的硬币'
    return f"当前区间可收集 `cnt = {S['cnt']}`，最大 `res` =={S['res']}=="


CONFIG = dict(
    num=3413, title='收集连续 K 个袋子可以获得的最多硬币数量', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='端点对齐 · 正倒各扫一趟',
    tags=['不定长滑动窗口', '难度分 2374'],
    code='''
class Solution(object):
    def maximumCoins(self, coins, k):
        
        n = len(coins)
        coins.sort()
        res = 0

        p = 0
        cnt = 0
        for index in range(n):
            end = coins[index][0] + k - 1
            while p < n and end >= coins[p][1]:
                cnt += (coins[p][1] - coins[p][0] + 1) * coins[p][2]
                p += 1
            
            if p < n and end >= coins[p][0]:
                cnt += (end - coins[p][0] + 1) * coins[p][2]
            
            res = max(res, cnt)

            if index == p:
                cnt -= (end - coins[index][0] + 1) * coins[index][2]
                p += 1
            else:
                cnt -= (coins[index][1] - coins[index][0] + 1) * coins[index][2]
                if p < n and end >= coins[p][0]:
                    cnt -= (end - coins[p][0] + 1) * coins[p][2]

        p = n - 1
        cnt = 0
        for index in range(n - 1, -1, -1):
            start = coins[index][1] - k + 1
            while p >= 0 and start <= coins[p][0]:
                cnt += (coins[p][1] - coins[p][0] + 1) * coins[p][2]
                p -= 1
            
            if p >= 0 and start <= coins[p][1]:
                cnt += (coins[p][1] - start + 1) * coins[p][2]
            
            res = max(res, cnt)

            if index == p:
                cnt -= (coins[index][1] - start + 1) * coins[index][2]
                p -= 1
            else:
                cnt -= (coins[index][1] - coins[index][0] + 1) * coins[index][2]
                if p >= 0 and start <= coins[p][1]:
                    cnt -= (coins[p][1] - start + 1) * coins[p][2]

        return res
''',
    call='Solution().maximumCoins([[8,10,1],[1,3,2],[5,6,4]], 4)',
    expect=10,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', h=70, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'yellow'), ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'coins.sort()': '先排序，区间从左到右排好',
        'end = coins[index][0]': '起点对齐 `l = {coins[index][0]}`，长 `{k}` → 终点 `end = {end}`',
        'while p < n and end >= coins[p][1]': '`end = {end}` 与 `coins[p]` 右端比：{"能完整盖住这一段，吃进窗口" if (p < n and end >= coins[p][1]) else "盖不全了，p 停下"}',
        'cnt += (coins[p][1] - coins[p][0] + 1)': '整段 `[{coins[p][0]}, {coins[p][1]}]` 进窗口：`cnt` → {cnt}',
        'p += 1': '`p` 右移到 {p}',
        16: '`end` 可能只伸进 `coins[p]` 的一部分：{"是，要算上这半段" if (p < n and end >= coins[p][0]) else "没有，不用算"}',
        'cnt += (end - coins[p][0] + 1)': '部分覆盖：加 `({end} - {coins[p][0]} + 1) × {coins[p][2]}` → `cnt = {cnt}`',
        'res = max(res, cnt)': '`res = max({B.res}, {cnt}) = {res}`',
        'if index == p': '`index == p`？{"窗口里只有 index 自己（部分覆盖）" if index == p else "窗口里还有别的区间"}',
        'cnt -= (end - coins[index][0] + 1) * coins[index][2]': '窗口起点要右移：去掉 `index` 这一段已算的部分 → `cnt = {cnt}`',
        'cnt -= (coins[index][1] - coins[index][0] + 1) * coins[index][2]': '起点离开 `index`：减掉它整段 → `cnt = {cnt}`',
        'cnt -= (end - coins[p][0] + 1) * coins[p][2]': '部分覆盖 `coins[p]` 那块下次会重算，先去掉避免重复 → `cnt = {cnt}`',
        'p = n - 1': '第二趟：倒序，终点对齐每个 `r`，起点往左扩',
        'start = coins[index][1] - k + 1': '终点对齐 `r = {coins[index][1]}`，长 `{k}` → 起点 `start = {start}`',
        'while p >= 0 and start <= coins[p][0]': '`start = {start}` 与 `coins[p]` 左端比：{"能完整盖住，吃进窗口" if (p >= 0 and start <= coins[p][0]) else "盖不全了，p 停下"}',
        'cnt += (coins[p][1] - coins[p][0] + 1)': '整段 `[{coins[p][0]}, {coins[p][1]}]` 进窗口：`cnt` → {cnt}',
        'p -= 1': '`p` 左移到 {p}',
        37: '`start` 可能只落在 `coins[p]` 中间：{"是，要算上右半段" if (p >= 0 and start <= coins[p][1]) else "没有，不用算"}',
        'cnt += (coins[p][1] - start + 1)': '部分覆盖：加 `({coins[p][1]} - {start} + 1) × {coins[p][2]}` → `cnt = {cnt}`',
        'cnt -= (coins[index][1] - start + 1)': '终点要左移：去掉 `index` 已算的部分 → `cnt = {cnt}`',
        'cnt -= (coins[p][1] - start + 1)': '部分覆盖那块下次会重算，先去掉 → `cnt = {cnt}`',
        26: '起点移走后，窗口末端那块部分覆盖的收益 {"还留在 cnt 里" if (p < n and end >= coins[p][0]) else "不存在，无需处理"}',
        47: '终点移走后，窗口起点那块部分覆盖的收益 {"还留在 cnt 里" if (p >= 0 and start <= coins[p][1]) else "不存在，无需处理"}',
        'for index in range(n):': lambda S, B, r: ('正序枚举完毕' if ('index' in B and B.index == S.index) else f'正序枚举：`index = {S.index}`，让选出的区间起点对齐 `coins[{S.index}]` 的左端'),
        'for index in range(n - 1, -1, -1)': lambda S, B, r: ('倒序枚举完毕' if (S.index == 0 and B.index == 0) else f'倒序枚举：`index = {S.index}`，让选出的区间终点对齐 `coins[{S.index}]` 的右端'),
        'return res': '正倒两趟的最大值：`{res}`',
    },
    cards=dict(
        one_liner='最优区间一定贴着某个区间的起点或终点',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数轴每个整点一个袋子，`[l, r, c]` 表示 `l..r` 每袋有 `c` 枚硬币',
                 '区间互不重叠，连续收集 `k` 个袋子，求最多硬币数',
                 '示例：`[[8,10,1],[1,3,2],[5,6,4]], k = 4` → `10`'],
        quote='选出来最终区间，要么起点与某个coins[i]的起点对齐，要么终点与某个coins[i]的终点对齐。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间两端都悬在外面时：往 c 更大的那一侧平移一定不亏',
              '所以只试：起点对齐每个 `l`，终点对齐每个 `r`',
              '正序一趟枚举 `l`，倒序一趟枚举 `r`，窗口用指针 `p` 维护'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '窗口末端可能只盖住某段的一部分，要单独算，离开时再扣掉',
                 '第一趟是起点对齐，第二趟是终点对齐，两趟都不能少',
                 '对比灵神：灵神把坐标取负复用同一份代码，yiduobo 写成对称的两段'],
    ),
)

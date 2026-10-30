_ST = {'fresh_start': False, 'fresh_end': False}


def _for_start(S, B):
    _ST['fresh_start'] = True
    _ST['fresh_end'] = True
    if 'start' in B and S.start == B.start:
        return '所有起点都枚举完了'
    return f'枚举起点 `start = {S.start}`'


def _for_end(S, B):
    if _ST['fresh_end']:
        _ST['fresh_end'] = False
    elif S.end == B.end:
        return f'`end` 已到末尾，这个起点枚举完了'
    return f'枚举终点 `end = {S.end}`：子数组 `{S.nums[S.start:S.end+1]}`'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums, p2 = S['nums'], S['p2']
    n = len(nums)
    cell = min(120, (x1 - x0 - 80) / n)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    ys = y0 + 56
    ch = cell * 0.7
    st, en = S.get('start'), S.get('end')
    cv.text((x0 + 18, y0 + 4), 'nums（下方 = 质因子 2 的个数 p2，蓝框 = 当前子数组）', 22, T['muted'], bold=True)
    for t, v in enumerate(nums):
        X = sx + t * cell
        inside = st is not None and en is not None and st <= t <= en
        mi = S.get('mi')
        is_min = inside and mi is not None and p2[t] == mi
        fill = T['yellow'] if is_min else (T['panel2'] if inside else T['panel'])
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['blue'] if inside else T['border'], width=4 if inside else 1)
        cv.text((X + cell / 2, ys + ch / 2), v, 34, T['bg'] if is_min else (T['text'] if inside else T['dim']), anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 8), f'p2={p2[t]}', 20, T['dim'], anchor='mt', mono=True)
        cv.text((X + cell / 2, ys + ch + 34), t, 18, T['dim'], anchor='mt', mono=True)
    if st is not None and en is not None:
        for name, idx, c, dy in (('start', st, T['blue'], 0), ('end', en, T['pink'], 28 if st == en else 0)):
            X = sx + idx * cell + cell / 2
            cv.tri_up(X, ys + ch + 66, 10, c)
            cv.text((X, ys + ch + 80 + dy), name, 22, c, anchor='mt', bold=True)
    yb = ys + ch + 150
    if st is None or en is None or 'g' not in S or 'mi' not in S:
        return
    mi, cnt, g = S['mi'], S['mi_cnt'], S['g']
    k = S['k']
    ok = cnt <= k
    L = en - st + 1
    cv.text((x0 + 18, yb), '黄色 = 子数组里 p2 最小的数（只有把它们都翻倍，GCD 的 2 才会多一个）', 22, T['muted'], bold=True)
    lines = [
        (f'去掉 2 之后的 GCD 部分 × 2 的幂：当前 g = {g}（它已经含 2^{mi} 这一项）', T['text']),
        (f'p2 最小值 mi = {mi}，出现 mi_cnt = {cnt} 次，k = {k}', T['yellow']),
        (f'mi_cnt {"≤" if ok else ">"} k → ' + ('可以全部翻倍，g 变成 2g' if ok else '次数不够，g 不变'), T['green'] if ok else T['orange']),
        (f'分数 = {g * (2 if ok else 1)} × {L} = {g * (2 if ok else 1) * L}', T['cyan']),
    ]
    for t, (s_, c) in enumerate(lines):
        cv.text((x0 + 30, yb + 44 + t * 44), s_, 27, c, bold=True)


CONFIG = dict(
    num=3574, title='最大子数组 GCD 分数', difficulty='Hard', category='位运算',
    author='yiduobo', technique='暴力枚举子数组 · 质因子 2 的个数',
    tags=['灵神题单·位运算', '灵神题单·数学算法', '难度分 2300'],
    code='''
class Solution(object):
    def maxGCDScore(self, nums, k):
        
        n = len(nums)
        p2 = [0] * n
        for index, v in enumerate(nums):
            while v % 2 == 0:
                p2[index] += 1
                v //= 2
        
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        res = 0
        for start in range(n):
            for end in range(start, n):
                if start == end:
                    g = nums[end]
                    mi = p2[end]
                    mi_cnt = 1
                else:
                    g = gcd(g, nums[end])
                    if p2[end] < mi:
                        mi = p2[end]
                        mi_cnt = 0
                    if p2[end] == mi:
                        mi_cnt += 1
                
                if mi_cnt <= k:
                    res = max(res, g * 2 * (end - start + 1))
                else:
                    res = max(res, g * (end - start + 1))
        
        return res
''',
    call='Solution().maxGCDScore([4,4,6], 1)',
    expect=12,
    skip=['while v % 2', 'p2[index] += 1', 'v //= 2', 'x, y = y', 'while y', 'return x', 'def gcd', 'n = len', 'p2 = [0]', 'for index, v', 19, 20, 21, 26, 27, 29],
    max_steps=90,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink'), ('g', 'g', 'cyan'), ('mi', 'mi', 'yellow'), ('mi_cnt', 'mi_cnt', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': lambda S, B, r: f'先把每个数的质因子 2 的个数算好：`p2 = {S.p2}`。翻倍 = 给某个数的 p2 加 1。`res = 0`',
        'for start in range': lambda S, B, r: _for_start(S, B),
        'for end in range': lambda S, B, r: _for_end(S, B),
        'if start == end': lambda S, B, r: ('子数组只有一个数：从头开始记录' if S.start == S.end else '子数组变长了：在上一轮的基础上接着算'),
        'mi_cnt = 1': '只有 `nums[{end}]`：`g = {g}`；`mi` = 最小的 `p2` = `{mi}`，`mi_cnt` = 取到最小值的个数 = `1`',
        'g = gcd(g, nums[end])': '加入 `nums[{end}] = {nums[end]}`：`g = gcd({B.g}, {nums[end]}) = {g}`',
        'if p2[end] < mi': lambda S, B, r: (f'`p2[{S.end}] = {S.p2[S.end]} < mi = {S.mi}`：出现更小的 2 的个数 → ==最小值换人==：`mi = {S.p2[S.end]}`，计数从 0 重来'
                                            if S.p2[S.end] < B.mi else f'`p2[{S.end}] = {S.p2[S.end]}` ≥ `mi = {S.mi}`：最小值不变'),
        'if p2[end] == mi': lambda S, B, r: (f'`p2[{S.end}] = {S.p2[S.end]}` == `mi = {S.mi}`：它也是最小的之一 → 计数 +1'
                                             if S.p2[S.end] == S.mi else f'`p2[{S.end}] = {S.p2[S.end]}` ≠ `mi = {S.mi}`：不是最小的，不用翻倍它'),
        'if mi_cnt <= k': lambda S, B, r: (f'`mi_cnt = {S.mi_cnt}` ≤ `k = {S.k}`：把这些 p2 最小的数都翻倍 → GCD 的 2 的次数 +1，==g 变成 2g=='
                                           if S.mi_cnt <= S.k else f'`mi_cnt = {S.mi_cnt}` > `k = {S.k}`：翻倍次数不够，==g 保持不变=='),
        'g * 2 * (end - start + 1)': '分数 = `2g × 长度` = `{g*2} × {end - start + 1}` = {g*2*(end-start+1)} → `res = {res}`',
        'res = max(res, g * (end': '分数 = `g × 长度` = `{g} × {end - start + 1}` = {g*(end-start+1)} → `res = {res}`',
        'return res': '最大分数 `{res}`',
    },
    cards=dict(
        one_liner='GCD 只多一个因子 2：看子数组里 2 最少的数有几个',
        complexity='时间 `O(n²)`（GCD 均摊），空间 `O(n)`',
        problem=['每个数最多翻倍一次，最多翻 `k` 次；子数组分数 = `GCD × 长度`',
                 '求翻倍后能得到的最大分数',
                 '示例：`[2,4]`，`k=1` → `8`；本视频：`[4,4,6]`，`k=1` → `12`'],
        quote='翻倍实际上就是新增了一个质因子2，因此在这里可以先将数组中每个元素所有的质因子2都提取出来。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p2[i]` = `nums[i]` 里质因子 2 的个数；子数组 GCD 的 2 的次数 = `min(p2)`',
              '翻倍 = 给某个 `p2` 加 1；要让最小值变大，必须把==所有==取到最小值的数都翻倍',
              '只需记 `mi` 和 `mi_cnt`：`mi_cnt ≤ k` 就用 `2g`，否则用 `g`；`n ≤ 1500`，枚举所有子数组'],
        summary=['时间 `O(n²)`（`end` 右移时 `g` 每次增量 gcd），空间 `O(n)`',
                 '`mi` 变小时 `mi_cnt` 要重置为 0 再在下一个 `if` 里加 1',
                 '原文就是 Python 3 可运行的写法（`//=` 本来就是整除），未改动',
                 '对比灵神：灵神方法一同样 `O(n²)` 暴力、用 lowbit 代替 p2；方法二用 LogTrick 做到 `O(n log U)`'],
    ),
)

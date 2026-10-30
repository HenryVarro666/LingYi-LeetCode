def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    cell = min(110, (x1 - x0 - 80) / n)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    i = S.get('i')
    ys = y0 + 56
    ch = cell * 0.7
    cv.text((x0 + 18, y0 + 4), 'nums（下方小字 = lowbit，即因子 2 的乘积）', 22, T['muted'], bold=True)
    for t, v in enumerate(nums):
        X = sx + t * cell
        live = i is not None and t <= i
        fill = T['panel2'] if live else T['panel']
        if t == i:
            fill = T['blue']
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), v, 34, T['bg'] if t == i else (T['text'] if live else T['dim']), anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 6), f'lb={v & -v}', 18, T['dim'], anchor='mt', mono=True)
        cv.text((X + cell / 2, ys + ch + 30), t, 18, T['dim'], anchor='mt', mono=True)
    if i is not None:
        cv.tri_up(sx + i * cell + cell / 2, ys + ch + 60, 10, T['blue'])
        cv.text((sx + i * cell + cell / 2, ys + ch + 66), 'i', 24, T['blue'], anchor='mt', bold=True)
    iv = S.get('intervals')
    if iv is None or i is None:
        return
    yb = ys + ch + 140
    cv.text((x0 + 18, yb - 8), '以 i 为右端点：左端点所在区间 (l, r] → gcd 都等于 g', 22, T['muted'], bold=True)
    cur = (S.get('g'), S.get('l'), S.get('r')) if 'g' in S and 'l' in S else None
    cols = ['cyan', 'orange', 'purple', 'green', 'pink']
    rh = 62
    for k, (g, l, r) in enumerate(iv):
        y = yb + 36 + k * (rh + 10)
        c = T[cols[k % len(cols)]]
        is_cur = cur is not None and cur == (g, l, r)
        a, b = sx + (l + 1) * cell, sx + (r + 1) * cell
        cv.rect((a + 4, y, b - 4, y + rh), fill=c, alpha=235 if is_cur else 120, r=10,
                outline=T['yellow'] if is_cur else None, width=5)
        cv.text(((a + b) / 2, y + rh / 2), f'g = {g}', 28, T['bg'] if is_cur else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((sx - 10, y + rh / 2), f'({l},{r}]', 20, T['muted'], anchor='rm', mono=True)


CONFIG = dict(
    num=3574, title='最大子数组 GCD 分数', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='LogTrick · GCD 区间 + lowbit 位置表',
    tags=['灵神题单·位运算', '灵神题单·数学算法', '难度分 2300'],
    code='''
class Solution:
    def maxGCDScore(self, nums: List[int], k: int) -> int:
        lowbit_pos = defaultdict(list)

        ans = 0
        intervals = []  # 每个元素是一个三元组 (g, l, r)，表示区间 (l, r] 的 GCD 为 g
        for i, x in enumerate(nums):
            lowbit_pos[x & -x].append(i)

            # 更新已有区间的 GCD
            for p in intervals:
                p[0] = gcd(p[0], x)
            # 添加新元素作为新区间
            intervals.append([x, i - 1, i])

            # 去重（合并 g 相同的区间）
            idx = 1
            for j in range(1, len(intervals)):
                if intervals[j][0] != intervals[j - 1][0]:
                    intervals[idx] = intervals[j]
                    idx += 1
                else:
                    intervals[idx - 1][2] = intervals[j][2]
            del intervals[idx:]

            # 此时我们将区间 [0,i] 划分成了 len(intervals) 个左开右闭区间
            # 对于 intervals 中的 (l,r]，对于任意 j∈(l,r]，gcd(区间[j,i]) 的计算结果均为 g
            for g, l, r in intervals:
                # 不做任何操作
                ans = max(ans, g * (i - l))
                # 看看能否乘 2
                pos = lowbit_pos[g & -g]
                min_l = max(l, pos[-k - 1]) if len(pos) > k else l  # 注意这里把 min_l 减少了 1
                if min_l < r:  # 可以乘 2
                    ans = max(ans, g * 2 * (i - min_l))

        return ans
''',
    call='Solution().maxGCDScore([8,4,4,6], 1)',
    expect=16,
    skip=['intervals[idx] = intervals[j]', 'idx += 1', 'for p in intervals', 'del intervals', 'idx = 1', 'lowbit_pos = defaultdict', 'ans = 0', 18, 28],
    max_steps=95,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('i', 'i', 'blue'), ('k', 'k'), ('g', 'g', 'cyan'), ('l', 'l'), ('r', 'r'), ('ans', 'ans', 'green')],
    captions={
        'lowbit_pos[x & -x].append': '`x = {x}` 的 lowbit = `{x & -x}`：把下标 `{i}` 记进 `lowbit_pos[{x & -x}]`，之后查“最近的 k 个同 lowbit 的数”',
        'p[0] = gcd': '已有区间的 GCD 都和新来的 `x = {x}` 取 gcd（只会变小或不变）',
        'intervals.append': '`x` 自己成为新区间 `({i-1}, {i}]`，GCD = `{x}`',
        'if intervals[j][0] != intervals[j - 1][0]': lambda S, B, r: (
            f'第 `{S.j}` 个区间 g=`{S.intervals[S.j][0]}`，前一个 g=`{S.intervals[S.j-1][0]}`：不同 → ==保留，各自一段=='
            if S.intervals[S.j][0] != S.intervals[S.j - 1][0] else
            f'两个区间 g 都是 `{S.intervals[S.j][0]}`：相同 → ==合并==，左端点区间连成一段'),
        'intervals[idx - 1][2] = intervals[j][2]': '合并：把前一个区间的右端点 r 延伸到 `{intervals[idx-1][2]}`',
        'for i, x in': lambda S, B, r: ('所有右端点都处理完了' if B.get('i') == S.i and 'i' in B else
                                       f'右端点来到 `i = {S.i}`，新元素 `x = {S.x}`'),
        'intervals = []': '`intervals` 存若干 `(g, l, r]`：左端点落在 `(l, r]` 里时，`[j, i]` 的 GCD 都是 `g`',
        'ans = max(ans, g * (i - l))': '区间 `({l}, {r}]`，GCD = `{g}`。不操作：`g × 长度` = `{g} × {i - l}` = {g * (i - l)}；区间里最左的左端点是 `l+1`，长度 `i - l`，`ans = {ans}`',
        'pos = lowbit_pos': '`g` 的 lowbit = `{g & -g}`：区间里 lowbit 最小的数正好就是 lowbit 等于它的那些，`pos = {pos}`',
        'min_l = max': lambda S, B, r: (
            f'`pos` 里有 `{len(S.pos)}` 个 > `k={S.k}`：倒数第 `k+1` 个下标是 `{S.pos[-S.k-1]}`，左端点必须在它右边，`min_l = {S.min_l}`'
            if len(S.pos) > S.k else f'`pos` 只有 `{len(S.pos)}` ≤ `k={S.k}` 个：操作次数够，不限制，`min_l = l = {S.min_l}`'),
        'if min_l < r': lambda S, B, r: (f'`min_l = {S.min_l} < r = {S.r}`：区间里还有左端点可以让 GCD 变 `2g` → ==能翻倍=='
                                         if S.min_l < S.r else f'`min_l = {S.min_l} ≥ r = {S.r}`：次数不够，GCD 翻不了倍'),
        'ans = max(ans, g * 2': '翻倍后 `2g × 长度` = `{g*2} × {i - min_l}` = {g*2*(i-min_l)}，`ans = {ans}`',
        'return ans': '最大分数 `{ans}`',
    },
    cards=dict(
        one_liner='固定右端点，GCD 只有 log 种；用 lowbit 判断能否乘 2',
        complexity='时间 `O(n log U)`，空间 `O(n + log U)`',
        problem=['每个数最多翻倍一次，最多翻 `k` 次；子数组分数 = `GCD × 长度`',
                 '求翻倍后能得到的最大分数',
                 '示例：`[2,4]`，`k=1` → `8`；本视频：`[8,4,4,6]`，`k=1` → `16`'],
        quote='固定右端点 i 时，只有 O(log U) 种不同的 GCD，其中 U=max(nums)。并且，相同的 GCD 对应的左端点是连续的，也就是说左端点组成了一个区间。',
        quote_src='—— 灵茶山艾府题解（方法二 · LogTrick）',
        idea=['`intervals` 里存 `(g, l, r]`：左端点在 `(l, r]` 时 GCD 都是 `g`',
              'GCD 至多翻成 `2g`，关键是子数组里因子 2 最少的那些数（lowbit 等于 `g` 的 lowbit）不超过 `k` 个',
              '`pos` = 这些数的下标；倒数第 `k+1` 个下标限制了左端点，`min_l` 之外都行'],
        summary=['时间 `O(n log U)`：每个区间 GCD 至多减半 30 次',
                 '`(l, r]` 是左开右闭；`min_l` 已经按“减 1”的写法，答案长度是 `i - min_l`',
                 '易错：不操作和翻倍两种情况都要更新 `ans`',
                 '灵神还给了 `O(n²)` 暴力枚举（维护 lowbit 最小值及次数），这里演示 LogTrick 写法'],
    ),
)

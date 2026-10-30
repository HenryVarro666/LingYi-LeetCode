from math import gcd as _g

NUMS = [2, 4, 9, 6]
MAXC = 1


def _left_min():
    n = len(NUMS)
    out = []
    for i in range(n):
        lo = n
        for l in range(i + 1):
            g = 0
            for x in NUMS[l:i + 1]:
                g = _g(g, x)
            if g >= 2:
                lo = l
                break
        out.append(lo)
    return out


LM = _left_min()


def _mods(upper):
    n, c, i, out, fail = len(NUMS), MAXC, upper, [], False
    while i < n:
        if i - LM[i] + 1 > upper:
            if c == 0:
                fail = True
                break
            c -= 1
            out.append(i)
            i += upper + 1
        else:
            i += 1
    return out, fail


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(NUMS)
    cell = min(110, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 70
    line = S.get('_line', 0)
    in_check = 'upper' in S
    lm = S.get('left_min', [])
    cur = S.get('i') if 'i' in S else None
    cv.text((x0 + 18, y0 + 4), 'nums（下方横条 = 以 i 结尾、GCD ≥ 2 的最长子数组）' if not in_check
            else f"nums（upper = {S['upper']}：横条超过 upper 就要把 i 改成 1）", 24, T['muted'], bold=True)
    mods, fail = (_mods(S['upper']) if in_check else ([], False))
    shown = mods[:MAXC - S['c']] if in_check and 'c' in S else []
    for idx, v in enumerate(NUMS):
        X = sx + idx * cell
        modded = idx in shown
        cv.rect((X + 4, top, X + cell - 4, top + cell * 0.7), fill=T['red'] if modded else (60, 68, 80), r=8)
        cv.text((X + cell / 2, top + cell * 0.35), 1 if modded else v, 36, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, top + cell * 0.7 + 6), idx, 18, T['dim'], anchor='mt', mono=True)
    ybar = top + cell * 0.7 + 40
    live_i = cur if (cur is not None and cur < n) else None
    for idx in range(n):
        if idx >= len(lm) or lm[idx] >= n:
            continue
        if not in_check and live_i is not None and idx > live_i:
            continue
        if not in_check and live_i is not None and idx == live_i and line < 23:
            continue
        if in_check and live_i is not None and idx != live_i:
            continue
        a = lm[idx]
        yy = ybar + (0 if in_check else idx * 42)
        L = idx - a + 1
        bad = in_check and L > S['upper']
        cv.rect((sx + a * cell + 8, yy, sx + (idx + 1) * cell - 8, yy + 16), fill=T['red'] if bad else T['cyan'], r=6, alpha=220)
        cv.text((sx + (a + idx + 1) * cell / 2, yy + 20), f'i={idx}: [{a}, {idx}] 长 {L}', 20, T['red'] if bad else T['muted'], anchor='mt', mono=True)
    if in_check and live_i is not None:
        X = sx + live_i * cell + cell / 2
        cv.tri_up(X, top + cell * 0.7 + 30, 9, T['yellow'])


def _top(S):
    line = S.get('_line', 0)
    if 'upper' in S:
        return f"`upper = {S['upper']}`：最长稳定子数组要 `<= {S['upper']}`，已用修改 `{MAXC - S.get('c', MAXC)}`/`{MAXC}`"
    if 'i' in S and line <= 23:
        return '预处理：对每个右端点 i，算 GCD ≥ 2 的==最长==子数组左端点 `left_min[i]`（LogTrick）'
    return '先 LogTrick 预处理，再二分上界 `upper`，用贪心判断要改几个'


def _ivs(S):
    return ', '.join(f'({a},{b})' for a, b in S['intervals'])


def _ret(S, B, ret):
    return (f'`upper = {S.upper}` 修改次数够用 → ==可行==' if ret
            else f'`c == 0` 已经没有修改次数 → `upper = {S.upper}` ==不行==')


CONFIG = dict(
    num=3605, title='数组的最小稳定性因子', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · LogTrick 预处理 left_min',
    tags=['灵神题单·二分算法', '灵神题单·位运算', '难度分 2410'],
    code='''
class Solution:
    def minStable(self, nums: List[int], maxC: int) -> int:
        n = len(nums)
        left_min = [n] * n
        intervals = [[1, 0]]  # 哨兵
        for i, x in enumerate(nums):
            # 计算以 i 为右端点的子数组 GCD
            for p in intervals:
                p[0] = gcd(p[0], x)
            # nums[i] 单独一个数作为子数组
            intervals.append([x, i])

            # 去重（合并 GCD 相同的区间）
            idx = 1
            for j in range(1, len(intervals)):
                if intervals[j][0] != intervals[j - 1][0]:
                    intervals[idx] = intervals[j]
                    idx += 1
            del intervals[idx:]

            # 由于我们添加了哨兵，intervals[1] 的 GCD >= 2 且最长，取其区间左端点作为子数组的最小左端点
            if len(intervals) > 1:
                left_min[i] = intervals[1][1]

        def check(upper: int) -> bool:
            c = maxC
            i = upper
            while i < n:
                if i - left_min[i] + 1 > upper:
                    if c == 0:
                        return False
                    c -= 1
                    i += upper + 1
                else:
                    i += 1
            return True

        return bisect_left(range(len(nums) // (maxC + 1)), True, key=check)
''',
    call=f'Solution().minStable({NUMS}, {MAXC})',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=25, h=90),
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=lambda S: ('`intervals`（GCD，最小左端点）= ' + _ivs(S)) if 'intervals' in S and 'upper' not in S else '', size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'orange'), ('left_min', 'left_min', 'cyan'), ('upper', 'upper', 'yellow'), ('c', 'c', 'green')],
    skip=['n = len(nums)', 'for p in intervals', 'for j in range', 'intervals[idx] = intervals[j]', 'idx += 1', 'idx = 1', 'del intervals'],
    max_steps=100,
    captions={
        'left_min = [n]': '`left_min[i]`：以 `i` 结尾、GCD ≥ 2 的最长子数组的左端点；没有就是 `n`',
        'intervals = [[1, 0]]': '`intervals` 存 `[GCD, 最小左端点]`，越靠左 GCD 越小；放一个 GCD=1 的==哨兵==',
        'for i, x in enumerate': lambda S, B, r: ('`nums` 遍历完 → 预处理结束，开始二分' if B.get('i') == S.i else f'处理右端点 `i = {S.i}`，`x = {S.x}`'),
        'return bisect_left': '二分 `upper ∈ [0, n // (maxC + 1))`：找最小的可行 upper，范围上界 `{len(nums) // (maxC + 1)}` 一定可行',
        'p[0] = gcd': '左端点 `{p[1]}` 的区间：GCD 和 `x = {x}` 取 gcd → `{p[0]}`',
        'intervals.append': '`nums[{i}] = {x}` 自己单独成一个区间 `[{x}, {i}]`；下面去重：GCD 相同的相邻区间合并，保留更靠左的',
        'if intervals[j][0] !=': lambda S, B, r: (f'`intervals[{S.j}]` 的 GCD `{S.intervals[S.j][0]}` ≠ 前一个 `{S.intervals[S.j - 1][0]}` → ==保留=='
                                                  if S.intervals[S.j][0] != S.intervals[S.j - 1][0]
                                                  else f'`intervals[{S.j}]` 的 GCD `{S.intervals[S.j][0]}` 与前一个相同 → ==合并==（丢掉右边这个）'),
        'del intervals': '删掉多余的尾部：`intervals` = {intervals}',
        'if len(intervals) > 1': lambda S, B, r: ('除了哨兵还有区间 → 有 GCD ≥ 2 的子数组' if len(S.intervals) > 1 else '只剩哨兵 → 没有 GCD ≥ 2 的子数组，`left_min[i]` 保持 `n`'),
        'left_min[i] = ': '`intervals[1]` 是 GCD ≥ 2 里最长的 → `left_min[{i}] = {left_min[i]}`：子数组 `[{left_min[i]}, {i}]` 长 `{i - left_min[i] + 1}`',
        'c = maxC': '二分判定：`upper = {upper}`，修改次数 `c = {c}`',
        'i = upper': '长度 `> upper` 的稳定子数组最早出现在右端点 `i = upper`，从这里开始查',
        'while i < n': lambda S, B, r: (f'`i = {S.i} < n` → 继续' if S.i < len(NUMS) else f'`i = {S.i} >= n` → 全部检查完'),
        'if i - left_min[i]': lambda S, B, r: (f'稳定子数组长度 `{S.i} - {S.left_min[S.i]} + 1 = {S.i - S.left_min[S.i] + 1}` '
                                               + (f'`> upper = {S.upper}` → ==必须修改==' if S.i - S.left_min[S.i] + 1 > S.upper
                                                  else f'`<= upper = {S.upper}` → 不用改')),
        'if c == 0': lambda S, B, r: ('`c == 0`：没有修改次数了 → 这个 upper ==做不到==' if S.c == 0 else f'`c = {S.c} > 0` → 还能改'),
        'c -= 1': '把 `nums[{i}]` 改成 1：包含它的子数组 GCD 都是 1 → `c = {c}`',
        'i += upper + 1': '`nums[{i}]` 已改成 1，下一个可能要改的右端点是 `i + upper + 1 = {i + upper + 1}`',
        'i += 1': '没问题，看下一个右端点 `i = {i}`',
        'return False': _ret,
        'return True': _ret,
    },
    cards=dict(
        one_liner='二分稳定性因子 upper；GCD≥2 的区间太长，就把右端点改成 1',
        complexity='时间 `O(n log U + n log M)`，空间 `O(n)`',
        problem=['子数组的 GCD ≥ 2 称为==稳定==；稳定性因子 = 最长稳定子数组的长度',
                 '最多修改 `maxC` 个元素为任意整数，使稳定性因子最小',
                 '示例：`[2,4,9,6], maxC = 1` → `2`（`[2,4]`、`[9,6]` 两段互不相交）'],
        quote='如果修改 nums[i]=1，那么包含 nums[i] 的任意子数组的 GCD 均为 1。这样后续就不用考虑 nums[i] 了，相比修改 i 左边的元素更好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最小化最大值 → ==二分 upper==：能否改至多 `maxC` 个，使最长稳定子数组 `<= upper`',
              '遇到长度超标的稳定子数组，就改它的==右端点==为 1，然后跳过 `upper+1` 个位置',
              '每次二分都算 GCD 太慢 → LogTrick 先预处理出 `left_min[i]`'],
        summary=['时间 `O(n log U + n log M)`，空间 `O(n)`',
                 '`intervals` 里放 GCD=1 的哨兵，`intervals[1]` 就是最长的 GCD ≥ 2 区间',
                 '二分上界 `n // (maxC + 1)`：把 `maxC` 个 1 均分整个数组，一定可行',
                 '未优化写法在每次 `check` 里现算 LogTrick；另有「栈 + 滑动窗口」预处理写法']
    ),
)

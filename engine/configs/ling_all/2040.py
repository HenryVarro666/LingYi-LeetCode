CODE = '''
class Solution:
    def kthSmallestProduct(self, a: List[int], b: List[int], k: int) -> int:
        i0 = bisect_left(a, 0)  # 四个区域的水平分界线
        j0 = bisect_left(b, 0)  # 四个区域的垂直分界线

        def check(mx: int) -> bool:
            if mx < 0:
                cnt = 0

                # 右上区域
                i, j = 0, j0
                while i < i0 and j < m:  # 不判断 cnt < k 更快
                    if a[i] * b[j] > mx:
                        j += 1
                    else:
                        cnt += m - j
                        i += 1

                # 左下区域
                i, j = i0, 0
                while i < n and j < j0:
                    if a[i] * b[j] > mx:
                        i += 1
                    else:
                        cnt += n - i
                        j += 1
            else:
                # 右上区域和左下区域的所有数都 <= 0 <= mx
                cnt = i0 * (m - j0) + (n - i0) * j0

                # 左上区域
                i, j = 0, j0 - 1
                while i < i0 and j >= 0:
                    if a[i] * b[j] > mx:
                        i += 1
                    else:
                        cnt += i0 - i
                        j -= 1

                # 右下区域
                i, j = i0, m - 1
                while i < n and j >= j0:
                    if a[i] * b[j] > mx:
                        j -= 1
                    else:
                        cnt += j - j0 + 1
                        i += 1

            return cnt >= k

        n, m = len(a), len(b)
        corners = (a[0] * b[0], a[0] * b[-1], a[-1] * b[0], a[-1] * b[-1])
        left, right = min(corners), max(corners)
        return left + bisect_left(range(left, right), True, key=check)
'''


def _region(S):
    L = S.get('_line', 0)
    if 'mx' not in S:
        return None
    for lo, hi, name in ((11, 17, '右上'), (20, 26, '左下'), (32, 38, '左上'), (41, 47, '右下')):
        if lo <= L <= hi:
            return name
    return None


def _info(S):
    if 'mx' not in S:
        return '把乘积看成矩阵 `a[i]·b[j]`，按正负分成四个区域，每个区域行列都有序'
    r = _region(S)
    t = f"猜 `mx = {S['mx']}`：数一数矩阵里 ≤ mx 的数有几个，现在 `cnt = {S.get('cnt', 0)}`"
    return t + (f'，正在扫==【{r}区域】==' if r else '')


def _prod(S):
    return f"{S['a'][S['i']]} × {S['b'][S['j']]} = {S['a'][S['i']] * S['b'][S['j']]}"


def _cmp(S, B, ret):
    i, j, mx = S.i, S.j, S.mx
    v = S.a[i] * S.b[j]
    r = _region(S)
    move = {'右上': '`j += 1`（往右更小）', '左下': '`i += 1`（往下更小）', '左上': '`i += 1`（往下更小）', '右下': '`j -= 1`（往左更小）'}[r]
    if v > mx:
        return f'`{_prod(S)}` > {mx}：太大，这格不算 → {move}'
    return f'`{_prod(S)}` ≤ {mx}：==这格以及它同行/列更小的一段都 ≤ mx==，一次性计数'


def _color(S, i, j, v):
    if 'mx' in S and v <= S['mx']:
        return 'green'
    return None


CONFIG = dict(
    num=2040, title='两个有序数组的第 K 小乘积', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 四区域双指针计数',
    tags=['难度分 2518'],
    code=CODE,
    call='Solution().kthSmallestProduct([-2, 0, 3], [-1, 4], 3)',
    expect=0,
    views=[
        dict(type='grid', var=lambda S: [[x * y for y in S['b']] for x in S['a']], rows='a', cols='b', h=380, cell=140, label='乘积矩阵 a[i]·b[j]（行 = a，列 = b；绿 = ≤ mx）',
             cursors=[('i', 'j', 'yellow', '')], color=_color),
        dict(type='text', fn=_info, size=26, h=100),
    ],
    watch=['i0', 'j0', 'left', 'right', 'mx', 'i', 'j', ('cnt', 'cnt', 'green')],
    captions={
        'i0 = bisect_left(a, 0)': '`a` 里第一个 ≥ 0 的下标 `i0 = {i0}`：矩阵的行以此为界，上面是负数行',
        'j0 = bisect_left(b, 0)': '`b` 里第一个 ≥ 0 的下标 `j0 = {j0}`：矩阵的列以此为界，左边是负数列',
        'if mx < 0': lambda S, B, r: (f'`mx = {S.mx} < 0`：只有「负 × 正」的两个区域（右上、左下）会有 ≤ mx 的数' if S.mx < 0
                                     else f'`mx = {S.mx} ≥ 0`：右上和左下全是 ≤ 0，直接全算；再数左上、右下'),
        'cnt = i0 * (m - j0)': '右上区域 `{i0}×{m - j0}` + 左下区域 `{n - i0}×{j0}` 个数全 ≤ 0 ≤ mx → `cnt = {cnt}`',
        11: '==右上区域==（负 × 非负）：从 `(0, j0)` 出发，每行向右乘积越来越小，每列向下越来越大',
        20: '==左下区域==（非负 × 负）：从 `(i0, 0)` 出发，向下、向右乘积都越来越小',
        32: '==左上区域==（负 × 负）：从 `(0, j0-1)` 出发，向下乘积变小，向左变大',
        41: '==右下区域==（非负 × 非负）：从 `(i0, m-1)` 出发，向下、向右乘积都越来越大',
        'if a[i] * b[j] > mx': _cmp,
        'cnt += m - j': '右上区域：第 `{i}` 行从 `j={j}` 到末尾共 `{m - j}` 个都 ≤ mx → `cnt = {cnt}`，换下一行',
        'cnt += n - i': '左下区域：第 `{j}` 列从 `i={i}` 到底共 `{n - i}` 个都 ≤ mx → `cnt = {cnt}`，换下一列',
        'cnt += i0 - i': '左上区域：第 `{j}` 列从 `i={i}` 到 `i0-1` 共 `{i0 - i}` 个都 ≤ mx → `cnt = {cnt}`，换左边一列',
        'cnt += j - j0 + 1': '右下区域：第 `{i}` 行从 `j0` 到 `j={j}` 共 `{j - j0 + 1}` 个都 ≤ mx → `cnt = {cnt}`，换下一行',
        'return cnt >= k': '`cnt = {cnt}`，`k = {k}` → ==`{cnt >= k}`==：{"≤ mx 的数够 k 个，答案 ≤ mx" if cnt >= k else "不够 k 个，答案 > mx"}',
        'corners = ': '矩阵最小值、最大值一定在四个角：`{corners}`',
        'left, right = min(corners)': '二分范围 `[{left}, {right})`',
        'return left + bisect_left': '开始二分：找最小的 `mx` 使 `check(mx)` 为真，下面每一轮是一次猜测',
    },
    skip=['while i < i0 and j < m', 'while i < n and j < j0', 'while i < i0 and j >= 0', 'while i < n and j >= j0', 'cnt = 0', 'n, m = len(a), len(b)', 'i0 = bisect_left', 'j0 = bisect_left'],
    max_steps=110,
    cards=dict(
        one_liner='二分答案 mx：数矩阵里 ≤ mx 的数，用双指针分四块数',
        complexity='时间 `O((n+m)·log U)`，空间 `O(1)`',
        problem=['两个升序数组，取所有乘积 `a[i]·b[j]`，求第 `k` 小',
                 '示例：`[2,5],[3,4],k=2` → `8`',
                 '本视频：`a=[-2,0,3], b=[-1,4], k=3` → `0`（乘积 -8,-3,0,0,2,12）'],
        quote='第 k 小等价于：求最小的 x，满足 ≤ x 的数至少有 k 个。（注意是至少不是恰好）',
        quote_src='—— 灵茶山艾府题解',
        idea=['乘积矩阵按正负分成四块（0 归到下面两块），每块的行列都有序',
              '统计 ≤ mx 的个数，和 378 题一样用==双指针==，每块 `O(n+m)`',
              '二分范围取矩阵四个角的乘积的最小、最大值'],
        summary=['`mx < 0` 时只有右上、左下两块有答案；`mx ≥ 0` 时这两块整块都算',
                 '二分结果一定在矩阵里（反证法：否则 `check(ans-1)` 也为真）',
                 '同类题：378 有序矩阵第 K 小、668 乘法表第 K 小',
                 '`bisect_left(range, True, key=check)` 要求 check 单调：False…True'],
    ),
)

def _col(S, j, v):
    i = S.get('index')
    if i is None:
        return None
    return 'blue' if j == i else 'cyan' if j == i - 1 else None


def _txt(S):
    if 'last_same' not in S:
        return '`same` = 这一位不交换的最少次数，`swap` = 这一位交换的最少次数'
    return f"上一位：不交换 `last_same = {S['last_same']}`，交换 `last_swap = {S['last_swap']}`"


def _c1(S, B, r):
    i = S.index
    ok = S.A[i] > S.A[i - 1] and S.B[i] > S.B[i - 1]
    return (f'`A[{i}] > A[{i-1}]` 且 `B[{i}] > B[{i-1}]`（`{S.A[i]} > {S.A[i-1]}`，`{S.B[i]} > {S.B[i-1]}`）：==上一位怎么做，这一位就怎么做==' if ok
            else f'`{S.A[i]} > {S.A[i-1]}` 且 `{S.B[i]} > {S.B[i-1]}` 不成立：上一位和这一位不能同做法')


def _c2(S, B, r):
    i = S.index
    ok = S.A[i] > S.B[i - 1] and S.B[i] > S.A[i - 1]
    return (f'`A[{i}] > B[{i-1}]` 且 `B[{i}] > A[{i-1}]`（`{S.A[i]} > {S.B[i-1]}`，`{S.B[i]} > {S.A[i-1]}`）：==上一位换了这一位就不换，反之亦然==' if ok
            else f'`{S.A[i]} > {S.B[i-1]}` 且 `{S.B[i]} > {S.A[i-1]}` 不成立：不能一换一不换')


CONFIG = dict(
    num=801, title='使序列递增的最小交换次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='换 / 不换 两个状态 DP',
    tags=['灵神题单', '动态规划', '难度分 2066'],
    code='''
class Solution(object):
    def minSwap(self, A, B):

        n = len(A)
        last_same = 0
        last_swap = 1
        for index in range(1, n):
            now_same = now_swap = n + 1
            if A[index] > A[index - 1] and B[index] > B[index - 1]:
                now_same = min(now_same, last_same)
                now_swap = min(now_swap, last_swap + 1)
            if A[index] > B[index - 1] and B[index] > A[index - 1]:
                now_same = min(last_swap, now_same)
                now_swap = min(last_same + 1, now_swap)
            last_same, last_swap = now_same, now_swap
        
        return min(last_same, last_swap)
''',
    call='Solution().minSwap([0, 3, 5, 8, 9], [2, 1, 4, 6, 9])',
    expect=1,
    views=[
        dict(type='array', var='A', label='A（蓝 = 当前位，青 = 上一位）', cell=96, h=170, color=_col),
        dict(type='array', var='B', label='B', cell=96, h=170, color=_col),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('last_same', 'last_same', 'green'), ('last_swap', 'last_swap', 'orange'),
           ('now_same', 'now_same', 'cyan'), ('now_swap', 'now_swap', 'pink')],
    captions={
        'n = len(A)': '`n = {n}`，`n + 1` 之后当“不可能”用',
        'last_same = 0': '第 0 位不交换：0 次',
        'last_swap = 1': '第 0 位交换：1 次',
        'for index in range': '处理第 `{index}` 位',
        'now_same = now_swap = n + 1': '先都设成不可能的大值 `{now_same}`，下面的分类讨论再取小',
        'if A[index] > A[index - 1]': _c1,
        'now_same = min(now_same, last_same)': '上一位没换、这一位也不换：`now_same` → ==`{now_same}`==',
        'now_swap = min(now_swap, last_swap + 1)': '上一位换了、这一位也换：`now_swap = last_swap + 1` → ==`{now_swap}`==',
        'if A[index] > B[index - 1]': _c2,
        'now_same = min(last_swap': '上一位换了、这一位不换：`now_same` → ==`{now_same}`==',
        'now_swap = min(last_same + 1': '上一位没换、这一位换：`now_swap = last_same + 1` → ==`{now_swap}`==',
        'last_same, last_swap =': '滚动：`last_same = {last_same}`，`last_swap = {last_swap}`',
        'return min': '最后一位两种状态取小：`min({last_same}, {last_swap})` = =={ret}==',
    },
    cards=dict(
        one_liner='每一位只有换或不换，且只受前一位影响',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两个等长数组 `A`、`B`，每次可交换 `A[i]` 与 `B[i]`',
                 '求让两个数组都严格递增的最少交换次数',
                 '本视频：`A = [0,3,5,8,9]`，`B = [2,1,4,6,9]` → `1`'],
        quote='对于数组中的每一位，只有换或者不换两种选择，而选择的可能性只与前一位数字有关，因此可以使用动态规划来求解。令f[i]表示第i位不进行交换且合法的最少交换次数，g[i]表示第i位交换且合法的最少交换次数',
        quote_src='—— yiduobo 题解原文',
        idea=['`A[i] > A[i-1]` 且 `B[i] > B[i-1]`：上一位不换则这位不换，上一位换则这位也换',
              '`A[i] > B[i-1]` 且 `B[i] > A[i-1]`：上一位换了这位就不换，反之亦然',
              '第 0 位既可以换也可以不换：`0` 和 `1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：两个 `if` 都可能成立，要用 `min` 合并，不能用 `elif`',
                 '交换一次计 1，所以“换”的转移都要 `+1`',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神用 `inf` 初始化，这里用 `n + 1`，思路相同'],
    ),
)

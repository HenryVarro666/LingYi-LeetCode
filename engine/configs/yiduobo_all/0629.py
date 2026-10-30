def _dep(S, i, j, v):
    I, J = S.get('i'), S.get('j')
    if I is None or J is None or J == 0:
        return None
    ln = S.get('_line')
    if ln in (11, 12, 13, 14):
        if (i, j) == (I, J - 1) or (i, j) == (I - 1, J):
            return 'blue'
        if J >= I and (i, j) == (I - 1, J - I) and ln in (12, 13, 14):
            return 'pink'
    return None


def _fm(S):
    I, J = S.get('i'), S.get('j')
    if I is None or J is None:
        return '`f[i][j]` = 1..i 的排列里恰有 `j` 个逆序对的个数；把 `i` 插进长度 i−1 的排列，新增 0..i−1 个逆序对'
    if J == 0:
        return f'`f[{I}][0] = 1`：只有升序排列没有逆序对'
    s = f'`f[{I}][{J}] = f[{I}][{J - 1}] + f[{I - 1}][{J}]`'
    if J >= I:
        s += f' `− f[{I - 1}][{J - I}]`'
    return s + '（滑动窗口式的区间和）'


CONFIG = dict(
    num=629, title='K个逆序对数组', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='插入法 DP + 前缀和差分',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def kInversePairs(self, n, k):

        f = [[0] * (k + 1) for _ in range(n + 1)]
        mod = 10 ** 9 + 7
        for i in range(1, n + 1):
            for j in range(min(k + 1, (i * (i - 1) // 2 + 1))):
                if j == 0:
                    f[i][j] = 1
                else:
                    f[i][j] = f[i][j - 1] + f[i - 1][j]
                    if j >= i:
                        f[i][j] -= f[i - 1][j - i]
                    f[i][j] %= mod

        return f[n][k]
''',
    call='Solution().kInversePairs(4, 3)',
    expect=6,
    skip=['for j in range', 'else:'],
    views=[
        dict(type='text', h=70, size=24, fn=_fm),
        dict(type='table', var='f', label='f[i][j]：1..i 的排列中恰有 j 个逆序对的个数', h=420, cell=96,
             rows=['i=0', 'i=1', 'i=2', 'i=3', 'i=4'], cols=['j=0', 'j=1', 'j=2', 'j=3'],
             cursors=[('i', 'j', 'yellow', '(i,j)')], color=_dep),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[n][k]', 'f[n][k]', 'green')],
    captions={
        'f = [[0]': '`f[i][j]`：排列 `1..i` 中恰有 `j` 个逆序对的个数，先全填 0',
        'mod = ': '答案取模',
        'for i in range': lambda S, B, r: ((f'把数字 `{S.i}` 插进 `1..{S.i - 1}` 的排列里' if S.i > 1 else '从 `1` 个数的排列开始') if S.i != B.get('i') else '`n` 个数都插完了'),
        'if j == 0': lambda S, B, r: ('`j = 0`：没有逆序对，直接给 1' if S.j == 0 else f'`j = {S.j}` ≠ 0：用相邻两格的差分关系递推'),
        'f[i][j] = 1': '没有逆序对：只有升序排列这 1 种 → `f[{i}][0] = 1`',
        'f[i][j] = f[i][j - 1]': '`f[{i}][{j}] = f[{i}][{j - 1}] + f[{i - 1}][{j}]` = {f[i][j]}：窗口右移一格，==加上新进窗口的 f[i-1][j]==',
        'if j >= i': lambda S, B, r: (f'`j = {S.j} >= i = {S.i}`：窗口里最左边的 `f[{S.i - 1}][{S.j - S.i}]` 滑出去了，要减掉' if S.j >= S.i else f'`j = {S.j} < i = {S.i}`：窗口还没满，不用减'),
        'f[i][j] -= f[i - 1][j - i]': '减去滑出窗口的 `f[{i - 1}][{j - i}]` → {f[i][j]}',
        'f[i][j] %= mod': '取模：`f[{i}][{j}] = {f[i][j]}`',
        'return f[n][k]': '`f[{n}][{k}]` = =={ret}==：4 个数恰有 3 个逆序对的排列有 6 个',
    },
    cards=dict(
        one_liner='把 i 插进旧排列：插在不同位置，恰好新增 0…i−1 个逆序对',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['给定 `n` 和 `k`，数出 `1..n` 的所有排列中，恰有 `k` 个逆序对的有多少个',
                 '答案对 `10^9+7` 取模',
                 '示例：`n=3, k=1` → `2`；本视频：`n=4, k=3` → `6`'],
        quote='f[i][j] = f[i - 1][j] + f[i - 1][j - 1] + ... + f[i - 1][j - i + 1]，不过这个做法最终的时间复杂度是O(n^3)，效率不太行。',
        quote_src='—— yiduobo 题解原文',
        idea=['`i` 插在倒数第 `t` 位，新增 `t−1` 个逆序对 → `f[i][j]` 是 `f[i-1]` 上长度为 `i` 的窗口和',
              '相邻两项的窗口只差两端：`f[i][j] = f[i][j-1] + f[i-1][j] − f[i-1][j-i]`',
              '省去前缀和数组，总复杂度降到 `O(nk)`'],
        summary=['时间 `O(nk)`，空间 `O(nk)`',
                 '`j >= i` 时才需要减去滑出窗口的那一项，否则会越界/减错',
                 '内层 `j` 只枚举到 `min(k, i(i−1)/2)`：逆序对不会超过 `i(i−1)/2`',
                 '原文为 Python 2 写法，`i * (i - 1) / 2` 的整数除法已改为 `//`',
                 '题面库里没有，题意依据原文与力扣 629 题'],
    ),
)

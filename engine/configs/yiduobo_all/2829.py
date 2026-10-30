def _nums(S):
    return list(range(1, S['k'] + S['n']))


def _color(S, i, v):
    if 'm' not in S:
        return None
    m, n, k = S['m'], S['n'], S['k']
    if v <= m:
        return 'green'
    if k <= v <= k + n - m - 1:
        return 'blue'
    return None


def _dim(S, i, v):
    if 'm' not in S:
        return False
    m, n, k = S['m'], S['n'], S['k']
    return not (v <= m or k <= v <= k + n - m - 1)


def _text(S):
    n, k = S['n'], S['k']
    if 'm' not in S:
        return f'k={k}：和为 k 的数对 `(1,{k-1})`、`(2,{k-2})`…… 每对只能留一个'
    m = S['m']
    s1 = m * (m + 1) // 2
    s2 = (k * 2 + n - m - 1) * (n - m) // 2
    return f'第一部分 `1..{m}` = =={s1}==　　第二部分 `{k}..{k+n-m-1}`（{n-m} 个）= =={s2}=='


CONFIG = dict(
    num=2829, title='k-avoiding 数组的最小总和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='分情况讨论 + 等差数列',
    tags=['灵神题单', '难度分 1347'],
    code='''
class Solution(object):
    def minimumSum(self, n, k):

        if k <= 2:
            return (1 + n) * n // 2

        m = k // 2
        if m >= n:
            return (1 + n) * n // 2
        else:
            return (1 + m) * m // 2 + (k + k + n - m - 1) * (n - m) // 2
''',
    call='Solution().minimumSum(5, 4)',
    expect=18,
    views=[
        dict(type='text', fn=_text, h=110, size=28),
        dict(type='array', var=_nums, color=_color, dim=_dim, h=240, cell=70,
             label='候选正整数（绿 = 1..m，蓝 = k 起往上补，灰 = 被丢弃）'),
    ],
    watch=['n', 'k', ('m', 'm', 'green')],
    captions={
        'if k <= 2': '`k = {k}`：{"k ≤ 2，不可能有两个不同正整数和为 k，直接取最小的 n 个数" if k <= 2 else "k > 2，存在和为 k 的数对，要讨论"}',
        'm = k // 2': '`k` 以内的数对 `(1,k-1)`…… 只能留小的，所以小于 k 的数最多取 `1..k//2` → `m = {m}`',
        'if m >= n': '`m = {m}`，`n = {n}`：{"m ≥ n，只取前 n 个就够" if m >= n else "m < n，前 m 个不够，还要从 k 往上补 n-m 个"}',
        'else': '走到 else：要补数',
        'return (1 + m)': '`1..{m}` 的和 + `{k}..{k+n-m-1}` 的和 = =={ret}==',
    },
    cards=dict(
        one_liner='k ≤ 2 或 n 小就取前 n 个；否则取 1..k/2，再从 k 往上补',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['数组由不同正整数组成，==没有两个元素之和等于 k==',
                 '求长度为 `n` 的这类数组的最小总和',
                 '示例：`n = 5, k = 4` → `18`'],
        quote='无论是奇数还是偶数的情况，在小于k的数中都只能选择1到k / 2这些数，而k / 2 + 1到k - 1这些则必然会被丢弃。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看特殊情况：`k <= 2` 没有数对，取最小的 `n` 个数',
              '`k > 2`：数对 `(1,k-1)`、`(2,k-2)`…… 留小的，记 `m = k // 2`',
              '`n <= m` 取 `1..n`；否则取 `1..m` 再补 `k` 起的 `n-m` 个数'],
        after=[dict(heading='验算 n = 5, k = 4', lines=['`k > 2`，`m = 2 < 5`，走 else',
                                                       '`1+2 = 3`，补 `4,5,6` 得 `15`',
                                                       '合计 `18`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：补的数是 `k, k+1, …, k+n-m-1`，末项别多算一个',
                 '`k` 本身能选，因为只有一个数不构成数对',
                 '原文为 Python 2 写法，整数除法 `/` 已全部改为 `//`'],
    ),
)

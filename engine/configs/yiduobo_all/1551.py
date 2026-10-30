CONFIG = dict(
    num=1551, title='使数组中所有元素相等的最小操作数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='等差数列首尾配对求和',
    code='''
class Solution(object):
    def minOperations(self, n):

        if n & 1:
            return (n + 1) * (n - 1) // 4
        else:
            return n * n // 4
''',
    call='Solution().minOperations(6)',
    expect=9,
    views=[
        dict(type='text', h=120, size=34, fn=lambda S: '数组 `arr[i] = 2i + 1`：' + ' '.join(str(2 * i + 1) for i in range(S['n'])) + f'；总和 `n×n` = {S["n"] * S["n"]}，目标全变成 =={S["n"]}=='),
        dict(type='bars', h=300, var=lambda S: [2 * i + 1 for i in range(S['n'])],
             color=lambda S, i, v: 'pink' if v < S['n'] else ('cyan' if v > S['n'] else 'green'),
             label='首尾配对：小的 +1 补给大的 -1，直到都等于 n'),
        dict(type='text', h=120, size=34, fn=lambda S: ' + '.join(f'{(S["n"] - (2 * i + 1)) * 2 // 2}' for i in range(S['n'] // 2)) + f' = =={S["n"] * S["n"] // 4 if S["n"] % 2 == 0 else (S["n"] + 1) * (S["n"] - 1) // 4}==（每对代价 = 小数到 n 的距离）'),
    ],
    watch=['n'],
    captions={
        'if n & 1': lambda S, B, r: (f'`n = {S.n}`，`n & 1 = 1` → 成立：n 是奇数，中间的 `n` 不用动' if S.n & 1
                                      else f'`n = {S.n}`，`n & 1 = 0` → 不成立：n 是偶数，首尾刚好两两配完'),
        'return (n + 1)': '奇数：每对代价 `n-1、n-3、…、2`，求和 = `(n+1)(n-1)/4` = =={ret}==',
        'return n * n': '偶数：每对代价 `n-1、n-3、…、1`，求和 = `n×n/4` = =={ret}==（整数除法用 `//`）',
    },
    cards=dict(
        before=[dict(heading='例：n = 6 的配对', lines=['数组 `[1, 3, 5, 7, 9, 11]`，总和 `36 = 6×6`，目标全变成 `6`',
                '配对 `[1,11]`、`[3,9]`、`[5,7]`',
                '每对只需把小数补到 `6`：代价 `5`、`3`、`1`',
                '合计 `5+3+1 = 9`，正是 `n×n/4 = 9`'])],
        one_liner='操作不改变总和，首尾配对把每个数补成 n',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['数组 `arr[i] = 2×i + 1`（`0 <= i < n`）',
                 '每次选两个下标，一个 `+1`、一个 `-1`，求让所有元素相等的最少操作数',
                 '本视频：`n = 6` → `9`'],
        quote='无论怎么操作，数组中所有数的总和是不变的。……最终操作的结果必然是让数组中的每个数都变成n。',
        quote_src='—— yiduobo 题解原文',
        idea=['总和 `1+3+…+(2n-1) = n×n`，所以最终每个数都是 `n`',
              '首尾配对 `[1, 2n-1]`、`[3, 2n-3]`…，每对的代价是小数到 `n` 的距离',
              '奇数 `n` 求和得 `(n+1)(n-1)/4`，偶数 `n` 得 `n×n/4`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：奇偶分开讨论，奇数时中间的 `n` 不需要操作',
                 '原文为 Python 2 写法，整数 `/` 已改为 `//`',
                 '本题没有循环，视频重点放在数学推导上'],
    ),
)

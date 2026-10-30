CONFIG = dict(
    num=1085, title='最小元素各数位之和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='取最小值 + 逐位求和',
    code='''
class Solution(object):
    def sumOfDigits(self, nums):

        mi = min(nums)
        s = 0
        while mi:
            s += mi % 10
            mi //= 10
        
        return (s + 1) % 2
''',
    call='Solution().sumOfDigits([99,77,48,67,88,53,91])',
    expect=1,
    views=[
        dict(type='array', var='nums', h=200, color=lambda S, i, v: 'green' if 'mi' in S and v == min(S['nums']) and 's' not in S else None),
        dict(type='text', fn=lambda S: (f"剩下的数 `mi = {S['mi']}`，已累加 `s = {S['s']}`" if 's' in S and 'mi' in S else ''), size=34),
    ],
    watch=['mi', 's'],
    captions={
        'mi = min(nums)': '一趟遍历找最小值：`mi = {mi}`',
        's = 0': '`s` 累加最小值的各位数字',
        'while mi': lambda S, B, r: (f'`mi = {S.mi}` 还没分离完 → 继续' if S.mi else '`mi = 0`：所有数位都取完了 → 退出循环'),
        's += mi % 10': '`mi % 10` 取出个位 `{mi % 10}`：`s` → {s}',
        'mi //=': '去掉个位：`mi` → {mi}（原文 `/`，Python 3 要用 `//`）',
        'return': '`s = {s}`：奇数返回 0，偶数返回 1，即 `(s + 1) % 2` = =={ret}==',
    },
    cards=dict(
        one_liner='最小值的数位和是奇数返回 0，偶数返回 1',
        complexity='时间 `O(n + log m)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，设 `s` 为最小元素各数位之和',
                 '`s` 为奇数返回 `0`，偶数返回 `1`',
                 '示例：`[99,77,48,67,88,53,91]`，最小是 `48`，`s=12` 偶数 → `1`'],
        quote='一趟遍历找出数组中的最小值，然后逐位分离个位数字并累加起来得到s，最后返回s + 1对2取模的结果即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `min(nums)` 得到最小值',
              '`% 10` 取个位、`// 10` 去个位，直到变成 0',
              '`(s + 1) % 2`：`s` 奇数得 0，偶数得 1，不用写 if'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `mi /= 10` 已改为 `mi //= 10`',
                 '`while mi` 到 0 就停；最小值本身不会是 0（题目 `nums[i] >= 1`）',
                 '返回的是奇偶取反，别直接返回 `s % 2`'],
    ),
)

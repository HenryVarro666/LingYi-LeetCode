CONFIG = dict(
    num=1304, title='和为零的 N 个不同整数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='前 n-1 个取 1..n-1，最后补负和',
    tags=['灵神题单', '贪心与思维', '难度分 1167'],
    code='''
class Solution(object):
    def sumZero(self, n):

        res = list(range(1, n))
        res.append(-(n - 1) * n // 2)
        return res
''',
    call='Solution().sumZero(6)',
    expect=[1, 2, 3, 4, 5, -15],
    views=[
        dict(type='text', fn=lambda S: (f"正数之和 = `{sum(S['res'][:S['n']-1])}`，补上 `{S['res'][-1]}` → 总和 ==0==" if 'res' in S and len(S['res']) == S['n'] else (f"前 `n-1 = {S['n']-1}` 个数：`1 .. {S['n']-1}`，和 = `n(n-1)/2`" if 'res' in S else ''))),
        dict(type='array', var='res', h=260, color=lambda S, i, v: 'pink' if v < 0 else 'green'),
    ],
    watch=['n', 'res'],
    captions={
        'res = list': '前 `n-1` 个数取 `1 .. {n-1}`：全是正数、互不相同，和 = `{sum(res)}`',
        'res.append': '再补一个 `-(n-1)*n/2 = {res[-1]}`：它是负数，和前面都不同，总和刚好 ==0==',
        'return res': '`{res}` 的和为 `{sum(res)}`，返回',
    },
    cards=dict(
        after=[dict(heading='为什么互不相同', lines=['前 `n-1` 个数是 `1..n-1`，两两不同', '最后一个数是负数，不会和它们重复', '和 = `n(n-1)/2 - n(n-1)/2 = 0`'])],
        one_liner='前 n-1 个数取 1 到 n-1，最后补一个相反的总和',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['给定 `n`，返回任意 `n` 个互不相同的整数，和为 `0`',
                 '示例：`n = 3` → `[-1,0,1]`',
                 '本视频：`n = 6`'],
        quote='先将前n - 1个数设为1到n - 1，此时的和为n * (n - 1) / 2，那么最后再添加一个 -n * (n - 1) / 2即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['只要一个可行解：前 `n-1` 个数全是正数且各不相同',
              '它们的和是等差数列和 `n(n-1)/2`，最后一个数取它的相反数',
              '最后一个是负数，所以不会和前面重复'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`range(1, n)` 已改为 `list(range(1, n))`，`/` 已改为 `//`',
                 '易错：`n = 1` 时前半为空，补 `0`，仍然正确',
                 '对比灵神：灵神方法二是同一个思路，方法一则是正负成对'],
    ),
)

CONFIG = dict(
    num=1374, title='生成每种字符都是奇数个的字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='构造',
    code='''
class Solution(object):
    def generateTheString(self, n):

        res = ['a'] * n
        if n % 2 == 0:
            res[-1] = 'b'
        
        return ''.join(res)
''',
    call='Solution().generateTheString(4)',
    expect='aaab',
    views=[
        dict(type='array', var='res', h=200),
        dict(type='text', fn=lambda S: f"n = {S['n']}，" + ('偶数：n−1 个 a（奇数）+ 1 个 b' if S['n'] % 2 == 0 else '奇数：全是 a'), size=32, h=80),
    ],
    watch=['n', ('res', "''.join(res)", 'green')],
    captions={
        "res = ['a']": '先放 `{n}` 个 `a`：`{res}`',
        'if n % 2 == 0': lambda S, B, r: (f'`n % 2 = {S.n % 2}`：n 是偶数，==全 a 会出现偶数个 a==，要改一个' if S.n % 2 == 0
                                          else f'`n % 2 = {S.n % 2}`：n 是奇数，`{S.n}` 个 a 本身就合法'),
        "res[-1] = 'b'": '最后一位改成 `b`：a 有 `{n - 1}` 个（奇数），b 有 1 个（奇数）',
        'return': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='奇数个全 a；偶数个就 n−1 个 a 加一个 b',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定 `n`，返回长度为 `n` 的字符串，要求每种字符出现的次数都是奇数',
                 '任意一个合法答案即可',
                 '本视频：`n = 4` → `aaab`'],
        quote='若n为奇数，那么n个\'a\'就是一个合法答案。若n为偶数，那么n - 1必然为奇数，因此n - 1个\'a\'加上一个\'b\'就是一个合法答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数 n：全是 `a`，次数 n 是奇数',
              '偶数 n：n−1 是奇数，再补一个 `b`（次数 1 也是奇数）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：偶数时不能全 a，也不能 n/2 个 a 加 n/2 个 b',
                 '构造题：先看奇偶性，再用最少的字符种类凑',
                 '原文为 Python 2 风格，除删去类型文档字符串外无需改动'],
    ),
)

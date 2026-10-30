CONFIG = dict(
    num=3959, title='判定好整数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模拟 · 分别累加两个和',
    code='''
class Solution(object):
    def checkGoodInteger(self, n):
        
        ds = 0
        ss = 0

        while n:
            d = n % 10
            n //= 10
            ds += d
            ss += d * d
        
        return ss - ds >= 50
''',
    call='Solution().checkGoodInteger(1934)',
    expect=True,
    views=[
        dict(type='text', h=110, size=38, fn=lambda S: f"剩下的 n = ==`{S['n']}`==" if 'n' in S else '输入 `n = 1934`'),
        dict(type='text', h=110, size=34, fn=lambda S: f"`ds` = ==`{S['ds']}`==    `ss` = ==`{S['ss']}`==" if 'ss' in S else ''),
        dict(type='text', h=110, size=34, fn=lambda S: f"`ss − ds` = ==`{S['ss'] - S['ds']}`==  （目标 ≥ 50）" if 'ss' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('d', 'd', 'pink'), ('ds', 'ds', 'cyan'), ('ss', 'ss', 'orange')],
    captions={
        'ds = 0': '`ds` 记数位和 digitSum',
        'ss = 0': '`ss` 记平方和 squareSum',
        'while n': lambda S, B, r: (f'`n = {S.n}` 非 0，继续分离数位' if S.n else '`n = 0`：数位分离完 → 结束'),
        'd = n % 10': '模 10 分离出个位 `d = {d}`',
        'n //= 10': '除以 10：`n` = =={n}==',
        'ds += d': '`ds` += {d} → =={ds}==',
        'ss += d * d': '`ss` += {d}×{d} → =={ss}==',
        'return ss - ds': '`ss − ds = {ss} − {ds} = {ss - ds}`，{"≥ 50，是好整数" if ss - ds >= 50 else "< 50，不是好整数"} → =={ret}==',
    },
    cards=dict(
        one_liner='按题意分别算数位和与平方和，再比较差值',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`digitSum` 是各位之和，`squareSum` 是各位平方之和',
                 '`squareSum − digitSum >= 50` 则为好整数',
                 '示例：`19` → `82 − 10 = 72` → `true`；本视频：`1934`'],
        quote='通过模10除以10的方法分离出n的每位数字，然后按照题目描述分别计算出squareSum和digitSum，最后判断前者减去后者是否大于等于50即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮取出个位 `d`，同时累加到 `ds` 和 `ss`',
              '循环结束后一次性比较 `ss - ds >= 50`',
              '完全照题意翻译，没有额外技巧'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错点：`ss - ds` 的顺序不能反',
                 '对比灵神：灵神把每位贡献合成 `d*d - d` 只用一个变量',
                 '原文为 Python 2 写法，整数除法已是 `//`，无需改动'],
    ),
)

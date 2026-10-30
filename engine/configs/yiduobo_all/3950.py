CONFIG = dict(
    num=3950, title='恰好一对连续置位', difficulty='Easy', category='位运算',
    author='yiduobo', technique='模 2 取位 · pre 记上一位',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def consecutiveSetBits(self, n):
        
        pre = 0
        cnt = 0
        while n:
            if n % 2 == 1 and pre == 1:
                cnt += 1
            pre = n % 2
            n //= 2
        
        return cnt == 1
''',
    call='Solution().consecutiveSetBits(50)',
    expect=True,
    views=[
        dict(type='string', var="format(n, 'b') if n else '0'", label='n 还剩的二进制（最右边是当前处理的最低位）', h=170, index=False),
        dict(type='text', fn=lambda S: f"pre = ==`{S['pre']}`==（上一位）　cnt = ==`{S['cnt']}`==（连续 1 的对数）" if 'cnt' in S else '', size=34, h=100),
    ],
    watch=[('n', 'n', 'blue'), ('pre', 'pre', 'pink'), ('cnt', 'cnt', 'green')],
    captions={
        'while n': lambda S, B, r: (f'`n = {S.n}` 还没除完，继续取下一位' if S.n else '`n = 0`：所有位都处理完了'),
        'if n % 2 == 1': lambda S, B, r: (f'当前位 `{S.n % 2}`，上一位 `pre = {S.pre}`：'
                                           + ('两个 1 相邻 → 成立' if S.n % 2 == 1 and S.pre == 1 else '不是连续两个 1 → 不成立')),
        'cnt += 1': '遇到一对连续的 1：`cnt` = =={cnt}==',
        'pre = n % 2': '无论当前位是多少都要更新：`pre` = {pre}',
        'n //= 2': '去掉最低位：`n` = {n}',
        'return cnt': '`cnt = {cnt}`，是否恰好为 1 → =={ret}==',
    },
    cards=dict(
        one_liner='从低位到高位扫一遍，数连续的 1 出现了几次',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['二进制里恰好有一对相邻的 `1` 才返回 `true`', '示例：`6 = 110` → `true`；`5 = 101` → `false`',
                 '本视频：`50 = 110010` → `true`'],
        quote='直接通过模2除以2的方法将n转换为二进制，同时使用一个变量pre记录上一位的值，另外使用一个变量cnt记录连续1出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n % 2` 取最低位，`n //= 2` 丢掉它，一位位转二进制', '当前位是 1 且 `pre` 也是 1 → `cnt += 1`',
              '不管当前位是什么，都要更新 `pre`，最后看 `cnt == 1`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：`pre` 要每一位都更新，不只在遇到 1 时更新',
                 '`111` 会让 `cnt` 加两次，所以不是「恰好一对」',
                 '原文已是 Python 3 可运行的写法（`//`），代码未改动',
                 '对比灵神：灵神用 `n & (n>>1)` 一步算出所有相邻对'],
    ),
)

CONFIG = dict(
    num=693, title='交替位二进制数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='n 与 n>>1 异或 · 判全 1',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def hasAlternatingBits(self, n):

        p = ((n >> 1) ^ n)

        return p & (p + 1) == 0
''',
    call='Solution().hasAlternatingBits(21)',
    expect=True,
    views=[
        dict(type='string', var="format(n, '06b')", label='n', h=150, index=False),
        dict(type='string', var="format(n >> 1, '06b')", label="n' = n >> 1（和 n 的 01 正好反过来）", h=150, index=False),
        dict(type='string', var=lambda S: format(S['p'], '06b') if 'p' in S else '------',
             label='p = n ^ n\'（必然全 1）', h=150, index=False,
             color=lambda S, i, v: 'green' if v == '1' and 'p' in S else None),
        dict(type='text', fn=lambda S: (f"p + 1 = `{format(S['p'] + 1, '07b')}`　p & (p+1) = `{format(S['p'] & (S['p'] + 1), '07b')}`"
                                        if S.get('_line', 0) >= 6 and 'p' in S else ''), size=34, h=90),
    ],
    watch=['n', 'p'],
    captions={
        'p = ((n >> 1) ^ n)': lambda S, B, r: (f"n 右移一位得 n'，若 n 是 01 相间，n' 也是，且两者正好反过来；"
                                              f"`{format(S.n, '06b')}` ^ `{format(S.n >> 1, '06b')}` = `{format(S.p, '06b')}` 全 1"),
        'return p &': lambda S, B, r: (f"问题变成 p 是否全 1：全 1 加一必为 `100…0`（`{format(S.p + 1, 'b')}`），"
                                       f"所以 `p & (p + 1) = {S.p & (S.p + 1)}` → =={r}=="),
    },
    cards=dict(
        one_liner='n 和 n 右移一位后异或，交替位就变成全 1',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['判断正整数 `n` 的二进制是否 0、1 相间', '示例：`5 = 101` → `true`；`11 = 1011` → `false`',
                 '本视频：`21 = 10101` → `true`'],
        quote='将n右移一位得到n\'，若n是01相间的，那么n\'也是01相间的，而且n和n\'的01正好是反过来的，此时如果将n异或上n\'，设其为p，那么p必然是全1。',
        quote_src='—— yiduobo 题解原文',
        idea=['不逐位拆开判断，换成整体运算：`p = (n >> 1) ^ n`',
              '01 相间 ⇒ `p` 全 1；反过来 `p` 全 1 ⇒ 相邻位都不同',
              '`p` 全 1 ⇒ `p + 1` 是 `100…0` ⇒ `p & (p + 1) == 0`'],
        after=[dict(heading='为什么 p & (p+1) 能判全 1', lines=['`p = 0111`，`p + 1 = 1000`', '进位把低位的 1 全清零，只在最高处留一个 1', '两者没有公共位，按位与必为 0'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`p & (p + 1) == 0` 中 `&` 优先级高于 `==`，Python 里无需额外括号',
                 '原文只多了 `p` 外一层括号和空行，代码未改动',
                 '对比灵神：思路同为「错位异或 + 判全 1」，原文先讲逐位分离再改成整体'],
    ),
)

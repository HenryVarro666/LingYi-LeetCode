def _b(x):
    return format(x, 'b') if x >= 0 else str(x)


def _row(S):
    if 'a' not in S:
        return ''
    a, b, c = S['a'], S['b'], S['c']
    w = max(a.bit_length(), b.bit_length(), c.bit_length(), 1)
    f = lambda v: format(v, 'b').zfill(w)
    return f"`a = {f(a)}`　`b = {f(b)}`　`c = {f(c)}`　（当前最低位在最右）　翻转 `res = {S.get('res', 0)}`"


CONFIG = dict(
    num=1318, title='或运算的最小翻转次数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='逐位扫描 · 分情况计数',
    tags=['灵神题单·位运算'],
    code='''
class Solution(object):
    def minFlips(self, a, b, c):

        res = 0
        while a or b or c:
            if c % 2 == 1:
                if a % 2 == 0 and b % 2 == 0:
                    res += 1
            else:
                if a % 2 == 1:
                    res += 1
                if b % 2 == 1:
                    res += 1
            
            a //= 2
            b //= 2
            c //= 2
        
        return res
''',
    call='Solution().minFlips(2, 6, 5)',
    expect=3,
    views=[
        dict(type='text', fn=_row, size=40),
        dict(type='text', fn=lambda S: (f"最低位：a 的位 = =={S['a'] % 2}==，b 的位 = =={S['b'] % 2}==，c 的位 = =={S['c'] % 2}==" if 'a' in S else ''), size=36),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('c', 'c', 'purple'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录翻转次数。从==低位到高位==逐位处理 a、b、c',
        'while a or b or c': lambda S, B, r: (f'`a={S.a}, b={S.b}, c={S.c}` 还有没处理的位，继续' if (S.a or S.b or S.c) else '三个数都被右移成 0：所有位处理完了'),
        'if c % 2 == 1': lambda S, B, r: (f'`c` 当前位是 ==1==：a 或 b 里至少要有一个 1' if S.c % 2 == 1 else f'`c` 当前位是 ==0==：a 和 b 的这一位都必须是 0'),
        'if a % 2 == 0 and b % 2 == 0': lambda S, B, r: ('`a`、`b` 这一位都是 0 → 或起来是 0，不满足 c 的 1' if (S.a % 2 == 0 and S.b % 2 == 0) else '`a`、`b` 至少有一个是 1 → 已经满足，不用翻转'),
        'res += 1': '需要翻转 1 次：`res` → {res}',
        'if a % 2 == 1': lambda S, B, r: ('`c` 位是 0 而 `a` 位是 1 → ==必须把 a 的这位翻成 0==' if S.a % 2 == 1 else '`a` 这位本来就是 0，不用动'),
        'if b % 2 == 1': lambda S, B, r: ('`c` 位是 0 而 `b` 位是 1 → ==必须把 b 的这位翻成 0==' if S.b % 2 == 1 else '`b` 这位本来就是 0，不用动'),
        'a //= 2': '三个数都右移一位（除以 2），处理下一位。`a` → {a}',
        'b //= 2': '`b` → {b}',
        'c //= 2': '`c` → {c}',
        'return res': '所有位处理完，最少翻转 `{res}` 次',
    },
    cards=dict(
        one_liner='c 的每一位独立：想要 1 至少一个 1，想要 0 两边都得是 0',
        complexity='时间 `O(log max(a,b,c))`，空间 `O(1)`',
        problem=['给三个正整数 `a`、`b`、`c`，可以翻转 `a` 或 `b` 二进制中的某些位（0↔1）',
                 '求使 `a OR b == c` 的最少翻转次数',
                 '示例：`a=2, b=6, c=5` → `3`'],
        quote='若c当前位为1，且a和b对应的位都为0，那么需要一次操作，将a或b中对应的位变为1。若c当前位为0，若a对应的位为1，需要一次操作；若b对应的位为1，需要一次操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['或运算按位独立：每一位只由 a、b 的同一位决定',
              'c 这位是 1：a、b 都是 0 才要翻 1 次（翻任意一个）',
              'c 这位是 0：a、b 里每个 1 都要翻成 0，各 1 次'],
        summary=['时间 `O(log)`，空间 `O(1)`，位数最多约 30',
                 '`c` 位为 1 且 a、b 都是 1 时不用翻；`c` 位为 0 且 a、b 都是 1 要翻 2 次',
                 '原文为 Python 2 写法，整数除法 `/= 2` 已改为 `//= 2`（Python 3 的 `/` 会变成小数）',
                 '同一思路也可写成 `a & 1`、`>> 1`，本质相同'],
    ),
)

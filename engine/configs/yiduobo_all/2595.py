CONFIG = dict(
    num=2595, title='奇偶位数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='枚举位下标 p · 与 2^p 判断',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def evenOddBit(self, n):

        res = [0, 0]
        p = 0
        while n > 0:
            if n & (1 << p) == (1 << p):
                res[p % 2] += 1
                n ^= (1 << p)
            p += 1
        
        return res
''',
    call='Solution().evenOddBit(50)',
    expect=[1, 2],
    views=[
        dict(type='array', var=lambda S: [(S['n'] >> k) & 1 for k in range(6)], pointers={'p': 'blue'},
             label='n 的二进制（下标 = 位下标 p，从右往左；处理过的 1 会被清掉）', h=240),
        dict(type='array', var='res', label='res：下标 0 = 偶数位个数，下标 1 = 奇数位个数', h=200,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['n', ('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'while n > 0': lambda S, B, r: (f'`n = {S.n}` 还有未处理的 1，继续' if S.n > 0 else '`n = 0`：所有的 1 都处理完了'),
        'if n & (1 << p)': lambda S, B, r: (f'`n & 2^{S.p}` = `{S.n & (1 << S.p)}`，'
                                            + (f'等于 `2^{S.p} = {1 << S.p}` → 这一位是 1' if S.n & (1 << S.p) == (1 << S.p) else f'不等于 `{1 << S.p}` → 这一位是 0')),
        'res[p % 2] += 1': '`p = {p}` 是{"偶" if p % 2 == 0 else "奇"}数 → `res[{p % 2}]` = =={res[p % 2]}==',
        'n ^= (1 << p)': '异或把这一位从 `n` 中去掉：`n` = {n}',
        'p += 1': '看更高一位：`p` = {p}',
        'return res': '返回 =={res}==',
    },
    cards=dict(
        one_liner='p 从 0 往上枚举，n 的第 p 位是 1 就按 p 的奇偶记数',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['统计 `n` 二进制中，偶数下标、奇数下标上 `1` 的个数（下标从右往左，从 0 开始）',
                 '示例：`50 = 110010` → `[1,2]`', '示例：`2 = 10` → `[0,1]`'],
        quote='若n在这一位上为1，那么n与2^p执行与运算的结果就应该等于2^p，此时就应该根据p的奇偶性更新答案，然后利用异或运算将2^p从n中去除。',
        quote_src='—— yiduobo 题解原文',
        idea=['用变量 `p` 从 0 开始枚举每一位', '`n & (1 << p) == (1 << p)` 说明第 `p` 位是 1，`res[p % 2] += 1`',
              '再用 `n ^= (1 << p)` 去掉这一位，`n` 变成 0 就停'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：`p` 每轮都要加一，不管这一位是不是 1，所以 `p += 1` 在 `if` 外面',
                 '去掉已处理的 1 让 `while n > 0` 能提前结束，不用跑满 32 位',
                 '原文已是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神每轮右移 `n`，yiduobo 固定 `n` 而移动掩码 `1 << p`'],
    ),
)

CONFIG = dict(
    num=3345, title='最小可整除数位乘积 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='从 n 向上枚举 · 拆数位',
    tags=[],
    code='''
class Solution(object):
    def smallestNumber(self, n, t):
        
        def check(n):
            m = 1
            while n:
                m *= n % 10
                n //= 10
            return m % t == 0

        while not check(n):
            n += 1
        
        return n
''',
    call='Solution().smallestNumber(15, 3)',
    expect=16,
    views=[
        dict(type='text', size=34, h=140, fn=lambda S: (f"`check` 拆数位：剩余 `n = {S['n']}`，乘积 `m` = =={S['m']}==" if 'm' in S['_inner'] else f"当前候选 `n = {S['n']}`")),
        dict(type='text', size=28, h=100, fn=lambda S: f"目标：`m % t == 0`，`t = {S['t']}`"),
    ],
    watch=[('n', 'n', 'blue'), ('t', 't', 'pink'), ('m', 'm', 'green')],
    captions={
        'm = 1': '`m` 存数位乘积，初始为 1',
        'while n:': lambda S, B, r: (f'`n = {S.n}` 还有数位 → 继续拆' if S.n else '数位拆完了'),
        'm *= n % 10': '取个位 `{n % 10}`：`m` = {B.m} × {n % 10} = =={m}==',
        'n //= 10': '去掉个位：`n` → {n}',
        'return m % t == 0': lambda S, B, r: (
            f'`{S.m} % {S.t} = {S.m % S.t}` → ==整除==，这个数满足要求' if S.m % S.t == 0
            else f'`{S.m} % {S.t} = {S.m % S.t} ≠ 0` → 不满足'),
        'while not check(n)': '检查 `{n}`：不满足就 `n += 1` 再试',
        'n += 1': '`n` → {n}',
        'return n': '找到了，返回 `{n}`',
    },
    cards=dict(
        one_liner='数据很小：从 n 往上一个个试',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['找 ≥ `n` 的最小整数，使各数位之积能被 `t` 整除',
                 '示例：`n=10, t=2` → `10`，`n=15, t=3` → `16`',
                 '本视频：`n=15, t=3`'],
        quote='由于n和t的数据规模都很小，只需从n开始向上枚举答案，拆分数位相乘后检测是否能被t整除即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['写一个 `check(n)`：循环 `% 10` 取个位、`// 10` 去个位，连乘',
              '`m % t == 0` 就通过',
              '不通过就 `n += 1`，直到通过'],
        summary=['时间 `O(log n)`：个位为 0 的数乘积为 0，最多试 10 个',
                 '内层函数 `check` 的参数 `n` 和外层 `n` 同名，但 `n //= 10` 只改内层',
                 '原文就是 Python 3 可运行的写法，代码未改动'],
    ),
)

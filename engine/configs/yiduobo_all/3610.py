def _col(S, i, v):
    if 'index' not in S or 'p' not in S:
        return None
    if i == S['index']:
        return 'blue'
    if i == S['index'] + S['p']:
        return 'yellow'
    return 'green' if v != -1 else None


CONFIG = dict(
    num=3610, title='目标和所需的最小质数个数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='完全背包 · 正序枚举',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def minNumberOfPrimes(self, n, m):
        
        prime_list = []
        p = 2

        def check(p):
            x = 2
            while x * x <= p:
                if p % x == 0:
                    return False
                x += 1
            return True

        cnt = 0
        f = [-1] * (n + 1)
        f[0] = 0
        while cnt < m:
            while not check(p):
                p += 1
            cnt += 1

            for index in range(n - p + 1):
                if f[index] != -1 and (f[index + p] == -1 or f[index + p] > f[index] + 1):
                    f[index + p] = f[index] + 1

            p += 1

        
        return f[n]
''',
    call='Solution().minNumberOfPrimes(8, 3)',
    expect=2,
    max_steps=80,
    skip=['prime_list = []', 'def check', 'x = 2', 'while x * x', 'if p % x', 'return False', 'x += 1', 'return True', 'for index in range'],
    views=[
        dict(type='text', fn=lambda S: (f"当前质数 `p = {S['p']}`（第 {S['cnt']} 个）" if 'cnt' in S and 'p' in S else ''), size=30),
        dict(type='array', var='f', label='f[s]：凑出和 s 最少要几个质数（-1 = 凑不出；蓝 = index，黄 = index + p）', h=330,
             pointers={'index': 'blue'}, color=_col),
    ],
    watch=[('p', 'p', 'blue'), ('cnt', 'cnt', 'pink'), ('index', 'index', 'orange'), ('f[n]', 'f[n]', 'green')],
    captions={
        'p = 2': '质数从 `2` 开始往上找',
        'cnt = 0': '`cnt` 记录已经取到几个质数',
        'f = [-1]': '`f[s]`：和为 `s` 最少用几个质数；`-1` 表示还凑不出',
        'f[0] = 0': '和为 0 不需要质数：`f[0] = 0`，其余都是 -1',
        'while cnt < m': lambda S, B, r: (f'`cnt = {S.cnt} < m = {S.m}`，还要处理下一个质数' if S.cnt < S.m else f'`cnt = {S.cnt}`，前 `{S.m}` 个质数都处理完 → 结束'),
        'while not check(p)': lambda S, B, r: f'从 `p` 往上找下一个质数 → =={S.p}==',
        'cnt += 1': '第 `{cnt}` 个质数 `p = {p}`：用它更新 `f`，`index` 从 0 到 `n - p`，==正序==枚举，同一个质数可重复用',
        'if f[index] != -1': lambda S, B, r: (
            f'`f[{S.index}] = {S.f[S.index]}`，`f[{S.index + S.p}] = {S.f[S.index + S.p]}`：' + (
                '`index` 本身凑不出，跳过' if S.f[S.index] == -1 else
                '`index + p` 还凑不出或更多 → ==在 index 基础上再加一个 p 更优==' if (S.f[S.index + S.p] == -1 or S.f[S.index + S.p] > S.f[S.index] + 1) else
                '已有的方案不比 `f[index] + 1` 差，不更新')),
        'f[index + p] = f[index] + 1': '`f[{index + p}] = f[{index}] + 1 = =={f[index + p]}==',
        'p += 1': '`p` 加 1，继续找下一个质数',
        'return f[n]': '`f[{n}] = {ret}`：凑出 {n} 最少需要 {ret} 个质数',
    },
    cards=dict(
        one_liner='把质数当物品，正序枚举就是完全背包',
        complexity='时间 `O(n·m + m√p)`，空间 `O(n)`',
        problem=['给定整数 `n` 和 `m`，从==前 m 个质数==里选若干个（每个可重复用），使和恰好为 `n`',
                 '求最少要用几个质数，凑不出返回 `-1`',
                 '本视频：`n = 8, m = 3`（质数 2、3、5）→ `2`（3 + 5）'],
        quote='非常标准的背包问题，令f[index]表示和为index所需的最少质数个数……每个质数可以使用多次，因此动态规划时应该==正序枚举==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]`：凑出和 `index` 最少的质数个数，`f[0] = 0`，其余为 `-1`',
              '对每个质数 `p`：`f[index + p] = min(f[index + p], f[index] + 1)`',
              '先从 2 开始往上找出前 `m` 个质数，找到一个就用它更新一遍 `f`'],
        summary=['完全背包：物品可重复 → 内层 `index` ==正序==；01 背包才倒序',
                 '用 `-1` 表示不可达，更新前要判断 `f[index] != -1`',
                 '质数用试除法 `check` 判断，复杂度小',
                 '原文为 Python 2 写法，代码未改动（无整数除法）'],
    ),
)

def _col(S, i, v):
    if 'index' not in S:
        return None
    if i == S['index']:
        return 'blue'
    if i in (S['index'] - 1, S['index'] - 2, S['index'] - 6):
        return 'yellow'
    return None


CONFIG = dict(
    num=3183, title='达到总和的方法数量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='完全背包 · 4 号硬币单独讨论',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def numberOfWays(self, n):

        mod = 10 ** 9 + 7
        
        f = [0] * (n + 1)
        f[0] = 1
        for index in range(1, n + 1):
            f[index] += f[index - 1]
        for index in range(2, n + 1):
            f[index] += f[index - 2]
        for index in range(6, n + 1):
            f[index] += f[index - 6]
            if f[index] >= mod:
                f[index] -= mod

        res = f[n]
        if n >= 4:
            res += f[n - 4]
            if n >= 8:
                res += f[n - 8]
        
        return res % mod
''',
    call='Solution().numberOfWays(8)',
    expect=11,
    max_steps=80,
    skip=['mod = 10', 'for index in range'],
    views=[
        dict(type='array', var='f', label='f[s]：只用 1、2、6 凑出和 s 的方案数（蓝 = index，黄 = 来源 index-1/-2/-6）', h=300,
             pointers={'index': 'blue'}, color=_col),
        dict(type='text', fn=lambda S: (f"答案 = f[{S['n']}] + f[{S['n']-4}] + f[{S['n']-8}] = ==" + str(S['res']) + '==' if 'res' in S and S['n'] >= 8 else (f"答案 = f[{S['n']}] + f[{S['n']-4}] = ==" + str(S['res']) + '==' if 'res' in S and S['n'] >= 4 else '')), size=30),
    ],
    watch=[('index', 'index', 'blue'), ('f[index]', 'f[index]', 'green'), ('res', 'res', 'orange')],
    captions={
        'f = [0]': '`f[s]`：只用面值 1、2、6 的硬币凑出和 `s` 的方案数',
        'f[0] = 1': '和为 0：什么都不选，算 `1` 种',
        'f[index] += f[index - 1]': lambda S, B, r: ('加入面值 ==1== 的硬币（正序）：' if S.index == 1 else '') + f'`f[{S.index}] += f[{S.index - 1}]`：最后一枚用 1 → =={S.f[S.index]}==',
        'f[index] += f[index - 2]': lambda S, B, r: ('再加入面值 ==2== 的硬币：' if S.index == 2 else '') + f'`f[{S.index}] += f[{S.index - 2}]`：最后一枚用 2 → =={S.f[S.index]}==',
        'f[index] += f[index - 6]': lambda S, B, r: ('最后加入面值 ==6== 的硬币：' if S.index == 6 else '') + f'`f[{S.index}] += f[{S.index - 6}]`：最后一枚用 6 → =={S.f[S.index]}==',
        'if f[index] >= mod': '没超过模数，不用减',
        'res = f[n]': '4 号硬币一枚不用：方案数 `f[{n}]` = =={res}==',
        'if n >= 4': '`n >= 4` 才可能用一枚 4',
        'res += f[n - 4]': '只用一枚 4（两枚 4 是一样的，只算一种）：剩 `{n - 4}` → 加 `f[{n - 4}]` → =={res}==',
        'if n >= 8': '`n >= 8` 才可能把两枚 4 都用上',
        'res += f[n - 8]': '两枚 4 全用：剩 `{n - 8}` → 加 `f[{n - 8}]` → =={res}==',
        'return res % mod': '`res % mod = {ret}`',
    },
    cards=dict(
        one_liner='两枚 4 只有三种用法：0 枚、1 枚、2 枚，其余是完全背包',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有无限枚面值 1、2、6 的硬币，另外只有==两枚面值 4==的硬币',
                 '求凑出总和 `n` 的方案数，对 `10^9+7` 取模',
                 '本视频：`n = 8`'],
        quote='面值为4的硬币只有两枚，那么就只有全用了、只用一枚、全都不用三种情况，分别对应的就是通过1、2、6构成面值和为n - 8、n - 4、n的方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['4 号硬币用 0 / 1 / 2 枚，剩下的和分别是 `n`、`n-4`、`n-8`，只用 1、2、6 凑',
              '`f[s]` 用完全背包：每种面值各扫一遍，`f[s] += f[s - 面值]`',
              '答案 `f[n] + f[n-4] + f[n-8]`，注意 `n >= 4`、`n >= 8` 才能加'],
        summary=['时间 `O(n)`；硬币种类固定，常数很小',
                 '一种面值扫一遍，==正序==表示这种硬币可重复用',
                 '两枚 4 完全相同：用 1 枚只算 1 种方案，不要乘 2',
                 '原文为 Python 2 写法，代码未改动（无整数除法）'],
    ),
)

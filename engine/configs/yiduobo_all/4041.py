def _fcolor(S, i, v):
    if 'usage' not in S or 's' not in S:
        return None
    if i == S['s']:
        return 'yellow'
    if S.get('x') is not None and S['s'] >= S['x'] and i == S['s'] - S['x'] and S.get('_line') in (31, 32, 33):
        return 'blue'
    return None


def _txt(S):
    if S.get('_line', 0) >= 26 and 'usage' in S:
        return '方案（体积, 操作数）从小到大：' + '，'.join(f'(=={x}==, {c})' for x, c in S['usage'])
    if 'usage' in S:
        return ('base（奇数时的除法基底）：' + '，'.join(f'({x}, {c})' for x, c in S['base'])
                + '　　usage：' + ('，'.join(f'({x}, {c})' for x, c in S['usage']) or '空'))
    return '每个数先生成所有有用的方案，再按背包处理'


CONFIG = dict(
    num=4041, title='构造子集和的最少操作次数 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包 · 奇数才值得先除后乘',
    code='''
class Solution(object):
    def minOperations(self, nums, sum):
        
        f = [-1] * (sum + 1)
        f[0] = 0
        for v in nums:
            base = [(v, 0)]
            usage = []
            x = v
            cost = 0
            while x > 1:
                cost += 1
                if x & 1:
                    x >>= 1
                    base.append((x, cost))
                else:
                    x >>= 1
                    usage.append((x, cost))
                    
            for x, cost in base:
                while x <= sum:
                    usage.append((x, cost))
                    x <<= 1
                    cost += 1
            
            usage.sort(key=lambda d:d[0])

            for s in range(sum, -1, -1):
                for x, cost in usage:
                    if s < x:
                        break
                    if f[s - x] != -1 and (f[s] == -1 or f[s] > f[s - x] + cost):
                        f[s] = f[s - x] + cost

        return f[-1]
''',
    call='Solution().minOperations([3, 2], 4)',
    expect=1,
    skip=['base = [(v', 'usage = []', 'x = v', 'cost = 0', 'for x, cost in base', 'for v in nums', 'for s in range', 'for x, cost in usage', 'if s < x', 'x <<= 1', 'cost += 1', 'while x > 1'],
    views=[
        dict(type='array', var='nums', label='nums', h=160, cell=80, color=lambda S, i, v: 'blue' if S.get('v') == v and 'v' in S else None),
        dict(type='text', fn=_txt, size=24, h=100),
        dict(type='array', var='f', label='f[s]：恰好凑出 s 的最少操作数（-1 = 凑不出；黄 = 正在更新，蓝 = f[s-x]）', h=260, cell=80,
             pointers={'s': 'yellow'}, color=_fcolor),
    ],
    watch=['v', 'x', 'cost', 's'],
    max_steps=90,
    captions={
        'f = [-1]': '`f[s]` = 恰好凑出 `s` 的最少操作数，`-1` 表示凑不出',
        'f[0] = 0': '什么都不选，和为 0，代价 0',
        'if x & 1': lambda S, B, r: (f'`x = {B.x}` 是奇数：除一次后丢了 1，==乘回去也不是原数== → 值得作为 base' if B.x & 1
                                     else f'`x = {B.x}` 是偶数：先除再乘会抵消，==没必要乘==，只记录除法结果'),
        'base.append': '`{x}` 进 base，代价 {cost}：后面还要对它不断乘 2',
        'usage.append((x, cost))': '方案 (体积 `{usage[-1][0]}`, 操作 {usage[-1][1]}) 收进 usage',
        'while x <= sum': lambda S, B, r: (f'`{S.x} <= {S.sum}`：还没超过 sum，这个体积有用' if S.x <= S.sum else f'`{S.x} > {S.sum}`：再乘 2 只会更大，停'),
        'usage.sort': '把所有方案按体积从小到大排好：`{usage}`',
        'break': '体积 `{x}` > `{s}`：放不下，后面更大，==break==',
        'if f[s - x] != -1': lambda S, B, r: (f'`s={S.s}, x={S.x}`：`f[{S.s - S.x}]` = {S.f[S.s - S.x]}，凑不出，跳过' if S.f[S.s - S.x] == -1
                                              else f'`f[{S.s - S.x}] + {S.cost}` = {S.f[S.s - S.x] + S.cost}，对比 `f[{S.s}]` = {S.f[S.s]}'),
        'f[s] = f[s - x] + cost': '`f[{s}]` 更新为 `f[{s-x}] + {cost}` = =={f[s]}==（`s` 倒序，每个数只用一次）',
        'return f[-1]': '`f[sum] = {ret}` → 答案 =={ret}==',
    },
    cards=dict(
        one_liner='只有奇数，先除后乘才有意义；其余套背包',
        complexity='时间 `O(n·sum·log x·log sum)`，空间 `O(sum)`',
        problem=['每次操作把一个数 `x` 换成 `x*2` 或 `x//2`，求最少操作数',
                 '使得某个子集的和恰好为 `sum`；做不到返回 -1',
                 '本视频：`nums=[3,2], sum=4` → `1`'],
        quote='如果除法先与乘法执行，那么就意味着后面这次乘法无法抵消前面这次除法的影响，也就是说，只有当x为奇数时，连续两步执行除法乘法才有意义。',
        quote_src='—— yiduobo 题解原文',
        idea=['不断除 2：偶数的结果直接进 `usage`，奇数的结果进 `base`',
              '`base` 里每个数再不断乘 2（不超过 `sum`），全部进 `usage`',
              '每个数是一组，`usage` 排序后按背包倒序更新 `f`'],
        summary=['`base` 不超过 `log x` 个，每个最多乘 `log sum` 次，方案数很小',
                 '`s` 倒序 + 内层遇到 `s < x` 就 break',
                 '`f` 用 -1 表示凑不出，比较前要先判断 `f[s-x] != -1`',
                 '原文代码是 Python 2 风格，但这题无需改动即可在 Python 3 运行',
                 '对比灵神：他枚举 `(a, b)` 并用哈希去重；yiduobo 用“奇数才乘”直接避开重复'],
    ),
)

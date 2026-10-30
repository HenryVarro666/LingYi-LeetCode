def _info(S):
    if 'x' not in S:
        return '把 `+` 号的数记作 P，`-` 号的记作 N：`P − N = target`，`P + N = sum` → ==P = (target + sum) / 2=='
    c = S.get('c')
    if c is None or S.get('_line', 0) < 12:
        return f'当前物品 `x = {S["x"]}`：每个数只能选一次 → ==c 倒序=='
    return f'`f[{c}] += f[{c} − {S["x"]}]`：不选 `x` 的方案数 + 选了 `x` 之后凑 `{c - S["x"]}` 的方案数'


CONFIG = dict(
    num='LCR 102', title='目标和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='转成 0-1 背包 · 恰好装满方案数',
    tags=[],
    code='''
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        target += sum(nums)
        if target < 0 or target % 2:
            return 0
        target //= 2

        f = [1] + [0] * target
        for x in nums:
            for c in range(target, x - 1, -1):
                f[c] += f[c - x]
        return f[target]
''',
    call='Solution().findTargetSumWays([1, 2, 1, 1], 3)',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='f', label='f[c]：恰好凑出 c 的方案数（蓝 = c，粉 = c − x）', h=260, cell=100,
             pointers={'c': 'blue', 'c - x': 'pink'},
             color=lambda S, i, v: ('blue' if i == S.get('c') else 'pink' if 'x' in S and 'c' in S and i == S['c'] - S['x'] else None)),
    ],
    watch=[('target', 'target', 'yellow'), ('x', 'x', 'purple'), ('c', 'c', 'blue'), ('f[target]', 'f[target]', 'green')],
    captions={
        'target += sum(nums)': '`target + sum = {target}`：`P − N = target`，`P + N = sum`，两式相加 ==2P = target + sum==',
        'if target < 0': lambda S, B, r: ('`target = {}` 是偶数且非负 → 有解'.format(S.target) if not (S.target < 0 or S.target % 2)
                                          else '`target` 为负或为奇数 → 凑不出整数 P，返回 0'),
        'target //= 2': '要选出一些数，和恰好为 `P = {target}`：变成 ==0-1 背包恰好装满==的方案数',
        'f = [1] + [0] * target': '`f[0] = 1`：什么都不选，和为 0 有 1 种；其余先是 0 种',
        'for x in nums': lambda S, B, r: (f'考虑物品 `x = {S.x}`：选或不选' if S.x != B.get('x') or B.get('c') is None else '所有物品都处理完了'),
        'for c in range': lambda S, B, r: (f'`c` 从 `{S.target}` ==倒序==到 `{S.x}`：保证 `f[c - x]` 还是上一轮（没选过当前 x）的值' if S.c == S.target
                                           else '`c` 倒序继续' if 'c' in B and B.c != S.c else '`c` 倒序继续'),
        'f[c] += f[c - x]': '`f[{c}] = {B.f[c]} + f[{c} − {x}] = {B.f[c]} + {f[c-x]}` = =={f[c]}==',
        'return f[target]': '凑出和为 `{target}` 的方案数 = =={ret}==',
    },
    cards=dict(
        one_liner='先把正负号问题转成「选一些数，和恰好为 P」的背包',
        complexity='时间 `O(n·(target+S))`，空间 `O(target+S)`',
        problem=['给正整数数组 `nums`，每个数前加 `+` 或 `-`，求结果等于 `target` 的表达式个数',
                 '示例：`nums = [1,1,1,1,1]`, `target = 3` → `5`',
                 '本视频：`[1,2,1,1]`, `target = 3` → `3`'],
        quote='target += sum(nums)  ……  target //= 2',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['设 `+` 的数之和为 `P`：`P − (S − P) = target`，得 `P = (target + S) / 2`',
              '问题变成：选若干数，和恰好为 `P` 的方案数 = 0-1 背包',
              '一维滚动数组：==c 倒序==，每个数只用一次'],
        summary=['时间 `O(n·(target+S))`，空间 `O(target+S)`',
                 '易错：`target + S` 为奇数或小于 0 时直接返回 0',
                 '易错：0-1 背包内层 ==倒序==，正序会变成完全背包',
                 '题解还给了记忆化搜索、二维递推、两个数组滚动三种写法，本视频演示最终的一维写法'],
    ),
)

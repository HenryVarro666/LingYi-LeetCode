CONFIG = dict(
    num=1774, title='最接近目标价格的甜点成本', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='枚举底座 + 配料背包（每种最多 2 份）',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def closestCost(self, baseCosts, toppingCosts, target):

        upperLimit = target + max(toppingCosts) - 1
        f = [False] * (upperLimit + 1)
        f[0] = True
        m = len(toppingCosts)
        for i in range(m):
            for j in range(upperLimit, toppingCosts[i] + toppingCosts[i] - 1, -1):
                if f[j - toppingCosts[i] - toppingCosts[i]] or f[j - toppingCosts[i]]:
                    f[j] = True
            for j in range(min(upperLimit, toppingCosts[i] + toppingCosts[i] - 1), toppingCosts[i] - 1, -1):
                if f[j - toppingCosts[i]]:
                    f[j] = True
                    
        res = baseCosts[0]
        for baseCost in baseCosts:
            if baseCost > target:
                if baseCost - target < abs(res - target):
                    res = baseCost
            else:
                lowerTarget = target - baseCost
                while lowerTarget > 0 and not f[lowerTarget]:
                    lowerTarget -= 1
                
                if target - baseCost - lowerTarget <= abs(res - target):
                    res = baseCost + lowerTarget
                
                upperTarget = target - baseCost
                while upperTarget <= upperLimit and not f[upperTarget]:
                    upperTarget += 1
                
                if upperTarget <= upperLimit and baseCost + upperTarget - target < abs(res - target):
                    res = baseCost + upperTarget
            
        return res
''',
    call='Solution().closestCost([3,10], [2,5], 9)',
    expect=8,
    views=[
        dict(type='array', var='baseCosts', label='baseCosts（底座只能选一种）', h=130, cell=60,
             color=lambda S, i, v: 'blue' if S.get('baseCost') == v and 'res' in S else None),
        dict(type='array', var='toppingCosts', label='toppingCosts（每种配料最多 2 份）', h=190, cell=60, pointers={'i': 'pink'}),
        dict(type='array', var='f', label='f[x]：配料能否凑出成本 x（绿 = 能）', h=230, cell=46,
             pointers={'j': 'yellow', 'lowerTarget': 'cyan', 'upperTarget': 'orange'},
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', h=56, size=26, fn=lambda S: (
            f"目标 `target={S['target']}`；当前最优 `res={S['res']}`（差 {abs(S['res'] - S['target'])}）" if 'res' in S else
            f"目标 `target={S['target']}`，配料成本上限 `upperLimit={S['upperLimit']}`" if 'upperLimit' in S else '')),
    ],
    watch=[('upperLimit', 'upperLimit', 'cyan'), ('j', 'j', 'yellow'), ('baseCost', 'baseCost', 'blue'), ('lowerTarget', 'lowerTarget', 'cyan'), ('upperTarget', 'upperTarget', 'orange'), ('res', 'res', 'green')],
    skip=['for j in range'],
    max_steps=90,
    captions={
        'upperLimit = target': '配料凑出的成本允许超过目标，但超过 `target + 最贵配料 - 1` 没意义 → `upperLimit = {upperLimit}`',
        'f[0] = True': '什么配料都不放，成本 0 一定能凑出',
        'for i in range(m)': lambda S, B, r: (f'处理第 `{S.i}` 种配料，成本 `{S.toppingCosts[S.i]}`：每种最多 2 份，`j` ==从大到小==，保证同一轮里不会重复叠加' if 'i' not in B or S.i != B.i else '所有配料处理完，`f` 里就是配料能凑出的全部成本'),
        'if f[j - toppingCosts[i] - ': lambda S, B, r: (lambda c, j: (f'放 2 份：`f[{j - 2 * c}]` = {S.f[j - 2 * c]}；放 1 份：`f[{j - c}]` = {S.f[j - c]} → 有一个为真，==`{j}` 能凑出==' if (S.f[j - 2 * c] or S.f[j - c]) else f'放 2 份：`f[{j - 2 * c}]` = {S.f[j - 2 * c]}；放 1 份：`f[{j - c}]` = {S.f[j - c]} → 都为假，`{j}` 凑不出'))(S['toppingCosts'][S.i], S.j),
        'if f[j - toppingCosts[i]]:': lambda S, B, r: (lambda c, j: (f'只放 1 份：`f[{j - c}]` 为真 → ==`{j}` 能凑出==' if S.f[j - c] else f'只放 1 份：`f[{j - c}]` 为假 → `{j}` 凑不出'))(S['toppingCosts'][S.i], S.j),
        'f[j] = True': '标记 `f[{j}] = True`',
        'res = baseCosts[0]': '先把第一个底座单独当作答案 `res = {res}`',
        'for baseCost in': lambda S, B, r: (f'枚举底座 `{S.baseCost}`：配料需要凑出 `target - baseCost = {S.target - S.baseCost}` 附近' if 'baseCost' not in B or S.baseCost != B.baseCost else '底座都试完了'),
        'if baseCost > target': lambda S, B, r: (f'底座 `{S.baseCost}` 已经超过目标 `{S.target}`，不放配料最接近' if S.baseCost > S.target else f'底座 `{S.baseCost}` ≤ 目标，还要配配料凑 `{S.target - S.baseCost}`'),
        'if baseCost - target < abs': lambda S, B, r: (f'超出 `{S.baseCost - S.target}` 比当前最优 `res={S.res}` 的差 `{abs(S.res - S.target)}` 更小吗？' + ('是 → 更新' if S.baseCost - S.target < abs(S.res - S.target) else '不是 → 保持')),
        'lowerTarget = target': '向下找：从 `{lowerTarget}` 起往小找第一个能凑出的配料成本',
        'lowerTarget -= 1': '`f[{B.lowerTarget}]` 为假，凑不出 → 往下走到 `{lowerTarget}`',
        'while lowerTarget > 0': lambda S, B, r: f'`f[{S.lowerTarget}]` = {S.f[S.lowerTarget]}：' + ('能凑出，向下的最近点就是它' if S.f[S.lowerTarget] else '凑不出，继续往下') if S.lowerTarget > 0 else '到 0 了（不放配料）',
        'if target - baseCost - lowerTarget <=': '向下的差 `{target - baseCost - lowerTarget}` ≤ 当前最优的差 `{abs(res - target)}`？（差相同取更小成本，所以允许 `<=` 先更新）',
        'res = baseCost + lowerTarget': '`res = {baseCost} + {lowerTarget} = {res}`',
        'upperTarget = target': '向上找：从 `{upperTarget}` 起往大找第一个能凑出的配料成本',
        'upperTarget += 1': '`f[{B.upperTarget}]` 为假 → 往上走到 `{upperTarget}`',
        'while upperTarget <=': lambda S, B, r: (f'`f[{S.upperTarget}]` = {S.f[S.upperTarget]}：' + ('能凑出，向上的最近点就是它' if S.f[S.upperTarget] else '凑不出，继续往上')) if S.upperTarget <= S.upperLimit else '超出 upperLimit，没有向上的可行点',
        'if upperTarget <= upperLimit': lambda S, B, r: (f'向上凑出 `{S.baseCost + S.upperTarget}`，比目标大 `{S.baseCost + S.upperTarget - S.target}`；当前差 `{abs(S.res - S.target)}`，要 ==严格小于== 才更新（平局保留更小的）→ ' + ('更新' if S.baseCost + S.upperTarget - S.target < abs(B.res - S.target) else '不更新，保持 `res = ' + str(S.res) + '`')),
        'return res': '最接近目标的总成本 = =={ret}==',
    },
    cards=dict(
        one_liner='枚举底座，配料用背包算出所有能凑的成本，前后各找最近点',
        complexity='时间 `O(m·U + n·U)`，`U = target + max(topping)`；空间 `O(U)`',
        problem=['选 ==恰好一种底座==，再选 ==零或多种配料==，每种配料最多 2 份',
                 '总成本是底座 + 所有配料。求最接近 `target` 的总成本，平局取更小的',
                 '示例：`baseCosts=[3,10]`，`toppingCosts=[2,5]`，`target=9` → `8`'],
        quote='底座只能选择一种，那么自然是想到枚举底座，那么问题就变成了如何搭配配料使得这些配料的成本之和最接近目标值减去底座的成本。这是一个非常典型的背包问题',
        quote_src='—— yiduobo 题解',
        idea=['`f[x]` = 配料能否凑出成本 `x`；每种配料 0、1、2 份 → 倒序枚举 `j`，两种情况分别判断',
              '上限取 `target + max(topping) - 1`：最接近的值最多超出目标一个配料的价格',
              '枚举底座，从 `target - 底座` 向下、向上各找第一个 `f` 为真的位置，取更接近的'],
        summary=['易错：每种配料最多 2 份，所以背包里要判断 `f[j-c]` 和 `f[j-2c]` 两种',
                 '平局取更小：向下的更新用 `<=`，向上的用 `<`（严格）',
                 '底座已经大于 `target` 时，不放配料才最接近',
                 '本题代码已是 Python 3 写法，无需改动'],
    ),
)

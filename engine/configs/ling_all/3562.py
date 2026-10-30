def _x(S):
    return S['_inner'].get('x')


def _full(f):
    return [r if r is not None else ['·'] * 4 for r in f] if f else None


def _info(S):
    x = _x(S)
    if x is None:
        return '树：员工 1 是根，`g[x]` 是 x 的下属；`f[k][j]`：花费恰好 j 时的最大利润'
    return (f'当前员工 `{x + 1}`：`present = {S.present[x]}`，`future = {S.future[x]}`；'
            f'k=0 原价 `{S.present[x]}`，k=1 半价 `{S.present[x] // 2}`')


CONFIG = dict(
    num=3562, title='折扣价交易股票的最大利润', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='树上背包（状态机 DP）',
    tags=['灵神题单', '难度分 2458'],
    code='''
fmax = lambda a, b: b if b > a else a

class Solution:
    def maxProfit(self, n: int, present: List[int], future: List[int], hierarchy: List[List[int]], budget: int) -> int:
        g = [[] for _ in range(n)]
        for x, y in hierarchy:
            g[x - 1].append(y - 1)

        def dfs(x: int) -> List[List[int]]:
            # 计算从 x 的所有儿子子树 y 中，能得到的最大利润之和
            sub_f = [[0] + [-inf] * budget for _ in range(2)]
            for y in g[x]:
                fy = dfs(y)
                for k, fyk in enumerate(fy):
                    nf = [0] + [-inf] * budget
                    for jy, res_y in enumerate(fyk):
                        if res_y < 0:  # 重要优化：物品价值为负数，一定不选
                            continue
                        for j in range(jy, budget + 1):
                            nf[j] = fmax(nf[j], sub_f[k][j - jy] + res_y)
                    sub_f[k] = nf

            f = [None] * 2
            for k in range(2):
                # 不买 x，转移来源为 sub_f[0]，因为对于子树来说，父节点一定不买
                f[k] = sub_f[0].copy()
                cost = present[x] // (k + 1)
                # 买 x，转移来源为 sub_f[1]，因为对于子树来说，父节点一定买
                for j in range(cost, budget + 1):
                    f[k][j] = fmax(f[k][j], sub_f[1][j - cost] + future[x] - cost)
            return f

        return max(dfs(0)[0])
''',
    call='Solution().maxProfit(2, [2, 2], [4, 5], [[1, 2]], 3)',
    expect=6,
    skip=['sub_f[k] = nf', 'for k in range(2)', 'for y in g[x]', 'res_y < 0', 'continue', 'for jy, res_y', 'for k, fyk', 'nf = [0]', 'for j in range', 'g = [[]', 'for x, y in', 'g[x - 1]', 'f = [None]'],
    max_steps=90,
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='calls', h=130),
        dict(type='table', var=lambda S: S['_inner'].get('sub_f'), label='sub_f[k][j]：儿子们合计花恰好 j 的最大利润（k=1：x 买了）', h=190,
             cols=lambda S: [str(j) for j in range(4)], rows=['k=0', 'k=1'], cell=88),
        dict(type='table', var=lambda S: S['_inner'].get('fy'), label='fy[k][j]：刚返回的儿子子树（k=1：它可半价）', h=190,
             cols=lambda S: [str(j) for j in range(4)], rows=['k=0', 'k=1'], cell=88),
        dict(type='table', var=lambda S: _full(S['_inner'].get('f')), label='f[k][j]：x 的子树，恰好花 j（k=1：x 的父节点买了）', h=190,
             cols=lambda S: [str(j) for j in range(4)], rows=['k=0', 'k=1'], cell=88),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('y', lambda S: S['_inner'].get('y'), 'pink'),
           ('k', lambda S: S['_inner'].get('k'), 'yellow'), ('cost', lambda S: S['_inner'].get('cost'), 'orange')],
    captions={
        'sub_f = [[0]': '`sub_f[k][j]`：先假设没有儿子，只有花 0 元、利润 0 的方案，其余 `-inf`（花不出这么多）',
        'fy = dfs(y)': '先递归算儿子 `{y + 1}` 的子树，==回来后再把它当一个物品组并入背包==',
        'nf[j] = fmax': lambda S, B, r: f'儿子 `{S.y + 1}` 花 `{S.jy}` 元利润 `{S.res_y}`，加上之前儿子花 `{S.j - S.jy}` 元的 `{S.sub_f[S.k][S.j - S.jy]}` → `nf[{S.j}] = {S.nf[S.j]}`',
        'sub_f[k] = nf': '`k={k}` 这一行合并完毕：`sub_f[{k}]` 换成新数组 `nf`（每个儿子只合并一次，所以不会重复选）',
        'f[k] = sub_f[0].copy()': '`k={k}`：先考虑==不买 x==，儿子们的父节点（x）没买，直接用 `sub_f[0]` 当底',
        'cost = present[x]': '`k={k}` 时 x 的价格：k=0 原价，k=1 半价，`cost = {present[x]} // {k + 1} = {cost}`',
        'f[k][j] = fmax': '==买 x==：儿子们可半价，用 `sub_f[1][{j}-{cost}] = {sub_f[1][j - cost]}`，加 `future - cost = {future[x] - cost}` → `f[{k}][{j}] = {f[k][j]}`',
        'return f': '子树 `{x + 1}` 的 `f` 算好，返回给父节点',
        'return max(dfs(0)[0])': '先 `dfs(0)` 算根的 `f`；根没有父节点，取 `k=0` 那一行，再在「恰好花 j」里取最大',
    },
    cards=dict(
        one_liner='树上背包：儿子子树是物品组，再决定买不买自己',
        complexity='时间 `O(n·budget^2)`，空间 `O(h·budget)`',
        problem=['公司是一棵树，员工 1 是 CEO；买员工 `i` 的股票花 `present[i]`，明天卖得 `future[i]`',
                 '直属上司买了股票，则本人半价买：`present // 2`',
                 '预算 `budget`，每只股最多买一次，求最大利润',
                 '示例：`present=[1,2], future=[4,3], 1→2, budget=3` → `5`'],
        quote='`dfs(x)` 返回一个长为 (budget+1)×2 的二维数组 f，其中 f[j][k]：从子树 x 中能得到的最大利润之和，预算为 j，k=0 表示 present[x] 不能半价购买，k=1 表示可以半价购买。',
        quote_src='—— 灵茶山艾府题解（状态设计）',
        idea=['站在 x：买或不买 x，决定儿子是否半价，所以状态多一维 `k`（父节点买没买）',
              '儿子们的子树互相独立，当成「物品组」做 0-1 背包合并，得到 `sub_f`',
              '不买 x：用 `sub_f[0]`；买 x：花 `cost`，用 `sub_f[1]`，再加 `future[x] - cost`',
              '写法二把状态改为「恰好花 j」，价值为负的直接跳过，更快'],
        summary=['时间：每条边合并一次，`O(budget^2)`，总共 `O(n·budget^2)`',
                 '易错：x 买不买决定的是==儿子==是否半价，所以子树状态里的 k 看的是父节点',
                 '易错：「恰好」写法里 `-inf` 表示达不到，合并前要跳过负值',
                 '原文状态是 f[j][k]，写法二把两维交换成 f[k][j]；另有「至多」写法一和字典版，思路相同',
                 '同类：树上背包 2378、337 等'],
    ),
)

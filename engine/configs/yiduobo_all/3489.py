CONFIG = dict(
    num=3489, title='零数组变换 IV', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='逐个下标求最小 k（01 背包）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 2068'],
    code='''
class Solution(object):
    def minZeroArray(self, nums, queries):
        
        res = 0
        for index, target in enumerate(nums):
            f = [False] * (target + 1)
            f[0] = True
            p = 0
            while p < len(queries) and not f[-1]:
                left, right, val = queries[p]
                p += 1
                if index < left or index > right:
                    continue
                
                for x in range(target, val - 1, -1):
                    if f[x - val]:
                        f[x] = True
            
            if not f[-1]:
                return -1

            res = max(res, p)
        
        return res
''',
    call='Solution().minZeroArray([2,0,3], [[0,2,1],[1,2,2],[0,0,1]])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（逐个下标单独求 k）', h=170, cell=70, pointers={'index': 'blue'}),
        dict(type='table', var='queries', label='queries（黄 = 刚取出的查询）', h=200, cell=60,
             cols=['l', 'r', 'val'], rows=lambda S: [f'q{k}' for k in range(len(S['queries']))],
             color=lambda S, r, c, v: 'yellow' if S.get('p') is not None and r == S['p'] - 1 and S.get('left') is not None else None),
        dict(type='array', var='f', label='f[v]：用已取出的查询能否凑出 v（绿 = 能；最右 = target）', h=200, cell=64,
             pointers={'x': 'pink'},
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('index', 'index', 'blue'), ('target', 'target', 'cyan'), ('p', 'p', 'yellow'), ('val', 'val', 'pink'), ('res', 'res', 'green')],
    skip=['for x in range(target'],
    max_steps=70,
    captions={
        'res = 0': '`res` 是各个下标所需 `k` 的最大值',
        'for index, target in': lambda S, B, r: (f'`nums[{S.index}] = {S.target}`：单独求「最少用前几个查询」凑出它' if 'index' not in B or S.index != B.index else '所有下标都算完了'),
        'f = [False]': '`f[0..{target}]`：`f[v]` 表示用已取出的查询能否恰好凑出 `v`；目标是 `f[{target}]`',
        'f[0] = True': '一个查询都不选，和为 0 → `f[0] = True`（`target = 0` 时 `f[-1]` 就是它，不用任何查询）',
        'p = 0': '`p` 是已经取出的查询个数，也就是当前的 `k`',
        'while p < len(queries)': lambda S, B, r: (f'`f[{S.target}]` 还是 False，且还有查询 → 继续取下一个' if S.p < len(S.queries) and not S.f[-1] else (f'`f[{S.target}]` 已经为 True → ==用了 {S.p} 个查询就够==，停止' if S.f[-1] else '查询取完了')),
        'left, right, val =': '取出第 `{p}` 个查询：`[{left}, {right}]`，每个选中下标减 `{val}`',
        'if index < left': lambda S, B, r: (f'下标 `{S.index}` 不在 `[{S.left}, {S.right}]` 内 → 这个查询对它没用，跳过' if S.index < S.left or S.index > S.right else f'下标 `{S.index}` 在 `[{S.left}, {S.right}]` 内，可以把 `{S.val}` 当作一个物品放进背包（下面 `x` ==从大到小==，保证它只被用一次）'),
        'if f[x - val]': lambda S, B, r: (f'`f[{S.x} - {S.val}]` = {S.f[S.x - S.val]}' + ('，==在它基础上加上 val 就能凑出 x==' if S.f[S.x - S.val] else '，凑不出 x')),
        'f[x] = True': '`f[{x}] = True`',
        'if not f[-1]': lambda S, B, r: (f'`f[{S.target}]` 仍是 False：所有查询用完也凑不出 → ==返回 -1==' if not S.f[-1] else f'`f[{S.target}]` 为 True：这个下标用前 `{S.p}` 个查询就行'),
        'res = max': '`res = max({B.res}, {p}) = {res}`：答案是各个下标所需 `k` 的最大值',
        'return res': '所有下标都能变成 0，最小的 `k` = =={ret}==',
    },
    cards=dict(
        one_liner='逐个下标单独做 01 背包，k 取最大值',
        complexity='时间 `O(n·q·U)`，空间 `O(U)`',
        problem=['每个查询 `[l, r, val]`：在 `[l, r]` 里选一个下标子集，各减 ==正好 `val`==',
                 '求最小的 `k`，使前 `k` 个查询后 `nums` 全为 0；不可能则返回 `-1`',
                 '示例：`nums=[2,0,3]`，`queries=[[0,2,1],[1,2,2],[0,0,1]]` → `3`'],
        quote='由于nums的长度不超过10，那么一个自然的想法就是分别针对nums中的每个元素计算最小的k，这些k中的最大值即为最终答案。',
        quote_src='—— yiduobo 题解',
        idea=['`nums` 很短 → 每个下标 `index` 单独算：覆盖它的查询的 `val`，能否凑出恰好 `target`？',
              '`f[v]` 表示能否凑出 `v`；倒序遍历 `x`：`f[x - val]` 为真则 `f[x]` 为真（01 背包）',
              '某一刻 `f[target]` 为真，已取出的查询数 `p` 就是这个下标的 `k`；所有下标取最大'],
        summary=['时间 `O(n·q·U)`，`U = max(nums)`；空间 `O(U)`',
                 '`target = 0` 时 `f[-1]` 就是 `f[0]`，一个查询都不用取，`p = 0`',
                 '易错：`x` 必须倒序，否则同一个查询会被重复使用',
                 '查询要「正好」减 `val`，所以是恰好凑出 `target` 的子集和，不是「最多」',
                 '本题代码已是 Python 3 写法，无需改动'],
    ),
)

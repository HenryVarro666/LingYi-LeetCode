def _ftxt(S):
    if 'f' not in S or 'i' not in S:
        return '`f[i]` = 根节点值为 `arr[i]` 的二叉树个数，初值都是 1（只有根自己）'
    i = S['i']
    return f"`f[{i}]`（根 = {S['arr'][i]}）目前 = =={S['f'][i]}==：1（只有根）+ 各种分解的方案数"


CONFIG = dict(
    num=823, title='带因子的二叉树', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='排序 + 哈希表 · 只枚举到 √val',
    tags=['灵神题单', '动态规划', '难度分 1900'],
    code='''
class Solution:
    def numFactoredBinaryTrees(self, arr: List[int]) -> int:
        arr.sort()
        idx = {x: i for i, x in enumerate(arr)}
        f = [1] * len(arr)
        for i, val in enumerate(arr):
            for j in range(i):
                x = arr[j]
                if x * x > val:
                    break
                if x * x == val:
                    f[i] += f[j] * f[j]
                    break
                if val % x == 0 and val // x in idx:
                    f[i] += f[j] * f[idx[val // x]] * 2
        return sum(f) % (10 ** 9 + 7)
''',
    call='Solution().numFactoredBinaryTrees([10, 2, 4, 5, 20, 8])',
    expect=23,
    views=[
        dict(type='array', var='arr', label='arr（已排序，从小到大算 f）', pointers={'i': 'blue', 'j': 'pink'}, h=190,
             color=lambda S, i, v: ('blue' if i == S['i'] else 'pink' if i == S['j'] else None) if 'j' in S else None),
        dict(type='array', var='f', label='f[i]：根节点值为 arr[i] 的二叉树个数', pointers={'i': 'blue'}, h=190,
             color=lambda S, i, v: 'green' if 'i' in S and i == S['i'] else None),
        dict(type='map', var='idx', label='idx：值 → 下标（判断另一个因子在不在 arr 中）', font=26, h=160,
             fmt=lambda k, v: f'{k}→{v}'),
        dict(type='text', fn=_ftxt, size=30, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'val', 'x'],
    captions={
        'arr.sort()': '先排序：分解出的因子一定比 `val` 小，所以 ==从小到大算 f== 时，用到的 `f[j]`、`f[k]` 都已算好',
        'idx = {': '哈希表 `idx`：O(1) 判断 `val // x` 是否在 `arr` 中，并取到它的下标',
        'f = [1]': '每个 `f[i]` 初值为 1：只有根节点这一棵树',
        'for i, val': '计算根节点值为 `val = {val}` 的方案数 `f[{i}]`',
        'for j in range(i)': '枚举比 `val` 小的因子 `x = arr[j]`',
        'x = arr[j]': '试因子 `x = {x}`（`val = {val}`）',
        'if x * x > val': lambda S, B, r: (f'`{S.x}² = {S.x*S.x} > {S.val}`：x 已超过 √val，更大的因子只是左右交换 → 已被 ×2 算过，==退出==' if S.x * S.x > S.val
                                          else f'`{S.x}² = {S.x*S.x} ≤ {S.val}`，x 还没超过 √val，继续'),
        'if x * x == val': lambda S, B, r: (f'`{S.x}² = {S.val}`：左右儿子都是 {S.x}，交换后还是同一棵 → 只算 `f[j]²`' if S.x * S.x == S.val
                                           else f'`{S.x}² ≠ {S.val}`，不是平方数情形'),
        'f[i] += f[j] * f[j]': '左右都是 `{x}`：`f[{j}]² = {f[j]*f[j]}`，`f[{i}]` → =={f[i]}==，然后退出循环',
        'if val % x == 0': lambda S, B, r: (f'`{S.val} % {S.x} = 0` 且 `{S.val // S.x}` 在 arr 中 → 能分解成 {S.x} × {S.val // S.x}' if S.val % S.x == 0 and S.val // S.x in S.idx
                                           else (f'`{S.val} % {S.x} = 0`，但 `{S.val // S.x}` 不在 arr 中，不能分解' if S.val % S.x == 0
                                                 else f'`{S.val} % {S.x} ≠ 0`，{S.x} 不是因子')),
        'f[i] += f[j] * f[idx': '`f[j] × f[k] × 2` = `{f[j]} × {f[idx[val // x]]} × 2`（乘 2：左右可交换），`f[{i}]` → =={f[i]}==',
        'return sum(f)': '根节点可以是任意一个数：答案 = 所有 `f[i]` 之和 = =={sum(f)}==，再对 `10^9+7` 取模',
    },
    cards=dict(
        one_liner='排序后从小到大算 f，因子只枚举到 √val，左右交换乘 2',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`arr` 中的数都大于 1 且互不相同，每个数可用任意次',
                 '非叶节点的值 = 两个儿子的值之积，数出能构成的二叉树个数（对 `10^9+7` 取模）',
                 '示例：`[2,4,5,10]` → `7`；本视频：`[10,2,4,5,20,8]` → `23`'],
        quote='例如 12 = 2×6 = 6×2，在计算答案时，其实只需要算出分解成 2 和 6 有多少种不同的二叉树，就知道分解成 6 和 2 有多少种不同的二叉树了。因此在枚举 x 时，其实不需要枚举超过 √val 的 x。',
        quote_src='—— 灵茶山艾府题解 · 五、优化',
        idea=['`f[i]` = 根为 `arr[i]` 的二叉树数：先算 1（只有根），再加上每种分解的 `f[j] × f[k]`（乘法原理）',
              '先排序：因子比 `val` 小，所以 `f[j]`、`f[k]` 一定先算好',
              '只枚举 `x² ≤ val`：`x²<val` 时左右可交换，乘 2；`x²=val` 时只算 `f[j]²`'],
        after=[dict(heading='灵神的思路演变', lines=['先写递归 `dfs(val)`，超时；改成下标当参数 + `@cache` 记忆化',
                                                  '再 1:1 翻译成递推；最后用 √val 优化去掉重复的对称分解'])],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '非叶节点必须有两个儿子；左右儿子不同时交换算不同的树，所以 ×2',
                 '`x*x == val` 时左右一样，不能乘 2，且要 `break`',
                 '只在最后取模也不会溢出（Python 本身也不会溢出）'],
    ),
)

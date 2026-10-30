_I = lambda S: S['_inner'].get('i')


def _state(S):
    if 'j' not in S['_inner']:
        return '`dfs(i, j, k)`：在 `[0, i]` 里选数，`j` = seq1 的 gcd，`k` = seq2 的 gcd（空序列 gcd = 0）'
    s = S['_inner']
    i, j, k = s['i'], s['j'], s['k']
    if i < 0:
        return f'选完了：seq1 的 gcd = `{j}`，seq2 的 gcd = `{k}` → ' + ('==相等，算 1 对==' if j == k else '不相等，0 对')
    x = S['nums'][i]
    return f'`dfs({i}, {j}, {k})`，x 取 {x}：不选 → `({j}, {k})`，放 seq1 → `({gcd(j, x)}, {k})`，放 seq2 → `({j}, {gcd(k, x)})`'


CONFIG = dict(
    num=3336, title='最大公约数相等的子序列数量', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多维 DP · 记忆化搜索（选或不选）',
    tags=['多维 DP', '数学算法', '难度分 2403'],
    code='''
class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 1_000_000_007

        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
        def dfs(i: int, j: int, k: int) -> int:
            if i < 0:
                return 1 if j == k else 0
            return (dfs(i - 1, j, k) + dfs(i - 1, gcd(j, nums[i]), k) + dfs(i - 1, j, gcd(k, nums[i]))) % MOD

        return (dfs(len(nums) - 1, 0, 0) - 1) % MOD
''',
    call='Solution().subsequencePairCount([2, 4, 2])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前考虑的 nums[i]）', cell=90, h=200, pointers={_I: 'blue'},
             pointer_labels={_I: 'i'},
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('i') else None),
        dict(type='text', fn=_state, size=24, h=110),
        dict(type='calls', h=300),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('j', "_inner.get('j')", 'pink'), ('k', "_inner.get('k')", 'cyan')],
    captions={
        'MOD = ': '`MOD = 10^9 + 7`，答案很大，中途取模',
        'if i < 0': lambda S, B, r: (f'`i = {B.i} < 0`：数都决定完了 → 到了递归边界' if B.i < 0
                                     else f'`i = {B.i} ≥ 0`：还有 `nums[{B.i}] = {B.nums[B.i]}` 没决定 → 往下分叉'),
        'return 1 if j == k': lambda S, B, r: (f'`j = {B.j}` 等于 `k = {B.k}`：两个序列 gcd 相同 → ==返回 1==' if B.j == B.k
                                             else f'`j = {B.j}` ≠ `k = {B.k}`：gcd 不同 → ==返回 0=='),
        'return (dfs(i': lambda S, B, r: (f'`dfs({B.i}, {B.j}, {B.k})` 三种互斥选法相加（不选 + 放 seq1 + 放 seq2）= =={r}=='
                                         if r is not None else
                                         f'`x = nums[{B.i}] = {B.nums[B.i]}`：不选 → `({B.j}, {B.k})`；放 seq1 → `({gcd(B.j, B.nums[B.i])}, {B.k})`；放 seq2 → `({B.j}, {gcd(B.k, B.nums[B.i])})`'),
        'return (dfs(len': lambda S, B, r: ('`dfs(n-1, 0, 0)` 把「两个序列都为空」也数进去了，==减 1== 去掉它'
                                            if r is None else f'`dfs(n-1, 0, 0) - 1` = =={r}=='),
    },
    cards=dict(
        one_liner='从右往左，每个数：不选、放 seq1、放 seq2，三选一',
        complexity='时间 `O(nU^2 log U)`，空间 `O(nU^2)`',
        problem=['`nums` 里选两个==不相交==的非空子序列 `seq1`、`seq2`',
                 '要求两个序列的 ==gcd 相等==，数一共有多少对，结果对 `10^9+7` 取模',
                 '示例：`[2, 4, 2]` → `6`'],
        quote='讨论 x = nums[i] 选或不选：……不选 dfs(i-1,j,k)；放第一个子序列 dfs(i-1,gcd(j,x),k)；放第二个子序列 dfs(i-1,j,gcd(k,x))。三种选法互斥，根据加法原理，三者相加。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['状态 `dfs(i, j, k)`：后面已选出的两个序列 gcd 分别是 `j`、`k`；规定空序列 gcd = 0',
              '边界 `i < 0`：`j == k` 才算一对合法方案，返回 1',
              '入口 `dfs(n-1, 0, 0)`，里面含「两个都空」的 1 种，所以最后减 1',
              '同样的 `(i, j, k)` 会反复出现 → `@cache` 记忆化'],
        summary=['状态数 `O(nU^2)`，每个状态里算 gcd 要 `O(log U)`',
                 '易错：空序列 gcd 记为 0，因为 `gcd(0, x) = x`；最后要减去「两个都空」的 1 种',
                 '易错：求和每一步都要取模；`@cache` 只是记忆化，不会改变递归结构',
                 '同题还可以 1:1 翻译成三维递推 `f[i+1][j][k]`，或用倍数容斥 + 莫比乌斯函数做到 `O(n + U^2)`'],
    ),
)

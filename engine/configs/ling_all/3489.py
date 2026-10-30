def _bits(S):
    if 'f' not in S or 'x' not in S:
        return []
    return [S['f'] >> k & 1 for k in range(S['x'] + 1)]


CONFIG = dict(
    num=3489, title='零数组变换 IV', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='每个下标独立 0-1 背包（bitset）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 2068'],
    code='''
class Solution:
    def minZeroArray(self, nums: List[int], queries: List[List[int]]) -> int:
        ans = 0
        for i, x in enumerate(nums):
            if x == 0:
                continue
            f = 1
            for k, (l, r, val) in enumerate(queries):
                if not l <= i <= r:
                    continue
                f |= f << val
                if f >> x & 1:
                    ans = max(ans, k + 1)
                    break
            else:
                return -1
        return ans
''',
    call='Solution().minZeroArray([2,3,1], [[0,1,1],[1,2,2],[0,1,1],[1,1,2],[2,2,1]])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（每个下标单独算）', h=170, cell=70, pointers={'i': 'blue'}),
        dict(type='table', var='queries', label='queries（黄 = 当前查询 k）', h=270, cell=60,
             cols=['l', 'r', 'val'], rows=lambda S: [f'k={k}' for k in range(len(S['queries']))],
             color=lambda S, r, c, v: ('yellow' if r == S.get('k') else None) if 'k' in S else None,
             dim=lambda S, r, c, v: ('l' in S and 'i' in S and r < len(S['queries']) and not S['queries'][r][0] <= S['i'] <= S['queries'][r][1])),
        dict(type='array', var=_bits, label='f 的比特位（1 = 子集和能恰好凑出该数；最右是目标 x）', h=150, cell=64,
             color=lambda S, i, v: 'green' if v and 'x' in S and i == S['x'] else ('blue' if v else None)),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('k', 'k', 'yellow'), ('val', 'val', 'cyan'), ('ans', 'ans', 'green')],
    max_steps=70,
    captions={
        'ans = 0': '`ans` 记录所有下标需要的最大 `k`',
        'for i, x in enumerate': lambda S, B, r: (f'`nums[{S.i}] = {S.x}`：能否用前 `k` 个询问（覆盖下标 `{S.i}`）的 `val` 凑出恰好 `{S.x}`？' if 'i' not in B or S.i != B.i else '所有下标都处理完了'),
        'if x == 0': lambda S, B, r: ('`x = 0` 本来就是 0，无需操作 → 跳过' if S.x == 0 else f'`x = {S.x}` 要凑出，继续'),
        'f = 1': '`f = 1`：二进制只有第 0 位是 1，表示「什么都不选，和为 0」',
        'for k, (l, r, val)': '第 `{k}` 个询问：`[{l}, {r}]` 减 `{val}`',
        'if not l <= i <= r': lambda S, B, r: (f'下标 `{S.i}` 不在 `[{S.l}, {S.r}]` 内，这个询问和 `nums[{S.i}]` 无关 → 跳过' if not S.l <= S.i <= S.r else f'下标 `{S.i}` 在 `[{S.l}, {S.r}]` 内，可以选它'),
        'f |= f << val': '`f |= f << {val}`：每个和都 ==加上 {val}==（选这个物品）再并上原来的（不选） → `f = {bin(f)}`',
        'if f >> x & 1': lambda S, B, r: (f'第 `{S.x}` 位是 1：已经能凑出 `{S.x}` → ==满足要求==' if S.f >> S.x & 1 else f'第 `{S.x}` 位还是 0，凑不出 `{S.x}`，继续看下一个询问'),
        'ans = max': '`nums[{i}]` 需要前 `{k + 1}` 个询问 → `ans = max({B.ans}, {k + 1}) = {ans}`',
        'else:': '',
        'return -1': '所有询问用完也凑不出 → 返回 `-1`',
        'return ans': '每个下标都满足了，最大的 `k` = =={ret}==',
    },
    cards=dict(
        one_liner='每个下标互相独立：前缀询问里选子集，凑出恰好 nums[i]',
        complexity='时间 `O(nqU/w)`，空间 `O(U/w)`',
        problem=['每个询问 `[l, r, val]`：在 `[l, r]` 内选任意下标子集，各减去 ==正好 `val`==',
                 '求最小的 `k`，使前 `k` 个询问后 `nums` 全为 0；做不到返回 `-1`',
                 '示例：`nums=[2,3,1]`，`queries=[[0,1,1],[1,2,2],[0,1,1],[1,1,2],[2,2,1]]` → `5`'],
        quote='由于题目让我们选的是范围 [l, r] 内的一个下标子集，所以每个 nums[i] 是互相独立的，可以分别计算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选出覆盖下标 `i` 的询问，其 `val` 组成 `vals`：能否选一些数，和恰好是 `nums[i]`？这是 ==0-1 背包==',
              '用 bitset（一个整数）代替布尔数组：`f |= f << val` 等价于「选或不选」',
              '一旦第 `x` 位变 1 就记录 `k+1` 并退出；每个下标的答案取最大'],
        after=[dict(heading='另外两种写法', lines=['写法一：布尔数组 `f[j] = f[j] or f[j - val]`，`j` 倒序，时间 `O(nqU)`', '方法二：二分答案 + 多重背包（二进制优化），理论更优但实测不如方法一'])],
        summary=['时间 `O(nqU/w)`，`U = max(nums)`，`w` 是机器字长；空间 `O(U/w)`',
                 '易错：`nums[i] = 0` 无需操作，要特判跳过',
                 '`for ... else`：没有中途 `break` 就说明凑不出，返回 `-1`',
                 '同类题：416. 分割等和子集（本题的简单版）'],
    ),
)

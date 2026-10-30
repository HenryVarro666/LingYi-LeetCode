NUMS = [3, 1, 8, 2, 4]


def _ncolor(S, k, v):
    i, j, line = S.get('i'), S.get('j'), S.get('_line', 0)
    if line >= 18 and 'path' in S:
        return 'green' if v in S['path'] else None
    if i is None:
        return None
    if k == i:
        return 'blue'
    if j is not None and k == j and line in (11, 12, 13):
        return 'pink'
    return None


def _fcolor(S, k, v):
    mi = S.get('max_i')
    if S.get('_line', 0) >= 14 and k == mi:
        return 'yellow'
    return None


def _info(S):
    line = S.get('_line', 0)
    if 'i' not in S or 'x' not in S:
        return '`f[i]`：以 `nums[i]` 结尾的合法子序列的最长长度'
    if line >= 18:
        return f'从 `max_i` 顺着 `from_` 往回走，得到方案 `{S.get("path")}`'
    i, x = S['i'], S['x']
    j = S.get('j')
    if j is not None and line in (11, 12, 13) and j < i:
        ok = x % S['nums'][j] == 0
        return f'`{x} % {S["nums"][j]} = {x % S["nums"][j]}` → ' + ('能接在 `nums[j]` 后面' if ok else '不是倍数，不能接')
    return f'`f[{i}] = max(f[j]) + 1`，`j < {i}` 且 `nums[j]` 整除 `{x}`'


def _if_cap(S, B, ret):
    x, j, i = S.x, S.j, S.i
    y = S.nums[j]
    if x % y:
        return f'`{x} % {y} ≠ 0`：{x} 不是 {y} 的倍数，不能接'
    if S.f[j] > S.f[i]:
        return f'`{x}` 是 `{y}` 的倍数，且 `f[{j}] = {S.f[j]} > {S.f[i]}` → 接在 {y} 后面更长'
    return f'`{x}` 是 `{y}` 的倍数，但 `f[{j}] = {S.f[j]}` 不比当前 `{S.f[i]}` 大'


CONFIG = dict(
    num=368, title='最大整除子集', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='排序 + 类 LIS 递推 + from 数组输出方案',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums.sort()

        n = len(nums)
        f = [0] * n
        from_ = [-1] * n
        max_i = 0

        for i, x in enumerate(nums):
            for j in range(i):
                if x % nums[j] == 0 and f[j] > f[i]:
                    f[i] = f[j]
                    from_[i] = j  # 记录最佳转移来源
            f[i] += 1
            if f[i] > f[max_i]:
                max_i = i  # 最长合法子序列的最后一个数的下标

        path = []
        i = max_i
        while i >= 0:
            path.append(nums[i])
            i = from_[i]
        return path  # 不需要 reverse，任意顺序返回均可
''',
    call=f'Solution().largestDivisibleSubset({NUMS})',
    expect=[8, 4, 2, 1],
    skip=['for j in range(i)', 'n = len(nums)'],
    views=[
        dict(type='text', h=70, size=26, fn=_info),
        dict(type='array', var='nums', label='nums（排序后；蓝 = i，粉 = j）', cell=84, h=210,
             pointers={'i': 'blue', 'j': 'pink'}, color=_ncolor),
        dict(type='array', var='f', label='f（黄 = max_i）', cell=76, h=140, color=_fcolor),
        dict(type='array', var='from_', label='from_（最佳转移来源下标）', cell=76, h=140),
        dict(type='array', var='path', label='path', cell=76, h=140,
             color=lambda S, k, v: 'green'),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('j', 'j', 'pink'), ('max_i', 'max_i', 'yellow')],
    captions={
        'nums.sort()': '先排序：子集变成==子序列==，只需右边是左边的倍数 → `{nums}`',
        'f = [0] * n': '`f[i]`：以 `nums[i]` 结尾的合法子序列的最长长度',
        'from_ = [-1] * n': '`from_[i]`：f[i] 从哪个 j 转移来，用来==输出具体方案==',
        'max_i = 0': '`max_i`：最长合法子序列最后一个数的下标',
        'for i, x in enumerate(nums)': lambda S, B, ret: (f'计算 `f[{S.i}]`：以 `x = {S.x}` 结尾' if 'i' not in B or S.i != B.i or 'path' in S
                                                          else 'DP 算完'),
        'if x % nums[j] == 0 and f[j] > f[i]': _if_cap,
        'f[i] = f[j]': '`f[{i}]` 暂取 `f[{j}] = {f[i]}`',
        'from_[i] = j': '记录来源：`from_[{i}] = {j}`（{x} 接在 {nums[j]} 后面）',
        'f[i] += 1': '加上 `{x}` 自己：`f[{i}] = {f[i]}`',
        'if f[i] > f[max_i]': lambda S, B, ret: (f'`f[{S.i}] = {S.f[S.i]} > f[{S.max_i}] = {S.f[S.max_i]}` → 更新最长' if S.f[S.i] > S.f[S.max_i]
                                                 else f'`f[{S.i}] = {S.f[S.i]}` 不超过当前最长 `{S.f[S.max_i]}`'),
        'max_i = i': '`max_i = {max_i}`：当前最长子序列以 `{nums[max_i]}` 结尾，长 `{f[max_i]}`',
        'path = []': '从 `max_i` 出发，顺着 `from_` 倒着找方案',
        'i = max_i': '`i = max_i = {i}`',
        'while i >= 0': lambda S, B, ret: (f'`i = {S.i} ≥ 0`，继续' if S.i >= 0 else '`i = -1`：走到子序列开头了'),
        'path.append(nums[i])': '把 `nums[{i}] = {nums[i]}` 加入 path',
        'i = from_[i]': '`i = from_[{B.i}] = {i}`',
        'return path': '返回 `{ret}`（顺序任意）',
    },
    max_steps=70,
    cards=dict(
        one_liner='排序后变成“最长倍数子序列”：照搬 300 题 LIS',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给一个==无重复==正整数集合 `nums`，找最大的子集',
                 '子集中任意两数，一个是另一个的倍数',
                 '示例：`[1,2,4,8]` → `[1,2,4,8]`；本视频：`[3,1,8,2,4]` → `[8,4,2,1]`'],
        quote='由于 x 的倍数的倍数仍然是 x 的倍数，只要相邻元素满足倍数关系，那么任意两数一定满足倍数关系。……这类似 300. 最长递增子序列',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后：选一个子序列，==相邻==两数右边是左边的倍数即可',
              '`f[i] = max(f[j]) + 1`，其中 `j < i` 且 `nums[i] % nums[j] == 0`',
              '用 `from_[i]` 记录转移来源，从 `max_i` 倒着走就能输出方案'],
        result='`f = [1, 2, 2, 3, 4]`，从 8 倒推：8 → 4 → 2 → 1',
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：必须先排序，倍数关系才有“方向”',
                 '输出方案的通用做法：`from` 数组记录转移来源，最后倒推',
                 '题解还给了记忆化搜索，以及用 `log2(maxNum/x)` 剪掉无用状态的最优性优化',
                 '同类：300 最长递增子序列'],
    ),
)

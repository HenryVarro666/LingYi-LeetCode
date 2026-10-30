def _cap_for_i(S, B, ret):
    if 'i' in B and B.i == S.i:
        return f'`f` 全部算完：`{S.f}`'
    return f'算 `f[{S.i}]`：`nums[{S.i}] = {S.x}` ==必选==，枚举它前面一个数 `nums[j]`'


def _cap_if(S, B, ret):
    if S.x > S.y:
        return f'`nums[{S.j}] = {S.y} < {S.x}` → `{S.x}` 能接在它后面，候选 `f[{S.j}] = {S.f[S.j]}`'
    return f'`nums[{S.j}] = {S.y} ≥ {S.x}` → 接不上（要==严格==递增），跳过'


def _cap_inc(S, B, ret):
    if B.f[S.i] == 0:
        return f'前面没有比 `{S.x}` 小的数 → `{S.x}` ==单独成一个子序列==：`f[{S.i}] = 1`'
    return f'再算上 `{S.x}` 自己：`f[{S.i}] = {B.f[S.i]} + 1 =` =={S.f[S.i]}=='


def _text(S):
    if 'i' not in S or 'f' not in S:
        return '`f[i]` = max( `f[j]` : j < i 且 `nums[j] < nums[i]` ) + 1'
    i = S['i']
    c = [f'f[{j}]={S["f"][j]}' for j in range(i) if S['nums'][j] < S['nums'][i]]
    body = ', '.join(c) if c else '无'
    return f"`f[{i}]` = max( {body} ) + 1"


CONFIG = dict(
    num=300, title='最长递增子序列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='线性 DP：枚举选哪个（递推）',
    code='''
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        f = [0] * len(nums)
        for i, x in enumerate(nums):
            for j, y in enumerate(nums[:i]):
                if x > y:
                    f[i] = max(f[i], f[j])
            f[i] += 1
        return max(f)
''',
    call='Solution().lengthOfLIS([0, 1, 0, 3, 2, 3])',
    expect=4,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（黄 = 当前 x，蓝 = 比 x 小的 y，红 = 接不上）', cell=96,
             pointers={'j': 'blue', 'i': 'yellow'},
             color=lambda S, k, v: 'yellow' if k == S.get('i') else
                                   (('blue' if v < S['nums'][S['i']] else 'red') if k == S.get('j') and S['j'] < S['i'] else None),
             dim=lambda S, k, v: 'i' in S and k > S['i']),
        dict(type='array', var='f', label='f[i]：以 nums[i] 结尾的 LIS 长度（黄 = 正在算，蓝 = 依赖的 f[j]）', cell=96,
             color=lambda S, k, v: 'yellow' if k == S.get('i') else
                                   ('blue' if k == S.get('j') and S['j'] < S['i'] and S['nums'][k] < S['nums'][S['i']] else None),
             dim=lambda S, k, v: 'i' in S and k > S['i']),
    ],
    watch=[('i', 'i', 'yellow'), ('x', 'x', 'yellow'), ('j', 'j', 'blue'), ('y', 'y', 'blue'), ('f[i]', 'f[i]', 'green')],
    skip=['for j, y in enumerate'],
    captions={
        'f = [0]': '`f[i]` 表示以 `nums[i]` ==结尾==的 LIS 长度，先全设 0',
        'for i, x': _cap_for_i,
        'if x > y': _cap_if,
        'f[i] = max': '取最大：`f[{i}] = max({B.f[i]}, {f[j]})` = {f[i]}（还没算 `{x}` 自己）',
        'f[i] += 1': _cap_inc,
        'return max(f)': 'LIS 可以在任何位置结尾 → 答案是 `max(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举子序列的倒数第二个数：f[i] = max(f[j]) + 1',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，求==最长严格递增子序列==的长度',
                 '子序列：删掉若干元素，不改变剩余元素的顺序',
                 '示例：`[0,1,0,3,2,3]` → `4`（如 `0,1,2,3`）'],
        before=[dict(heading='思考：选或不选？枚举选哪个？', lines=[
            '相邻无关的子序列问题（如 0-1 背包）→ 适合「==选或不选==」',
            '相邻相关的子序列问题（如本题，要比大小）→ 适合「==枚举选哪个==」',
            '`nums[i]` 必选，再枚举前一个必选的数 `nums[j]`，只需 `O(n)` 空间',
        ])],
        quote='dfs(i) 表示以 nums[i] 结尾的最长递增子序列（LIS）的长度。枚举子序列的倒数第二个数的下标是 j，如果 nums[j] < nums[i]，那么有 ==dfs(i) = dfs(j) + 1==，取最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['递推 `f[i]` 与 `dfs(i)` 定义相同，从左到右算，`f[j]` 都已算好',
              '`nums[i]` 可以==单独形成长为 1 的子序列==，所以最后要 `+1`',
              'LIS 不一定以最后一个数结尾 → 答案是 `max(f)`'],
        after=[dict(heading='方法三：贪心 + 二分，O(n log n)', lines=[
            '若 `f[3] = f[4]`，`nums[4]` 更小 → ==更容易被后面的数接上==，更大的是无用数据',
            '`g[i]`：长为 `i+1` 的递增子序列==末尾的最小值==，`g` 严格递增',
            '每个 `x`：`j = bisect_left(g, x)`，越界就 append，否则 `g[j] = x`；答案 `len(g)`',
        ])],
        summary=['两重循环 `O(n²)`；贪心 + 二分（还可原地修改 nums）做到 `O(n log n)`',
                 '易错：==严格==递增，判断用 `x > y`，相等不能接',
                 '易错：返回 `max(f)`，不是 `f[-1]`'],
    ),
)

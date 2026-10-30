def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'mx' not in S or S.get('_line', 0) < 8:
        return '`f[i][j]` = 前 `j` 个数里取 `i` 段（每段长度 ≥ m）的最大和'
    m, s = S['m'], S['s']
    return f"`f[{i}][{j}] = max(f[{i}][{j-1}], mx + s[{j}])`，`s[{j}] = {s[j]}`，`mx` = {S['mx']}"


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'mx' not in S:
        return None
    if r == i and c == j:
        return 'yellow'
    if r == i and c == j - 1:
        return 'blue'
    if r == i - 1 and c == j - S['m']:
        return 'green'
    return None


CONFIG = dict(
    num=3473, title='长度至少为 M 的 K 个子数组之和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 前缀和优化',
    tags=['灵神题单', '动态规划', '难度分 2274'],
    code='''
class Solution:
    def maxSum(self, nums: List[int], k: int, m: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))  # nums 的前缀和
        f = [[0] * (n + 1) for _ in range(k + 1)]
        for i in range(1, k + 1):
            f[i][i * m - 1] = mx = -inf
            # 左右两边留出足够空间给其他子数组
            for j in range(i * m, n - (k - i) * m + 1):
                # mx 表示最大的 f[i-1][L]-s[L]，其中 L 在区间 [(i-1)*m, j-m] 中
                mx = max(mx, f[i - 1][j - m] - s[j - m])
                f[i][j] = max(f[i][j - 1], mx + s[j])  # 不选 vs 选
        return f[k][n]
''',
    call='Solution().maxSum([1,2,-1,3,3,4], 2, 2)',
    expect=13,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=80,
             color=lambda S, i, v: 'yellow' if 'j' in S and i == S['j'] - 1 and 'mx' in S else None),
        dict(type='array', var='s', label='前缀和 s（s[j] = nums 前 j 个数之和）', h=200, cell=80,
             pointers={'j': 'pink'}),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 不选，绿 = f[i-1][j-m]）',
             h=270, cell=80, color=_cell),
        dict(type='text', fn=_formula, size=26, h=60),
    ],
    watch=['i', 'j', ('mx', 'mx', 'yellow'), ('ans', "f[k][n]", 'green')],
    captions={
        'n = len': '`n = {n}`，前缀和下标从 0 到 n',
        's = list': '前缀和：`s[j]` = 前 j 个数之和，区间和 = `s[j] - s[L]`',
        'f = [[0]': '`f[i][j]`：前 `j` 个数里取出 `i` 个子数组的最大和；第 0 行全 0（一个都不取）',
        'for i in range': lambda S, B, ret: ('`i` 已经枚举完，取 `k` 段的这一行算好了' if B.get('i') == S['i'] else f"开始算取 =={S['i']}== 个子数组的这一行"),
        'f[i][i * m - 1] = mx': '前 `{i*m-1}` 个数不够凑 `{i}` 段（每段至少 `{m}` 个）→ 设为 `-inf`，`mx` 也从 `-inf` 开始',
        'mx = max': '新增候选起点 `L = {j-m}`：`f[{i-1}][{j-m}] - s[{j-m}]` = `{f[i-1][j-m]} - {s[j-m]}`，`mx = max({B.mx}, 它) = {mx}`',
        'f[i][j] = max': '不选 `nums[{j-1}]` 得 `{f[i][j-1]}`；选它则最后一段以它结尾，得 `mx + s[{j}]`，即 `{mx} + {s[j]}` → ==f[{i}][{j}] = {f[i][j]}==',
        'return f[k][n]': '答案是 `f[{k}][{n}]` = =={f[k][n]}==',
    },
    skip=['for j in range'],
    cards=dict(
        one_liner='把 max(f[i-1][L] - s[L]) 用一个变量 mx 滚动维护',
        complexity='时间 `O((n-km)k)`，空间 `O(nk)`',
        problem=['在 `nums` 里选 `k` 个不重叠子数组，每个长度 `≥ m`，求最大和',
                 '示例：`nums=[1,2,-1,3,3,4]`，`k=2`，`m=2` → `13`',
                 '最优：`[1,2]` 和 `[3,3,4]`，和为 `3+10`'],
        quote='按照划分型 DP 的套路，定义 f[i][j] 表示从长为 j 的前缀 nums[0] 到 nums[j-1] 取出 i 个连续子数组所得到的最大和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分类讨论：不选 `nums[j-1]` 就是 `f[i][j-1]`；选它则枚举最后一段左端点 `L`',
              '选的情况 `f[i-1][L] + s[j] - s[L]`，把与 `j` 无关的部分提出来：`s[j] + (f[i-1][L] - s[L])`',
              '`L` 随 `j` 右移只会新增一个，用 `mx` 维护最大值，枚举 `L` 的一层循环就省掉了'],
        summary=['时间 `O((n-km)k)`，空间 `O(nk)`；灵神还给了滚动数组版本，空间 `O(n)`',
                 '`f[i][i*m-1] = -inf`：不合法状态用负无穷，`max` 不会选到',
                 '`j` 的范围要给前后其他子数组留出 `m` 的空间，`L` 最小为 `(i-1)*m`',
                 '相似题：5.3 节约束划分个数的划分型 DP'],
    ),
)

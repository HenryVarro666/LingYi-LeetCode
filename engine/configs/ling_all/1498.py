CONFIG = dict(
    num=1498, title='满足条件的子序列数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 相向双指针 + 2 的幂',
    tags=['灵神题单·滑动窗口与双指针', '难度分 2276'],
    code='''
MOD = 1_000_000_007
MX = 100_000

pow2 = [1] * MX  # pow2[i] = 2 ** i % MOD
for i in range(1, MX):
    pow2[i] = pow2[i - 1] * 2 % MOD

class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        nums.sort()
        ans = 0
        left, right = 0, len(nums) - 1
        while left <= right:  # 可以相等，此时子序列的最小最大是同一个数
            if nums[left] + nums[right] <= target:
                # nums[left] 可以作为子序列的最小值
                # 其余下标在 [left+1,right] 中的数选或不选都可以
                ans += pow2[right - left]
                left += 1
            else:
                # nums[right] 太大了，即使与剩余元素的最小值 nums[left] 相加也不满足要求
                right -= 1
        return ans % MOD
''',
    call='Solution().numSubseq([3, 2, 7, 4, 3, 6], 12)',
    expect=61,
    views=[
        dict(type='array', var='nums', h=230, label='nums（排序后；蓝 = left，粉 = right）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else None) if 'right' in S else None),
        dict(type='text', fn=lambda S: (f"`{S['nums'][S['left']]} + {S['nums'][S['right']]}` = =={S['nums'][S['left']] + S['nums'][S['right']]}==，target = {S['target']}；以 `nums[left]` 为最小值，其余 `{S['right'] - S['left']}` 个数可选可不选 → `2^{S['right'] - S['left']}` 种"
                                 if 'right' in S and S['left'] <= S['right'] else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort': '只关心最小值和最大值，不关心位置 → ==先排序==：子序列第一个数最小，最后一个数最大',
        'left, right = 0': '`left`、`right` 是剩余元素的最小、最大下标：`left = 0`，`right = {right}`',
        'while left <= right': lambda S, B, r: ('`left <= right`：还有剩余元素，继续（相等时子序列只有一个数）' if S.left <= S.right
                                                else f'`left = {S.left} > right = {S.right}`：没有剩余元素 → 结束'),
        'if nums[left] + nums[right] <= target': lambda S, B, r: (
            f'`{S.nums[S.left]} + {S.nums[S.right]} = {S.nums[S.left] + S.nums[S.right]} <= {S.target}`：最小值 `nums[left]` 配最大值 `nums[right]` 合法，配更小的当然也合法'
            if S.nums[S.left] + S.nums[S.right] <= S.target else
            f'`{S.nums[S.left]} + {S.nums[S.right]} = {S.nums[S.left] + S.nums[S.right]} > {S.target}`：`nums[right]` 连最小的 `nums[left]` 都配不上，更配不上更大的'),
        'ans += pow2': '`nums[left]` 作最小值，其余 `{right - left}` 个数各选或不选 → `2^{right - left} = {ans - B.ans}` 种，`ans` → {ans}',
        'left += 1': '`nums[left]` 作最小值的情况已全部算完，去掉它：`left` → {left}',
        'right -= 1': '`nums[right]` 不可能当最大值，去掉它：`right` → {right}',
        'return ans': '最后才对 `10^9 + 7` 取模：`{ans} % MOD = {ans % MOD}`',
    },
    cards=dict(
        one_liner='排序后相向双指针：每次删掉一个端点，并一次数完它的所有方案',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`，不计预处理',
        problem=['统计 `nums` 中「最小值 + 最大值 `<= target`」的非空子序列个数，结果对 `10^9+7` 取模',
                 '示例：`nums = [3,5,6,7], target = 9` → `4`',
                 '本视频：`[3,2,7,4,3,6], target = 12` → `61`（63 个非空子序列里 2 个不合法）'],
        quote='虽然本题要求的是子序列，但由于我们只关心子序列的最小值和最大值，并不关心元素的位置，所以可以先把 nums 排序，从而方便计算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，子序列的第一个数最小、最后一个数最大',
              '`nums[left] + nums[right] <= target`：选 `nums[left]` 作最小值，中间 `right - left` 个数随便选 → `2^(right-left)`',
              '否则 `nums[right]` 太大，直接丢掉；最小最大可以是同一个数，所以是 `left <= right`'],
        summary=['预处理 `pow2`，中途不取模也行（Python 大整数），最后统一 `% MOD`',
                 '易错：`while left <= right`，相等时单个元素也是合法子序列',
                 '思考题：改成差 `<= target` 要用同向双指针（滑动窗口）',
                 '前置题：2824 统计和小于目标的下标对数目'],
    ),
)

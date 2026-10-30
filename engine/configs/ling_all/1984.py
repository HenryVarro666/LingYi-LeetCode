CONFIG = dict(
    num=1984, title='学生分数的最小差值', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 定长窗口',
    tags=['贪心与思维', '难度分 1306'],
    code='''
class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        nums.sort()
        n = len(nums)
        return min(nums[i] - nums[i - k + 1] for i in range(k - 1, n))
''',
    call='Solution().minimumDifference([9,4,1,7,12,5], 3)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: ('各窗口 `nums[i] − nums[i-k+1]`：' + '； '.join(f"{S['nums'][i]}−{S['nums'][i-S['k']+1]} = =={S['nums'][i]-S['nums'][i-S['k']+1]}==" for i in range(S['k']-1, len(S['nums']))) + f"  → 最小 =={min(S['nums'][i]-S['nums'][i-S['k']+1] for i in range(S['k']-1, len(S['nums'])))}==") if 'n' in S else ''),
        dict(type='array', var='nums', h=300,
             color=lambda S, i, v: ('green' if (lambda m: m - S['k'] + 1 <= i <= m)(min(range(S['k']-1, len(S['nums'])), key=lambda j: S['nums'][j]-S['nums'][j-S['k']+1])) else None) if 'n' in S else None),
    ],
    watch=['k', 'n'],
    captions={
        'nums.sort()': '先排序：这样选 `k` 个数的最大、最小值就是窗口两端：`{nums}`',
        'n = len': '`n = {n}`',
        'return min': '最大值下标 `i` 从 `k-1` 到 `n-1`，最小值取 `i-k+1`（最小值越小差越大，所以贴着最大值选）；取所有差的最小值 `{ret}`',
    },
    cards=dict(
        after=[dict(heading='为什么贴着最大值选', lines=['固定最大值 `nums[i]`，其余 `k-1` 个数都在它左边', '最小值的下标最多是 `i-k+1`（中间还要塞 `k-2` 个数）', '最小值越小，差越大 → 取 `i-k+1` 最优', '所以只需检查 `n-k+1` 个连续窗口'])],
        one_liner='排序后，选 k 个数的最优解一定是连续的 k 个',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`nums[i]` 是第 `i` 名学生的分数，选出 `k` 名，使最高分与最低分之差最小',
                 '示例：`nums=[9,4,1,7], k=2` → `2`',
                 '本视频：`[9,4,1,7,12,5], k=3` → `3`'],
        quote='如果 nums[i] 是 k 个数中的最大值，那么最小值的下标至多为 i-k+1。但最小值越小，差值越大，所以最小值的下标恰好为 i-k+1 是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先排序，数轴上从小到大排好', '枚举最大值 `nums[i]`，最小值只能在 `i-k+1` 及更左，越靠左差越大', '所以最小值就取 `nums[i-k+1]`，对所有 `i` 取最小差'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '`i` 从 `k-1` 开始，保证 `i-k+1 >= 0`',
                 '`k = 1` 时每个窗口只有自己，答案 0',
                 '写法二：`zip(nums[k-1:], nums)` 同时遍历最大值与最小值，思路相同',
                 '原文代码用制表符缩进，这里统一成 4 个空格；同类：排序后看定长窗口的题'],
    ),
)

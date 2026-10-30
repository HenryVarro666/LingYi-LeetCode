def _orline(S):
    if 'i' not in S or 'x' not in S:
        return ''
    if 'j' in S and S['_line'] >= 8:
        return f"右端点 `i={S['i']}`，`x={S['x']}`：`nums[j]` 现在 = 从 `j` 到 `i` 的或值 = ==`{S['nums'][S['j']]}`=="
    return f"右端点 `i={S['i']}`，`x = nums[i] = {S['x']}`"


CONFIG = dict(
    num=2411, title='按位或最大的最小子数组长度', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='LogTrick · 原地维护后缀或值',
    tags=['灵神题单·位运算', '难度分 1938'],
    code='''
class Solution:
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        ans = [1] * len(nums)  # 子数组的长度至少是 1
        for i, x in enumerate(nums):  # 计算右端点为 i 的子数组的或值
            for j in range(i - 1, -1, -1):
                if (nums[j] | x) == nums[j]:  # nums[j] 及其左边元素无法增大
                    break
                nums[j] |= x  # nums[j] 增大，现在 nums[j] = 原数组 nums[j] 到 nums[i] 的或值
                ans[j] = i - j + 1  # nums[j] 最后一次增大时的子数组长度就是答案
        return ans
''',
    call='Solution().smallestSubarrays([1,0,2,1,3])',
    expect=[3, 3, 2, 2, 1],
    views=[
        dict(type='text', fn=_orline, h=60),
        dict(type='array', var='nums', label='nums（原地改成：下标 j 到 i 的或值）', pointers={'j': 'blue', 'i': 'pink'}, h=200),
        dict(type='array', var='ans', label='ans（最后一次增大时的长度）', h=170,
             color=lambda S, i, v: 'green' if S.get('j') == i and S['_line'] >= 8 else None),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), 'x'],
    captions={
        'ans = [1]': '每个位置至少自己一个数，长度先填 `1`',
        'for i, x in': lambda S, B, r: ('所有右端点都处理完了，循环结束' if B.get('i') == S.i and 'i' in B else
                                       f'右端点来到 `i = {S.i}`，新元素 `x = {S.x}`：把它的 1 往左“传”给还能变大的数'),
        'for j in range': lambda S, B, r: ('`i = 0` 左边没有元素，内层循环为空' if 'j' not in S else
                                          '`j` 已扫到最左端，内层循环结束' if B.get('j') == S.j else
                                          f'从 `i-1` 往左扫，`j = {S.j}`'),
        'if (nums[j] | x)': lambda S, B, r: (f"`{S.nums[S.j]} | {S.x} = {S.nums[S.j] | S.x}`：==或不出新的 1== → `nums[j]` 及其左边都已包含 x，左边只会更饱和，直接 break")
                            if (S.nums[S.j] | S.x) == S.nums[S.j] else
                            f"`{S.nums[S.j]} | {S.x} = {S.nums[S.j] | S.x}` ≠ `{S.nums[S.j]}`：x 带来了新的 1 → 继续更新",
        'break': '`break`：这一轮 x 到此为止，`j` 左边的答案都不会变了',
        'nums[j] |= x': '`nums[j]` 增大为 `{nums[j]}`：它现在就是 `[j, i]` 的或值',
        'ans[j] = i - j + 1': '`nums[j]` 刚增大 → 说明 `nums[i]` 是 `j` 开始必须包含的最远位置 → `ans[{j}] = {i} - {j} + 1 = =={ans[j]}==`',
        'return ans': '每个位置最后一次增大时的长度就是答案：`{ans}`',
    },
    cards=dict(
        one_liner='固定右端点，往左更新或值；一旦不增大就停',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['对每个下标 `i`，求以 `i` 开头、按位或值最大的 ==最短== 子数组长度',
                 '示例：`[1,0,2,1,3]` → `[3,3,2,2,1]`'],
        quote='nums[j] 增大，现在 nums[j] = 原数组 nums[j] 到 nums[i] 的或值；nums[j] 最后一次增大时的子数组长度就是答案',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['把 `nums[j]` 原地改成「`j` 到当前 `i` 的或值」',
              '或值只会加 1，每个数最多增大 30 次；一旦 `nums[j] | x == nums[j]`，更左边的也不会再变，直接 `break`',
              '`ans[j]` 被最后一次覆盖时，`i` 就是让或值到达最大的最短右端点'],
        summary=['时间 `O(n log U)`，`U < 2^30`，每个数最多增大 30 次',
                 '会原地修改 `nums`；`ans` 初始为 1，因为子数组至少一个元素',
                 '灵神还给了「滑动窗口 + 栈」的 `O(n)` 写法，这里只演示 LogTrick',
                 '同类题：LogTrick 系列（AND / OR / GCD）'],
    ),
)

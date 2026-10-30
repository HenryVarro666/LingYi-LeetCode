CONFIG = dict(
    num=2420, title='找到所有好下标', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解',
    tags=['灵神题单·动态规划', '难度分 1695'],
    code='''
class Solution:
    def goodIndices(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        ans = []
        dec = [1] * n
        for i in range(n - 2, k, -1):
            if nums[i] <= nums[i + 1]:
                dec[i] = dec[i + 1] + 1  # 递推
        inc = 1
        for i in range(1, n - k):
            if inc >= k and dec[i + 1] >= k:
                ans.append(i)
            if nums[i - 1] >= nums[i]:
                inc += 1  # 递推
            else:
                inc = 1
        return ans
''',
    call='Solution().goodIndices([2,1,1,1,3,4,1], 2)',
    expect=[2, 3],
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=80, pointers={'i': 'blue'},
             color=lambda S, j, v: 'green' if j in S.get('ans', []) else None),
        dict(type='array', var='dec', label='dec[i]：从 i 往后的最长非递减长度', h=170, cell=80),
        dict(type='text', h=70, size=26,
             fn=lambda S: (f"向前非递增长度 `inc = {S['inc']}`，向后非递减长度 `dec[i+1]` = {S['dec'][S['i']+1]}，k = {S['k']}"
                           if 'inc' in S and 'i' in S and S['i'] + 1 < len(S['nums']) and S.get('_line', 0) >= 11
                           else '先从右往左填 `dec`，再从左往右维护 `inc` 并判断')),
    ],
    watch=[('i', 'i', 'blue'), 'k', 'inc', ('ans', 'ans', 'green')],
    captions={
        'dec = [1] * n': '`dec[i]`：从下标 `i` 往后的最长非递减段长度，先全设为 1',
        'for i in range(n - 2, k, -1)': '==倒着==遍历：`dec[i]` 要用到右边的 `dec[i+1]`',
        'if nums[i] <= nums[i + 1]': '`nums[{i}] = {nums[i]}` 与 `nums[{i+1}] = {nums[i+1]}`：{"不大于右边，能接上" if nums[i] <= nums[i+1] else "比右边大，断开，dec 保持 1"}',
        'dec[i] = dec[i + 1] + 1': '`dec[{i}] = dec[{i+1}] + 1` = =={dec[i]}==：往后的非递减段延长了一格',
        9: '`inc` 记录以 `i-1` 结尾的最长非递增段，初始为 1',
        'for i in range(1, n - k)': '`i` 从 1 到 `n-k-1`：==正着==遍历，一边维护 `inc` 一边判断下标 `i`',
        'if inc >= k and': '前面 `inc = {inc}`，后面 `dec[{i+1}] = {dec[i+1]}`：{"都 ≥ k，下标 i 是好下标" if inc >= k and dec[i+1] >= k else "至少一边不足 k，不是好下标"}',
        'ans.append(i)': '下标 `{i}` 满足 → 加入答案 `{ans}`',
        'if nums[i - 1] >= nums[i]': '为下一个下标准备：`nums[{i-1}] = {nums[i-1]}` 与 `nums[{i}] = {nums[i]}`，{"前者不小于后者，非递增段可延长" if nums[i-1] >= nums[i] else "出现上升，非递增段断开"}',
        'inc += 1': '`inc` 加一 → =={inc}==',
        16: '出现上升，非递增段断开：`inc` 重置为 =={inc}==',
        'return ans': '好下标：`{ans}`',
    },
    cards=dict(
        one_liner='倒着算后缀、正着算前缀，边走边判断',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 和正整数 `k`，下标 `i`（`k <= i < n-k`）前 `k` 个元素非递增、后 `k` 个元素非递减，则 `i` 是好下标',
                 '按升序返回所有好下标',
                 '示例：`nums = [2,1,1,1,3,4,1], k = 2` → `[2,3]`'],
        quote='先倒着遍历，得到从每个位置向后的最长连续非降序列的长度，然后正着遍历，得到每个位置向前的最长连续非增序列的长度，同时统计答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['后缀信息 `dec[i]` 先倒着预处理好',
              '前缀信息 `inc` 只用一个变量，正着遍历时顺手维护',
              '在判断下标 `i` 之前，`inc` 刚好是以 `i-1` 结尾的非递增段长度'],
        summary=['时间 `O(n)`，空间 `O(n)`（`inc` 用变量，只有 `dec` 是数组）',
                 '易错：`inc` 的更新放在判断之后，保证判断时 `inc` 对应 `i-1`',
                 '易错：`dec[i+1]` 对应 `i` 之后的一段，不含 `i` 自己',
                 '灵神思考题：子数组改成子序列就变成 LIS'],
    ),
)

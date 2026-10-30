CONFIG = dict(
    num=2903, title='找出满足差值条件的下标 I', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举右维护左 · 前缀最值', tags=[],
    code='''
class Solution:
    def findIndices(self, nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
        max_idx = min_idx = 0
        for j in range(indexDifference, len(nums)):
            i = j - indexDifference
            if nums[i] > nums[max_idx]:
                max_idx = i
            elif nums[i] < nums[min_idx]:
                min_idx = i
            if nums[max_idx] - nums[j] >= valueDifference:
                return [max_idx, j]
            if nums[j] - nums[min_idx] >= valueDifference:
                return [min_idx, j]
        return [-1, -1]
''',
    call='Solution().findIndices([3,5,2,6,1,9], 2, 5)',
    expect=[2, 5],
    views=[
        dict(type='array', var='nums', h=260, label='nums', pointers={'max_idx': 'pink', 'min_idx': 'cyan', 'j': 'blue'},
             window=(0, 'j - indexDifference'),
             color=lambda S, i, v: 'pink' if i == S.get('max_idx') else 'cyan' if i == S.get('min_idx') else ('blue' if i == S.get('j') else None)),
        dict(type='text', size=32, fn=lambda S: f"左侧可用 `[0, {S['j']-S['indexDifference']}]`：最大 =={S['nums'][S['max_idx']]}==，最小 =={S['nums'][S['min_idx']]}==" if 'j' in S and 'max_idx' in S else ''),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i'), ('max_idx', 'max_idx', 'pink'), ('min_idx', 'min_idx', 'cyan')],
    captions={
        'max_idx = min_idx': '`max_idx` / `min_idx` 记录左侧可用区间里最大、最小值的下标，初始为 0',
        'for j in range': '枚举右边的 `j = {j}`，左边的 `i` 要满足 `i ≤ j - {indexDifference}`',
        'i = j - indexDifference': '`i = {j} - {indexDifference} = {i}`：==刚好进入可用区间的新下标==',
        'if nums[i] > nums[max_idx]': '`nums[{i}] = {nums[i]}` 比当前最大 `{nums[max_idx]}` {"大" if nums[i] > nums[max_idx] else "不大"}',
        'max_idx = i': '更新最大值下标 → `max_idx = {i}`',
        'elif nums[i] < nums[min_idx]': '`nums[{i}] = {nums[i]}` 比当前最小 `{nums[min_idx]}` {"小" if nums[i] < nums[min_idx] else "不小"}',
        'min_idx = i': '更新最小值下标 → `min_idx = {i}`',
        'if nums[max_idx] - nums[j]': '最大值减当前：`{nums[max_idx]} - {nums[j]} = {nums[max_idx]-nums[j]}` {"≥" if nums[max_idx]-nums[j] >= valueDifference else "<"} `{valueDifference}`',
        'return [max_idx, j]': '最大值与 `j` 的差够大 → 返回 `[{max_idx}, {j}]`',
        'if nums[j] - nums[min_idx]': '当前减最小值：`{nums[j]} - {nums[min_idx]} = {nums[j]-nums[min_idx]}` {"≥" if nums[j]-nums[min_idx] >= valueDifference else "<"} `{valueDifference}`',
        'return [min_idx, j]': '`j` 与最小值的差够大 → 返回 `[{min_idx}, {j}]`',
        'return [-1, -1]': '所有 `j` 都试过，没有满足的 → `[-1, -1]`',
    },
    cards=dict(
        one_liner='枚举右端点 j，左边只需看最大值和最小值',
        complexity='时间 `O(n - indexDifference)`，空间 `O(1)`',
        problem=['找下标 `i, j`，要求 `|i-j| ≥ indexDifference` 且 `|nums[i]-nums[j]| ≥ valueDifference`',
                 '找不到返回 `[-1, -1]`，`i` 和 `j` 可以相等',
                 '本视频：`[3,5,2,6,1,9]`，下标差 2，值差 5'],
        quote='枚举 j，寻找左边的 i。要想满足绝对值不小于 valueDifference，要找的 nums[i] 应当尽量大或者尽量小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不妨设 `i` 在左：枚举 `j`，左边可用的是 `[0, j - indexDifference]`',
              '只需维护这段里的 ==最大值下标 和 最小值下标==，类似买卖股票',
              '只检查 `最大 - nums[j]` 和 `nums[j] - 最小` 两个不等式，不用绝对值'],
        summary=['时间 `O(n - indexDifference)`，空间 `O(1)`',
                 '`j` 从 `indexDifference` 开始，保证 `i = j - indexDifference ≥ 0`',
                 '不用绝对值：若 `nums[j]-max ≥ d`，则 `nums[j]-min` 更大，也满足',
                 '只记下标而不记值：下标能推出值，还能直接返回'],
    ),
)

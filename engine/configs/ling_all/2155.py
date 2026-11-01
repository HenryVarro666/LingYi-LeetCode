CONFIG = dict(
    num=2155, title='分组得分最高的所有下标', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='一次遍历，边扫边维护左 0 右 1（Go 原文转写）', tags=[],
    code='''
class Solution:
    def maxScoreIndices(self, nums: List[int]) -> List[int]:
        left, right = 0, 0
        for i in range(len(nums) - 1, -1, -1):
            right += nums[i]  # 先算出整个数组的 1 的个数
        maxSum = right
        ans = [0]
        for i, v in enumerate(nums):
            left += v ^ 1  # 不断增加左边 0 的个数
            right -= v  # 减少右边 1 的个数
            if left + right > maxSum:  # 更新答案
                maxSum = left + right
                ans = [i + 1]
            elif left + right == maxSum:
                ans.append(i + 1)
        return ans
''',
    call='Solution().maxScoreIndices([0,0,1,0,1,0])',
    expect=[2, 4, 6],
    views=[
        dict(type='array', var='nums', h=200, pointers={'i': 'blue'},
             color=lambda S, i, v: ('blue' if i == S['i'] else None) if 'v' in S else None,
             dim=lambda S, i, v: 'v' in S and i > S['i']),
        dict(type='text', h=90, fn=lambda S: (
            f"切在下标 `{S['i']+1}`：左边 0 有 `{S['left']}` 个 + 右边 1 有 `{S['right']}` 个 = =={S['left']+S['right']}==（目前最高 `{S['maxSum']}`）"
            if 'v' in S and 'i' in S else '')),
        dict(type='array', var='ans', label='ans（得分最高的切分下标）', h=150),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('maxSum', 'maxSum', 'green')],
    captions={
        'left, right = 0, 0': '`left` = 左边 0 的个数，`right` = 右边 1 的个数；先都记 0',
        'right += nums[i]': '把 `nums[{i}] = {nums[i]}` 加进来：`right` = =={right}==（先数出全部 1，下标 0 切分时右边就是整个数组）',
        'maxSum = right': '下标 0 切分的得分就是 `right = {right}`，先当作最高分',
        'ans = [0]': '答案先放切分下标 `0`',
        'left += v ^ 1': '`v = {v}`：{"是 0，归到左边，左边 0 的个数加一" if v == 0 else "是 1，左边 0 的个数不变"} → `left = {left}`',
        'right -= v': '`v = {v}`：{"是 1，离开右边，右边 1 少一个" if v == 1 else "是 0，右边 1 的个数不变"} → `right = {right}`',
        'if left + right > maxSum': lambda S, B, r: (f'得分 `{S.left} + {S.right} = {S.left+S.right}` > 最高分 `{S.maxSum}`：创新高，之前的下标全部作废' if S.left + S.right > S.maxSum else f'得分 `{S.left+S.right}` 没超过最高分 `{S.maxSum}`，看是否打平'),
        'maxSum = left + right': '最高分更新为 `{maxSum}`',
        'ans = [i + 1]': '答案重置为只有切分下标 `{i+1}`：`{ans}`',
        'elif left + right == maxSum': lambda S, B, r: (f'得分 `{S.left+S.right}` == 最高分 `{S.maxSum}`：打平，这个下标也要' if S.left + S.right == S.maxSum else f'得分 `{S.left+S.right}` < 最高分 `{S.maxSum}`：不如已有答案，跳过'),
        'ans.append': '同分，切分下标 `{i+1}` 追加进答案：`{ans}`',
        'return ans': '最高分 `{maxSum}`，所有取到它的下标：`{ans}`',
    },
    cards=dict(
        one_liner='先数出全部 1，再随着切点右移：左 0 加、右 1 减',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['在下标 `i` 把数组切成左右两段（可空）',
                 '得分 = 左段 0 的个数 + 右段 1 的个数',
                 '返回得分最高的所有下标；示例：`[0,0,1,0]` → `[2,4]`'],
        quote='先算出整个数组的 1 的个数；不断增加左边 0 的个数，减少右边 1 的个数，更新答案。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['切在下标 0：左边为空，右边是整个数组，得分 = 全部 1 的个数',
              '切点右移一格，吃进的那个数 `v`：是 0 则 `left` 加一，是 1 则 `right` 减一',
              '每次只改一两个数就得到新得分，边扫边比较最高分'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python',
                 '切分下标有 `n+1` 个：初始放下标 0，循环里记 `i + 1`',
                 '==严格大于==才重置答案，相等要追加；`v ^ 1` 就是「是 0 则得 1」'],
    ),
)

CONFIG = dict(
    num=2905, title='找出满足差值条件的下标 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 最大最小值下标',
    tags=['灵神题单', '难度分 1764'],
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
    call='Solution().findIndices([3,5,2,4,1,9], 2, 6)',
    expect=[2, 5],
    views=[
        dict(type='array', var='nums', label='nums（粉 = 最大值下标，青 = 最小值下标，蓝 = j，黄 = 刚并入的 i）', h=230, cell=100,
             pointers={'max_idx': 'pink', 'min_idx': 'cyan', 'j': 'blue'},
             dim=lambda S, i, v: 'j' in S and 'i' in S and i > S['i'] and i != S['j'],
             color=lambda S, i, v: ('blue' if S.get('j') == i else 'yellow' if S.get('i') == i else None)),
        dict(type='text', size=28, h=130,
             fn=lambda S: (f"左边最大 `{S['nums'][S['max_idx']]}`，最小 `{S['nums'][S['min_idx']]}`；"
                           f"`nums[j]` = {S['nums'][S['j']]}：`{S['nums'][S['max_idx']]} − {S['nums'][S['j']]}` = {S['nums'][S['max_idx']] - S['nums'][S['j']]}，"
                           f"`{S['nums'][S['j']]} − {S['nums'][S['min_idx']]}` = {S['nums'][S['j']] - S['nums'][S['min_idx']]}，要 ≥ =={S['valueDifference']}=="
                           if 'j' in S and 'i' in S else '左边只留最大和最小两个下标：差值要大，只能找最大或最小')),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i', 'yellow'), ('max_idx', 'max_idx', 'pink'), ('min_idx', 'min_idx', 'cyan')],
    captions={
        'max_idx = min_idx = 0': '`max_idx`、`min_idx` 记录左边最大/最小值的下标，起点都是 `0`；只存下标，值随时能查',
        'for j in range': lambda S, B, r: (f'枚举右端点 `j = {S.j}`，从 `indexDifference = {S.indexDifference}` 开始，保证左边至少有一个数' if 'j' in S and ('j' not in B or S.j != B.j) else '遍历结束，没有找到'),
        'i = j - indexDifference': '`i = {j} − {indexDifference} = {i}`：==下标刚好相距够远的新左端点==，把它并入左边的范围',
        'if nums[i] > nums[max_idx]': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} > nums[{S.max_idx}] = {S.nums[S.max_idx]}` → 成立，它是新的最大值' if S.nums[S.i] > S.nums[S.max_idx] else f'`nums[{S.i}] = {S.nums[S.i]}` 不比最大值 `{S.nums[S.max_idx]}` 大'),
        'max_idx = i': '最大值下标更新为 `{max_idx}`（值 `{nums[max_idx]}`）',
        'elif nums[i] < nums[min_idx]': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} < nums[{S.min_idx}] = {S.nums[S.min_idx]}` → 成立，它是新的最小值' if S.nums[S.i] < S.nums[S.min_idx] else f'`nums[{S.i}] = {S.nums[S.i]}` 也不比最小值 `{S.nums[S.min_idx]}` 小，左边不变'),
        'min_idx = i': '最小值下标更新为 `{min_idx}`（值 `{nums[min_idx]}`）',
        'if nums[max_idx] - nums[j]': lambda S, B, r: (f'`{S.nums[S.max_idx]} − {S.nums[S.j]} = {S.nums[S.max_idx] - S.nums[S.j]}` ≥ {S.valueDifference} → ==成立=={chr(65292)}最大值够远' if S.nums[S.max_idx] - S.nums[S.j] >= S.valueDifference else f'`{S.nums[S.max_idx]} − {S.nums[S.j]} = {S.nums[S.max_idx] - S.nums[S.j]}` < {S.valueDifference}，最大值离 j 不够远'),
        'return [max_idx, j]': '找到：`[{max_idx}, {j}]`',
        'if nums[j] - nums[min_idx]': lambda S, B, r: (f'`{S.nums[S.j]} − {S.nums[S.min_idx]} = {S.nums[S.j] - S.nums[S.min_idx]}` ≥ {S.valueDifference} → ==成立=={chr(65292)}最小值够远' if S.nums[S.j] - S.nums[S.min_idx] >= S.valueDifference else f'`{S.nums[S.j]} − {S.nums[S.min_idx]} = {S.nums[S.j] - S.nums[S.min_idx]}` < {S.valueDifference}，最小值也不够远'),
        'return [min_idx, j]': '找到：`[{min_idx}, {j}]`',
        'return [-1, -1]': '所有 j 都试过，没有满足的下标对',
    },
    cards=dict(
        one_liner='枚举右 j，左边只需要最大值和最小值的下标',
        complexity='时间 `O(n − indexDifference)`，空间 `O(1)`',
        problem=['找下标 `i, j`：`|i − j| ≥ indexDifference` 且 `|nums[i] − nums[j]| ≥ valueDifference`',
                 '有解返回 `[i, j]`，否则 `[-1, -1]`',
                 '本视频：`nums=[3,5,2,4,1,9]`，`indexDifference=2`，`valueDifference=6` → `[2,5]`'],
        quote='要找的 nums[i] 应当尽量大或者尽量小。……在枚举 j 的同时，维护 nums[0] 到 nums[j - indexDifference] 中的最大值 mx 和最小值 mn。',
        quote_src='—— 灵茶山艾府题解',
        idea=['假设 i 在左：`i ≤ j − indexDifference`，左边的数随着 j 右移一个个并入',
              '绝对值要大，nums[i] 得离 nums[j] 尽量远：取左边最大或最小',
              '不用算绝对值：若最大值那边是负的，最小值只会更远'],
        summary=['时间 `O(n − indexDifference)`，空间 `O(1)`',
                 '只记下标 `max_idx`、`min_idx`，值随时能由下标查到',
                 '易错：`j` 从 `indexDifference` 开始；每轮先并入 `i = j − indexDifference`，再判断',
                 '思考题（统计对数）需要有序结构，不再是 O(1) 维护'],
    ),
)

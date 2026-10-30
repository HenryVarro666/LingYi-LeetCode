CONFIG = dict(
    num=3914, title='使数组非递减需要的最小累计值', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 · 负差分之和',
    tags=['常用数据结构', '二、差分', '难度分 1662'],
    code='''
class Solution:
    def minOperations(self, nums: list[int]) -> int:
        return sum(max(x - y, 0) for x, y in pairwise(nums))
''',
    call='Solution().minOperations([3,3,2,1,5,4])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: '差分 `d[i] = nums[i+1] − nums[i]`：' + '，'.join(f"`{S['nums'][i+1]-S['nums'][i]}`" for i in range(len(S['nums'])-1)), size=28),
        dict(type='array', var='nums', label='nums', h=200, color=lambda S, i, v: None),
        dict(type='text', fn=lambda S: '负的差分取反再求和：' + ' + '.join(f"`{max(S['nums'][i]-S['nums'][i+1],0)}`" for i in range(len(S['nums'])-1)) + f" = ==`{sum(max(S['nums'][i]-S['nums'][i+1],0) for i in range(len(S['nums'])-1))}`==", size=28),
    ],
    watch=[],
    captions={
        'return sum': '`pairwise(nums)` 取相邻两项 `(x, y)`，下降量 `max(x − y, 0)` 全部相加 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='操作只需改后缀，等价于把负的差分补成 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作选任意子数组，每个元素加同一个正整数 `x`',
                 '求让数组非递减所需的 ==`x` 之和== 的最小值',
                 '示例：`[3,3,2,1]` → `2`；`[5,1,2,3]` → `4`'],
        quote='题目让我们把 nums 变成递增的，这等价于把每个 d[i] 都变成非负数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['差分 `d[i] = nums[i+1] − nums[i]`，非递减 ⇔ 所有 `d[i] ≥ 0`',
              '子数组加 `x` = 一个差分加 `x`、另一个减 `x`；减少 `d` 没有意义',
              '所以只操作后缀，把每个负的 `d[i]` 补成 0，代价 `-d[i]`'],
        before=[dict(heading='差分数组', lines=[
            '`d[i] = nums[i+1] − nums[i]`，下标 0 不放进 `d`',
            '示例 1：`d = [0, -1, -1]`；示例 2：`d = [-4, 1, 1]`',
            '`nums[0]` 变大没有意义，所以不需要差分的首项'])],
        summary=['答案 `Σ max(nums[i-1] − nums[i], 0)`，一行搞定',
                 '时间 `O(n)`，空间 `O(1)`',
                 '`pairwise` 是 Python 3.10 的 itertools 函数，已预置',
                 '相似题：1526、3229，都是差分里「只补正/负部分」',
                 '对比 yiduobo：他用显式循环累加下降量'],
    ),
)

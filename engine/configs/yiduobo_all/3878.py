def _info(S):
    if 'res' in S:
        return '第三趟：每个数当「最左的最大值」，左 × 右 个子数组都是好子数组'
    if 'right' in S:
        return '第二趟（从右往左）：只要 x 能 cover 住栈顶（OR 后不变）就弹出'
    return '第一趟（从左往右）：x 必须严格大于栈顶且能 cover 住它才弹，等值的留作左墙'


CONFIG = dict(
    num=3878, title='统计好子数组', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='单调栈 · cover 住就弹出',
    tags=['灵神题单', '单调栈', '难度分 2230'],
    code='''
class Solution(object):
    def countGoodSubarrays(self, nums):
        
        n = len(nums)

        stack = []
        left = [-1] * n
        for index in range(n):
            while stack and nums[stack[-1]] < nums[index] and (nums[stack[-1]] | nums[index]) == nums[index]:
                stack.pop()
            if stack:
                left[index] = stack[-1]
            else:
                left[index] = -1
            stack.append(index)
        
        stack = []
        right = [n] * n
        for index in range(n - 1, -1, -1):
            while stack and (nums[stack[-1]] | nums[index]) == nums[index]:
                stack.pop()
            if stack:
                right[index] = stack[-1]
            else:
                right[index] = n
            stack.append(index)
        
        res = 0
        for index in range(n):
            res += (index - left[index]) * (right[index] - index)
        
        return res
''',
    call='Solution().countGoodSubarrays([1, 3, 1, 1])',
    expect=10,
    skip=['n = len(nums)', 'stack = []', 'left = [-1] * n', 'right = [n] * n', 'res = 0'],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, cell=100, h=190,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='stack', var='stack', label='stack（下标，卡壳位置）', h=120, font=26),
        dict(type='array', var='left', label='left[i]：左侧卡住 i 的位置', cell=70, h=110, index=False),
        dict(type='array', var='right', label='right[i]：右侧卡住 i 的位置', cell=70, h=110, index=False),
        dict(type='text', fn=_info, size=22, h=50),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'while stack and nums[stack[-1]] < nums[index]': lambda S, B, r: (
            f'`{S.nums[S.stack[-1]]} < {S.nums[S.index]}` 且 `{S.nums[S.stack[-1]]} | {S.nums[S.index]} = {S.nums[S.stack[-1]] | S.nums[S.index]}` 没变：栈顶被 cover 住，不是卡壳 → 弹出'
            if S.stack and S.nums[S.stack[-1]] < S.nums[S.index] and (S.nums[S.stack[-1]] | S.nums[S.index]) == S.nums[S.index]
            else ('栈空：没有元素能卡住它' if not S.stack else
                  f'栈顶 `{S.nums[S.stack[-1]]}` 没被 `{S.nums[S.index]}` cover（或等值要保留）→ 它卡住了当前数，停')),
        'left[index] = stack[-1]': '`left[{index}] = {stack[-1]}`：被下标 `{stack[-1]}` 卡住，左边界从它右边开始',
        'left[index] = -1': '栈空：`left[{index}] = -1`，能 cover 整个左侧',
        'stack.append(index)': '`{index}` 入栈：后面能 cover 它的数，也能 cover 它 cover 的那些',
        'while stack and (nums[stack[-1]] | nums[index]) == nums[index]': lambda S, B, r: (
            f'`{S.nums[S.stack[-1]]} | {S.nums[S.index]} = {S.nums[S.stack[-1]] | S.nums[S.index]}` == `{S.nums[S.index]}`：栈顶被 cover → 弹出（右侧不要求严格小，等值也弹）'
            if S.stack and (S.nums[S.stack[-1]] | S.nums[S.index]) == S.nums[S.index]
            else ('栈空：没有元素能卡住它' if not S.stack else
                  f'`{S.nums[S.stack[-1]]} | {S.nums[S.index]}` 变大了：栈顶卡住当前数 → 停')),
        'right[index] = stack[-1]': '`right[{index}] = {stack[-1]}`：右边界到它左边为止',
        'right[index] = n': '栈空：`right[{index}] = n = {n}`，能 cover 整个右侧',
        'res += ': '`nums[{index}]`：`({index} − {left[index]}) × ({right[index]} − {index})` = =={(index - left[index]) * (right[index] - index)}==，累计 =={res}==',
        'return res': '好子数组共 =={ret}== 个',
    },
    cards=dict(
        one_liner='好子数组里，最大值就是 OR 值：枚举最左的最大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组所有元素按位或，等于子数组里出现过的某个元素，称为好子数组',
                 '示例：`[4,2,3]` → `4`；`[1,3,1]` → `6`',
                 '本视频用 `[1,3,1,1]`，含重复数字'],
        quote='由于按位或是越或越大的，因此如果一个子数组是好子数组，其中元素的按位或必然等于其中的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['OR 越或越大：好子数组的 OR 就是最大值，其他数都被它「cover 住」',
              '以最左的最大值为准：左边遇到等值或 cover 不住的就停，右边只看 cover 不住',
              '栈里存的是卡壳位置；cover 具有传递性，所以弹掉的不用再留'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：左侧弹栈要加 `< nums[index]` 保留等值（保证最左），右侧不加',
                 '`left` 默认 `-1`、`right` 默认 `n`，对应「没有墙」',
                 '原文为 Python 2 风格，代码未做修改即可在 Python 3 运行',
                 '对比灵神：灵神用子集判断 + 哨兵，yiduobo 用 cover 的传递性'],
    ),
)

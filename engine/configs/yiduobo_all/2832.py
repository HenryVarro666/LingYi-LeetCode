CONFIG = dict(
    num=2832, title='每个元素为最大值的最大范围', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='两趟单调栈求左右边界', tags=['灵神题单'],
    code='''
class Solution(object):
    def maximumLengthOfRanges(self, nums):

        n = len(nums)
        left = [-1] * n
        right = [n] * n

        stack = []
        for index in range(n):
            while stack and nums[stack[-1]] < nums[index]:
                right[stack[-1]] = index
                stack.pop()
            
            stack.append(index)

        stack = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[index]:
                left[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        return [right[index] - left[index] - 1 for index in range(n)]
''',
    call='Solution().maximumLengthOfRanges([1,5,4,3,6])',
    expect=[1, 4, 2, 1, 5],
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums（蓝 = 当前遍历到的 index）', h=230,
             color=lambda S, i, v: 'pink' if 'stack' in S and S['stack'] and S['stack'][-1] == i else None),
        dict(type='stack', var='stack', fmt=lambda i: f'{i}', label='stack（存下标，栈底到栈顶对应值递减）', h=150),
        dict(type='array', var='left', label='left[i]：左侧最近的更大值下标（-1 = 没有）', h=150, cell=70),
        dict(type='array', var='right', label='right[i]：右侧最近的更大值下标（n = 没有）', h=150, cell=70),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'pink'), ('left', 'left', 'cyan'), ('right', 'right', 'orange')],
    captions={
        'left = [-1] * n': '`left[i]` 先填 `-1`：表示左边没有更大的数',
        'right = [n] * n': '`right[i]` 先填 `n`：表示右边没有更大的数',
        'while stack and nums[stack[-1]] < nums[index]': lambda S, B, r: (
            '栈是空的，没有谁在等更大的数 → 不弹' if not S.stack else
            f'栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` < 当前 `{S.nums[S.index]}` → ==当前就是它右边第一个更大的数==，弹出定边界'
            if S.nums[S.stack[-1]] < S.nums[S.index] else
            f'栈顶 `{S.nums[S.stack[-1]]}` ≥ 当前 `{S.nums[S.index]}` → 当前不是它的更大数，先不弹'),
        'right[stack[-1]] = index': '栈顶下标的右边界就是当前 `index = {index}`：`right[{stack[-1]}] = {index}`',
        'left[stack[-1]] = index': '栈顶下标的左边界就是当前 `index = {index}`：`left[{stack[-1]}] = {index}`',
        'stack.pop()': '栈顶的边界已确定，弹出，不再需要它',
        'stack.append(index)': '`index = {index}` 入栈，等着后面更大的数来给它定边界',
        8: '空栈：先正向扫，求每个数的右边界 `right`',
        16: '清空栈，改成从右往左扫，求每个数的左边界 `left`',
        'return [': lambda S, B, r: f'`res[i] = right[i] - left[i] - 1`：两个更大值之间夹着的长度 → `{r}`',
    },
    cards=dict(
        one_liner='找左右两侧第一个更大的数，夹在中间的就是范围',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`（元素互不相同），求每个 `nums[i]` 作为最大值的最长子数组长度',
                 '例：`[1,5,4,3,6]` → `[1,4,2,1,5]`',
                 '本视频：`[1,5,4,3,6]`'],
        quote='对于每个nums[i]，找出其左侧最大的满足nums[left[i]]大于nums[i]的下标left[i]，以及其右侧最小的满足nums[right[i]]大于nums[i]的下标right[i]，那么其对应的res[i]就是right[i] - left[i] - 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[i]` 要当最大值，范围不能碰到更大的数',
              '所以左右各找最近的更大数，边界之间就是它的范围',
              '求“下一个更大”是经典单调栈：正扫得 `right`，反扫得 `left`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`left` 默认 `-1`、`right` 默认 `n`：没有更大数时范围延伸到数组边缘',
                 '长度 = `right - left - 1`，别忘了减 1（两端的更大数不算在内）',
                 '原文本身已是 Python 3 可运行写法，未作修改'],
    ),
)

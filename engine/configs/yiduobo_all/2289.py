CONFIG = dict(
    num=2289, title='使数组按非递减顺序排列', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈找左侧更大数 · use_step 数组',
    tags=['灵神题单', '难度分 2482'],
    code='''
class Solution(object):
    def totalSteps(self, nums):
        n = len(nums)
        use_step = []
        stack = []
        res = 0
        for index, num in enumerate(nums):
            now = 0
            while stack and nums[stack[-1]] <= num:
                now = max(now, use_step[stack[-1]])
                stack.pop()
            if stack:
                now += 1
            else:
                now = 0
            
            use_step.append(now)
            stack.append(index)
        return max(use_step)
''',
    call='Solution().totalSteps([9,2,3,4,1,5])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', h=190, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='array', var='use_step', label='use_step（每个数被删除的轮次）', h=170,
             color=lambda S, i, v: 'green' if i == len(S['use_step']) - 1 else None),
        dict(type='stack', var='stack', label='stack（下标，对应的数递减）', h=130, font=28),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num', 'blue'), ('now', 'now', 'orange'), ('stack', 'stack', 'yellow')],
    captions={
        'use_step = []': '`use_step[i]`：第 `i` 个数被删除的==轮次==（没被删记 0）',
        'stack = []': '栈用来找每个数左边最近的更大数 `nums[p]`',
        'for index, num': '看 `nums[{index}] = {num}`',
        8: '`now` 准备记录 `p+1` 到 `index-1` 之间最晚被删的轮次',
        'while stack and nums[stack[-1]] <= num': lambda S, B, ret: (
            f'栈顶数 `{S.nums[S.stack[-1]]}` ≤ `{S.num}`：它不是左边更大的数 p → 弹出并看它的轮次'
            if S.stack and S.nums[S.stack[-1]] <= S.num else
            ('栈空：左边没有比它大的数' if not S.stack else f'栈顶 `{S.nums[S.stack[-1]]}` > `{S.num}`：找到了 p，就是它')),
        'now = max(now, use_step[stack[-1]])': '`now` → =={now}==：中间的数最晚在第 `{now}` 轮删完',
        'stack.pop()': '弹出这个下标',
        'if stack:': lambda S, B, ret: ('有 p：要等中间的数删完，再被 p 删除' if S.stack else '没有 p：这个数永远不会被删'),
        'now += 1': '`now` = 最晚轮次 + 1 = =={now}==',
        15: '没有 p：这个数不会被删，`now = 0`',
        'use_step.append(now)': '`use_step[{index}] = {now}`',
        'stack.append(index)': '下标 `{index}` 入栈',
        'return max(use_step)': '答案是所有数被删轮次的最大值 =={ret}==',
    },
    cards=dict(
        one_liner='换个角度：问每个数在第几轮被删，答案取最大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每轮同时删除所有比左邻居小的数，直到数组非递减',
                 '求需要多少轮',
                 '示例：`[5,3,4,4,7,3,6,11,8,5,11]` → `3`',
                 '本视频用 `[9,2,3,4,1,5]` → `4`'],
        quote='知道了这个问题的结果也就知道了最终的答案，因为最终答案就是所有数被删除轮次中的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['无法直接模拟：同时有别的数在删别的数，轮次互相影响',
              '设 `p` 是左侧最近的更大数：`use_step[index] = max(use_step[p+1..index-1]) + 1`',
              '没有 `p` 就是 0；找 `p` 用单调栈'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`p` 被更前面的数先删也不影响 `index` 的轮次',
                 '弹栈条件含等号 `<=`：相等的数不会删除对方',
                 '对比灵神：灵神把轮次直接存进栈里，这里单独用 `use_step` 数组'],
    ),
)

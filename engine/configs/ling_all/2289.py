CONFIG = dict(
    num=2289, title='使数组按非递减顺序排列', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调递减栈 · 记录删除时刻',
    tags=['灵神题单', '难度分 2482'],
    code='''
class Solution:
    def totalSteps(self, nums: List[int]) -> int:
        ans, st = 0, []
        for num in nums:
            max_t = 0
            while st and st[-1][0] <= num:
                max_t = max(max_t, st.pop()[1])
            max_t = max_t + 1 if st else 0
            ans = max(ans, max_t)
            st.append((num, max_t))
        return ans
''',
    call='Solution().totalSteps([9,2,3,4,1,5])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（互不相同，便于定位）', h=200, pointers={'nums.index(num)': 'blue'},
             pointer_labels={'nums.index(num)': 'num'},
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None),
        dict(type='stack', var='st', label='st（元素:被删除的时刻，栈顶在右）', h=150, font=28,
             fmt=lambda x: f'{x[0]}:{x[1]}'),
        dict(type='text', fn=lambda S: (f"当前 `num = {S['num']}`，弹出的最大时刻 `max_t = {S['max_t']}`，答案 `ans = {S['ans']}`" if 'num' in S and 'max_t' in S else ''), size=26, h=90),
    ],
    watch=[('num', 'num', 'blue'), ('max_t', 'max_t', 'orange'), ('st', 'st', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans, st = 0, []': '`ans` 是所有元素被删除时刻的最大值；`st` 是递减栈，存 (元素, 被删时刻)',
        'for num in nums': '处理 `{num}`',
        'max_t = 0': '`max_t` 记录要弹掉的元素里最晚的删除时刻',
        'while st and st[-1][0] <= num': lambda S, B, ret: (
            f'栈顶 `{S.st[-1][0]}` ≤ `{S.num}`：它挡不住 `{S.num}`，要弹出，并看它的删除时刻 `{S.st[-1][1]}`'
            if S.st and S.st[-1][0] <= S.num else
            ('栈空：左边没有比 `{}` 大的数'.format(S.num) if not S.st else f'栈顶 `{S.st[-1][0]}` > `{S.num}`：它就是删除 `{S.num}` 的那个数 → 停')),
        'max_t = max(max_t, st.pop()[1])': '弹出元素的删除时刻 → `max_t = {max_t}`：中间的数都删完，才轮到 `{num}`',
        'max_t = max_t + 1 if st': lambda S, B, ret: (
            f'栈不空：被左边更大的数删除，时刻 = 中间最晚的 `{B.max_t}` + 1 = =={S.max_t}=='
            if S.st else f'栈空：左边没有更大的数，`{S.num}` 不会被删，时刻记 ==0=='),
        'ans = max(ans, max_t)': '`ans = max({B.ans}, {max_t}) = {ans}`',
        'st.append((num, max_t))': '`({num}, {max_t})` 入栈',
        'return ans': '最后一个被删的元素在第 =={ret}== 轮被删 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='算出每个元素被删除的时刻，答案就是其中最大的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每一步删掉所有比左邻居小的元素，重复直到非递减',
                 '返回需要的操作次数',
                 '示例：`[5,3,4,4,7,3,6,11,8,5,11]` → `3`',
                 '本视频用 `[9,2,3,4,1,5]`'],
        quote='元素 x 会被左边某个比他大的元素 y 给删除（如果存在的话）。我们需要计算在删除 x 之前，删除了多少个比 y 小的元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 等价于被==左边最近且更大==的数删除，删除时刻 = 中间所有元素最晚删除时刻 + 1',
              '递减栈里存「元素 + 删除时刻」，弹出时取最大的时刻',
              '栈空说明没人能删它，时刻为 0'],
        summary=['时间 `O(n)`：每个元素至多入栈出栈各一次',
                 '易错：弹栈条件是 `<=`，相等的数不会互相删除，也要弹',
                 '易错：栈空时 `max_t` 必须是 0，不是弹出值 + 1',
                 '原文还提到单调栈 + 线段树的做法，这里用更简洁的栈'],
    ),
)

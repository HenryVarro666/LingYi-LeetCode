NUMS = [3, 1, 2, 1, 2, 2, 3]


def _show(S):
    if 'nxt' not in S:
        return '先一趟遍历：单调栈求 `f`（右边第一个更小的下标），哈希表求 `nxt`（下一个相同值的下标）'
    if S.get('index') is None:
        return f'`f = {S["f"]}`\n`nxt = {S["nxt"]}`'
    return f'`f = {S["f"]}`    `nxt = {S["nxt"]}`'


CONFIG = dict(
    num=3542, title='将所有元素变为 0 的最少操作次数', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='f / nxt 数组 + 单调栈',
    tags=['灵神题单·单调栈', '难度分 1890'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        n = len(nums)

        f = [None] * n
        stack = []
        last = {}
        nxt = [None] * n
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index]:
                f[stack.pop()] = index
            
            stack.append(index)
        
            if nums[index] in last:
                nxt[last[nums[index]]] = index
            last[nums[index]] = index
        
        res = 0
        for index in range(n):
            if nums[index] > 0 and nxt[index] is None or (f[index] is not None and f[index] < nxt[index]):
                res += 1
        
        return res
''',
    call=f'Solution().minOperations({NUMS!r})',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前 index）', h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='array', var='f', label='f[i]：右边第一个更小数的下标（· = 没有）', h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='array', var='nxt', label='nxt[i]：下一个相同值的下标（· = 没有）', h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='stack', var='stack', label='stack（下标，对应值递增）', fmt=lambda i: f'{i}:{NUMS[i]}', h=130),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'purple'), ('res', 'res', 'green')],
    captions={
        'f = [None]': '`f[i]`：右边第一个比 `nums[i]` ==更小==的位置，先都设为 None',
        'nxt = [None]': '`nxt[i]`：下一个和 `nums[i]` 相等的位置',
        'while stack and nums[stack[-1]] > nums[index]': lambda S, B, r: ('栈空，停止弹栈' if not S.stack else f'栈顶值 `{S.nums[S.stack[-1]]}` 比 `nums[{S.index}] = {S.nums[S.index]}` 大？' + ('是，它的右边更小 → 记下 f' if S.nums[S.stack[-1]] > S.nums[S.index] else '否，停止弹栈')),
        'f[stack.pop()] = index': '栈顶找到了右边更小的数：`f[{B.stack[-1]}] = {index}`',
        'stack.append(index)': '下标 `{index}` 入栈，栈里的值保持递增',
        'if nums[index] in last': '`{nums[index]}` 之前出现过吗？{"出现过" if nums[index] in B.last else "没有"}',
        'nxt[last[nums[index]]] = index': '上一个 `{nums[index]}` 的 `nxt` 指向当前下标：`nxt[{last[nums[index]]}] = {index}`',
        'last[nums[index]] = index': '`last[{nums[index]}] = {index}`：记住最近出现的位置',
        'if nums[index] > 0 and nxt': lambda S, B, r: (
            f'`nums[{S.index}] = {S.nums[S.index]}`：' + (
                '后面没有相同值，必须自己操作一次' if S.nxt[S.index] is None
                else f'`f = {S.f[S.index]}` < `nxt = {S.nxt[S.index]}`：中间有更小的数隔开 → 必须操作一次' if (S.f[S.index] is not None and S.f[S.index] < S.nxt[S.index])
                else f'`nxt = {S.nxt[S.index]}` 之前没有更小数隔开 → 能和下一个同值一起消，这里不加')),
        'res += 1': '`res` = {res}',
        'return res': '一共需要 `{res}` 次操作',
    },
    cards=dict(
        one_liner='相同的数之间没有更小的数隔开，才能一起消',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次选子数组，把其中最小的非负数全变成 0，求把数组变成全 0 的最少操作次数',
                 '示例：`[3,1,2,1]` → `3`',
                 '本视频：`[3,1,2,1,2,2,3]` → `5`'],
        quote='为了同时消除两个相同的元素x，一个前提条件就是这两个x之间不能存在小于x的元素y。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数 `x` 看「下一个更小的位置 `f`」和「下一个相同值的位置 `nxt`」',
              '`f < nxt`：两个 `x` 之间有更小的数 → 这个 `x` 必须单独花一次操作',
              '没有 `nxt`（最后一个 `x`）也要花一次；0 本身不用操作'],
        summary=['时间 `O(n)`，单调栈求 `f`，哈希表求 `nxt`',
                 '`nums[index] > 0` 把 0 排除；`nxt` 为 None 时靠短路避免比较 None',
                 '同一值连续的一串，只有最后一个（或被隔断的那个）计一次',
                 '对比灵神：灵神一个栈边扫边计数；yiduobo 先分别预处理 `f` 和 `nxt`，再统一数'],
    ),
)

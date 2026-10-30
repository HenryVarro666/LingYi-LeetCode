CONFIG = dict(
    num=1950, title='所有子数组最小值中的最大值', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 + 差分式逆序取 max', tags=['灵神题单'],
    code='''
class Solution(object):
    def findMaximums(self, nums):

        n = len(nums)
        right = [n] * n
        stack = []
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index]:
                right[stack[-1]] = index
                stack.pop()
            stack.append(index)
        

        left = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[index]:
                left[stack[-1]] = index
                stack.pop()
            stack.append(index)

        res = [-1] * n
        for index in range(n):
            length = right[index] - 1 - (left[index] + 1) + 1
            res[length - 1] = max(res[length - 1], nums[index])
            
        for index in range(n - 2, -1, -1):
            res[index] = max(res[index], res[index + 1])
            
        return res
''',
    call='Solution().findMaximums([2,6,1,5,3])',
    expect=[6, 3, 1, 1, 1],
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums（蓝 = 当前 index）', h=230,
             color=lambda S, i, v: 'pink' if S.get('_line', 0) <= 23 and S.get('stack') and S['stack'][-1] == i else None),
        dict(type='stack', var='stack', fmt=lambda i: f'{i}', label='stack（存下标，值从栈底到栈顶递增）', h=120),
        dict(type='array', var='left', label='left[i]：左侧第一个更小值下标', h=100, cell=64, index=False),
        dict(type='array', var='right', label='right[i]：右侧第一个更小值下标', h=100, cell=64, index=False),
        dict(type='array', var='res', label='res[k]：长度为 k+1 的子数组，最小值的最大值（-1 = 暂无）', h=180, cell=70,
             pointers={'index': 'blue'}, color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    max_steps=72,
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'pink'), ('length', 'length', 'orange')],
    captions={
        'right = [n] * n': '先正向扫，求每个数右侧第一个更小值 `right`（没有则为 `n`）',
        'while stack and nums[stack[-1]] > nums[index]': lambda S, B, r: (
            '栈是空的 → 不弹' if not S.stack else
            f'栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` > 当前 `{S.nums[S.index]}` → ==当前是它{"右" if S["_line"] == 8 else "左"}边第一个更小的数=='
            if S.nums[S.stack[-1]] > S.nums[S.index] else
            f'栈顶 `{S.nums[S.stack[-1]]}` ≤ 当前 `{S.nums[S.index]}` → 栈顶还没遇到更小的数，不弹'),
        'right[stack[-1]] = index': '`right[{stack[-1]}] = {index}`：栈顶下标的右边界确定',
        'left[stack[-1]] = index': '`left[{stack[-1]}] = {index}`：栈顶下标的左边界确定',
        'stack.pop()': '边界已确定，弹出',
        'stack.append(index)': '`index = {index}` 入栈，等后面更小的数来给它定边界',
        'left = [-1] * n': '再从右往左扫一遍，求左侧第一个更小值 `left`（没有则为 `-1`）',
        'res = [-1] * n': '`res[k]`：长度为 `k+1` 的答案，先全填 `-1`',
        'length = right': '`nums[{index}] = {nums[index]}` 是区间 `({left[index]}, {right[index]})` 内的最小值 → 它能当长度 1 到 `{length}` 的子数组的最小值，长度 = `{right[index]} − ({left[index]}) − 1` = =={length}=='
                          ,
        'res[length - 1] = max': '先只记在最长处：`res[{length - 1}] = max({B.res[length - 1]}, {nums[index]}) = {res[length - 1]}`（更短的长度留给下一趟补）',
        'res[index] = max': '长度 `{index + 1}` 的答案也要吃下长度 `{index + 2}` 的候选（从长的子数组去掉一个端点，最小值不会变小）：`res[{index}] = {res[index]}`',
        'return res': '`res[k]` 就是长度 `k+1` 的所有子数组最小值的最大值：`{res}`',
    },
    cards=dict(
        one_liner='换个角度：每个数能当多长子数组的最小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['对每个长度 `k`（1 到 `n`），求所有长度为 `k` 的子数组的最小值里的最大值',
                 '返回长度为 `n` 的数组，第 `k-1` 位是长度 `k` 的答案',
                 '例：`[2,6,1,5,3]` → `[6,3,1,1,1]`'],
        quote='不妨从单个数字的角度来考虑。对于数组中的某个数nums[index]，只有当这个数是子数组中的最小值时才会对答案产生影响。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[i]` 能当最小值的最长子数组，长度 `right - left - 1`',
              '更短的长度也都能取到它，所以影响 `res[0..长度-1]`，区间左端都是 0',
              '先只在最长处记 `max`，再从后往前传 `res[i] = max(res[i], res[i+1])`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`left` 默认 `-1`、`right` 默认 `n`，长度公式不用特判',
                 '逆序传播能成立：长度 `k+1` 的候选也是长度 `k` 的候选',
                 '“更小”用严格大于弹栈，相等的数可以共存，不影响最终答案',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)

CONFIG = dict(
    num=3113, title='边界元素是最大值的子数组数目', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='下一个更大元素 + 哈希表分组计数',
    tags=['灵神题单·单调栈', '难度分 2046'],
    code='''
class Solution(object):
    def numberOfSubarrays(self, nums):

        stack = []
        n = len(nums)
        f = [-1] * n
        for index, v in enumerate(nums):
            while stack and nums[stack[-1]] < v:
                f[stack[-1]] = index
                stack.pop()
            stack.append(index)
        
        counter = Counter()
        for index in range(n):
            key = (nums[index], f[index])
            counter[key] += 1
        
        res = 0
        for cnt in counter.values():
            res += (cnt + 1) * cnt // 2
        
        return res
''',
    call='Solution().numberOfSubarrays([3,1,3,2,3])',
    expect=8,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=150, label='nums',
             color=lambda S, i, v: 'blue' if i == S.get('index', -1) else None),
        dict(type='array', var='f', h=150, label='f：下一个更大元素的下标（-1 = 没有）',
             color=lambda S, i, v: 'green' if v != -1 else None),
        dict(type='stack', var='stack', h=130, fmt=lambda i: f'{i}'),
        dict(type='map', var='counter', h=130, fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('res', 'res', 'green')],
    captions={
        'stack = []': '栈存下标，对应的值从底到顶 ==不增==：它们都还没找到下一个更大元素',
        'f = [-1] * n': '`f[i]` = i 右边第一个更大元素的下标，先全设成 -1',
        'while stack and nums[stack[-1]] < v': lambda S, B, r: (
            f'栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` < `v = {S.v}`：v 就是它的下一个更大元素' if S.stack and S.nums[S.stack[-1]] < S.v
            else ('栈空了，停止' if not S.stack else f'栈顶 `{S.nums[S.stack[-1]]}` >= `v = {S.v}`：停止弹出')),
        'f[stack[-1]] = index': '`f[{B.stack[-1]}] = {index}`：下标 {B.stack[-1]} 的下一个更大元素在 {index}',
        'stack.pop()': '这个下标已经找到答案，弹出',
        'stack.append(index)': '`index = {index}` 入栈，等着以后的更大元素',
        'counter = Counter()': '按 `(值, 下一个更大元素的下标)` 分组：同组的数两两可以做左右端点',
        'key = (nums[index], f[index])': '`key = ({nums[index]}, {f[index]})`：值相同、下一个更大元素也相同',
        'counter[key] += 1': '这一组现在有 `{counter[key]}` 个下标',
        'for cnt in counter.values()': lambda S, B, r: (
            '每一组都算完了' if S.res == sum((c + 1) * c // 2 for c in S.counter.values()) else '取出下一组：`cnt = {}`'.format(S.cnt)),
        'res += (cnt + 1) * cnt // 2': '这一组 `cnt = {cnt}` 个：任选左右端点（可重合）：`({cnt}+1)×{cnt}//2` = {(cnt + 1) * cnt // 2} → `res` = =={res}==',
        'return res': '一共 `{res}` 个子数组',
    },
    max_steps=90,
    cards=dict(
        one_liner='两端相等，且下一个更大元素是同一个 → 中间都不超过两端',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数一数有多少子数组，左右边界都是子数组里的最大值',
                 '单个元素也算（左右边界是同一个数）',
                 '本视频示例：`[3,1,3,2,3]` → `8`'],
        quote='对于一个子数组，如果其左右边界的元素相等，且这两个元素的下一个更大的元素是同一个，那么就说明子数组内部的所有元素都小于等于左右边界的元素，即这是一个合法的子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用单调栈求每个元素的下一个更大元素下标 `f`',
              '把 `(nums[i], f[i])` 当 key，用哈希表数每组的个数',
              '一组有 `cnt` 个，就有 `cnt*(cnt+1)//2` 个合法子数组'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '栈里的值不增，所以弹出时 `v` 恰好是下一个更大元素',
                 '`(cnt + 1) * cnt // 2` 包含长度为 1 的子数组（左右端点是同一个下标）',
                 '对比灵神：灵神边走边在栈里记次数，yiduobo 先求 `f` 再分组数数'],
    ),
)

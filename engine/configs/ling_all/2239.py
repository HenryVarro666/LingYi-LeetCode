CONFIG = dict(
    num=2239, title='找到最接近 0 的数字', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='一次遍历 · 比绝对值',
    tags=[],
    code='''
class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        ans = nums[0]
        for x in nums:
            if abs(x) < abs(ans) or abs(x) == abs(ans) and x > 0:
                ans = x
        return ans
''',
    call='Solution().findClosestNumber([2,-4,-1,1,8])',
    expect=1,
    views=[
        dict(type='array', var='nums', h=260, label='nums',
             color=lambda S, i, v: 'green' if 'ans' in S and v == S['ans'] else None),
        dict(type='text', h=60, fn=lambda S: f"当前 `x = {S['x']}`，`|x| = {abs(S['x'])}`；答案 `ans = {S['ans']}`，`|ans| = {abs(S['ans'])}`" if 'x' in S and 'ans' in S else ''),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green'), ('|x|', 'abs(x) if "x" in S else ""', 'blue'), ('|ans|', 'abs(ans)', 'green')],
    captions={
        'ans = nums[0]': '先假设第一个数就是答案：`ans = {ans}`',
        'if abs(x)': '`|x| = {abs(x)}`，`|ans| = {abs(ans)}`：{"更小 → 更新" if abs(x) < abs(ans) else ("绝对值相同且 x 为正 → 更新（题目要最大值）" if abs(x) == abs(ans) and x > 0 else "没有更近，也不是同距离的正数 → 跳过")}',
        'ans = x': '更新答案 `ans = {ans}`',
        'return ans': '最接近 0 的数是 =={ret}==',
    },
    cards=dict(
        one_liner='「最接近 0」就是「绝对值最小」，平局取正数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定整数数组 `nums`，返回最接近 `0` 的数',
                 '距离相同时返回 ==较大的那个==',
                 '示例：`[-4,-2,1,4,8]` → `1`；`[2,-1,1]` → `1`'],
        quote='「最接近 0」等价于「绝对值最小」。如果 |nums[i]| 和答案的绝对值相同，且 nums[i] > 0，则更新答案为 nums[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历数组，维护当前绝对值最小的数 `ans`',
              '`|x|` 更小就更新；`|x|` 相同时只有 `x > 0` 才更新（取较大值）',
              '初值取 `nums[0]`，不需要额外的无穷大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：平局时要取正数，`and` 优先级高于 `or`，无需加括号',
                 '另一种写法：`-min((abs(x), -x) for x in nums)[1]`，把「绝对值小、值大」编码成元组比较'],
    ),
)

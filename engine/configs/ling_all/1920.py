CONFIG = dict(
    num=1920, title='基于排列构建数组', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='原地数字搬家（取反标记）',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def buildArray(self, nums: List[int]) -> List[int]:
        for i, x in enumerate(nums):
            if x < 0:  # 已搬家
                continue
            cur = i
            while nums[cur] != i:
                nxt = nums[cur]
                nums[cur] = ~nums[nxt]  # 把下一个数搬过来，同时做标记（取反）
                cur = nxt
            nums[cur] = ~x  # 对于这一组的最后一个数，把起点 x=nums[i] 搬过来

        for i, x in enumerate(nums):
            nums[i] = ~x  # 复原
        return nums
''',
    call='Solution().buildArray([1,2,0,4,3])',
    expect=[2, 0, 1, 3, 4],
    views=[
        dict(type='text', fn=lambda S: ('负数 = 已搬家（存的是 ~值）；第二轮再取反复原' if 'nums' in S else '')),
        dict(type='array', var='nums', pointers={'i': 'blue', 'cur': 'pink'}, h=300,
             color=lambda S, i, v: 'purple' if v < 0 else None),
    ],
    watch=[('i', 'i', 'blue'), ('cur', 'cur', 'pink'), ('x', 'x', 'orange')],
    captions={
        'for i, x in enumerate(nums):': lambda S, B, r: (f'第一轮（搬家）：看下标 `i = {S.i}`，`x = {S.x}`' if S._line == 3 else f'第二轮（复原）：看下标 `i = {S.i}`，`x = {S.x}`'),
        'if x < 0': lambda S, B, r: (f'`x = {S.x} < 0`：这个位置已经搬过家 → 跳过' if S.x < 0 else f'`x = {S.x} >= 0`：这一组还没搬 → 从 `i = {S.i}` 开始搬'),
        'cur = i': '环的起点：`cur = {cur}`',
        'while nums[cur] != i': lambda S, B, r: (f'`nums[{S.cur}] = {S.nums[S.cur]}` ≠ `{S.i}`：环还没走完，继续搬' if S.nums[S.cur] != S.i else f'`nums[{S.cur}] = {S.i}` 指回起点 → 这一组到头了'),
        'nxt = nums[cur]': '下一个位置 `nxt = nums[{B.cur}] = {nxt}`',
        'nums[cur] = ~nums[nxt]': '把 `nums[{nxt}]` 搬到 `nums[{B.cur}]`，同时取反做标记：`nums[{B.cur}] = {nums[B.cur]}`',
        'cur = nxt': '`cur` 跳到 `{cur}`',
        'nums[cur] = ~x': '最后一个位置拿起点原来的值 `x = {x}`（取反）：`nums[{cur}] = {nums[cur]}`',
        'nums[i] = ~x': '`~x` 还原：`nums[{i}] = {nums[i]}`',
        'return nums': '全部复原，返回 `{nums}`',
    },
    cards=dict(
        one_liner='把「i → nums[i]」连成环，沿环把数字一个个搬家',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是 `0..n-1` 的排列，构造 `ans[i] = nums[nums[i]]`',
                 '进阶：不用额外空间',
                 '本视频：`[1,2,0,4,3]` → `[2,0,1,3,4]`'],
        quote='所以从 i 开始，不断迭代 i=nums[i]，一定会回到起点 i。我把这个过程叫做「数字搬家」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排列的值域和下标域相同，所以 `i → nums[i]` 构成若干个环',
              '沿环把 `nums[nums[cur]]` 搬到 `nums[cur]`，最后一个位置拿起点的旧值',
              '用 `~x`（等于 -(x+1)）把搬过的位置变成负数，遇到负数就跳过；最后全部再取反复原'],
        summary=['时间 `O(n)`，空间 `O(1)`：虽然是二重循环，但每个数只被标记一次',
                 '`~x = -x - 1`，保证非负数变成负数，且能无损还原',
                 '起点的旧值 `x` 要先存下来，环尾才能用它',
                 '同类题：442、448、41、287；题解另有一行写法二'],
    ),
)

CONFIG = dict(
    num=3038, title='相同分数的最大操作数目 I', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='枚举相邻二元组',
    tags=[],
    code='''
class Solution:
    def maxOperations(self, nums: List[int]) -> int:
        s = nums[0] + nums[1]
        for i in range(3, len(nums), 2):
            if nums[i - 1] + nums[i] != s:
                return i // 2
        return len(nums) // 2
''',
    call='Solution().maxOperations([3,2,1,4,5,1])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"第一次操作的分数 `s = {S['s']}`，后面每一对都要等于它" if 's' in S else '每次删掉前两个，等价于把数组按 2 个一组切开'), size=28),
        dict(type='array', var='nums', label='nums（每两个一组：蓝 = 当前这一对）', cell=96,
             pointers={'i - 1': 'blue', 'i': 'pink'},
             color=lambda S, k, v: ('blue' if ('i' in S and k in (S['i'] - 1, S['i'])) else 'green' if (k < 2 and 's' in S) else None)),
    ],
    watch=[('s', 's', 'green'), ('i', 'i', 'pink')],
    captions={
        's = nums': '第一次操作删掉 `nums[0]` 和 `nums[1]`，分数 `s = {s}`，==后面的每次操作都要等于它==',
        'for i in range': '`i` 是每一对的右端点，从 3 开始，每次 +2：`i = {i}`，这一对是 `nums[{i-1}]` 和 `nums[{i}]`',
        'if nums[i - 1]': lambda S, B, ret: (f"`{S.nums[S.i-1]} + {S.nums[S.i]} = {S.nums[S.i-1]+S.nums[S.i]}` ≠ `s = {S.s}` → ==分数变了，不能继续=="
                                              if S.nums[S.i-1] + S.nums[S.i] != S.s else
                                              f"`{S.nums[S.i-1]} + {S.nums[S.i]} = {S.s}` == `s` → 这次操作合法，继续下一对"),
        'return i // 2': '已经做完了前面 `i // 2 = {i//2}` 对（第一对 + 之后合法的），返回 =={ret}==',
        'return len(nums)': '一路都相等，答案就是 `len(nums) // 2`，返回 =={ret}==',
    },
    cards=dict(
        one_liner='第一对的和定下分数，后面逐对检查是否相等',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次删除数组前两个元素，得分是两数之和；要求==所有操作分数相同==',
                 '求最多能做几次操作',
                 '示例：`[3,2,1,4,5]` → `2`（两次都是 5）'],
        quote='设 s = nums[0] + nums[1]。答案初始化为 1。从 i=3 开始，如果 nums[i-1] + nums[i] = s 就继续，把 i 增加 2，答案增加 1；否则退出循环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只能删前两个，所以操作顺序固定：第 1 对、第 2 对、第 3 对……',
              '第一对必做，它的和就是 `s`；之后第一对不合法的位置就是终点',
              '遇到 `i` 不合法时，前面已做 `i // 2` 次，直接返回'],
        result='第 3 对 `5 + 1 = 6 ≠ 5`，停下，一共做了 2 次 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`，不需要真的删除元素',
                 '易错：循环从 `i = 3` 开始、步长 2，比较的是 `nums[i-1]` 和 `nums[i]`',
                 '落单的最后一个元素不够一对，循环到不了它，所以返回 `len(nums) // 2`',
                 '思考题：1679. K 和数对的最大数目'],
    ),
)

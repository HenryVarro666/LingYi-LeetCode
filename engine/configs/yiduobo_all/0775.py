CONFIG = dict(
    num=775, title='全局倒置与局部倒置', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='维护前缀最大值',
    code='''
class Solution(object):
    def isIdealPermutation(self, A):

        max_num = 0
        for index in range(2, len(A)):
            max_num = max(max_num, A[index - 2])
            if max_num > A[index]:
                return False

        return True
''',
    call='Solution().isIdealPermutation([1,0,2,4,3])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"`max(A[0..{S['index']-2}]) = {S['max_num']}`  对比  `A[{S['index']}] = {S['A'][S['index']]}`") if 'index' in S and 'max_num' in S else ''),
        dict(type='array', var='A', pointers={'index': 'blue'}, h=300,
             color=lambda S, i, v: ('pink' if i == S['index'] - 2 else 'cyan' if i < S['index'] - 2 else None) if 'index' in S else None),
    ],
    watch=[('index', 'index', 'blue'), ('max_num', 'max_num', 'pink')],
    captions={
        'max_num = 0': '`max_num` 维护 `A[0..index-2]` 的最大值（排列里最小是 0，初值 0 安全）',
        'for index': '看 `A[{index}] = {A[index]}`，只需和它前面隔了至少一个位置的数比',
        'max_num = max': '把 `A[{index-2}] = {A[index-2]}` 纳入前缀：`max_num` = {max_num}',
        'if max_num > A[index]': lambda S, B, r: (f'`{S.max_num} > {S.A[S.index]}`：存在不相邻的逆序对 → 全局倒置更多' if S.max_num > S.A[S.index]
                                                   else f'`{S.max_num} < {S.A[S.index]}`：没有非局部倒置，继续'),
        'return False': '找到非局部的逆序对 → `False`',
        'return True': '所有逆序对都相邻 → 全局倒置 == 局部倒置 → `True`',
    },
    cards=dict(
        one_liner='局部倒置必是全局倒置，只需查有没有隔位的逆序对',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是 `[0, n-1]` 的排列',
                 '全局倒置：`i<j` 且 `nums[i]>nums[j]`；局部倒置：`nums[i]>nums[i+1]`',
                 '判断两者数量是否相等。本视频：`[1,0,2,4,3]` → `True`'],
        quote='所有满足局部倒置的数对必然也是全局倒置，那么要判断全局倒置是否等于局部倒置，那么实际上就是要求是否存在不连续的逆序对。',
        quote_src='—— yiduobo 题解原文',
        idea=['全局倒置 ⊇ 局部倒置，相等 ⇔ 没有不相邻的逆序对',
              '扫描 `index`，`max_num` 维护 `A[0..index-2]` 的最大值',
              '它若大于 `A[index]`，就是一个不相邻的逆序对'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '前缀只到 `index-2`，不含 `index-1`，因为相邻的逆序对是允许的',
                 '原文为 Python 2 风格，参数名为 `A`，代码无需改动'],
    ),
)

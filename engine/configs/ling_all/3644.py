def _bits(v):
    return 'ALL1' if v < 0 else format(v, '04b')


def _txt(S):
    if 'ans' not in S:
        return ''
    nums = S['nums']
    if 'x' not in S:
        return '先看 `nums[0]`：非 0 则答案必为 0'
    i, x = S['i'], S['x']
    if i == x:
        return f'`nums[{i}] = {x}` 已在原位 → 不参与 AND'
    return f'`nums[{i}] = {x}`（`{_bits(x)}`）不在原位 → ans &= 它，ans = `{_bits(S["ans"])}`'


CONFIG = dict(
    num=3644, title='排序排列', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='所有错位元素的 AND',
    tags=['位运算', '思维题', '难度分 1775'],
    code='''
class Solution:
    def sortPermutation(self, nums: List[int]) -> int:
        if nums[0]:  # 小优化：此时 0 参与 AND，结果一定是 0
            return 0
        ans = -1  # 二进制全为 1
        for i, x in enumerate(nums):
            if i != x:
                ans &= x
        return max(ans, 0)
''',
    call='Solution().sortPermutation([0,1,2,7,4,5,6,3])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=30, h=60),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=170,
             color=lambda S, i, v: ('red' if i != v else 'green') if 'ans' in S else None),
        dict(type='text', fn=lambda S: ('下标 = 值 → 绿；不在原位 → 红，k 必须是所有红色数的子集' if 'ans' in S else ''), size=26, h=60),
    ],
    watch=['i', 'x', ('ans', 'ans', 'green')],
    captions={
        'if nums[0]': '`nums[0] = {nums[0]}`：若不是 0，0 一定要被换走，0 参与 AND，结果只能是 0',
        'ans = -1': '`ans = -1`：补码全 1，当作 AND 的初始值，AND 谁都不变',
        'if i != x': lambda S, B, r: (f'`{S.i} != {S.x}`：不在原位，必须被交换，==它要参与 AND==' if S.i != S.x
                                      else f'`{S.i} == {S.x}`：已在原位，不用动，跳过'),
        'ans &= x': '`ans &= {x}` → `{ans}`：k 必须是每个错位数的子集，所以取交集',
        'return max': '答案就是错位元素的 AND = ==`{max(ans, 0)}`==（全有序时 ans 仍是 -1，取 0）',
    },
    cards=dict(
        one_liner='k 最大 = 所有「不在原位」的数按位与',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['排列 `nums`，可交换 `nums[i] & nums[j] == k` 的两个数',
                 '求能把数组排成升序的最大 `k`，已有序返回 0',
                 '示例：`[0,3,2,1]` → `1`；本视频：`[0,1,2,7,4,5,6,3]` → `3`'],
        quote='所以答案至多为所有不满足 nums[i] = i 的 nums[i] 的 AND，下文就用 k 表示这个上界。',
        quote_src='—— 灵茶山艾府题解',
        idea=['错位的数一定要交换，它们都得包含 k：==k 是这些数的子集==，最大就是它们的 AND',
              '上界能取到：用 `0`（或 `k`）当中转，三次交换就能换任意一对',
              'AND 只会变小，所以 k ≤ n-1，一定在 nums 里'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '已有序：ans 保持 -1，==要 `max(ans, 0)` 返回 0==',
                 '`nums[0] != 0` 时 0 必须参与，直接返回 0',
                 '思考题：k 的取值个数，就是上界 k 的子集里满足条件的个数'],
    ),
)

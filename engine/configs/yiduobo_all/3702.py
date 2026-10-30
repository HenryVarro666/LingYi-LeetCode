def _eq(S):
    if 'xor' not in S:
        return ''
    return f"累计异或 `xor = {S['xor']}`，全为 0？ `all_zero = {S.get('all_zero')}`"


CONFIG = dict(
    num=3702, title='按位异或非零的最长子序列', difficulty='Medium', category='位运算',
    author='yiduobo', technique='先全选，异或为 0 再去一个', tags=['灵神题单', '难度分 1489'],
    code='''
class Solution(object):
    def longestSubsequence(self, nums):

        xor = 0
        all_zero = True
        for v in nums:
            xor ^= v
            if v > 0:
                all_zero = False

        if xor > 0:
            return len(nums)

        if all_zero:
            return 0

        return len(nums) - 1
''',
    call='Solution().longestSubsequence([2, 3, 1])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=190, label='nums',
             color=lambda S, i, v: 'yellow' if 'v' in S and v == S['v'] else None),
        dict(type='text', size=28, fn=_eq),
    ],
    watch=[('v', 'v', 'blue'), ('xor', 'xor', 'yellow'), ('all_zero', 'all_zero', 'green')],
    captions={
        4: '`xor` 记录整个数组的异或，从 0 开始',
        5: '`all_zero` 先假设全是 0',
        'for v in nums': lambda S, B, r: ('`nums` 取完，循环结束' if B.get('v') == S.v else f'取下一个数 `v = {S.v}`'),
        'xor ^= v': '`xor` 异或上 `{v}` → `{xor}`',
        'if v > 0': lambda S, B, r: (f'`v = {S.v} > 0`：出现非零元素，`all_zero` 将变为 False' if S.v > 0 else f'`v = 0`，仍可能全是 0'),
        'all_zero = False': '发现非零元素，`all_zero = False`',
        'if xor > 0': lambda S, B, r: (f'`xor = {S.xor} > 0`：整个数组异或非零，==全选== 最长' if S.xor > 0 else f'`xor = {S.xor}`，全选不行，继续判断'),
        12: '全选，返回 `{ret}`',
        'if all_zero': lambda S, B, r: ('`all_zero` 为真：任何子序列异或都是 0 → 无解' if S.all_zero else '有非零元素：可以去掉它'),
        15: '全是 0，返回 0',
        17: '异或为 0 但有非零元素：去掉任意一个非零元素，异或就变非零 → `{ret}`',
    },
    cards=dict(
        one_liner='能全选就全选；异或为 0 就去掉一个非零数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，求按位异或结果非零的最长子序列的长度',
                 '不存在这样的子序列则返回 0',
                 '示例：`[1,2,3]` → `2`；本视频：`[2,3,1]`（异或为 0）'],
        quote='最理想的情况自然就是选取整个nums数组，当然前提是按位异或的结果不为0。若按位异或的结果为0，则需要去掉其中某一个非零的元素，这样一来异或结果就会变为非零',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历同时算整体异或 `xor` 和是否全零 `all_zero`',
              '`xor > 0`：直接全选，长度 `len(nums)`',
              '`xor == 0`：全为 0 就返回 0；否则去掉一个非零元素，长度 `len(nums) - 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：全为 0 时子序列异或必为 0，要返回 0 而不是 `n - 1`',
                 '`xor` 为 0 且有非零元素时，去掉哪个非零数都行',
                 '对比灵神：灵神先判全 0，再用 `reduce(xor, nums)`；这里一趟遍历同时记录'],
    ),
)

CONFIG = dict(
    num=2149, title='按符号重排数组', difficulty='Medium', category='模拟',
    author='yiduobo', technique='双指针隔位填充',
    tags=[],
    code='''
class Solution(object):
    def rearrangeArray(self, nums):

        n = len(nums)
        res = [None] * n
        p_pos = 0
        n_pos = 1
        for num in nums:
            if num > 0:
                res[p_pos] = num
                p_pos += 2
            else:
                res[n_pos] = num
                n_pos += 2
        
        return res
''',
    call='Solution().rearrangeArray([3, 1, -2, -5, 2, -4])',
    expect=[3, -2, 1, -5, 2, -4],
    views=[
        dict(type='array', var='nums', label='nums', cell=84, h=170,
             color=lambda S, i, v: 'green' if v > 0 else 'pink'),
        dict(type='array', var='res', label='res（偶数位放正数，奇数位放负数）', cell=84, h=210,
             pointers={'p_pos': 'green', 'n_pos': 'pink'},
             color=lambda S, i, v: ('green' if v > 0 else 'pink') if v is not None else None),
    ],
    watch=[('num', 'num', 'yellow'), ('p_pos', 'p_pos', 'green'), ('n_pos', 'n_pos', 'pink')],
    captions={
        'n = len': '`n = {n}`',
        'res = [None]': '先开一个长为 `n` 的答案数组，位置待填',
        'p_pos = 0': '`p_pos`：下一个==正数==放的下标，正数放在 0, 2, 4…',
        'n_pos = 1': '`n_pos`：下一个==负数==放的下标，负数放在 1, 3, 5…',
        'for num in nums': lambda S, B, ret: (f'看 `{S.num}`' if S.num != B.get('num') else '遍历完了'),
        'if num > 0': lambda S, B, ret: (f'`{S.num} > 0` → 正数，放到 `p_pos = {S.p_pos}`' if S.num > 0 else f'`{S.num} < 0` → 负数，放到 `n_pos = {S.n_pos}`'),
        'res[p_pos] = num': '`res[{p_pos}] = {num}`，保持正数原有顺序',
        'p_pos += 2': '跳过中间留给负数的位置：`p_pos` → {p_pos}',
        'res[n_pos] = num': '`res[{n_pos}] = {num}`，保持负数原有顺序',
        'n_pos += 2': '跳过中间留给正数的位置：`n_pos` → {n_pos}',
        'return res': '正负交替，且以正数开头：`{res}`',
    },
    cards=dict(
        one_liner='正数填偶数位，负数填奇数位，各自按原顺序',
        complexity='时间 `O(n)`，空间 `O(n)`（返回值）',
        problem=['`nums` 中正负数各占一半，重排使得正负交替、以正数开头',
                 '同号元素保持原来的相对顺序',
                 '示例：`[3,1,-2,-5,2,-4]` → `[3,-2,1,-5,2,-4]`'],
        quote='使用两个指针p_pos和n_pos分别指向当前答案中下一个正数放置的下标以及下一个负数放置的下标，然后遍历原数组……',
        quote_src='—— yiduobo 题解原文',
        idea=['结果必须正负交替且正数开头 → 正数的位置固定是 0, 2, 4…，负数是 1, 3, 5…',
              '按顺序遍历 `nums`，正数放 `p_pos` 并加 2，负数放 `n_pos` 并加 2',
              '遍历顺序就是原顺序，同号元素的相对顺序自然保留'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`n_pos` 从 1 开始、`p_pos` 从 0 开始，别写反（要求正数开头）',
                 '题目保证正负数量相等，所以两个指针不会越界',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)

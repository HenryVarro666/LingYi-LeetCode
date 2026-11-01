CONFIG = dict(
    num=2149, title='按符号重排数组', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='双指针 · 正负数分别填偶奇下标（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        ans = [0] * len(nums)
        i, j = 0, 1
        for v in nums:
            if v > 0:
                ans[i] = v
                i += 2
            else:
                ans[j] = v
                j += 2
        return ans
''',
    call='Solution().rearrangeArray([3, 1, -2, -5, 2, -4])',
    expect=[3, -2, 1, -5, 2, -4],
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: 'yellow' if 'v' in S and S['v'] == v else None),
        dict(type='array', var='ans', label='ans（偶数下标放正数，奇数下标放负数）', h=210, pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, i, v: ('blue' if i % 2 == 0 else 'pink') if v != 0 else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'v'],
    captions={
        'ans = [0]': '准备答案数组 `ans`，长度和 `nums` 一样，先全填 `0`',
        'i, j = 0, 1': '`i = 0` 指向下一个放正数的位置（偶数下标），`j = 1` 指向下一个放负数的位置（奇数下标）',
        'for v in nums': '取下一个数 `v = {v}`',
        'if v > 0': lambda S, B, r: f'`v = {S.v}`：' + ('==正数==，放到偶数下标那一列' if S.v > 0 else '==负数==，放到奇数下标那一列'),
        'ans[i] = v': '正数 `{v}` 放进 `ans[{i}]`，保持原来的先后顺序',
        'i += 2': '隔一个位置再放下一个正数：`i` → {i}',
        'ans[j] = v': '负数 `{v}` 放进 `ans[{j}]`，保持原来的先后顺序',
        'j += 2': '隔一个位置再放下一个负数：`j` → {j}',
        'return ans': lambda S, B, r: f'正负交替，且以正数开头：`{S.ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='正数只填偶数下标，负数只填奇数下标',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['`nums` 正负数个数相等；重排成==正负交替==、正数开头',
                 '同号的数保持原来的相对顺序',
                 '示例：`[3,1,-2,-5,2,-4]` → `[3,-2,1,-5,2,-4]`'],
        quote='另外一种做法，利用符号位：',
        quote_src='—— 灵茶山艾府题解（第二种写法，用符号位当下标）',
        idea=['结果必须以正数开头且正负交替 → 正数的位置固定是 `0,2,4…`，负数是 `1,3,5…`',
              '按顺序扫一遍：正数放 `i` 再 `i += 2`，负数放 `j` 再 `j += 2`',
              '同号数的先后顺序天然保留'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（取原文第一种写法）',
                 '原文另一种写法：用符号位当下标，`i[uint(v)>>63]` 选择 `i` 或 `j`，思路相同，省掉 if',
                 '时间 `O(n)`，空间 `O(n)`（答案数组）',
                 '易错点：`i` 从 `0`、`j` 从 `1` 开始，每次加 `2`'],
    ),
)

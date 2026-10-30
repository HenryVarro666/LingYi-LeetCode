def _ev(S):
    n = S['nums']
    e = [v for v in n if v % 2 == 0]
    return f'偶数有 =={len(e)}== 个：`{e}`；`len(nums) − 奇数个数 = {len(n)} − {sum(v % 2 for v in n)} = {len(e)}`'


CONFIG = dict(
    num=2980, title='检查按位或是否存在尾随零', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='奇偶性 · 数偶数个数',
    tags=['灵神题单·位运算', '难度分 1234'],
    code='''
class Solution:
    def hasTrailingZeros(self, nums: List[int]) -> bool:
        return len(nums) - sum(x % 2 for x in nums) >= 2
''',
    call='Solution().hasTrailingZeros([1,2,3,4,5])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 偶数，最低位是 0；灰色 = 奇数，最低位是 1）', cell=96, h=260,
             color=lambda S, i, v: 'green' if v % 2 == 0 else None,
             dim=lambda S, i, v: v % 2 == 1),
        dict(type='text', h=120, size=30, fn=_ev),
    ],
    watch=[('len(nums)', 'len(nums)', 'blue'), ('奇数个数', 'sum(x % 2 for x in nums)', 'pink'),
           ('偶数个数', 'len(nums) - sum(x % 2 for x in nums)', 'green')],
    captions={
        'return len': '奇数个数 `sum(x % 2)` = `{sum(x % 2 for x in nums)}`，偶数个数 = `{len(nums)}` − `{sum(x % 2 for x in nums)}` = =={len(nums) - sum(x % 2 for x in nums)}==；是否 `>= 2`？==是==，返回 `{ret}`',
    },
    cards=dict(
        after=[dict(heading='为什么奇数不能选', lines=['`2 | 4 = 010 | 100 = 110`：最低位 `0`，有尾随零',
                                                    '`1 | 2 = 001 | 010 = 011`：最低位 `1`，没有尾随零',
                                                    '多选几个数，最低位只会被 `1` 拉成 `1`，不会变回 `0`',
                                                    '所以只在偶数里选，且至少选 ==两个==']),],
        one_liner='奇数一参与，或结果最低位必为 1；只看有几个偶数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从数组里选 ==两个或更多== 元素做按位或，结果的二进制要有至少一个尾随零',
                 '示例：`[1,2,3,4,5]`，选 `2` 和 `4`，或 = `6` = `110` → `true`',
                 '`[1,3,5,7,9]` 全是奇数 → `false`'],
        quote='nums 中的奇数肯定不能参与或运算，这会导致或运算结果的最低位必然是 1。所以只有偶数能参与或运算，这样最低位必然是 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['或运算：只要有一个数最低位是 1，结果最低位就是 1',
              '想要尾随零，只能挑偶数；偶数的或，最低位一定是 0',
              '题目要求至少选两个 → 数组里至少要有 ==两个偶数=='],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`x % 2` 是 1 就是奇数，`sum` 数出奇数个数，用总数一减得偶数个数',
                 '易错：必须选至少两个元素，只有一个偶数时不行',
                 '同类：位运算里「只看最低位」的奇偶性思路'],
    ),
)

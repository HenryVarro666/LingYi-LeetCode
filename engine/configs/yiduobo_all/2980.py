CONFIG = dict(
    num=2980, title='检查按位或是否存在尾随零', difficulty='Easy', category='位运算',
    author='yiduobo', technique='一趟遍历 · 统计偶数',
    tags=['灵神题单·位运算', '难度分 1234'],
    code='''
class Solution(object):
    def hasTrailingZeros(self, nums):

        even = 0
        for v in nums:
            if v % 2 == 0:
                even += 1
        
        return even >= 2
''',
    call='Solution().hasTrailingZeros([1,2,3,4,5])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 已数到的偶数）', cell=96, h=260,
             color=lambda S, i, v: 'green' if v % 2 == 0 and 'even' in S and sum(1 for u in S['nums'][:i + 1] if u % 2 == 0) <= S['even'] else None,
             dim=lambda S, i, v: False),
        dict(type='text', h=110, size=30,
             fn=lambda S: f'目前偶数个数 `even = ` =={S["even"]}==，还差 =={max(0, 2 - S["even"])}== 个才满足' if 'even' in S else ''),
    ],
    watch=[('v', 'v', 'blue'), ('even', 'even', 'green')],
    captions={
        'even = 0': '`even` 统计数组里偶数的个数',
        'for v in nums': lambda S, B, r: (f'取下一个数 `v = {S.v}`' if 'v' not in B or True else ''),
        'if v % 2 == 0': lambda S, B, r: (f'`{S.v} % 2 == 0`，是偶数，可以参与或运算' if S.v % 2 == 0
                                          else f'`{S.v}` 是奇数：一参与结果最低位就是 1，==不能选=='),
        'even += 1': '偶数个数 `even = {even}`',
        'return even >= 2': '`even = {even}`，`even >= 2` → `{ret}`：至少两个偶数，选它们做或，最低位是 0',
    },
    cards=dict(
        one_liner='奇数一参与，结果最后一位必为 1，只能靠偶数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从数组里选 ==两个或更多== 元素做按位或，结果的二进制要有至少一个尾随零',
                 '示例：`[1,2,3,4,5]` → `true`（选 2 和 4）',
                 '`[1,3,5,7,9]` → `false`'],
        quote='只要有一个奇数参与了运算，结果的最后这一位就必然为一。为了让末尾为零，就只能选出若干个偶数来进行计算，也就是说数组中必须存在至少两个偶数。',
        quote_src='—— yiduobo 题解原文',
        idea=['按位或：某一位只要有一个 1，结果这一位就是 1',
              '末位要是 0，参与的数末位都得是 0，即全是偶数',
              '一趟遍历数偶数，`even >= 2` 就行'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '“两个或更多”所以偶数个数要 `>= 2`，不是 `>= 1`',
                 '和灵神对比：灵神用 `len − sum(x % 2)` 一行算偶数个数；yiduobo 写成显式循环计数'],
    ),
)

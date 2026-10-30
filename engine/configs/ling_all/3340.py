def _col(S, i, v):
    if 'i' not in S or i > S['i']:
        return None
    return 'pink' if i % 2 == 0 else 'cyan'


CONFIG = dict(
    num=3340, title='检查平衡字符串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='奇偶下标 · 一个变量记差',
    tags=[],
    code='''
class Solution:
    def isBalanced(self, num: str) -> bool:
        s = 0
        for i, c in enumerate(map(int, num)):
            s += c if i % 2 else -c
        return s == 0
''',
    call='Solution().isBalanced("24123")',
    expect=True,
    views=[
        dict(type='string', var='num', pointers={'i': 'blue'}, color=_col, h=200, label='num（粉 = 偶数下标取负，青 = 奇数下标取正）'),
        dict(type='text', size=34, h=120, fn=lambda S: f"奇数下标和 − 偶数下标和 `s` = =={S['s']}==" if 's' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), 'c', ('s', 's', 'green')],
    captions={
        's = 0': '`s` 记录「奇数下标之和 − 偶数下标之和」，初始为 0',
        's += c if i % 2 else -c': lambda S, B, r: (
            f"下标 `{S.i}` 是奇数 → 加上 `{S.c}`：`s` = {B.s} + {S.c} = =={S.s}==" if S.i % 2
            else f"下标 `{S.i}` 是偶数 → 减去 `{S.c}`（取相反数）：`s` = {B.s} − {S.c} = =={S.s}=="),
        'return s == 0': lambda S, B, r: (
            f'`s = {S.s}`，奇偶下标之和相等 → ==平衡字符串==，返回 `True`' if S.s == 0
            else f'`s = {S.s} ≠ 0`，两边之和不同 → 返回 `False`'),
    },
    cards=dict(
        one_liner='偶数下标取负，一个变量 s 就能判相等',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数字串 `num`，偶数下标数字之和 == 奇数下标数字之和，就是平衡字符串',
                 '示例：`"1234"` → `false`（4 ≠ 6）',
                 '本视频：`"24123"` → `true`（6 = 6）'],
        quote='把偶数下标对应的数字取相反数，这样只需一个变量 s 记录 奇数之和 - 偶数之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「奇数之和 = 偶数之和」等价于「奇数之和 − 偶数之和 = 0」',
              '遍历时奇数下标 `+c`，偶数下标 `−c`，不用开两个变量',
              '最后看 `s` 是不是 0'],
        summary=['时间 `O(n)`，空间 `O(1)`（`map` 是惰性的，不建数组）',
                 '下标从 0 开始：下标 0 算「偶数」，要取负',
                 '另一种写法：`sum(a[::2]) == sum(a[1::2])`，用 Python 切片，空间 `O(n)`'],
    ),
)

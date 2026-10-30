def _col(S, i, v):
    if 'index' not in S or i > S['index']:
        return None
    return 'pink' if i % 2 == 0 else 'cyan'


CONFIG = dict(
    num=3340, title='检查平衡字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · 维护奇偶差值',
    tags=[],
    code='''
class Solution(object):
    def isBalanced(self, num):

        diff = 0
        for index, c in enumerate(num):
            if index % 2 == 0:
                diff += int(c)
            else:
                diff -= int(c)
        
        return diff == 0
''',
    call='Solution().isBalanced("24123")',
    expect=True,
    views=[
        dict(type='string', var='num', pointers={'index': 'blue'}, color=_col, h=200, label='num（粉 = 偶数下标加，青 = 奇数下标减）'),
        dict(type='text', size=34, h=120, fn=lambda S: f"偶数下标和 − 奇数下标和 `diff` = =={S['diff']}==" if 'diff' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('c', 'c'), ('diff', 'diff', 'green')],
    captions={
        'diff = 0': '`diff` 表示「偶数下标之和 − 奇数下标之和」，初始为 0',
        'if index % 2 == 0': lambda S, B, r: (
            f'下标 `{S.index}` 是偶数 → 数字 `{S.c}` 属于偶数下标一侧' if S.index % 2 == 0
            else f'下标 `{S.index}` 是奇数 → 数字 `{S.c}` 属于奇数下标一侧'),
        'diff += int(c)': '偶数下标：`diff` = {B.diff} + {c} = =={diff}==',
        'diff -= int(c)': '奇数下标：`diff` = {B.diff} − {c} = =={diff}==',
        'return diff == 0': lambda S, B, r: (
            f'`diff = {S.diff}`：两侧之和相等 → 返回 `True`' if S.diff == 0
            else f'`diff = {S.diff} ≠ 0` → 返回 `False`'),
    },
    cards=dict(
        one_liner='按下标奇偶更新差值，最后看差是不是 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数字串 `num`，偶数下标数字之和等于奇数下标数字之和，则为平衡字符串',
                 '示例：`"1234"` → `false`，`"24123"` → `true`',
                 '本视频：`"24123"`：2+1+3 = 4+2 = 6'],
        quote='比较基础的题目，直接一趟遍历，根据下标的奇偶性计算更新奇偶下标数字之和的差值即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['不必分别求两个和，只维护它们的==差值== `diff`',
              '偶数下标加、奇数下标减，遍历一遍',
              '差为 0 就说明两侧相等'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '下标 0 是偶数，别把奇偶搞反',
                 '字符要先 `int(c)` 转成数字再加减',
                 '原文就是 Python 3 可运行的写法，代码未改动'],
    ),
)

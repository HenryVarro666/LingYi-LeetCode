CONFIG = dict(
    num=3931, title='检查相邻数字差', difficulty='Easy', category='字符串',
    author='yiduobo', technique='直接模拟 · 逐对比较',
    tags=[],
    code='''
class Solution(object):
    def isAdjacentDiffAtMostTwo(self, s):
        
        for index in range(1, len(s)):
            if abs(int(s[index]) - int(s[index - 1])) > 2:
                return False

        return True
''',
    call='Solution().isAdjacentDiffAtMostTwo("13289")',
    expect=False,
    views=[
        dict(type='text', size=28, fn=lambda S: (f"比较 `s[{S['index']-1}] = {S['s'][S['index']-1]}` 和 `s[{S['index']}] = {S['s'][S['index']]}`：差 `{abs(int(S['s'][S['index']]) - int(S['s'][S['index']-1]))}`，限制 `≤ 2`" if 'index' in S else '')),
        dict(type='string', var='s', label='s（蓝 = s[index-1]，粉 = s[index]）', cell=110, h=220,
             pointers={'index - 1': 'blue', 'index': 'pink'} if False else {'index': 'pink'},
             color=lambda S, i, v: ('pink' if i == S['index'] else 'blue' if i == S['index'] - 1 else None) if 'index' in S else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
    ],
    watch=[('index', 'index', 'pink'), ('差', 'abs(int(s[index]) - int(s[index - 1])) if "index" in dir() and index >= 1 else "-"', 'orange')],
    captions={
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：看第 `{S.index}` 位和它前一位' if 'index' in S and S.index != B.get('index') or 'index' not in B
                                               else '所有相邻对都检查完了，没有超限'),
        'if abs': lambda S, B, r: (f"`|{S.s[S.index]} - {S.s[S.index-1]}| = {abs(int(S.s[S.index]) - int(S.s[S.index-1]))}`"
                                   + (' 大于 2 → ==这一对超限==' if abs(int(S.s[S.index]) - int(S.s[S.index-1])) > 2 else ' 不大于 2 → 合格，继续')),
        'return False': '有一对差大于 2 → 整体不合格，立刻返回 `False`',
        'return True': '每一对都合格 → 返回 `True`',
    },
    cards=dict(
        one_liner='从下标 1 开始，逐个和前一位比，差超过 2 就失败',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数字字符串 `s`，看每一对相邻数字',
                 '所有绝对差都 `≤ 2` 返回 `true`，否则 `false`',
                 '示例：`"132"` → `true`；`"129"` → `false`；本视频：`"13289"`'],
        quote='从下标1开始向后遍历。对于当前遍历到的下标index，若nums[index]与nums[index - 1]差的绝对值大于2，则返回false。若顺利遍历完成，则返回true。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标从 `1` 开始，才有前一位可比',
              '字符要先 `int()` 转成数字再相减',
              '一旦发现超限立刻返回；全部通过才返回 `True`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`s[index]` 是字符，必须 `int()` 之后再做减法',
                 '易错：循环从 `1` 开始，从 `0` 开始会比较 `s[-1]`',
                 '原文已是 Python 3 可运行写法，代码未改',
                 '对比灵神：灵神用 `all` + `pairwise` 一行写完，这里是显式 `for` 循环'],
    ),
)

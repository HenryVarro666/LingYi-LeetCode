_POS = [-1]


def _next(S, B, r):
    _POS[0] = _POS[0] + 1 if 'char' in B else 0
    if _POS[0] >= len(S.s):
        return '所有字符都看完了，退出循环'
    return f'看下一个字符 `{S.char}`（下标 {_POS[0]}）'


CONFIG = dict(
    num=2315, title='统计星号', difficulty='Easy', category='字符串',
    author='yiduobo', technique='布尔标记 flag 一趟遍历',
    code='''
class Solution(object):
    def countAsterisks(self, s):

        res = 0
        flag = False
        for char in s:
            if char == '|':
                flag = not flag
            elif char == '*' and not flag:
                res += 1
        
        return res
''',
    call="Solution().countAsterisks('l|*e*et|c**o|*de|')",
    expect=2,
    views=[
        dict(type='string', var='s', label='s（橙 = 竖线）', cell=40, h=220,
             color=lambda S, i, v: 'orange' if v == '|' else None),
        dict(type='text', size=34, fn=lambda S: ('当前 `flag = ' + str(S['flag']) + '`：' + ('==在竖线对里面==，星号不算' if S['flag'] else '==在对外面==，星号要数')) if 'flag' in S else ''),
    ],
    watch=['char', ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计不在竖线对之间的星号数',
        'flag = False': '`flag` 表示当前是否==在竖线对里面==：一开始在外面，`False`',
        'for char in s': _next,
        "if char == '|'": lambda S, B, r: ('`char` 是竖线 → 进入或离开一个竖线对' if S.char == '|' else '`char` 不是竖线，看下一个条件'),
        'flag = not flag': '遇到竖线：`flag` 取反 → ==`{flag}`==（{"进入竖线对" if flag else "离开竖线对"}）',
        "elif char == '*'": lambda S, B, r: (f'`char` 是星号，且 `flag = {S.flag}`：==在对外面，要数==' if S.char == '*' and not S.flag
                                             else (f'`char` 是星号，但 `flag = True`：在对里面，不数' if S.char == '*' else f'`char = {S.char}` 是普通字母，跳过')),
        'res += 1': '数到一个对外面的星号：`res` → =={res}==',
        'return res': '遍历结束，不在竖线对之间的星号共 =={res}== 个',
    },
    cards=dict(
        one_liner='用一个 flag 记录现在是否在竖线对里面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['竖线 `|` 两两成对，求==不在竖线对之间==的 `*` 的个数',
                 '题目保证竖线是成对出现的',
                 '示例：`l|*e*et|c**o|*de|` → `2`'],
        quote='可以使用一个状态标记flag来表示当前是否处于竖线对中，并根据竖线出现的情况来更新flag的值。flag的初始值为false，表示一开始不在竖线对中。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：遇到 `|` 就把 `flag` 取反', '遇到 `*` 且 `flag` 为假，答案加 1；否则不处理',
              '其他字符直接跳过'],
        summary=['时间 `O(n)`，空间 `O(1)`，只用一个布尔变量',
                 '`flag` 初始为 `False`：第一个竖线之前不在对里面',
                 '星号要同时满足「是 `*`」和「`not flag`」才加 1',
                 '对比灵神：他用 `split` + `[::2]` 一行搞定，yiduobo 手动维护状态'],
    ),
)

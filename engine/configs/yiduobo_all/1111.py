SEQ = '(()(()))'


def _info(S):
    if 'index' not in S:
        return '按层数奇偶划分：偶数层给 A（0），奇数层给 B（1）'
    i, c = S['index'], S['char']
    if c == '(':
        return f'左括号：层数 k 与下标 `{i}` 同奇偶 → 下标{"偶" if i % 2 == 0 else "奇"}'
    return f'右括号：层数 k 与下标奇偶相反 → 下标 `{i}` 是{"偶" if i % 2 == 0 else "奇"}数'


def _col(S, i, v):
    if 'res' not in S:
        return None
    cur = S['index']
    if i == cur and len(S['res']) <= cur:
        return 'yellow'
    if i < len(S['res']):
        return 'cyan' if S['res'][i] == 0 else 'orange'
    return None


CONFIG = dict(
    num=1111, title='有效括号的嵌套深度', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按层数奇偶划分 · 下标奇偶判层',
    tags=['栈', '合法括号字符串', '难度分 1749'],
    code='''
class Solution(object):
    def maxDepthAfterSplit(self, seq):

        res = []
        for index, char in enumerate(seq):
            if char == '(':
                if index % 2 == 0:
                    res.append(0)
                else:
                    res.append(1)
            else:
                if index % 2 == 0:
                    res.append(1)
                else:
                    res.append(0)
        
        return res
''',
    call=f'Solution().maxDepthAfterSplit({SEQ!r})',
    expect=[0, 1, 1, 1, 0, 0, 1, 0],
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='string', var='seq', label='seq（黄 = 当前括号，青 = 进 A，橙 = 进 B）', pointers={'index': 'blue'}, color=_col, cell=90, h=200),
        dict(type='array', var='res', label='res（0 = A，1 = B）', cell=90, h=200,
             color=lambda S, i, v: 'cyan' if v == 0 else 'orange'),
        dict(type='text', fn=lambda S: ('左括号：下标奇偶 = 层数奇偶；右括号：下标奇偶 与 层数奇偶相反' if 'index' in S else ''), size=24, h=80),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 依次记录每个括号分给 A（0）还是 B（1）',
        'for index, char': lambda S, B, ret: ('整串扫描完毕' if 'index' in B and B.index == S.index else f'看第 `{S.index}` 个括号 `{S.char}`'),
        "if char == '('": lambda S, B, ret: (f"`{S.char}` 是左括号：它的层数 k 与下标 `{S.index}` ==同奇偶==" if S.char == '(' else f"`{S.char}` 是右括号：它的层数 k 与下标 `{S.index}` ==奇偶相反=="),
        'if index % 2 == 0': lambda S, B, ret: f'下标 `{S.index}` 是{"偶" if S.index % 2 == 0 else "奇"}数 → 看这一支{"成立" if S.index % 2 == 0 else "不成立，走 else"}',
        'res.append(0)': '加入 `0`：这个括号属于 ==A 组==，`res = {res}`',
        'res.append(1)': '加入 `1`：这个括号属于 ==B 组==，`res = {res}`',
        'return res': '一趟扫描完成，返回 `{ret}`',
    },
    cards=dict(
        one_liner='偶数层进 A、奇数层进 B，下标奇偶就能判断层数',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['把有效括号序列拆成两个有效子序列 A、B',
                 '使两者的最大深度尽量小，用 0/1 标记每个括号属于谁',
                 '示例：`"()(())()"` → `[0,0,0,1,1,0,1,1]`'],
        quote='将其第0、2、4、...这些偶数层分到A组，将1、3、5、...这些奇数层分到B组，这样一来就可以使得最终答案的最大深度最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前是第 k 层左括号：前面有 k 个未匹配左括号加 n 组匹配括号 → 下标 `= k + 2n`',
              '所以左括号的下标奇偶就是层数奇偶',
              '右括号前面还多一个本层左括号 → 下标 `= k + 2n + 1`，奇偶正好相反'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '不用栈、不用数深度：只看下标 `index % 2` 和括号方向',
                 '易错：右括号的奇偶判断与左括号==相反==',
                 '对比灵神：灵神把左右括号合并成 `(i + ord(ch)) % 2`；这里是分支写法'],
    ),
)

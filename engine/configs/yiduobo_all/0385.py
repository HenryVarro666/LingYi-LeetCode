SETUP = '''
class NestedInteger:
    def __init__(self, value=None):
        self._v = value if value is not None else []
        self._int = value is not None
    def isInteger(self):
        return self._int
    def add(self, elem):
        self._v.append(elem)
    def setInteger(self, value):
        self._v, self._int = value, True
    def getInteger(self):
        return self._v if self._int else None
    def getList(self):
        return None if self._int else self._v
    def __repr__(self):
        return str(self._v) if self._int else '[' + ','.join(map(repr, self._v)) + ']'
'''

ST = {'i': -1}


def trk(fn):
    """代码里没有下标变量：每次执行 for 行就把「当前第几个字符」记进 S['_inner']，供视图高亮。"""
    def cap(S, B, ret):
        if S['_line'] == 8:
            ST['i'] = ST['i'] + 1 if 'char' in B else 0
        S['_inner']['_i'] = ST['i']
        if callable(fn):
            return fn(S, B, ret)
        from make import render_caption
        return render_caption(fn, S, B, ret)
    return cap


def _is(c):
    return lambda S, B, r: (f'`{S.char}` 是 `{c}` → 进入这个分支' if S.char == c else f'`{S.char}` 不是 `{c}` → 看下一类字符')


def _digit(S, B, r):
    if S.char.isdigit():
        return f'`{S.char}` 是数字字符（ASCII 48–57）→ 累积成数'
    return f'`{S.char}` 不是数字 → 看下一类字符'


CAPS = {
    4: trk('`stack` 存放还没结束的 NestedInteger：遇 `[` 压入，遇 `]` 弹出'),
    5: trk('`now` 是正在拼的数字，`None` 表示还没读到数字'),
    6: trk('`sign` 记正负号，默认 `1`'),
    8: trk(lambda S, B, r: f'读第 {ST["i"] + 1} 个字符：`{S.char}`'),
    9: trk(_is('[')),
    10: trk('左括号：新建一个空 NestedInteger 压栈，之后的内容都属于它 → 栈深 `{len(stack)}`'),
    12: trk(_digit),
    13: trk(lambda S, B, r: '`now` 还是 `None`：这是数字的第一位' if S.now is None else f'`now = {S.now}` 已有前几位，继续往后拼'),
    14: trk('第一位：`now = {now}`'),
    16: trk('接着往后拼：`now = {B.now} × 10 + {char}` = =={now}=='),
    18: trk(_is(',')),
    19: trk(lambda S, B, r: '逗号前有数字 → 它是列表里的一项' if S.now is not None else '逗号前没有数字（例如 `],[` 的逗号）→ 无事发生'),
    20: trk('数字带上符号加进栈顶：`stack[-1].add(NestedInteger({sign * now}))`，栈顶变成 `{stack[-1]}`'),
    21: trk('数字已入列，`now` 清空，准备读下一项'),
    22: trk('符号重置为 `1`'),
    24: trk(_is('-')),
    25: trk('读到负号：`sign = -1`，等数字出来再乘'),
    27: trk(_is(']')),
    28: trk(lambda S, B, r: f'右括号前还有没入列的数字 `{S.now}` → 先加进去' if S.now is not None else '右括号前没有数字（刚结束一个子列表或空列表）'),
    29: trk('补上最后一项：`stack[-1].add(NestedInteger({sign * now}))` → `{stack[-1]}`'),
    30: trk('弹出栈顶，当前这个 NestedInteger 完结：`tmp = {tmp}`'),
    31: trk(lambda S, B, r: '栈空了：第一个 `[` 也被弹出，整体完结' if not S.stack else f'栈里还有外层 `{S.stack[-1]}`，`tmp` 要并入它'),
    32: trk('栈弹空 → 直接返回整个结果 `{tmp}`'),
    34: trk('`tmp` 并入外层：`stack[-1].add(tmp)` → `{stack[-1]}`'),
    35: trk('`now` 清空'),
    36: trk('符号重置'),
    38: trk('整个字符串就是一个数字（样例一）→ 直接返回 `NestedInteger(sign * now)`'),
}


def _txt(S):
    if 'now' not in S:
        return ''
    return f"当前数字 `now = {S['now']}`　符号 `sign = {S['sign']}`"


CONFIG = dict(
    num=385, title='迷你语法分析器', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 遇括号压栈弹栈',
    tags=[],
    code='''
class Solution(object):
    def deserialize(self, s):

        stack = []
        now = None
        sign = 1

        for char in s:
            if char == '[':
                stack.append(NestedInteger())

            elif ord(char) >= 48 and ord(char) <= 57:
                if now is None:
                    now = int(char)
                else:
                    now = now * 10 + int(char)

            elif char == ',':
                if now is not None:
                    stack[-1].add(NestedInteger(sign * now))
                now = None
                sign = 1

            elif char == '-':
                sign = -1

            elif char == ']':
                if now is not None:
                    stack[-1].add(NestedInteger(sign * now))
                tmp = stack.pop()
                if not stack:
                    return tmp
                else:
                    stack[-1].add(tmp)
                now = None
                sign = 1

        return NestedInteger(sign * now)
''',
    setup=SETUP,
    call="Solution().deserialize('[-3,[4,[]]]')",
    expect='[-3,[4,[]]]',
    result_fn=str,
    views=[
        dict(type='string', var='s', h=150, label='输入字符串（黄 = 正在读的字符）',
             color=lambda S, i, v: 'yellow' if i == S['_inner'].get('_i') else None,
             dim=lambda S, i, v: i < S['_inner'].get('_i', -1)),
        dict(type='text', fn=_txt, size=28),
        dict(type='stack', var='stack', h=330, label='stack（栈顶在上）', fmt=lambda x: repr(x)),
    ],
    watch=[('char', 'char', 'yellow'), ('now', 'now', 'cyan'), ('sign', 'sign', 'orange')],
    captions=CAPS,
    max_steps=80,
    cards=dict(
        one_liner='遇 `[` 压栈、遇 `]` 弹栈，弹出的结果并入外层',
        complexity='时间 `O(n)`，空间 `O(d)`（d 为嵌套深度）',
        problem=['把字符串解析成 `NestedInteger`：它要么是一个整数，要么是一个嵌套列表',
                 '字符串里有 `[` `]` `,` 数字，数字可以是负数',
                 '示例：`"324"` → 整数 324；`"[123,[456,[789]]]"` → 嵌套列表',
                 '本视频：`"[-3,[4,[]]]"`'],
        quote='这类问题一般做法就是弄一个栈，在碰到某些特定字符时将当前结果压入栈中，然后继续往后处理，直到碰到另一个特定字符时就将栈中的值弹出进行某些运算。',
        quote_src='—— yiduobo 题解原文',
        idea=['`[`：新建一个 NestedInteger 压栈，后面的内容都属于它',
              '`,`：若前面有数字，把数字加进栈顶；没有（如 `],[`）就什么也不做',
              '`]`：补上最后的数字，弹栈；栈空了就是答案，否则并入外层',
              '数字可能为负，所以单独维护 `sign`'],
        summary=['时间 `O(n)`，空间 `O(d)`',
                 '`now is None` 与 `now == 0` 要区分：0 也是一个有效数字',
                 '`]` 前要把还没入列的数字补进去；逗号或右括号后记得重置 `now` 和 `sign`',
                 '整个字符串只是一个数字时不会进栈，在循环外直接返回',
                 '原文代码未改动；NestedInteger 的 API 由题目给出，视频里用等价的小类代替'],
    ),
)

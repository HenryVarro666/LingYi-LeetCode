SETUP = '''
class _Str(str):
    k = -1
    def __iter__(self):
        for j, ch in enumerate(str.__iter__(self)):
            self.k = j
            yield ch
        self.k = len(self)
'''
S0 = 'abc1d23e'


def _k(S):
    s = S.get('s')
    k = getattr(s, 'k', -1)
    return k if 0 <= k < len(S['s']) else None


def _show(S):
    if 'stack' not in S:
        return '最左数字配左侧最近字符：先进后出 → 栈'
    return f"栈中剩余字符 = `\"{''.join(S['stack'])}\"`"


CONFIG = dict(
    num=3174, title='清除数字', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='正序遍历 · 栈存未删字符',
    tags=[],
    code='''
class Solution(object):
    def clearDigits(self, s):
        stack = []
        for char in s:
            if '0' <= char <= '9':
                if stack:
                    stack.pop()
            else:
                stack.append(char)

        return ''.join(stack)
''',
    setup=SETUP,
    call=f'Solution().clearDigits(_Str({S0!r}))',
    expect='ae',
    views=[
        dict(type='string', var='s', label='s（框 = 当前字符）', cell=90, h=210,
             pointers={_k: 'blue'}, pointer_labels={_k: 'char'},
             window=(_k, _k)),
        dict(type='stack', var='stack', label='stack（已遍历且未删除的字符，栈顶在右）', h=160, font=34),
        dict(type='text', fn=_show, size=30, h=90),
    ],
    watch=[('char', 'char', 'blue'), ('stack', 'stack', 'green')],
    captions={
        'stack = []': '`stack` 保存遍历过、还没被删掉的字符',
        'for char in s': lambda S, B, ret: (f"正序遍历：`s[{_k(S)}] = {S.char!r}`" if _k(S) is not None else '遍历完成'),
        "if '0' <= char <= '9'": lambda S, B, ret: (f"`{S.char!r}` 是数字：要删它左侧最近的字符" if S.char.isdigit()
                                                    else f"`{S.char!r}` 是字符：留下来，等以后的数字来删"),
        'if stack': lambda S, B, ret: (f"栈非空 `{S.stack}`：栈顶就是左侧最近的字符" if S.stack
                                       else '栈为空：左边没有字符可删（题目保证不会出现）'),
        'stack.pop()': '删去栈顶 `{B.stack[-1]!r}`，这个数字也不入栈，一起消失',
        'stack.append(char)': '`{char!r}` 入栈，栈顶是 `{stack[-1]!r}`',
        'return': '栈中剩余字符拼接 = `{ret!r}`',
    },
    cards=dict(
        one_liner='最左数字删最近字符：正序遍历 + 栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 含小写字母和数字，每轮删除最左侧的数字以及它左侧最近的字符',
                 '问删完所有数字后剩下的字符串',
                 '示例：`"cb34"` → `""`',
                 '本视频：`"abc1d23e"` → `"ae"`'],
        quote='为了适配最左侧的数字，就可以考虑正序遍历，逐个处理遍历到的数字……是先进后出的场景，因此可以使用栈来储存遍历过的字符',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮删的都是最左的数字 → ==正序遍历==逐个处理数字',
              '数字左侧最近的字符 = 已遍历且未被删除的最后一个字符',
              '后进先出 → 用栈存字符，遇数字删栈顶，最后栈里就是答案'],
        result='栈中剩 `a`、`e` → 返回 `"ae"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文有 `if stack` 防空，更稳；题目保证有解时它总为真',
                 '连续数字依次删掉栈顶，所以 `2`、`3` 删的是 `d`、`b`',
                 '原文为 Python 2 风格，只删去 def 后空行，代码无需其他修改'],
    ),
)

STR = 'erase***'


def _f(prefix):
    """prefix 经过「星号删左边最近字母」之后剩下的字符串"""
    st = []
    for ch in prefix:
        if ch == '*':
            st.pop()
        else:
            st.append(ch)
    return ''.join(st)


def _pos(S):
    """(当前下标 k, 已处理的前缀长度 upto)。s 里有重复字符，用 c 和栈内容反查。"""
    c, st = S.get('char'), S.get('stack')
    if c is None or st is None:
        return None
    after = S.get('_line', 0) in (6, 8, 10)     # pop / append 之后，栈里已经包含 s[k] 的效果
    cur = ''.join(st)
    for k, ch in enumerate(STR):
        if ch == c and _f(STR[:k + (1 if after else 0)]) == cur:
            return k, k + (1 if after else 0)
    return len(STR) - 1, len(STR)               # for 循环结束的那一步


def _k(S):
    p = _pos(S)
    return None if p is None else p[0]


def _done(S):
    """已处理过的下标 -> 状态（用下标栈模拟）"""
    p = _pos(S)
    if p is None:
        return {}
    alive, res = [], {}
    for i, ch in enumerate(STR[:p[1]]):
        if ch == '*':
            res[alive.pop()] = 'gone'
            res[i] = 'star'
        else:
            alive.append(i)
            res[i] = 'keep'
    return res


def _color(S, i, v):
    p = _pos(S)
    if p is None:
        return None
    if i == p[0] and p[1] == p[0]:
        return 'blue'
    return {'keep': 'green', 'star': 'orange'}.get(_done(S).get(i))


def _dim(S, i, v):
    return _done(S).get(i) == 'gone'


def _text(S):
    st = S.get('stack')
    if st is None:
        return '每个 `*` 吃掉一个字符：吃的就是栈里==最后存进去的那个=='
    p = _pos(S)
    if _done_loop(S) or S.get('_line') == 10:
        return f"遍历完了，栈里是 `\"{''.join(st)}\"`"
    return f"处理 `s[{p[0]}] = '{STR[p[0]]}'`，栈里现在是 `\"{''.join(st)}\"`"


def _done_loop(S):
    p = _pos(S)
    return p is not None and p[1] == len(STR) and S.get('_line') == 4


KP = lambda S: _k(S)


CONFIG = dict(
    num=2390, title='从字符串中移除星号', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 一趟遍历',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1348'],
    code='''
class Solution(object):
    def removeStars(self, s):
        stack = []
        for char in s:
            if char == '*':
                stack.pop()
            else:
                stack.append(char)

        return ''.join(stack)
''',
    call=f'Solution().removeStars({STR!r})',
    expect='er',
    views=[
        dict(type='text', fn=_text, size=28, h=64),
        dict(type='string', var='s', label='s（蓝 = 正在看的字符，绿 = 还在栈里，橙 = 星号，暗 = 已被星号吃掉）', cell=84,
             pointers={KP: 'blue'}, pointer_labels={KP: 'char'}, color=_color, dim=_dim, h=230),
        dict(type='stack', var='stack', label='stack', font=34, h=130),
        dict(type='text', fn=lambda S: (f"栈里有 `{len(S['stack'])}` 个字符，每个星号吃掉一个" if S.get('stack') is not None else ''), size=24, h=50),
    ],
    watch=[('char', 'char', 'blue'), ('stack', 'stack', 'green'), ('len(stack)', 'len(stack)')],
    captions={
        'stack = []': '准备一个栈 `stack`，存放当前还没被吃掉的字符',
        'for char in s': lambda S, B, ret: ('一趟遍历结束，栈里剩下的就是最终答案' if _done_loop(S)
                                            else f"从头往后看第 `{_k(S)}` 个字符 `'{S.char}'`"),
        "if char == '*'": lambda S, B, ret: (f"`'*'`：它会消耗掉当前存着的==最后一个字符=={'（连续星号，接着吃）' if _k(S) and STR[_k(S) - 1] == '*' else ''}"
                                             if S.char == '*' else f"`'{S.char}'` 是普通字符：先存起来，等着后面的星号"),
        'stack.pop()': lambda S, B, ret: f"弹出栈顶 `'{B.stack[-1]}'`，被这个星号吃掉；栈里还剩 `{len(S.stack)}` 个：`\"{''.join(S.stack)}\"`",
        'stack.append(char)': lambda S, B, ret: f"`'{S.char}'` 入栈，栈里现在有 `{len(S.stack)}` 个：`\"{''.join(S.stack)}\"`",
        'return': '栈里剩下的字符从底到顶拼起来 `"{ret}"`，就是答案',
    },
    cards=dict(
        one_liner='星号会吃掉最后存的字符：这正是栈的后进先出',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `s` 里有若干 `*`，每个 `*` 会删掉自己和==它左边最近的非星号字符==',
                 '题目保证每次都有字符可删，返回删完所有星号后的字符串',
                 '本视频用 `"erase***"`：三个连续星号把后三个字符吃掉 → `"er"`'],
        quote='每个星号则会消耗掉当前储存的最后一个字符，那么很自然联想到使用栈来储存字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['“消耗最后一个字符”：后存的先被删，是典型的后进先出',
              '一趟遍历：星号 → 弹出栈顶；其他字符 → 入栈',
              '遍历完成后，栈里剩余的字符就是最终答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '连续星号会连续弹栈，`"erase***"` 弹了三次',
                 '题目保证有字符可删，所以 `stack.pop()` 不会遇到空栈',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：思路相同，灵神额外指出把 `s` 当栈可做到空间 `O(1)`'],
    ),
)

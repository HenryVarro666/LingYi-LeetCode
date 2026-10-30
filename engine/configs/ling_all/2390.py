STR = 'leet**cod*e'


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
    c, st = S.get('c'), S.get('st')
    if c is None or st is None:
        return None
    after = S.get('_line', 0) in (6, 8, 9)      # pop / append 之后，栈里已经包含 s[k] 的效果
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
    st = S.get('st')
    if st is None:
        return '遇到 `*` 就删掉它左边最近的字母，==最近的 = 最后放进去的=='
    p = _pos(S)
    if _done_loop(S) or S.get('_line') == 9:
        return f"遍历完了，栈里是 `\"{''.join(st)}\"`"
    return f"处理 `s[{p[0]}] = '{STR[p[0]]}'`，栈里现在是 `\"{''.join(st)}\"`"


def _done_loop(S):
    p = _pos(S)
    return p is not None and p[1] == len(STR) and S.get('_line') == 4


KP = lambda S: _k(S)

CONFIG = dict(
    num=2390, title='从字符串中移除星号', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 星号弹栈顶',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1348'],
    code='''
class Solution:
    def removeStars(self, s: str) -> str:
        st = []
        for c in s:
            if c == '*':
                st.pop()
            else:
                st.append(c)
        return ''.join(st)
''',
    call=f'Solution().removeStars({STR!r})',
    expect='lecoe',
    views=[
        dict(type='text', fn=_text, size=28, h=64),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿 = 还在栈里，橙 = 星号，暗 = 已被删掉）', cell=84,
             pointers={KP: 'blue'}, pointer_labels={KP: 'c'}, color=_color, dim=_dim, h=230),
        dict(type='stack', var='st', label='st', font=34, h=130),
    ],
    watch=[('c', 'c', 'blue'), ('st', 'st', 'green'), ('len(st)', 'len(st)')],
    captions={
        'st = []': '用列表 `st` 当栈：存放==还没被删掉==的字母',
        'for c in s': lambda S, B, ret: ('遍历完了，栈里剩下的就是答案' if _done_loop(S)
                                         else f"从左到右遍历：`c = '{S.c}'`（`s[{_k(S)}]`）"),
        "if c == '*'": lambda S, B, ret: ("`c` 是星号：要删掉左边==最近的非星号字母==，也就是==栈顶=="
                                          if S.c == '*' else f"`c = '{S.c}'` 不是星号：先留着，之后可能被后面的星号删掉"),
        'st.pop()': lambda S, B, ret: f"弹出栈顶 `'{B.st[-1]}'`（离这个星号最近的字母）→ 栈变成 `\"{''.join(S.st)}\"`",
        'st.append(c)': lambda S, B, ret: f"`'{S.c}'` 入栈 → 栈变成 `\"{''.join(S.st)}\"`",
        'return': '栈底到栈顶拼起来 `"{ret}"`，就是删完所有星号的结果',
    },
    cards=dict(
        one_liner='遇到星号弹栈顶，否则入栈，最后栈里就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`（把 s 当栈可以做到 `O(1)`）',
        problem=['字符串 `s` 含若干星号 `*`，一步操作：选一个星号，删掉它==左侧最近的非星号字符==和它自己',
                 '返回删完所有星号后的字符串，输入保证每次都有字符可删',
                 '示例：`"leet**cod*e"` → `"lecoe"`'],
        quote='用栈维护，遇到星号 `*` 则弹出栈顶，否则把字符入栈。最后从栈底到栈顶就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['星号删的是==左边最近的字母==：最近 = 最后放进去的 = 栈顶',
              '字母先入栈；星号来了弹一个，连续星号就连续弹',
              '从栈底到栈顶读出来，顺序和原串一致'],
        summary=['时间 `O(n)`，空间 `O(n)`；把 `s` 当栈用可以优化到 `O(1)`（见灵神 C 语言写法）',
                 '题目保证有字母可删，所以 `st.pop()` 不会遇到空栈',
                 '连续星号 `**` 会连续弹出两个字母',
                 '同类题：3174. 清除数字；灵神数据结构题单 3.1 节、3.3 节'],
    ),
)

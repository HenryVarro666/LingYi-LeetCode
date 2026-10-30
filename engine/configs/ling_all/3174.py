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
    if 'st' not in S:
        return '数字删掉“它左边最近的字母”：后进先出 → 栈'
    return f"栈（栈底到栈顶）= `\"{''.join(S['st'])}\"`"


CONFIG = dict(
    num=3174, title='清除数字', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 遇数字弹栈顶',
    tags=[],
    code='''
class Solution:
    def clearDigits(self, s: str) -> str:
        st = []
        for c in s:
            if c.isdigit():
                st.pop()
            else:
                st.append(c)
        return ''.join(st)
''',
    setup=SETUP,
    call=f'Solution().clearDigits(_Str({S0!r}))',
    expect='ae',
    views=[
        dict(type='string', var='s', label='s（框 = 当前字符）', cell=90, h=210,
             pointers={_k: 'blue'}, pointer_labels={_k: 'c'},
             window=(_k, _k)),
        dict(type='stack', var='st', label='st（栈，栈顶在右）', h=160, font=34),
        dict(type='text', fn=_show, size=30, h=90),
    ],
    watch=[('c', 'c', 'blue'), ('st', 'st', 'green'), ('len(st)', 'len(st)')],
    captions={
        'st = []': '用列表 `st` 当栈，存放==还没被删掉==的字母',
        'for c in s': lambda S, B, ret: (f"读到 `s[{_k(S)}] = {S.c!r}`" if _k(S) is not None else '遍历完了，栈里剩下的就是答案'),
        'if c.isdigit()': lambda S, B, ret: (f"`{S.c!r}` 是数字 → 要删它左边==最近==的字母，也就是栈顶" if S.c.isdigit()
                                             else f"`{S.c!r}` 是字母 → 先留着，入栈"),
        'st.pop()': '弹出栈顶 `{B.st[-1]!r}`：它就是这个数字左边最近的字母，数字本身不入栈',
        'st.append(c)': '`{c!r}` 入栈，栈顶变成 `{st[-1]!r}`',
        'return': '栈底到栈顶拼起来 = `{ret!r}`',
    },
    cards=dict(
        one_liner='遇到数字就弹栈顶，剩下的字母就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['反复删除==第一个数字字符==以及它左边==最近的非数字字符==，直到没有数字',
                 '题目保证每个数字左边都有字母可删',
                 '示例：`"cb34"` → `""`',
                 '本视频：`"abc1d23e"` → `"ae"`'],
        quote='用栈维护，遇到数字则弹出栈顶，否则把字符入栈。最后从栈底到栈顶就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右读：每次删的都是==最左的数字==，它左边的字母都已经读过',
              '字母入栈；数字到来时，最近的字母就是栈顶，弹掉即可',
              '数字本身不入栈，等于和栈顶一起被删'],
        result='栈里剩下 `a`、`e` → 返回 `"ae"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`；把 s 当栈原地改可做到 `O(1)`（C 语言写法）',
                 '题目保证数字都能删，所以 `st.pop()` 前不用判空',
                 '连续数字会连续弹栈：`"abc1d23e"` 里 `2`、`3` 依次弹掉 `d`、`b`',
                 '栈入门题，可以练数据结构题单的 3.1、3.3 节'],
    ),
)

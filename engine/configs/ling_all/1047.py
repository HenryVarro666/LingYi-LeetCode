# 输入字符串用 _Str 包一层：遍历时每个字母带上自己的下标 .i，视图靠它画“当前读到哪”和“哪些还在栈里”
SETUP = '''
class _Ch(str):
    pass


class _Str(str):
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            c = _Ch(ch)
            c.i = k
            yield c
'''
TEXT = "abbaca"


def _sim(s):
    """复现算法，得到 {下标: 与它一起被消掉的栈顶下标}（只用于画图）"""
    st, pair = [], {}
    for k, ch in enumerate(s):
        if st and s[st[-1]] == ch:
            pair[k] = st.pop()
        else:
            st.append(k)
    return pair


PAIR = _sim(TEXT)


def _state(S):
    c = S.get('ch')
    if c is None:
        return None
    ln = S['_line']
    cur = c.i
    kept = {x.i for x in S['st']}
    red = set()
    if ln in (5, 6) and cur in PAIR:
        red = {cur, PAIR[cur]}
    return cur, kept, red, ln


def _color(S, i, v):
    r = _state(S)
    if r is None:
        return None
    cur, kept, red, ln = r
    if i in red:
        return 'red'
    if ln >= 9:
        return 'green' if i in kept else None
    if i == cur:
        return 'green' if (ln == 8 and i in kept) else 'blue'
    if i < cur and i in kept:
        return 'green'
    return None


def _dim(S, i, v):
    r = _state(S)
    if r is None:
        return False
    cur, kept, red, ln = r
    if i in red or i in kept:
        return False
    return i < cur or ln >= 9


def _msg(S, B):
    c = S.get('ch')
    if c is None:
        return '栈 `st` 记录所有“还没被消除”的字母'
    ln = S['_line']
    st = S['st']
    if ln == 4:
        return f'读到 `{c}`；左边最近没被消除的字母（栈顶）是 `{st[-1] if st else "（没有）"}`'
    if ln == 5:
        if not st:
            return '栈是空的 → 左边没有字母可以消'
        same = st[-1] == c
        return f'栈顶 `{st[-1]}` 和当前 `{c}` ' + ('==相同，能消==' if same else '不同，不能消')
    if ln == 6:
        return f'`{c}{c}` 消掉，栈里剩 `{"".join(st) or "空"}`'
    if ln == 8:
        return f'`{c}` 入栈，栈里 `{"".join(st)}`'
    return f'栈从底到顶拼起来：`{"".join(st)}`'


CONFIG = dict(
    num=1047, title='删除字符串中的所有相邻重复项', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 从左到右消除相邻相同字母',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1286'],
    code='''
class Solution:
    def removeDuplicates(self, s: str) -> str:
        st = []
        for ch in s:
            if st and st[-1] == ch:
                st.pop()
            else:
                st.append(ch)
        return ''.join(st)
''',
    setup=SETUP,
    call=f'Solution().removeDuplicates(_Str("{TEXT}"))',
    expect='ca',
    views=[
        dict(type='text', fn=_msg, size=28, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前字母，绿 = 还在栈里，红 = 正被消掉，灰 = 已消）', cell=84,
             pointers={'ch.i': 'blue'}, pointer_labels={'ch.i': 'ch'}, color=_color, dim=_dim, h=190),
        dict(type='stack', var='st', label='st（未被消除的字母）', fmt=lambda x: str(x), font=34, h=130),
    ],
    watch=[('ch', 'ch', 'blue'), ('栈顶', 'st[-1] if st else None', 'purple'), ('len(st)', 'len(st)', 'green')],
    captions={
        'st = []': '用栈 `st` 记录==所有未被消除==的字母，栈底到栈顶就是它们的顺序',
        'for ch in s': lambda S, B, ret: (f'从左到右读第 `{S.ch.i}` 个字母 `ch = {S.ch}`' if 'ch' not in B or B.ch.i != S.ch.i
                                          else '字母都读完了，栈里就是剩下的字母'),
        'if st and': lambda S, B, ret: (
            f'栈是空的，左边没有字母可以消 → `{S.ch}` 只能入栈' if not S.st else
            (f'栈顶 `{S.st[-1]}` == `ch = {S.ch}`：==左边最近的字母和它相同== → 消掉'
             if S.st[-1] == S.ch else f'栈顶 `{S.st[-1]}` ≠ `ch = {S.ch}` → 无法消除，入栈')),
        'st.pop()': lambda S, B, ret: (f'`{B.st[-1]}{S.ch}` 相邻重复：`ch` 不入栈，同时移除栈顶 `{B.st[-1]}`。'
                                       + (f'新栈顶是 `{S.st[-1]}`，它成了后面字母的“左邻居”' if S.st else '栈空了')),
        'st.append(ch)': '`{ch}` 无法消除，入栈 → 栈 `{"".join(st)}`',
        "return ''.join": '栈里从底到顶拼起来：`{ret}`',
    },
    cards=dict(
        one_liner='消除顺序不影响结果 → 从左到右，用栈记住没被消掉的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['小写字母串 `s`，每次选两个==相邻且相同==的字母删掉，直到不能再删',
                 '返回最终的字符串，答案唯一',
                 '示例：`"abbaca"` → 先删 `bb` 得 `aaca`，再删 `aa` 得 `"ca"`'],
        quote='如果栈不为空且 s[i] 与栈顶相同，那么可以消除 s[i]，同时移除栈顶。否则 s[i] 无法消除，把 s[i] 入栈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想：消除顺序会不会影响结果？`aaa` 先消前两个还是后两个，剩下的都是一个 `a` → ==不影响=='
              '，所以能从左到右消',
              '再想：消掉 `bb` 后，遍历到第二个 `a` 时怎么快速知道左边最近没被消的字母？',
              '需要 `O(1)` 查看、删除最近添加的字母 → ==栈=='],
        result='栈从底到顶是 `c`、`a`，返回 `"ca"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`（原地做法可以 `O(1)`，见灵神 C 语言写法二）',
                 '先判 `st and`，栈空时没有 `st[-1]`',
                 '返回的是字符串：最后要 `\'\'.join(st)`',
                 '连续奇数个相同字母（如 `aaa`）最后留下一个，偶数个全消掉',
                 '同类题：第 2696、3561 题，见题单 §3.3 邻项消除'],
    ),
)

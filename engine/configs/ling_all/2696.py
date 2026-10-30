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
TEXT = "ABFCACDB"


def _sim(s):
    """复现算法，得到 {下标: 与它一起被消掉的栈顶下标}（只用于画图）"""
    st, pair = [], {}
    for k, ch in enumerate(s):
        if st and (ch == 'B' and s[st[-1]] == 'A' or ch == 'D' and s[st[-1]] == 'C'):
            pair[k] = st.pop()
        else:
            st.append(k)
    return pair


PAIR = _sim(TEXT)


def _state(S):
    c = S.get('c')
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
    c = S.get('c')
    if c is None:
        return '栈 `st` 里放“还没被删掉”的字母，从左往右一个个处理'
    ln = S['_line']
    st = S['st']
    if ln == 4:
        return f'读到 `{c}`；栈顶 `{st[-1] if st else "（空）"}`'
    if ln == 5:
        if not st:
            return '栈是空的 → 没有能配对的字母'
        pair = f'{st[-1]}{c}'
        ok = pair in ('AB', 'CD')
        return f'栈顶 + 当前 = `{pair}` → ' + ('==能删==' if ok else '不是 AB / CD，不能删')
    if ln == 6:
        return f'`{B["st"][-1]}{c}` 一起删掉，栈里只剩 `{"".join(st) or "空"}`'
    if ln == 8:
        return f'`{c}` 入栈，栈里 `{"".join(st)}`'
    return f'栈里还剩 `{"".join(st) or "空"}`，共 ==`{len(st)}`== 个字母'


CONFIG = dict(
    num=2696, title='删除子串后的字符串最小长度', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 邻项消除（AB 当 () ，CD 当 {}）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1282'],
    code='''
class Solution:
    def minLength(self, s: str) -> int:
        st = []
        for c in s:
            if st and (c == 'B' and st[-1] == 'A' or c == 'D' and st[-1] == 'C'):
                st.pop()
            else:
                st.append(c)
        return len(st)
''',
    setup=SETUP,
    call=f'Solution().minLength(_Str("{TEXT}"))',
    expect=2,
    views=[
        dict(type='text', fn=_msg, size=28, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前字母，绿 = 还在栈里，红 = 正被删掉，灰 = 已删）', cell=84,
             pointers={'c.i': 'blue'}, pointer_labels={'c.i': 'c'}, color=_color, dim=_dim, h=190),
        dict(type='stack', var='st', label='st（还没被删掉的字母）', fmt=lambda x: str(x), font=34, h=130),
    ],
    watch=[('c', 'c', 'blue'), ('栈顶', 'st[-1] if st else None', 'purple'), ('len(st)', 'len(st)', 'green')],
    captions={
        'st = []': '`st` 是栈，装着遍历过、==还没被删掉==的字母',
        'for c in s': lambda S, B, ret: (f'读入第 `{S.c.i}` 个字母 `c = {S.c}`' if 'c' not in B or B.c.i != S.c.i
                                         else '字母都读完了，栈里剩下的就是删不掉的'),
        'if st and': lambda S, B, ret: (
            f'栈是空的，没有能配对的栈顶 → `{S.c}` 只能入栈' if not S.st else
            (f'`c = {S.c}`，栈顶 `{S.st[-1]}`：==`{S.st[-1]}{S.c}` 配成一对== → 可以删'
             if (S.c == 'B' and S.st[-1] == 'A' or S.c == 'D' and S.st[-1] == 'C')
             else f'`c = {S.c}`，栈顶 `{S.st[-1]}`：`{S.st[-1]}{S.c}` 不是 AB 也不是 CD → 不能删，入栈')),
        'st.pop()': lambda S, B, ret: (f'弹出栈顶 `{B.st[-1]}`，`{S.c}` 也不入栈 → 这一对一起删掉。'
                                       + (f'新栈顶是 `{S.st[-1]}`，后面的字母要和它比' if S.st else '栈空了，后面的字母重新开始')),
        'st.append(c)': '无法配对，`{c}` 入栈，等后面的字母来配 → 栈 `{"".join(st)}`',
        'return len(st)': '栈里剩下 `{"".join(st) or "空"}`，长度 =={len(st)}==',
    },
    cards=dict(
        one_liner='把 AB、CD 看成括号：用栈把能配对的邻项消掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `s` 只含大写字母，每步可以删掉任意一个子串 `"AB"` 或 `"CD"`',
                 '删完后断开的两边会接上，可能又出现新的 AB / CD，求最短能删到多长',
                 '示例：`"ABFCACDB"` → `2`（剩下 `FC`）；`"ACBBD"` → `5`（一步也删不了）'],
        quote='用栈记录遍历过的，没有删除的字母。如果当前字母是 B，且栈顶为 A，那么这两个字母都可以删除。同理，如果当前字母是 D，且栈顶为 C，那么这两个字母都可以删除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['本题和第 20 题“有效的括号”一样：`AB` 当成 `()`，`CD` 当成 `{}`',
              '`B` 碰到栈顶 `A`、`D` 碰到栈顶 `C` 就一起消掉，否则入栈',
              '删掉一对后，原来不相邻的字母变相邻 —— 栈顶正好就是它的新左邻居'],
        result='栈里剩 `FC`，长度 `2` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`；每个字母最多入栈、出栈各一次',
                 '暴力做法：`while "AB" in s or "CD" in s: s = s.replace(...)`，最坏 `O(n^2)`（如 AAA...BBB）',
                 '易错：只有 `A→B`、`C→D` 这个顺序能删；`BA`、`DC`、`AD` 都不行',
                 '易错：栈空时没有 `st[-1]`，要先写 `st and ...`',
                 '同类题：第 1047 题（相邻重复项）、第 3561 题，见题单 §3.3 邻项消除'],
    ),
)

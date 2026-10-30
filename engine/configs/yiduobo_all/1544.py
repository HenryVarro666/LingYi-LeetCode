# 输入字符串用 _Str 包一层：遍历时每个字符带上自己的下标 .i，视图靠它画“当前读到哪”和“哪些还在栈里”
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
TEXT = "abBAcCd"


def _sim(s):
    """复现算法，得到 {下标: 与它一起被消掉的栈顶下标}（只用于画图）"""
    st, pair = [], {}
    for k, ch in enumerate(s):
        if st and abs(ord(s[st[-1]]) - ord(ch)) == 32:
            pair[k] = st.pop()
        else:
            st.append(k)
    return pair


PAIR = _sim(TEXT)


def _state(S):
    c = S.get('char')
    if c is None:
        return None
    ln = S['_line']
    cur = c.i
    kept = {x.i for x in S['stack']}
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
    if ln >= 10:
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
    return i < cur or ln >= 10


def _diff(top, c):
    return f"`|ord('{top}') − ord('{c}')| = |{ord(top)} − {ord(c)}|` = {abs(ord(top) - ord(c))}"


def _msg(S, B):
    c = S.get('char')
    if c is None:
        return '栈 `stack` 存当前剩下的字符；大小写配对 ↔ ASCII 码差 32'
    ln = S['_line']
    st = S['stack']
    if ln == 4:
        return f'扫到 `{c}`；栈顶 `{st[-1] if st else "（空）"}`'
    if ln == 5:
        if not st:
            return '栈是空的，没有可配对的字符'
        d = abs(ord(st[-1]) - ord(c))
        return _diff(st[-1], c) + (' → ==配对==' if d == 32 else ' → 不配对')
    if ln == 6:
        return f'`{B["stack"][-1]}{c}` 配对消去，栈里剩 `{"".join(st) or "空"}`'
    if ln == 8:
        return f'`{c}` 压入栈，栈里 `{"".join(st)}`'
    return f'栈里 `{"".join(st)}` 就是整理好的字符串'


CONFIG = dict(
    num=1544, title='整理字符串', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='栈 · 括号匹配（ASCII 差 32 配对）',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def makeGood(self, s):
        stack = []
        for char in s:
            if stack and abs(ord(stack[-1]) - ord(char)) == 32:
                stack.pop()
            else:
                stack.append(char)

        return ''.join(stack)
''',
    setup=SETUP,
    call=f'Solution().makeGood(_Str("{TEXT}"))',
    expect='d',
    views=[
        dict(type='text', fn=_msg, size=26, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿 = 还在栈里，红 = 正被消去，灰 = 已消去）', cell=84,
             pointers={'char.i': 'blue'}, pointer_labels={'char.i': 'char'}, color=_color, dim=_dim, h=190),
        dict(type='stack', var='stack', label='stack（当前剩下的字符）', fmt=lambda x: str(x), font=34, h=130),
    ],
    watch=[('char', 'char', 'blue'), ('栈顶', 'stack[-1] if stack else None', 'purple'), ('len(stack)', 'len(stack)', 'green')],
    captions={
        'stack = []': '把它当成括号匹配：`stack` 维护当前==剩下==的字符',
        'for char in s': lambda S, B, ret: (f'一趟扫描，第 `{S.char.i}` 个字符 `char = {S.char}`'
                                            if 'char' not in B or B.char.i != S.char.i else '扫描完成'),
        'if stack and': lambda S, B, ret: (
            f'栈是空的，没有可配对的字符 → `{S.char}` 压入栈' if not S.stack else
            (_diff(S.stack[-1], S.char) + ' → ==同一个字母的大小写，配对=='
             if abs(ord(S.stack[-1]) - ord(S.char)) == 32
             else _diff(S.stack[-1], S.char) + ' ≠ 32 → 不配对，压入栈')),
        'stack.pop()': lambda S, B, ret: (f'弹出栈顶 `{B.stack[-1]}`，`{S.char}` 也不入栈：这一对一起消去。'
                                          + (f'新栈顶 `{S.stack[-1]}` 接着和后面的字符比' if S.stack else '栈空了')),
        'stack.append(char)': '`{char}` 压入栈 → 栈 `{"".join(stack)}`',
        "return ''.join": '栈中剩下的字符即答案：`{ret}`',
    },
    cards=dict(
        one_liner='相邻的“大小写同一字母”配对消去 → 括号匹配 → 栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 由大小写字母组成；相邻两个字符是==同一个字母的大小写==（如 `e` 和 `E`）就不合格',
                 '每次删掉一对这样的相邻字符，直到字符串整理好（空串也算），返回结果',
                 '示例：`"leEeetcode"` → `"leetcode"`；`"abBAcC"` → `""`',
                 '本视频用 `"abBAcCd"` → `"d"`'],
        quote='题目要求将相邻的特定字符对消去，可以视为某种特殊的括号匹配问题，那么可以一趟扫描，使用一个栈来维护当前剩下的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['配对的两个字符是同一个字母的大、小写：大写 `65–90`，小写 `97–122`，==正好差 32==',
              '当前字符和栈顶配对 → 弹出栈顶（相当于括号匹配成功）',
              '不配对 → 压入栈；扫完后栈里剩下的就是整理好的字符串'],
        result='栈里剩 `d`，返回 `"d"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '判断条件是 `abs(ord(a) - ord(b)) == 32`：用 `abs` 就不用管谁大谁小',
                 '易错：只看“字母相同”不行，`aa` 不能删，必须一大一小',
                 '消去一对后两边会接上（`abBA` 里 `bB` 消去后 `a`、`A` 相邻），栈顶正好处理这种情况',
                 '最后要用 `\'\'.join(stack)` 把栈转成字符串'],
    ),
)

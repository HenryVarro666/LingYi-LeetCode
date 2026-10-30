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
TEXT = "AACDBBF"


def _sim(s):
    """复现算法，得到 {下标: 与它一起被消掉的栈内下标}（只用于画图）"""
    st, pair = [], {}
    for k, ch in enumerate(s):
        st.append(k)
        if len(st) >= 2 and (s[st[-1]] == 'D' and s[st[-2]] == 'C' or s[st[-1]] == 'B' and s[st[-2]] == 'A'):
            st.pop()
            pair[k] = st.pop()
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
    if cur in PAIR and ln in (6, 7, 8) and (ln != 6 or (len(S['stack']) >= 2 and S['stack'][-1].i == cur)):
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
        return 'blue' if ln == 4 else ('green' if i in kept else 'blue')
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


def _msg(S, B):
    c = S.get('char')
    if c is None:
        return '用栈 `stack` 存当前留下来的字符'
    st = S['stack']
    ln = S['_line']
    if ln == 4:
        return f'读到第 `{c.i}` 个字符 `{c}`'
    if ln == 5:
        return f'`{c}` 先压入栈，栈里 `{"".join(st)}`'
    if ln == 6:
        if len(st) < 2:
            return f'栈里 `{"".join(st) or "空"}` 不足两个，不用检测'
        pair = st[-2] + st[-1]
        return f'栈顶两个 = `{pair}` → ' + ('==是 AB / CD==，弹出' if pair in ('AB', 'CD') else '不是 AB / CD，不弹')
    if ln in (7, 8):
        return f'弹出一个，栈里 `{"".join(st) or "空"}`'
    return f'栈里剩 `{"".join(st) or "空"}`，长度 ==`{len(st)}`=='


def _cap_while(S, B, ret):
    st, c = S.stack, S.char
    again = (not st) or st[-1].i != c.i      # 栈顶不是刚压入的 char → 是弹出之后的再次检测
    head = '弹出之后再检测一次：' if again else ''
    if len(st) < 2:
        return head + (f'栈里只有 {len(st)} 个字符，不够两个' if st else '栈空了，不够两个') + ' → 结束检测，读下一个'
    pair = st[-2] + st[-1]
    if pair in ('AB', 'CD'):
        return head + f'栈顶两个是 `{pair}` → ==正好是 AB / CD==，弹出这两个'
    return head + f'栈顶两个是 `{pair}`，不是 AB 也不是 CD → 结束检测，读下一个'


CONFIG = dict(
    num=2696, title='删除子串后的字符串最小长度', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='栈 · 先入栈再检查栈顶两个',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1282'],
    code='''
class Solution(object):
    def minLength(self, s):
        stack = []
        for char in s:
            stack.append(char)
            while len(stack) >= 2 and ((stack[-1] == 'D' and stack[-2] == 'C') or (stack[-1] == 'B' and stack[-2] == 'A')):
                stack.pop()
                stack.pop()

        return len(stack)
''',
    setup=SETUP,
    call=f'Solution().minLength(_Str("{TEXT}"))',
    expect=1,
    views=[
        dict(type='text', fn=_msg, size=28, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿 = 还在栈里，红 = 正被弹出，灰 = 已删）', cell=84,
             pointers={'char.i': 'blue'}, pointer_labels={'char.i': 'char'}, color=_color, dim=_dim, h=190),
        dict(type='stack', var='stack', label='stack（当前留下来的字符）', fmt=lambda x: str(x), font=34, h=130),
    ],
    watch=[('char', 'char', 'blue'), ('栈顶', 'stack[-1] if stack else None', 'purple'), ('len(stack)', 'len(stack)', 'green')],
    captions={
        'stack = []': '`stack` 存放当前==留下来==的字符',
        'for char in s': lambda S, B, ret: (f'读入第 `{S.char.i}` 个字符 `char = {S.char}`'
                                            if 'char' not in B or B.char.i != S.char.i else '字符都读完了，栈里剩下的就是答案'),
        'stack.append(char)': '不管能不能配对，先把 `{char}` 压入栈 → 栈 `{"".join(stack)}`',
        'while len(stack)': _cap_while,
        7: '`{B.stack[-2]}{B.stack[-1]}` 是一对：连弹两次，先弹出栈顶 `{B.stack[-1]}`',
        8: lambda S, B, ret: (f'再弹出 `{B.stack[-1]}`，这一对都删掉了 → 栈 `{"".join(S.stack) or "空"}`。'
                              + (f'栈顶回到 `{S.stack[-1]}`，弹完要再检测一次' if S.stack else '栈空了，弹完还是要再检测一次')),
        'return len(stack)': '栈里剩下 `{"".join(stack)}`，长度 =={len(stack)}==',
    },
    cards=dict(
        one_liner='先压栈，再看栈顶两个能不能凑成 AB / CD',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `s` 只含大写字母，可以反复删掉子串 `"AB"` 或 `"CD"`',
                 '删掉后两边会接上，可能产生新的 AB / CD，问最后最短剩多长',
                 '示例：`"ABFCACDB"` → `2`；`"ACBBD"` → `5`',
                 '本视频用 `"AACDBBF"` → `1`（剩下 `F`）'],
        quote='一趟遍历，将字符串中的字符逐个加入到栈中，每次加入后检测当前栈顶的两个元素是否为AB或者CD，若是，则将这两个字符弹出然后再次检测。',
        quote_src='—— yiduobo 题解原文',
        idea=['为什么要用栈？样例一里删掉 `CD` 后冒出第二组 `AB`，==要把之前的字符存起来=='
              '，删完才能接着往回看',
              '每读一个字符就==先入栈==，再检测栈顶两个是不是 AB 或 CD，是就连弹两次',
              '栈里本来没有相邻的 AB / CD，所以弹完一对后，栈顶两个还是合法的，不会连环出新的一对'],
        result='栈里剩 `F`，长度 `1` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`while` 实际最多执行一次：压入前栈里就没有相邻的 AB / CD，弹出一对后剩下的部分仍然干净',
                 '易错：检测时要看栈顶两个 `stack[-2]`、`stack[-1]`，而且 `A` 在前、`B` 在后',
                 '易错：`len(stack) >= 2` 要写在前面，否则栈里只有一个字符时会越界',
                 '对比灵神：灵神先看栈顶再决定入不入栈，这里是先入栈再检测，结果一样'],
    ),
)

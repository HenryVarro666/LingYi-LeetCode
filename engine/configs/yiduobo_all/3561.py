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
TEXT = "xzcdab"


def _sim(s):
    """复现算法，得到 {下标: 与它一起被消掉的栈顶下标}（只用于画图）"""
    st, pair = [], {}
    for k, ch in enumerate(s):
        if st and abs(ord(ch) - ord(s[st[-1]])) in (1, 25):
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


def _diff(c, top):
    return f"`|ord('{c}') − ord('{top}')| = |{ord(c)} − {ord(top)}|` = {abs(ord(c) - ord(top))}"


def _msg(S, B):
    c = S.get('char')
    if c is None:
        return '栈 `stack` 存处理完的字符串，栈顶是它的最后一个字符'
    ln = S['_line']
    st = S['stack']
    if ln == 4:
        return f'扫到 `{c}`；处理完的字符串 `{"".join(st) or "（空）"}`'
    if ln == 5:
        if not st:
            return '栈是空的，没有最后一个字符可比'
        d = abs(ord(c) - ord(st[-1]))
        return _diff(c, st[-1]) + (' → ==连续，消除==' if d in (1, 25) else ' → 不连续')
    if ln == 6:
        return f'`{B["stack"][-1]}{c}` 连续，删去最后一个字符；剩 `{"".join(st) or "空"}`'
    if ln == 8:
        return f'`{c}` 加到末尾，处理完的字符串 `{"".join(st)}`'
    return f'处理完的字符串 `{"".join(st)}` 就是答案'


def _cap_if(S, B, ret):
    if not S.stack:
        return f'栈是空的，没有最后一个字符可比 → `{S.char}` 加入栈'
    d = abs(ord(S.char) - ord(S.stack[-1]))
    head = _diff(S.char, S.stack[-1])
    if d == 1:
        return head + ' → ==等于 1，字母表里相邻==，消除'
    if d == 25:
        return head + ' → ==等于 25，a 和 z 首尾相接==，也算连续，消除'
    return head + ' → 既不是 1 也不是 25，不连续，加入栈'


CONFIG = dict(
    num=3561, title='移除相邻字符', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 后进先出地消除连续字符',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1397'],
    code='''
class Solution(object):
    def resultingString(self, s):
        stack = []
        for char in s:
            if stack and (abs(ord(char) - ord(stack[-1])) == 1 or abs(ord(char) - ord(stack[-1])) == 25):
                stack.pop()
            else:
                stack.append(char)

        return ''.join(stack)
''',
    setup=SETUP,
    call=f'Solution().resultingString(_Str("{TEXT}"))',
    expect='xb',
    views=[
        dict(type='text', fn=_msg, size=26, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿 = 还在栈里，红 = 正被消除，灰 = 已消除）', cell=84,
             pointers={'char.i': 'blue'}, pointer_labels={'char.i': 'char'}, color=_color, dim=_dim, h=190),
        dict(type='stack', var='stack', label='stack（处理完的字符串）', fmt=lambda x: str(x), font=34, h=130),
    ],
    watch=[('char', 'char', 'blue'), ('栈顶', 'stack[-1] if stack else None', 'purple'), ('len(stack)', 'len(stack)', 'green')],
    captions={
        'stack = []': '`stack` 存放==已经处理完==的字符串，栈顶就是它的最后一个字符',
        'for char in s': lambda S, B, ret: (f'一趟遍历，第 `{S.char.i}` 个字符 `char = {S.char}`'
                                            if 'char' not in B or B.char.i != S.char.i else '遍历完成'),
        'if stack and': _cap_if,
        'stack.pop()': lambda S, B, ret: (f'连续就消除：把处理完的字符串的最后一个 `{B.stack[-1]}` 删去，`{S.char}` 也不加入。'
                                          + (f'现在最后一个字符是 `{S.stack[-1]}`' if S.stack else '栈空了')),
        'stack.append(char)': lambda S, B, ret: (('不连续，' if B.stack else '') +
                                                 f'把 `{S.char}` 加到末尾 → 栈 `{"".join(S.stack)}`'),
        "return ''.join": '栈中字符形成的字符串即答案：`{ret}`',
    },
    cards=dict(
        one_liner='和已处理字符串的最后一个比：连续就删，不连续就追加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['小写字母串 `s`，只要有两个相邻字符在字母表里==连续==（正序、逆序都行，`a` 和 `z` 也算），就移除==最左边==的一对',
                 '剩下的字符向左靠拢，重复直到不能再移除，返回最终字符串',
                 '示例：`"abc"` → `"c"`；`"adcb"` → `""`；`"zadb"` → `"db"`',
                 '本视频用 `"xzcdab"` → `"xb"`'],
        quote='可以发现这是一个后进先出的场景，于是可以使用一个栈来储存处理完的字符串，然后对于当前字符，将其与栈顶字符进行比较，若连续，则弹出栈顶字符，否则将当前字符加入到栈中。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：当前字符先和==已处理字符串的最后一个字符==比，连续就把那个字符删掉',
              '“只和最后一个比、删的也是最后一个”→ 后进先出 → 栈',
              '连续 = ASCII 码差 `1`，或差 `25`（`a` 和 `z` 首尾相接）'],
        result='栈里剩 `x`、`b`，返回 `"xb"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '连续的判断写了两遍 `abs(ord(char) - ord(stack[-1]))`，分别比较 `1` 和 `25`',
                 '易错：别漏掉差 `25`；相同字母（差 `0`）不算连续',
                 '示例里 `cd` 消去后 `z` 和 `a` 变成相邻，又能消去 —— 栈顶自动处理了这种连锁',
                 '对比灵神：灵神把判断封装成 `is_consecutive`，逻辑完全一样'],
    ),
)

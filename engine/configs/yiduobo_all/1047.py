# 输入字符串用 _Str 包一层：遍历时每个字符带上自己的下标 .i，视图靠它画“当前读到哪”和“哪些幸存”
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
TEXT = "azxxzy"


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


def _msg(S, B):
    c = S.get('char')
    if c is None:
        return '栈 `stack` 存当前“幸存”的字符'
    ln = S['_line']
    st = S['stack']
    if ln == 4:
        return f'扫到 `{c}`；最后一个幸存的字符是 `{st[-1] if st else "（没有）"}`'
    if ln == 5:
        if not st:
            return '栈是空的，没有幸存字符可比'
        return f'栈顶 `{st[-1]}` vs 当前 `{c}` → ' + ('==相同，成对移除==' if st[-1] == c else '不同，压入栈')
    if ln == 6:
        return f'`{c}{c}` 成对移除，幸存字符 `{"".join(st) or "（无）"}`'
    if ln == 8:
        return f'`{c}` 压入栈，幸存字符 `{"".join(st)}`'
    return f'扫描完成，栈里 `{"".join(st)}` 就是答案'


CONFIG = dict(
    num=1047, title='删除字符串中的所有相邻重复项', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='栈 · 维护幸存字符',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1286'],
    code='''
class Solution(object):
    def removeDuplicates(self, S):
        stack = []
        for char in S:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)

        return ''.join(stack)
''',
    setup=SETUP,
    call=f'Solution().removeDuplicates(_Str("{TEXT}"))',
    expect='ay',
    views=[
        dict(type='text', fn=_msg, size=28, h=70),
        dict(type='string', var='S', label='S（蓝 = 当前字符，绿 = 幸存在栈里，红 = 正被移除，灰 = 已移除）', cell=84,
             pointers={'char.i': 'blue'}, pointer_labels={'char.i': 'char'}, color=_color, dim=_dim, h=190),
        dict(type='stack', var='stack', label='stack（当前幸存的字符）', fmt=lambda x: str(x), font=34, h=130),
    ],
    watch=[('char', 'char', 'blue'), ('栈顶', 'stack[-1] if stack else None', 'purple'), ('len(stack)', 'len(stack)', 'green')],
    captions={
        'stack = []': '`stack` 专门存==幸存下来==的字符',
        'for char in S': lambda S, B, ret: (f'从头向后扫描第 `{S.char.i}` 个字符 `char = {S.char}`'
                                            if 'char' not in B or B.char.i != S.char.i else '扫描完成'),
        'if stack and': lambda S, B, ret: (
            f'栈是空的，没有幸存字符可比 → `{S.char}` 压入栈' if not S.stack else
            (f'栈顶 `{S.stack[-1]}` 与 `char = {S.char}` 相同 → ==成对移除=='
             if S.stack[-1] == S.char else f'栈顶 `{S.stack[-1]}` 与 `char = {S.char}` 不同 → 压入栈')),
        'stack.pop()': lambda S, B, ret: (f'弹出栈顶 `{B.stack[-1]}`，`char` 也不入栈：两个相同字符一起移除。'
                                          + (f'下一个字符要和幸存的 `{S.stack[-1]}` 比' if S.stack else '栈空了')),
        'stack.append(char)': '`{char}` 压入栈 → 栈 `{"".join(stack)}`',
        "return ''.join": '栈中的字符就是最终答案：`{ret}`',
    },
    cards=dict(
        one_liner='用栈存幸存字符：和栈顶相同就弹出，不同就压入',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['小写字母串 `S`，每次删除两个==相邻且相同==的字母，反复进行直到不能再删',
                 '返回最终字符串',
                 '示例：`"abbaca"` → `"ca"`；`"azxxzy"` → `"ay"`',
                 '本视频用 `"azxxzy"`：先删 `xx`，`z` 和 `z` 才会碰到一起'],
        quote='对于当前的S[index]，若其与栈顶字符相同，那么就将栈顶字符弹出，否则将S[index]压入栈中。扫描完成后，栈中的字符就是最终的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素想法：扫到 `S[index] == S[index+1]` 就移除这一对',
              '移除后还要拿 index 之前==最后一个幸存的字符==去和后面的字符比，所以得把幸存字符存起来',
              '最后进入的先比较 → 后进先出 → 栈'],
        result='栈里是 `a`、`y`，返回 `"ay"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '栈顶永远是“最后一个幸存的字符”，弹出一对后新的栈顶接着参与比较',
                 '易错：别忘了 `stack and`，栈空时没有 `stack[-1]`',
                 '易错：返回要用 `\'\'.join(stack)` 转成字符串',
                 '对比灵神：灵神先证明“消除顺序不影响结果”，再用栈；这里直接从扫描过程推出要存幸存字符'],
    ),
)

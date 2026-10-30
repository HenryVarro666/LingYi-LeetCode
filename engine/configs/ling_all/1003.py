TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

S0 = 'aabcbc'


def _cur(S):
    k = getattr(S.get('s'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _gone(S):
    """已经被消除的 abc 的下标（只用于画图）"""
    s = S.get('s')
    if s is None:
        return set()
    k = getattr(s, 'k', -1)
    if k == -1:
        return set()
    if k is None:
        k = len(s)
    stk, gone = [], set()          # stk 里每项是 [a 的下标, b 的下标或 None]
    for i in range(k):
        ch = s[i]
        if ch == 'a':
            stk.append([i, None])
        elif ch == 'b' and stk and stk[-1][1] is None:
            stk[-1][1] = i
        elif ch == 'c' and stk and stk[-1][1] is not None:
            a, b = stk.pop()
            gone |= {a, b, i}
        else:
            break
    if k < len(s) and s[k] == 'c' and S.get('_line', 0) >= 5 and stk and stk[-1][1] is not None and len(S['st']) < len(stk):
        gone |= {stk[-1][0], stk[-1][1], k}
    return gone


def _color(S, i, v):
    return 'blue' if i == _cur(S) else None


def _note(S):
    if 'c' not in S:
        return '规则：`a`=97、`b`=98、`c`=99，==相邻两个字符的码差恰好为 1== 才能接上'
    c = S['c']
    st = S.get('st', [])
    top = f"，栈顶 `{chr(st[-1])}`" if st else '，栈空'
    return f'当前 `c = {chr(c)}`（{c}）{top}。`a` 入栈；`b` 要接在 `a` 后；`c` 要接在 `b` 后'


def _chk(S, B, ret):
    c = S.c
    ch = chr(c)
    if c == 97:
        return "`c = 'a'`（97）不大于 `ord('a')` → 不用检查，==a 像左括号，直接去入栈=="
    need = chr(c - 1)
    if not B.st:
        return f'`{ch}` 要接在 `{need}` 后面，但栈是空的 → 前面没有可配的字符 → ==无效=='
    top = B.st[-1]
    if c - top == 1:
        what = 'b 接在 a 后面' if c == 98 else 'c 接在栈里的 b（代表 ab）后面，凑成 abc'
        return f'`{ch}` 来了：弹出栈顶 `{chr(top)}`，`{c} − {top} = 1` → =={what}=='
    return f'`{ch}` 来了：弹出栈顶 `{chr(top)}`，`{c} − {top} = {c - top} ≠ 1` → 配不上 → ==返回 False=='


def _lt(S, B, ret):
    c = S.c
    if c == 97:
        return '`a` 小于 `c` → 要入栈（等后面的 b）'
    if c == 98:
        return '`b` 小于 `c` → 要入栈：刚弹出的 a 换成 b，==栈里的 b 代表 ab==，等一个 c'
    return '`c` 不小于 `c` → ==不入栈==：刚弹出的 b 就是 `ab`，加上 c 正好消掉一个 `abc`'


CONFIG = dict(
    num=1003, title='检查替换后的词是否有效', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 邻项消除（abc 类比括号）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1427'],
    code='''
class Solution:
    def isValid(self, s: str) -> bool:
        st = []
        for c in map(ord, s):
            if c > ord('a') and (len(st) == 0 or c - st.pop() != 1):
                return False
            if c < ord('c'):
                st.append(c)
        return len(st) == 0
''',
    setup=TRACK,
    call=f'Solution().isValid(Tracked({S0!r}))',
    expect=True,
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（灰色 = 已经消掉的 abc）', h=190, cell=100,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'c'},
             dim=lambda S, i, v: i in _gone(S), color=_color),
        dict(type='stack', var='st', label='st（栈里存 ASCII 码，这里显示成字母；栈顶在右）', h=150, font=34,
             fmt=lambda x: chr(x)),
        dict(type='text', fn=_note, size=28, h=110),
    ],
    watch=[('c', 'chr(c)', 'blue'), ('ord', 'c', 'cyan'), ('st', "''.join(map(chr, st))", 'green'), ('len(st)', 'len(st)', 'purple')],
    captions={
        'st = []': '像括号匹配一样用栈：==a 当左括号==，b、c 逐步和它配成 abc',
        'for c in map(ord, s)': lambda S, B, ret: (f"取 `s[{S.s.k}] = '{chr(S.c)}'`，转成 ASCII 码 `{S.c}`"
                                                 if getattr(S.s, 'k', None) is not None else '`s` 遍历完毕，循环结束'),
        "if c > ord('a')": _chk,
        'return False': '无效，直接返回 ==False==',
        "if c < ord('c')": _lt,
        'st.append(c)': lambda S, B, ret: ("`a` 入栈：栈 = `" + ''.join(map(chr, S.st)) + "`" if S.c == 97
                                           else "`b` 入栈：栈顶由 a 变成 b → 栈 = `" + ''.join(map(chr, S.st)) + "`"),
        'return len(st) == 0': '遍历结束，栈为空 → 每个字符都被消掉了 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='把 abc 当成一对括号：a 入栈，b、c 逐步把它消掉，栈空才有效',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`t` 从空串开始，每次可在任意位置插入 `"abc"`，问能否得到 `s`',
                 '示例：`"aabcbc"` → `true`（`abc` 里再插一个 `abc`）',
                 '示例：`"abccba"` → `false`'],
        quote='如果把问题改成「将字符串 `()` 插入到 t 中的任意位置」，比如 `() -> (()) -> (()())`，是不是很眼熟？',
        quote_src='—— 灵茶山艾府题解',
        idea=['和有效的括号同一类题：逆着插入操作去==邻项消除==，用栈',
              '`a` 直接入栈；`b` 要接在栈顶 `a` 上，把栈顶改成 `b`；`c` 要接在 `b` 上，弹出栈顶',
              '`b`、`c` 合并成一个判断：`c - st.pop() != 1`，`a`、`b` 合并成一个入栈：`c < ord(\'c\')`'],
        result='栈空 → `aabcbc` 是有效字符串，返回 `True` ✓',
        summary=['时间 `O(n)`；空间 `O(n)`，若能直接改字符串可做到 `O(1)`',
                 '`c > ord(\'a\') and (...)` 短路：`len(st) == 0` 写在前面，空栈不会被 `pop`',
                 '易错：`b` 要先弹出 `a` 再入栈，不能忘了 `c < ord(\'c\')` 这一句',
                 '易错：结束时栈非空（还有没配成的 `a`、`ab`）也无效'],
    ),
)

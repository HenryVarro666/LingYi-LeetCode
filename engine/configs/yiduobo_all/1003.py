TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

S0 = 'ababcc'


def _cur(S):
    k = getattr(S.get('s'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _gone(S):
    """已经凑成 abc 并弹出的字符下标（只用于画图）"""
    s = S.get('s')
    if s is None:
        return set()
    k = getattr(s, 'k', -1)
    if k == -1:
        return set()
    if k is None:
        k = len(s)
    stk, gone = [], set()
    for i in range(k):
        if s[i] == 'c':
            if len(stk) < 2:
                break
            gone |= {i, stk.pop(), stk.pop()}
        else:
            stk.append(i)
    if k < len(s) and s[k] == 'c' and S.get('_line', 0) >= 20 and len(stk) >= 2:
        gone |= {k, stk[-1], stk[-2]}
    return gone


def _rule(S):
    st = S.get('stack')
    if st is None:
        return '用栈做括号匹配：三种字符，==栈顶是什么，决定下一个字符能不能来=='
    if S.get('_line') == 26:
        return '扫描结束：栈里什么都不剩 → 所有字符都凑成了 ==abc=='
    if not st:
        return '栈空 → 下一个字符只能是 ==a==（合法串必须从 a 起头）'
    t = st[-1]
    if t == 'a':
        return '栈顶 `a` → 下一个可以是 ==a== 或 ==b==（压栈）；==c== 不行'
    return '栈顶 `b` → ==c== 弹出栈顶两个（凑成 abc）；==a== 压栈；==b== 不行'


def _top(S, B):
    st = B.stack
    return st[-1] if st else None


def _if_c(S, B, ret):
    t = B.stack[-1]
    if t == 'a':
        return f"栈顶是 `a`：`char = {S.char}`" + ('，是 c → ==a 后面不能直接接 c==' if S.char == 'c' else '，不是 c → 可以压栈')
    return f"栈顶是 `b`：`char = {S.char}`" + ('，是 c → 栈顶 b，它下面必是 a → ==凑成 abc==' if S.char == 'c' else '，不是 c → 再看是不是 a')


def _push(S, B, ret):
    t = B.stack[-1] if B.stack else None
    s = ''.join(S.stack)
    if t is None:
        return f'栈空，来的是 `a` → 压入，栈 = `{s}`'
    if t == 'a':
        return (f'栈顶 a，又来 `a` → 压入（如 aabcbc 的前两个 a），栈 = `{s}`' if S.char == 'a'
                else f'栈顶 a，来 `b` → 压入，`ab` 先放着等 c，栈 = `{s}`')
    return f'栈顶 b，来 `a` → 压入（如 ababcc 的第 2 个 a），栈 = `{s}`'


def _pop(S, B, ret):
    if S['_line'] == 19:
        return f'弹出栈顶 `{B.stack[-1]}`，栈 = `{"".join(S.stack)}`'
    return fXX


def _ret_false(S, B, ret):
    st = B.stack
    if not st:
        return f'栈空但来的是 `{S.char}` → 不是 a 起头 → ==返回 False=='
    if st[-1] == 'a':
        return '栈顶 a 后面来了 c → ==返回 False=='
    return '栈顶 b 后面又来 b → ==返回 False=='


CONFIG = dict(
    num=1003, title='检查替换后的词是否有效', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='栈 · 按栈顶分情况讨论',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1427'],
    code='''
class Solution(object):
    def isValid(self, s):

        stack = []
        for char in s:
            if not stack:
                if char != 'a':
                    return False
                else:
                    stack.append(char)
            else:
                if stack[-1] == 'a':
                    if char == 'c':
                        return False
                    else:
                        stack.append(char)
                elif stack[-1] == 'b':
                    if char == 'c':
                        stack.pop()
                        stack.pop()
                    elif char == 'a':
                        stack.append(char)
                    else:
                        return False
        
        return not stack
''',
    setup=TRACK,
    call=f'Solution().isValid(Tracked({S0!r}))',
    expect=True,
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（灰色 = 已经凑成 abc 弹出的字符）', h=190, cell=100,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'char'},
             dim=lambda S, i, v: i in _gone(S), color=lambda S, i, v: 'blue' if i == _cur(S) else None),
        dict(type='stack', var='stack', label='stack（栈顶在右）', h=150, font=34),
        dict(type='text', fn=_rule, size=28, h=110),
    ],
    watch=[('char', 'char', 'blue'), ('stack', 'stack', 'green'), ('len(stack)', 'len(stack)', 'purple')],
    captions={
        'stack = []': '栈里放“还没凑成 abc 的字符”，从空栈开始',
        'for char in s': lambda S, B, ret: (f"从左到右扫描：`s[{S.s.k}] = '{S.char}'`"
                                          if getattr(S.s, 'k', None) is not None else '`s` 扫描完毕'),
        'if not stack': lambda S, B, ret: ('栈为空 → 合法的子串必须是 a 起头，只有 `a` 能进来' if not S.stack
                                           else f'栈不空 → 看栈顶 `{S.stack[-1]}` 是 a 还是 b'),
        'if char != ': lambda S, B, ret: (f'`char = {S.char}` 不是 `a` → 空栈来了 b 或 c，非法' if S.char != 'a'
                                          else '`char = a` → 可以起头，走 else 压栈'),
        'return False': _ret_false,
        "if stack[-1] == 'a'": lambda S, B, ret: (f'栈顶 `{S.stack[-1]}`：' + ('是 a → 先看 a 的后继' if S.stack[-1] == 'a'
                                                   else '不是 a → 往下走 elif 分支')),
        "if char == 'c'": _if_c,
        "elif stack[-1] == 'b'": '栈顶不是 a，那就是 `b`：它的下一个字符要分 a、b、c 三种情况',
        'stack.pop()': _pop,
        "elif char == 'a'": lambda S, B, ret: (f'`char = {S.char}`' + ('，是 a → b 后面可以新开一个 a' if S.char == 'a'
                                                                   else '，不是 a → 只剩 b：b 后再来 b 非法')),
        'stack.append(char)': _push,
        'return not stack': '扫描完，栈空 → 每个 a 都配上了 bc → 返回 =={ret}==；栈里还剩东西就是 False',
    },
    cards=dict(
        one_liner='括号匹配的变形：看栈顶是 a 还是 b，决定下一个字符能不能来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['空串开始，每次在任意位置插入 `"abc"`，问能否得到 `s`',
                 '示例：`"aabcbc"` → `true`，`"abccba"` → `false`',
                 '本视频：`"ababcc"` → `true`（`ab` 后又来 `a`，再来两个 `c`）'],
        quote='若当前字符为c，那么根据上面的结论，栈顶元素为b，合法情况下栈顶的下一个元素必然是a，那么此时出现了一组abc，于是此时应该将栈顶以及栈顶的下一个元素弹出',
        quote_src='—— yiduobo 题解原文',
        idea=['先回顾括号匹配：左括号入栈，右括号和栈顶配对。这里有三种字符，不能只靠计数',
              '栈空：只有 `a` 能进；栈顶 `a`：来 `a`、`b` 压栈，来 `c` 非法',
              '栈顶 `b`：来 `c` 弹两个，来 `a` 压栈，来 `b` 非法；最后栈空才有效'],
        result='栈空 → `ababcc` 是有效字符串，返回 `True` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '栈里 `a`、`b` 是分开存的：`c` 来时要连弹 ==两次==（b 再 a）',
                 '易错：栈顶 `a` 后面可以接 `a` 或 `b`，但不能直接接 `c`',
                 '易错：遍历完栈里还有 `a`（或 `ab`）就是无效，要写 `return not stack`',
                 '对比灵神：他把 `b` 改写成栈顶、用 `c - st.pop() != 1` 压成两个判断；这里是逐种情况写出'],
    ),
)

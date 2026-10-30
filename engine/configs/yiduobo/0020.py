TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

PAIR = {')': '(', ']': '[', '}': '{'}


def _gone(S):
    """已经配对成功的括号下标（只用于画图）"""
    s = S.get('s')
    if s is None:
        return set()
    k = getattr(s, 'k', -1)
    if k == -1:
        return set()
    if k is None:
        k = len(s)
    stack, gone = [], set()
    for i in range(k):
        ch = s[i]
        if ch not in PAIR:
            stack.append(i)
        elif stack and s[stack[-1]] == PAIR[ch]:
            gone |= {stack.pop(), i}
    st = S.get('stack')
    if k < len(s) and s[k] in PAIR and st is not None and len(st) < len(stack) and s[stack[-1]] == PAIR[s[k]]:
        gone |= {stack.pop(), k}
    return gone


def _bad(S):
    """当前右括号弹出了不同类型的左括号 → 标红"""
    s = S.get('s')
    k = getattr(s, 'k', None)
    st = S.get('stack')
    if not isinstance(k, int) or k < 0 or s[k] not in PAIR or st is None:
        return None
    exp = sum(1 if ch not in PAIR else -1 for ch in s[:k])
    return k if len(st) < exp and k not in _gone(S) else None


def _cur(S):
    s = S.get('s')
    k = getattr(s, 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _pair_cap(close, open_):
    def f(S, B, ret):
        if S.char != close:
            return f'`{S.char}` 不是 `{close}` → `and` 短路，==不会弹栈==，接着看下一个分支'
        top = B.stack[-1]
        if top == open_:
            return f'`{close}` 弹出栈顶 `{top}`：同类型 → ==配对成功==，这对括号“脱单”'
        return f'`{close}` 弹出栈顶 `{top}`，但它需要 `{open_}` → ==类型不匹配==，不合法'
    return f


CONFIG = dict(
    num=20, title='有效的括号', difficulty='Easy', category='栈',
    author='yiduobo', technique='栈 · 括号匹配',
    code='''
class Solution(object):
    def isValid(self, s):
        stack = []
        for char in s:
            if char in ['(', '[', '{']:
                stack.append(char)
            elif not stack:
                return False
            elif char == ')' and stack.pop() != '(':
                return False
            elif char == ']' and stack.pop() != '[':
                return False
            elif char == '}' and stack.pop() != '{':
                return False

        return not stack
''',
    setup=TRACK,
    call='Solution().isValid(Tracked("{[]}([)]"))',
    expect=False,
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（灰色 = 已配对，红色 = 冲突）', h=200, cell=100,
             pointers={_cur: 'cyan'}, pointer_labels={_cur: 'char'},
             dim=lambda S, i, v: i in _gone(S),
             color=lambda S, i, v: 'red' if i == _bad(S) else None),
        dict(type='stack', var='stack', label='stack（单身的左括号）', h=130),
        dict(type='text', fn=lambda S: '左括号 → 压栈；右括号 → 栈空 或 栈顶==不同类== 就不合法，否则弹栈配对', size=26),
    ],
    watch=[('char', 'char', 'cyan'), ('len(stack)', 'len(stack)', 'purple')],
    captions={
        'stack = []': '准备一个栈，存还没配对的左括号',
        'for char in s': lambda S, B, ret: (f'扫描下一个字符 `char = {S.char}`' if getattr(S.s, 'k', None) is not None
                                            else '扫描结束'),
        "if char in ['('": lambda S, B, ret: (f'`{S.char}` 是左括号 → 直接压栈' if S.char in '([{'
                                              else f'`{S.char}` 是右括号 → 要找栈顶的左括号配对'),
        'stack.append(char)': '压入栈顶：stack = `{"".join(stack)}`',
        'elif not stack': lambda S, B, ret: ('栈是空的 → 右括号没人配对，不合法' if not B.stack
                                             else f'栈不空（栈顶 `{B.stack[-1]}`）→ 继续检查类型'),
        "elif char == ')'": _pair_cap(')', '('),
        "elif char == ']'": _pair_cap(']', '['),
        "elif char == '}'": _pair_cap('}', '{'),
        'return False': '返回 ==False==：`)` 想配 `(`，栈顶却是 `[`，括号交叉了',
        'return not stack': '扫描结束：栈里若还有元素，就是“依然单身的左括号” → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='左括号压栈，右括号弹出栈顶配对，类型不同就不合法',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 只含 `()[]{}`，判断是否有效',
                 '有效 = 左括号被==同类型==右括号、按==正确顺序==闭合',
                 '示例：`"()[]{}"` → `true`，`"([)]"` → `false`'],
        quote='对于一个左括号，直接压入栈顶，而对于一个右括号，如果当前栈为空或者栈顶不是左括号，那么就不合法，否则弹出栈顶的左括号来和这个右括号配对。',
        quote_src='—— yiduobo 题解',
        idea=['三种括号：碰到右括号还要判断是不是==同类别==的左括号',
              '例如 `( [ ) ]`：扫到 `)` 时栈顶是 `[`，依然不合法',
              '扫描结束栈里还有元素 → 存在“依然单身的左括号”'],
        result='`)` 碰到栈顶 `[` → 返回 `False` ✓（前半段 `{[]}` 是合法的）',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '每种右括号各写一个 `elif`，`and` 短路保证只有类型对上才弹栈',
                 '易错：先判 `not stack` 再 `pop`；结尾要返回 `not stack`',
                 '原文为 Python 2 写法：仅删去 `"""type"""` 文档字符串，逻辑未改'],
    ),
)

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
    """已经被“消除”的括号下标（只用于画图）"""
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
    st = S.get('st')
    if k < len(s) and s[k] in PAIR and st is not None and len(st) < len(stack):
        gone |= {stack.pop(), k}
    return gone


def _cur(S):
    s = S.get('s')
    k = getattr(s, 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _pop_cap(S, B, ret):
    c = S.c
    if not B.st:
        return f'右括号 `{c}`，但栈是空的 → 没有左括号和它配对'
    top = B.st[-1]
    if top == S.mp[c]:
        return f'右括号 `{c}`：弹出栈顶 `{top}`，正好等于 `mp["{c}"]` → ==消除一对==，栈剩 {len(S.st)} 个'
    return f'右括号 `{c}`：弹出栈顶 `{top}`，但需要 `{S.mp[c]}` → ==类型不匹配=='


CONFIG = dict(
    num=20, title='有效的括号', difficulty='Easy', category='栈',
    author='灵茶山艾府', technique='邻项消除 · 栈',
    code='''
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2:  # s 长度必须是偶数
            return False
        mp = {')': '(', ']': '[', '}': '{'}
        st = []
        for c in s:
            if c not in mp:  # c 是左括号
                st.append(c)  # 入栈
            elif not st or st.pop() != mp[c]:  # c 是右括号
                return False  # 没有左括号，或者左括号类型不对
        return not st  # 所有左括号必须匹配完毕
''',
    setup=TRACK,
    call='Solution().isValid(Tracked("{[()]}"))',
    expect=True,
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（灰色 = 已消除）', h=200, cell=100,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'c'},
             dim=lambda S, i, v: i in _gone(S)),
        dict(type='stack', var='st', label='st 栈（还没配对的左括号）', h=130),
        dict(type='map', var='mp', label='mp：右括号 → 左括号', fmt=lambda k, v: f'{k} → {v}', h=110),
        dict(type='text', fn=lambda S: '消消乐：每次消掉一对==相邻==的匹配括号，能消成空串就有效', size=26),
    ],
    watch=[('c', 'c', 'blue'), ('len(st)', 'len(st)', 'purple')],
    captions={
        'if len(s) % 2': '括号两两一对：`len(s) = {len(s)}` 是偶数 → 还有希望，继续',
        'mp = {': '哈希表存 ==右括号 → 对应的左括号==，省去一大串 if-else',
        'st = []': '创建空栈：存放“还在等右括号”的左括号',
        'for c in s': lambda S, B, ret: (f'取下一个字符 `c = {S.c}`' if getattr(S.s, 'k', None) is not None
                                         else '`s` 遍历完毕，循环结束'),
        'if c not in mp': lambda S, B, ret: (f'`{S.c}` 不在 mp 的键里 → ==是左括号==' if S.c not in S.mp
                                             else f'`{S.c}` 在 mp 的键里 → ==是右括号==，要和栈顶配对'),
        'st.append(c)': '左括号入栈，等后面的右括号来消除它：栈 = `{"".join(st)}`',
        'elif not st': _pop_cap,
        'return not st': '遍历结束，栈为空 → 所有左括号都被消除 → 返回 ==True==',
    },
    cards=dict(
        one_liner='括号消消乐：右括号必须和栈顶的左括号配对消除',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 只含 `()[]{}`，判断是否有效',
                 '有效 = 左括号被==同类型==右括号、按==正确顺序==闭合',
                 '示例：`"([])"` → `true`，`"([)]"` → `false`'],
        quote='可以从消消乐的角度理解，每次可以消除一对==相邻==的匹配括号，不断消除，如果可以把 s 变成空字符串，则 s 是有效字符串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['本题是==邻项消除==问题，这类问题都可以用栈解决',
              '左括号入栈；右括号必须和==栈顶==组成一对，否则无效',
              '细节：长度为奇数直接 `False`；哈希表存“右 → 左”'],
        result='栈空 → `{[()]}` 是有效字符串，返回 `True` ✓',
        summary=['时间 `O(n)`；空间 `O(n)`，若能修改 `s` 可把它当栈做到 `O(1)`',
                 '三种无效：缺右括号、缺左括号、类型不匹配',
                 '易错：`not st` 要写在 `st.pop()` ==前面==，空栈不能弹',
                 '易错：结束时栈非空也无效，所以返回 `not st`',
                 '另两种写法：入栈“对应的右括号”，或用 if-else 代替 mp'],
    ),
)

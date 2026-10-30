SETUP = '''
class _Ch(str):
    pass

class _S(str):
    def __iter__(self):
        for k, c in enumerate(str.__str__(self)):
            x = _Ch(c)
            x.idx = k
            yield x
'''


def _idx(S):
    c = S.get('ch', S.get('char'))
    return getattr(c, 'idx', None) if c is not None else None


def _depths(s):
    d, out = 0, []
    for c in s:
        if c == '(':
            d += 1
        out.append(d)
        if c == ')':
            d -= 1
    return out


def _color(S, i, v):
    k = _idx(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    if i < k:
        return 'green' if v in '()' else None
    return None


def _txt(S):
    k = _idx(S)
    if k is None:
        return '准备从左到右扫描，`depth` 表示当前未闭合的左括号数'
    return f"当前 `depth = {S.get('depth')}`（左侧未闭合的左括号数），目前最大 `ans = {S.get('ans')}`"


CONFIG = dict(
    num=1614, title='括号的最大嵌套深度', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='遍历 · 左括号加一右括号减一',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1323'],
    setup=SETUP,
    code='''
class Solution:
    def maxDepth(self, s: str) -> int:
        ans = depth = 0
        for ch in s:
            if ch == '(':
                depth += 1
                ans = max(ans, depth)
            elif ch == ')':
                depth -= 1
        return ans
''',
    call='Solution().maxDepth(_S("(1+(2*3)+((8)/4))+1"))',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿 = 已扫过的括号）', cell=48, color=_color, h=200),
        dict(type='text', fn=lambda S: '遇 `(` → depth + 1；遇 `)` → depth - 1；最大值就是答案', size=24),
    ],
    watch=[('ch', 'ch', 'blue'), ('depth', 'depth', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = depth = 0': '`depth` 记录当前嵌套层数，`ans` 记录出现过的最大层数，都从 0 开始',
        'for ch in s': "遍历 s：`ch = '{ch}'`",
        "if ch == '('": lambda S, B, r: (f"`'{S.ch}'` 是左括号 → 进入更深一层" if S.ch == '(' else f"`'{S.ch}'` 不是左括号，看看是不是右括号"),
        'depth += 1': '遇到左括号，嵌套深度加一：`depth` = =={depth}==',
        'ans = max': '深度只在左括号处才可能创新高：`ans = max({B.ans}, {depth})` = =={ans}==',
        "elif ch == ')'": lambda S, B, r: (f"`'{S.ch}'` 是右括号 → 退出一层" if S.ch == ')' else f"`'{S.ch}'` 是数字或运算符，深度不变"),
        'depth -= 1': '遇到右括号，嵌套深度减一：`depth` = =={depth}==',
        'return ans': '扫完整串，最大深度 `ans = {ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='左括号深度加一，右括号减一，取最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定有效括号字符串 `s`，返回括号的最大嵌套深度',
                 '示例：`(1+(2*3)+((8)/4))+1` → `3`（数字 8 在 3 层括号里）'],
        quote='遇到左括号，嵌套深度（嵌套层数）就增加一，遇到右括号，嵌套深度就减少一。这也等于当前字符左侧未闭合的左括号的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把括号看成代码里的 `{}`，缩进层数就是嵌套深度',
              '`depth` = 左侧未闭合的左括号个数',
              '深度只会在遇到左括号时变大，所以只在那里更新 `ans`'],
        summary=['时间 `O(n)`，空间 `O(1)`，不需要真的用栈，一个计数器就够',
                 '易错：`ans` 在左括号处更新，别漏了；右括号只减 `depth`',
                 '数字和运算符直接忽略',
                 '同类：合法括号字符串（RBS）题单，如 1249、1963'],
    ),
)

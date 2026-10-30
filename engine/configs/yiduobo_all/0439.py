def _st(S):
    e = S.get('expression')
    if e is None or 'p' not in S:
        return '表达式只有两种形态：单个值，或 `a?b:c`'
    p, n = S['p'], len(e)
    if p >= n:
        return ''
    c = e[p]
    if S.get('_line') in range(15, 25):
        return f"在找 `?` 对应的 `:`：`cnt = {S.get('cnt')}`（嵌套的 `?` 个数）"
    if c in 'TF' and p + 1 < n and e[p + 1] == '?':
        return f"`{c}?…:…`：条件是 `{c}`，选 {'左边 b' if c == 'T' else '右边 c'}"
    return f"`{c}` 后面不是 `?` → 它是最终的值"


def _col(S, i, v):
    if 'p' not in S:
        return None
    p = S['p']
    if i == p:
        return 'blue'
    if i < p:
        return None
    return None


def _dim(S, i, v):
    return 'p' in S and i < S['p']


CONFIG = dict(
    num=439, title='三元表达式解析器', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='下标 p 扫描 · 括号匹配式找冒号',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def parseTernary(self, expression):

        p = 0
        n = len(expression)
        while True:
            if expression[p] == 'T':
                if p + 1 < n and expression[p + 1] == '?':
                    p += 2
                else:
                    return 'T'
            elif expression[p] == 'F':
                if p + 1 < n and expression[p + 1] == '?':
                    cnt = 0
                    p += 2
                    while p + 1 < n:
                        if cnt == 0 and expression[p + 1] == ':':
                            break
                        p += 1
                        if expression[p] == '?':
                            cnt += 1
                        elif expression[p] == ':':
                            cnt -= 1
                    p += 2
                else:
                    return 'F'
            else:
                return expression[p]
''',
    call='Solution().parseTernary("F?T?1:2:T?3:4")',
    expect='3',
    views=[
        dict(type='text', fn=_st, size=26, h=80),
        dict(type='string', var='expression', label='expression（蓝 = 当前下标 p，灰 = 已经跳过）', cell=62,
             pointers={'p': 'blue'}, color=_col, dim=_dim, h=300),
    ],
    watch=[('p', 'p', 'blue'), ('n', 'n'), ('cnt', 'cnt', 'yellow')],
    captions={
        'p = 0': '`p` 记录当前解析到的下标，从 0 开始',
        'n = len': '`n = {n}`',
        'while True': '每一轮只看 `expression[p]`，直到得出最终的值',
        "if expression[p] == 'T'": lambda S, B, r: (f"`expression[{S.p}] = 'T'` → 条件为真，看后面是不是 `?`" if S.expression[S.p] == 'T' else f"`expression[{S.p}] = '{S.expression[S.p]}'` 不是 T"),
        "elif expression[p] == 'F'": lambda S, B, r: (f"`expression[{S.p}] = 'F'` → 条件为假，看后面是不是 `?`" if S.expression[S.p] == 'F' else f"`'{S.expression[S.p]}'` 既不是 T 也不是 F → 是数字"),
        "if p + 1 < n and expression[p + 1] == '?'": lambda S, B, r: ("后面是 `?` → 这是 `a?b:c` 形式" if S.p + 1 < S.n and S.expression[S.p + 1] == '?' else '后面不是 `?` → 它就是单个值'),
        9: '条件为 T：答案就是 b，跳过 `T?`，从 b 开始解析 → `p = {p}`',
        'cnt = 0': '条件为 F：答案是 c，要跳过整个 b。`cnt` 记录 b 里嵌套了几个 `?`',
        15: '跳过 `F?`，`p` 指到 b 的第一个字符 → `p = {p}`',
        'while p + 1 < n': lambda S, B, r: (f"`p = {S.p}`，下一个字符是 `{S.expression[S.p + 1]}`，继续往右找" if S.p + 1 < S.n else '到末尾了'),
        "if cnt == 0 and expression[p + 1] == ':'": lambda S, B, r: (f"`cnt = 0` 且下一个是 `:` → ==找到匹配的冒号== 了" if S.cnt == 0 and S.expression[S.p + 1] == ':' else f"下一个是 `{S.expression[S.p + 1]}`，`cnt = {S.cnt}`，还不是匹配的冒号"),
        18: '`p` 停在冒号前一格',
        "if expression[p] == '?'": lambda S, B, r: (f"`'?'` → 嵌套了一层，`cnt` 加一" if S.expression[S.p] == '?' else f"`'{S.expression[S.p]}'` 不是 `?`"),
        'cnt += 1': '嵌套 +1：`cnt = {cnt}`，后面要多等一个冒号',
        "elif expression[p] == ':'": lambda S, B, r: (f"`':'` → 嵌套的一层结束，`cnt` 减一" if S.expression[S.p] == ':' else f"`'{S.expression[S.p]}'` 不是 `:`"),
        'cnt -= 1': '一个内层冒号配对完：`cnt = {cnt}`',
        24: '`p` 跳过冒号到 c 的开头 → `p = {p}`',
        "return 'T'": '`T` 后面没有 `?` → 答案就是 `T`',
        "return 'F'": '`F` 后面没有 `?` → 答案就是 `F`',
        'return expression[p]': '是数字 → 解析结束，返回 `{expression[p]}`',
    },
    cards=dict(
        one_liner='T 就往 b 走；F 就用括号匹配跳到 c',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`expression` 是任意嵌套的三元表达式，值只有 `T`、`F` 和一位数字',
                 '`a?b:c` 中 `a` 是条件：`T` 取 `b`，`F` 取 `c`；从右向左结合',
                 '本视频：`"F?T?1:2:T?3:4"` → `"3"`'],
        quote='可以发现，一个表达式只有可能以单个值，或者a?b:c的形式出现。',
        quote_src='—— yiduobo 题解原文',
        idea=['`expression[p]` 后面是 `?` → `a?b:c`；否则是最后的单个值',
              '条件为 `T`：答案就是 b，`p += 2` 直接去解析 b',
              '条件为 `F`：要跳过 b，对每个 `?` 计数、遇到 `:` 抵消，`cnt == 0` 时遇到的冒号才是配对的'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：F 分支里跳 b 必须算嵌套，不能碰到第一个冒号就停',
                 '易错：`T` / `F` 后面没有 `?` 时，它本身就是结果',
                 '原文已是 Python 3 可运行的写法，没有修改'],
    ),
)

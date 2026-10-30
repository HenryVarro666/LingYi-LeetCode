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
    author='yiduobo', technique='一趟扫描 · 记录敞开的左括号数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1323'],
    setup=SETUP,
    code='''
class Solution(object):
    def maxDepth(self, s):

        cnt = 0
        res = 0
        for char in s:
            if char == '(':
                cnt += 1
                res = max(res, cnt)
            elif char == ')':
                cnt -= 1

        return res
''',
    call='Solution().maxDepth(_S("(1+(2*3)+((8)/4))+1"))',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: ('准备一趟扫描，`cnt` = 当前敞开的左括号数' if _idx(S) is None else f"`cnt = {S.get('cnt')}` 个左括号还没闭合，历史最大 `res = {S.get('res')}`"), size=28),
        dict(type='string', var='s', label='s（蓝 = 当前字符，绿 = 已扫过的括号）', cell=48, color=lambda S, i, v: _color(S, i, v), h=200),
        dict(type='text', fn=lambda S: '题目保证括号有效，不用栈，数一数敞开的左括号就行', size=24),
    ],
    watch=[('char', 'char', 'blue'), ('cnt', 'cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt = 0': '`cnt`：此刻==敞开==的左括号数目',
        'res = 0': '`res`：扫描过程中 `cnt` 出现过的最大值',
        'for char in s': "取下一个字符：`char = '{char}'`",
        "if char == '('": lambda S, B, r: (f"`'{S.char}'` 是左括号 → 又敞开一个" if S.char == '(' else f"`'{S.char}'` 不是左括号，继续判断"),
        'cnt += 1': '敞开的左括号多了一个：`cnt` = =={cnt}==',
        'res = max': '`cnt` 刚变大，才可能创新高：`res = max({B.res}, {cnt})` = =={res}==',
        "elif char == ')'": lambda S, B, r: (f"`'{S.char}'` 是右括号 → 合上一个" if S.char == ')' else f"`'{S.char}'` 是数字或运算符，直接忽略"),
        'cnt -= 1': '合上一个左括号：`cnt` = =={cnt}==',
        'return res': '扫描结束，最大嵌套深度 `res = {res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='题目保证括号有效，一趟扫描数敞开的左括号',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定有效括号字符串 `s`，返回括号的最大嵌套深度',
                 '示例：`(1+(2*3)+((8)/4))+1` → `3`'],
        quote='由于题目保证了括号字符串是有效的，那么只需一趟扫描，记录当前敞开的左括号数目即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['有效字符串里每个右括号都能配上左括号，所以不必真的配对',
              '遇 `(` 敞开数 +1，遇 `)` 敞开数 -1',
              '敞开数的历史最大值就是嵌套深度'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 只在遇到左括号后更新',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神把括号看成代码缩进，称之为嵌套深度；yiduobo 称为敞开的左括号数'],
    ),
)

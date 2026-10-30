CODE = '''
class Solution(object):
    def scoreOfParentheses(self, S):
        cnt = 0
        res = 0
        for index, char in enumerate(S):
            if char == '(':
                cnt += 1
            else:
                cnt -= 1
                if S[index - 1] == '(':
                    res += (1 << cnt)

        return res
'''
_LINES = CODE.strip('\n').split('\n')
L_FOR = next(i + 1 for i, l in enumerate(_LINES) if 'for index' in l)
L_RET = next(i + 1 for i, l in enumerate(_LINES) if 'return res' in l)
WORD = '(()(()))'
TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环是否已经结束（k = None 表示遍历完）
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''


def _ended(S):
    return S.get('_line') == L_FOR and getattr(S.get('S'), 'k', 0) is None


def _cur(S):
    """当前正在处理的下标；还没进循环 / 已返回时为 None"""
    if S.get('_line') == L_RET or 'index' not in S or _ended(S):
        return None
    return S['index']


def _done(S):
    """已经处理完的字符个数"""
    if S.get('_line') == L_RET or _ended(S):
        return len(WORD)
    if 'index' not in S:
        return 0
    return S['index'] + (0 if S.get('_line') == L_FOR else 1)


def _pairs(S):
    """已被计分的简单括号 '()' 的右括号下标 -> 当时的层数"""
    out, c = {}, 0
    for k in range(_done(S)):
        if WORD[k] == '(':
            c += 1
        else:
            c -= 1
            if WORD[k - 1] == '(':
                out[k] = c
    return out


def _depth_row(S):
    """每个字符处理后的 cnt（未处理的留空）"""
    row, c = [], 0
    n = _done(S)
    for k, ch in enumerate(WORD):
        c += 1 if ch == '(' else -1
        row.append(str(c) if k < n else '')
    return row


def _color(S, i, v):
    pr = _pairs(S)
    if i in pr or (i + 1) in pr and WORD[i] == '(':
        return 'green'
    if i == _cur(S):
        return 'yellow'
    return None


def _formula(S):
    pr = _pairs(S)
    if not pr:
        return '每遇到一个简单括号 `()`，答案加上 ==2^cnt==（cnt = 它外面还没闭合的左括号数）'
    terms = ' + '.join(f'2^{c}' for c in pr.values())
    vals = ' + '.join(str(1 << c) for c in pr.values())
    return f'`res` = {terms} = {vals} = =={sum(1 << c for c in pr.values())}=='


def _if_cap(S, B, ret):
    if B.char == '(':
        return f"`S[{B.index}] = '('` → 左括号，嵌套层数要加一"
    return f"`S[{B.index}] = ')'` → 右括号，闭合一层"


def _simple_cap(S, B, ret):
    i = B.index
    if B.S[i - 1] == '(':
        return f"上一个字符 `S[{i - 1}] = '('`：出现了一个==简单括号 `()`==，外面还套着 {B.cnt} 层"
    return f"上一个字符 `S[{i - 1}] = ')'`：这是外层括号的闭合，==不单独计分==（分数已由里面的 `()` 翻倍体现）"


CONFIG = dict(
    num=856, title='括号的分数', difficulty='Medium', category='栈',
    author='yiduobo', technique='按层数计贡献 · 2^cnt',
    tags=['字节3个月', '字节6个月'],
    code=CODE,
    setup=TRACK,
    call=f"Solution().scoreOfParentheses(Tracked('{WORD}'))",
    expect=6,
    views=[
        dict(type='string', var=lambda S: WORD, label='S（黄 = 当前字符，绿 = 已计分的简单括号）', cell=100, h=230,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'index'}, color=_color,
             dim=lambda S, i, v: i >= _done(S) and i != _cur(S)),
        dict(type='array', var=_depth_row, label='处理完该字符后的 cnt（未闭合的左括号数）', cell=100, index=False, h=170,
             color=lambda S, i, v: 'green' if i in _pairs(S) else None),
        dict(type='text', fn=_formula, size=28, h=80),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('cnt', 'cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt = 0': '`cnt` 记录当前==未闭合的左括号数==（嵌套层数）',
        'res = 0': '`res` 累加每个简单括号 `()` 的贡献',
        'for index': lambda S, B, ret: (f"从左往右扫描：`S[{S.index}] = '{S.char}'`" if _cur(S) is not None
                                        else '整个串扫描完毕'),
        "if char == '('": _if_cap,
        'cnt += 1': '`cnt` → {cnt}：又多了一层没闭合的左括号',
        'cnt -= 1': '`cnt` → {cnt}：这一层闭合了，外面还剩 {cnt} 层',
        "if S[index - 1] == '('": _simple_cap,
        'res += (1 << cnt)': '被 {cnt} 层括号包着，每层都让它 ×2 → 贡献 `1 << {cnt}` = =={1 << cnt}==，`res` = {res}',
        'return res': '所有简单括号的贡献之和就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='每个 () 贡献 2 的「嵌套层数」次方，一趟扫描累加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个平衡括号串，按规则计分：',
                 '`()` 得 1 分；`AB` 得 A + B 分；`(A)` 得 2 × A 分',
                 '示例：`"(()(()))"` → `2 × (1 + 2 × 1)` = `6`'],
        quote='对于第k层的每个简单括号，其都将为答案添加2^k的得分，而这里的k正是当前从左到右扫描过程中未闭合左括号的数量。',
        quote_src='—— yiduobo 题解',
        idea=['先想到递归分治：`(X)` → 2 × X，`(X)Y` → X + Y，但遇到 `(((())))` 会退化成 ==O(n²)==',
              '分数只有「×2」和「相加」两种运算，把式子==展开==：每个 `()` 外面每套一层就 ×2',
              '扫描时用 `cnt` 记层数；遇到 `)` 且前一个是 `(` → 加上 `2^cnt`'],
        summary=['时间 `O(n)`，空间 `O(1)`：比递归分治的 `O(n²)` 更好',
                 '先 `cnt -= 1` 再算 `1 << cnt`：简单括号自己那层不算翻倍',
                 '只有「前一个是 `(`」的右括号才计分；外层的 `)` 只负责减层数',
                 '原文为 Python 2 写法（`class Solution(object)`），已删去文档字符串，逻辑未改'],
    ),
)

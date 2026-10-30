TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

# 代码行号（第 1 行是 class Solution）：7 l += 1 / 9 l -= 1 / 10 if l < 0 / 11 l = 0 / 12 res += 1
BODY_LINES = (7, 9, 10, 11, 12)


def _cur(S):
    s = S.get('S')
    i = getattr(s, 'k', None)
    return i if isinstance(i, int) and i >= 0 else None


def _upto(S):
    s = S.get('S')
    i = getattr(s, 'k', -1)
    if i == -1:
        return 0
    if i is None:
        return len(s)
    return i + 1 if S['_line'] in BODY_LINES else i


def _sim(s, upto):
    """返回 (已配对的下标, 多余右括号的下标, 还在等右括号的左括号下标)"""
    st, matched, extra = [], set(), set()
    for i in range(upto):
        if s[i] == '(':
            st.append(i)
        elif st:
            matched |= {st.pop(), i}
        else:
            extra.add(i)
    return matched, extra, set(st)


def _color(S, i, v):
    s = S.get('S')
    if s is None:
        return None
    u = _upto(S)
    if i >= u:
        return None
    matched, extra, waiting = _sim(str(s), u)
    if i in matched:
        return 'green'
    if i in extra:
        return 'red'
    return 'cyan'


def _txt(S):
    if 'res' not in S:
        return '左括号多了可以等后面补；右括号多了就必须马上补左括号'
    l, res = S['l'], S['res']
    if l < 0 and S['_line'] in (9, 10):
        return f'`l = {l}`：右括号比左括号多 `1` 个，前面已经没有 `(` 可配了'
    return f'未配对的左括号 `l = {l}`；已补的左括号 `res = {res}`；答案 = `res + l`'


def _for(S, B, ret):
    if getattr(S['S'], 'k', None) is None:
        return '扫描结束，看看还剩多少没配上的左括号'
    return f"扫描到第 `{S['S'].k}` 个括号 `char = \"{S['char']}\"`"


def _if10(S, B, ret):
    if S.l < 0:
        return '`l < 0`：右括号比左括号多 → 前面没有 `(` 能配它，必须==立刻补一个左括号=='
    return f'`l = {S.l} ≥ 0`：前面的左括号够用，不用补'


def _l9(S, B, ret):
    if S.l < 0:
        return '右括号来了，但手里没有未配对的左括号，`l` 变成 `-1`'
    return f'右括号配掉一个未配对的左括号：`l` = {S.l}'


CONFIG = dict(
    num=921, title='使括号有效的最少添加', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='计数代替栈 · 一趟扫描',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def minAddToMakeValid(self, S):
        l = 0
        res = 0
        for char in S:
            if char == '(':
                l += 1
            else:
                l -= 1
                if l < 0:
                    l = 0
                    res += 1

        return res + l
''',
    setup=TRACK,
    call='Solution().minAddToMakeValid(Tracked("())((()"))',
    expect=3,
    views=[
        dict(type='string', var=lambda S: str(S['S']), label='S（绿 = 已配对，红 = 多余的 )，青 = 还在等 )）',
             h=250, cell=100, pointers={_cur: 'blue'}, pointer_labels={_cur: 'char'}, color=_color),
        dict(type='stack', var=lambda S: ['('] * S['l'], label='l：还没配对的左括号', h=130, font=34),
        dict(type='stack', var=lambda S: ['('] * S['res'], label='res：已经补上的左括号', h=130, font=34,
             top_color='red'),
        dict(type='text', fn=_txt, size=28, h=100),
    ],
    watch=[('char', 'char', 'blue'), ('l', 'l', 'cyan'), ('res', 'res', 'red')],
    captions={
        3: '`l` 记录当前==还没被配对的左括号==个数，它们可以指望后面的右括号来配',
        4: '`res` 记录==必须补上的左括号==个数',
        'for char in S': _for,
        "if char == '('": lambda S, B, ret: (f'`char = "("` 是左括号：让 `l` 变多，后面也许有右括号来配，先不管'
                                              if S.char == '(' else f'`char = ")"` 是右括号：要去配掉一个未配对的左括号'),
        7: '多了一个等着被配的左括号：`l` = {l}',
        9: _l9,
        'if l < 0': _if10,
        11: '补上的 `(` 刚好和这个 `)` 配成一对，所以未配对的左括号归零：`l = 0`',
        12: '补了一个左括号：`res` = {res}',
        'return res + l': '扫描完还剩 `l = {l}` 个左括号没配上，一次性补 `{l}` 个右括号：`res + l = {res} + {l}` = =={ret}==',
    },
    cards=dict(
        one_liner='右括号多了必须立刻补左括号；左括号多了留到最后再补',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`S` 只含 `(` 和 `)`，每次可以在任意位置插入一个括号',
                 '求让 `S` 变成有效括号串所需的==最少插入次数==',
                 '示例：`"())"` → `1`，`"((("` → `3`；本视频用 `"())((()"` → `3`'],
        quote='若某一时刻右括号数量多于左括号，那么添加一个左括号配平，同时答案加一。',
        quote_src='—— yiduobo 题解原文',
        idea=['左括号多了：可以指望后面的右括号来配 → 先不管，只记个数 `l`',
              '右括号多了：前面已经没有左括号可配 → 必须==立刻补一个左括号==，`res + 1`',
              '扫完后还剩 `l` 个左括号没配上 → 一次性补 `l` 个右括号'],
        result='补了 `1` 个左括号，结尾还剩 `2` 个左括号没配上，再补 `2` 个右括号：`1 + 2 = 3` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`l < 0` 时要把 `l` 重置回 `0`（补的左括号刚好被用掉），再 `res += 1`',
                 '易错：答案是 `res + l`，别漏掉结尾还没配上的左括号',
                 '只有一种括号，栈里全是 `(`，所以用一个计数器 `l` 代替栈',
                 '原文为 Python 2 风格写法，在 Python 3 下无需修改（只去掉了多余的空行）'],
    ),
)

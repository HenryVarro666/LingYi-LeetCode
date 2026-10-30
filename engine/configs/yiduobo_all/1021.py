TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

# 代码行号（第 1 行是 class Solution）：7-9 处理 '('；11-13 处理 ')'；到这些行时当前字符的去留已经确定
DECIDED = (7, 8, 9, 11, 12, 13)


def _kinds(s):
    """每个括号是 'keep'（保留）还是 'outer'（最外层，删掉）——只用于画图"""
    out, cnt = [], 0
    for c in s:
        if c == '(':
            out.append('keep' if cnt > 0 else 'outer')
            cnt += 1
        else:
            cnt -= 1
            out.append('keep' if cnt > 0 else 'outer')
    return out


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
    return i + 1 if S['_line'] in DECIDED else i


def _color(S, i, v):
    s = S.get('S')
    if s is None or i >= _upto(S):
        return None
    return 'green' if _kinds(str(s))[i] == 'keep' else 'red'


def _txt(S):
    if 'cnt' not in S:
        return '去掉每个「原语」最外面的一对括号，其余括号原样保留'
    c = S['cnt']
    if c == 0:
        return '`cnt = 0`：已扫过的左右括号==正好相等== → 下一个 `(` 是最外层左括号'
    return f'`cnt = {c}`：还有 `{c}` 个左括号没配完，当前处在最外层括号的==里面=='


def _for(S, B, ret):
    if getattr(S['S'], 'k', None) is None:
        return '扫描结束，把 `res` 拼成字符串'
    return f"扫描到第 `{S['S'].k}` 个括号 `char = \"{S['char']}\"`"


def _if7(S, B, ret):
    if S.cnt > 0:
        return f'`cnt = {S.cnt} > 0`：前面还有没配完的左括号，当前 `(` 在里面 → ==要保留=='
    return '`cnt = 0`：前面的括号恰好配完，当前 `(` 就是最外层左括号 → ==不收=='


def _if12(S, B, ret):
    if S.cnt > 0:
        return f'`cnt = {S.cnt} > 0`：外面还有没配完的左括号，当前 `)` 在里面 → ==要保留=='
    return '`cnt = 0`：括号全部配完，当前 `)` 就是配最外层左括号的最外层右括号 → ==不收=='


CONFIG = dict(
    num=1021, title='删除最外层的括号', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='计数 · cnt 为 0 即最外层',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def removeOuterParentheses(self, S):
        res = []
        cnt = 0
        for char in S:
            if char == '(':
                if cnt > 0:
                    res.append(char)
                cnt += 1
            else:
                cnt -= 1
                if cnt > 0:
                    res.append(char)

        return ''.join(res)
''',
    setup=TRACK,
    call='Solution().removeOuterParentheses(Tracked("(()())()"))',
    expect='()()',
    views=[
        dict(type='string', var=lambda S: str(S['S']), label='S（绿 = 保留，红 = 最外层括号，删掉）',
             h=230, cell=80, pointers={_cur: 'blue'}, pointer_labels={_cur: 'char'}, color=_color),
        dict(type='stack', var=lambda S: ['('] * S['cnt'], label='cnt：还没匹配的左括号', h=120, font=32),
        dict(type='stack', var='res', label='res：保留下来的括号', h=120, font=32),
        dict(type='text', fn=_txt, size=28, h=100),
    ],
    watch=[('char', 'char', 'blue'), ('cnt', 'cnt', 'cyan'), ('res', "''.join(res)", 'green')],
    captions={
        3: '`res` 收集要保留的括号，最后拼成答案',
        4: '`cnt` 维护==还没匹配的左括号数==：`cnt == 0` 时，已扫过的括号正好全部配对',
        'for char in S': _for,
        "if char == '('": lambda S, B, ret: ('`char = "("`：左括号。先看它是不是最外层，再把 `cnt` 加一'
                                              if S.char == '(' else '`char = ")"`：右括号。先把 `cnt` 减一，再看它是不是最外层'),
        7: _if7,
        8: '内层的左括号，加入答案：`res` = `"{"".join(res)}"`',
        9: '不论收不收，都多了一个没匹配的左括号：`cnt` = {cnt}',
        11: '右括号先配掉一个左括号：`cnt` = {cnt}',
        12: _if12,
        13: '内层的右括号，加入答案：`res` = `"{"".join(res)}"`',
        'return': '把 `res` 里的括号拼起来，返回 =={ret}==',
    },
    cards=dict(
        one_liner='cnt 记没配完的左括号：它为 0 的时刻，当前括号就是最外层',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有效括号串 `S` 可拆成若干个「原语」（不能再拆的非空有效括号串）',
                 '去掉每个原语最外面的一对括号，把剩下的拼起来',
                 '示例：`"(()())(())"` → `"()()()"`；本视频用 `"(()())()"` → `"()()"`'],
        quote='对于最外层括号，有一个性质是当处于在左括号之前以及右括号之后时，当前串中的左右括号正好是相等的。',
        quote_src='—— yiduobo 题解原文',
        idea=['最外层左括号之前、最外层右括号之后：左右括号==正好相等== → `cnt == 0`',
              '碰到 `(`：`cnt == 0` 说明是最外层，不收；否则收。然后 `cnt + 1`',
              '碰到 `)`：先 `cnt - 1`；`cnt == 0` 说明是最外层，不收；否则收'],
        result='两个原语 `(()())` 和 `()`：前者去掉最外层得 `()()`，后者整个删光 → `"()()"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：左括号==先判断再加一==，右括号==先减一再判断==，顺序不能反',
                 '`cnt` 回到 0 的瞬间就是一个原语的结尾；像 `()` 这样的原语会被整个删光',
                 '用列表 `res` 收集再 `join`，比反复拼接字符串更高效',
                 '原文为 Python 2 风格写法，在 Python 3 下无需修改（只去掉了多余空行）'],
    ),
)

def _tokens(s):
    """把 s 切成 token：括号外的单个字母，或一整个括号对；返回每个 token 的 (起, 止)"""
    out, i = [], 0
    while i < len(s):
        if s[i] == '(':
            j = s.index(')', i)
            out.append((i, j))
            i = j + 1
        else:
            out.append((i, i))
            i += 1
    return out


def _state(S):
    s = S.get('s')
    if s is None or 'res' not in S:
        return None
    return _tokens(s), len(S['res'])


def _color(S, i, v):
    st = _state(S)
    if st is None:
        return None
    toks, k = st
    done = toks[k - 1][1] if k else -1
    if i <= done:
        return 'green'
    if k < len(toks) and 'char' in S and toks[k][0] <= i <= toks[k][1]:
        a, b = toks[k]
        if b > a:
            if S.get('flag') and S.get('key') is not None and i <= a + len(S['key']):
                return 'yellow'
            if S['char'] == ')' or i == a and S['char'] == '(':
                return 'yellow'
        elif S['char'] == v and i == a:
            return 'yellow'
    return None


def _txt(S):
    if 'res' not in S:
        return '一趟遍历 `s`，括号外的字母直接进 `res`，括号内的字母攒成 `key`'
    key = ''.join(S['key']) if 'key' in S else ''
    mode = f"正在括号里，已攒 `key = {key!r}`" if S.get('flag') else '当前在括号外'
    return f"{mode}；`res = {''.join(S['res'])!r}`"


CONFIG = dict(
    num=1807, title='替换字符串中的括号内容', difficulty='Medium', category='字符串',
    author='yiduobo', technique='一趟遍历 · flag 标记括号内外',
    tags=[],
    code='''
class Solution(object):
    def evaluate(self, s, knowledge):

        knowledge_dict = {}
        for key, value in knowledge:
            knowledge_dict[key] = value
        
        res = []
        flag = False
        for char in s:
            if char == '(':
                key = []
                flag = True
            elif char == ')':
                flag = False
                res.append(knowledge_dict.get(''.join(key), '?'))
            elif flag:
                key.append(char)
            else:
                res.append(char)
        
        return ''.join(res)
''',
    call='Solution().evaluate("(a)b(c)(a)", [["a", "yes"], ["b", "no"]])',
    expect='yesb?yes',
    views=[
        dict(type='text', h=70, fn=_txt),
        dict(type='string', var='s', h=210, color=_color, label='s（绿 = 已处理，黄 = 正在读的括号对）'),
        dict(type='map', var='knowledge_dict', label='knowledge_dict（key → value）', fmt=lambda k, v: f'{k} → {v}', h=170),
    ],
    watch=[('char', 'char', 'blue'), ('flag', 'flag', 'pink'), ('key', "''.join(key)", 'yellow')],
    captions={
        'knowledge_dict = {}': '先把 `knowledge` 放进字典，方便按 key 查 value',
        'for key, value in knowledge': lambda S, B, ret: ('`knowledge` 读完了' if B.get('key') == S.key and B.get('value') == S.value else f"读 `[{S.key!r}, {S.value!r}]`"),
        'knowledge_dict[key] = value': '`knowledge_dict[{key!r}] = {value!r}`',
        'res = []': '`res` 收集结果',
        9: '`flag` 表示==现在是否在括号里==，一开始不在',
        'for char in s': lambda S, B, ret: ('`s` 扫完了，每个 token 都处理过' if _state(S)[1] == len(_state(S)[0]) else f"读到 `{S.char!r}`"),
        "if char == '('": lambda S, B, ret: ("`'('` → 开始记录括号里的 key" if S.char == '(' else f"`{S.char!r}` 不是左括号"),
        'key = []': '准备一个空列表攒 key',
        'flag = True': '`flag = True`：之后的字母都属于 key',
        "elif char == ')'": lambda S, B, ret: ("`')'` → key 攒完了，去查字典" if S.char == ')' else f"`{S.char!r}` 不是右括号"),
        15: '`flag = False`：括号结束，之后的字母又在括号外',
        'res.append(knowledge_dict.get': lambda S, B, ret: (
            f"`key = {''.join(S.key)!r}`，字典里有 → 追加 `{S.res[-1]!r}`" if ''.join(S.key) in S.knowledge_dict
            else f"`key = {''.join(S.key)!r}`，字典里==没有== → 追加 `'?'`"),
        'elif flag': lambda S, B, ret: ("`flag` 为真：在括号里，这个字母是 key 的一部分" if S.flag else "`flag` 为假：在括号外，字母要原样保留"),
        'key.append(char)': '`key` 追加 `{char!r}` → `{"".join(key)!r}`',
        'res.append(char)': '括号外的字母原样加入：`res = {"".join(res)!r}`',
        "return ''.join(res)": '拼接得到 `{ret!r}`',
    },
    cards=dict(
        one_liner='用 flag 标记在不在括号里：括号内攒 key，括号外直接放',
        complexity='时间 `O((m+n)L)`，空间 `O(m+nL)`',
        problem=['字符串 `s` 里有不嵌套的括号对，括号内是非空 key',
                 '`knowledge` 给出 key → value；括号对替换成 value，没有就替换成 `?`',
                 '本视频：`"(a)b(c)(a)"`，`[["a","yes"],["b","no"]]` → `"yesb?yes"`',
                 '注意：括号外的 `b` 不是 key，不能被替换'],
        quote='当碰到左括号时开始记录括号内的key，当碰到右括号时则去knowledge中查找这个key，若存在那么将对应的value加入到答案中，否则将问号加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`flag` 为真就是在括号里：字母攒进 `key`',
              '碰到右括号再去字典查，查不到就放 `?`',
              '作者说：更普适的做法是用 knowledge 的 key 建一棵 trie，这里偷懒用 dict'],
        summary=['时间 `O((m+n)L)`，空间 `O(m+nL)`',
                 '易错：括号外的字母要直接进 `res`，不能当 key 去查',
                 '每次遇到左括号要重新建空的 `key`，不然会混进上一个括号的内容',
                 '对比灵神：灵神记左括号下标再切片，用 defaultdict 自动给 `?`；这里用 `flag` 加列表攒字母，用 `dict.get`',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动'],
    ),
)

S_IN, T_IN = 'egga', 'addd'


def _color(name):
    def f(S, i, v):
        idx = S.get('index')
        if idx is None:
            return None
        if i < idx:
            return 'green'
        if i == idx and S.get('_line') in (12, 14):
            return 'red'
        if i == idx and S.get('_line') in (16, 17):
            return 'green'
        return None
    return f


def _for_cap(S, B, ret):
    if B.get('index') != S.get('index') or 'index' not in B:
        return f'第 `index = {S.index}` 位：`s[{S.index}] = \'{S.s[S.index]}\'`，`t[{S.index}] = \'{S.t[S.index]}\'`'
    return '扫描完毕，没有冲突'


def _in_dict(S, B, ret):
    a = S.s[S.index]
    if a in S.char_dict:
        return f'`\'{a}\'` 已经有映射 `\'{a}\' → \'{S.char_dict[a]}\'` → 检查它是否等于 `t[{S.index}]`'
    return f'`\'{a}\'` 还没有映射'


def _neq(S, B, ret):
    a, b = S.s[S.index], S.t[S.index]
    if b != S.char_dict[a]:
        return f'`t[{S.index}] = \'{b}\'` ≠ `\'{S.char_dict[a]}\'`：同一个字符映射到了两个字符 → ==不同构=='
    return f'`t[{S.index}] = \'{b}\'` 正好等于映射 `\'{S.char_dict[a]}\'` → 一致，继续'


def _used(S, B, ret):
    b = S.t[S.index]
    if b in S.used_char:
        owner = [k for k, v in S.char_dict.items() if v == b]
        return (f'`\'{b}\'` 已经被 `\'{owner[0]}\'` 映射过了：再让 `\'{S.s[S.index]}\'` 映射到它，'
                f'==两个字符映射到同一字符== → 不同构')
    return f'`\'{b}\'` 也没被用过 → 可以建立新映射'


CONFIG = dict(
    num=205, title='同构字符串', difficulty='Easy', category='哈希',
    author='yiduobo', technique='映射表 + 已用字符集合',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def isIsomorphic(self, s, t):
        if len(s) != len(t):
            return False

        char_dict = {}
        used_char = set()

        for index in range(len(s)):
            if s[index] in char_dict:
                if t[index] != char_dict[s[index]]:
                    return False
            elif t[index] in used_char:
                return False
            else:
                char_dict[s[index]] = t[index]
                used_char.add(t[index])

        return True
''',
    call=f'Solution().isIsomorphic({S_IN!r}, {T_IN!r})',
    expect=False,
    views=[
        dict(type='string', var='s', label='s', pointers={'index': 'blue'}, color=_color('s'), cell=96),
        dict(type='string', var='t', label='t', pointers={'index': 'pink'}, color=_color('t'), cell=96),
        dict(type='map', var='char_dict', label='char_dict（s 的字符 → t 的字符）', h=130, fmt=lambda k, v: f"'{k}' → '{v}'"),
        dict(type='set', var='used_char', label='used_char（t 中已被映射过的字符）', h=120, fmt=lambda x: f"'{x}'"),
    ],
    watch=[('index', 'index', 'blue'), ('s[index]', lambda S: S['s'][S['index']] if 'index' in S else None),
           ('t[index]', lambda S: S['t'][S['index']] if 'index' in S else None, 'pink')],
    captions={
        'if len(s) != len(t)': '两个串等长（都是 {len(s)}），才有可能同构',
        'char_dict = {}': '`char_dict` 记录 s 的每个字符映射到 t 的哪个字符',
        'used_char = set()': '`used_char` 记录 t 中==已经被映射过==的字符',
        'for index in range': _for_cap,
        'if s[index] in char_dict': _in_dict,
        'if t[index] != char_dict': _neq,
        'elif t[index] in used_char': _used,
        12: '映射不一致 → 返回 `False`',
        14: '字符被重复占用 → 返回 `False`',
        'char_dict[s[index]] = t[index]': "建立映射 `'{s[index]}' → '{t[index]}'`",
        'used_char.add': "记录 `'{t[index]}'` 已经被映射过",
        'return True': '扫描完没有冲突 → 同构',
    },
    cards=dict(
        one_liner='s→t 的映射要一致，并且 t 的字符不能被两个字符共用',
        complexity='时间 `O(n)`，空间 `O(Σ)`（字符集大小）',
        problem=['把 `s` 中的字符替换后能得到 `t`，则两串==同构==',
                 '同一字符必须映射到同一字符；==不同字符不能映射到同一字符==',
                 '示例：`"egg","add"` → `true`；`"foo","bar"` → `false`',
                 '本视频：`"egga","addd"` → `false`'],
        quote='若s[index]还没有映射，但是t[index]已经被映射过了，由于题目规定两个字符不能映射到同一字符，因此不同构。',
        quote_src='—— yiduobo 知乎题解',
        idea=['先判长度：不等长一定不同构',
              '`s[index]` 已有映射 → 检查映射是否等于 `t[index]`',
              '没有映射但 `t[index]` 已被用过 → 不同构；否则建立映射并记入 `used_char`'],
        summary=['时间 `O(n)`；`char_dict` 管 s→t，`used_char` 管 t 不被重复占用',
                 '易错：只检查 s→t 会漏掉 `"ab","aa"` 这种==两个字符映射到同一字符==的情况',
                 '等价写法：再建一个 t→s 的反向字典',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '同类题：290 单词规律（字符 ↔ 单词）'],
    ),
)

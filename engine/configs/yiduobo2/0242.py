CASES = [('ab', 'ba'), ('aab', 'ab'), ('ab', 'abb')]


def _pos_s(S):
    if 'chars' not in S or S['_line'] not in (4, 5):
        return None
    k = sum(S['chars'].values()) - (1 if S['_line'] == 5 else 0)
    return k if 0 <= k < len(S['s']) else None


def _pos_t(S):
    if 'chars' not in S or S['_line'] not in (7, 8, 9, 10):
        return None
    k = len(S['s']) - sum(S['chars'].values()) - (1 if S['_line'] == 10 else 0)
    return k if 0 <= k < len(S['t']) else None


def _col_s(S, i, v):
    if 'chars' not in S:
        return None
    if S['_line'] in (4, 5):
        return 'green' if i < sum(S['chars'].values()) else None
    return 'green'


def _col_t(S, i, v):
    if 'chars' not in S or S['_line'] < 7:
        return None
    k = len(S['s']) - sum(S['chars'].values())
    if S['_line'] in (8, 9) and i == k:
        return 'red' if S['chars'].get(S['t'][k], 0) == 0 else None
    return 'pink' if i < k else None


def _case(S):
    s, t = S.get('s'), S.get('t')
    if s is None:
        return ''
    k = CASES.index((s, t)) + 1 if (s, t) in CASES else '?'
    return f'第 {k}/3 组：`s = "{s}"`，`t = "{t}"`（`len(s) = {len(s)}`，`len(t) = {len(t)}`）'


def _if(S, B, ret):
    c, have = S.char, S.chars.get(S.char, 0)
    if have == 0:
        return f'`chars.get({c!r}, 0) = 0`：s 里的 `{c!r}` 已经用完（或根本没有）→ ==t 多出一个 {c!r}=='
    return f'`chars[{c!r}] = {have} > 0`：s 里还有 `{c!r}` 可以配对'


def _ret(S, B, ret):
    if ret:
        return f't 的每个字母都配上了，且 `len(s) == len(t) = {len(S.s)}` → s 正好被用完 → ==True=='
    return (f't 的每个字母都配上了，但 `len(s) = {len(S.s)} ≠ len(t) = {len(S.t)}`：'
            f's 还剩字母没用完 → ==False==')


CONFIG = dict(
    num=242, title='有效的字母异位词', difficulty='Easy', category='哈希',
    author='yiduobo', technique='dict 计数 · 逐个抵消 + 最后比长度',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def isAnagram(self, s, t):
        chars = {}
        for char in s:
            chars[char] = chars.get(char, 0) + 1

        for char in t:
            if chars.get(char, 0) == 0:
                return False
            chars[char] -= 1

        return len(s) == len(t)
''',
    call='''sol = Solution()
[sol.isAnagram(s, t) for s, t in [('ab', 'ba'), ('aab', 'ab'), ('ab', 'abb')]]''',
    expect=[True, False, False],
    views=[
        dict(type='text', size=26, fn=_case),
        dict(type='string', var='s', label='s（绿 = 已计入 chars）', cell=80, h=170, min_slots=4,
             pointers={_pos_s: 'yellow'}, pointer_labels={_pos_s: 'char'}, color=_col_s),
        dict(type='string', var='t', label='t（粉 = 已经抵消；红 = 配不上）', cell=80, h=170, min_slots=4,
             pointers={_pos_t: 'yellow'}, pointer_labels={_pos_t: 'char'}, color=_col_t),
        dict(type='map', var='chars', label='chars：s 中还没被 t 抵消的字母个数', font=30, h=140,
             fmt=lambda k, v: f"'{k}': {v}"),
    ],
    watch=[('char', 'char', 'yellow'), ('len(s)', lambda S: len(S['s'])), ('len(t)', lambda S: len(S['t']))],
    captions={
        'chars = {}': lambda S, B, r: f'新一组 `s = "{S.s}"`，`t = "{S.t}"`：用 dict 统计 s 里每个字母的频率',
        'for char in s': lambda S, B, r: (f'扫 s：`char = {S.char!r}`' if _pos_s(S) is not None else 's 统计完毕'),
        'chars[char] = chars.get(char, 0) + 1': '`chars[{char!r}]` → `{chars[char]}`',
        'for char in t': lambda S, B, r: (f'扫 t：`char = {S.char!r}`，看 s 里还有没有它' if _pos_t(S) is not None
                                          else 't 扫完了，中途没有 `return False`'),
        'if chars.get(char, 0) == 0': _if,
        'return False': '直接返回 ==False==（t 比 s 多出字母的情况都在这里被抓到）',
        'chars[char] -= 1': '用掉 s 里的一个 `{char!r}`：`chars[{char!r}]` → `{chars[char]}`',
        'return len(s) == len(t)': _ret,
    },
    cards=dict(
        one_liner='t 的字母逐个去 s 的计数里“销账”，销完再比一下长度',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['判断 `t` 是不是 `s` 的==字母异位词==：每个字母出现的次数都相同',
                 '示例：`"anagram"`、`"nagaram"` → `true`；`"rat"`、`"car"` → `false`',
                 '本视频三组：`ab/ba`、`aab/ab`、`ab/abb`'],
        quote='首先两个词长度必须要相等，然后使用dict统计其中一个词中各个字母的频率，再==逐个判断另一个词中的字母是否出现在dict中且出现次数相等==即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`chars` 统计 s 的字母；t 每来一个字母就把对应计数减一',
              '计数已经是 0 还要减 → t 多出了这个字母 → 立即 `False`',
              '循环走完说明 t 能被 s 完全“覆盖”，==长度再相等==才是异位词'],
        summary=['时间 `O(n)`，空间 `O(26)`（字符集大小）',
                 '代码把长度判断放到了最后：t 更长会在循环里被抓到，==t 更短只能靠长度判断==（如 `aab/ab`）',
                 '也可以一开始就比长度、提前返回，结果一样',
                 '原文为 Python 2 写法：只删去了类型说明文档字符串，逻辑未改'],
    ),
)

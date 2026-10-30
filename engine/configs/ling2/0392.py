def _cur(S):
    c, t = S.get('c'), S.get('t')
    if c is None or t is None or c not in t:
        return None
    return t.index(c)


def _matched(S, upto):
    """贪心匹配：t[0..upto] 里哪些位置被 s 匹配上了"""
    s, t = S['s'], S['t']
    out, k = set(), 0
    for idx in range(upto + 1):
        if k < len(s) and s[k] == t[idx]:
            out.add(idx)
            k += 1
    return out


def _t_color(S, idx, v):
    cur = _cur(S)
    if cur is None:
        return None
    if idx == cur:
        return 'green' if (S['_line'] in (8, 9, 10) and idx in _matched(S, cur)) else 'blue'
    if idx < cur and idx in _matched(S, cur):
        return 'green'
    return None


def _t_dim(S, idx, v):
    cur = _cur(S)
    return cur is not None and idx < cur and idx not in _matched(S, cur)


def _top(S):
    if 'i' not in S or not S.get('s'):
        return ''
    s, i = S['s'], S['i']
    if i >= len(s):
        return f'`i = {i} == len(s)`：s 全部匹配完'
    if 'c' in S and S['_line'] == 7:
        return f"比较 `s[{i}] = '{s[i]}'` 和 `c = '{S['c']}'`"
    return f"下一个要匹配：`s[{i}] = '{s[i]}'`"


def _if(S, B, ret):
    i, s, c = S.i, S.s, S.c
    if s[i] == c:
        return f"`s[{i}] = '{s[i]}'` == `'{c}'` → ==匹配上了=="
    return f"`s[{i}] = '{s[i]}'` ≠ `'{c}'` → 这个字母没用，相当于==把它删掉=="


CONFIG = dict(
    num=392, title='判断子序列', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='同向双指针 · 遍历 t 匹配 s',
    tags=['面试经典150'],
    code='''
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True
        i = 0
        for c in t:
            if s[i] == c:
                i += 1
                if i == len(s):  # 所有字符匹配完毕
                    return True  # s 是 t 的子序列
        return False
''',
    call='''Solution().isSubsequence("abc", "ahbgdc")
Solution().isSubsequence("axc", "ahbgdc")''',
    expect=False,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（绿 = 已匹配）', cell=84, pointers={'i': 'pink'},
             color=lambda S, k, v: 'green' if k < S.get('i', 0) else None),
        dict(type='string', var='t', label='t（绿 = 匹配上的字母，灰 = 被“删掉”的字母）', cell=84,
             pointers={'t.index(c)': 'blue'}, pointer_labels={'t.index(c)': 'c'}, color=_t_color, dim=_t_dim),
        dict(type='text', fn=lambda S: '两个示例依次运行：`s = "abc"` → True；`s = "axc"` → False', size=24),
    ],
    watch=[('i', 'i', 'pink'), ('c', 'c', 'blue'), ('len(s)', 'len(s)')],
    captions={
        'if not s': '`s = "{s}"` 不为空（空串是任何字符串的子序列，会直接返回 True）',
        'i = 0': '`i` 指向 s 中==下一个要匹配==的字母',
        'for c in t': lambda S, B, ret: (f"遍历 t：`c = t[{S.t.index(S.c)}] = '{S.c}'`" if S.get('c') != B.get('c') or 'c' not in B
                                         else 't 遍历完了'),
        'if s[i] == c': _if,
        'i += 1': '`i` → `{i}`，下一次去匹配 s 的下一个字母',
        'if i == len(s)': lambda S, B, ret: (f'`i == len(s) = {S.i}` → ==所有字符匹配完毕==' if S.i == len(S.s)
                                             else f'`i = {S.i} < len(s) = {len(S.s)}`，s 还没匹配完'),
        'return True': '剩下的字母恰好就是 s → s 是 t 的子序列，返回 `True`',
        'return False': lambda S, B, ret: f"t 遍历完了，s 还剩 `\"{S.s[S.i:]}\"` 没匹配上 → `False`",
    },
    cards=dict(
        one_liner='遍历 t，能匹配 s[i] 就匹配，匹配完 s 就是子序列',
        complexity='时间 `O(n)`，空间 `O(1)`，`n = len(t)`',
        problem=['判断 `s` 是否为 `t` 的==子序列==（删掉 t 的一些字符、不改变相对顺序得到 s）',
                 '示例：`s = "abc"`，`t = "ahbgdc"` → `true`',
                 '`s = "axc"`，`t = "ahbgdc"` → `false`'],
        quote='按照子序列的定义，在遍历 t 的过程中，把没匹配到的字母删除，剩下的就是匹配的字母，即字符串 s，这就说明 s 是 t 的子序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i` 指向 s 中待匹配的字母；遍历 t 中的字母 `c`',
              '`c == s[i]` 就把 `i` 加一；加一后 `i == len(s)` 说明全部匹配，立刻返回 `true`',
              '循环中没返回 → s 不是 t 的子序列'],
        result='`"abc"` → True；`"axc"` 的 `x` 在 t 里找不到 → False ✓',
        after=[dict(heading='进阶：有 10 亿个 s 怎么办？', lines=[
            '预处理 `nxt[i][c]`：t 中下标 ≥ i 的最近字母 c 的下标，找不到记为 `n`',
            '从后往前 DP：`t[i] == c` 时 `nxt[i][c] = i`，否则 `nxt[i][c] = nxt[i+1][c]`',
            '匹配时 `i = nxt[i + 1][c]` 一步跳到位，`i == n` 就失败 → 每个 s 只要 `O(m)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：先特判 s 为空，否则 `s[0]` 越界',
                 '`i` 加一后要==立刻==判断 `i == len(s)`，否则下一轮 `s[i]` 越界',
                 'Python 炫技写法：`it = iter(t)`，`all(c in it for c in s)`'],
    ),
)

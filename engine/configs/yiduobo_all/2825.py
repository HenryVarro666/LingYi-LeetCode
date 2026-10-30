def _ok(b, c):
    return b == c or chr((ord(b) - 97 + 1) % 26 + 97) == c


def _idx(s, t, k):
    out, p = [], 0
    for i, ch in enumerate(s):
        if p < k and _ok(ch, t[p]):
            out.append(i)
            p += 1
    return out


def _s_color(S, i, v):
    if 'p' not in S:
        return None
    return 'green' if i in _idx(S['str1'], S['str2'], S['p']) else None


def _top(S):
    if 'p' not in S:
        return ''
    t, p = S['str2'], S['p']
    if p >= len(t):
        return '`p = len(str2)`：str2 全部匹配完'
    head = f"已匹配 str2 的前 =={p}== 个字母，下一个要找 `str2[{p}] = {t[p]}`"
    if 'char' in S and S['_line'] >= 6:
        head += f"；当前 `char = {S['char']}`"
    return head


def _if(S, B, ret):
    ch, t, p = S.char, S.str2, S.p
    nxt = chr((ord(ch) - 97 + 1) % 26 + 97)
    if ch == t[p]:
        return f"`{ch}` == `str2[{p}] = {t[p]}` → ==直接相等==，匹配"
    if nxt == t[p]:
        return f"`{ch}` 加一得 `{nxt}` == `str2[{p}] = {t[p]}` → ==循环增长后相等==，匹配"
    return f"`{ch}` 和加一后的 `{nxt}` 都不是 `{t[p]}` → 跳过"


CONFIG = dict(
    num=2825, title='循环增长使字符串子序列等于另一个字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='贪心匹配 · 相等或加一后相等',
    tags=['灵神题单', '难度分 1415'],
    code='''
class Solution(object):
    def canMakeSubsequence(self, str1, str2):

        p = 0
        for char in str1:
            if char == str2[p] or chr((ord(char) - 97 + 1) % 26 + 97) == str2[p]:
                p += 1
                if p == len(str2):
                    return True
        
        return False
''',
    call="Solution().canMakeSubsequence('zcxab', 'adb')",
    expect=True,
    views=[
        dict(type='text', fn=_top, h=60),
        dict(type='string', var='str1', color=_s_color, label='str1（绿 = 已匹配的字母）', h=180),
        dict(type='string', var='str2', pointers={'p': 'blue'}, color=lambda S, i, v: 'green' if 'p' in S and i < S['p'] else None,
             dim=lambda S, i, v: False, label='str2（箭头 p = 下一个要匹配的字母）', h=200),
    ],
    watch=[('p', 'p', 'blue'), 'char'],
    captions={
        'p = 0': '`p = 0`：str2 里下一个要匹配的位置',
        'for char in str1': '遍历 str1，按顺序尽量匹配 str2',
        'if char == str2[p]': _if,
        'p += 1': '匹配上，`p` → {p}。能匹配就匹配，待匹配的越少、剩下的原串越长，成功率越高',
        'if p == len(str2)': lambda S, B, r: ('`p == len(str2)`：完整匹配 → 返回 True' if S.p == len(S.str2) else f'`p = {S.p} < {len(S.str2)}`：继续扫'),
        'return True': '返回 True',
        'return False': 'str1 扫完仍没匹配完 → False',
    },
    cards=dict(
        one_liner='循环增长只是多一种“能匹配”的情况，贪心照旧',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`str1` 里任选若干下标，各自循环加一（`z` → `a`），只能操作一次',
                 '问 `str2` 能否成为 `str1` 的子序列',
                 '示例：`zcxab` 与 `adb` → `True`'],
        quote='待匹配的剩余字符越少，匹配成功率越高，而剩余的原字符串越长，匹配成功率越高，综合这两点，对于可以匹配的位置尽量匹配就是最优的选择了。',
        quote_src='—— yiduobo 题解原文',
        idea=['普通子序列的贪心：==能匹配就匹配==，理由是两头都对匹配有利',
              '加了循环增长后这个贪心不受影响，只是匹配条件多了一种',
              '`char == str2[p]` 或 `chr((ord(char)-97+1)%26+97) == str2[p]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`z` 加一回到 `a`，所以用 `% 26`',
                 '`p == len(str2)` 立即返回，避免下一轮 `str2[p]` 越界',
                 '原文为 Python 2 风格，本题无需改动，直接可在 Python 3 运行'],
    ),
)

def _ok(b, c):
    nxt = chr(ord(b) + 1) if b != 'z' else 'a'
    return b == c or nxt == c


def _idx(s, t, k):
    out, p = [], 0
    for i, ch in enumerate(s):
        if p < k and _ok(ch, t[p]):
            out.append(i)
            p += 1
    return out


def _s_color(S, i, v):
    if 'j' not in S:
        return None
    return 'green' if i in _idx(S['s'], S['t'], S['j']) else None


def _top(S):
    if 'j' not in S:
        return ''
    t, j = S['t'], S['j']
    if j >= len(t):
        return '`j = len(t)`：t 全部匹配完'
    head = f"已匹配 t 的前 =={j}== 个字母，下一个要找 `t[{j}] = {t[j]}`"
    if 'b' in S and 'c' in S and S['_line'] >= 7:
        head += f"；当前 `b = {S['b']}`，加一后 `c = {S['c']}`"
    return head


def _if(S, B, ret):
    b, c, t, j = S.b, S.c, S.t, S.j
    if b == t[j]:
        return f"`b = {b}` 直接等于 `t[{j}] = {t[j]}` → ==匹配==（不用操作）"
    if c == t[j]:
        return f"`b = {b}` 不等，但加一后 `c = {c}` == `t[{j}] = {t[j]}` → ==匹配==（这位要循环增长）"
    return f"`b = {b}`、`c = {c}` 都不是 `{t[j]}` → 这个字母用不上，只让 s 往后走"


CONFIG = dict(
    num=2825, title='循环增长使字符串子序列等于另一个字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='判断子序列 · 可匹配 b 或 b+1',
    tags=['灵神题单', '难度分 1415'],
    code='''
class Solution:
    def canMakeSubsequence(self, s: str, t: str) -> bool:
        if len(s) < len(t):
            return False
        j = 0
        for b in s:
            c = chr(ord(b) + 1) if b != 'z' else 'a'
            if b == t[j] or c == t[j]:
                j += 1
                if j == len(t):
                    return True
        return False
''',
    call="Solution().canMakeSubsequence('zcxab', 'adb')",
    expect=True,
    views=[
        dict(type='text', fn=_top, h=60),
        dict(type='string', var='s', color=_s_color, label='s（绿 = 已匹配的字母）', h=180),
        dict(type='string', var='t', pointers={'j': 'blue'}, color=lambda S, i, v: 'green' if 'j' in S and i < S['j'] else None,
             dim=lambda S, i, v: False, label='t（箭头 j = 下一个要匹配的字母）', h=200),
    ],
    watch=[('j', 'j', 'blue'), 'b', 'c'],
    captions={
        'if len(s) < len(t)': lambda S, B, r: (f's 比 t 短，子序列不可能 → 直接 False' if len(S.s) < len(S.t) else f'`len(s) = {len(S.s)} ≥ len(t) = {len(S.t)}`：长度够，开始匹配'),
        'j = 0': '`j = 0`：t 里下一个要匹配的位置',
        'for b in s': '遍历 s 的每个字母 `b`',
        'c = chr': '`b` 循环加一后是 `c = {c}`（`z` 的下一个是 `a`）',
        'if b == t[j]': _if,
        'j += 1': '能匹配就==必须匹配==：不然后面可能没有机会了。`j` → {j}',
        'if j == len(t)': lambda S, B, r: ('`j == len(t)`：t 每个字母都匹配上了 → 返回 True' if S.j == len(S.t) else f'`j = {S.j} < {len(S.t)}`：继续往后匹配'),
        'return False': '扫完 s 还有字母没匹配上 → False',
        'return True': '全部匹配 → True',
    },
    cards=dict(
        one_liner='能匹配就立刻匹配：s[i] 等于 t[j]，或加一后等于 t[j]',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['可对 `str1` 选若干下标，各自循环加一（`z` → `a`），==至多操作一次==',
                 '问能否让 `str2` 成为 `str1` 的子序列',
                 '示例：`zcxab` 与 `adb`：`z→a`、`c→d`、`a→b` → `True`'],
        quote='想一想，如果 s[0] 可以匹配 t[0]，那么此时一定要匹配，不然后面可能没有机会匹配 t[0]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一次操作能选任意多个下标，所以每个字母独立：==保持原样 或 加一==',
              '双指针：`b == t[j]` 或 `c == t[j]` 就 `j += 1`，否则只移动 s',
              '`j` 走到 `len(t)` 就成功；先判断 `len(s) < len(t)` 可提前返回'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`z` 加一是 `a`，不是 `{`',
                 '`j == len(t)` 要在 `j += 1` 之后立刻判断，避免下一轮 `t[j]` 越界',
                 '同类题：392 判断子序列、2486'],
    ),
)

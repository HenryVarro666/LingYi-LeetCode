def _top(S):
    if 'ch' not in S:
        return '`j0`：不修改时 s 已匹配的长度；`j1`：已修改过一次时 s 已匹配的长度'
    return (f"当前 t 的字母 `'{S['ch']}'`：`j0 = {S['j0']}`（没改过），`j1 = {S['j1']}`（改过一次，总是 ≥ j0）")


def _tpos(S):
    t, ch = S.get('t'), S.get('ch')
    if t is None or ch is None:
        return None
    return t.index(ch)


CONFIG = dict(
    num=3983, title='一次替换后的子序列', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='状态机 DP · 双指针 j0 / j1',
    tags=['双序列双指针', '状态机 DP', '难度分 1755'],
    code='''
class Solution:
    def canMakeSubsequence(self, s: str, t: str) -> bool:
        n = len(s)
        if n > len(t):
            return False

        j0 = 0  # 在不修改的情况下，s 的前缀 [0, j0-1] 是 t 的当前前缀的子序列
        j1 = 0  # 在改过一次的情况下，s 的前缀 [0, j1-1] 是 t 的当前前缀的子序列

        for ch in t:
            # j1 普通匹配
            if s[j1] == ch:
                j1 += 1

            # 也可以修改 s[j0] 为 ch，强行匹配
            j1 = max(j1, j0 + 1)

            # j0 普通匹配
            if s[j0] == ch:
                j0 += 1

            if j1 == n:
                # s 是 t 的子序列
                return True

        return False
''',
    call='Solution().canMakeSubsequence("abcd", "aebfd")',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='string', var='s', label='s（绿 = j0 已匹配，青 = j1 多出的部分，含修改）', cell=84, h=210,
             pointers={'j0': 'blue', 'j1': 'pink'},
             color=lambda S, k, v: 'green' if k < S.get('j0', 0) else ('cyan' if k < S.get('j1', 0) else None)),
        dict(type='string', var='t', label='t（当前遍历到的字母）', cell=84, h=210,
             pointers={'t.index(ch)': 'yellow'}, pointer_labels={'t.index(ch)': 'ch'},
             color=lambda S, k, v: 'yellow' if k == _tpos(S) else None),
    ],
    watch=[('j0', 'j0', 'blue'), ('j1', 'j1', 'pink'), ('n', 'n')],
    captions={
        'n = len(s)': '`n = len(s) = {n}`：`j1` 走到 `n` 就说明 s 全部匹配',
        'if n > len(t)': '`{n} > {len(t)}` 不成立；若 s 比 t 还长，改一个字母也不可能是子序列',
        'j0 = 0': '`j0`：==一次都不改==时，s 的前 `j0` 个字母已匹配',
        'j1 = 0': '`j1`：==允许改一次==时，s 的前 `j1` 个字母已匹配',
        'for ch in t': "遍历 t：`ch = '{ch}'`",
        'if s[j1] == ch': lambda S, B, r: (f"`s[{S.j1}] = '{S.s[S.j1]}'` == `'{S.ch}'` → ==普通匹配=="
                                           if S.s[S.j1] == S.ch else f"`s[{S.j1}] = '{S.s[S.j1]}'` ≠ `'{S.ch}'` → 不能普通匹配"),
        'j1 += 1': '`j1` 普通匹配成功 → `{j1}`',
        'j1 = max': lambda S, B, r: (f"改 `s[{S.j0}]` 为 `'{S.ch}'` 强行匹配：`j1 = max({B.j1}, {S.j0} + 1)` = =={S.j1}=="
                                     + ('，改一次比普通匹配更远' if S.j1 > B.j1 else '，不比现有的好')),
        'if s[j0] == ch': lambda S, B, r: (f"`s[{S.j0}] = '{S.s[S.j0]}'` == `'{S.ch}'` → `j0` 也能往前走"
                                           if S.s[S.j0] == S.ch else f"`s[{S.j0}] = '{S.s[S.j0]}'` ≠ `'{S.ch}'` → `j0` 不动（没改过，只能原样匹配）"),
        'j0 += 1': '`j0` → `{j0}`',
        'if j1 == n': lambda S, B, r: (f'`j1 = {S.j1} == n = {S.n}` → ==s 已全部匹配=='
                                       if S.j1 == S.n else f'`j1 = {S.j1} < n = {S.n}`，继续看 t 的下一个字母'),
        'return True': 's 能在至多改一个字母后成为 t 的子序列 → `True`',
        'return False': 't 遍历完了 `j1` 仍不到 `n` → `False`',
    },
    cards=dict(
        one_liner='j0 不改，j1 允许改一次：改的那一次直接让 j1 追上 j0+1',
        complexity='时间 `O(m)`，空间 `O(1)`，`m = len(t)`',
        problem=['最多把 `s` 的一个字母改成任意小写字母',
                 '问能否让 `s` 成为 `t` 的子序列',
                 '示例：`s = "abcd"`，`t = "aebfd"` → `true`（把 `c` 改成 `f`）'],
        quote='对于 j1，有两种情况：普通匹配：如果 s[j1] = t[i]，那么 j1 增加一。修改：把 s[j0] 改成 t[i]，那么 j1 在 j0 的基础上加一。两种情况取最大值。',
        quote_src='—— 灵茶山艾府题解（方法二：状态机 DP）',
        idea=['在 392 题的基础上多维护一个状态：==已经改过一次==的最长匹配 `j1`',
              '改的位置选 `s[j0]`：前面 `j0` 个没改就匹配好了，这个字母强行变成 `ch`',
              '`j0 ≤ j1` 恒成立，所以只需看 `j1 == n`'],
        result='`j1` 追到 `n = 4` → True ✓',
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '先判 `n > len(t)`，否则 `s[j1]` 可能越界',
                 '`j1 = max(j1, j0 + 1)` 要写在 `j0` 更新之前，用的是==旧的 j0==',
                 '题解另给了前后缀分解（pre / suf）和记忆化搜索，本视频演示状态机写法'],
    ),
)

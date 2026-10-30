def _ptr_j(S):
    j = S.get('j')
    return j if isinstance(j, int) and 0 <= j < len(S['t']) else None


def _phase2(S):
    return 'c' in S


def _t_color(S, k, v):
    if 'j' not in S:
        return None
    j = S['j']
    if not _phase2(S):
        return 'orange' if k > j else None
    # 第二阶段：绿 = 前缀已匹配，橙 = 后缀已匹配，红 = 要删掉的子串
    i = S['i']
    nxt = S['suf'][i + 1] if i + 1 < len(S['suf']) else len(S['t'])
    if k < j:
        return 'green'
    if k >= nxt:
        return 'orange'
    return 'red' if S['_line'] in (21, 22, 20) else None


def _s_color(S, k, v):
    if 'j' not in S or 'i' not in S:
        return None
    if _phase2(S):
        return 'green' if k <= S['i'] and S['_line'] >= 17 else None
    return 'orange' if k >= S['i'] else None


def _top(S):
    if 'i' not in S:
        return ''
    if _phase2(S):
        i, j = S['i'], S['j']
        if S['_line'] in (18, 19, 20, 21) and 'suf' in S:
            nxt = S['suf'][i + 1]
            return f"前缀 `t[:{j}]` + 后缀 `t[{nxt}:]` 都能匹配 → 删 `t[{j}:{nxt}]`，长度 `{nxt} − {j}` = =={nxt - j}=="
        return f"第二阶段：从左往右匹配 t 的前缀（`j = {j}`）"
    return '第一阶段：从右往左，求 t 的最长后缀能匹配 s 的哪一段'


CONFIG = dict(
    num=2565, title='最少得分子序列', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前后缀分解 · 删除子串',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·动态规划', '难度分 2432'],
    code='''
class Solution:
    def minimumScore(self, s: str, t: str) -> int:
        n, m = len(s), len(t)
        suf = [m] * (n + 1)
        j = m - 1
        for i in range(n - 1, -1, -1):
            if s[i] == t[j]:
                j -= 1
            if j < 0:  # t 是 s 的子序列
                return 0
            suf[i] = j + 1

        ans = suf[0]  # 删除 t[:suf[0]]
        j = 0
        for i, c in enumerate(s):
            if c == t[j]:  # 注意上面判断了 t 是 s 子序列的情况，这里 j 不会越界
                j += 1
                # 此时 t[:j] 是 s[:i+1] 的子序列
                # t[suf[i+1]:] 是 s[i+1:] 的子序列
                # 删除 t[j:suf[i+1]]
                ans = min(ans, suf[i + 1] - j)
        return ans
''',
    call="Solution().minimumScore('abacaba', 'bzaa')",
    expect=1,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='s', label='s（橙 = 后缀阶段已用到，绿 = 前缀阶段已扫过）', cell=84, h=190,
             pointers={'i': 'pink'}),
        dict(type='string', var='t', label='t（橙 = 能匹配 s 后缀的 t 后缀，绿 = 能匹配 s 前缀的 t 前缀，红 = 删掉的子串）', cell=84, h=190,
             pointers={_ptr_j: 'blue'}, pointer_labels={_ptr_j: 'j'}, color=_t_color),
        dict(type='array', var='suf', label='suf[i]：s[i:] 能匹配的 t 最长后缀的起点', cell=84, h=140, pointers={'i': 'pink'}),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('suf', 'suf', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'n, m = len': '`s = "{s}"`（n = {n}），`t = "{t}"`（m = {m}）：删一段 t 的子串，让剩下的前缀 + 后缀都是 s 的子序列',
        'suf = [m] * (n + 1)': '`suf[i]`：`s[i:]` 能匹配的 ==t 最长后缀==的起点；先填 `m`，表示后缀为空',
        'j = m - 1': '`j` 指向 t 的末尾：从后往前给 t 的后缀找匹配，`j = {j}`',
        'for i in range(n - 1, -1, -1)': lambda S, B, r: ('第一阶段结束' if S.get('i') == B.get('i') and 'i' in B else f'`i` 从后往前枚举 s：`i = {S.i}`'),
        'if s[i] == t[j]': lambda S, B, r: (f"`s[{S.i}] = '{S.s[S.i]}'` == `t[{S.j}] = '{S.t[S.j]}'` → ==匹配==，t 的后缀可以更长"
                                            if S.s[S.i] == S.t[S.j] else f"`s[{S.i}] = '{S.s[S.i]}'` ≠ `t[{S.j}] = '{S.t[S.j]}'` → 匹配不上，`j` 不动"),
        'j -= 1': '`j` → {j}：`t[{j+1}:]` 已经是 `s[{i}:]` 的子序列',
        'if j < 0': lambda S, B, r: ('`j < 0`：t 整个都匹配上了 → t 本来就是 s 的子序列，得分 `0`' if S.j < 0
                                     else f'`j = {S.j} ≥ 0`：t 还没匹配完，继续'),
        'return 0': 't 已经是 s 的子序列，不用删，返回 `0`',
        'suf[i] = j + 1': '`suf[{i}] = {j + 1}`：`t[{j + 1}:]` 是 `s[{i}:]` 的子序列',
        'ans = suf[0]': '一个字符都不留前缀：删掉 `t[:suf[0]]`，得分 `{suf[0]}`，先记为 `ans`',
        'j = 0': '第二阶段：`j` 表示 t 的前缀已经匹配了几个，从 `0` 开始',
        'for i, c in enumerate(s)': lambda S, B, r: ('第二阶段结束' if S.get('i') == B.get('i') and S.get('c') == B.get('c') else f"从左往右枚举：`s[{S.i}] = '{S.c}'`"),
        'if c == t[j]': lambda S, B, r: (f"`'{S.c}'` == `t[{S.j}] = '{S.t[S.j]}'` → ==匹配==，立刻匹配（越早匹配，前缀越短，留给删除的越多）"
                                         if S.c == S.t[S.j] else f"`'{S.c}'` ≠ `t[{S.j}] = '{S.t[S.j]}'` → 这个字母用不上，看 s 的下一个"),
        'j += 1': '`j` → {j}：`t[:{j}]` 是 `s[:{i+1}]` 的子序列',
        'ans = min': '删 `t[{j}:{suf[i+1]}]`，长度 `{suf[i+1]} − {j}` = `{suf[i+1] - j}` → `ans = min({B.ans}, {suf[i+1] - j}) = =={ans}==`',
        'return ans': '最小得分 `{ans}`',
    },
    cards=dict(
        one_liner='只删一段子串；前缀、后缀分头匹配 s，删掉中间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从 `t` 删任意字符，使 `t` 成为 `s` 的子序列；得分 = 删掉的最大下标 − 最小下标 + 1（不删得 0）',
                 '示例：`s = "abacaba"`，`t = "bzaa"` → `1`（删掉 `z`）',
                 '`s = "cde"`，`t = "xyz"` → `3`'],
        quote='删除子串后，剩余部分是 t 的一个前缀和一个后缀。……这个技巧叫做「前后缀分解」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['区间 `[left, right]` 里的字符全删不影响得分 → ==只需考虑删子串==',
              '剩下 t 的前缀匹配 `s[:i]`，t 的后缀匹配 `s[i:]`；枚举 `i`',
              '先倒着算 `suf`，再正着一边匹配前缀一边更新 `ans`，`pre` 数组可以省掉'],
        summary=['时间 `O(n)`，与 t 的长度无关；空间 `O(n)`',
                 '第一阶段发现 `j < 0` 要立刻返回 0，否则第二阶段 `t[j]` 会越界',
                 '`ans = suf[0]` 是「前缀为空」的情况，也要参与取最小',
                 '第二阶段匹配上才更新答案；每个 `i` 最多更新一次',
                 '变形题：删 s 的子串使 t 仍是子序列，见 CF1203D2'],
    ),
)

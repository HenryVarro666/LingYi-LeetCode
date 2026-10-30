def _pending(S, i, v):
    if 'old_ans' in S:
        return S['old_ans'][i] == '?'
    return v == '?'


def _top(S):
    if 'i' not in S or 'ans' not in S:
        return ''
    ln = S['_line']
    if ln <= 14 and 'b' in S:
        return f"处理 `s[{S['i']}] = {S['b']}`" + ('：子串必须等于 `t`' if S['b'] == 'T' else '')
    if 'b' in S:
        return f"处理 `s[{S['i']}] = {S['b']}`" + ('：子串必须不等于 `t`' if S['b'] == 'F' else '')
    return ''


CONFIG = dict(
    num=3474, title='字典序最小的生成字符串', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='先填 T 再贪心改 b',
    tags=['灵神题单·贪心与思维', '灵神题单·字符串', '难度分 2605'],
    code='''
class Solution:
    def generateString(self, s: str, t: str) -> str:
        n, m = len(s), len(t)
        ans = ['?'] * (n + m - 1)  # ? 表示待定位置

        # 处理 T
        for i, b in enumerate(s):
            if b != 'T':
                continue
            # 子串必须等于 t
            for j, c in enumerate(t):
                v = ans[i + j]
                if v != '?' and v != c:
                    return ""
                ans[i + j] = c

        old_ans = ans
        ans = ['a' if c == '?' else c for c in ans]  # 待定位置的初始值为 a

        # 处理 F
        for i, b in enumerate(s):
            if b != 'F':
                continue
            # 子串必须不等于 t
            if ''.join(ans[i: i + m]) != t:
                continue
            # 找最后一个待定位置
            for j in range(i + m - 1, i - 1, -1):
                if old_ans[j] == '?':  # 之前填 a，现在改成 b
                    ans[j] = 'b'
                    break
            else:
                return ""

        return ''.join(ans)
''',
    call='Solution().generateString("TFF", "aa")',
    expect='aaba',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（T = 子串必须等于 t，F = 必须不等于 t）', cell=84, h=190,
             pointers={'i': 'pink'},
             color=lambda S, k, v: 'green' if v == 'T' else 'orange'),
        dict(type='array', var='ans', label='ans（黄 = 待定位置，初始填 a）', cell=84, h=210,
             window=('i', 'i+m-1'),
             color=lambda S, k, v: 'yellow' if _pending(S, k, v) else None),
        dict(type='string', var='t', label='t', cell=84, h=130, color=lambda S, k, v: 'blue'),
    ],
    watch=['n', 'm', 'i', 'j'],
    captions={
        'n, m = len': '`n = {n}`，`m = {m}`：答案长度 `n + m - 1 = {n + m - 1}`',
        "ans = ['?']": '全部先设为待定 `?`',
        "if b != 'T'": lambda S, B, r: (f"`s[{S.i}] = {S.b}` 不是 T，先跳过" if S.b != 'T' else f"`s[{S.i}] = T` → ==这一段必须等于 t=="),
        'for j, c in enumerate(t)': '把 `t` 逐个字符填到 `ans[{i}..{i + m - 1}]`',
        'v = ans[i + j]': '看看 `ans[{i + j}]` 里原来是什么：`{v}`',
        "if v != '?'": lambda S, B, r: (f"`ans[{S.i + S.j}] = {S.v}` 和 `t[{S.j}] = {S.c}` 冲突 → ==无解==" if S.v != '?' and S.v != S.c
                                         else f"`ans[{S.i + S.j}]` 是待定或已经等于 `{S.c}`，没有冲突"),
        'ans[i + j] = c': '`ans[{i + j}] = {c}`',
        'old_ans = ans': '`old_ans` 记住哪些位置是待定的（之后才能改）',
        "ans = ['a'": '待定位置全部先填 `a`：这是字典序最小的填法',
        "if b != 'F'": lambda S, B, r: (f"`s[{S.i}] = {S.b}` 不是 F，跳过" if S.b != 'F' else f"`s[{S.i}] = F` → ==这一段必须不等于 t=="),
        "if ''.join": lambda S, B, r: (f"`ans[{S.i}:{S.i + S.m}] = {''.join(S.ans[S.i:S.i + S.m])}` == `t` → 违规，必须改" if ''.join(S.ans[S.i:S.i + S.m]) == S.t
                                       else f"`ans[{S.i}:{S.i + S.m}] = {''.join(S.ans[S.i:S.i + S.m])}` ≠ `t` → 已满足，不用改"),
        'for j in range(i + m - 1': '从子串最后一个位置往前找第一个待定位置：改得越靠右，字典序越小',
        "if old_ans[j]": lambda S, B, r: (f"`j = {S.j}`：待定位置 → ==把 a 改成 b==" if S.old_ans[S.j] == '?'
                                          else f"`j = {S.j}`：已被 T 固定，不能改，继续往左"),
        "ans[j] = 'b'": '`ans[{j}] = b`：这个子串现在不等于 t 了',
        'continue': '这一项不用处理，看下一个 `s[i]`',
        'break': '改一个就够了，退出',
        'return ""': '子串里没有待定位置可改 → 无解，返回空串',
        "return ''.join": '所有 F 都满足，答案 `{ret}`',
    },
    cards=dict(
        one_liner='先把 T 的子串填好，待定的填 a，不够再改 b',
        complexity='时间 `O(nm)`，空间 `O(n+m)`',
        problem=['`str1` 里 `T` 表示从该下标开始的长 `m` 子串等于 `str2`，`F` 表示不等于',
                 '构造长 `n+m-1` 的字典序最小字符串，不存在则返回空串',
                 '示例：`"TFTF"`、`"ab"` → `"ababa"`；本视频：`"TFF"`、`"aa"` → `"aaba"`'],
        quote='先模拟：处理 s 中的 T，把字符串 t 填入答案的对应位置，如果发现矛盾，就返回空串。没填的位置（待定位置）初始化为 a。再贪心：从左到右检查 F 对应的答案子串，如果发现子串和 t 相同，那么把子串的最后一个待定位置改成 b。',
        quote_src='—— 灵茶山艾府题解',
        idea=['T 的位置必须等于 `t`，先填进去；两个 T 重叠时有冲突就无解',
              '待定位置先填 `a`（最小）；F 的子串若恰好等于 `t`，就把它的==最后一个待定位置==改成 `b`',
              '题解证明了：这样改不会让之前的 F 子串变成 `t`，且只需要改成 `b`'],
        summary=['时间 `O(nm)`，空间 `O(n+m)`',
                 '关键：改最后一个待定位置，才能让字典序尽量小',
                 '易错：只能改待定位置，T 填好的字符不能动；找不到待定位置就无解',
                 '题解另有方法二：用 Z 函数把时间优化到 `O(n+m)`，本视频演示方法一'],
    ),
)

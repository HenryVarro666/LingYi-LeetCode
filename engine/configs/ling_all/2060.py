_I = lambda S: S['_inner']
_PI = lambda S: S['_inner'].get('i')
_PJ = lambda S: S['_inner'].get('j')


def _vis_list(S):
    vis = S.get('vis')
    out = set()
    if not vis:
        return out
    for i, a in enumerate(vis):
        for j, b in enumerate(a):
            for k, x in enumerate(b):
                if x:
                    out.add(f'({i},{j},{k - 1000})')
    return out


def _txt(S):
    d = _I(S)
    if 'd' not in d:
        return '`dfs(i, j, d)`：`s1[:i]` 与 `s2[:j]` 的原串长度差 `d = len1 − len2`，能否匹配'
    i, j, dd = d['i'], d['j'], d['d']
    if dd == 0:
        w = '长度相同 → 字母要相同，或任一边扩展数字'
    elif dd < 0:
        w = '`s2` 更长 → 只扩展 `s1`（数字或字母）'
    else:
        w = '`s1` 更长 → 只扩展 `s2`（数字或字母）'
    return f'`i={i}, j={j}, d={dd}`：{w}'


CONFIG = dict(
    num=2060, title='同源字符串检测', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索 · 状态 (i, j, 长度差 d)（Go 原文转写）',
    tags=['灵神题单·动态规划', '难度分 2804'],
    code='''
class Solution:
    def possiblyEquals(self, s1: str, s2: str) -> bool:
        n, m = len(s1), len(s2)
        mx, bias = 2000, 1000
        vis = [[[False] * mx for _ in range(m + 1)] for _ in range(n + 1)]

        def dfs(i: int, j: int, d: int) -> bool:
            if i == n and j == m:
                return d == 0  # 匹配成功
            if vis[i][j][d + bias]:
                return False
            vis[i][j][d + bias] = True
            # 原始字符串长度相同时，若 s1[i] == s2[j]，则 s1[:i] 和 s2[:j] 均可以向后扩展一个字母
            if d == 0 and i < n and j < m and s1[i] == s2[j] and dfs(i + 1, j + 1, 0):
                return True
            if d <= 0 and i < n:  # s1[:i] 的原始字符串长度不超过 s2[:j] 的原始字符串长度时，扩展 s1[:i]
                if s1[i].isdigit():  # 数字
                    p, v = i, 0
                    while p < n and s1[p].isdigit():
                        v = v * 10 + int(s1[p])
                        if dfs(p + 1, j, d + v):
                            return True
                        p += 1
                elif d < 0 and dfs(i + 1, j, d + 1):  # 字符，扩展一位，注意这里 d 不能为 0
                    return True
            if d >= 0 and j < m:  # s2[:j] 的原始字符串长度不超过 s1[:i] 的原始字符串长度时，扩展 s2[:j]
                if s2[j].isdigit():  # 数字
                    q, v = j, 0
                    while q < m and s2[q].isdigit():
                        v = v * 10 + int(s2[q])
                        if dfs(i, q + 1, d - v):
                            return True
                        q += 1
                elif d > 0 and dfs(i, j + 1, d - 1):  # 字符，扩展一位，注意这里 d 不能为 0
                    return True
            return False

        return dfs(0, 0, 0)
''',
    call='Solution().possiblyEquals("a2b", "3b")',
    expect=True,
    views=[
        dict(type='string', var='s1', label='s1', cell=80, h=170,
             pointers={_PI: 'blue'}, pointer_labels={_PI: 'i'}),
        dict(type='string', var='s2', label='s2', cell=80, h=205,
             pointers={_PJ: 'pink'}, pointer_labels={_PJ: 'j'}),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='calls', h=170),
        dict(type='set', var=_vis_list, label='vis：已访问的状态 (i, j, d)', fmt=lambda x: str(x), h=150, font=22),
    ],
    watch=[('i', _PI, 'blue'), ('j', _PJ, 'pink'), ('d', lambda S: S['_inner'].get('d'), 'orange')],
    skip=['n, m = len', 'mx, bias', 'p += 1', 'q += 1', 'p, v = i, 0', 'q, v = j, 0'],
    captions={
        'vis = [[[False]': '`vis[i][j][d+bias]` 标记状态是否访问过；`d` 在 (-1000, 1000) 内，所以加偏移 `bias = 1000`',
        'return dfs(0, 0, 0)': '从 `dfs(0, 0, 0)` 出发：两边都还没读任何字符，长度差 0',
        'if i == n and j == m': lambda B, S, r: (f'两个串都读完了：长度差 `d = {S.d}`' + ('，==等于 0 → 匹配成功==' if S.d == 0 else '，不为 0 → 失败')
                                                 if S.i == S.n and S.j == S.m else f'`i = {S.i}, j = {S.j}`，还没读完，继续'),
        'return d == 0': '读完且 `d == 0` → 返回 ==True==' ,
        'if vis[i][j][d + bias]': lambda B, S, r: ('这个状态 `(i, j, d)` 以前搜过了（搜过还没成功就不会成功）→ 直接 False' if S.vis[S.i][S.j][S.d + S.bias]
                                                    else '没搜过这个状态，继续'),
        'vis[i][j][d + bias] = True': '标记 `({i}, {j}, {d})` 已访问',
        'if d == 0 and i < n': lambda B, S, r: (f'`d == 0`：长度相同，`s1[{S.i}] = {S.s1[S.i]!r}`，`s2[{S.j}] = {S.s2[S.j]!r}`'
                                                  + ('，相同 → 两边各扩展一个字母' if S.s1[S.i] == S.s2[S.j] else '，不同 → 这条路不行')
                                                  if S.d == 0 and S.i < S.n and S.j < S.m else f'`d = {S.d} ≠ 0`（或已读完一边），不能直接配字母'),
        'if d <= 0 and i < n': lambda B, S, r: (f'`d = {S.d} ≤ 0`：`s1` 的原串不比 `s2` 长 → ==扩展 s1== 一步' if S.d <= 0 and S.i < S.n
                                                  else '`s1` 已经比 `s2` 长（或读完）→ 这一步不扩展 s1'),
        's1[i].isdigit()': lambda B, S, r: (f'`s1[{S.i}] = {S.s1[S.i]!r}` 是数字 → 可以当作长为这个数的一段' if S.s1[S.i].isdigit()
                                             else f'`s1[{S.i}] = {S.s1[S.i]!r}` 是字母'),
        'v = v * 10 + int(s1[p])': '`s1` 连续数字拼成 `v = {v}`（至多 3 位）：原串多出 `{v}` 个字符',
        'if dfs(p + 1, j, d + v)': '`s1` 读到 `p+1`，长度差 `d + v = {B.d + B.v}`：往下搜',
        'elif d < 0 and dfs(i + 1, j, d + 1)': lambda B, S, r: (f'字母：`d = {S.d} < 0`（s2 更长，多出的部分是数字，可以吃掉这个字母）→ `d + 1`' if S.d < 0
                                                               else f'字母：`d = {S.d}`，不是负数 → ==不能在 d = 0 时先吃字母==（字母得和对面字母相配）'),
        'if d >= 0 and j < m': lambda B, S, r: (f'`d = {S.d} ≥ 0`：`s2` 的原串不比 `s1` 长 → ==扩展 s2== 一步' if S.d >= 0 and S.j < S.m
                                                  else '`s2` 已经比 `s1` 长（或读完）→ 这一步不扩展 s2'),
        's2[j].isdigit()': lambda B, S, r: (f'`s2[{S.j}] = {S.s2[S.j]!r}` 是数字 → 可以当作长为这个数的一段' if S.s2[S.j].isdigit()
                                             else f'`s2[{S.j}] = {S.s2[S.j]!r}` 是字母'),
        'v = v * 10 + int(s2[q])': '`s2` 连续数字拼成 `v = {v}`：原串多出 `{v}` 个字符',
        'if dfs(i, q + 1, d - v)': '`s2` 读到 `q+1`，长度差 `d − v = {B.d - B.v}`：往下搜',
        'elif d > 0 and dfs(i, j + 1, d - 1)': lambda B, S, r: (f'字母：`d = {S.d} > 0`（s1 更长，多出的是数字）→ s2 的字母吃掉一个，`d − 1`' if S.d > 0
                                                               else f'字母：`d = {S.d}`，不是正数 → 不能在这里先吃字母'),
        'return True': '子问题成功 → ==一路返回 True==',
        'return False': '这个状态的所有扩展都失败 → 返回 False，回到上一层',
    },
    max_steps=90,
    cards=dict(
        one_liner='状态 (i, j, d)：记住两边原串的长度差，长的那边多出来的一定是数字',
        complexity='时间 `O(n·m·D)`，空间 `O(n·m·D)`，`D` 约 2000',
        problem=['`s1`、`s2` 是编码串：数字表示一段子串被替换成了它的长度',
                 '问是否存在同一个原字符串，能同时编码成 `s1` 和 `s2`',
                 '示例：`"l123e"` 和 `"44"` → `true`；本视频：`"a2b"` 与 `"3b"` → `true`'],
        quote='这一规则同时意味着，当 d≠0 时，较长的原始字符串多出的那部分必然对应着一串数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j, d)`：`s1[:i]` 与 `s2[:j]` 的原串长度差为 `d` 时能否匹配',
              '`d = 0`：字母相同就一起前进，或任意一边展开数字',
              '`d < 0` 只扩展 `s1`（数字或字母），`d > 0` 只扩展 `s2`；连续数字至多 3 位，所以 `d` 在 ±1000 内'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`unicode.IsDigit` → `isdigit()`，`s[i]&15` → `int(s[i])`）',
                 '状态数 `n·m·2000`，每个状态至多枚举 3 位数字，用 `vis` 去重',
                 '易错：`d == 0` 时字母不能单独扩展，必须和对面字母相等才能一起走',
                 '数字可以拆成多种数值，例如 `"12"` 既可当 12，也可当 1 + 2'],
    ),
)

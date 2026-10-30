S0, T0 = 'abac', 'cab'


def _p1(S):
    return 'ans' not in S and 'x' in S and 'y' in S


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if 'ans' in S:
        return 'yellow' if (r, c) == (i + 1, j + 1) and i >= 0 and j >= 0 else None
    if 'x' not in S:
        return None
    if (r, c) == (i + 1, j + 1):
        return 'yellow'
    if S['x'] == S['y']:
        return 'green' if (r, c) == (i, j) else None
    return 'blue' if (r, c) in ((i, j + 1), (i + 1, j)) else None


def _sc(S, k, v):
    i = S.get('i')
    if i is None or k != i:
        return None
    return 'blue'


def _tc(S, k, v):
    j = S.get('j')
    if j is None or k != j:
        return None
    return 'pink'


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i+1][j+1]` = `s[:i+1]` 与 `t[:j+1]` 的最短公共超序列长度'
    if 'ans' in S:
        if i < 0 or j < 0:
            return f'有一个串走完了：把剩下的 `s[:{i + 1}]` = `{S["s"][:i + 1]}`、`t[:{j + 1}]` = `{S["t"][:j + 1]}` 补在前面'
        return f'从 `f[{i + 1}][{j + 1}]` 往回走：`s[{i}] = {S["s"][i]}`，`t[{j}] = {S["t"][j]}`'
    if 'x' not in S:
        return '`f[i+1][j+1]` = `s[:i+1]` 与 `t[:j+1]` 的最短公共超序列长度'
    if S['x'] == S['y']:
        return f'`{S["x"]} = {S["y"]}`：`f[{i + 1}][{j + 1}] = f[{i}][{j}] + 1`'
    return f'`{S["x"]} ≠ {S["y"]}`：`f[{i + 1}][{j + 1}] = min(f[{i}][{j + 1}], f[{i + 1}][{j}]) + 1`'


def _ptr(name, S):
    v = S.get(name)
    return v if isinstance(v, int) and 0 <= v else None


def _cap_if(S, B, ret):
    return None


CONFIG = dict(
    num=1092, title='最短公共超序列', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='LCS 式递推 + 迭代构造答案',
    tags=['灵神题单', '动态规划', '难度分 1977'],
    code='''
class Solution:
    def shortestCommonSupersequence(self, s: str, t: str) -> str:
        n, m = len(s), len(t)
        # f[i+1][j+1] 表示 s 的前缀 [0,i] 和 t 的前缀 [0,j] 的最短公共超序列的长度
        f = [[0] * (m + 1) for _ in range(n + 1)]
        f[0] = list(range(m + 1))  # 递归边界 f[0][j] = j
        for i in range(1, n + 1):
            f[i][0] = i  # 递归边界
        for i, x in enumerate(s):
            for j, y in enumerate(t):
                if x == y:  # 最短公共超序列一定包含 s[i]
                    f[i + 1][j + 1] = f[i][j] + 1
                else:  # 取更短的组成答案
                    f[i + 1][j + 1] = min(f[i][j + 1], f[i + 1][j]) + 1

        ans = []
        i, j = n - 1, m - 1
        while i >= 0 and j >= 0:
            if s[i] == t[j]:  # 公共超序列一定包含 s[i]
                ans.append(s[i])
                i -= 1
                j -= 1  # 相当于继续递归 make_ans(i - 1, j - 1)
            elif f[i + 1][j + 1] == f[i][j + 1] + 1:
                ans.append(s[i])
                i -= 1  # 相当于继续递归 make_ans(i - 1, j)
            else:
                ans.append(t[j])
                j -= 1  # 相当于继续递归 make_ans(i, j - 1)

        # 补上前面的递归边界
        # reversed(ans) 也可以写成 ans[::-1]
        return s[:i + 1] + t[:j + 1] + ''.join(reversed(ans))
''',
    call=f'Solution().shortestCommonSupersequence({S0!r}, {T0!r})',
    expect='cabac',
    skip=['for i in range(1, n + 1)', 'f[i][0] = i', 'for j, y in enumerate', 'n, m = len'],
    views=[
        dict(type='string', var='s', label='s（蓝 = i）', h=120, cell=56, color=_sc),
        dict(type='string', var='t', label='t（粉 = j）', h=120, cell=56, color=_tc),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算/正在回溯，绿/蓝 = 它依赖的格子）', h=320, cell=64,
             rows=lambda S: ['∅'] + list(S0), cols=lambda S: ['∅'] + list(T0), color=_cell),
        dict(type='array', var='ans', label='ans（从后往前追加，最后要反转）', h=120, cell=50),
    ],
    watch=['i', 'j', ('ans', "''.join(ans) if 'ans' in S else ''", 'green')],
    captions={
        'f = [[0] * (m + 1)': '建 `(n+1) × (m+1)` 的表，多出的第 0 行、第 0 列表示空串',
        'f[0] = list(range': '`s` 为空时，超序列就是整个 `t`：`f[0][j] = j`（左边界 `f[i][0] = i` 同理，已一并填好）',
        'for i, x in enumerate': lambda S, B, r: (f'`i = {S.i}`：外层枚举 `s[{S.i}]` = `{S.x}`' if S.i != B.get('i') or 'x' not in B else '`s` 的每个字母都枚举过了，表填完'),
        'if x == y': lambda S, B, r: (f'`s[{S.i}] = t[{S.j}] = {S.x}` → ==相同字母只需放一个==，等价于 LCS 里的“匹配”' if S.x == S.y
                                      else f'`s[{S.i}] = {S.x}` ≠ `t[{S.j}] = {S.y}` → 末尾字母二选一'),
        'f[i + 1][j + 1] = f[i][j] + 1': '`f[{i+1}][{j+1}] = f[{i}][{j}] + 1` = =={f[i+1][j+1]}==：共用同一个字母',
        'f[i + 1][j + 1] = min': '`f[{i+1}][{j+1}] = min({f[i][j+1]}, {f[i+1][j]}) + 1` = =={f[i+1][j+1]}==：取更短的一边，再追加一个字母',
        'ans = []': '表填完了，`f[{n}][{m}] = {f[n][m]}` 就是最短长度；再从右下角往回走，==还原出具体的串==',
        'i, j = n - 1': '回溯起点：`i = {i}`，`j = {j}`，即 `f[{i+1}][{j+1}]`',
        'while i >= 0 and j >= 0': lambda S, B, r: ('`i >= 0 and j >= 0`：两个串都还没用完，继续' if S.i >= 0 and S.j >= 0
                                                    else f'`i = {S.i}`，`j = {S.j}`：有一个串用完了，退出循环'),
        'if s[i] == t[j]': lambda S, B, r: (f'`s[{S.i}] = t[{S.j}] = {S.s[S.i]}` → 这个字母==一定在答案里==，两个指针一起退' if S.s[S.i] == S.t[S.j]
                                           else f'`s[{S.i}] = {S.s[S.i]}` ≠ `t[{S.j}] = {S.t[S.j]}` → 看 f 是从哪边转移来的'),
        'ans.append(s[i])': lambda S, B, r: f'追加 `{S.s[B.i]}`，`ans = {"".join(S.ans)}`',
        'ans.append(t[j])': lambda S, B, r: f'追加 `{S.t[B.j]}`，`ans = {"".join(S.ans)}`',
        'elif f[i + 1][j + 1] == f[i][j + 1] + 1': lambda S, B, r: (f'`f[{S.i+1}][{S.j+1}] = {S.f[S.i+1][S.j+1]}` 等于 `f[{S.i}][{S.j+1}] + 1 = {S.f[S.i][S.j+1]+1}` → 当初取的是 ==s 那边==，追加 `s[{S.i}]`' if S.f[S.i+1][S.j+1] == S.f[S.i][S.j+1] + 1 else
                                                                  f'`f[{S.i+1}][{S.j+1}] = {S.f[S.i+1][S.j+1]}` 不等于 `f[{S.i}][{S.j+1}] + 1 = {S.f[S.i][S.j+1]+1}` → 当初取的是 ==t 那边==，追加 `t[{S.j}]`'),
        'i -= 1  # 相当于继续递归 make_ans(i - 1, j)': '`i` 退到 {i}',
        'j -= 1  # 相当于继续递归 make_ans(i, j - 1)': '`j` 退到 {j}',
        'i -= 1': '`i` 退到 {i}',
        'j -= 1': '`j` 退到 {j}',
        'return s[:i + 1]': lambda S, B, r: f'补上没走完的前缀：`s[:{S.i+1}]` = `{S.s[:S.i+1]}`，`t[:{S.j+1}]` = `{S.t[:S.j+1]}`；再接上反转的 ans → ==`{r}`=='
    },
    cards=dict(
        one_liner='和 LCS 一样填表，再顺着表从后往前拼出答案',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['给两个字符串 `str1`、`str2`，返回==同时以它们为子序列的最短字符串==，多解返回任意一个',
                 '示例：`str1 = "abac"`，`str2 = "cab"` → `"cabac"`',
                 '本视频：`s = abac`，`t = cab`，答案长度 `5`'],
        quote='答案的最后一个字母，要么是 s 的最后一个字母，要么是 t 的最后一个字母。其它字母是没有意义的。',
        quote_src='—— 灵茶山艾府题解（一、初步思路）',
        idea=['末尾字母相同：它必在答案里，问题缩成两个前缀；不同：二选一，取更短的',
              '先只算长度 `f`（这样才不会拼接字符串超时），再从 `f[n][m]` 往回走构造方案',
              '看 `f[i+1][j+1]` 是否等于 `f[i][j+1] + 1` 就知道当初选了哪一边'],
        after=[dict(heading='灵神的演进路线', lines=['递归 → 加 `@cache` 记忆化 → 只返回长度 + `make_ans` 构造', '再 1:1 翻译成递推 + 迭代回溯（本视频的写法）'])],
        summary=['时间、空间都是 `O(nm)`；回溯一步 `O(1)`，全程 `O(n+m)`',
                 '易错：`f` 要多开一行一列放空串边界，下标整体 +1',
                 '易错：回溯是从后往前，`ans` 最后要反转；循环结束后还要补上没走完的前缀',
                 '同一思路：1143 最长公共子序列、打印方案类题'],
    ),
)

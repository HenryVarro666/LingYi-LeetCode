_pending = set()   # (i, j)：x != y 时这一行会触发两次（先判断、再赋值），用来区分两步


def _stale(S):
    # 刚执行完 f[i+1][0] = i+1 时，j / y 还是上一行留下的旧值（本输入中第 1 行起的 f 值都 ≥ 1）
    return 'y' not in S or S['f'][S['i'] + 1][S['j']] == 0


def _dep(S, i, j, v):
    if _stale(S):
        return None
    ci, cj = S['i'], S['j']
    if S['x'] == S['y']:
        return 'green' if (i, j) == (ci, cj) else None          # 左上：不用操作
    if (i, j) == (ci, cj + 1):
        return 'blue'                                           # 上：删除 x
    if (i, j) == (ci + 1, cj):
        return 'pink'                                           # 左：插入 y
    if (i, j) == (ci, cj):
        return 'purple'                                         # 左上：替换
    return None


def _cursor_i(S):
    return S['i'] + 1 if 'i' in S else None


def _cursor_j(S):
    return 0 if _stale(S) else S['j'] + 1


def _formula(S):
    if 'i' not in S:
        return '`f[i+1][j+1]` = 把 `s` 前 `i+1` 个字母变成 `t` 前 `j+1` 个字母的最少操作数'
    if _stale(S):
        return f'f[{S["i"] + 1}][0] = {S["i"] + 1}：t 为空串，只能全删'
    i, j, x, y, f = S['i'], S['j'], S['x'], S['y'], S['f']
    if x == y:
        return f'x = y = {x}：f[{i + 1}][{j + 1}] = 左上 =={f[i][j]}==（不用操作）'
    a, b, c = f[i][j + 1], f[i + 1][j], f[i][j]
    return f'x = {x} ≠ y = {y}：min(删 {a}, 插 {b}, 换 {c}) + 1 = =={min(a, b, c) + 1}=='


def _cap_cell(S, B, ret):
    i, j, x, y, f = S.i, S.j, S.x, S.y, S.f
    if x == y:
        return f'`x = y = {x}`：最后一个字母相同，==什么都不用做== → `f[{i + 1}][{j + 1}] =` 左上 `{f[i][j]}`'
    if (i, j) not in _pending:
        _pending.add((i, j))
        if (i, j) == (0, 0):
            return f'`x = {x}` ≠ `y = {y}`：必须对 x 做一次操作，删除 / 插入 / 替换选最省的 → 走 `else`'
        return f'`x = {x}` ≠ `y = {y}` → 走 `else`'
    _pending.discard((i, j))
    a, b, c = f[i][j + 1], f[i + 1][j], f[i][j]
    if (i, j) == (0, 0):
        return (f'删 x → 上 `{a}`；插入 y → 左 `{b}`；把 x 换成 y → 左上 `{c}`；'
                f'取最小再 +1 → `{f[i + 1][j + 1]}`')
    return f'`min(删 {a}, 插 {b}, 换 {c}) + 1 = {f[i + 1][j + 1]}`'


CONFIG = dict(
    num=72, title='编辑距离', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='线性 DP：记忆化搜索 → 1:1 翻译成递推',
    code='''
class Solution:
    def minDistance(self, s: str, t: str) -> int:
        n, m = len(s), len(t)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        f[0] = list(range(m + 1))
        for i, x in enumerate(s):
            f[i + 1][0] = i + 1
            for j, y in enumerate(t):
                f[i + 1][j + 1] = f[i][j] if x == y else \\
                        min(f[i][j + 1], f[i + 1][j], f[i][j]) + 1
        return f[n][m]
''',
    call='Solution().minDistance("horse", "ros")',
    expect=3,
    skip=['f = [[0] * (m + 1)', 'for i, x in enumerate(s)', 'for j, y in enumerate(t)',
          'min(f[i][j + 1], f[i + 1][j], f[i][j]) + 1'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='table', var='f', label='f（行头 = s 的字母 x，列头 = t 的字母 y；蓝 删 · 粉 插 · 紫 换）',
             rows=lambda S: ['∅'] + list(S['s']), cols=lambda S: ['∅'] + list(S['t']),
             cursors=[('n', 'm', 'green'), (_cursor_i, _cursor_j, 'yellow')], color=_dep, cell=84, h=574),
    ],
    watch=['i', 'j', ('x', 'x', 'orange'), ('y', 'y', 'orange'), ('f[n][m]', 'f[n][m]', 'green')],
    captions={
        'n, m = len(s), len(t)': 'f 开 `(n+1) × (m+1)`：多出的第 0 行 / 第 0 列代表==空串==（即 `dfs(-1, ·)` 和 `dfs(·, -1)`）',
        'f[0] = list(range(m + 1))': '第 0 行：`s` 是空串，要变成 `t` 的前 `j` 个字母只能==插入 j 次==（翻译自 `dfs(-1, j) = j + 1`）',
        'f[i + 1][0] = i + 1': lambda S, B, ret: (
            f'外层 `x = {S.x}`。第 0 列：`t` 是空串，`s` 的前 `{S.i + 1}` 个字母==全删掉==：`{S.i + 1}` 次（`dfs(i, -1) = i + 1`）'
            if S.i == 0 else f'外层换到 `x = {S.x}`，第 0 列：全删 → `{S.i + 1}`'),
        'f[i + 1][j + 1] = f[i][j] if x == y else': _cap_cell,
        'return f[n][m]': '`f[n][m]` 翻译自递归入口 `dfs(n-1, m-1)`：最少 =={ret}== 次操作',
    },
    cards=dict(
        one_liner='只看最后一个字母：相同就跳过，不同就删 / 插 / 换选最省的',
        complexity='时间 `O(nm)`，空间 `O(nm)`（可优化到 `O(m)`）',
        problem=['把 `word1` 变成 `word2`，每次可以==插入、删除或替换==一个字符',
                 '求最少操作数',
                 '示例：`"horse"` → `"ros"`：`3`（h 换成 r，删 r，删 e）'],
        quote='先操作 i 再操作 j，还是先操作 j 再操作 i，结果都是一样的。推广，任意一种操作顺序，都可以==重新排列成从右往左（从左往右）操作==。',
        quote_src='—— 灵茶山艾府题解（答疑）',
        idea=['所以只需从右往左看：`dfs(i,j)` = `s[0..i]` 变成 `t[0..j]` 的最少操作数',
              '`s[i] = t[j]`：不用操作，`dfs(i-1,j-1)`',
              '否则 `+1`：删 `dfs(i-1,j)` / 插 `dfs(i,j-1)` / 换 `dfs(i-1,j-1)` 取最小',
              '边界：`dfs(-1,j) = j+1`，`dfs(i,-1) = i+1`；`@cache` 记忆化',
              '1:1 翻译成递推：`f[i+1][j+1]` 就是 `dfs(i,j)`，第 0 行 / 列就是边界'],
        after=[dict(heading='记忆化搜索 → 递推：逐项对照', lines=[
            '`dfs(i, j)` ↔ `f[i+1][j+1]`（下标整体 +1）',
            '`dfs(-1, j) = j+1` ↔ 第 0 行 `f[0] = list(range(m+1))`',
            '`dfs(i, -1) = i+1` ↔ 第 0 列 `f[i+1][0] = i+1`',
            '删 / 插 / 换 ↔ 上 / 左 / 左上；入口 `dfs(n-1, m-1)` ↔ `f[n][m]`',
        ])],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '易错：边界不是 0：`f[0][j] = j`，`f[i][0] = i`',
                 '易错：字母相同时直接继承左上，==不要再 +1==',
                 '原文还有滚动数组和一个数组（用 `pre` 暂存左上角）的写法，空间 `O(m)`'],
    ),
)

def _cmp(S):
    if 'k' not in S or 'i' not in S:
        return ''
    c, w = S['grid'][S['i']][S['j']], S['target'][S['k']]
    cs = f"'{c}'" if c else "''（已访问）"
    return f"当前格子 `grid[{S['i']}][{S['j']}] = {cs}`，要匹配 `target[{S['k']}] = '{w}'`"


def _bounds(S, B, ret):
    if 'x' in S and not (0 <= S.x < S.m and 0 <= S.y < S.n):
        return f'相邻格子 `({S.x}, {S.y})` ==出界== → 跳过'
    return f'`({S.i}, {S.j})` 没出界 → 递归 `dfs({S.i}, {S.j}, {S.k})`，看它能否匹配 `target[{S.k}]`'


def _for(S, B, ret):
    if 'x' in S and (S.x, S.y) != (B.get('x'), B.get('y')):
        return f'枚举相邻格子：`(x, y) = ({S.x}, {S.y})`'
    return f'`({S.i}, {S.j})` 的四个相邻格子都没搜到'


CONFIG = dict(
    num='LCR 129', title='字母迷宫', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='网格图 DFS + 回溯 + 两个优化',
    code='''
class Solution:
    def wordPuzzle(self, grid: List[List[str]], target: str) -> bool:
        cnt = Counter(c for row in grid for c in row)
        if not cnt >= Counter(target):  # 优化一
            return False
        if cnt[target[-1]] < cnt[target[0]]:  # 优化二
            target = target[::-1]

        m, n = len(grid), len(grid[0])
        def dfs(i: int, j: int, k: int) -> bool:
            if grid[i][j] != target[k]:  # 匹配失败
                return False
            if k == len(target) - 1:  # 匹配成功！
                return True
            grid[i][j] = ''  # 标记访问过
            for x, y in (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j):  # 相邻格子
                if 0 <= x < m and 0 <= y < n and dfs(x, y, k + 1):
                    return True  # 搜到了！
            grid[i][j] = target[k]  # 恢复现场
            return False  # 没搜到
        return any(dfs(i, j, 0) for i in range(m) for j in range(n))
''',
    call="Solution().wordPuzzle([['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], 'SEE')",
    expect=True,
    views=[
        dict(type='grid', var='grid', label='grid（橙 = 已访问，黄框 = 当前格子）', cell=64, h=260,
             cursors=[('i', 'j', 'yellow')],
             color=lambda S, i, j, v: 'orange' if v == '' else None),
        dict(type='string', var='target', label='target（蓝 = 要匹配的 target[k]，绿 = 已匹配）', cell=60, h=120,
             color=lambda S, i, v: 'blue' if i == S['k'] else ('green' if i < S['k'] else None)),
        dict(type='text', fn=_cmp, h=48, size=24),
        dict(type='calls', h=200),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('k', 'k', 'blue'), 'x', 'y'],
    captions={
        'cnt = Counter': '统计 grid 里每个字母出现的次数：`C` {cnt["C"]} 个、`E` {cnt["E"]} 个、`S` {cnt["S"]} 个',
        'if not cnt >= Counter(target)': lambda S, B, ret: (
            f"优化一：`target = '{S.target}'` 的每个字母，grid 里都够用 → 继续"),
        'if cnt[target[-1]] < cnt[target[0]]': lambda S, B, ret: (
            f"优化二：末尾 `'{S.target[-1]}'` 有 {S.cnt[S.target[-1]]} 个 < 开头 `'{S.target[0]}'` 有 {S.cnt[S.target[0]]} 个 → ==从更少的那头开始搜=="
            if S.cnt[S.target[-1]] < S.cnt[S.target[0]] else '优化二：开头字母不比末尾多，不反转'),
        'target = target[::-1]': "`target` 反转成 `'{target}'`：起点更容易一上来就匹配失败，递归更少",
        'return any(': '枚举每个格子 `(i, j)` 当起点，调用 `dfs(i, j, 0)`，有一个成功就返回 `True`',
        'if grid[i][j] != target[k]': lambda S, B, ret: (
            (f"`grid[{S.i}][{S.j}]` 已访问（被置空）→ 不能重复用" if S.grid[S.i][S.j] == '' else
             f"`grid[{S.i}][{S.j}] = '{S.grid[S.i][S.j]}' ≠ target[{S.k}] = '{S.target[S.k]}'` → ==匹配失败==")
            if S.grid[S.i][S.j] != S.target[S.k] else
            f"`grid[{S.i}][{S.j}] = '{S.target[S.k]}'` 和 `target[{S.k}]` ==匹配上了=="),
        12: '返回 `False`',
        'if k == len(target) - 1': lambda S, B, ret: (
            f'`k == len(target) - 1`：最后一个字母也匹配上了 → ==匹配成功！==' if S.k == len(S.target) - 1 else
            f'`k = {S.k}`，还没匹配到最后一个字母'),
        14: '返回 `True`',
        "grid[i][j] = ''": "标记访问过：`grid[{i}][{j}]` 置为空，后面就不会重复走这个格子",
        'for x, y in': _for,
        'if 0 <= x < m': _bounds,
        'return True  # 搜到了': '子递归搜到了 → 一路返回 `True`（不用恢复现场了）',
        'grid[i][j] = target[k]': "恢复现场：`grid[{i}][{j}]` 改回 `'{target[k]}'`，让别的路径还能用它",
        'return False  # 没搜到': '四个方向都没搜到 → 返回 `False`',
    },
    max_steps=66,
    cards=dict(
        one_liner='走过的格子先置空，搜不到再恢复；从更稀有的字母那头开始搜',
        complexity='时间 `O(mn·3^k)`，空间 `O(|Σ| + k)`',
        problem=['在 `m×n` 字母网格里，能否沿上下左右相邻格子拼出 `target`（同一格不能重复用）',
                 "示例改小：第 1 个示例的 grid，`target = \"SEE\"` → `true`"],
        quote='`dfs(i,j,k)` 表示当前在 `grid[i][j]` 这个格子，要匹配 `target[k]`……==直接修改 grid[i][j]，将其置为空，返回 false 前再恢复成原来的值（恢复现场）==。',
        quote_src='—— 灵茶山艾府题解「基本思路」',
        idea=['不匹配 → `False`；匹配且 `k` 是最后一位 → `True`；否则递归四个邻居',
              '优化一：target 某字母比 grid 里还多 → 直接 `False`',
              '优化二：末尾字母更少就反转 target，开头更容易失败，递归更少'],
        result='从右边的 `S` 出发，走 `(1,3) → (2,3) → (2,2)`，拼出 `SEE` ✓',
        summary=['除了入口，每层至多 3 个分支 → `O(mn·3^k)`',
                 '返回 `True` 时不用恢复现场：已经搜到了，grid 不再使用',
                 '返回 `False` 前一定要恢复，否则别的起点用不了这个格子',
                 '加上两个优化，Java/C++/Go/Rust 都能跑到 0ms'],
    ),
)

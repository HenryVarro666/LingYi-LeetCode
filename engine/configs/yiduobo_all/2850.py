G0 = [[2, 1, 0], [1, 0, 1], [1, 2, 1]]


def _cell(S, i, j, v):
    z = S.get('z') or []
    lv = S['_inner'].get('level') if '_inner' in S else None
    x, y = S['_inner'].get('x'), S['_inner'].get('y')
    if lv is not None and lv < len(z) and (i, j) == tuple(z[lv]):
        return 'cyan'
    if x is not None and (i, j) == (x, y) and S.get('_line') in (21, 22, 23, 24, 25, 26, 27):
        return 'pink'
    if v > 1:
        return 'orange'
    return None


def _txt(S):
    z = S.get('z')
    if not z:
        return '青 = 空格（要接收石头），橙 = 石头多的格子（可以送出）'
    lv = S['_inner'].get('level')
    s = S['_inner'].get('s')
    if lv is None:
        return ''
    if lv < len(z):
        return f"现在给第 `{lv}` 个空格 `({z[lv][0]},{z[lv][1]})` 找石头来源；已累计距离 `s = {s}`"
    return f"所有空格都分到了石头：总距离 `s = {s}`"


CONFIG = dict(
    num=2850, title='将石头分散到网格图的最少移动次数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='空格逐个选来源 · 暴力回溯',
    tags=['图论算法', '动态规划', '难度分 2001'],
    code='''
class Solution(object):
    def minimumMoves(self, grid):
        z = []
        g = []
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    z.append([i, j])
                elif grid[i][j] > 1:
                    g.append([i, j])

        global res
        res = 10000

        def dfs(level, s):
            if level == len(z):
                global res
                res = min(res, s)
                return

            for x, y in g:
                if grid[x][y] > 1:
                    grid[x][y] -= 1
                    s += abs(x - z[level][0]) + abs(y - z[level][1])
                    dfs(level + 1, s)
                    s -= abs(x - z[level][0]) + abs(y - z[level][1])
                    grid[x][y] += 1

        dfs(0, 0)
        return res
''',
    call=f'Solution().minimumMoves({G0!r})',
    expect=3,
    views=[
        dict(type='grid', var='grid', label='grid（回溯时石头数会被占用、再还回来）', h=250, cell=66, color=_cell),
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='calls', h=250),
    ],
    watch=[('level', "_inner.get('level')", 'blue'), ('s', "_inner.get('s')", 'pink')],
    captions={
        'z = []': '`z` 收集初始值为 0 的格子（要接收石头）',
        'g = []': '`g` 收集初始值大于 1 的格子（能送出石头）；值为 1 的格子直接无视',
        'if grid[i][j] == 0': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 0` → 空格' if S.grid[S.i][S.j] == 0 else f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}`，不是空格'),
        'z.append': '空格 `{[i, j]}` 加入 `z`',
        'elif grid[i][j] > 1': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` > 1 → 可以送出石头' if S.grid[S.i][S.j] > 1 else '值为 1，无视'),
        'g.append': '`{[i, j]}` 加入 `g`（石头多的来源）',
        'res = 10000': '`res` 记录最小总距离，先设成很大的数',
        'dfs(0, 0)': '从第 0 个空格开始，逐个为空格选一个来源',
        'if level == len(z)': lambda S, B, r: (f'`level = {S.level}` = 空格个数 `{len(S.z)}`：每个空格都分到了石头 → 记录答案' if S.level == len(S.z) else f'`level = {S.level}` < `{len(S.z)}`：还有空格没分配，继续'),
        'res = min': lambda S, B, r: f'这套分配的总距离 `s = {S.s}`：`res = min(res, s)`，比当前最优小就更新',
        19: '这条分配方案处理完了，返回上一层（接着回溯）',
        'for x, y in g': lambda S, B, r: (f'空格 `z[{S.level}]` 的来源都试完了，返回上一层' if (S['_inner'].get('x') is not None and B.get('_inner') and B['_inner'].get('x') == S['_inner'].get('x') and B['_inner'].get('y') == S['_inner'].get('y') and B['_inner'].get('level') == S.level) else f'为空格 `z[{S.level}]` 试一个来源：`({S.x},{S.y})`'),
        'if grid[x][y] > 1': lambda S, B, r: (f'`({S.x},{S.y})` 还剩 `{S.grid[S.x][S.y]}` 个 > 1 → 还能送出一个' if S.grid[S.x][S.y] > 1 else f'`({S.x},{S.y})` 只剩 1 个了，不能再送（否则它自己会变空）→ 换下一个来源'),
        'grid[x][y] -= 1': '从 `({x},{y})` 拿走一个石头，剩 `{grid[x][y]}`',
        's += ': '走到空格 `z[{level}]`：曼哈顿距离 `{abs(x - z[level][0]) + abs(y - z[level][1])}` → `s = {s}`',
        'dfs(level + 1': '空格 `z[{B.level}]` 已有来源，递归去处理下一个空格 `z[{B.level + 1}]`',
        's -= ': '==回溯==：撤销这一步的距离，`s` 回到 {s}',
        'grid[x][y] += 1': '==回溯==：把石头还给 `({x},{y})`，换下一个来源',
        'return res': '最少移动次数 =={ret}==',
    },
    cards=dict(
        one_liner='空格逐个挑来源：回溯所有分配，取总距离最小',
        complexity='时间最坏约 `4^5 = 1024` 种分配，可忽略；空间 `O(1)`',
        problem=['`3×3` 网格共 9 个石头，一步可把石头移到相邻格',
                 '要让每格恰好 1 个石头，求最少移动次数',
                 '示例：`[[1,3,0],[1,0,0],[1,0,3]]` → `4`；本视频：`[[2,1,0],[1,0,1],[1,2,1]]` → `3`'],
        quote='初始值为1的单元格实际上是可以直接无视的，因此在这里实际上就只需要考虑如果从初始值大于1的单元格移动石头到初始值为0的单元格。……将这两种单元格收集起来，然后暴力搜索回溯。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把格子分成两堆：0 的（要接收）和 >1 的（能送出）',
              '对每个空格，枚举从哪个 >1 的格子拿一个石头来',
              '拿之前判断 `grid[x][y] > 1`，拿走后 `-= 1`，回溯时 `+= 1`'],
        summary=['最坏 8 个 0 配 1 个来源 `1^8`，7-2 为 `2^7`，6-3 为 `3^6`，5-4 为 `4^5 = 1024`，所以不怕超时',
                 '易错：拿石头要判断 `> 1`，否则来源格自己会被掏空',
                 '`s` 加了要减、`grid` 减了要加：回溯必须恢复现场',
                 '原文用 `global res` 存答案，本视频保持原样（原文已是 Python 3 可运行写法，只删了空行末尾的空格）',
                 '对比灵神：灵神把「多余石头」按 `cnt-1` 展开后全排列；yiduobo 按空格逐个挑来源'],
    ),
)

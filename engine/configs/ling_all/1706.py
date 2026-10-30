
def _col(S):
    return S.get('cur_col')

CONFIG = dict(
    num=1706, title='球会落何处', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='拆成水平+垂直移动模拟',
    tags=[],
    code='''
class Solution:
    def findBall(self, grid: List[List[int]]) -> List[int]:
        n = len(grid[0])
        ans = [-1] * n
        for j in range(n):
            # 模拟第 j 列球的移动
            cur_col = j  # 当前列号
            for row in grid:
                d = row[cur_col]  # -1 或 1，表示左/右
                cur_col += d  # 左/右走一步
                # 如果球出界或者卡在 V 形，退出循环，否则继续循环（垂直落入下一排）
                # V 形就是 -1 的左边是 1，1 的右边是 -1，即 row[cur_col] != d
                if cur_col < 0 or cur_col == n or row[cur_col] != d:
                    break
            else:  # 没有中途 break，说明球成功到达底部
                ans[j] = cur_col
        return ans
''',
    call='Solution().findBall([[1,1,1,-1],[-1,-1,1,1],[1,1,-1,-1]])',
    expect=[1, 2, -1, -1],
    setup='',
    views=[
        dict(type='grid', var='grid', h=330, cell=90,
             cursors=[('grid.index(row)', 'cur_col', 'yellow', '球')],
             color=lambda S, i, j, v: ('blue' if v == 1 else 'pink')),
        dict(type='array', var='ans', label='ans（-1 表示卡住）', pointers={'j': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if v != -1 else None)),
        dict(type='text', size=26, fn=lambda S: (f"第 `{S['j']}` 列的球，现在在第 `{S['cur_col']}` 列" if 'cur_col' in S and 'j' in S else '')),
    ],
    watch=[('j', 'j', 'blue'), ('cur_col', 'cur_col', 'yellow'), ('d', 'd', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '箱子有 `{n}` 列，也就有 `{n}` 颗球',
        'ans = [-1]': '`ans` 先全填 `-1`：默认每颗球都卡住',
        'for j in range': '放第 `{j}` 列的球，一排一排模拟',
        'cur_col = j': '球的当前列号 `cur_col = {j}`',
        'for row in grid': '球落到新的一排',
        'd = row[cur_col]': '这一格挡板 `d = {d}`：{"==1 向右==" if d == 1 else "==-1 向左=="}',
        'cur_col += d': '先水平走一步：`cur_col` {B.cur_col} → =={cur_col}==',
        'if cur_col < 0': lambda S, B, r: (
            f'`cur_col = {S.cur_col}` 出界 → ==卡住==，break' if (S.cur_col < 0 or S.cur_col == len(S.grid[0]))
            else (f'隔壁格 `row[{S.cur_col}] = {S.row[S.cur_col]}` ≠ `d = {S.d}`：是 V 形 → ==卡住==，break' if S.row[S.cur_col] != S.d
                  else f'没出界，隔壁格 `{S.row[S.cur_col]}` 与 `d = {S.d}` 同向 → 垂直落入下一排')),
        'break': '球卡住了，不记录，`ans[{j}]` 保持 `-1`',
        'ans[j] = cur_col': '循环没有被 break：球从底部第 `{cur_col}` 列掉出 → `ans[{j}] = {cur_col}`',
        'return ans': '每颗球的结果：`{ans}`',
    },
    cards=dict(
        one_liner='把斜着走拆成先水平一步、再垂直一步',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计）',
        problem=['`m x n` 的箱子，每格有斜挡板：`1` 把球导向右，`-1` 导向左',
                 '每列顶部放一颗球，卡住（V 形或撞边）记 `-1`，否则记掉出的列号',
                 '示例：`[[1,1,1,-1],[-1,-1,1,1],[1,1,-1,-1]]`  → `[1,2,-1,-1]`'],
        quote='球是斜着移动的，不好分析。为了方便分析，我们把球的斜向移动，拆分成水平和垂直的移动。',
        quote_src='—— 灵茶山艾府题解',
        idea=['球在 `(r, c)`：`grid[r][c]` 为 `-1` 先左一步，为 `1` 先右一步',
              '卡住只有两种：水平走一步==出界==，或者隔壁格方向与 `d` 不同（V 形）',
              '没卡住就垂直落到下一排，用 `for-else` 记录最终列号'],
        summary=['时间 `O(mn)`：`n` 颗球，每颗最多走 `m` 排',
                 'V 形的判断就是 `row[cur_col] != d`，要在 `cur_col` 更新之后比较',
                 '`for-else`：只有没 break 才会进 else',
                 '出界判断要放在下标访问之前（`or` 短路）'],
    ),
)

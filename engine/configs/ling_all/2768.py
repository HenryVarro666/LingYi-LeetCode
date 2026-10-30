M, N = 3, 4
COORDS = [[0, 0], [1, 1], [0, 2]]


def _cell(S, i, j, v):
    if 's' not in S:
        return None
    black = (i, j) in S['s']
    inblk = 'i' in S and S['_line'] >= 8 and S['i'] <= i <= S['i'] + 1 and S['j'] <= j <= S['j'] + 1
    if inblk:
        return 'orange' if black else 'yellow'
    return 'purple' if black else None


CONFIG = dict(
    num=2768, title='黑格子的数目', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='只枚举含黑格的 2×2 块 + 哈希去重',
    tags=[],
    code='''
class Solution:
    def countBlackBlocks(self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
        s = set(map(tuple, coordinates))
        arr = [0] * 5
        vis = set()
        for x, y in coordinates:
            for i in range(max(x - 1, 0), min(x + 1, m - 1)):
                for j in range(max(y - 1, 0), min(y + 1, n - 1)):
                    if (i, j) not in vis:
                        vis.add((i, j))
                        cnt = ((i, j) in s) + ((i, j + 1) in s) + \\
                              ((i + 1, j) in s) + ((i + 1, j + 1) in s)
                        arr[cnt] += 1
        arr[0] = (m - 1) * (n - 1) - len(vis)
        return arr
''',
    call=f'Solution().countBlackBlocks({M}, {N}, {COORDS})',
    expect=[1, 3, 2, 0, 0],
    skip=['arr = [0]', 'vis = set()', '((i + 1, j) in s) + ((i + 1, j + 1) in s)', 'cnt = ((i, j) in s)'],
    views=[
        dict(type='grid', label='网格（紫 = 黑格；黄/橙 = 正在统计的 2×2 块）', h=330, cell=70,
             var=lambda S: [[0] * S['n'] for _ in range(S['m'])] if 'm' in S else None, values=False,
             color=_cell, cursors=[('i', 'j', 'yellow')]),
        dict(type='array', var='arr', label='arr[k]：恰含 k 个黑格的块数', h=170),
        dict(type='text', fn=lambda S: f"已统计的块 `len(vis) = {len(S['vis'])}`，总块数 `(m-1)(n-1) = {(S['m']-1)*(S['n']-1)}`" if 'vis' in S else ''),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('i', 'i'), ('j', 'j'), 'vis'],
    captions={
        's = set(map': '黑格坐标放进集合 `s`，判断某格是不是黑格 `O(1)`',
        'for x, y in coordinates': lambda S, B, r: ('黑格都处理完了' if 'x' in B and (S.x, S.y) == (B.x, B.y) and S.j == B.j
                                                    else f'取黑格 `({S.x},{S.y})`：只有包含它的块才可能有黑格'),
        'for i in range(max': lambda S, B, r: (f'黑格 `({S.x},{S.y})` 的块都看完了' if 'i' in B and S.i == B.i and 'j' in B and S.j == B.j
                                               else f'包含 `({S.x},{S.y})` 的块，左上角行号 `i` 在 `[{max(S.x-1,0)}, {min(S.x+1,S.m-1)})`（别越界）'),
        'for j in range(max': lambda S, B, r: (f'这一行的块看完了' if 'j' in B and S.j == B.j and S.i == B.i
                                               else f'左上角列号 `j` 在 `[{max(S.y-1,0)}, {min(S.y+1,S.n-1)})`，现在 `j = {S.j}`'),
        'if (i, j) not in vis': lambda S, B, r: (f'块 `({S.i},{S.j})` 还没统计过 → ==统计它==' if (S.i, S.j) not in S.vis
                                                 else f'块 `({S.i},{S.j})` 已统计过，跳过（同一块会被多个黑格碰到）'),
        'vis.add': '记下块 `({i},{j})`，以后不再重复数',
        'arr[cnt] += 1': '数块 `({i},{j})` 四个格子，查集合 `s`：有 ==`{cnt}`== 个黑格 → 恰有 `{cnt}` 个黑格的块 +1：`arr = {arr}`',
        'arr[0] =': '没统计过的块全是白块：`(m-1)(n-1) - len(vis) = {(m-1)*(n-1)} - {len(vis)}` = =={arr[0]}==',
        'return arr': '返回 `{arr}`',
    },
    cards=dict(
        one_liner='网格很大、黑格很少：只数含黑格的 2×2 块',
        complexity='时间 `O(k)`，空间 `O(k)`（k 为黑格数）',
        problem=['`m × n` 网格，`coordinates` 里的格子是黑色',
                 '2×2 的子矩阵叫块，求恰含 `0~4` 个黑格的块各有多少',
                 '示例：`m=n=3, [[0,0]]` → `[3,1,0,0,0]`；本视频用 3×4、3 个黑格'],
        quote='只需要考虑有黑色格子的子矩阵。如果 (x,y) 处有黑色格子，那么子矩阵左上角在 (x-1,y-1),(x-1,y),(x,y-1),(x,y) 都是包含这个黑色格子的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个黑格最多落在 4 个块里，枚举这 4 个块的左上角',
              '用 `vis` 记录数过的块，避免被多个黑格重复统计',
              '全白块数 = 总块数 `(m-1)(n-1)` − `len(vis)`'],
        summary=['时间 `O(k)`，与网格大小无关',
                 '左上角范围 `[max(x-1,0), min(x+1,m-1))`，防止块越界',
                 '`arr[0]` 最后用总块数减去 `len(vis)` 得到',
                 '`vis` 去重是关键：一个含 3 个黑格的块会被碰到 3 次'],
    ),
)

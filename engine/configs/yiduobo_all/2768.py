M, N = 3, 3
COORDS = [[0, 0], [1, 1]]


def _cell(S, i, j, v):
    if 'black_set' not in S:
        return None
    black = (i, j) in S['black_set']
    if 'd' in S and 'x' in S and S['_line'] >= 12 and 'dx' in S:
        blk = [(S['x'], S['y'])] + [(S['x'] + S['dx'][S['d']][k], S['y'] + S['dy'][S['d']][k]) for k in range(3)]
        if (i, j) in blk:
            return 'orange' if black else 'yellow'
    return 'purple' if black else None


CONFIG = dict(
    num=2768, title='黑格子的数目', difficulty='Medium', category='网格图',
    author='yiduobo', technique='从黑格出发数四个方向的块 · 重复次数回除',
    tags=[],
    code='''
class Solution(object):
    def countBlackBlocks(self, m, n, coordinates):
        black_set = set()
        for x, y in coordinates:
            black_set.add((x, y))

        res = [0] * 5
        dx = [[1, 0, 1], [1, 0, 1], [-1, 0, -1], [-1, 0, -1]]
        dy = [[0, 1, 1], [0, -1, -1], [0, 1, 1], [0, -1, -1]]

        for x, y in coordinates:
            for d in range(4):
                cnt = 1
                flag = True
                for index in range(3):
                    xx = x + dx[d][index]
                    yy = y + dy[d][index]
                    if xx >= 0 and xx < m and yy >= 0 and yy < n:
                        if (xx, yy) in black_set:
                            cnt += 1
                    else:
                        flag = False

                if flag:
                    res[cnt] += 1


        res[2] //= 2
        res[3] //= 3
        res[4] //= 4
        res[0] = (m - 1) * (n - 1) - res[1] - res[2] - res[3] - res[4]
        return res
''',
    call=f'Solution().countBlackBlocks({M}, {N}, {COORDS})',
    expect=[0, 3, 1, 0, 0],
    max_steps=80,
    skip=['black_set = set()', 'black_set.add', 'res = [0]', 'dx = [', 'dy = [', 'cnt = 1', 'flag = True',
          'for index in range(3)', 'xx = x + dx', 'yy = y + dy', 'else:', 'flag = False'],
    views=[
        dict(type='grid', label='网格（紫 = 黑格；黄/橙 = 当前方向下，以 (x,y) 为一角的 2×2 块）', h=330, cell=80, values=False,
             var=lambda S: [[0] * S['n'] for _ in range(S['m'])] if 'm' in S else None,
             color=_cell, cursors=[('x', 'y', 'blue')]),
        dict(type='array', var='res', label='res[k]：恰含 k 个黑格的块数（重复统计，最后回除）', h=170),
        dict(type='text', fn=lambda S: f"`d = {S['d']}`，`cnt = {S['cnt']}`，`flag = {S['flag']}`" if 'd' in S and 'cnt' in S else ''),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('d', 'd'), ('cnt', 'cnt', 'green'), ('flag', 'flag')],
    captions={
        'for d in range(4)': lambda S, B, r: ('四个方向都试完了' if 'd' in B and S.d == B.d
                                              else f'第 `{S.d}` 个方向：让 `({S.x},{S.y})` 当这个 2×2 块的 {["左上", "右上", "左下", "右下"][S.d]} 角'),
        'if xx >= 0 and xx < m': lambda S, B, r: (f'`({S.xx},{S.yy})` 在网格内' if 0 <= S.xx < S.m and 0 <= S.yy < S.n
                                                   else f'`({S.xx},{S.yy})` 出界 → 这个块不存在，`flag = False`'),
        'if (xx, yy) in black_set': lambda S, B, r: (f'`({S.xx},{S.yy})` 是黑格 → `cnt` 加 1' if (S.xx, S.yy) in S.black_set
                                                      else f'`({S.xx},{S.yy})` 是白格，不加'),
        'cnt += 1': '块里黑格数 `cnt = {cnt}`',
        'if flag': lambda S, B, r: (f'块完整，有 `{S.cnt}` 个黑格 → `res[{S.cnt}] += 1`' if S.flag else '块越界，不统计'),
        'res[cnt] += 1': '`res = {res}`（含 k 个黑格的块会被它的 k 个黑格各数一次）',
        'res[2] //= 2': '有 2 个黑格的块被数了 2 次 → 除以 2：`res[2] = {res[2]}`',
        'res[3] //= 3': '有 3 个黑格的块被数了 3 次 → 除以 3：`res[3] = {res[3]}`',
        'res[4] //= 4': '全黑的块被数了 4 次 → 除以 4：`res[4] = {res[4]}`',
        'res[0] =': '全白块 = 总块数 `(m-1)(n-1)` 减去其余：`res[0] = {res[0]}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='从每个黑格出发数块，含 k 个黑格的块被数 k 次，最后回除',
        complexity='时间 `O(k)`，空间 `O(k)`（k 为黑格数）',
        problem=['`m × n` 网格，`coordinates` 里是黑格；2×2 子矩阵叫块',
                 '求恰含 `0~4` 个黑格的块各有多少',
                 '示例：`m=n=3, [[0,0],[1,1],[0,2]]` → `[0,2,2,0,0]`；本视频用 `[[0,0],[1,1]]`'],
        quote='对于含有黑色格子的网格的计算，则可以从单个格子出发，分别处理这个网格是当前2*2网格的左上角、右上角、左下角以及右下角这四种情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['网格太大不能枚举所有块，只处理含黑格的块',
              '每个黑格当块的四个角各试一次，越界的块跳过',
              '含 2/3/4 个黑格的块分别被数 2/3/4 次，最后除回去'],
        summary=['时间 `O(k)`，与网格大小无关',
                 '`res[1]` 不用除：只含 1 个黑格的块只会被那一个黑格数到',
                 '`res[0]` 用总块数 `(m-1)(n-1)` 减去其他',
                 '原文为 Python 2 写法，`res[2] /= 2` 等三处整数除法已改为 `//=`',
                 '对比灵神：灵神用 `vis` 去重避免重复；yiduobo 允许重复，最后回除'],
    ),
)

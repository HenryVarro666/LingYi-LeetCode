CONFIG = dict(
    num=1914, title='循环轮转矩阵', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按层取出 · 位置下标平移 k % l',
    code='''
class Solution(object):
    def rotateGrid(self, grid, k):

        m = len(grid)
        n = len(grid[0])

        res = [[0] * n for _ in range(m)]

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for level in range(min(m // 2, n // 2)):
            tx = level
            bx = m - 1 - level
            ly = level
            ry = n - 1 - level

            level_list = []
            nowx = tx
            nowy = ly
            d = 0
            while True:
                level_list.append([nowx, nowy])
                if nowx == bx and nowy == ly:
                    d = 1
                elif nowx == bx and nowy == ry:
                    d = 2
                elif nowx == tx and nowy == ry:
                    d = 3
                
                nowx += dx[d]
                nowy += dy[d]
                if nowx == tx and nowy == ly:
                    break
            
            l = len(level_list)
            step = k % l
            for index in range(l):
                target = (index + step) % l
                res[level_list[target][0]][level_list[target][1]] = grid[level_list[index][0]][level_list[index][1]]

        return res
''',
    call='Solution().rotateGrid([[1,2,3,4],[5,6,7,8]], 3)',
    expect=[[4,8,7,6],[3,2,1,5]],
    views=[
        dict(type='grid', var='grid', h=220, cell=64, label='grid（黄 = 当前层）',
             cursors=[('nowx', 'nowy', 'blue', '(nowx,nowy)')],
             color=lambda S, i, j, v: ('yellow' if 'level' in S and S['level'] == min(i, j, len(S['grid']) - 1 - i, len(S['grid'][0]) - 1 - j) and not (i == S.get('nowx') and j == S.get('nowy')) else None)),
        dict(type='grid', var='res', h=220, cell=64, label='res（填入答案）',
             color=lambda S, i, j, v: 'green' if v else None),
        dict(type='text', fn=lambda S: (f"这一层 `{len(S['level_list'])}` 个格子，`step = k % l = {S['k']} % {len(S['level_list'])} = {S['step']}`" if S.get('level_list') and 'step' in S else (f"已收集 `{len(S['level_list'])}` 个坐标" if S.get('level_list') else '')), size=26),
    ],
    watch=['level', ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue'), 'd', 'l', 'step', ('index', 'index', 'orange'), 'target'],
    skip=['tx = level', 'bx = m - 1', 'ly = level', 'ry = n - 1', 'level_list = []', 'nowx = tx', 'nowy = ly', 'd = 0', 'while True', 'd = 1', 'd = 2', 'd = 3', 'nowx += dx[d]', 'dy = ['],
    max_steps=80,
    captions={
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列',
        'res = [[0]': '`res` 是答案矩阵，轮转后的值按位置填进去',
        'dx = [1': '方向：`dx, dy` 依次是下、右、上、左（`d` 为下标）',
        'for level in range': lambda S, B, r: ('所有层都填完了' if 'level' in B and B.level == S.level else f'处理第 `{S.level}` 层，四角：`({S.level},{S.level})`、`({S.m-1-S.level},{S.level})`、`({S.level},{S.n-1-S.level})`、`({S.m-1-S.level},{S.n-1-S.level})`'),
        'level_list.append': '收集坐标 `({nowx},{nowy})`，共 `{len(level_list)}` 个',
        'if nowx == bx and nowy == ly': lambda S, B, r: ('到达左下角 → 改向右走（`d = 1`）' if S.nowx == S.bx and S.nowy == S.ly else '不是左下角，方向不变'),
        'elif nowx == bx and nowy == ry': lambda S, B, r: ('到达右下角 → 改向上走（`d = 2`）' if S.nowx == S.bx and S.nowy == S.ry else '不是右下角，方向不变'),
        'elif nowx == tx and nowy == ry': lambda S, B, r: ('到达右上角 → 改向左走（`d = 3`）' if S.nowx == S.tx and S.nowy == S.ry else '不是右上角，方向不变'),
        'nowy += dy[d]': '沿方向 `d = {d}` 走一步 → `({nowx},{nowy})`',
        'if nowx == tx and nowy == ly': lambda S, B, r: ('绕回左上角：这一层收集完毕' if S.nowx == S.tx and S.nowy == S.ly else '还没回到左上角，继续走'),
        'l = len(level_list)': '这一层共 `l = {l}` 个数',
        'step = k % l': '轮转 `l` 次等于没转 → 每个数往后挪 `k % l = {k} % {l} = {step}` 个位置',
        'for index in range(l)': lambda S, B, r: ('这一层的数都挪完了' if 'index' in B and B.index == S.index else f'第 `{S.index}` 个数'),
        'target = (index + step) % l': '第 `{index}` 个数移到第 `(index + step) % l = {target}` 个位置',
        'res[level_list[target][0]]': lambda S, B, r: f'`res[{S.level_list[S.target][0]}][{S.level_list[S.target][1]}] = grid[{S.level_list[S.index][0]}][{S.level_list[S.index][1]}] = {S.grid[S.level_list[S.index][0]][S.level_list[S.index][1]]}`',
        'return res': '返回 `res`',
    },
    cards=dict(
        one_liner='一层一层拎出来，每个数往后挪 k % l 个位置再填进答案',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['矩阵由若干层组成，每次轮转层中元素取代其逆时针方向相邻元素',
                 '返回轮转 `k` 次后的矩阵（`m`、`n` 均为偶数）',
                 '本视频：`[[1,2,3,4],[5,6,7,8]]`，`k = 3`'],
        quote='最直观的做法是从外向内一层一层拎出来，轮转完之后再填充到最后答案中。设这个层中数字的个数为l，那么轮转k次之后每个数字将会往后移动k % l个位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['按左上、左下、右下、右上的顺序，用方向数组 `dx, dy` 走一圈收集坐标',
              '坐标序列是逆时针的，所以轮转就是每个下标后移 `k % l`',
              '不改原矩阵，把值写进新矩阵 `res`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（额外的 `res` 与坐标表）',
                 '层数是 `min(m//2, n//2)`；每层的左上角是 `(level, level)`',
                 '拐弯条件是到达角点：左下、右下、右上',
                 '原文为 Python 2 写法，整数除法 `m / 2`、`n / 2` 已改为 `//`'],
    ),
)

IMAGE = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]


def _nb(S, B, r):
    x, y = B.x, B.y
    m, n = B.m, B.n
    if not (0 <= x < m and 0 <= y < n):
        return f'邻居 `({x},{y})` 越界'
    c = B.image[x][y]
    if c == B.original_color:
        return f'邻居 `({x},{y})` 颜色 `{c}` 等于原色 → ==染色并入队=='
    if c == B.newColor:
        return f'邻居 `({x},{y})` 已经染成 `{c}`（不再等于原色）→ 不会重复入队'
    return f'邻居 `({x},{y})` 颜色 `{c}` ≠ 原色 `{B.original_color}` → 不扩展'


def _cell(S, i, j, v):
    if 'newColor' not in S:
        return None
    if v == S['newColor'] and IMAGE[i][j] != S['newColor']:
        return 'green'
    return None


CONFIG = dict(
    num=733, title='图像渲染', difficulty='Easy', category='图论',
    author='yiduobo', technique='BFS（数组模拟队列）',
    tags=['字节30天'],
    code='''
class Solution(object):
    def floodFill(self, image, sr, sc, newColor):
        original_color = image[sr][sc]
        if original_color == newColor:
            return image

        image[sr][sc] = newColor
        q = [[sr, sc]]
        l = 0
        r = 1
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        m = len(image)
        n = len(image[0])
        while l < r:
            now_x, now_y = q[l]
            l += 1
            for index in range(4):
                x = now_x + dx[index]
                y = now_y + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and image[x][y] == original_color:
                    image[x][y] = newColor
                    q.append([x, y])
                    r += 1

        return image
''',
    call=f'Solution().floodFill({IMAGE}, 1, 1, 2)',
    expect=[[2, 2, 2], [2, 2, 0], [2, 0, 1]],
    skip=['l = 0', 'r = 1', 'dx = [', 'dy = [', 'm = len', 'n = len', 'l += 1', 'for index in range(4)',
          'x = now_x', 'y = now_y', 'q.append', 'r += 1'],
    views=[
        dict(type='grid', var='image', label='image（绿 = 已染成新颜色；蓝框 = 出队的格子，粉框 = 正在看的邻居）', cell=96, h=380,
             color=_cell, cursors=[('now_x', 'now_y', 'blue'),
                                   ('x if _line in (21, 22) else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，l 指向下一个出队的）', cell=80, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=190),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('original_color', 'original_color'), ('newColor', 'newColor', 'green')],
    captions={
        'original_color = image[sr][sc]': '记下起点 `({sr},{sc})` 的原始颜色 `original_color = {original_color}`',
        'if original_color == newColor': lambda S, B, r: (f'原色 `{B.original_color}` ≠ 新色 `{B.newColor}`，需要渲染'
                                                          if B.original_color != B.newColor
                                                          else '原色 == 新色：什么都不用改，直接返回'),
        'image[sr][sc] = newColor': '起点先染成新颜色 `{newColor}`',
        'q = [[sr, sc]]': '起点入队：用数组当队列，`l` 是队首、`r` 是队尾（左闭右开）',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续 BFS' if B.l < B.r
                                        else f'`l == r = {B.r}`：队列空了，BFS 结束'),
        'now_x, now_y = q[l]': '出队 `({now_x},{now_y})`，依次看下、左、上、右四个邻居',
        'if x >= 0 and x < m': _nb,
        'image[x][y] = newColor': lambda S, B, r: ('==入队时就染色==：新颜色 ≠ 原色，相当于 visited 标记' if B.r == 1
                                                   else f'`image[{S.x}][{S.y}] = {S.newColor}`，`({S.x},{S.y})` 入队'),
        'return image': '渲染完成，返回 `image`',
    },
    cards=dict(
        one_liner='从起点 BFS，只扩展颜色等于原色的邻居，入队时就染色',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的图像 `image`，从像素 `(sr, sc)` 开始上色',
                 '与起点==上下左右相连==、且颜色与起点==相同==的像素都改成 `color`',
                 '示例：`[[1,1,1],[1,1,0],[1,0,1]]`，从 `(1,1)` 染成 `2`',
                 '→ `[[2,2,2],[2,2,0],[2,0,1]]`（右下角的 1 不相连，不变）'],
        quote='从(sr, sc)开始进行bfs，每次将与当前节点相邻，且==颜色等于original_color的节点加入bfs的队列中==，然后将当前节点的颜色改为目标颜色即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['BFS 的队列用数组 + 双下标 `l`、`r` 模拟',
              '邻居在界内且颜色 == 原色 → 染色、入队',
              '染过色的格子颜色变了，自然不会被再次入队'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '易错：原色 == 新色时要直接返回，否则染色不改变颜色，会无限入队',
                 '方向数组 `dx`、`dy` 统一处理四个邻居',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)

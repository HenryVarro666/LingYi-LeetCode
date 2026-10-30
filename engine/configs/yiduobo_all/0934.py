G = [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1]]


def _c(S, i, j, v):
    if v == 2:
        return 'green'
    if v == 1:
        return 'orange'
    return None


CONFIG = dict(
    num=934, title='最短的桥', difficulty='Medium', category='网格图',
    author='yiduobo', technique='两次 BFS（先染色再扩张）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def shortestBridge(self, A):

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        n = len(A)
        q = []
        for i in range(n):
            for j in range(n):
                if A[i][j] == 1:
                    q.append([i, j])
                    A[i][j] = 2
                    break
            if len(q) > 0:
                break

        l = 0
        r = 1
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < n and y >= 0 and y < n and A[x][y] == 1:
                    A[x][y] = 2
                    q.append([x, y])
                    r += 1

        l = 0
        r = len(q)
        step = 0
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < n and y >= 0 and y < n:
                        if A[x][y] == 0:
                            A[x][y] = 2
                            q.append([x, y])
                        elif A[x][y] == 1:
                            return step - 1
            
            l, r = r, len(q)
''',
    call=f'Solution().shortestBridge({G})',
    expect=3,
    skip=['dx = [', 'dy = [', 'n = len', 'q = []', 'l = 0', 'r = 1', 'l += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'for nowx, nowy in q[l : r]', 'q.append', 'r += 1', 'for i in range', 'for j in range', 'if len(q) > 0', 'break'],
    views=[
        dict(type='grid', var='A', label='A（橙 = 另一座岛 1，绿 = 已染成 2 的队列区域；蓝框 = 当前格，粉框 = 邻居）',
             cell=96, h=400, color=_c,
             cursors=[('nowx', 'nowy', 'blue'), ('x', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（第一座岛的所有格子，随后是一圈圈新染的格子）', cell=60, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=170),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('step', 'step', 'green')],
    captions={
        'A[i][j] == 1': '找第一个值为 1 的格子 `({i},{j})`，它属于其中一座岛',
        'A[i][j] = 2': '把它染成 `2`，同时放进队列 `q`：==2 表示“第一座岛”==',
        'if x >= 0 and x < n and y >= 0 and y < n and A[x][y] == 1': lambda S, B, r: (
            f'邻居 `({B.x},{B.y})` 在界内且是 1 → 同一座岛，染成 2 入队'
            if 0 <= B.x < B.n and 0 <= B.y < B.n and B.A[B.x][B.y] == 1
            else f'邻居 `({B.x},{B.y})` 越界或不是 1 → 不属于这座岛'),
        'while l < r:': lambda S, B, r: (
            f'队列区间 `[{B.l}, {B.r})` 非空，继续' if B.l < B.r else f'`l == r`：这一阶段的队列处理完了'),
        'nowx, nowy = q[l]': '取队首 `({nowx},{nowy})`，往四个方向看',
        'step += 1': '==新的一轮==：整圈往外扩一步，`step = {step}`（本轮走过 {step} 步）',
        'if A[x][y] == 0': lambda S, B, r: (
            f'邻居 `({B.x},{B.y})` 是海（0）→ 染成 2 并入队，作为下一圈' if B.A[B.x][B.y] == 0
            else f'邻居 `({B.x},{B.y})` 不是海，再看是不是另一座岛'),
        27: '邻居染成 2、入队（入队即染色，兼作 visited）',
        42: '把海染成 2：==这格就是要填的一格==',
        40: lambda S, B, r: (f'邻居 `({B.x},{B.y})` ' + ('在界内' if 0 <= B.x < B.n and 0 <= B.y < B.n else '越界，跳过')),
        'elif A[x][y] == 1': lambda S, B, r: (
            f'邻居 `({B.x},{B.y})` 是 1 → ==碰到另一座岛了=='
            if B.A[B.x][B.y] == 1 else f'邻居 `({B.x},{B.y})` 是 2，已经访问过'),
        'return step - 1': '本轮第 `{step}` 步碰到岛，其中最后一步是岛本身，所以要填的海格数 = `{step} - 1 = {ret}`',
        'l, r = r, len(q)': '下一圈：`l = {l}`，`r = {r}`',
    },
    cards=dict(
        one_liner='先把一座岛染成 2，再把它整圈整圈往外扩，碰到另一座岛为止',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`n × n` 的 0/1 矩阵里恰好有两座岛（四连通的 1）',
                 '可以把 0 翻成 1，求连接两座岛==最少要翻几个 0==',
                 '示例：`[[1,1,0,0],[1,0,0,0],[0,0,0,0],[0,0,1,1]]` → `3`'],
        quote='随便从A中找一个1，然后从这个1开始进行bfs，将这个1以及与之连通的所有1都覆盖成2……从这些点开始继续进行bfs，每一轮都往外扩展一步，那么当某一次扩展到值为1的节点时，当前轮次就是答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一次 BFS：把一座岛染成 2，队列 `q` 里正好存下它的所有格子',
              '第二次 BFS：以整座岛为多源起点，一圈圈往外扩',
              '第 `step` 圈碰到 1，说明前 `step-1` 圈填的海就是答案'],
        summary=['时间 `O(n^2)`：每个格子最多入队一次',
                 '易错：碰到岛的那一步不算填海，所以返回 `step - 1`',
                 '易错：必须把整座岛都入队，不能只用一个点作起点',
                 '本题输入会被原地改写（1 变 2），原文没有恢复'],
    ),
)

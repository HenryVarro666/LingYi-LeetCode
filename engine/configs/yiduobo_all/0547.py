PAL = ['green', 'blue', 'orange', 'purple', 'cyan', 'pink']
POS = {0: (0.10, 0.30), 1: (0.30, 0.75), 2: (0.50, 0.30), 3: (0.72, 0.75), 4: (0.90, 0.30)}
EDGES = [(0, 1), (3, 4)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '朋友关系图（同色 = 同一个圈子，白色 = 还没分圈，蓝环 = now，粉环 = 正在看的 friend）', 21, T['muted'], bold=True)
    W, H = x1 - x0 - 80, y1 - y0 - 90
    P = {k: (x0 + 40 + W * a, y0 + 56 + H * b) for k, (a, b) in POS.items()}
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 4)
    color = S.get('color') or []
    now, fr = S.get('now'), S.get('friend')
    inloop = S.get('_line') in (16, 17, 19)
    for k, (px, py) in P.items():
        c = color[k] if k < len(color) else None
        fill = T[PAL[c % len(PAL)]] if c is not None else T['panel2']
        cv.rect((px - 34, py - 34, px + 34, py + 34), fill=fill, outline=T['border'], r=34)
        cv.text((px, py), k, 34, T['bg'] if c is not None else T['muted'], anchor='mm', bold=True)
        if k == now and 'q' in S and S.get('l', 0) > 0:
            cv.rect((px - 42, py - 42, px + 42, py + 42), outline=T['blue'], width=5, r=42)
        if k == fr and inloop:
            cv.rect((px - 48, py - 48, px + 48, py + 48), outline=T['pink'], width=5, r=48)


CONFIG = dict(
    num=547, title='朋友圈', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='种子染色法 · BFS', tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def findCircleNum(self, M):

        n = len(M)
        now_color = 0
        color = [None] * n
        for index in range(n):
            if color[index] is None:
                q = [index]
                l = 0
                r = 1
                color[index] = now_color
                while l < r:
                    now = q[l]
                    l += 1
                    for friend, relation in enumerate(M[now]):
                        if relation == 1 and color[friend] is None:
                            q.append(friend)
                            color[friend] = now_color
                            r += 1
                now_color += 1
        
        return now_color
''',
    call='Solution().findCircleNum(M0)',
    setup='''
M0 = [[1,1,0,0,0],
      [1,1,0,0,0],
      [0,0,1,0,0],
      [0,0,0,1,1],
      [0,0,0,1,1]]
''',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=290),
        dict(type='array', var='color', label='color（None = 还没有圈子）', cell=100, h=170,
             color=lambda S, i, v: PAL[v % 6] if v is not None else None),
        dict(type='array', var=lambda S: S.get('q'), label='q（BFS 队列，l 指向下一个出队的）', cell=100, h=200,
             pointers={'l': 'blue'}, dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=['index', 'now', 'friend', 'now_color'],
    captions={
        'color = [None] * n': '`color[i]` 记录第 i 个人属于哪个圈子，==None 表示还没分圈==',
        'for index in range': '依次看每个人 `index = {index}`',
        'if color[index] is None': lambda S, B, r: (f'`color[{S.index}]` 还没有圈子 → 这是一个新圈子的起点（种子）' if S.color[S.index] is None
                                                  else f'`{S.index}` 已经在圈子 {S.color[S.index]} 里 → 他的朋友也都分过了，跳过'),
        'color[index] = now_color': '种子 `{index}` 染成当前圈子颜色 `{now_color}`',
        'while l < r': lambda S, B, r: ('队列里还有人，继续' if S.l < S.r else '队列空了 → 这个圈子分完了'),
        'now = q[l]': '出队：取出 `now = {now}`，去找他的朋友',
        'if relation == 1 and color[friend] is None': lambda S, B, r: (
            f'`friend={S.friend}`：是朋友且没分圈 → ==成立==，拉进当前圈子' if (S.relation == 1 and S.color[S.friend] is None)
            else (f'`friend={S.friend}`：不是朋友 → 跳过' if S.relation != 1 else f'`friend={S.friend}`：已经有圈子了 → 跳过')),
        'color[friend] = now_color': '`friend {friend}` 染成 `{now_color}`，同一个圈子',
        'now_color += 1': '这个圈子的 BFS 结束，下一个圈子编号 `{now_color}`',
        'return now_color': '圈子编号发到 `{now_color}`，==圈子总数 = {now_color}==',
    },
    max_steps=110,
    skip=['l = 0', 'r = 1', 'q.append', 'r += 1', 'l += 1'],
    cards=dict(
        one_liner='遍历每个人：没分圈就从他开始 BFS，整圈染成同色',
        complexity='时间 `O(n²)`（遍历邻接矩阵），空间 `O(n)`',
        problem=['`M[i][j] = 1` 表示第 i 个人和第 j 个人是直接朋友，朋友关系可传递',
                 '朋友的朋友也在同一个朋友圈里，求朋友圈的总数（连通块个数）',
                 '本视频：5 个人，`{0,1}`、`{2}`、`{3,4}` → `3`'],
        quote='若这个人当前不属于任何圈子，那么说明这个人的朋友也不属于任何圈子……于是可以从这个人开始执行bfs或者dfs，将这个人的朋友加入到当前这个人的圈子。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历到没有圈子的人，说明==没有任何已分圈的人认识他==，他是新圈子的种子',
              '从种子 BFS，把能传递到的朋友全部染成同一种颜色',
              '全部分完后，用掉的颜色数就是圈子数'],
        summary=['时间 `O(n²)`：每个人出队一次，扫一遍他的整行',
                 '空间 `O(n)`：`color` 和队列 `q`',
                 '队列用列表 + 头指针 `l`，不弹出元素，`r` 就是队列长度',
                 '同类题：岛屿数量（网格染色）；也可以用并查集'],
    ),
)

BLOCKED = [[0, 3], [1, 2], [2, 1], [3, 0]]
N = 6  # 只画左上角 N×N 的局部


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '真实网格 10^6×10^6，只画左上角 6×6；红 = 封锁，绿 = 已发现', 20, T['muted'], bold=True)
    if 'blocked_set' not in S:
        return
    blocked = {(k // 1000000, k % 1000000) for k in S['blocked_set']}
    used = {(k // 1000000, k % 1000000) for k in S.get('used', ())}
    src, tgt = tuple(S['source']), tuple(S['target'])
    cell = min(80, (x1 - x0 - 60) / N, (y1 - y0 - 110) / N)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * N) / 2
    sy = y0 + 56
    for i in range(N):
        for j in range(N):
            X, Y = sx + j * cell, sy + i * cell
            p = (i, j)
            fill = T['panel2']
            if p in blocked:
                fill = T['red']
            elif p in used:
                fill = T['green']
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6, outline=T['border'], width=1)
            tag = 'S' if p == src else ('T' if p == tgt else '')
            if tag:
                cv.text((X + cell / 2, Y + cell / 2), tag, int(cell * 0.45), T['bg'] if p in used or p in blocked else T['text'], anchor='mm', bold=True)
            if p == src:
                cv.rect((X, Y, X + cell, Y + cell), outline=T['cyan'], width=4, r=8)
            if p == tgt:
                cv.rect((X, Y, X + cell, Y + cell), outline=T['orange'], width=4, r=8)
    if 'nowx' in S and 'l' in S and S['l'] > 0:
        cx, cy = S['nowx'], S['nowy']
        if 0 <= cx < N and 0 <= cy < N:
            cv.rect((sx + cy * cell - 1, sy + cx * cell - 1, sx + cy * cell + cell + 1, sy + cx * cell + cell + 1), outline=T['blue'], width=5, r=8)
    cv.text((x0 + 30, sy + N * cell + 14), 'S = source（青框），T = target（橙框），蓝框 = 当前出队的格子', 20, T['muted'])


def _txt(S):
    if 'r' not in S:
        return ''
    return f"已发现 ==`{S['r']}`== 个格子（阈值 `19900`），队头 `l = {S['l']}`"


CONFIG = dict(
    num=1036, title='逃离大迷宫', difficulty='未知', category='网格图',
    author='yiduobo', technique='有限步 BFS · 双向判围',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def isEscapePossible(self, blocked, source, target):

        max_l = 19900
        blocked_set = set()
        for x, y in blocked:
            blocked_set.add(x * 1000000 + y)

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        q = [source]
        l = 0
        r = 1
        used = set()
        used.add(source[0] * 1000000 + source[1])
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < 1000000 and y >= 0 and y < 1000000 and x * 1000000 + y not in blocked_set and x * 1000000 + y not in used:
                    q.append([x, y])
                    r += 1
                    used.add(x * 1000000 + y)
                    if x == target[0] and y == target[1]:
                        return True
            
            if r > 19900:
                break
        
        if r <= 19900:
            return False
        
        q = [target]
        l = 0
        r = 1
        used = set()
        used.add(target[0] * 1000000 + target[1])
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < 1000000 and y >= 0 and y < 1000000 and x * 1000000 + y not in blocked_set and x * 1000000 + y not in used:
                    q.append([x, y])
                    r += 1
                    used.add(x * 1000000 + y)
            
            if r > 19900:
                break

        return r > 19900
''',
    call=f'Solution().isEscapePossible({BLOCKED}, [0, 0], [0, 4])',
    expect=False,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'green'), ('nowx', 'nowx'), ('nowy', 'nowy')],
    max_steps=48,
    skip=['max_l', 'blocked_set = set()', 'dx = [', 'dy = [', 'used = set()', 'used.add', 'q.append', 'r += 1', 'l += 1',
          'for index in range(4)', 'if x == target[0]', 'x = nowx', 'y = nowy', 'for x, y in blocked', 'blocked_set.add'],
    captions={
        'q = [source]': '从 ==source== 出发 BFS：队列 `q`、队头 `l`、已发现数 `r`',
        'l = 0': '`l` = 队头下标',
        'r = 1': '`r` = 已发现的格子数（含起点）',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续扩展' if B.l < B.r
                                        else f'`l == r = {B.r}`：队列空了，能到的格子一共只有 `{B.r}` 个'),
        'nowx, nowy = q[l]': '取出 `({nowx},{nowy})`，往四个方向扩展',
        'if x >= 0 and x < 1000000': lambda S, B, r: (
            f'邻居 `({B.x},{B.y})` 在界内、不是封锁格、没走过 → ==入队==（`r` 加 1），不是 target 就继续'
            if (0 <= B.x < 1000000 and 0 <= B.y < 1000000 and B.x * 1000000 + B.y not in B.blocked_set and B.x * 1000000 + B.y not in B.used)
            else f'邻居 `({B.x},{B.y})` 越界 / 被封锁 / 已经走过 → 不入队'),
        'if r > 19900': lambda S, B, r: (f'`r = {B.r}` > 19900：已发现的格子比 200 个障碍能围出的最大面积还多 → ==没被围住，停止 BFS=='
                                         if B.r > 19900 else f'`r = {B.r}` ≤ 19900：还不能下结论，继续'),
        'if r <= 19900': lambda S, B, r: ('source 所在区域 ≤ 19900，被障碍围死了，到不了 target → 返回 False' if B.r <= 19900
                                          else 'source 没被围死（超过 19900）；还要看 target 有没有被围'),
        'q = [target]': '换成从 ==target== 出发做同样的 BFS：只有 source 和 target 都没被围住，才能互相到达',
        'return r > 19900': lambda S, B, r: (f'target 这边 `r = {B.r}`，不超过 19900 → target 被围死 → 返回 =={r}==' if B.r <= 19900
                                             else 'target 也没被围住 → 返回 True'),
    },
    cards=dict(
        one_liner='障碍只有 200 个，围不住太大的区域，BFS 超过 19900 格就算逃出',
        complexity='时间 `O(max_l)`，空间 `O(max_l)`（`max_l = 19900`）',
        problem=['`10^6 × 10^6` 的网格，`blocked` 里至多 200 个封锁格',
                 '每次走上下左右，问能否从 `source` 走到 `target`（题库未给题面，按原题理解）',
                 '本视频：4 个封锁格在左上角围出一个小三角，`source` 在里面 → `false`'],
        quote='若source或target被封锁在某个封闭平面内，那么该平面最多也只有19900个格子。',
        quote_src='—— yiduobo 题解原文',
        idea=['网格太大，不能整张图搜；但 200 个障碍 + 边界最多围出 19900 格（等腰直角三角形）',
              '从 `source` 做 BFS：到 target 就 True；少于 19900 格就结束 → 被围死，False',
              '超过 19900 格 → source 没被围；再对 `target` 做同样的 BFS',
              '两边都 ==没被围住== 才返回 True'],
        summary=['时间/空间 `O(max_l)`，`max_l = 19900`（约 `200 × 199 / 2`）',
                 '用 `x * 1000000 + y` 把坐标压成一个整数放进 set',
                 '易错：只判 source 不够，target 也可能被围死（本例就是）',
                 '易错：BFS 过程中碰到 target 要立刻返回 True',
                 '演示用小例子：source 被围在小三角里，BFS 很快结束；真实数据里会一直扩展到 19900 才停',
                 '原文已是 Python 3 可运行的写法，代码未改'],
    ),
)

N_ = 6
EDGES = [[0, 1, 5], [1, 2, 3], [3, 4, 4], [4, 5, 1], [1, 4, 2]]
SRC, TGT, KK = 0, 3, 1
POS = {0: (0.08, 0.5), 1: (0.32, 0.5), 2: (0.32, 0.12), 4: (0.62, 0.5), 3: (0.9, 0.5), 5: (0.62, 0.88)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    th = S.get('mid')
    vis = S.get('vis') if th is not None else None
    fr = S.get('r') if th is not None else None
    W, H = x1 - x0 - 120, y1 - y0 - 150
    P = {k: (x0 + 60 + v[0] * W, y0 + 70 + v[1] * H) for k, v in POS.items()}
    cv.text((x0 + 18, y0 + 4), '图（绿线 = 轻边 ≤ mid，红线 = 重边 > mid；蓝 = 已到达 vis，橙框 = 下一轮候选 r）', 22, T['muted'], bold=True)
    for a, b, w in EDGES:
        heavy = th is not None and w > th
        c = T['red'] if heavy else (T['green'] if th is not None else T['dim'])
        cv.line([P[a], P[b]], c, 5)
        mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
        cv.rect((mx - 22, my - 17, mx + 22, my + 17), fill=T['panel2'], r=8)
        cv.text((mx, my), w, 26, c, anchor='mm', bold=True)
    for v, (px, py) in P.items():
        seen = vis is not None and v in vis
        cand = fr is not None and v in fr
        fill = T['blue'] if seen else T['panel2']
        out = T['orange'] if cand else (T['pink'] if v == TGT else T['border'])
        cv.rect((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=out, width=6 if (cand or v == TGT) else 2, r=32)
        cv.text((px, py), v, 32, T['bg'] if seen else T['text'], anchor='mm', bold=True)
        if v == SRC:
            cv.text((px, py - 46), '起点', 20, T['cyan'], anchor='mb', bold=True)
        if v == TGT:
            cv.text((px, py - 46), '终点', 20, T['pink'], anchor='mb', bold=True)


def _top(S):
    mid = S.get('mid')
    if mid is None:
        return f'阈值越大，重边越少 → ==二分阈值==；重边数不能超过 `k = {KK}`'
    return f'试探阈值 `mid = {mid}`：先走光轻边，再跨一条重边，最多重复 `k + 1 = {KK + 1}` 轮'


def _mid(S, B, ret):
    return f'`mid = ({S.left} + {S.right}) // 2 = {S.mid}`：权重 `> {S.mid}` 的算重边'


def _ret(S, B, ret):
    return f'`left = {S.left}` {"== ma + 1：二分到了上界外，无解 → -1" if S.left == S.ma + 1 else f"<= ma：就是最小阈值 → =={S.left}=="}'


CONFIG = dict(
    num=3924, title='有限重边的最小阈值路径', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分阈值 · 分层 BFS',
    tags=['灵神题单·二分算法', '灵神题单·图论算法', '难度分 2080'],
    code='''
class Solution(object):
    def minimumThreshold(self, n, edges, source, target, k):

        ma = 0
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))
            ma = max(ma, w)
        
        left = 0
        right = ma + 1
        while left < right:
            mid = (left + right) // 2

            q = [source]
            vis = set([source])
            head, tail = 0, 1
            r = set()
            for _ in range(k + 1):
                vis.update(r)
                r.clear()
                while head < tail:
                    for x in q[head : tail]:
                        for y, w in g[x]:
                            if y in vis:
                                continue
                            if w <= mid:
                                q.append(y)
                                vis.add(y)
                                if y in r:
                                    r.remove(y)
                            elif y not in r:
                                r.add(y)
                    
                    head, tail = tail, len(q)

                if target in vis:
                    break

                q = list(r)
                head, tail = 0, len(q)
                

            if target in vis:
                right = mid
            else:
                left = mid + 1
        
        if left == ma + 1:
            return -1
        return left
''',
    call=f'Solution().minimumThreshold({N_}, {EDGES}, {SRC}, {TGT}, {KK})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: f"本轮队列 `q = {S['q']}`，候选 `r = {sorted(S['r'])}`，已到达 `vis = {sorted(S['vis'])}`" if 'vis' in S and 'r' in S else '', size=22, h=70),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('x', 'x', 'cyan'), ('y', 'y', 'orange')],
    skip=['g[x].append', 'g[y].append', 'ma = max', 'head, tail = 0, 1', 'r = set()', 'vis = set'], max_steps=60,
    captions={
        'ma = 0': '`ma` 记最大边权：二分上界',
        'g = [[]': '邻接表 `g[x]` 存 `(邻居, 边权)`',
        'for x, y, w in edges': lambda S, B, r: (f'建图完成，最大边权 `ma = {S.ma}`' if B.get('x') == S.x and B.get('y') == S.y and B.get('w') == S.w and 'mid' not in S
                                                 else f'读入边 `{S.x} - {S.y}`（权 {S.w}）：两头加进邻接表，更新 `ma`'),
        'left = 0': '二分下界 `left = 0`',
        'right = ma + 1': '上界取 `ma + 1 = {right}`：二分停在这里就说明==无解==（兼容不连通）',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}` → 继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`：区间收缩完'),
        'mid = (left + right)': _mid,
        'q = [source]': '从起点出发做分层 BFS：`q` 是当前层的节点',
        'for _ in range(k + 1)': lambda S, B, r: (f'第 `{S._ + 1}` 轮（最多 `k + 1 = {S.k + 1}` 轮）：这一轮只走轻边' if True else ''),
        'vis.update(r)': '把上一轮收集的“跨过重边”的节点并入 `vis`',
        'r.clear()': '清空候选集 `r`，重新收集下一轮要跨过去的节点',
        'while head < tail': lambda S, B, r: (f'这一层还有节点 `q[{S.head}:{S.tail}]` 要处理' if S.head < S.tail else '轻边已经走光 → 这一轮结束'),
        'for x in q[head : tail]': lambda S, B, r: ('这一层的节点都处理完了' if B.get('x') == S.x else f'取出当前层的节点 `x = {S.x}`'),
        'for y, w in g[x]': lambda S, B, r: (f'`{S.x}` 的邻居看完了' if B.get('x') == S.x and B.get('y') == S.y
                                             else f'看 `{S.x}` 的邻居 `y = {S.y}`，边权 `w = {S.w}`'),
        'if y in vis': '`y = {y}` {"已经到达过 → continue 跳过" if y in vis else "还没到达 → 继续判断边权"}',
        'if w <= mid': '`w = {w}` {"<=" if w <= mid else ">"} `mid = {mid}`：{"轻边，可以直接走过去" if w <= mid else "重边，这一轮不能走"}',
        'q.append(y)': '轻边：`{y}` 加入本轮 BFS 队列',
        'vis.add(y)': '标记 `{y}` 已到达',
        'if y in r': '如果 `{y}` 之前被当成“跨重边候选”，现在轻边就能到，不用算重边了',
        'r.remove(y)': '把 `{y}` 从候选集 `r` 里移除',
        'elif y not in r': '重边：`{y}` 还没到达，{"先放进候选集 r" if y not in r else "已在候选集里"}',
        'r.add(y)': '`{y}` 记入候选集 `r = {sorted(r)}`（下一轮从这些点出发）',
        'head, tail = tail': '队列推进一层：`head, tail = {head}, {tail}`',
        'if target in vis': lambda S, B, r: (f'终点 `{TGT}` {"已经到达" if TGT in S.vis else "还没到"}' + ('，不必再扩展' if TGT in S.vis else '')
                                             if S._line == 38 else
                                             (f'终点 `{TGT}` {"已到达 → mid 可行，`right = mid`" if TGT in S.vis else "没到 → mid 太小，`left = mid + 1`"}')),
        'head, tail = 0, len(q)': '新一轮的队列范围 `q[0:{tail}]`',
        'q = list(r)': '候选集 `r` 变成下一轮的起点：相当于==多用一条重边==',
        'right = mid': '`right = {right}`：阈值 `mid` 可行，上界下移',
        'left = mid + 1': '`left = {left}`：阈值 `mid` 不行，下界上移',
        'if left == ma + 1': _ret,
        'return -1': '无解，返回 `-1`',
        'return left': '最小阈值 =={ret}==',
    },
    cards=dict(
        one_liner='二分阈值；判定时分层 BFS，每层多允许跨一条重边',
        complexity='时间 `O((n+m) log U · k)` 量级，空间 `O(n+m)`',
        problem=['无向带权图，找最小阈值 `threshold`，使 `source` 到 `target` 有路径，且权重 `> threshold` 的边不超过 `k` 条',
                 '找不到就返回 `-1`，`n, m <= 1000`',
                 f'本视频：`n = 6, source = 0, target = 3, k = 1` → `4`'],
        quote='阈值越大，受到权重限制的边就越少，就越容易找出可行的路径，因此在这里可以二分最终的threshold，将题目转化为判定问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['二分范围 `[0, ma + 1]`，停在 `ma + 1` 就是无解',
              '判定 `mid`：先 BFS 走光所有轻边，到不了再用一条重边跨一层',
              '用集合 `r` 记“重边一步可达、尚未到达”的点，下一轮当起点，最多 `k + 1` 轮'],
        summary=['时间约 `O((n+m) · k · log ma)`，空间 `O(n+m)`',
                 '`vis` 包含已经到达的点；候选集 `r` 要在点被轻边到达后移除',
                 '`for _ in range(k + 1)`：k 条重边对应 k+1 层 BFS',
                 '二分上界取 `ma + 1`，用返回值是否等于它来判断无解',
                 '对比灵神：灵神用 0-1 BFS 一次求最少重边数；这里按重边条数分层扩展'],
    ),
)

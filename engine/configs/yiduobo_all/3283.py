def _tbl(S):
    try:
        return [list(r) for r in S['pawn2pawn']] + [list(S['knight2pawn'])]
    except Exception:
        return [[0] * 3 for _ in range(4)]


def _fv(S):
    try:
        f = S['f']
        out = []
        for st in range(len(f[0])):
            out.append([('·' if v is None else v) for v in f[1][st]] + [('·' if v is None else v) for v in f[0][st]])
        return out
    except Exception:
        return [['·'] * 6 for _ in range(8)]


def _n(S):
    return S.get('n', 3)


def _hl(S, r, c, v):
    I = S['_inner']
    if 'now_state' not in I or 'index' not in I and 'last' not in I:
        return None
    last = I.get('last')
    idx = I.get('index')
    if S['_line'] in LINES_USE and idx is not None and r == last and c == idx:
        return 'yellow'
    return None


def _hl_f(S, r, c, v):
    I = S['_inner']
    if 'now_state' not in I:
        return None
    n = _n(S)
    if r == I['now_state']:
        col = (n if I['sign'] == 0 else 0) + I['last']
        if c == col:
            return 'yellow'
    return None


def _state(S):
    I = S['_inner']
    if 'now_state' not in I:
        return '先 BFS 出马到每个兵、兵到兵的最少步数，再做状压 DP'
    n = _n(S)
    st, last, sign = I['now_state'], I['last'], I['sign']
    eaten = [str(k) for k in range(n) if st >> k & 1]
    who = 'Alice（max）' if sign else 'Bob（min）'
    return f'已吃兵 `{{{",".join(eaten)}}}`（二进制 `{st:0{n}b}`），马停在兵{last}，轮到 =={who}=='


LINES_USE = ()

CONFIG = dict(
    num=3283, title='吃掉所有兵需要的最多移动次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='博弈 + 状压 DP · 两次 BFS 预处理',
    tags=['状压 DP', '难度分 2473'],
    code='''
class Solution(object):
    def maxMoves(self, kx, ky, positions):

        dx = [-2, -1, 1, 2, 2, 1, -1, -2]
        dy = [1, 2, 2, 1, -1, -2, -2, -1]

        def bfs(sx, sy):
            q = [[sx, sy]]
            dis = [[None] * 50 for _ in range(50)]
            dis[sx][sy] = 0

            head, tail = 0, 1
            while head < tail:
                for nowx, nowy in q[head : tail]:
                    for d in range(8):
                        x = nowx + dx[d]
                        y = nowy + dy[d]
                        if 0 <= x < 50 and 0 <= y < 50 and dis[x][y] is None:
                            dis[x][y] = dis[nowx][nowy] + 1
                            q.append([x, y])
                
                head, tail = tail, len(q)
            
            dis_list = []
            for x, y in positions:
                dis_list.append(dis[x][y])
            
            return dis_list
        
        knight2pawn = bfs(kx, ky)
        pawn2pawn = []
        for x, y in positions:
            pawn2pawn.append(bfs(x, y))
        
        n = len(positions)
        max_state = (1 << n) - 1
        f = [[[None] * n for _ in range(max_state + 1)] for _ in range(2)]

        def dfs(f, sign, now_state, last):
            if f[sign][now_state][last] is not None:
                return f[sign][now_state][last]
            if now_state == max_state:
                f[sign][now_state][last] = 0
            else:
                best = None
                for index in range(n):
                    if now_state & (1 << index) == 0:
                        nxt_state = now_state | (1 << index)
                        cost = dfs(f, 1 - sign, nxt_state, index) + pawn2pawn[last][index]
                        if best is None:
                            best = cost
                        elif sign == 0:
                            best = min(best, cost)
                        else:
                            best = max(best, cost)
                
                f[sign][now_state][last] = best
            
            return f[sign][now_state][last]

        res = 0
        for index in range(n):
            res = max(res, knight2pawn[index] + dfs(f, 0, (1 << index), index))
        
        return res
''',
    call='Solution().maxMoves(0, 2, [[1,1],[2,2],[3,3]])',
    expect=8,
    setup='''
import tracer
tracer._SKIP_NAMES.add('bfs')  # 仅演示用：BFS 有两万多次循环，不逐行追踪（代码本身不变）
''',
    skip=['dx = [', 'dy = [', 'max_state = (1', 'nxt_state =', 'best = None', 'pawn2pawn = []', 'for x, y in positions',
          'if f[sign][now_state][last] is not None', 'return f[sign][now_state][last]',
          'if best is None', 'best = cost', 'elif sign == 0', 'best = min', 'best = max', 'def bfs'],
    views=[
        dict(type='text', fn=_state, size=26, h=60),
        dict(type='table', var=_tbl, label='步数：行 = 出发点（兵 / 马），列 = 目标兵', h=260, cell=70,
             rows=lambda S: [f'兵{k}' for k in range(_n(S))] + ['马'], cols=lambda S: [f'兵{k}' for k in range(_n(S))]),
        dict(type='table', var=_fv, label='f：行 = 已吃集合，列 = 谁操作+停在哪个兵（A=Alice，B=Bob）', h=420, cell=60,
             rows=lambda S: [format(k, f'0{_n(S)}b') for k in range(1 << _n(S))],
             cols=lambda S: [f'A{k}' for k in range(_n(S))] + [f'B{k}' for k in range(_n(S))], color=_hl_f),
        dict(type='calls', h=130, hide=('f',)),
    ],
    watch=[('sign', lambda S: S['_inner'].get('sign'), 'blue'), ('now_state', lambda S: format(S['_inner']['now_state'], 'b') if 'now_state' in S['_inner'] else '', 'cyan'),
           ('last', lambda S: S['_inner'].get('last'), 'pink'), ('best', lambda S: S['_inner'].get('best'), 'green'), ('res', lambda S: S.get('res'), 'orange')],
    captions={
        'knight2pawn = bfs': '从马出发做一次 BFS，得到马到每个兵的最少步数 `knight2pawn = {knight2pawn}`',
        'pawn2pawn.append': '从第 `{len(pawn2pawn)}` 个兵出发做 BFS，得到它到每个兵的步数：`pawn2pawn[{len(pawn2pawn)-1}] = {pawn2pawn[-1]}`',
        'n = len(positions)': '预处理完毕，`pawn2pawn = {pawn2pawn}`',
        'f = [[[None]': '`f[sign][now_state][last]`：sign 是谁操作，`now_state` 是已吃的兵，`last` 是马停的兵；`None` 表示没算过',
        'if now_state == max_state': lambda S, B, r: ('兵全吃完了 → `f` = ==0==' if S['_inner']['now_state'] == S.max_state
                                                      else '还有兵没吃 → 枚举下一个要吃的兵'),
        'f[sign][now_state][last] = 0': '游戏结束：`f[{sign}][{now_state:b}][{last}] = 0`',
        'if now_state & (1 << index) == 0': lambda S, B, r: (f'兵 {S._inner["index"]} 还没吃 → 可以选它' if S['_inner']['now_state'] & (1 << S['_inner']['index']) == 0
                                                             else f'兵 {S._inner["index"]} 已吃 → 跳过'),
        'cost = dfs': '吃兵 `{B.index}`：`pawn2pawn[{B.last}][{B.index}]` = `{pawn2pawn[B.last][B.index]}` 步，加上换手后对手的最优 → `cost`',
        'f[sign][now_state][last] = best': lambda S, B, r: ('`f[{}][{:b}][{}] = {}`：'.format(S.sign, S.now_state, S.last, S.best) +
                                                           ('Alice 取各选择里的==最大== cost' if S.sign == 1 else 'Bob 取各选择里的==最小== cost')),
        'res = max(res': '第一步让 Alice 吃兵 `{index}`：`knight2pawn[{index}]` = `{knight2pawn[index]}`，加上 Bob 接手后的 `f[0][..][{index}]`，取最大',
        'return res': '答案 = =={ret}==',
    },
    max_steps=66,
    cards=dict(
        one_liner='两次 BFS 求步数，再用 (谁操作, 已吃集合, 马停哪) 做博弈 DP',
        complexity='时间 `O(nL^2 + n^2 2^n)`，空间 `O(n 2^n)`',
        problem=['50×50 棋盘上有一匹马和 ≤15 个兵，Alice、Bob 轮流选一个兵，马用最少步数吃掉它',
                 'Alice 要总步数最大，Bob 要最小，求最优策略下的总步数',
                 '示例：`kx=0, ky=2, positions=[[1,1],[2,2],[3,3]]` → `8`'],
        quote='令f[sign][now_state][last]表示当前玩家为sign，当前已经被踩掉的兵的状态表示为now_state，且马当前停留在下标为last的棋子原先的坐标上时的最优步数。',
        quote_src='—— yiduobo 题解原文',
        idea=['马的移动只影响目标兵：先从马、从每个兵各做 BFS，预处理 `knight2pawn`、`pawn2pawn`',
              '`f[sign][state][last]`：sign = 1 是 Alice 要大，sign = 0 是 Bob 要小',
              '枚举没吃的兵 index：`f[1-sign][state|(1<<index)][index] + pawn2pawn[last][index]`',
              '最外层再枚举 Alice 第一步吃谁'],
        summary=['时间 `O(nL^2 + n^2 2^n)`，L = 50；空间 `O(n 2^n)`',
                 '马吃兵途中经过别的兵不算吃，所以每段都是纯最短路',
                 'Alice 取 max，Bob 取 min；别忘了第一步的 `knight2pawn`',
                 '对比灵神：灵神用已吃兵数的奇偶判断轮到谁，yiduobo 把 sign 显式放进状态；这份原文本身已是 Python 3 可运行的写法'],
    ),
)

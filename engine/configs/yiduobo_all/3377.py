_P = [True] * 100
_P[1] = False
for _i in range(2, 100):
    if _P[_i]:
        for _j in range(_i * _i, 100, _i):
            _P[_j] = False
_P[0] = False   # check(0)：x <= 1 → 非质数，允许走
N0, M0 = 10, 12


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    dis = S.get('dis') or {}
    x = S.get('x') if 'd' in S and 'x' in S else None
    cur_y = S.get('y') if 'delta' in S and S.get('_line') in range(26, 36) else None
    cv.text((x0 + 18, y0 + 4), '数字 0~99（红 = 质数不能走，蓝 = 当前 x，绿 = 已确定 dis，黄 = 正在看的 y）', 20, T['muted'], bold=True)
    cell = min((x1 - x0 - 60) / 10, (y1 - y0 - 60) / 10)
    sx = x0 + ((x1 - x0) - cell * 10) / 2
    sy = y0 + 46
    heap_best = {}
    for it in S.get('heap', []) or []:
        c, v = it
        if v not in heap_best or c < heap_best[v]:
            heap_best[v] = c
    for v in range(100):
        r, c = divmod(v, 10)
        X, Y = sx + c * cell, sy + r * cell
        lab = None
        if v == x and v not in dis:
            fill, tc = T['blue'], T['bg']
        elif v in dis:
            fill, tc, lab = (T['blue'] if v == x else T['green']), T['bg'], dis[v]
        elif v == cur_y:
            fill, tc = T['yellow'], T['bg']
        elif _P[v]:
            fill, tc = (74, 40, 48), T['dim']
        elif v in heap_best:
            fill, tc, lab = T['orange'], T['bg'], heap_best[v]
        else:
            fill, tc = T['panel2'], T['muted']
        cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6)
        cv.text((X + cell / 2, Y + cell * (0.36 if lab is not None else 0.5)), v, int(cell * 0.38), tc, anchor='mm', bold=True, mono=True)
        if lab is not None:
            cv.text((X + cell / 2, Y + cell * 0.74), lab, int(cell * 0.26), tc, anchor='mm', mono=True)
        if v == M0:
            cv.rect((X, Y, X + cell, Y + cell), outline=T['pink'], width=4, r=8)
        if v == N0:
            cv.rect((X, Y, X + cell, Y + cell), outline=T['yellow'], width=4, r=8)


def _txt(S, B):
    if 'd' not in S:
        return f'从 `n = {N0}` 出发，目标 `m = {M0}`；每一步都不能落在质数上，代价累加每个到过的数'
    return f"当前弹出：代价 `{S['d']}`，数 `{S['x']}`；已确定 {len(S.get('dis', {}))} 个数的最短代价"


CONFIG = dict(
    num=3377, title='使两个整数相等的数位操作', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='带堆 Dijkstra · 现算邻居',
    tags=['灵神题单·图论算法', '难度分 2186'],
    code='''
class Solution(object):
    def minOperations(self, n, m):
        
        def check(x, prime):
            if x not in prime:
                if x <= 1:
                    prime[x] = False
                else:
                    prime[x] = True
                y = 2
                while y * y <= x:
                    if x % y == 0:
                        prime[x] = False
                        break
                    y += 1
            
            return not prime[x]

        prime = {}
        if not check(n, prime):
            return -1

        dis = {}
        heap = [(n, n)]
        

        while m not in dis and heap:
            d, x = heapq.heappop(heap)
            if x in dis:
                continue
            
            dis[x] = d

            tmp = x
            delta = 1
            while tmp:
                v = tmp % 10
                tmp //= 10
                if v > 0:
                    y = x - delta
                    if y not in dis and check(y, prime):
                        heapq.heappush(heap, (d + y, y))
                if v < 9:
                    y = x + delta
                    if y not in dis and check(y, prime):
                        heapq.heappush(heap, (d + y, y))
                
                delta *= 10

        return dis.get(m, -1)
''',
    call=f'Solution().minOperations({N0}, {M0})',
    expect=85,
    max_steps=68,
    skip=['if x not in prime', 'if x <= 1', 'prime[x] = False', 'prime[x] = True', 'y = 2', 'while y * y', 'if x % y',
          'break', 'y += 1', 'tmp = x', 'delta = 1', 'delta *= 10', 'def check', 'prime = {}'],
    views=[
        dict(type='text', fn=_txt, h=44, size=22),
        dict(type='custom', draw=_draw, h=540),
        dict(type='heap', var='heap', label='heap（最小堆，元素 = (已花代价, 当前数)）', h=95, fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('d', 'd', 'blue'), ('x', 'x', 'blue'), ('v', 'v'), ('y', 'y', 'yellow'), ('delta', 'delta')],
    captions={
        'if not check(n, prime)': '先判断起点：`check` 返回「不是质数」；起点是质数就 `-1`',
        'dis = {}': '`dis` 用字典：只有出过堆的数才有最短代价',
        'heap = [(n, n)]': '起点代价就是 `n` 本身，`({n}, {n})` 入堆',
        'while m not in dis': lambda S, B, r: '`m` 还没确定且堆非空，继续取最小的' if S.m not in S.dis and S.heap else '`m` 的最短代价已确定，退出循环',
        'heapq.heappop': '弹出代价最小的 `({d}, {x})`：边权都是正的，先出堆的就是最短',
        'if x in dis': lambda S, B, r: f'`{S.x}` 已在 `dis` 里：这是旧记录，==跳过==' if S.x in S.dis else f'`{S.x}` 第一次出堆',
        'continue': '不用再处理，邻居早被更小的代价展开过',
        'dis[x] = d': '确定 `dis[{x}] = {d}`：到 `{x}` 的最小代价',
        'v = tmp % 10': '取当前最低位 `v = {v}`，这一位对应的变化量 `delta = {delta}`',
        'tmp //= 10': '去掉最低位，`tmp = {tmp}`，下一轮看更高一位',
        'if v > 0': lambda S, B, r: f'这一位是 `{S.v}`，非 0 → ==可以减 1==' if S.v > 0 else '这一位是 `0`，不能减',
        'if v < 9': lambda S, B, r: f'这一位是 `{S.v}`，非 9 → ==可以加 1==' if S.v < 9 else '这一位是 `9`，不能加',
        'y = x - delta': '减 1 得到 `y = {x} - {delta}` = =={y}==',
        'y = x + delta': '加 1 得到 `y = {x} + {delta}` = =={y}==',
        'check(y, prime)': lambda S, B, r: (f'`{S.y}` 已确定过 → 不用再看' if S.y in S.dis else (f'`{S.y}` 是质数 → 不能走' if _P[S.y] else f'`{S.y}` 不是质数 → 入堆，代价 `{S.d} + {S.y}` = =={S.d + S.y}==')),
        'heapq.heappush': '`({d} + {y}, {y})` = `({d + y}, {y})` 入堆，之后可能出现更小的同一个数',
        'return not prime[x]': lambda S, B, r: f'`check({S.x})`：{"质数 → False" if _P[S.x] else "不是质数 → True"}',
        'return dis.get': '`dis.get(m, -1)`：`m` 到不了就返回 `-1`，否则就是最短代价 `{ret}`',
    },
    cards=dict(
        one_liner='非质数当点，改一位当边，边权是新数，跑 Dijkstra',
        complexity='时间 `O(M log M)`，空间 `O(M)`',
        problem=['`n`、`m` 位数相同；每次让 `n` 的某一位加 1（非 9）或减 1（非 0）',
                 '`n` 从头到尾都不能是质数，代价是路过的所有数之和',
                 '示例：`n = 10, m = 12` → `85`；到不了返回 `-1`',
                 '本视频用示例 1，所有数都落在 0~99'],
        quote='可以将每个非质数都视为图中的点，而如果x经过操作可以变为y，那么设置一条从x出发到y的边，这条边的权重就是y。接下来只需从n开始做dijkstra。',
        quote_src='—— yiduobo 题解',
        idea=['先挡特殊情况：`n` 是质数，一开始就违规 → `-1`',
              '不真的建图：对当前 `x` 逐位拆开，现算 `x±delta`，质数就丢掉',
              '`prime` 用字典记忆，每个数只判断一次素数'],
        summary=['时间 `O(M log M)`，`M = n log n`；`check` 用试除法，每个数只算一次',
                 '本视频跳过 `check` 内部的试除循环，只讲结果',
                 '易错：起点代价是 `n` 本身；`m` 是质数时永远进不了堆，最后返回 `-1`',
                 '代码原文已是 Python 3 写法，无需修改',
                 '对比灵神：他用埃氏筛预处理，yiduobo 用字典按需试除'],
    ),
)

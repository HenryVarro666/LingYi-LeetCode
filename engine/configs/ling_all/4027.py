INF = float('inf')


def _rq(S):
    r = S.get('requests')
    return [f'{a},{b}' for a, b in r] if r else None


def _fcell(S, r, c, v):
    if 'j' in S and 'i' in S and r == S['j'] and S.get('_line', 0) >= 14:
        return 'yellow' if v != INF else 'blue'
    if v == INF:
        return None
    return None


def _formula(S):
    if 'i' not in S or 'j' not in S or 't' not in S:
        return '`f[j][0]`：最后完成请求 `i`；`f[j][1]`：最后完成请求 `j`（已完成 `[1,i]` 与 `[j+1,m-2]`）'
    r = S['requests']
    return f'当前请求 `[到达={S["t"]}, 楼层={S["x"]}]`：到楼层不能早于到达时间 → `max(…, t)`'


CONFIG = dict(
    num=4027, title='电梯请求 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP · 逆过程（到达时间变截止时间）',
    tags=['区间 DP', '状压 DP'],
    code='''
class Solution:
    def elevatorRequests(self, n: int, start: int, requests: list[list[int]]) -> int:
        requests += [[0, -1], [0, n]]  # 插入两个哨兵
        requests.sort(key=lambda r: r[1])  # 按楼层排序
        m = len(requests)  # 不含哨兵的下标范围是 [1, m-2]
        f = [[inf, inf] for _ in range(m)]

        for i in range(1, m - 1):
            t, x = requests[i]
            for j in range(m - 2, i - 1, -1):
                t2, y = requests[j]
                if i == 1 and j == m - 2:  # 当前请求是第一个请求
                    # 从 start 到当前楼层
                    f[j][0] = max(abs(x - start), t)
                    f[j][1] = max(abs(y - start), t2)
                    continue
                f[j][1] = min(max(f[j][0] + y - requests[i - 1][1], t2),  # 从 floor[i-1] 到当前楼层
                              max(f[j + 1][1] + requests[j + 1][1] - y, t2))  # 从 floor[j+1] 到当前楼层
                f[j][0] = min(max(f[j][0] + x - requests[i - 1][1], t),  # 从 floor[i-1] 到当前楼层
                              max(f[j + 1][1] + requests[j + 1][1] - x, t))  # 从 floor[j+1] 到当前楼层

        # 枚举最后一个完成的请求
        return min(f[i][0] for i in range(1, m - 1))
''',
    call='Solution().elevatorRequests(7, 3, [[0, 5], [0, 1], [6, 3]])',
    expect=8,
    skip=['for _ in range', 'for j in range', 'max(f[j + 1][1] + requests[j + 1][1] - y, t2))',
          'max(f[j + 1][1] + requests[j + 1][1] - x, t))', 'continue', 't2, y = requests[j]'],
    views=[
        dict(type='array', var=_rq, label='requests 按楼层排序：到达,楼层（首尾是哨兵）', h=250, cell=100,
             pointers={'i': 'blue', 'j': 'pink'},
             dim=lambda S, k, v: k in (0, len(S['requests']) - 1)),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[j] = [最后完成 i, 最后完成 j]（黄 = 当前 j 行）', h=260, cell=56,
             rows=lambda S: [f'j={k}' for k in range(len(S['f']))], cols=['i', 'j'], color=_fcell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('t', 't', 'yellow'), ('x', 'x', 'green')],
    captions={
        'requests += ': '插入两个哨兵楼层 `-1` 和 `n`，下面就不用判断越界了',
        'requests.sort': '按楼层排序：`{requests}`。逆着看，已完成的请求是一段连续的楼层区间',
        'm = len': '`m = {m}`，真实请求的下标范围是 `[1, {m-2}]`',
        'f = [[inf': '`f[j]` 保存两个值：电梯停在区间左端 `i` / 右端 `j` 时的最短完成时间',
        'return min': '最后完成的请求可以是任意一个，取 `f[i][0]` 的最小 =={ret}==',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：当前请求是 `[到达 {S.requests[S.i][0]}, 楼层 {S.requests[S.i][1]}]`，==i 从小到大==（左端往外扩）' if S.get('i') != B.get('i') else '所有 i 都算完了'),
        'if i == 1 and j == m - 2': lambda S, B, r: ('`i = 1` 且 `j = m-2`：当前请求是==第一个被处理的==' if (S.i == 1 and S.j == S.m - 2) else f'`i = {S.i}, j = {S.j}`：不是第一个请求，要从相邻请求转移'),
        'f[j][0] = max(abs': '第一个请求：从 `start` 走到楼层 `{x}`，到了也不能早于 `{t}` → `max(|{x}−{start}|, {t})` = =={f[j][0]}==',
        'f[j][1] = max(abs': '同理停在 `j` 端：`max(|{y}−{start}|, {t2})` = =={f[j][1]}==',
        'f[j][1] = min(': lambda S, B, r: (f'`f[{S.j}][1]` 取小 → =={S.f[S.j][1]}==' if S.f[S.j][1] != B.f[S.j][1] else f'完成 j（楼层 {S.y}，到达 {S.t2}）：从 i-1 来 `max({B.f[S.j][0]} + {S.y - S.requests[S.i-1][1]}, {S.t2})` = {max(B.f[S.j][0] + S.y - S.requests[S.i-1][1], S.t2)}；从 j+1 来 `max({B.f[S.j+1][1]} + {S.requests[S.j+1][1] - S.y}, {S.t2})` = {max(B.f[S.j+1][1] + S.requests[S.j+1][1] - S.y, S.t2)}；==取小=='),
        'f[j][0] = min(': lambda S, B, r: (f'`f[{S.j}][0]` 取小 → =={S.f[S.j][0]}==' if S.f[S.j][0] != B.f[S.j][0] else f'完成 i（楼层 {S.x}，到达 {S.t}）：从 i-1 来 `max({B.f[S.j][0]} + {S.x - S.requests[S.i-1][1]}, {S.t})` = {max(B.f[S.j][0] + S.x - S.requests[S.i-1][1], S.t)}；从 j+1 来 `max({B.f[S.j+1][1]} + {S.requests[S.j+1][1] - S.x}, {S.t})` = {max(B.f[S.j+1][1] + S.requests[S.j+1][1] - S.x, S.t)}；==取小=='),
    },
    cards=dict(
        one_liner='倒着看：到达时间变成截止时间，已完成的请求是连续区间',
        complexity='时间 `O(m^2)`，空间 `O(m)`',
        problem=['电梯在 `start`，每秒可上、下一层或停留；请求 `[arrival, floor]` 到达后，电梯在该楼层就立即处理',
                 '求处理完所有请求的==最短时间==，请求最多 16 个',
                 '示例：`n=7, start=3, requests=[[0,5],[0,1],[6,3]]` → `8`'],
        quote='设当前请求的发起时间为 t，楼层为 x。枚举上一个完成的请求是 i-1 还是 j+1：……加上从 floor[i-1] 到当前楼层 x 的距离，再与 t 取最大值。',
        quote_src='—— 灵茶山艾府题解（方法二：区间 DP）',
        idea=['逆过程：请求的「到达时间」变成「截止时间」，路过某层就能顺带完成它',
              '于是逆过程已完成的请求在楼层排序后是连续区间，和 4023 一样往外扩',
              '每次转移取 `max(…, t)`：到得早也得等到请求出现；方法一是状压 DP（`O(m^2 2^m)`）'],
        summary=['时间 `O(m^2)`，空间 `O(m)`；题解方法一用状压 DP / 最短路',
                 '易错：`start` 不进数组；哨兵是 `[0, -1]` 和 `[0, n]`，到达时间填 0',
                 '`max(…, t)`：到得比请求早要原地等，所以完成时间不能早于 `t`',
                 '题解同时给了记忆化与二维递推，这里演示最后的空间优化写法',
                 '同类：4023 电梯请求 II（区间 DP）、旅行商 / 排列型状压 DP'],
    ),
)

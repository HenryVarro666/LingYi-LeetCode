INF = float('inf')


def _ts(mask, T=2):
    s = [str(t + 1) for t in range(T) if mask >> t & 1]
    return '{' + ','.join(s) + '}' if s else '{}'


def _fv(v):
    return '∞' if v == INF else str(v)


def _grid(S):
    rain, T = S.get('rain'), 2
    if not rain:
        return [[0]]
    return [[rain[p] >> t & 1 for p in range(len(rain))] for t in range(T)]


def _top(S):
    if 'i' in S and 'j' in S and S['_line'] >= 22:
        i, j = S['i'], S['j']
        s = f'第 `{i}` 个舱室：与第 `{i + 1}` 个联合的时刻集合 `j = {_ts(j)}`'
        if 'pre' in S and S['_line'] >= 24:
            s += f'；第 `{i - 1}` 个的联合集合 `pre = {_ts(S["pre"])}`'
        return s
    return '`f[i][j]`：前 `i` 个舱室，第 `i` 个与第 `i+1` 个在时刻集合 `j` 联合，最少能量'


def _fcolor(S, r, c, v):
    if 'i' not in S or 'j' not in S or S['_line'] < 22:
        return None
    if (r, c) == (S['i'], S['j']):
        return 'yellow'
    if 'pre' in S and S['_line'] >= 24 and (r, c) == (S['i'] - 1, S['pre']):
        return 'blue'
    return None


def _cost(S, B, r):
    i, j, pre, mask = S.i, S.j, S.pre, S.mask
    k = (mask ^ pre) & S.rain[i]
    return f'`pre={_ts(pre)}`：`f[{i-1}][{pre}]`={_fv(S.f[i-1][pre])} + `union` {S.union[j]} + `single` {S.single[k]} = =={_fv(S.cost)}=='


CONFIG = dict(
    num='LCP 53', title='守护太空城', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状压 DP · 联合屏障时间点集合',
    tags=['灵神题单'],
    code='''
class Solution:
    def defendSpaceCity(self, time: List[int], position: List[int]) -> int:
        n, m = max(position), 1 << max(time)
        rain = [0] * (n + 1)
        for t, p in zip(time, position):
            rain[p] |= 1 << (t - 1)

        union = [0] * m
        single = [0] * m
        for i in range(1, m):
            lb = i & -i
            j = i ^ lb
            lb2 = j & -j
            union[i] = union[j] + (1 if lb == (lb2 >> 1) else 3)  # lb == (lb2 >> 1) 表示两个时间点相邻
            single[i] = single[j] + (1 if lb == (lb2 >> 1) else 2)  # 递推

        f = [[inf] * m for _ in range(n + 1)]
        for j in range(m):
            f[0][j] = union[j] + single[((m - 1) ^ j) & rain[0]]
        for i in range(1, n + 1):
            for j in range(m):
                pre = mask = (m - 1) ^ j
                while True:  # 枚举 j 的补集 mask 中的子集 pre
                    cost = f[i - 1][pre] + union[j] + single[(mask ^ pre) & rain[i]]
                    f[i][j] = min(f[i][j], cost)
                    if pre == 0:
                        break
                    pre = (pre - 1) & mask
        return f[n][0]
''',
    call='Solution().defendSpaceCity([1,1,2,2], [1,2,1,2])',
    expect=4,
    skip=['for t, p in zip', 'for i in range(1, m)', 'lb = i', 'j = i ^ lb', 'lb2 =', 'for j in range(m)', 'for i in range(1, n + 1)',
          'while True', 'f[i][j] = min', 'if pre == 0', 'break', 'pre = (pre - 1)', 'n, m =', 'rain = [0]', 'union = [0]', 'single = [0]',
          'f[0][j] ='],
    max_steps=70,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='table', var=_grid, label='陨石雨 rain（行 = 时刻 1,2；列 = 舱室 0,1,2；1 = 该时刻该舱室被击中）', h=200, cell=64,
             rows=['t1', 't2'], cols=['0', '1', '2'],
             color=lambda S, r, c, v: 'orange' if v else None),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 来源 f[i-1][pre]）', h=260, cell=64,
             rows=['i=0', 'i=1', 'i=2'], cols=['j=0', 'j=1', 'j=2', 'j=3'], color=_fcolor),
        dict(type='array', var='union', label='union[j]：联合屏障集合恰好为 j 的能量', h=150, cell=60),
        dict(type='array', var='single', label='single[j]：单独屏障集合恰好为 j 的能量', h=150, cell=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('pre', 'pre', 'green'), ('cost', 'cost', 'yellow')],
    captions={
        'rain[p] |=': '舱室 `{p}` 时刻 `{t}` 被击中：`rain[{p}] = {rain[p]}`',
        'union[i] =': lambda S, B, r: f'`union[{S.i}]`：时刻 {_ts(S.i)} 开联合屏障 = `{S.union[S.i]}`（相邻续 1，否则重开 3）',
        'single[i] =': lambda S, B, r: f'`single[{S.i}]`：时刻 {_ts(S.i)} 开单独屏障 = `{S.single[S.i]}`（相邻续 1，否则重开 2）',
        'f = [[inf]': '`f[i][j]` 先全设无穷',
        'pre = mask': lambda S, B, r: f'`j={_ts(S.j)}`，补集 `mask={_ts(S.mask)}`：枚举子集 `pre`（与 `j` 不相交）',
        'cost =': _cost,
        'return': '最后舱室无需向右联合：答案 `f[{n}][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='按舱室从左到右 DP，状态记「哪些时刻与右边联合」',
        complexity='时间 `O(n·3^m)`，空间 `O(n·2^m)`',
        problem=['舱室 `0~N` 排成一排，陨石在 `time[i]` 时刻击中 `position[i]`；单舱 2、相邻两舱联合 3，多维持一时刻各 1',
                 '同一时间一个舱室只能被一个屏障覆盖，求守住所有陨石的最少能量',
                 '示例：`time=[1,1,1,2,2,3,5], position=[1,2,3,1,2,1,3]` → `9`',
                 '本视频：`time=[1,1,2,2], position=[1,2,1,2]` → `4`'],
        quote='枚举第 i-1 个舱室在哪些时间点（记作 pre 集合）开启了联合屏障，这会对第 i 个舱室产生如下影响（限制）：……将「开启联合屏障的时间点集合」当作状态中的一个维度。',
        quote_src='—— 灵茶山艾府题解（提示 3、提示 4）',
        idea=['`f[i][j]`：考虑前 `i` 个舱室，第 `i` 与第 `i+1` 个联合屏障的时刻集合为 `j` 的最小能量',
              '转移枚举上一个舱室的联合集合 `pre`，要求 `pre ∩ j = ∅`',
              '既不在 `pre` 也不在 `j` 且被击中的时刻，必须开单独屏障；`union`、`single` 预处理成数组'],
        summary=['时间 `O(n·3^m)`：每个 `j` 枚举补集的子集，合起来是 `3^m`',
                 '`union` / `single` 靠最低位递推：相邻时刻续费 1，否则重开（联合 3 / 单独 2）',
                 '`n = max(position)`，答案取 `f[n][0]`：最后一个舱室无需向右联合',
                 '易错：`pre` 与 `j` 必须不相交，同一时刻一个舱室不能被两个屏障覆盖'],
    ),
)

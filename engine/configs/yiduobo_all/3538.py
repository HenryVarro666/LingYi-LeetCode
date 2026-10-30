def _tbl(S):
    f = S.get('f')
    if f is None:
        return None
    return [[v for row in fj for v in row] for fj in f]


def _cols(S):
    k = S['k']
    return [f'{a},{b}' for a in range(k + 1) for b in range(k + 1)]


def _rows(S):
    return [f'{i}' for i in range(S['n'])]


def _color(S, r, c, v):
    if 'pre_last_merge' not in S or 'last_merge' not in S:
        return None
    k = S['k']
    if (r, c) == (S['index'], S['merge_time'] * (k + 1) + S['last_merge']):
        return 'yellow'
    if (r, c) == (S['pre_index'], S['pre_merge_time'] * (k + 1) + S['pre_last_merge']):
        return 'blue'
    return None


def _w0(S):
    if 'pre_last_merge' in S and 'pre_index' in S:
        return S['pre_index'] - S['pre_last_merge']
    return None


def _cap_cost(S, B, ret):
    pi, plm = S.pre_index, S.pre_last_merge
    seg = S.st[pi + 1] - S.st[pi - plm]
    dist = S.position[S.index] - S.position[pi]
    base = S.f[pi][S.pre_merge_time][plm]
    return (f'上一段终点 `{pi}`（往前合并了 `{plm}` 次）：系数 = `time[{pi - plm}..{pi}]` 之和 `{seg}`，'
            f'距离 `{dist}`；总 = `{base}` + `{dist}×{seg}` = =={S.cost}==')


def _cap_upd(S, B, ret):
    return (f'`f[{S.index}][{S.merge_time}][{S.last_merge}]` 更新为 =={S.f[S.index][S.merge_time][S.last_merge]}=='
            '（更小，或第一个可行值）')


CONFIG = dict(
    num=3538, title='合并得到最小旅行时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='三维 DP · 记下最后一段合并了几次',
    tags=['灵神题单·动态规划', '难度分 2461'],
    code='''
class Solution(object):
    def minTravelTime(self, l, n, k, position, time):

        intervals = [position[index] - position[index - 1] for index in range(1, n)]
        f = [[[None] * (k + 1) for _ in range(k + 1)] for _ in range(n)]
        f[0][0][0] = 0

        st = [0]
        for t in time:
            st.append(st[-1] + t)

        for index in range(1, n):
            for merge_time in range(min(k + 1, index)):
                for last_merge in range(merge_time + 1):
                    pre_index = index - last_merge - 1
                    pre_merge_time = merge_time - last_merge
                    for pre_last_merge in range(pre_merge_time + 1):
                        if f[pre_index][pre_merge_time][pre_last_merge] is not None:
                            cost = f[pre_index][pre_merge_time][pre_last_merge] + (position[index] - position[pre_index]) * (st[pre_index + 1] - st[pre_index - pre_last_merge])
                            if f[index][merge_time][last_merge] is None or f[index][merge_time][last_merge] > cost:
                                f[index][merge_time][last_merge] = cost

        res = None
        for last_merge in range(k + 1):
            if f[-1][-1][last_merge] is not None and (res is None or res > f[-1][-1][last_merge]):
                res = f[-1][-1][last_merge]
        return res
''',
    call='Solution().minTravelTime(10, 4, 1, [0, 3, 8, 10], [5, 8, 3, 6])',
    expect=62,
    views=[
        dict(type='text', fn=lambda S: '`f[index][merge][last]`：走到路标 `index`，共合并 `merge` 次，其中最后一段合并了 `last` 次', size=21, h=50),
        dict(type='array', var='time', label='time（蓝框 = 上一段）', window=(_w0, 'pre_index'), h=125, cell=70),
        dict(type='array', var='position', label='position', pointers={'pre_index': 'blue', 'index': 'pink'}, h=185, cell=70),
        dict(type='table', var=_tbl, label='f（行 = index，列 = merge,last；· 不可达）', cols=_cols, rows=_rows, color=_color, h=290, cell=70),
    ],
    watch=[('index', 'index', 'pink'), 'merge_time', 'last_merge', ('pre_index', 'pre_index', 'blue'), 'pre_last_merge', 'cost'],
    skip=[4, 8, 9, 12, 13, 14, 15, 16, 17, 18, 23, 24, 25],
    captions={
        5: '建 `f[index][merge_time][last_merge]`，`None` 表示不可达',
        6: '起点：在路标 0，没合并过 → `f[0][0][0] = 0`',
        10: '前缀和 `st = {st}`：段 `[a, b]` 的时间和 = `st[b+1] − st[a]`',
        19: _cap_cost,
        20: lambda S, B, r: (f'当前 `f[{S.index}][{S.merge_time}][{S.last_merge}]` = `{S.f[S.index][S.merge_time][S.last_merge]}`，'
                             f'候选 `{S.cost}`：' + ('还没有值 → 采用候选' if S.f[S.index][S.merge_time][S.last_merge] is None
                                              else ('候选更小 → 更新' if S.f[S.index][S.merge_time][S.last_merge] > S.cost else '候选不更小 → 保持'))),
        21: _cap_upd,
        26: '`f[n−1][k][{last_merge}]` = `{f[-1][-1][last_merge]}` 比当前 `res` 更优 → `res` = =={res}==',
        27: '终点、恰好合并 `k` 次，`last_merge` 取最小的那个 → =={ret}==',
    },
    cards=dict(
        one_liner='状态里多记一维：最后一段往前合并了几次',
        complexity='时间 `O(n·k³)`，空间 `O(n·k²)`',
        problem=['直路上有 `n` 个路标 `position`，`time[i]` 是从 `position[i]` 往后每公里的时间',
                 '要恰好合并 `k` 次：删掉一个中间路标，把它的 time 加到下一个路标上',
                 '示例：`position=[0,3,8,10], time=[5,8,3,6], k=1` → `62`'],
        quote='因此如果不清楚起点坐标往前合并了多少次，就无法确定其对应的time值，也就无法计算转移的代价。不过好在本题的数据规模不大，直接将需要的东西往里加就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['常规状态 `f[index][merge_time]` 不够：一段路的时间系数取决于==起点==，而状态只记了终点',
              '所以加一维 `last_merge`：终点往前合并了几次，起点 `pre_index = index − last_merge − 1`',
              '再枚举上一段自己合并了几次 `pre_last_merge`，用前缀和 `st` 算它的时间系数',
              '代价 = 上一状态 + 距离差 × 上一段的时间和'],
        summary=['时间 `O(n·k³)`，空间 `O(n·k²)`，数据范围小所以够用',
                 '`merge_time` 上限取 `min(k, index−1)`，自然避免越界',
                 '`None` 表示不可达，转移前要判断；答案是 `f[n−1][k]` 中所有 `last_merge` 的最小值',
                 '原文是 Python 2 风格的类写法，本题无需改动；对比灵神：灵神用子数组长度 `sz` 倒着转移'],
    ),
)

ROBOT = [0, 4, 6]
FACTORY = [[2, 2], [6, 2]]


def _tbl(S):
    if 'f' not in S:
        return None
    return [['—' if x is None else x for x in row] for row in S['f']]


def _col(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    k = S.get('k')
    if S.get('_line') in (29, 30) and k is not None and (r, c) == (i - k, j - 1):
        return 'green'
    if S.get('_line') in (23, 24) and (r, c) == (i, j - 1):
        return 'blue'
    return None


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'robot' not in S:
        return '`f[i][j]` = 前 `i` 个机器人送到前 `j` 个工厂的最小总距离（— = 修不完）'
    p, lim = S['factory'][j - 1]
    return f'算 `f[{i}][{j}]`：工厂 {j} 在 `x={p}`，上限 `{lim}`'


def _cmp(S):
    i, j, k, cost = S.i, S.j, S.k, S.cost
    prev = S.f[i - k][j - 1]
    cur = S.f[i][j]
    if prev is None:
        return f'`f[{i-k}][{j-1}]` 是 None：前 {i-k} 个机器人没法被前 {j-1} 个工厂修完 → 这种分法不行'
    if cur is None or cur > prev + cost:
        return f'`{prev} + {cost} = {prev + cost}` 比当前 `{_ic(cur)}` 更小 → ==更新=='
    return f'`{prev} + {cost} = {prev + cost}` 不比当前 `{cur}` 小 → 不更新'


def _ic(x):
    return '—' if x is None else x


CONFIG = dict(
    num=2463, title='最小移动总距离', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='划分型 DP · 逐个累加距离',
    tags=['图论算法', '动态规划', '难度分 2454'],
    code='''
class Solution(object):
    def minimumTotalDistance(self, robot, factory):

        m = len(robot)
        n = len(factory)

        f = [[None] * (n + 1) for _ in range(m + 1)]
        for j in range(n + 1):
            f[0][j] = 0

        robot.sort()
        factory.sort(key=lambda d:d[0])

        s = [0]
        for pos, limit in factory:
            s.append(s[-1] + limit)
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[j] < i:
                    continue
                
                if f[i][j - 1] is not None:
                    f[i][j] = f[i][j - 1]
                
                cost = 0
                for k in range(1, min(i, factory[j - 1][1]) + 1):
                    cost += abs(robot[i - k] - factory[j - 1][0])
                    if f[i - k][j - 1] is not None and (f[i][j] is None or f[i][j] > f[i - k][j - 1] + cost):
                        f[i][j] = f[i - k][j - 1] + cost
        
        return f[-1][-1]
''',
    call=f'Solution().minimumTotalDistance({ROBOT}, {FACTORY})',
    expect=4,
    skip=['m = len', 'n = len', 'for j in range(n + 1)', 'f[0][j] = 0', 's = [0]', 'for pos, limit', 's.append', 'robot.sort', 'factory.sort'],
    views=[
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='table', var=_tbl, label='f[i][j]（黄 = 正在算，蓝 = 工厂 j 不用，绿 = 依赖的格子）', h=360, cell=100,
             rows=lambda S: [f'i={k}' for k in range(len(ROBOT) + 1)],
             cols=lambda S: [f'j={k}' for k in range(len(FACTORY) + 1)], color=_col),
        dict(type='array', var=lambda S: S['robot'] if 'robot' in S else None, label='robot（已排序；蓝 = robot[i−k]，正被送去工厂 j）', h=190, cell=90,
             color=lambda S, idx, v: 'blue' if S.get('k') is not None and S.get('i') is not None and idx == S['i'] - S['k'] and S.get('_line') in (28, 29, 30) else None),
    ],
    watch=['i', 'j', 'k', ('cost', 'cost', 'yellow'), ('s', 's')],
    captions={
        'f = [[None]': '`f[i][j]`：前 `i` 个机器人送到前 `j` 个工厂；`None` 表示修不完；`f[0][j] = 0`（没有机器人，不用移动）',
        'for i in range(1, m + 1)': lambda S, B, r: (f'`i = {S.i}`：现在要安排前 `{S.i}` 个机器人' if S.i != B.get('i') else '所有 `i` 都算完了'),
        'for j in range(1, n + 1)': lambda S, B, r: (f'考虑前 `{S.j}` 个工厂' if S.j != B.get('j') or S.i != B.get('i') else f'`i = {S.i}` 的所有工厂都算完了'),
        'if s[j] < i': lambda S, B, r: (f'前 `{S.j}` 个工厂总上限 `s[{S.j}] = {S.s[S.j]}` < `{S.i}` 个机器人 → ==肯定修不完==，留 None'
                                         if S.s[S.j] < S.i else f'前 `{S.j}` 个工厂总上限 `{S.s[S.j]}` ≥ `{S.i}`，有可能修完'),
        'continue': '跳过这个状态',
        'if f[i][j - 1] is not None': lambda S, B, r: ('情况 1：前 `j-1` 个工厂就够，工厂 `{}` 一个都不用'.format(S.j) if S.f[S.i][S.j - 1] is not None
                                                        else '前 `j-1` 个工厂修不完 → 工厂 `{}` 必须出力'.format(S.j)),
        'f[i][j] = f[i][j - 1]': '`f[{i}][{j}] = f[{i}][{j-1}] = {f[i][j]}`',
        'cost = 0': '情况 2：把最后 `k` 个机器人送到工厂 `{j}`，`cost` 累计它们的距离',
        'for k in range': lambda S, B, r: (f'`k = {S.k}`：最后 `{S.k}` 个机器人去工厂 `{S.j}`（不超过上限 `{S.factory[S.j-1][1]}`）' if S.k != B.get('k') or S.cost == 0
                                           else f'`k` 到上限了，工厂 `{S.j}` 的方案试完'),
        'cost += abs': '`cost` 只需加上新增的 `|robot[{i-k}] − {factory[j-1][0]}|` → `{cost}`（复用上一轮的和）',
        'if f[i - k][j - 1] is not None and': lambda S, B, r: (
            _cmp(S)),
        'f[i][j] = f[i - k][j - 1] + cost': '`f[{i}][{j}] = f[{i-k}][{j-1}] + {cost}` = =={f[i][j]}==',
        'return f[-1][-1]': '`f[{m}][{n}]` = =={ret}==：全部机器人送到全部工厂的最小总距离',
    },
    cards=dict(
        one_liner='f[i][j]：最后几个机器人给最后一个工厂，距离边枚举边累加',
        complexity='时间 `O(m·n·limit)`，空间 `O(m·n)`',
        problem=['X 轴上有机器人 `robot` 与工厂 `[位置, 修理上限]`',
                 '每个机器人被某个工厂修好，求移动总距离的最小值',
                 '示例：`robot=[0,4,6]`，`factory=[[2,2],[6,2]]` → `4`'],
        quote='由于机器人不会出现中途的相遇，因此只能安排前i个机器人中的最后几个到第j个工厂。',
        quote_src='—— yiduobo 题解原文',
        idea=['机器人若中途相遇，可互换目的地，所以最终分配==不交叉==',
              '`f[i][j]`：要么工厂 `j` 不用；要么最后 `k` 个机器人去它那里（`k ≤ limit`）',
              '枚举 `k` 时距离和在上一轮基础上加一项，转移不用再套循环'],
        summary=['时间 `O(m·n·limit)`，空间 `O(m·n)`（原文提到转移还可再优化）',
                 '`None` 表示无法修完：用 `s[j]`（前 j 个工厂总上限）提前剪掉',
                 '`f[0][j] = 0`：没有机器人不需要移动',
                 '对比灵神：他把转移看成滑动窗口最小值，用单调队列优化',
                 '原文为 Python 2 风格，代码未改，可直接在 Python 3 运行'],
    ),
)

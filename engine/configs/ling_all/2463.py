ROBOT = [0, 4, 6]
FACTORY = [[2, 2], [6, 2]]


def _f(S):
    if 'f' not in S:
        return None
    return ['∞' if x == inf else x for x in S['f']]


def _i(x):
    return '∞' if x == inf else x


def _fmt(x):
    j, v = x
    return f'f[{j}]−s={"∞" if v == inf else v}'


def _txt(S):
    if 'position' not in S:
        return '`f[j]` = 当前这些工厂修好前 `j` 个机器人的最小总距离；工厂按位置从左到右一个个加进来'
    pos, lim = S['position'], S['limit']
    if 'j' in S and 'dis_sum' in S:
        j = S['j']
        return f'工厂 `x={pos}`，上限 {lim}：`f[j] = dis_sum + 窗口最小值`'
    return f'工厂 `x={pos}`，最多修 `{lim}` 个'


def _enq(S, B, r):
    v = S.v
    return f'`v = f[{S.j}] − dis_sum` = {"∞" if v == inf else v}：先入队，因为 `f[j]` 的窗口包含 `k = j`'


CONFIG = dict(
    num=2463, title='最小移动总距离', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 单调队列优化',
    tags=['图论算法', '动态规划', '难度分 2454'],
    code='''
class Solution:
    def minimumTotalDistance(self, robot: List[int], factory: List[List[int]]) -> int:
        factory.sort(key=lambda f: f[0])
        robot.sort()

        m = len(robot)
        f = [0] + [inf] * m

        for position, limit in factory:
            dis_sum = 0
            q = deque([(0, 0)])
            for j, r in enumerate(robot, 1):  # r = robot[j - 1]
                dis_sum += abs(r - position)

                # 1. 入
                v = f[j] - dis_sum
                while q and q[-1][1] >= v:
                    q.pop()
                q.append((j, v))

                # 2. 出
                while q[0][0] < j - limit:
                    q.popleft()

                # 3. 队首为滑动窗口最小值
                f[j] = dis_sum + q[0][1]

        return f[m]
''',
    call=f'Solution().minimumTotalDistance({ROBOT}, {FACTORY})',
    expect=4,
    skip=['factory.sort', 'robot.sort', 'm = len', 'q = deque', 'dis_sum = 0'],
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var='robot', label='robot（已排序；蓝 = 当前 r = robot[j−1]）', h=200, cell=90,
             color=lambda S, i, v: 'blue' if S.get('j') == i + 1 else None),
        dict(type='array', var=_f, label='f[j]：前 j 个机器人的最小总距离（∞ = 修不完）', h=200, cell=90,
             pointers={'j': 'pink'}),
        dict(type='queue', var='q', label='单调队列 q：(下标 k, f[k]−s[k])，队首是窗口最小值', h=200, fmt=_fmt),
    ],
    watch=['position', 'limit', ('j', 'j', 'pink'), 'dis_sum', ('v', 'v', 'yellow')],
    captions={
        'f = [0] + [inf] * m': '`f[0] = 0`：没有机器人，距离 0；`f[1..m] = ∞`：还没有工厂可修',
        'for position, limit in factory': '加入工厂 `{position}`，最多修 `{limit}` 个：`f` 原地滚动成「含这个工厂」的新一行',
        'for j, r in enumerate': lambda S, B, r: (f'`j = {S.j}`：现在算前 `{S.j}` 个机器人，`r = robot[{S.j-1}] = {S.r}`' if S.j != B.get('j') or S.j == 1 and 'dis_sum' not in B
                                                  else '这个工厂的 `j` 都扫完了'),
        'dis_sum += abs': '`dis_sum` = 前 `{j}` 个机器人到工厂 `{position}` 的距离前缀和 = `{dis_sum}`',
        'v = f[j] - dis_sum': _enq,
        'while q and q[-1][1] >= v': lambda S, B, r: (
            '队列空了，不用再弹' if not S.q else
            f'队尾 `{_i(S.q[-1][1])}` ≥ `v = {_i(S.v)}`：队尾又老又差，==永远不会是最小值== → 弹出' if S.q[-1][1] >= S.v
            else '队尾比 `v` 小，保留：队列从队首到队尾严格递增'),
        'q.pop()': '弹出队尾',
        'q.append((j, v))': '`(j, v)` 入队',
        'while q[0][0] < j - limit': lambda S, B, r: (
            f'队首下标 `{S.q[0][0]} < j − limit = {S.j - S.limit}`：已经修不到这么靠左的起点 → 出队'
            if S.q[0][0] < S.j - S.limit else f'队首下标 `{S.q[0][0]}` 还在窗口 `[{max(S.j - S.limit, 0)}, {S.j}]` 内'),
        'q.popleft()': '弹出队首（滑出窗口）',
        'f[j] = dis_sum + q[0][1]': lambda S, B, r: f'队首就是窗口最小值：`f[{S.j}] = dis_sum + min(f[k]−s[k])` = =={"∞" if S.f[S.j] == inf else S.f[S.j]}=='
        ,
        'return f[m]': '全部工厂用完，`f[m]` = =={ret}== 就是最小总移动距离',
    },
    cards=dict(
        one_liner='工厂修连续一段机器人，转移是滑动窗口最小值，用单调队列',
        complexity='时间 `O(nm + n log n + m log m)`，空间 `O(m)`',
        problem=['X 轴上有机器人 `robot` 和工厂 `[位置, 修理上限]`',
                 '每个机器人走到某个工厂被修好，工厂有上限，求总移动距离最小',
                 '示例：`robot=[0,4,6]`，`factory=[[2,2],[6,2]]` → `4`'],
        quote='存在这样的最优解，对于任意一对机器人 i 和 j（i<j），机器人 i 去的工厂编号 ≤ 机器人 j 去的工厂编号。同一个工厂修理的机器人，在排序后的机器人序列里是连续的一段。',
        quote_src='—— 灵茶山艾府题解（一、贪心性质）',
        idea=['先排序：交叉分配不会更优，所以每个工厂修一段连续的机器人',
              '`f[i+1][j] = s_i[j] + min(f[i][k] − s_i[k])`，`k` 在窗口 `[j−limit, j]`',
              '窗口随 `j` 右移 → 单调队列维护最小值；滚动数组把空间压到 `O(m)`'],
        summary=['时间 `O(nm)`（排序另计），空间 `O(m)`',
                 '易错：先入队再算 DP，因为窗口包含 `k = j`（修 0 个机器人）',
                 '`f[0] = 0`，其余初始 `∞`；`f[j]` 原地覆盖前先用它算 `v`',
                 '题解还给出：记忆化搜索 → 递推 → 单调队列 → 空间优化，本视频演示最后一种',
                 '同类题：239 滑动窗口最大值、1425 带限制的子序列和'],
    ),
)

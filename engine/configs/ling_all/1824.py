OB = [0, 1, 2, 0]
N0 = len(OB)


def _dis(S):
    d = S.get('dis')
    if d is None:
        return None
    return [['∞' if d[i][j] == N0 else d[i][j] for i in range(N0)] for j in range(3)]


def _cell(S, r, c, v):
    j, i = r, c
    if OB[c] == r + 1:
        return 'red'
    cur = (S.get('i'), S.get('j'))
    if cur == (i, j) and S.get('i') is not None:
        return 'yellow'
    return None


def _cur(S, k):
    return S.get(k)


def _text(S):
    i, j, d = S.get('i'), S.get('j'), S.get('d')
    if i is None or d is None:
        return '行 = 跑道，列 = 点；红格 = 障碍；格内数字 = 到这里的最少侧跳次数 `dis`'
    return f'青蛙在 `(点 {i}, 跑道 {j + 1})`，已侧跳 `d = {d}` 次；队首 = 次数最少的状态'


CONFIG = dict(
    num=1824, title='最少侧跳次数', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='0-1 BFS（双端队列）',
    tags=['灵神核心路线', '灵神题单·网格图', '灵神题单·动态规划', '难度分 1778'],
    code='''
class Solution:
    def minSideJumps(self, obstacles: List[int]) -> int:
        n = len(obstacles)
        dis = [[n] * 3 for _ in range(n)]
        dis[0][1] = 0
        q = deque([(0, 1)])  # 起点
        while True:
            i, j = q.popleft()
            d = dis[i][j]
            if i == n - 1: return d  # 到达终点
            if obstacles[i + 1] != j + 1 and d < dis[i + 1][j]:  # 向右
                dis[i + 1][j] = d
                q.appendleft((i + 1, j))  # 加到队首
            for k in (j + 1) % 3, (j + 2) % 3:  # 枚举另外两条跑道（向上/向下）
                if obstacles[i] != k + 1 and d + 1 < dis[i][k]:
                    dis[i][k] = d + 1
                    q.append((i, k))  # 加到队尾
''',
    call=f'Solution().minSideJumps({OB})',
    expect=1,
    max_steps=80,
    skip=['n = len(obstacles)', 'dis = [[n]', 'for k in', 'while True', 'd = dis[i][j]', 'appendleft', 'q.append'],
    views=[
        dict(type='text', fn=_text, size=22, h=55),
        dict(type='table', var=_dis, label='dis[点][跑道]（转置显示：行 = 跑道 1/2/3，列 = 点 0..n；黄 = 当前，红 = 障碍）', h=250, cell=84,
             rows=lambda S: ['跑1', '跑2', '跑3'], cols=lambda S: [f'点{c}' for c in range(N0)],
             color=_cell),
        dict(type='queue', var='q', label='双端队列 q（左 = 队首，向右走加队首；侧跳加队尾）', h=130,
             fmt=lambda x: f'点{x[0]}·跑{x[1] + 1}'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('d', 'd', 'green'), ('k', 'k', 'purple')],
    captions={
        'dis[0][1] = 0': '青蛙从点 0 的第二条跑道出发（下标 1），侧跳次数 `0`',
        'q = deque': '队列里放 `(点, 跑道)`，起点先入队',
        'i, j = q.popleft': '取队首：它的 `dis` 是当前队列里==最小==的（0-1 BFS 的两段性）',
        'if i == n - 1': lambda S, B, r: (f'`i = {S.i}` 已是最后一列 → 第一次到就是最优，直接返回 ==`{S.d}`==' if S.i == S.n - 1 else f'取出点 {S.i}·跑道 {S.j+1}，`d = {S.d}`；还没到最后一列（`{S.n-1}`）'),
        'if obstacles[i + 1]': lambda S, B, r: (f'向右（边权 0）：点 {S.i+1} 的跑道 {S.j+1} ' + ('有障碍，过不去' if S.obstacles[S.i+1] == S.j+1 else f'无障碍；`{S.d} < dis[{S.i+1}][{S.j}] = {S.dis[S.i+1][S.j] if S.dis[S.i+1][S.j] < S.n else "∞"}` → ' + ('更优，更新' if S.d < S.dis[S.i+1][S.j] else '不更优，跳过'))),
        'dis[i + 1][j] = d': '向右不用侧跳：`dis[{i+1}][{j}] = {d}`，==加到队首==（边权 0），马上处理',
        'if obstacles[i] != k + 1': lambda S, B, r: (f'侧跳到跑道 {S.k+1}：' + ('当前点该跑道有障碍，不能跳' if S.obstacles[S.i] == S.k+1 else f'无障碍；`{S.d}+1` 与 `dis[{S.i}][{S.k}]` = {"∞" if S.dis[S.i][S.k] >= S.n else S.dis[S.i][S.k]} 比较 → ' + ('更优' if S.d+1 < S.dis[S.i][S.k] else '不更优，跳过'))),
        'dis[i][k] = d + 1': '在同一点侧跳到跑道 `{k+1}`：次数 +1 → `dis[{i}][{k}] = {d+1}`，==加到队尾==（边权 1）',
    },
    cards=dict(
        one_liner='向右前进免费、侧跳花 1 次：0 放队首，1 放队尾',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['3 条跑道、`n+1` 个点，青蛙从点 0 的跑道 2 出发，要到点 `n`',
                 '`obstacles[i] = x` 表示点 `i` 的跑道 `x` 有障碍；同点可侧跳到无障碍的别的跑道',
                 '示例：`[0,1,2,3,0]` → `2`；`[0,1,2,0]` → `1`'],
        quote='对于边权为 0 的边 x→y，如果 dis[x]<dis[y]，更新 dis[y]=dis[x]，把 y 加到队首。对于边权为 1 的边 x→y，如果 dis[x]+1<dis[y]，更新后把 y 加到队尾。这个算法叫 0-1 BFS。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 3 条跑道看成 `3×(n+1)` 网格：向右边权 0，侧跳边权 1，求最短路',
              '普通 BFS 只处理边权 1；边权 0 的点要插队，所以用双端队列',
              '队列里始终只有 `d` 和 `d+1` 两段，所以不需要 vis 数组'],
        summary=['时间 `O(n)`：每个状态最多入队两次（队首一次、队尾一次）',
                 '易错：向右走==要检查下一点==的障碍，侧跳检查==当前点==的障碍',
                 '到达第 `n` 列任一行就可返回，不必等队列为空',
                 '边权不止 0/1 时换成最小堆就是 Dijkstra；类似题 1368、2290'],
    ),
)

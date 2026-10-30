POWER = [3, 4]


def _sub(S):
    """怪物 × 天数 的费用矩阵（取自 w 的右上块）"""
    if 'w' not in S or 'n' not in S:
        return None
    n = S['n']
    return [[S['w'][i][j] for j in range(n + 1, 2 * n + 1)] for i in range(1, n + 1)]


def _used(S, i, j, v):
    """怪物 i+1 暂定放在第 j+1 次击杀：反向边有流量"""
    n = S['n']
    return 'green' if S['c'][n + 1 + j][i + 1] > 0 else None


def _flowtxt(S):
    if 'res' not in S:
        return ''
    n = S['n']
    pairs = [f'怪{i}→第{j}杀' for i in range(1, n + 1) for j in range(1, n + 1) if S['c'][n + j][i] > 0]
    return f'当前分配：{"  ".join(pairs) if pairs else "（空）"}　累计天数 =={S["res"]}=='


CONFIG = dict(
    num=2403, title='杀死所有怪物的最短时间', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='最小费用最大流（怪物与击杀顺序的最优匹配）',
    tags=['灵神题单·图论算法', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def minimumTime(self, power):

        n = len(power)
        s = 0
        c = [[0] * (n + n + 2) for _ in range(n + n + 2)]
        w = [[0] * (n + n + 2) for _ in range(n + n + 2)]
        t = n + n + 1

        for i in range(1, n + 1):
            c[s][i] = 1
        
        for i in range(n + 1, n + n + 1):
            c[i][t] = 1
        
        for i in range(1, n + 1):
            for j in range(n + 1, n + n + 1):
                c[i][j] = 1
                w[i][j] = power[i - 1] // (j - n)
                if power[i - 1] % (j - n) > 0:
                    w[i][j] += 1
                w[j][i] = -w[i][j]

        res = 0
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                next = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + w[now][index]):
                        dis[index] = dis[now] + w[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        next = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(next)
                now = next

            res += dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]

        return res
''',
    call=f'Solution().minimumTime({POWER})',
    expect=5,
    skip=['n = len', 's = 0', 't = n + n + 1', 'c = [[0]', 'w = [[0]', 'c[s][i] = 1', 'c[i][t] = 1',
          'c[i][j] = 1', 'w[j][i] = -', 'min_dis = None', 'next = None', 'for index in range',
          'prev[index] = now', 'if index in used:', 'used.remove', 'min_dis = dis[index]', 'next = index',
          'for i in range', 'for j in range', 'c[prev[now]][now] -= 1', 'now = prev[now]', 'if power[i - 1] %', 'w[i][j] += 1',
          'dis = [None]', 'prev = [None]', 'used = set', 'dis[s] = 0', 'now = s', 'now = t',
          'if c[now][index] > 0', 'if index not in used and dis', 'now = next', 'while t not in used',
          'if min_dis is None', 'while now != s'],
    max_steps=110,
    views=[
        dict(type='grid', var=_sub, label='w[怪物][第几杀] = 天数 ceil(power/增益)（绿 = 暂定）', cell=84, h=300,
             rows=lambda S: [f'怪{i}' for i in range(1, S['n'] + 1)] if 'n' in S else None,
             cols=lambda S: [f'第{j}杀' for j in range(1, S['n'] + 1)] if 'n' in S else None,
             color=_used),
        dict(type='array', var='dis', label='dis[点]（0=s，1-2=怪物，3-4=第几杀，5=t；蓝=now）', cell=64, h=190,
             color=lambda S, i, v: 'blue' if i == S.get('now') else ('green' if i in S.get('used', ()) else None)),
        dict(type='array', var='prev', label='prev[点]：最短路上的前驱', cell=64, h=170),
        dict(type='text', fn=_flowtxt, h=60),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'blue'), 'used'],
    captions={
        'dis[index] = dis[now]': lambda S, B, r: (f'从点 `{S.now}` 经边 `{S.now}→{S.index}`（费用 `{S.w[S.now][S.index]}`）松弛：`dis[{S.index}] = {S.dis[S.index]}`，前驱 `{S.now}`'
                                                   + ('（==负费用边：撤销之前的分配==）' if S.w[S.now][S.index] < 0 else '')),
        'used.add(next)': '选 `dis` 最小的未确定点 `{next}`（`dis = {dis[next]}`）标为已确定，下一步从它出发松弛',
        'w[i][j] = power': '怪物 `{i}`（`power = {power[i - 1]}`）作第 `{j - n}` 个击杀：增益为 `{j - n}`，需要 `ceil({power[i - 1]}/{j - n})` = =={-(-power[i - 1] // (j - n))}== 天',
        'w[j][i] = -': '`w[{i}][{j}] = {w[i][j]}`，反向边取负：`w[{j}][{i}] = {w[j][i]}`',
        'return res': '最短总天数 ==`{res}`==',
        'res += dis[t]': '沿最便宜的增广路送 1 单位流，费用 `{dis[t]}`：`res = {res}`',
        'c[now][prev[now]] += 1': '回溯路径：边 `{prev[now]}→{now}` 容量 −1，反向边 `{now}→{prev[now]}` +1（==反向边以后可以“退回”这次分配==）',
        'res = 0': '`res` 累计总天数',
        'while True': '开始新一轮：找一条费用最小的增广路',
    },
    cards=dict(
        one_liner='击杀顺序是一个排列：怪物配“第几个击杀”，费用流求最小总天数',
        complexity='时间约 `O(n^2)` 条边 × `n` 次增广，空间 `O(n^2)`',
        problem=['有 `n` 个怪物，`power[i]` 是击败它所需的法力，初始法力 0，增益 `gain = 1`',
                 '每天法力 += `gain`；法力 ≥ `power[i]` 时可击杀，击杀后法力清零、`gain` += 1',
                 '求击杀全部怪物所需的最少天数',
                 '本视频：`power = [3,4]` → `5`'],
        quote='题目实际上是需要找出power的一个排列，也就是将power[i]对应到i + 1，使得power[i] / (i + 1)向上取整后的和最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `k` 个击杀时增益是 `k`，杀 `power` 要 `ceil(power / k)` 天',
              '怪物和“第几个击杀”各 `n` 个，费用 = 天数 → 二分图最优匹配',
              '建图：源点→怪物，怪物→第 k 杀（费用 `ceil`），第 k 杀→汇点，容量都是 1；跑最小费用最大流'],
        summary=['状压 DP 是 `O(2^n · n)`，匹配/费用流是多项式，更稳',
                 '本写法每轮用类 Dijkstra 找最短增广路（有负边，所以允许点被“撤销已确定”）',
                 '负费用反向边让后面的怪物可以把先前的分配“换走”',
                 '原文为 Python 2 写法，其中 `power[i - 1] / (j - n)` 的整数除法已改为 `//`，其余未改'],
    ),
)

CAPS = [4, 3, 2, 2]


def _txt(S):
    if 'c' not in S:
        return '`f[j]`：恰好留下 j 人的方案数'
    c = S['c']
    return f'当前安检室 `c = {c}`：要么不留人，要么当栈留 `c − 1 = {c - 1}` 人'


CONFIG = dict(
    num='LCP 47', title='入场安检', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包方案数 · 滚动数组',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def securityCheck(self, capacities, k):

        f = [0] * (k + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for c in capacities:
            for j in range(k, c - 2, -1):
                f[j] += f[j - (c - 1)]
                if f[j] >= mod:
                    f[j] -= mod
        
        return f[k]
''',
    call='Solution().securityCheck([4,3,2,2], 6)',
    expect=2,
    skip=['mod = ', 'if f[j] >= mod', 'f[j] -= mod'],
    max_steps=46,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='f', label='f[j]（j = 蓝色箭头；f[j] 累加 f[j − (c−1)]）', h=260, cell=90,
             pointers={'j': 'blue'},
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('c', 'c', 'yellow'), ('j', 'j', 'blue'), ('f[k]', 'f[k]', 'green')],
    captions={
        'f = [0] * (k + 1)': '`f[j]`：栈安检室填充人数之和恰好为 `j` 的方案数，共 `k + 1` 格',
        'f[0] = 1': '一个安检室都不选当栈：和为 0 的方案只有 ==1 种==',
        'for c in capacities': lambda S, B, r: f'第 `{S.c}` 号容量的安检室：当栈可留 `{S.c - 1}` 人，当队列留 0 人',
        'for j in range': lambda S, B, r: (f'`j` 从大到小：倒序保证 `f[j − {S.c - 1}]` 还是上一轮的值（每个安检室只用一次）'
                                          if 'j' in S else '这个房间的 `c − 1` 比 `k` 还大，放不进 → 跳过'),
        'f[j] += f[j - (c - 1)]': '当栈：`f[{j}] += f[{j} − {c - 1}]` = `{B.f[j]} + {B.f[j - (c - 1)]}` → =={f[j]}==',
        'return f[k]': '和恰好为 `k = {k}` 的方案数 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='安检室当栈留 c−1 人，转成 0-1 背包数方案',
        complexity='时间 `O(N·k)`，空间 `O(k)`',
        problem=['`N` 个安检室，容量 `capacities[i]`，每个可设为队列（先进先出）或栈（后进先出）',
                 '观众依次入场，问有几种类型设定，能让编号 `k` 的观众第一个通过最后一个安检室',
                 '示例：`[2,2,3], k=2` → `2`；本视频：`[4,3,2,2], k=6` → `2`'],
        quote='题目给出了若干个房间，其中第i个房间可以选择留下capacities[i] - 1名游客，或者不留下任何游客。……这是一个典型的背包问题',
        quote_src='—— yiduobo 题解原文',
        idea=['栈房间先填 `c − 1` 人，就和长度 1 的队列一样；队列房间不留人',
              '每个房间 ==选 / 不选== 留 `c − 1` 人，总共要恰好留下 `k` 人',
              '`f[i][j] = f[i−1][j] + f[i−1][j−(c−1)]`，只依赖上一轮 → 滚动成一维倒序'],
        summary=['时间 `O(N·k)`，空间 `O(k)`；答案对 `10^9+7` 取模',
                 '`c = 1` 时 `c − 1 = 0`：栈和队列等价，两种设定都计数，所以 `f` 会翻倍',
                 '倒序遍历 `j`，否则同一个房间会被重复选',
                 '原文题解文字写成 `k − 1` 名游客，但代码里的目标是 `k`，以代码为准',
                 '原文为 Python 2 风格，代码未改'],
    ),
)

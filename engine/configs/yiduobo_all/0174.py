CONFIG = dict(
    num=174, title='地下城游戏', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='从终点倒推 DP',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def calculateMinimumHP(self, dungeon):

        m = len(dungeon)
        n = len(dungeon[0])

        f = [[0] * n for _ in range(m)]

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if i == m - 1:
                    if j == n - 1:
                        f[i][j] = 1
                    else:
                        f[i][j] = f[i][j + 1]
                elif j == n - 1:
                    f[i][j] = f[i + 1][j]
                else:
                    f[i][j] = min(f[i + 1][j], f[i][j + 1])

                f[i][j] = max(1, f[i][j] - dungeon[i][j])

        return f[0][0]
''',
    call='Solution().calculateMinimumHP([[-2,-3,3],[-5,-10,1],[10,30,-5]])',
    expect=7,
    skip=['m = len', 'n = len', 'for j in range'],
    views=[
        dict(type='grid', var='dungeon', label='dungeon（房间加减血）', h=230, cell=84,
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='table', var='f', label='f[i][j]：从 (i,j) 出发，至少需要多少初始生命值', h=230, cell=84,
             cursors=[('i', 'j', 'yellow', '')],
             color=lambda S, i, j, v: ('green' if (i, j) == (S.get('i'), S.get('j')) and S.get('_line') in (17, 18, 19, 21) else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i][j]', lambda S: S['f'][S['i']][S['j']] if 'i' in S and 'j' in S else '', 'green')],
    captions={
        'f = [[0]': '`f[i][j]` = 从 `(i,j)` 出发走到终点，==至少需要的初始生命值==（倒着定义）',
        'for i in range': '==从终点倒着填表==：后面要付出的血量，已经隐含在状态里了',
        'f[i][j] = 1': '终点：到了这里生命值至少要是 `1`，先记 `f = 1`（下面再减去本格的加减血）',
        'f[i][j] = f[i][j + 1]': '最后一行只能往右走：`f[{i}][{j}]` 先取右边的 `{f[i][j+1]}`',
        'f[i][j] = f[i + 1][j]': '最后一列只能往下走：`f[{i}][{j}]` 先取下面的 `{f[i+1][j]}`',
        'min(f[i + 1][j]': '右、下两条路取需求更小的：`min({f[i+1][j]}, {f[i][j+1]}) = {f[i][j]}`',
        'max(1,': '本格 `{dungeon[i][j]}`：进来时需要 `{B.f[i][j]} - ({dungeon[i][j]})`，但血量不能低于 1 → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[0][0]': '起点的需求就是答案：初始至少 `{ret}` 点生命值',
    },
    cards=dict(
        one_liner='正着定义 DP 不满足最优子结构，从终点倒着算',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['骑士从左上角出发，只能向右或向下走到右下角救公主',
                 '房间的数是正 = 加血，负 = 扣血，生命值任何时刻都必须 `> 0`',
                 '求骑士最少需要多少初始生命值。示例 `[[-2,-3,3],[-5,-10,1],[10,30,-5]]` → `7`'],
        quote='可以从终点开始往回做动态规划，此时的f[i][j]表示从第i行第j列开始，至少需要多少生命值才能走到终点。这样一来，为后面的负数格子累积生命值这个概念就已经隐含在状态中了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先付出血量才能走到大加血的房间，所以“从起点到 (i,j) 最少血量”会在竞争中误删好路线',
              'g（剩余血量）等辅助数组也不行：够用就好，无法决定谁优先',
              '倒着定义：`f[i][j] = max(1, min(下, 右) - dungeon[i][j])`'],
        summary=['时间、空间 `O(mn)`',
                 '`max(1, ...)`：本格是大加血房时结果会变成 0 或负数，但血量至少要 1',
                 '最后一行、最后一列只有一个方向可走，要单独处理',
                 '同类：需要“倒推”才满足无后效性的 DP'],
    ),
)

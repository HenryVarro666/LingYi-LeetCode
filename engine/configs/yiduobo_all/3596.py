CONFIG = dict(
    num=3596, title='最小花费路径交替方向 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='曼哈顿距离 · 分类讨论',
    tags=[],
    code='''
class Solution(object):
    def minCost(self, m, n):
        
        if m == 1 and n == 1:
            return 1
        if m == 2 and n == 1:
            return 3
        if m == 1 and n == 2:
            return 3
        
        return -1
''',
    call='Solution().minCost(2, 3)',
    expect=-1,
    views=[
        dict(type='grid', var=lambda S: [[(i + 1) * (j + 1) for j in range(S['n'])] for i in range(S['m'])],
             label='网格：格子里是进入该格的花费 (i+1)×(j+1)，终点在右下角', cell=130, h=300,
             color=lambda S, i, j, v: 'green' if (i, j) == (S['m'] - 1, S['n'] - 1) else ('blue' if (i, j) == (0, 0) else None)),
        dict(type='text', h=120, size=30,
             fn=lambda S: (f"起点 (0,0) 到终点距离 = `{S['m'] - 1} + {S['n'] - 1}` = =={S['m'] + S['n'] - 2}=="
                           f"；奇数步 −1，偶数步 +1，一步到不了就永远到不了")),
    ],
    watch=['m', 'n'],
    captions={
        'm == 1 and n == 1': '`m={m}, n={n}`：起点就是终点吗？=={"是，只付 1" if m == 1 and n == 1 else "不是"}==',
        'm == 2 and n == 1': '`m={m}, n={n}`：终点 (1,0)，第 1 步右/下一步到达？=={"是" if m == 2 and n == 1 else "不是"}==',
        'm == 1 and n == 2': '`m={m}, n={n}`：终点 (0,1)，第 1 步一步到达？=={"是" if m == 1 and n == 2 else "不是"}==',
        'return 1': '起点即终点，只付入场费 `1`',
        'return 3': '`1 + 2 = 3`：先付起点 1，再一步走进终点付 2',
        'return -1': '三种能一步到位的情况都不是 → 永远走不到终点，返回 =={ret}==',
    },
    cards=dict(
        after=[dict(heading='为什么只有三种', lines=['第 1 步进入 `(0,0)` 后，距离终点 `m+n-2`', '第 2 步（奇数次移动）靠近 1，第 3 步（偶数次）又远离 1', '要想到达，必须第一次移动就走进终点：距离恰为 1', '距离为 1 只有 `(1,2)` 与 `(2,1)`；距离 0 就是 `(1,1)`'])],
        one_liner='奇数步靠近、偶数步远离：一步到不了，就永远到不了',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`m × n` 网格，进入 `(i,j)` 的花费是 `(i+1)*(j+1)`，第一步先进入 `(0,0)` 并付费',
                 '之后第奇数次移动必须向右/下，第偶数次必须向左/上',
                 '求到达 `(m-1, n-1)` 的最小总花费，到不了返回 `-1`'],
        quote='在奇数次移动后，与终点的曼哈顿距离将减少1，反之在偶数次移动后，与终点的曼哈顿距离将增加1。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数步离终点近 1，偶数步又远 1 → ==来回抵消，无法深入==',
              '所以只有第一次移动就走进终点才行',
              '只剩 `(1,1)` 花费 1、`(1,2)`/`(2,1)` 花费 3 三种，其余都是 `-1`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：别写 DP/BFS，距离的奇偶性已经决定了结果',
                 '`(1,2)`、`(2,1)` 的花费是 `1 + 2 = 3`，不要漏掉起点的 1',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)

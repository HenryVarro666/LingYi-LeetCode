CONFIG = dict(
    num=598, title='区间加法 II', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='逐个矩形求重叠',
    tags=['灵神题单', '难度分 1400'],
    code='''
class Solution(object):
    def maxCount(self, m, n, ops):

        for x, y in ops:
            m = min(m, x)
            n = min(n, y)
        
        return m * n
''',
    call='Solution().maxCount(3, 4, [[2,3],[3,2],[3,4]])',
    expect=4,
    views=[
        dict(type='grid', h=330, var=lambda S: [[1 if x < S['m'] and y < S['n'] else 0 for y in range(4)] for x in range(3)],
             color=lambda S, i, j, v: 'green' if v else None, label='当前重叠区域（绿）：右下角 (m, n)'),
        dict(type='text', fn=lambda S: f"重叠矩形：左上 (0,0)，右下 (`{S['m']}`, `{S['n']}`)，大小 =={S['m']*S['n']}=="),
    ],
    watch=['m', 'n', 'x', 'y'],
    captions={
        'for x, y in ops': lambda S, B, r: ('ops 都处理完了，循环结束' if 'x' in B and B['x'] == S.x and B['y'] == S.y else f'取下一个操作矩形，右下角 `({S.x}, {S.y})`'),
        'm = min': '重叠部分的行数：`min(m, x)` → =={m}==',
        'n = min': '重叠部分的列数：`min(n, y)` → =={n}==',
        'return': '所有矩形的重叠部分是 `{m} × {n}` → =={ret}==（被加次数最多的格子数）',
    },
    cards=dict(
        one_liner='前 k 个矩形的重叠 = 前 k-1 个的重叠再和第 k 个重叠',
        complexity='时间 `O(k)`，空间 `O(1)`',
        problem=['`m × n` 矩阵全 0，每个操作让左上 `x × y` 区域加 1',
                 '求最后最大整数的个数',
                 '示例：`m=3, n=4, ops=[[2,3],[3,2],[3,4]]` → `4`'],
        quote='对于任意两个矩形，二者重叠的部分左上角不变，右下角为(min(x1, x2), min(y1, y2))。',
        quote_src='—— yiduobo 题解原文',
        idea=['所有矩形左上角都重合，必有公共部分',
              '两个矩形重叠：右下角取各坐标最小值',
              '一趟遍历，把 m、n 直接当作当前重叠的右下角，不断取 min'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '直接复用参数 m、n 当重叠区域，ops 为空时自然是 `m * n`',
                 '重叠是“前缀递推”：已有重叠 + 新矩形'],
    ),
)

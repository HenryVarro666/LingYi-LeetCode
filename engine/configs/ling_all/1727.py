M = [[0, 0, 1, 1], [1, 1, 1, 1], [1, 0, 1, 1]]


def _mc(S, i, j, v):
    if 'row' not in S or 'matrix' not in S:
        return None
    return 'cyan' if S['matrix'][i] is S['row'] and v else None


def _txt(S):
    if 'idx' not in S or 'heights' not in S:
        return ''
    n = len(S['heights'])
    line = S.get('_line', 0)
    if line == 23 and 'i' in S:
        h = S['heights'][S['idx'][S['i']]]
        return f"取最高的 `{n - S['i']}` 列，高度至少 `{h}` → 面积 `{n - S['i']} × {h}` = =={(n - S['i']) * h}=="
    return '`heights` 按列号 `idx` 排好序（高度从小到大）；取后面 k 列，矩形高 = 这 k 列里最小的'


CONFIG = dict(
    num=1727, title='重新排列后的最大子矩阵', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='枚举底边 + 贪心取最高的 k 列',
    tags=['贪心与思维', '难度分 1927'],
    code='''
class Solution:
    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        n = len(matrix[0])
        heights = [0] * n
        idx = list(range(n))  # 按照高度排序后的列号
        ans = 0

        for row in matrix:
            zeros = []
            non_zeros = []
            for j in idx:
                if row[j] == 0:
                    heights[j] = 0
                    zeros.append(j)
                else:
                    heights[j] += 1
                    non_zeros.append(j)
            idx = zeros + non_zeros  # 把高度为 0 的列号排在其他高度前面

            # heights[idx[i]] 是递增的
            for i in range(len(zeros), n):  # 高度 0 无需计算
                ans = max(ans, (n - i) * heights[idx[i]])

        return ans
''',
    call=f'Solution().largestSubmatrix({M})',
    expect=6,
    skip=['n = len', 'zeros = []', 'non_zeros = []', 'zeros.append', 'non_zeros.append', 'for j in idx'],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='grid', var='matrix', label='matrix（青 = 当前底边这一行的 1）', cell=80, h=250, color=_mc),
        dict(type='array', var='heights', label='heights[j]：第 j 列向上连续 1 的个数', cell=84, h=150),
        dict(type='array', var=lambda S: [S['heights'][j] for j in S['idx']] if 'idx' in S else None,
             label='按 idx 排序后的高度（越靠右越高）', cell=84, pointers={'i': 'blue'}, h=170),
    ],
    watch=[('i', 'i', 'blue'), ('idx', 'idx'), ('ans', 'ans', 'green')],
    captions={
        'for row in matrix': '枚举子矩形的==底边==：这一行是 `{row}`',
        'heights[j] = 0': '这一列是 0：柱子断了，高度归 0（列号 `{j}` 进 zeros）',
        'heights[j] += 1': '这一列是 1：在柱子下面垫一块石头，抬高到 `{heights[j]}`',
        'idx = zeros + non_zeros': '高度变 0 的列排前面，其余列保持原来的相对顺序（都 +1，==相对大小不变，无需重新排序==）→ `idx = {idx}`',
        'ans = max': lambda S, B, r: (f'`i = {S.i}`：后 `{len(S.heights) - S.i}` 列最矮 `{S.heights[S.idx[S.i]]}` → 面积 `{(len(S.heights) - S.i) * S.heights[S.idx[S.i]]}`，'
                                       f'`ans` {B.ans} → =={S.ans}==' ),
        'return ans': '最大面积 ==`{ret}`==',
    },
    cards=dict(
        one_liner='列能随便换，就把最高的 k 列排在一起',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`m × n` 的 0/1 矩阵，可以把==整列==任意重排',
                 '求重排后全为 1 的最大子矩阵面积',
                 '示例：`[[0,0,1],[1,1,1],[1,0,1]]` → `4`（视频用 3×4 的小例子）'],
        quote='贪心地，把 heights 最大的 k 个数排在一起，就可以让子数组的最小值（矩形的高）尽量大，从而得到最大的矩形面积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举底边，`heights[j]` = 这一列向上连续 1 的个数（柱子）',
              '重排后取 k 个相邻柱子：宽 k，高 = 最小柱高；最优是取最高的 k 根',
              '从上一行到下一行，+1 的列相对大小不变，只需把变 0 的列放前面，免去排序'],
        summary=['优化后时间 `O(mn)`，优化前每行排序是 `O(mn log n)`',
                 '`idx` 排的是==列号==，这样才知道每个高度属于哪一列',
                 '高度为 0 的列无需计算：循环从 `len(zeros)` 开始',
                 '灵神还给出了每行直接 `sorted(heights)` 的写法，视频演示的是线性优化'],
    ),
)

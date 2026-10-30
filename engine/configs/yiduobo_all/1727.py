M = [[0, 0, 1, 1], [1, 1, 1, 1], [1, 0, 1, 1]]


def _mc(S, i, j, v):
    if 'i' not in S or 'matrix' not in S:
        return None
    return 'cyan' if i == S['i'] and v else None


def _txt(S):
    if 'height' not in S or 'res' not in S:
        return ''
    if S.get('_line', 0) >= 15 and 'h' in S:
        return f"以第 `{S['j'] + 1}` 高的列为右端：宽 `{S['j'] + 1}` × 高 `{S['h']}` = =={(S['j'] + 1) * S['h']}=="
    return '每列向上延伸的高度 `height`；从大到小排好后，前 `j+1` 列的最小高度就是第 `j` 个'


CONFIG = dict(
    num=1727, title='重新排列后的最大子矩阵', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='逐行累计高度 + 降序排序后一趟扫描',
    tags=['灵神题单', '难度分 1927'],
    code='''
class Solution(object):
    def largestSubmatrix(self, matrix):

        m = len(matrix)
        n = len(matrix[0])
        height = [0] * n
        res = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j]:
                    height[j] += 1
                else:
                    height[j] = 0
            
            for j, h in enumerate(sorted(height, reverse=True)):
                res = max(res, (j + 1) * h)

        return res
''',
    call=f'Solution().largestSubmatrix({M})',
    expect=6,
    skip=['m = len', 'n = len', 'height = [0]', 'res = 0'],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='grid', var='matrix', label='matrix（青 = 当前加入的这一行）', cell=80, h=250, color=_mc),
        dict(type='array', var='height', label='height[j]：向上延伸的最大高度', cell=84, h=150),
        dict(type='array', var=lambda S: sorted(S['height'], reverse=True) if 'height' in S and S.get('_line', 0) >= 15 else None,
             label='height 从大到小排序后（扫描时才出现）', cell=84, h=170,
             pointers={'j': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'for i in range(m)': '加入第 `{i}` 行，考察以它为==下边==的最大子矩阵',
        'height[j] += 1': '`matrix[{i}][{j}] = 1`：这一列的高度 +1 → `{height[j]}`',
        'height[j] = 0': '`matrix[{i}][{j}] = 0`：这一列断了，高度归 0',
        'for j, h in enumerate': '把所有列按高度从大到小排，一趟扫描：`{sorted(height, reverse=True)}`',
        'res = max': lambda S, B, r: (f'前 `{S.j + 1}` 列的最小高度是 `{S.h}`：面积 `{S.j + 1} × {S.h}` = {(S.j + 1) * S.h}，'
                                       f'`res` {B.res} → =={S.res}=='),
        'return res': '最大面积 ==`{res}`==',
    },
    cards=dict(
        one_liner='每行算出柱高，按高度降序排，第 j 根配宽 j+1',
        complexity='时间 `O(mn log n)`，空间 `O(n)`',
        problem=['0/1 矩阵，可以按任意顺序重排==列==',
                 '求重排后全为 1 的最大子矩阵面积',
                 '示例：`[[0,0,1],[1,1,1],[1,0,1]]` → `4`（视频用 3×4 的小例子）'],
        quote='将所有位置按照向上可以延伸的高度从大到小进行排序，然后一趟扫描。对于当前位置j而言，显然是有height[i][0] >= height[i][1] >= ... >= height[i][j]，因此以当前位置作为右下角的最大矩形面积就是(j + 1) * height[i][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 85 题类似：逐行加入，`height[j]` 由上一行递推',
              '列可以重排，所以把高的列全部挤到左边',
              '降序后前 `j+1` 列的最小高度就是 `height[j]`，面积 `(j+1) × height[j]`'],
        summary=['时间 `O(mn log n)`：每行一次排序；空间 `O(n)`',
                 '`height` 只依赖上一行，省去了行这一维',
                 '`sorted` 返回新列表，不会打乱 `height` 原来的列顺序',
                 '对比灵神：灵神用 idx 维护有序列号，免去每行排序，降到 `O(mn)`'],
    ),
)

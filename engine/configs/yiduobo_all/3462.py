CONFIG = dict(
    num=3462, title='提取至多 K 个元素的最大总和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='行内 top limit 再全局 top k',
    tags=['贪心', '排序', '难度分 1416'],
    code='''
class Solution(object):
    def maxSum(self, grid, limits, k):
        
        candidate = []
        m = len(grid)
        for index in range(m):
            candidate.extend(sorted(grid[index], reverse=True)[:limits[index]])
        
        return sum(sorted(candidate, reverse=True)[:k])
''',
    call='Solution().maxSum([[5,3,7,1],[8,2,6,4],[9,0,2,1]], [2,1,2], 4)',
    expect=29,
    views=[
        dict(type='grid', var='grid', h=250, cell=70,
             cursors=[('index', 0, 'yellow', '')]),
        dict(type='array', var='candidate', h=130, label='candidate'),
        dict(type='text', fn=lambda S: '多路归并用堆更优，这里暴力排序：先取每行 top limit，再取总的 top k', size=26),
    ],
    watch=[('index', 'index', 'blue'), ('k', 'k', 'blue')],
    captions={
        'candidate = []': '`candidate` 用来装每一行的 top limit 元素',
        'candidate.extend': '第 `{index}` 行完整降序排序后取前 `limits[{index}]` = `{limits[index]}` 个，加入候选：`candidate` = {candidate}',
        'return sum': '候选整体降序，取 top `{k}`：`{sorted(candidate, reverse=True)[:k]}` → =={ret}==',
    },
    cards=dict(
        one_liner='先每行取 top limit，再合起来取 top k',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['矩阵 `grid` 第 `index` 行至多取 `limits[index]` 个，总共至多取 `k` 个',
                 '求取出元素的最大总和',
                 '示例：`[[1,2],[3,4]]`，`limits=[1,2]`，`k=2` → `7`'],
        quote='先对每一行，分别找出这一行中的 top limit 个元素，然后对于所有行，使用一个堆来执行多路归并，获取其中的 top k 大的元素。我在这里采用的是比较暴力的处理方法。',
        quote_src='—— yiduobo 题解',
        idea=['每行只可能用到最大的 `limit` 个数',
              '作者最优思路是堆做多路归并，实际写的是暴力版',
              '先逐行完整排序取 top limit，放进 `candidate`，再整体排序取 top k'],
        summary=['时间 `O(mn log(mn))`，空间 `O(mn)`',
                 '提速：行内用堆 / 多路归并取 top k',
                 '易错点：排序要降序；`limits[index]` 可能是 0',
                 '专题：贪心 §1.1 从最小/最大开始贪心'],
    ),
)

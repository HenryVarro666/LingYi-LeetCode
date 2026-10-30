G = [[4, 2, 1, 5], [3, 3, 1, 2], [6, 1, 2, 2], [2, 5, 3, 1]]


def _sorted_line(S):
    line = S.get('line')
    return sorted(line) if line else []


CONFIG = dict(
    num=2500, title='删除每行中的最大值', difficulty='Easy', category='模拟',
    author='yiduobo', technique='逐行排序 · 维护每列最大值',
    tags=[],
    code='''
class Solution(object):
    def deleteGreatestValue(self, grid):

        n = len(grid[0])
        max_list = [0] * n
        for line in grid:
            for index, v in enumerate(sorted(line)):
                max_list[index] = max(max_list[index], v)
        
        return sum(max_list)
''',
    call=f'Solution().deleteGreatestValue({G!r})',
    expect=13,
    views=[
        dict(type='grid', var='grid', label='grid（原始输入，逐行处理）', cell=90, h=280),
        dict(type='array', var=lambda S: sorted(S['line']) if S.get('line') else [], label='sorted(line)（当前行排序后）',
             color=lambda S, i, v: 'blue' if i == S.get('index') else None, cell=90, h=170),
        dict(type='array', var='max_list', label='max_list（每一列目前见过的最大值）', pointers={'index': 'blue'}, cell=90, h=170,
             color=lambda S, i, v: 'green' if i == S.get('index') else None),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink')],
    captions={
        'n = len': '`n = {n}`：矩阵有 n 列，所以要记 n 个列最大值',
        'max_list = [0]': '`max_list` 第 k 项 = 排序后第 k 列出现过的最大值，初始为 0',
        'for line in grid': lambda S, B, r: ('所有行都处理完，循环结束' if B.get('line') == S.line else f'处理下一行 `{S.line}`'),
        'for index, v in enumerate': lambda S, B, r: ('这一行的数都处理完了' if B.get('index') == S.index and B.get('v') == S.v and B.get('line') == S.line else f'排序后的第 `{S.index}` 个数是 `{S.v}`：它就是这一行第 {S.index+1} 轮要删的值'),
        'max_list[index] = max': '`max({B.max_list[index]}, {v}) = {max_list[index]}`：这一列的最大值更新为 =={max_list[index]}==',
        'return sum': '各列最大值相加 `{max_list}` → =={ret}==',
    },
    cards=dict(
        one_liner='每行排序后，第 k 小的数对应第 k 轮删除的值',
        complexity='时间 `O(mn log n)`，空间 `O(n)`',
        problem=['矩阵每轮从每行删掉最大值，把被删值里的最大者加进答案',
                 '直到矩阵为空，返回答案',
                 '示例：`[[1,2,4],[3,3,1]]` → `8`'],
        quote='只需遍历每行，先进行排序然后一趟遍历，使用当前位置上的数值更新其所在列的最大值，最后将每一列的最大值求和即为最终的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，直接模拟：排序保证每行最大值在最后',
              '用 `max_list[index]` 记录第 `index` 轮所有行的删除值的最大者',
              '不改原矩阵，额外开 `n` 个格子存列最大值'],
        summary=['时间 `O(mn log n)`，空间 `O(n)`（`sorted` 另开一份）',
                 '易错点：`max_list` 按排序后的下标记，不是原始列下标',
                 '对比灵神：灵神原地排序再 `zip(*grid)` 转置取列最大，yiduobo 边遍历边更新'],
    ),
)

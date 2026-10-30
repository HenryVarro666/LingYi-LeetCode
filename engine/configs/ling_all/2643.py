CONFIG = dict(
    num=2643, title='一最多的行', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='逐行求和，严格大于才更新', tags=[],
    code='''
class Solution:
    def rowAndMaximumOnes(self, mat: List[List[int]]) -> List[int]:
        row_idx = max_sum = -1
        for i, row in enumerate(mat):
            s = sum(row)
            if s > max_sum:
                row_idx, max_sum = i, s
        return [row_idx, max_sum]
''',
    call='Solution().rowAndMaximumOnes([[0,0,1,0],[1,1,0,1],[1,1,0,0],[0,0,0,0]])',
    expect=[1, 3],
    views=[
        dict(type='grid', var='mat', cursors=[('i', 0, 'yellow', 'i')], h=330,
             color=lambda S, i, j, v: ('green' if i == S.get('row_idx') else 'blue' if i == S.get('i') else None) if 'row_idx' in S else None),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'orange'), ('row_idx', 'row_idx', 'green'), ('max_sum', 'max_sum', 'green')],
    captions={
        'row_idx = max_sum': '都初始化为 `-1`：这样第 0 行（和 ≥ 0）一定能更新',
        's = sum': '第 `{i}` 行 1 的个数 `s` = =={s}==',
        'if s > max_sum': '`{s} > {max_sum}`？' + '严格大于才更新：相等时保留更靠前的行',
        'row_idx, max_sum': '更新答案：行 `{row_idx}`，1 的个数 `{max_sum}`',
        'return': '返回 `[{row_idx}, {max_sum}]`',
    },
    cards=dict(
        one_liner='从上往下扫，只有严格更多才更新，天然取最小行号',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['二进制矩阵，找 1 最多的行的下标和 1 的数量',
                 '多行并列时取行下标最小的',
                 '示例：`[[0,0,0],[0,1,1]]` → `[1,2]`'],
        quote='由于我们是从上到下遍历行，所以找到的最大和的行号，一定是相同最大和的行号中最小的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每行元素和 = 这一行 1 的个数',
              '`s > max_sum` 用严格大于：并列的后面行不会覆盖前面的'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '==用 `>` 而不是 `>=`==，否则并列时会取到更大的行号',
                 '初值设为 `-1`，保证第一行就能更新'],
    ),
)

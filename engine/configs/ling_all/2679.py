def _cur_row(S):
    row = S.get('row')
    if row is None:
        return -1
    for k, r in enumerate(S['nums']):
        if r is row:
            return k
    return -1


def _color(S, i, j, v):
    nums = S['nums']
    if S.get('_line', 0) >= 4:  # 已经全部排好序：每列最大值（最后一行向上数）
        return 'green' if v == max(r[j] for r in nums) else None
    return 'yellow' if i == _cur_row(S) else None


def _txt(S):
    nums = S['nums']
    if S.get('_line', 0) >= 4:
        mx = [max(r[j] for r in nums) for j in range(len(nums[0]))]
        return '每列最大值：' + ' + '.join(f'`{m}`' for m in mx) + f' = =={sum(mx)}=='
    return '先让每一行从小到大排好序'


CONFIG = dict(
    num=2679, title='矩阵中的和', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='每行排序 · 按列取最大',
    tags=[],
    code='''
class Solution:
    def matrixSum(self, nums: List[List[int]]) -> int:
        for row in nums: row.sort()
        return sum(map(max, zip(*nums)))  # zip(*nums) 枚举每一列
''',
    call='Solution().matrixSum([[7,2,1],[6,4,2],[6,5,3],[3,2,1]])',
    expect=15,
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var='nums', color=_color, h=420, label='nums（排序后每列最大值标绿）'),
    ],
    watch=[],
    captions={
        'for row in nums': '每一行各自从小到大排序：这样每行的「当前最大」总在最右边，第 1 轮删最后一列，第 2 轮删倒数第二列……',
        'return sum': lambda S, B, ret: (f'排序后每一列的最大值就是每轮得分；`zip(*nums)` 逐列取出，`max` 取列最大，加起来 =={ret}==')
    },
    cards=dict(
        before=[dict(heading='先手动模拟一遍', lines=['第 1 轮：删 `7, 6, 6, 3`，其中最大 `7` 入分',
                                                     '第 2 轮：删 `2, 4, 5, 2`，其中最大 `5` 入分',
                                                     '第 3 轮：删 `1, 2, 3, 1`，其中最大 `3` 入分 → 共 `15`'])],
        after=[dict(heading='为什么按列', lines=['排序后，同一轮各行删的数恰好在同一列',
                                               '所以「一轮里的最大值」就是「这一列的最大值」',
                                               '不用真的删除元素，列最大值之和即答案'])],
        one_liner='每行排好序，第 j 轮删的就是第 j 大，按列取最大',
        complexity='时间 `O(mn log n)`，空间 `O(1)`',
        problem=['矩阵每一轮：每行删掉最大数，再把删掉的数里最大的一个加进分数',
                 '重复到矩阵变空，求总分',
                 '示例：`[[7,2,1],[6,4,2],[6,5,3],[3,2,1]]` → `7+5+3 = 15`'],
        quote='既然每次选最大的数，那么干脆对每行排序，这样每次就选的是一列的最大值。累加这些最大值，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每行升序排好后，第 1 轮删的是最后一列，第 2 轮删倒数第二列……',
              '每一轮得分 = 这一列的最大值',
              '`zip(*nums)` 把列转成行，`max` 取每列最大，`sum` 累加'],
        summary=['时间 `O(mn log n)`，空间 `O(1)`（忽略排序栈）',
                 '易错点：同一轮每行删的是「各自」当前最大，所以列要在行内对齐（先排序）',
                 '`zip(*nums)` 要求各行等长，本题满足',
                 '这里的 `row.sort()` 会直接改动输入矩阵'],
    ),
)

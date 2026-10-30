NUMS = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def _tri(x):
    return f'{x[0]},{x[1]},{x[2]}'


def _arr(S):
    nl = S.get('num_list')
    if not nl:
        return None
    if S.get('_line') == 8:
        nl = sorted(nl, key=lambda d: (d[0], -d[1]))
    return [_tri(x) for x in nl]


CONFIG = dict(
    num=1424, title='对角线遍历 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='三元组 + 排序',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def findDiagonalOrder(self, nums):
        num_list = []
        for i in range(len(nums)):
            for j in range(len(nums[i])):
                num_list.append([i + j, i, nums[i][j]])
        
        return [x[2] for x in sorted(num_list, key=lambda d:(d[0], -d[1]))]
''',
    call=f'Solution().findDiagonalOrder({NUMS})',
    expect=[1, 4, 2, 7, 5, 3, 8, 6, 9],
    skip=['for j in range'],
    views=[
        dict(type='grid', var='nums', label='nums（黄 = 当前格子 (i,j)；同一反斜线上 i+j 相同）', cell=88, h=300,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='text', h=50, size=26,
             fn=lambda S: (f"当前格子 `({S['i']},{S['j']})`：i + j = =={S['i'] + S['j']}==，三元组 `({S['i'] + S['j']}, {S['i']}, {S['nums'][S['i']][S['j']]})`"
                           if 'j' in S and 'i' in S and S.get('_line') == 6 else
                           ('排序：先按 `i+j` 从小到大，再按 `i` 从大到小' if S.get('_line') == 8 else ''))),
        dict(type='array', var=_arr,
             label='num_list：i+j, i, 值（排序后按此顺序取值）', cell=100, h=170, index=True),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'num_list = []': '准备一个列表，装每个数字的三元组 `(i+j, i, 值)`',
        'num_list.append': '`nums[{i}][{j}] = {nums[i][j]}` 记成三元组 `({i+j}, {i}, {nums[i][j]})`：同一条对角线上 ==i+j 相等==',
        'return [x[2]': lambda S, B, r: f'按 (i+j 升序, i 降序) 排序，取每项的值：同一对角线内先==下面的行==（i 大）后上面的行 → `{r}`',
    },
    cards=dict(
        one_liner='同一条对角线上的格子，横纵坐标之和相等',
        complexity='时间 `O(N log N)`（N 为元素总数），空间 `O(N)`',
        problem=['给一个每行长度可能不同的二维列表 `nums`，按对角线（右上到左下方向）顺序输出所有数字',
                 '同一对角线上，行号大的（靠下的）先输出',
                 '本视频：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,4,2,7,5,3,8,6,9]`'],
        quote='位于同一对角线上的格子，其横纵坐标之和是一样的，于是一个自然的想法是遍历列表中的所有数字，对于位于第i行第j列的数字nums[i][j]，我们将其转化成三元组（i + j, i, nums[i][j]）',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每个数字，记成 `(i+j, i, 值)`',
              '排序：`i+j` 小的对角线在前，同一对角线上 `i` 大的在前',
              '排完取第三项，就是遍历顺序'],
        summary=['时间 `O(N log N)`，主要花在排序；空间 `O(N)`',
                 '易错：第二关键字是 ==-i==（i 从大到小），写成 i 会得到反方向',
                 '遍历要用 `len(nums[i])`，每行长度不同，不能用固定列数',
                 '原文为 Python 2 风格，只删去了 `:type` 说明文档字符串，代码未改'],
    ),
)

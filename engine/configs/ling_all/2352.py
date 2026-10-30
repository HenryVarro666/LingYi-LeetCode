CONFIG = dict(
    num=2352, title='相等行列对', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表统计行 · 列查表',
    tags=[],
    code='''
class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:
        cnt = Counter(tuple(row) for row in grid)
        return sum(cnt[col] for col in zip(*grid))
''',
    call='Solution().equalPairs([[3,2,1],[1,7,6],[2,7,7]])',
    expect=1,
    views=[
        dict(type='grid', var='grid', label='grid（行 R，列 C）', h=260, cell=90),
        dict(type='map', var='cnt', label='cnt：每种行出现的次数', fmt=lambda k, v: f'{list(k)}: {v}', h=200, font=30),
    ],
    watch=[],
    captions={
        'cnt = Counter': '把每一行变成 `tuple`（列表不能当键），统计每种行出现几次：共 =={len(cnt)}== 种',
        'return sum': '`zip(*grid)` 依次给出每一列，`cnt[col]` = 与这一列相等的行有几个，全部加起来 =={ret}==',
    },
    cards=dict(
        after=[dict(heading='为什么要转成 tuple', lines=['`list` 不可哈希，不能直接当 `Counter` 的键','`tuple(row)` 与 `zip(*grid)` 给出的列（也是 tuple）可以直接比较','`cnt[col]` 查的是与这一列相等的行有几行','每一列各自累加，就是所有相等行列对的总数'])],
        one_liner='先数每一行出现几次，再用每一列去查表',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`n x n` 矩阵，求行 `R_i` 与列 `C_j` 完全相同的 `(i, j)` 对数',
                 '相同 = 元素和顺序都一样',
                 '示例：`[[3,2,1],[1,7,6],[2,7,7]]` → `1`'],
        quote='用哈希表统计每行出现的次数，然后遍历列，累加哈希表中列出现的次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['行转成 `tuple` 才能当哈希表的键',
              '`zip(*grid)` 把矩阵转置，每个元素就是一列（也是 tuple）',
              '一列对应的行对数 = 这种行出现的次数，累加即可'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错点：列表不可哈希，必须转 `tuple`',
                 '`Counter` 查不存在的键返回 0，所以不用判断'],
    ),
)

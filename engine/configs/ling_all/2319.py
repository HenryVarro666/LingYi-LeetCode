def _diag(S, i, j, v):
    n = len(S['grid'])
    d = (i == j or i + j == n - 1)
    if d:
        return 'green' if v != 0 else 'red'
    return 'red' if v != 0 else None


CONFIG = dict(
    num=2319, title='判断矩阵是否是一个 X 矩阵', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='对角线下标公式 + all',
    code='''
class Solution:
    def checkXMatrix(self, grid: List[List[int]]) -> bool:
        return all((v != 0) == (i == j or i + j == len(grid) - 1) for i, row in enumerate(grid) for j, v in enumerate(row))
''',
    call='Solution().checkXMatrix([[2,0,0,1],[0,3,1,0],[0,5,2,0],[4,0,0,2]])',
    expect=True,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 对角线上且非 0，其余的 0 不着色，红 = 违规）', cell=96, h=420, color=_diag),
        dict(type='text', size=32, fn=lambda S: '对角线：`i == j`（主）或 `i + j == n − 1`（反），这里 `n − 1 = ' + str(len(S['grid']) - 1) + '`' if 'grid' in S else ''),
    ],
    watch=[],
    captions={
        'return all': '对每个格子检查 `(v != 0) == (在对角线上)`：对角线上必须非 0，其余必须是 0。全部成立 → 返回 =={ret}==',
    },
    cards=dict(
        before=[dict(heading='格子应该满足什么', lines=['对角线上的格子：`v != 0` 必须为真，`i == j` 或 `i + j == n − 1`',
                                                 '其他格子：`v != 0` 必须为假（即 `v == 0`）',
                                                 '两个布尔值==必须相等==：写成 `(v != 0) == (在对角线上)`',
                                                 '四种组合里，只有「一真一假」才是违规']),
                dict(heading='用示例验证', lines=['`(0,0)=2`：在对角线，非 0 → 真 == 真 ✓',
                                              '`(0,1)=0`：不在对角线，是 0 → 假 == 假 ✓',
                                              '`(1,2)=1`：`i + j = 3 = n − 1`，在反对角线，非 0 → 真 == 真 ✓'])],
        one_liner='对角线非 0、其余为 0：两个布尔值相等就合格',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`n × n` 的矩阵，==对角线上的数都不是 0==，==其余的数都是 0== 才是 X 矩阵',
                 '示例：`[[2,0,0,1],[0,3,1,0],[0,5,2,0],[4,0,0,2]]` → `true`'],
        quote='主对角线上的下标需满足：i=j。反对角线上的下标需满足：i+j=n-1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先判断每个格子是不是在对角线上：`i == j or i + j == n - 1`',
              '对角线要非 0、非对角线要为 0 → `(v != 0) == 在对角线上`',
              '`all(...)` 遍历所有格子，只要有一个不满足就返回 `False`'],
        after=[dict(heading='all 的短路', lines=['`all` 遇到第一个 `False` 就立刻返回，不再检查后面的格子',
                                             '本例所有格子都合格，所以遍历了全部 16 个格子才返回 `True`'])],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '主对角线 `i == j`，反对角线 `i + j == n - 1`，注意是 `n - 1` 不是 `n`',
                 '`n` 为奇数时中心格同时在两条对角线上，用 `or` 不会重复判断',
                 '对比 yiduobo：他用循环 + 提前 `return False`，效果相同'],
    ),
)

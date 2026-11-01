def _dug(S):
    n = 3
    d = S.get('d') or {}
    return [[1 if (i, j) in d else 0 for j in range(n)] for i in range(n)]


def _col(S, i, j, v):
    if v:
        return 'green'
    return None


def _cur(S):
    return 'i' in S and 'j' in S


CONFIG = dict(
    num=2201, title='统计可以提取的工件', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表记录挖掘 + 暴力检查（Go 原文转写）',
    code='''
class Solution:
    def digArtifacts(self, _, artifacts: List[List[int]], dig: List[List[int]]) -> int:
        ans = 0
        d = {}
        for p in dig:
            d[(p[0], p[1])] = True
        for art in artifacts:
            for i in range(art[0], art[2] + 1):
                for j in range(art[1], art[3] + 1):
                    if not d.get((i, j), False):
                        break
                else:
                    continue
                break
            else:
                ans += 1
        return ans
''',
    call='Solution().digArtifacts(3, [[0,0,0,0],[0,1,1,1],[1,2,2,2]], [[0,0],[0,1],[1,1],[1,2]])',
    expect=2,
    views=[
        dict(type='grid', var=_dug, label='3×3 网格（绿 = 已挖；黄框 = 正在检查的格子）', cell=110, h=420,
             color=_col, cursors=[('i', 'j', 'yellow')]),
        dict(type='array', var='art', label='当前工件 [r1, c1, r2, c2]', cell=90, h=150),
    ],
    watch=[('art', 'art'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'd[(p[0], p[1])] = True': '记下挖过的格子 `{p}` → d 里共 {len(d)} 个',
        'for art in artifacts': '检查下一个工件 `{art}`：左上 ({art[0]},{art[1]})，右下 ({art[2]},{art[3]})',
        'if not d.get': lambda S, B, r: (f"格子 ({S['i']},{S['j']}) 没挖过 → 这个工件拿不到，==直接 break 跳到下一个工件==（原文 continue next）"
                                         if (S['i'], S['j']) not in S['d'] else f"格子 ({S['i']},{S['j']}) 挖过了，继续看下一格"),
        'ans += 1': '工件的每一格都挖过了 → 可以提取，`ans` = =={ans}==',
        'return ans': '一共可以提取 `{ans}` 个工件',
    },
    cards=dict(
        one_liner='每个工件最多 4 格：挖过的格子进哈希表，逐格查',
        complexity='时间 `O(dig + artifacts)`，空间 `O(dig)`',
        problem=['`n×n` 网格里埋着矩形工件，给出每个工件的左上、右下角', '挖开 `dig` 里的格子，工件所有格子都露出才能提取，求能提取几个',
                 '示例：`n=3` 的 3 个工件，挖 4 格 → `2`'],
        quote='由于每个工件最多只覆盖 4 个单元格，可以用哈希表记录哪些单元格被挖掘过，然后暴力检查每个工件覆盖的格子是否被挖过。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把所有挖掘的格子放进哈希表 `d`', '对每个工件枚举它的每一格，只要有一格不在 `d` 里就放弃', '工件最多 4 格，所以总检查次数不超过 `4×工件数`；参数 n 用不上'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（Go 的 `continue next` 用 for-else 实现）',
                 '时间 `O(dig + artifacts)`（每个工件至多 4 格），空间 `O(dig)`',
                 '易错点：必须整个工件都挖到才算，一格没挖就不行',
                 '对比：yiduobo 用二维前缀和判断面积'],
    ),
)

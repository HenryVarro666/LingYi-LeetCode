def _color(S, i, j, v):
    if 'j' not in S or 'i' not in S:
        return 'green' if (j == 0 or j == i) else None
    ci, cj = S['i'], S['j']
    if i == ci and j == cj:
        return 'orange'
    if i == ci - 1 and j == cj - 1:
        return 'blue'
    if i == ci - 1 and j == cj:
        return 'pink'
    if j == 0 or j == i:
        return 'green'
    return None


def _rows(S):
    if 'c' in S:
        return S['c']
    if 'i' in S:  # 列表推导式还在逐排构造
        return [[1] * (k + 1) for k in range(S['i'] + 1)]
    return None


def _formula(S):
    if 'c' not in S:
        return '列表推导式：第 `i` 排放 `i+1` 个 1' if 'i' in S else ''
    if 'j' not in S:
        return '每排==首尾都是 1==：`c[i][0] = c[i][i] = 1`，其余位置先填 1 占位'
    i, j, c = S['i'], S['j'], S['c']
    return (f"`c[{i}][{j}] = c[{i - 1}][{j - 1}] + c[{i - 1}][{j}]` = "
            f"{c[i - 1][j - 1]} + {c[i - 1][j]} = =={c[i - 1][j - 1] + c[i - 1][j]}==")


def _legend(cv, S, B, box, T):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    for c, t in [('orange', '当前 c[i][j]'), ('blue', '左上方 c[i-1][j-1]'), ('pink', '正上方 c[i-1][j]'),
                 ('green', '首尾的 1')]:
        cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 30


CONFIG = dict(
    num=118, title='杨辉三角', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='左对齐 + 递推',
    code='''
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        c = [[1] * (i + 1) for i in range(numRows)]
        for i in range(2, numRows):
            for j in range(1, i):
                # 左上方的数 + 正上方的数
                c[i][j] = c[i - 1][j - 1] + c[i - 1][j]
        return c
''',
    call='Solution().generate(6)',
    expect=[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var=_rows, label='c（每排左对齐）', color=_color,
             rows=lambda S: [f'i={k}' for k in range(len(_rows(S)))],
             cols=lambda S: [f'j={k}' for k in range(len(_rows(S)))], cell=78, h=560),
        dict(type='custom', draw=_legend, h=46),
    ],
    watch=[('i', 'i', 'orange'), ('j', 'j', 'orange')],
    skip=['for j in'],
    captions={
        'c = [[1]': lambda S, B, ret: ((f'第 `{S.i}` 排放 `{S.i + 1}` 个 1' + ('：==左对齐==存成二维数组' if S.i == 0 else '')) if 'c' not in S
                                       else f'第 `i` 排先填 `i+1` 个 1（==左对齐==），共 `{len(S.c)}` 排：首尾的 1 已经对了，只剩中间要算'),
        'for i in': lambda S, B, ret: (f'第 `{S.i}` 排：首尾已是 1，只需算中间 `j = 1..{S.i - 1}`'
                                       if B.get('i') != S.i else '所有排都算完了'),
        'c[i][j] = c': '左上方 `{c[i-1][j-1]}` + 正上方 `{c[i-1][j]}` → `c[{i}][{j}]` = =={c[i][j]}==',
        'return c': '返回整个三角形，共 `{len(c)}` 排',
    },
    cards=dict(
        one_liner='把每一排左对齐，每个数 = 左上方 + 正上方',
        complexity='时间 `O(numRows²)`，空间 `O(1)`（返回值不计入）',
        problem=['生成「杨辉三角」的前 `numRows` 行',
                 '每个数是它==左上方和右上方==的数的和（居中画法）',
                 '示例：`numRows = 5` → `[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]`'],
        quote='设要计算的二维数组是 c：每一排的第一个数和最后一个数都是 1，即 c[i][0]=c[i][i]=1。==其余数字，等于左上方的数，加上正上方的数==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['居中的「左上 + 右上」，左对齐后变成 ==「左上方 + 正上方」==',
              '先全填 1（首尾就对了），再从第 2 排起填中间',
              '每排只依赖上一排 → 从上往下算，用到的数一定算好了'],
        after=[dict(heading='附：如何理解这个式子（选或不选）', lines=[
            '`c[i][j]` = 从 `i` 个不同物品中选 `j` 个的方案数（组合数）',
            '盯住某一个物品：==选它== → 剩下 `i-1` 个里选 `j-1` 个，即 `c[i-1][j-1]`',
            '==不选它== → 剩下 `i-1` 个里选 `j` 个，即 `c[i-1][j]`',
            '加法原理：`c[i][j] = c[i-1][j-1] + c[i-1][j]`',
        ])],
        summary=['时间 `O(numRows²)`；除返回值外只用 `O(1)` 额外空间',
                 '`[[1] * (i + 1) for ...]` 每排是==独立的列表==；别写成 `[[1]] * n`',
                 '外层从 `i = 2` 开始、内层 `j` 取 `1..i-1`：首尾不用算',
                 '本质是组合数恒等式，「选或不选」是 DP 的基本思考方式'],
    ),
)

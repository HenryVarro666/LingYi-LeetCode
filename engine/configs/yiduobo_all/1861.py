BOX = [["#", ".", "*", "."], ["#", "#", "*", "."]]


def _c(S, i, j, v):
    return {'#': 'orange', '*': 'red'}.get(v)


CONFIG = dict(
    num=1861, title='旋转盒子', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='逐行倒序 · p 记录最上被占的行',
    tags=['难度分 1537'],
    code='''
class Solution(object):
    def rotateTheBox(self, box):

        m = len(box)
        n = len(box[0])

        res = [['.'] * m for _ in range(n)]

        for i in range(m):
            p = n
            for j in range(n - 1, -1, -1):
                if box[i][j] == '*':
                    res[j][m - i - 1] = '*'
                    p = j
                elif box[i][j] == '#':
                    res[p - 1][m - i - 1] = '#'
                    p -= 1

        return res
''',
    call=f'Solution().rotateTheBox({BOX!r})',
    expect=[["#", "."], ["#", "#"], ["*", "*"], [".", "."]],
    views=[
        dict(type='grid', var='box', label='box：第 i 行从右往左扫（# 石头，* 障碍物）', h=220, cell=70, color=_c,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='grid', var='res', label='res：第 i 行 → 第 m−i−1 列；青框 = 下一块石头的落点 p−1', h=360, cell=70, color=_c,
             cursors=[('p - 1 if p > 0 else None', 'm - 1 - i', 'cyan')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('p', 'p', 'cyan')],
    captions={
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列；旋转后答案是 `{n}×{m}`',
        'res = [': '答案先全填 `.`：每一列对应原来的一行',
        'for i in range': '处理原矩阵第 `{i}` 行 → 填进答案的第 `{m - i - 1}` 列（`m - i - 1`）',
        'p = n': '`p` = 答案列中最上面被占用的行号；还没有被占用，所以 `p = n = {p}`',
        'for j in range': lambda S, B, r: ('这一行扫完了' if 'j' in B and B.j == S.j
                                           else f'从右往左（答案里从下往上）：`j = {S.j}`，格子 `{S.box[S.i][S.j]!r}`'),
        "if box[i][j] == '*'": lambda S, B, r: (f'`box[{S.i}][{S.j}] = {S.box[S.i][S.j]!r}`：障碍物' if S.box[S.i][S.j] == '*'
                                                else f'`box[{S.i}][{S.j}] = {S.box[S.i][S.j]!r}`：不是障碍物'),
        "res[j][m - i - 1] = '*'": '障碍物不下落：它的列 `j` 就是答案中的行：`res[{j}][{m - i - 1}] = *`',
        'p = j': '它左侧的石头会被挡住：`p` → =={p}==（`p` 之上才能放石头）',
        "elif box[i][j] == '#'": lambda S, B, r: (f'`box[{S.i}][{S.j}] = {S.box[S.i][S.j]!r}`：石头' if S.box[S.i][S.j] == '#'
                                                  else f'`box[{S.i}][{S.j}]` 是空位，不用处理'),
        "res[p - 1][m - i - 1] = '#'": '石头下落到 `p` 的上一行：`res[{p - 1}][{m - i - 1}] = #`',
        'p -= 1': '这一行被占了：`p` → =={p}==，下一块石头堆在它上面',
        'return res': '旋转后的结果：`{res}`',
    },
    cards=dict(
        one_liner='原来的一行 = 答案里的一列：从右往左填，p 标出最上占用行',
        complexity='时间 `O(mn)`，空间 `O(mn)`（答案矩阵）',
        problem=['`m×n` 的盒子里有石头 `#`、障碍物 `*`、空位 `.`',
                 '顺时针旋转 90 度，石头在重力下垂直掉落，直到碰到障碍物、石头或底部',
                 '示例：`[["#",".","*","."],["#","#","*","."]]`'],
        quote='原始矩阵的第i行对应到的是旋转后的m - i - 1列，且各行各列之间是互补影响的。',
        quote_src='—— yiduobo 题解原文',
        idea=['原来的行在答案里是列，所以逐行处理、逐列填答案',
              '答案列从下往上考虑 = 原来的行从右往左遍历',
              '`p` 初值 `n`：石头落到 `p-1` 再 `p -= 1`；遇障碍物 `p = j`'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（答案矩阵）',
                 '`p` 初始是 `n`，表示答案列里还没有被占用的行',
                 '障碍物的位置不变：原来的列 `j` 就是答案里的行',
                 '原文已是 Python 3 可运行的写法，没有修改',
                 '对比灵神：灵神用 `k` 指向下一个落点（初值 `n-1`），yiduobo 用 `p` 指向最上占用行（落点是 `p-1`）'],
    ),
)

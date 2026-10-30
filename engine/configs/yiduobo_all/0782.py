B0 = [[0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1]]


def _cell(S, i, j, v):
    if i == 0:
        return 'blue'
    return None


def _bits(x, m):
    return format(x, '0%db' % m)


def _fn(S):
    if 'target_col' in S:
        m = S['m']
        return f"行目标 `{_bits(S['target_row'], m)}`，列目标 `{_bits(S['target_col'], m)}`，行需换 {S['res_row']} 次"
    if 'cnt_row' in S:
        return f"与第 0 行相同的行 {S['cnt_row']} 个，与第 0 列相同的列 {S['cnt_col']} 个"
    if 'row' in S and 'col' in S:
        m = S['m']
        return '把每行、每列当成二进制数：行 `' + ' '.join(_bits(x, m) for x in S['row']) + '`'
    return '行和列的操作互不影响，可以分开统计'


CONFIG = dict(
    num=782, title='变为棋盘', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='二进制压缩 · 行列分别统计',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def movesToChessboard(self, board):

        m = len(board)

        row = []
        col = []
        for i in range(m):
            row.append(0)
            for j in range(m):
                row[-1] = (row[-1] << 1) + board[i][j]
        
        for j in range(m):
            col.append(0)
            for i in range(m):
                col[-1] = (col[-1] << 1) + board[i][j]

        cnt_row = cnt_col = 1
        for index in range(1, m):
            if row[index] == row[0]:
                cnt_row += 1
            elif row[index] ^ row[0] != (1 << m) - 1:
                return -1
            
            if col[index] == col[0]:
                cnt_col += 1
            elif col[index] ^ col[0] != (1 << m) - 1:
                return -1

        res_row = res_col = 0
        if cnt_row != m // 2 and cnt_row != (m + 1) // 2:
                return -1
        if cnt_col != m // 2 and cnt_col != (m + 1) // 2:
            return -1

        if cnt_row == m // 2:
            target_row = ((1 << m) - 1) ^ row[0]
        else:
            target_row = row[0]
            
        for index in range(0, m, 2):
            if row[index] != target_row:
                res_row += 1

        if cnt_col == m // 2:
            target_col = ((1 << m) - 1) ^ col[0]
        else:
            target_col = col[0]

        for index in range(0, m, 2):
            if col[index] != target_col:
                res_col += 1

        if m % 2 == 0:
            res_row = min(m // 2 - res_row, res_row)
            res_col = min(m // 2 - res_col, res_col)
        
        return res_col + res_row
''',
    call=f'Solution().movesToChessboard({B0})',
    expect=2,
    skip=['m = len', 'row.append', 'col.append', 'for j in range(m)', 'for i in range(m)', 'cnt_row = cnt_col', 'res_row = res_col',
          'for index in range(1, m)', 'for index in range(0, m, 2)'],
    views=[
        dict(type='grid', var='board', label='board（蓝 = 第 0 行）', h=290, cell=66, color=_cell),
        dict(type='text', fn=_fn, size=22, h=60),
        dict(type='array', var='row', label='row：每行压成二进制数', h=150, cell=70),
        dict(type='array', var='col', label='col：每列压成二进制数', h=150, cell=70),
    ],
    watch=['cnt_row', 'cnt_col', 'index', 'res_row', 'res_col'],
    captions={
        'row[-1] = (row[-1] << 1)': '`row[{i}]` 逐位拼成二进制：目前 = =={row[-1]}==',
        'col[-1] = (col[-1] << 1)': '`col[{j}]` 逐位拼成二进制：目前 = =={col[-1]}==',
        'if row[index] == row[0]': lambda S, B, r: f'`row[{S.index}] = {S.row[S.index]}` 与 `row[0] = {S.row[0]}` ' + ('相同 → 归为一类，`cnt_row` + 1' if S.row[S.index] == S.row[0] else '不同 → 看是不是逐位相反'),
        'elif row[index] ^ row[0]': lambda S, B, r: ('异或 = `' + str(S.row[S.index] ^ S.row[0]) + '` = 全 1 → 与第 0 行==逐位相反==，合法' if S.row[S.index] ^ S.row[0] == (1 << S.m) - 1 else '既不相同也不相反 → 无解，返回 -1'),
        'if col[index] == col[0]': lambda S, B, r: f'`col[{S.index}] = {S.col[S.index]}` 与 `col[0] = {S.col[0]}` ' + ('相同 → 归为一类，`cnt_col` + 1' if S.col[S.index] == S.col[0] else '不同 → 看是不是逐位相反'),
        'elif col[index] ^ col[0]': lambda S, B, r: ('异或 = `' + str(S.col[S.index] ^ S.col[0]) + '` = 全 1 → 与第 0 列==逐位相反==，合法' if S.col[S.index] ^ S.col[0] == (1 << S.m) - 1 else '既不相同也不相反 → 无解，返回 -1'),
        'if cnt_row != m': lambda S, B, r: f'与第 0 行相同的行有 `{S.cnt_row}` 个，应为 ' + (f'`{S.m // 2}`' if S.m % 2 == 0 else f'`{S.m // 2}` 或 `{(S.m + 1) // 2}`') + ' → ' + ('数量不对，返回 -1' if S.cnt_row not in (S.m // 2, (S.m + 1) // 2) else '数量合格'),
        'if cnt_col != m': lambda S, B, r: f'与第 0 列相同的列有 `{S.cnt_col}` 个，应为 ' + (f'`{S.m // 2}`' if S.m % 2 == 0 else f'`{S.m // 2}` 或 `{(S.m + 1) // 2}`') + ' → ' + ('数量不对，返回 -1' if S.cnt_col not in (S.m // 2, (S.m + 1) // 2) else '数量合格'),
        'if cnt_row == m': lambda S, B, r: f'`cnt_row = {S.cnt_row}`' + (' == m//2 → 第 0 行取反当首行' if S.cnt_row == S.m // 2 else ' → 第 0 行本身当首行'),
        'target_row = ((1 << m)': '首行目标 `target_row` = `{target_row}`（第 0 行逐位取反）',
        'target_row = row[0]': '首行目标 `target_row` = `{target_row}`',
        'if row[index] != target_row': lambda S, B, r: f'偶数位 `row[{S.index}] = {S.row[S.index]}` ' + ('≠ ' if S.row[S.index] != S.target_row else '= ') + f'目标 `{S.target_row}` ' + ('→ 需要换一次，`res_row` + 1' if S.row[S.index] != S.target_row else '→ 已就位'),
        'if cnt_col == m': lambda S, B, r: f'`cnt_col = {S.cnt_col}`' + (' == m//2 → 第 0 列取反当首列' if S.cnt_col == S.m // 2 else ' → 第 0 列本身当首列'),
        'target_col = ((1 << m)': '首列目标 `target_col` = `{target_col}`',
        'target_col = col[0]': '首列目标 `target_col` = `{target_col}`',
        'if col[index] != target_col': lambda S, B, r: f'偶数位 `col[{S.index}] = {S.col[S.index]}` ' + ('≠ ' if S.col[S.index] != S.target_col else '= ') + f'目标 `{S.target_col}` ' + ('→ 需要换一次，`res_col` + 1' if S.col[S.index] != S.target_col else '→ 已就位'),
        'if m % 2 == 0': lambda S, B, r: ('m 是偶数：首行有 0101 / 1010 两种选法，取较小' if S.m % 2 == 0 else 'm 是奇数：目标唯一，不用比较'),
        'res_row = min': '`res_row = min({m//2} - {B.res_row}, {B.res_row})` = =={res_row}==',
        'res_col = min': '`res_col = min({m//2} - {B.res_col}, {B.res_col})` = =={res_col}==',
        'return res_col + res_row': '列 `{res_col}` + 行 `{res_row}` = =={ret}==',
    },
    cards=dict(
        one_liner='行列互不影响，压成二进制后和第 0 行比：相同或取反',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n×n` 的 0/1 矩阵，每次交换任意两行或两列',
                 '求变成「棋盘」的最少次数，不可能返回 `-1`',
                 '示例：`[[0,1,1,0],[0,1,1,0],[1,0,0,1],[1,0,0,1]]` → `2`'],
        quote='所有行的分布只能与第0行row[0]完全一致，或者与row[0]逐位相反……这个结论在列上也成立。',
        quote_src='—— yiduobo 题解原文',
        idea=['横竖操作互不影响，行和列分开处理',
              '每行/每列压成二进制数：只能等于第 0 个，或等于它的按位取反',
              '数量要对：与第 0 个相同的个数是 `n//2` 或 `(n+1)//2`',
              '选定首行目标，隔一行（偶数位）检查是否就位，不对的就要换一次'],
        summary=['时间 `O(n^2)`，空间 `O(n)`；`n ≤ 30` 所以二进制压缩没有问题',
                 '偶数 `n`：首行有两种选法，`res` 与 `n/2 - res` 取较小；奇数 `n` 目标唯一',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神用「0/1 个数之差」+ 异或 diff 数，yiduobo 用二进制压缩 + 隔行数就位数'],
    ),
)

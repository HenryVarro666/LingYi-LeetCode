def _cell(S, r, c):
    v = S['board'][r][c]
    return 'None（用过了）' if v is None else f"'{v}'"


def _check(S, B, ret):
    dx, dy = S.dx, S.dy
    if not (0 <= dx < len(S.board) and 0 <= dy < len(S.board[0])):
        return f'`({dx}, {dy})` ==出界== → 不能走'
    v = S.board[dx][dy] if len(S.get('board', [])) else None
    if 'level' in S and B.get('level') == S.level and B.board[dx][dy] is None:
        return f'`({dx}, {dy})` 是 `None`：==已经用过== → 和任何字母都对不上，不能走'
    if B.board[dx][dy] != S.word[S.level]:
        return f"`board[{dx}][{dy}] = '{B.board[dx][dy]}' ≠ word[{S.level}] = '{S.word[S.level]}'` → 对不上"
    return f"`board[{dx}][{dy}] = '{B.board[dx][dy]}'` 对上 `word[{S.level}]`，且没用过 → ==可以走=="


def _for_index(S, B, ret):
    if 'index' in S and (S.index != B.get('index') or (S.x, S.y) != (B.get('x'), B.get('y')) or S.level != B.get('level')):
        d = ['右', '左', '下', '上'][S.index]
        return f'试方向 `move[{S.index}] = {S.move[S.index]}`（向{d}）'
    return f'`({S.x}, {S.y})` 四个方向都试过了'


def _ndx(S):  # 当前方向指向的下一个点（dy 那行合并进 dx 那一步显示）
    return S['x'] + S['move'][S['index']][0]


def _ndy(S):
    return S['y'] + S['move'][S['index']][1]


CONFIG = dict(
    num=79, title='单词搜索', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯 · 用过的点置为 None',
    code='''
class Solution(object):
    def exist(self, board, word):
        if not board:
            return False

        if not word:
            return True

        move = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        for i, line in enumerate(board):
            for j, char in enumerate(line):
                if char == word[0]:
                    tmp = board[i][j]
                    board[i][j] = None
                    if self.dfs(1, board, i, j, move, word):
                        return True
                    board[i][j] = tmp

        return False

    def dfs(self, level, board, x, y, move, word):
        if level == len(word):
            return True

        for index in range(len(move)):
            dx = x + move[index][0]
            dy = y + move[index][1]
            if dx >= 0 and dx < len(board) and dy >= 0 and dy < len(board[0]) and board[dx][dy] == word[level]:
                tmp = board[dx][dy]
                board[dx][dy] = None
                if self.dfs(level + 1, board, dx, dy, move, word):
                    return True
                board[dx][dy] = tmp

        return False
''',
    call="Solution().exist([['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], 'SEE')",
    expect=True,
    views=[
        dict(type='grid', var='board', label='board（橙 = None 已用过；黄框 = 当前点，粉框 = 下一步 (dx,dy)）', cell=64, h=260,
             cursors=[('i', 'j', 'cyan'), ('x', 'y', 'yellow'), (_ndx, _ndy, 'pink')],
             color=lambda S, i, j, v: 'orange' if v is None else None),
        dict(type='string', var='word', label='word（绿 = 已匹配，蓝 = 要匹配的 word[level]）', cell=60, h=120,
             color=lambda S, i, v: ('green' if i < S['level'] else ('blue' if i == S['level'] else None)) if 'level' in S else ('blue' if i == 0 else None)),
        dict(type='calls', h=210),
    ],
    watch=[('level', 'level', 'blue'), ('(x, y)', '(x, y)', 'yellow'), ('(dx, dy)', lambda S: (_ndx(S), _ndy(S)), 'pink'), ('tmp', 'tmp')],
    skip=['dy = y + move[index][1]'],
    captions={
        'if not board': '`board` 非空，继续',
        'if not word': '`word` 非空，继续',
        'move = [[0, 1]': '四个方向：右 `[0,1]`、左 `[0,-1]`、下 `[1,0]`、上 `[-1,0]`',
        'for i, line in enumerate(board)': lambda S, B, ret: (
            f'在 board 中枚举 word 的起点：第 `{S.i}` 行' if S.i != B.get('i') else '所有起点都试过了'),
        'for j, char in enumerate(line)': lambda S, B, ret: (
            f"看格子 `({S.i}, {S.j})` = `'{S.char}'`" if (S.j, S.i) != (B.get('j'), B.get('i')) else f'第 `{S.i}` 行看完了'),
        'if char == word[0]': lambda S, B, ret: (
            f"`'{S.char}' == word[0]` → 以 `({S.i}, {S.j})` 为起点" if S.char == S.word[0] else
            f"`'{S.char}' ≠ word[0] = '{S.word[0]}'`，不能当起点"),
        'tmp = board[i][j]': "先把 `'{tmp}'` 存进 `tmp`，回溯时要还原",
        'board[i][j] = None': '把用过的点置为 `None`：之后比较字符时==自然对不上==，起到去重作用',
        'if self.dfs(1, board': '起点匹配了 `word[0]`，从 `level = 1` 开始往四周探索',
        17: '搜索成功 → 返回 `True`',
        'board[i][j] = tmp': "以 `({i}, {j})` 为起点搜不到，还原成 `'{tmp}'`，换下一个起点",
        'if level == len(word)': lambda S, B, ret: (
            f'`level == len(word)`（{S.level} == {len(S.word)}）→ ==整个 word 都对上了==' if S.level == len(S.word) else
            f"`level = {S.level}`：在 `({S.x}, {S.y})` 四周找 `word[{S.level}] = '{S.word[S.level]}'`"),
        24: '返回 `True`',
        'for index in range(len(move))': _for_index,
        'dx = x + move[index][0]': '下一个点 `(dx, dy) = ({dx}, {y + move[index][1]})`',
        'if dx >= 0 and dx < len(board)': _check,
        'tmp = board[dx][dy]': "存下 `tmp = '{tmp}'`",
        'board[dx][dy] = None': '`({dx}, {dy})` 置为 `None`，标记已使用',
        'if self.dfs(level + 1': '加入这个点，进行下一步探索：`level` → {level}',
        33: '下一层搜到了 → 一路返回 `True`',
        'board[dx][dy] = tmp': "这条路走不通：`({dx}, {dy})` 还原成 `'{tmp}'`",
        'return False': '四个方向都走不通 → 返回 `False`',
    },
    max_steps=74,
    cards=dict(
        one_liner='走过的点置为 None，比较字符时自然去重',
        complexity='时间 `O(mn·3^k)`，空间 `O(k)`（递归深度）',
        problem=['在 `m×n` 字母网格里，能否沿上下左右相邻格子拼出 `word`（同一格不能重复用）',
                 "示例：第 1 个示例的 board，`word = \"SEE\"` → `true`"],
        quote='需要满足这些点的字符能与 word 中的字符对上，且没有被使用过。==我的做法是将使用过的点置为 None==，然后在判断字符是否能与 word 中的字符对上时就起到了去重的作用。',
        quote_src='—— yiduobo 题解',
        idea=['外层枚举起点：`char == word[0]` 才开始搜',
              '`dfs(level, …)`：已经匹配了 `word[0..level-1]`，在四周找 `word[level]`',
              '`None` 和任何字母都不相等 → 一次比较同时完成「匹配 + 判重」'],
        result='从 `(1,3)` 出发找到 `S → E → E` ✓',
        summary=['时间 `O(mn·3^k)`：除了起点，每步最多 3 个没走过的方向',
                 '先置 `None` 再递归，失败后用 `tmp` 还原（恢复现场）',
                 '第一个 S `(1,0)` 四周没有 E → 还原后换下一个起点',
                 '原文提到：若有长度/不拐弯限制可用自动机，本题只能搜索回溯',
                 '原文为 Python 2 风格，仅删去 docstring，其余代码未改'],
    ),
)

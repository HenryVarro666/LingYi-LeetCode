SOL = ["534678912", "672195348", "198342567", "859761423", "426853791",
       "713924856", "961537284", "287419635", "345286179"]
BLANKS = [(0, 2), (1, 2), (2, 2), (2, 4), (2, 5)]
BOARD = [list(r) for r in SOL]
for _i, _j in BLANKS:
    BOARD[_i][_j] = '.'


def _cur(S):
    inner = S.get('_inner', {})
    if 'i' in inner and 'j' in inner and S.get('_line', 0) >= 26:
        return inner['i'], inner['j']
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    bd = S.get('board')
    if bd is None:
        return
    cs = min(46, (y1 - y0 - 50) / 9)
    bx, by = x0 + 24, y0 + 40
    cv.text((bx, y0 + 4), '数独（黄 = 原来的空格，绿 = 已填，蓝框 = 当前格子）', 20, T['muted'], bold=True)
    cur = _cur(S)
    x = S.get('_inner', {}).get('x')
    for i in range(9):
        for j in range(9):
            X, Y = bx + j * cs, by + i * cs
            blank = (i, j) in BLANKS
            v = bd[i][j]
            fill = T['panel2']
            if blank:
                fill = T['green'] if v != '.' else (90, 78, 30)
            cv.rect((X + 1, Y + 1, X + cs - 1, Y + cs - 1), fill=fill, r=4)
            if v != '.':
                cv.text((X + cs / 2, Y + cs / 2), v, 22, T['bg'] if blank else T['text'], anchor='mm', bold=blank)
    for t in range(4):
        cv.line([(bx, by + t * 3 * cs), (bx + 9 * cs, by + t * 3 * cs)], T['muted'], 3)
        cv.line([(bx + t * 3 * cs, by), (bx + t * 3 * cs, by + 9 * cs)], T['muted'], 3)
    if cur:
        i, j = cur
        X, Y = bx + j * cs, by + i * cs
        cv.rect((X - 2, Y - 2, X + cs + 2, Y + cs + 2), outline=T['blue'], width=4, r=6)
    # 右侧：当前格子的行 / 列 / 宫集合
    rx = bx + 9 * cs + 30
    if cur and 'row_set' in S:
        i, j = cur
        rows = [(f'row_set[{i}]', S['row_set'][i]), (f'col_set[{j}]', S['col_set'][j]),
                (f'sub_box_set[{i // 3}][{j // 3}]', S['sub_box_set'][i // 3][j // 3])]
        yy = by
        cv.text((rx, yy), f'格子 ({i},{j}) 的三个集合：', 20, T['muted'], bold=True)
        yy += 34
        for name, st in rows:
            cv.text((rx, yy), name, 18, T['muted'], mono=True)
            yy += 24
            for d in range(1, 10):
                X = rx + (d - 1) * 30
                on = d in st
                hi = d == x and S.get('_line') == 35
                cv.rect((X, yy, X + 26, yy + 26), fill=T['orange'] if on else T['panel2'], r=4,
                        outline=T['blue'] if hi else T['border'], width=3 if hi else 1)
                cv.text((X + 13, yy + 13), d, 16, T['bg'] if on else T['dim'], anchor='mm', bold=True)
            yy += 40
        allset = S['row_set'][i] | S['col_set'][j] | S['sub_box_set'][i // 3][j // 3]
        left = [d for d in range(1, 10) if d not in allset]
        cv.text((rx, yy), f'三个集合都没有的：{left}', 20, T['green'], bold=True)


def _heap_fmt(t):
    return f'{t[0]}:({t[1]},{t[2]})'


def _xif(S, B, ret):
    x, i, j = S.x, S.i, S.j
    where = []
    if x in S.row_set[i]:
        where.append(f'第 {i} 行')
    if x in S.col_set[j]:
        where.append(f'第 {j} 列')
    if x in S.sub_box_set[i // 3][j // 3]:
        where.append('同一宫')
    if where:
        return f'`x = {x}` 在' + '、'.join(where) + '已出现 → continue'
    return f'`x = {x}` 行、列、宫都没有 → ==可以填=='


CONFIG = dict(
    num=37, title='解数独', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='回溯 · 最小堆优先填候选最少的格子',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    setup='from string import digits',
    code='''
class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        row_set = [set() for _ in range(9)]  # 每行填入的数字
        col_set = [set() for _ in range(9)]  # 每列填入的数字
        sub_box_set = [[set() for _ in range(3)] for _ in range(3)]  # 每宫填入的数字
        empty_pos = []  # 空格子的位置

        for i, row in enumerate(board):
            for j, b in enumerate(row):
                if b == '.':
                    empty_pos.append((i, j))  # 记录空格子的位置
                else:
                    x = int(b)
                    # 标记行、列、宫包含数字 x
                    row_set[i].add(x)
                    col_set[j].add(x)
                    sub_box_set[i // 3][j // 3].add(x)

        # get_candidates(i, j) 计算 (i, j) 这个空格子的待定数字个数，最小的在堆顶
        get_candidates = lambda i, j: 9 - len(row_set[i] | col_set[j] | sub_box_set[i // 3][j // 3])
        empty_heap = [(get_candidates(i, j), i, j) for i, j in empty_pos]
        heapify(empty_heap)

        # 每次递归，选一个空格子，枚举填入的数字
        def dfs() -> bool:
            if not empty_heap:  # 所有格子都已填入数字
                return True  # 完成数独

            # 数独玩法：优先考虑待定数字个数最少的空格子
            _, i, j = heappop(empty_heap)

            candidates = 0  # 受之前填入的数字影响，实际待定数字个数可能比入堆时的少，需要重新计算
            # 枚举 1~9 中没填过的数字 x，填入 board[i][j]
            for x in range(1, 10):
                if x in row_set[i] or x in col_set[j] or x in sub_box_set[i // 3][j // 3]:
                    continue  # x 填过了

                # 把数字 x 转成字符，填入 board[i][j]
                board[i][j] = digits[x]
                # 标记行、列、宫包含数字 x
                row_set[i].add(x)
                col_set[j].add(x)
                sub_box_set[i // 3][j // 3].add(x)

                # 填下一个空格子
                if dfs():
                    return True  # 完成数独

                # 恢复现场（撤销）
                # 注意 board[i][j] 无需恢复现场，因为我们会直接覆盖掉之前填入的数字
                row_set[i].remove(x)
                col_set[j].remove(x)
                sub_box_set[i // 3][j // 3].remove(x)

                # 统计待定数字个数
                candidates += 1

            # 恢复现场（撤销）
            heappush(empty_heap, (candidates, i, j))  # 重新入堆（更新待定数字个数）
            # 所有填法都不行，说明之前（祖先节点）的填法是错的
            return False

        dfs()
''',
    call=f'board = {BOARD}\nSolution().solveSudoku(board)\n["".join(r) for r in board]',
    expect=SOL,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='heap', var='empty_heap', label='empty_heap（待定个数:(i,j)）', fmt=_heap_fmt, h=110),
        dict(type='calls', h=120),
    ],
    watch=[('i', lambda S: S['_inner'].get('i') if S.get('_line', 0) >= 26 else None, 'blue'),
           ('j', lambda S: S['_inner'].get('j') if S.get('_line', 0) >= 26 else None, 'blue'),
           ('x', lambda S: S['_inner'].get('x'), 'pink'), ('candidates', lambda S: S['_inner'].get('candidates'))],
    skip=[3, 4, 5, 6, 8, 9, 10, 11, 13, 15, 16, 17, 34, 36, 41, 42],
    captions={
        20: '初始化完成：`row_set / col_set / sub_box_set` 记下了每行、每列、每宫已有的数字',
        21: lambda S, B, ret: '每个空格子算出待定数字个数，组成三元组 `(candidates, i, j)`：' + '、'.join(f'`{c}:({i},{j})`' for c, i, j in S.empty_heap),
        22: '`heapify` 成最小堆：==待定数字最少的格子在堆顶==',
        26: lambda S, B, ret: ('堆空了：所有格子都已填入数字 → ==完成数独==' if not S.empty_heap
                               else f'还有 `{len(S.empty_heap)}` 个空格子'),
        27: '返回 `True`',
        30: lambda S, B, ret: f'弹出堆顶 `({B.empty_heap[0][0]}, {S.i}, {S.j})`：数独玩法，==先填待定数字最少的格子==',
        32: lambda S, B, ret: ('入堆时它有 `3` 个待定数字，但前面填的数已经把它压到只剩 `1` 个' if (S.i, S.j) == (2, 2)
                               else '`candidates` 重新统计实际待定个数（失败时才用得上）'),
        35: _xif,
        39: '`board[{i}][{j}] = digits[{x}]`：把数字转成字符填进去',
        43: '标记第 `{i}` 行、第 `{j}` 列、`({i // 3},{j // 3})` 宫都有了 `{x}`',
        46: '填下一个空格子：递归 `dfs()`',
        47: '后面的格子全填好了 → 一路返回 `True`',
        63: '开始回溯 `dfs()`：每层从堆顶取一个格子，枚举填入的数字',
    },
    max_steps=75,
    cards=dict(
        one_liner='像玩数独一样：每次先填待定数字最少的空格子',
        complexity='时间 `O(9^m·log m)`（上界，实际远小于），空间 `O(m)`',
        problem=['`9×9` 数独，`\'.\'` 是空格；每行、每列、每个 `3×3` 宫中 `1~9` 各出现一次',
                 '原地填好 `board`，保证有唯一解',
                 '本视频：示例 1 的解答盘面挖掉 5 个格子'],
        quote='游玩数独的技巧之一是，==优先填待定数字最少的空格子==……用一个最小堆维护三元组 `(candidates,i,j)`，那么堆顶就是 candidates 最少的空格子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三组集合 `row_set / col_set / sub_box_set` 维护行、列、宫已有的数字',
              '`(i, j)` 在 `(i // 3, j // 3)` 这个宫；待定个数 = `9 - |三个集合的并|`',
              '堆不动态修改：恢复现场时把==重新统计==的 `candidates` 再入堆'],
        summary=['复杂度上界 `O(9^m·log m)`，`m ≤ 81` 是空格数，优先填候选少的格子让实际搜索很小',
                 '`board[i][j]` 不用恢复现场：下次直接覆盖',
                 '三个集合在递归返回后==都要 remove==，再把格子重新入堆',
                 '`digits` 来自 `string.digits`（`digits[x]` 就是字符 `x`）',
                 '本例每次都只有一个可填数字，没有走到撤销；有多个候选时才会 remove + 重新入堆',
                 '前置题：36. 有效的数独、46. 全排列；更高级的做法是 Dancing Links'],
    ),
)

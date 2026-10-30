B0 = [[0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1]]


def _ri(S):
    row = S.get('row')
    if row is None:
        return None
    for i, r in enumerate(S['board']):
        if r is row:
            return i
    return None


def _cell(S, i, j, v):
    ri = _ri(S)
    if ri is not None and S.get('_line') not in (None,):
        if i == ri and ri != 0:
            return 'yellow'
    if i == 0:
        return 'blue'
    return None


def _fn(S):
    if 'diff' in S and 's' in S:
        s, n = S['s'], len(S['s'])
        t = ''.join(str(i % 2 ^ S['x0']) for i in range(n))
        return f"s = `{''.join(map(str, s))}`，目标 t = `{t}`，不同位置 diff = =={S['diff']}=="
    if 'row_cnt' in S:
        return '先看第一行、第一列的 0/1 个数，再逐行和第一行比较'
    return ''


CONFIG = dict(
    num=782, title='变为棋盘', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='逆向思维 · 行列独立',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution:
    def movesToChessboard(self, board: List[List[int]]) -> int:
        # 第一行，0 和 1 的个数之差不能超过 1
        first_row = board[0]
        row_cnt = Counter(first_row)
        if abs(row_cnt[0] - row_cnt[1]) > 1:
            return -1

        # 第一列，0 和 1 的个数之差不能超过 1
        first_col = list(next(zip(*board)))
        col_cnt = Counter(first_col)
        if abs(col_cnt[0] - col_cnt[1]) > 1:
            return -1

        # 每一行和第一行比较，要么完全相同，要么完全不同
        for row in board:
            same = row[0] == first_row[0]
            for x, y in zip(row, first_row):
                if (x == y) != same:
                    return -1

        # 计算最小交换次数
        def min_swap(s: List[int], cnt: Counter) -> int:
            n = len(s)
            x0 = 1 if cnt[1] > cnt[0] else 0  # 如果 n 是偶数，x0 是 0
            # 计算规则见题解正文最后一段，这里 t[i] = i % 2 ^ x0
            diff = sum(x ^ i % 2 ^ x0 for i, x in enumerate(s))
            return diff // 2 if n % 2 else min(diff, n - diff) // 2

        return min_swap(first_row, row_cnt) + min_swap(first_col, col_cnt)
''',
    call=f'Solution().movesToChessboard({B0})',
    expect=2,
    skip=['same = row[0]', 'for x, y in zip', 'n = len(s)'],
    views=[
        dict(type='grid', var='board', label='board（蓝 = 第一行，黄 = 正在和第一行比较的行）', h=300, cell=70, color=_cell),
        dict(type='text', fn=_fn, size=24, h=60),
        dict(type='array', var='first_row', label='first_row', h=150, cell=70),
        dict(type='array', var='first_col', label='first_col', h=150, cell=70),
    ],
    watch=['row_cnt', 'col_cnt', 'same', 'diff'],
    captions={
        'first_row = board[0]': '以第一行为==参照物==：能变成棋盘的行只有 A（0101…）和 B（1010…）两种',
        'abs(row_cnt[0]': lambda S, B, r: f'第一行 0 有 `{S.row_cnt[0]}` 个，1 有 `{S.row_cnt[1]}` 个，差 `{abs(S.row_cnt[0]-S.row_cnt[1])}` ' + ('> 1 → 不可能' if abs(S.row_cnt[0]-S.row_cnt[1]) > 1 else '≤ 1 → 继续'),
        'first_col = list': '第一列取出来：`{first_col}`，列和行完全对称',
        'abs(col_cnt[0]': lambda S, B, r: f'第一列 0 有 `{S.col_cnt[0]}` 个，1 有 `{S.col_cnt[1]}` 个，差 `{abs(S.col_cnt[0]-S.col_cnt[1])}` ' + ('> 1 → 不可能' if abs(S.col_cnt[0]-S.col_cnt[1]) > 1 else '≤ 1 → 继续'),
        'for row in board': '逐行和第一行比：要么==完全相同==，要么==完全相反==，否则无解',
        'if (x == y) != same': lambda S, B, r: ('这一列和第一行' + ('相同' if S.x == S.y else '不同') + '，与整行判定 `same = ' + str(S.same) + '` ' + ('不一致 → 返回 -1' if (S.x == S.y) != S.same else '一致')),
        'def min_swap': '行、列各自独立：把一个 0/1 串换成 0101… 或 1010… 的最少交换',
        'x0 = 1 if': '`x0 = {x0}`：n 为奇数时多的那个数必须在偶数下标，偶数时先取 0',
        'diff = sum': '`diff` = 与目标 `t[i] = i%2^x0` 不同的位数 = =={diff}==，每次交换能修好 2 位',
        'return diff // 2': '偶数长度两种目标都行：`min({diff}, {n}-{diff}) // 2` = =={ret}==',
        'return min_swap(first_row': '分别算第一行、第一列的最少交换次数，然后相加',
    },
    cards=dict(
        one_liner='行和列互不影响：各自算最少交换，相加',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n×n` 的 0/1 矩阵，每次可交换任意两行或两列',
                 '求变成「棋盘」（上下左右都不同）的最少次数，不行返回 `-1`',
                 '示例：`[[0,1,1,0],[0,1,1,0],[1,0,0,1],[1,0,0,1]]` → `2`'],
        quote='以 board 第一行（或者任意一行）为参照物。……对于其余行，要么和第一行完全相同，要么完全不同。',
        quote_src='—— 灵茶山艾府题解',
        idea=['必要条件：只有 A、B 两种行，且个数相差不超过 1；列同理',
              '满足后行列独立：第一行换成 0101…，第一列也一样',
              '定理：与目标有 `diff` 个位置不同，只需 `diff/2` 次交换'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：偶数长度要在 0101… 和 1010… 两个目标里取小；奇数只有一个目标',
                 '列的判断用第一列计数，行的判断用逐行对比，两者不能漏',
                 '同类：逆向/对称性思维题，先找必要条件再证充分'],
    ),
)

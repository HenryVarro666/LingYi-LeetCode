IMG = [[5, 6, 7, 10], [8, 9, 10, 10], [11, 12, 13, 10]]


def _in_win(S, r, c):
    return 'i' in S and S['_line'] <= 30 and 'j' in S and S['i'] - 2 <= r <= S['i'] and S['j'] - 2 <= c <= S['j']


def _col_a(S, r, c, v):
    return 'blue' if _in_win(S, r, c) else None


def _col_res(S, r, c, v):
    if 'cnt' in S and S['_line'] >= 32 and S['cnt'][r][c] > 0:
        return 'green'
    return 'blue' if _in_win(S, r, c) and S['_line'] >= 27 else None


def _col_cnt(S, r, c, v):
    return 'green' if v > 0 else None


def _info(S):
    if 'cnt' not in S:
        return ''
    ln = S['_line']
    if ln <= 30 and 'j' in S:
        i, j = S['i'], S['j']
        return f"子网格 右下角 `({i},{j})`：行 {i-2}..{i}，列 {j-2}..{j}" + (f"，平均 `avg` = =={S['avg']}==" if 'avg' in S and ln >= 25 else '')
    if ln >= 32 and 'j' in S:
        return f"`cnt[{S['i']}][{S['j']}] = {S['cnt'][S['i']][S['j']]}`：被 {S['cnt'][S['i']][S['j']]} 个合法子网格覆盖"
    return ''


CONFIG = dict(
    num=3030, title='找出网格的区域平均强度', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='枚举 3×3 子网格 + 累加计数',
    tags=[],
    code='''
class Solution:
    def resultGrid(self, a: List[List[int]], threshold: int) -> List[List[int]]:
        m, n = len(a), len(a[0])
        result = [[0] * n for _ in range(m)]
        cnt = [[0] * n for _ in range(m)]
        for i in range(2, m):
            for j in range(2, n):
                # 检查左右相邻格子
                ok = True
                for row in a[i - 2: i + 1]:
                    if abs(row[j - 2] - row[j - 1]) > threshold or abs(row[j - 1] - row[j]) > threshold:
                        ok = False
                        break  # 不合法，下一个
                if not ok: continue

                # 检查上下相邻格子
                for y in range(j - 2, j + 1):
                    if abs(a[i - 2][y] - a[i - 1][y]) > threshold or abs(a[i - 1][y] - a[i][y]) > threshold:
                        ok = False
                        break  # 不合法，下一个
                if not ok: continue

                # 合法，计算 3x3 子网格的平均值
                avg = sum(a[x][y] for x in range(i - 2, i + 1) for y in range(j - 2, j + 1)) // 9

                # 更新 3x3 子网格内的 result
                for x in range(i - 2, i + 1):
                    for y in range(j - 2, j + 1):
                        result[x][y] += avg  # 先累加，最后再求平均值
                        cnt[x][y] += 1

        for i, row in enumerate(cnt):
            for j, c in enumerate(row):
                if c == 0:  # (i,j) 不属于任何子网格
                    result[i][j] = a[i][j]
                else:
                    result[i][j] //= c  # 求平均值
        return result
''',
    call=f'Solution().resultGrid({IMG}, 3)',
    expect=[[9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9]],
    skip=[3, 4, 5, 9, 10, 17, 27, 28, 30, 32, 33, 34],
    max_steps=120,
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='grid', var='a', label='a（蓝 = 当前 3×3 子网格）', cell=70, h=230, color=_col_a),
        dict(type='grid', var='result', label='result（累加各子网格的 avg；绿 = 已确定）', cell=70, h=230,
             color=_col_res, cursors=[('x if 27 <= _line <= 30 else None', 'y', 'yellow')]),
        dict(type='grid', var='cnt', label='cnt（被多少个合法子网格覆盖）', cell=70, h=230, color=_col_cnt,
             cursors=[('x if 27 <= _line <= 30 else (i if _line >= 32 else None)', 'y if 27 <= _line <= 30 else j', 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), 'ok', ('avg', 'avg', 'green'), 'threshold'],
    captions={
        6: lambda S, B, r: (f'枚举子网格的==右下角== `(i, j)`，所以从 `2` 开始，`i = {S.i}`' if getattr(B, 'i', None) != S.i or getattr(B, 'cnt', None) is None else '所有子网格枚举完了'),
        7: lambda S, B, r: (f'子网格右下角 `({S.i}, {S.j})`，覆盖行 `{S.i-2}..{S.i}`、列 `{S.j-2}..{S.j}`' if getattr(B, 'j', None) != S.j else '这一行的子网格枚举完了'),
        'if abs(row[j - 2]': lambda S, B, r: (
            f"左右相邻：`|{B.row[B.j-2]}-{B.row[B.j-1]}|={abs(B.row[B.j-2]-B.row[B.j-1])}`，`|{B.row[B.j-1]}-{B.row[B.j]}|={abs(B.row[B.j-1]-B.row[B.j])}`，"
            + ('有一个 > threshold → ==不合法==' if abs(B.row[B.j-2]-B.row[B.j-1]) > B.threshold or abs(B.row[B.j-1]-B.row[B.j]) > B.threshold else '都不超过 threshold')),
        'ok = False': '差值超过 `threshold`：这个子网格不是区域',
        14: lambda S, B, r: ('子网格不合法，换下一个' if not B.ok else '左右相邻都通过，接着检查上下相邻'),
        21: lambda S, B, r: ('子网格不合法，换下一个' if not B.ok else '上下相邻也都通过 → 这是一个合法区域'),
        'if abs(a[i - 2][y]': lambda S, B, r: (
            f"上下相邻（第 {B.y} 列）：`|{B.a[B.i-2][B.y]}-{B.a[B.i-1][B.y]}|={abs(B.a[B.i-2][B.y]-B.a[B.i-1][B.y])}`，`|{B.a[B.i-1][B.y]}-{B.a[B.i][B.y]}|={abs(B.a[B.i-1][B.y]-B.a[B.i][B.y])}`，"
            + ('有一个 > threshold → ==不合法==' if abs(B.a[B.i-2][B.y]-B.a[B.i-1][B.y]) > B.threshold or abs(B.a[B.i-1][B.y]-B.a[B.i][B.y]) > B.threshold else '都不超过 threshold')),
        'avg = sum': '合法区域！9 个数之和 `//` 9：`avg` = =={avg}==（先取整，再参与后面的平均）',
        'result[x][y] += avg': '`result[{x}][{y}]` 先累加 `avg`，不急着除：现在是 `{result[x][y]}`',
        'result[i][j] = a[i][j]': '`cnt = 0`：不属于任何区域，保持原值 `{a[i][j]}`',
        'result[i][j] //= c': '属于 `{c}` 个区域：`result[{i}][{j}] = 累加和 // {c}` = =={result[i][j]}==',
        'return result': '全部算完，返回 `result`',
    },
    cards=dict(
        one_liner='枚举 3×3 子网格，合法就把平均值累加进每个格子，最后除以次数',
        complexity='时间 `O(Amn)`（A = 9），空间 `O(mn)`',
        problem=['`image` 中 3×3 子网格里所有相邻像素差 ≤ `threshold` 才算区域',
                 '每个像素的结果 = 所属各区域（取整后）平均强度的平均值，向下取整',
                 '不属于任何区域则保持原值',
                 '示例：`[[5,6,7,10],[8,9,10,10],[11,12,13,10]]`，`threshold = 3` → 全是 `9`'],
        quote='由于需要计算平均值，我们先把 avg 加到 result[i][j] 中，同时用一个 cnt 矩阵统计 (i,j) 在多少个合法子网格内。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举每个 3×3 子网格的右下角，先查左右、再查上下相邻差',
              '合法时求 `avg = 9 个数之和 // 9`，累加到 9 个格子的 `result`，`cnt += 1`',
              '最后 `cnt == 0` 保持原值，否则 `result //= cnt`'],
        summary=['时间 `O(9mn)`，空间 `O(mn)`',
                 '易错：区域平均要先取整，再算多个区域的平均，不能直接除以 9 之外的数',
                 '易错：右下角下标从 `2` 开始，否则越界',
                 '思考题 w×h：用二维差分 / 前缀和 + 滑窗可做到 `O(mn)`'],
    ),
)

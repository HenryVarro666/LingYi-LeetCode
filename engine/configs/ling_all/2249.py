def _marks(S):
    if 'max_y' not in S:
        return None
    cs = S['circles']
    X, Y = S['max_x'], S['max_y']
    i, j = S.get('i'), S.get('j')
    g = [[0] * (Y + 1) for _ in range(X + 1)]
    if i is None:
        return g
    for a in range(X + 1):
        for b in range(Y + 1):
            if (a, b) < (i, j or 0) and any((x - a) ** 2 + (y - b) ** 2 <= r * r for x, y, r in cs):
                g[a][b] = 1
    return g


def _info(S):
    if 'max_y' not in S:
        return '先把圆按半径从大到小排序，再确定要扫描的范围'
    if 'x' in S and 'i' in S and S.get('_line') in (10, 11, 12):
        i, j, x, y, r = S['i'], S['j'], S['x'], S['y'], S['r']
        d = (x - i) ** 2 + (y - j) ** 2
        return f'点 `({i},{j})` 到圆心 `({x},{y})`：`d² = {d}`，`r² = {r * r}` → ' + ('==在圆内==' if d <= r * r else '不在这个圆内')
    return f"已确认的格点数 `ans` = =={S.get('ans', 0)}=="


CONFIG = dict(
    num=2249, title='统计圆内格点数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举格点 + 大圆优先',
    tags=[],
    code='''
class Solution:
    def countLatticePoints(self, circles: List[List[int]]) -> int:
        ans = 0
        circles.sort(key=lambda c: -c[2])  # 按半径从大到小排序，这样能更早遇到包含 (i,j) 的圆
        max_x = max(c[0] + c[2] for c in circles)
        max_y = max(c[1] + c[2] for c in circles)
        for i in range(max_x + 1):
            for j in range(max_y + 1):
                for x, y, r in circles:
                    if (x - i) * (x - i) + (y - j) * (y - j) <= r * r:
                        ans += 1
                        break
        return ans
''',
    call='Solution().countLatticePoints([[1, 1, 1], [2, 1, 1]])',
    expect=8,
    views=[
        dict(type='text', fn=_info, size=27),
        dict(type='grid', var=_marks, label='格点（行 = i，列 = j；绿 = 已算进答案；黄框 = 当前枚举的点）', cell=84, h=430,
             color=lambda S, i, j, v: 'green' if v == 1 else None, values=False,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
    ],
    watch=['i', 'j', 'x', 'y', 'r', ('ans', 'ans', 'green')],
    skip=['ans = 0', 'for i in range', 'for j in range', 'for x, y, r in circles'],
    max_steps=110,
    captions={
        'circles.sort': '按半径从大到小排序：大圆覆盖得多，更早碰到包含当前点的圆，能早点 `break`',
        'max_x =': '横坐标最多到 `max_x = {max_x}`，扫描范围从 0 到这里',
        'max_y =': '纵坐标最多到 `max_y = {max_y}`，在 `(0..{max_x}) × (0..{max_y})` 里逐点枚举',
        'if (x - i)': lambda S, B, r: (f'点 `({S.i},{S.j})` 到圆心 `({S.x},{S.y})` 距离平方 `{(S.x-S.i)**2+(S.y-S.j)**2}` '
                                       f'{"≤" if (S.x-S.i)**2+(S.y-S.j)**2 <= S.r*S.r else ">"} `r² = {S.r*S.r}` → '
                                       + ('==在圆内==' if (S.x-S.i)**2+(S.y-S.j)**2 <= S.r*S.r else '不在，换下一个圆')),
        'ans += 1': '这个点在某个圆内：`ans` → =={ans}==',
        'break': '只要被一个圆盖住就够了，==不再看其他圆，避免重复计数==',
        'return ans': '所有格点扫描完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='枚举每个格点，被任意一个圆盖住就计一次并跳出',
        complexity='时间 `O(U·V·n)`（`U, V` 为扫描范围，`n` 为圆数），空间 `O(1)`',
        problem=['`circles[i] = [x, y, r]` 是圆心和半径，圆周上的点也算圆内',
                 '求至少在一个圆内的整数格点个数',
                 '示例：`[[2,2,1]]` → `5`；本视频用 `[[1,1,1],[2,1,1]]` → `8`'],
        quote='先按半径从大到小排序，这样可以更早地遇到包含当前枚举的点的圆。',
        quote_src='—— 灵茶山艾府题解',
        idea=['坐标最大是 `x + r`，所以只需枚举 `0..max_x`、`0..max_y` 的点',
              '对每个点依次判断 `(x-i)² + (y-j)² ≤ r²`，全程整数运算',
              '命中就 `ans += 1` 并 `break`，一个点只数一次',
              '半径大的圆排在前面，更早命中，提早结束内层循环'],
        summary=['数据范围：坐标和半径 ≤ 100，最多 `200×200×200` 次判断',
                 '易错点：==命中后必须 `break`==，否则被多个圆覆盖的点会重复计数',
                 '易错点：圆周上的点也算，所以是 `<=`',
                 '用 `x*x` 比较，避免开方的浮点误差'],
    ),
)

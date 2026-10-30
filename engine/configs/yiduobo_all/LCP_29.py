def _spiral(n):
    g = [[0] * n for _ in range(n)]
    x = y = 0
    dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
    d = 0
    for k in range(1, n * n + 1):
        g[x][y] = k
        nx, ny = x + dx[d], y + dy[d]
        if not (0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0):
            d = (d + 1) % 4
            nx, ny = x + dx[d], y + dy[d]
        x, y = nx, ny
    return g


N = 6
SP = _spiral(N)


def _color(S, i, j, v):
    if i == S['xPos'] and j == S['yPos']:
        return 'pink'
    if 'level' in S and min(i, j, N - 1 - i, N - 1 - j) < S['level']:
        return 'blue'
    if 'level' in S and min(i, j, N - 1 - i, N - 1 - j) == S['level']:
        return 'yellow'
    return None


def _edge(S, B, ret):
    n, L, x, y = S.num, S.level, S.xPos, S.yPos
    if x == L:
        return f'`xPos = {x} = level` → 在第 {L} 层的==上边=='
    if y == n - 1 - L:
        return f'`xPos ≠ level`，`yPos = {y} = n-1-level` → 在==右边=='
    if x == n - 1 - L:
        return f'`xPos = {x} = n-1-level` → 在==下边=='
    return '都不是 → 在==左边=='


CONFIG = dict(
    num='LCP 29', title='乐团站位', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按层求螺旋位置',
    tags=[],
    code='''
class Solution(object):
    def orchestraLayout(self, num, xPos, yPos):

        level = min(xPos, num - 1 - xPos, yPos, num - 1 - yPos)
        tot = 4 * (num - level) * level % 9
        
        if xPos == level:
            tot += yPos - level + 1
        elif yPos == num - 1 - level:
            tot += (num - level * 2 - 1) + xPos - level + 1
        elif xPos == num - 1 - level:
            tot += 2 * (num - level * 2 - 1) + num - 1 - level - yPos + 1
        else:
            tot += 3 * (num - level * 2 - 1) + num - 1 - level - xPos + 1
        return (tot - 1) % 9 + 1
''',
    call='Solution().orchestraLayout(6, 3, 4)',
    expect=8,
    views=[
        dict(type='grid', var=lambda S: SP, h=470, cell=70, label='螺旋矩阵（格内是第几个被访问；粉 = 目标，蓝 = 已走完的外层，黄 = 当前层）',
             color=_color),
        dict(type='text', size=30, fn=lambda S: (
            f"前面 `{S['level']}` 层共 `4×{S['level']}×({S['num']}−{S['level']})` = =={4 * S['level'] * (S['num'] - S['level'])}== 格"
            if 'level' in S else '')),
    ],
    watch=[('num', 'num', 'blue'), ('xPos', 'xPos', 'pink'), ('yPos', 'yPos', 'cyan'), ('level', 'level', 'yellow'), ('tot', 'tot', 'green')],
    captions={
        'level = min': '到四条边的距离取最小，得层数：`min({xPos}, {num-1-xPos}, {yPos}, {num-1-yPos})` = =={level}==，前面有 `{level}` 层整圈',
        'tot = 4 *': '前 `level` 层总格数 `4·level·(n−level)` = {4*level*(num-level)}，只关心模 9：`tot` = =={tot}==',
        'if xPos == level': lambda S, B, r: f'`xPos = {S.xPos}`，`level = {S.level}` → 不相等，不在上边' if S.xPos != S.level else '`xPos == level` → 在==上边==',
        'elif yPos == num - 1 - level': lambda S, B, r: f'`yPos = {S.yPos}`，`n-1-level = {S.num - 1 - S.level}` → 相等，在==右边==',
        'elif xPos == num - 1 - level': _edge,
        'tot += yPos - level + 1': '上边的第 `yPos − level + 1` 个：`tot` = {tot}',
        'tot += (num - level * 2 - 1) + xPos': '上边走了 `n−2·level−1` 格，再加右边第 `xPos − level + 1` 个：`tot` = =={tot}==',
        'tot += 2 *': '上、右两边各 `n−2·level−1` 格，再加下边第 `n−1−level−yPos+1` 个：`tot` = {tot}',
        'tot += 3 *': '三条边各 `n−2·level−1` 格，再加左边的第几个：`tot` = {tot}',
        'return': '`({B.tot} − 1) % 9 + 1` = ==`{ret}`==：先减 1 再加 1，让 9 的倍数得 9 而不是 0',
    },
    cards=dict(
        one_liner='一层一层剥螺旋，算出是第几个，再对 9 取模',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`num × num` 的方阵，从左上角顺时针螺旋写入 1、2、3……，每个数只保留 ==对 9 取模后的 1~9==',
                 '给出位置 `(xPos, yPos)`，返回该位置的数字',
                 '本视频：`num=6, (3,4)` → `8`（是第 26 个）'],
        quote='level = min(xPos, yPos, n - 1 - xPos, n - 1 - yPos)……第0层的路径长度为4 * (n - 1)，第1层的路径长度为4 * (n - 3)，依次类推。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模很大，不能模拟；改成「外层一圈一圈剥开」',
              '第 `k` 层一圈 `4·(n−2k−1)` 格，前 `level` 层合计 `4·level·(n−level)`',
              '再看目标在这层的上/右/下/左哪条边，加上边内序号，得到总序号'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '先判断上边 `xPos == level`，顺序决定了四个角落归哪条边',
                 '答案 9 的倍数时是 9：用 `(tot - 1) % 9 + 1`',
                 '`tot` 先对 9 取模，防止乘积过大（Python 本身不溢出）',
                 '代码已是 Python 3 可运行，未做修改'],
    ),
)

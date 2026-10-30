N0, A0, B0 = 9, 3, 5


def _players(cv, x0, x1, y, n, a, b, T, r=21, arcs=False):
    gap = min(2 * r + 12, (x1 - x0) / max(n, 1))
    sx = x0 + ((x1 - x0) - gap * n) / 2 + gap / 2
    pos = lambda i: sx + (i - 1) * gap
    if arcs:
        for i in range(1, n // 2 + 1):
            j = n + 1 - i
            hot = i in (a, b) or j in (a, b)
            col = T['yellow'] if hot else T['border']
            cv.arc_arrow((pos(i), y - r - 4), (pos(j), y - r - 4), min(60, 8 + 8 * (j - i)), col, width=3 if hot else 2, head=1)
    for i in range(1, n + 1):
        if i == a:
            fill, tc = T['blue'], T['bg']
        elif i == b:
            fill, tc = T['pink'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((pos(i) - r, y - r, pos(i) + r, y + r), fill=fill, outline=T['border'], width=1, r=r)
        cv.text((pos(i), y), i, 22, tc, anchor='mm', bold=True)
        if i in (a, b):
            cv.text((pos(i), y + r + 6), 'L' if i == a else 'R', 22, fill, anchor='mt', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'第 1 回合：{N0} 人，两位最强者在第 {A0}、{B0} 位（L、R）', 24, T['muted'], bold=True)
    _players(cv, x0 + 20, x1 - 20, y0 + 90, N0, A0, B0, T, arcs=True)
    n, l, r = S.get('n'), S.get('left'), S.get('right')
    if isinstance(n, int) and isinstance(l, int) and isinstance(r, int) and 1 <= l <= n and 1 <= r <= n and 'f' in S:
        cv.text((x0 + 18, y0 + 150), f'当前 dfs：还剩 {n} 人，最强者在第 {l}、{r} 位（黄线 = 他们的对手）', 24, T['muted'], bold=True)
        _players(cv, x0 + 20, x1 - 20, y0 + 235, n, l, r, T, arcs=True)
        nn = (n + 1) // 2
        inn = S.get('_inner') or S
        nl, nr = inn.get('next_left'), inn.get('next_right')
        if isinstance(nl, int) and isinstance(nr, int) and 1 <= nl < nr <= nn:
            cv.text((x0 + 18, y0 + 295), f'下一轮：{nn} 人，他们去到第 {nl}、{nr} 位', 24, T['muted'], bold=True)
            _players(cv, x0 + 20, x1 - 20, y0 + 365, nn, nl, nr, T, arcs=True)


def _fg(S):
    try:
        n, l, r = S['n'], S['left'], S['right']
        fv, gv = S['f'][n][l][r], S['g'][n][l][r]
        if fv is None:
            return f'`f[{n}][{l}][{r}]` 还没算出'
        return f'`f[{n}][{l}][{r}]` = =={fv}==（最早），`g[{n}][{l}][{r}]` = =={gv}==（最晚）'
    except Exception:
        return ''


CONFIG = dict(
    num=1900, title='最佳运动员的比拼回合', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='对称性 + 记忆化搜索（f 最早 / g 最晚）',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 2455'],
    code='''
class Solution(object):
    def earliestAndLatest(self, n, firstPlayer, secondPlayer):
        f = [[[None] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]
        g = [[[None] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]
        self.dfs(n, firstPlayer, secondPlayer, f, g)
        return [f[n][firstPlayer][secondPlayer], g[n][firstPlayer][secondPlayer]]
    
    def dfs(self, n, left, right, f, g):
        if f[n][left][right] is not None:
            return
        if f[n][n - right + 1][n - left + 1] is not None:
            return
        if left + right == n + 1:
            f[n][left][right] = g[n][left][right] = 1
            f[n][right][left] = g[n][right][left] = 1
            return
        next_n = (n + 1) // 2
        if left > n // 2:
            left, right = n - right + 1, n - left + 1
        if right <= next_n:
            for i in range(left):
                for j in range(right - left):
                    next_left = i + 1
                    next_right = i + j + 2
                    self.dfs(next_n, next_left, next_right, f, g)
                    if f[n][left][right] is None or f[n][left][right] > f[next_n][next_left][next_right] + 1:
                        f[n][left][right] = f[next_n][next_left][next_right] + 1
                    if g[n][left][right] is None or g[n][left][right] < g[next_n][next_left][next_right] + 1:
                        g[n][left][right] = g[next_n][next_left][next_right] + 1
        
        else:
            if left + right > n + 1:
                left, right = n - right + 1, n - left + 1
            
            mirror_right = n - right + 1
            mid_rest = (n - mirror_right * 2 + 1) // 2
            for i in range(left):
                for j in range(mirror_right - left):
                    next_left = i + 1
                    next_right = i + j + 1 + mid_rest + 1
                    self.dfs(next_n, next_left, next_right, f, g)
                    if f[n][left][right] is None or f[n][left][right] > f[next_n][next_left][next_right] + 1:
                        f[n][left][right] = f[next_n][next_left][next_right] + 1
                    if g[n][left][right] is None or g[n][left][right] < g[next_n][next_left][next_right] + 1:
                        g[n][left][right] = g[next_n][next_left][next_right] + 1
        
        f[n][n - right + 1][n - left + 1] = f[n][left][right]
        g[n][n - right + 1][n - left + 1] = g[n][left][right]
''',
    call='Solution().earliestAndLatest(9, 3, 5)',
    expect=[2, 4],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_fg, h=50),
        dict(type='calls', h=130, hide=('f', 'g')),
    ],
    watch=['n', 'left', 'right', 'next_left', 'next_right'],
    captions={
        3: '`f[n][l][r]`：还剩 n 人、两位最强者在第 l、r 位时，==最早==相遇回合；`None` = 还没算',
        4: '`g[n][l][r]`：同样位置下，==最晚==相遇回合',
        9: lambda S, B, r: ('`f[{0}][{1}][{2}]` 已经算过 → 直接返回'.format(S.n, S.left, S.right) if S.f[S.n][S.left][S.right] is not None else '这个状态还没算过 → 往下算'),
        10: '已算过，不再展开（记忆化）',
        11: lambda S, B, r: ('它的镜像状态 `f[n][n−right+1][n−left+1]` 已算过 → 同样直接用' if S.f[S.n][S.n - S.right + 1][S.n - S.left + 1] is not None else '镜像状态也没算过 → 继续'),
        12: '镜像状态已算过，返回',
        13: lambda S, B, r: (f'`left + right = {S.left + S.right}` = `n + 1`：两人互为对手，==这一轮就相遇==' if S.left + S.right == S.n + 1 else f'`left + right = {S.left + S.right} ≠ {S.n + 1}`：这轮碰不上，要枚举谁晋级'),
        14: '相遇：`f = g = 1`',
        15: '左右互换的状态结果相同，也写上 1',
        16: '返回（结果已写进 f、g）',
        17: '下一轮人数 `next_n = ceil(n/2) = {next_n}`',
        18: lambda S, B, r: (f'`left = {S.left}` > `n//2 = {S.n // 2}`：在中点右侧 → 整体镜像成 `({S.n - S.right + 1}, {S.n - S.left + 1})`，让 left 在左半' if S.left > S.n // 2 else f'`left = {S.left}` ≤ `n//2 = {S.n // 2}`：已在左半，不用镜像'),
        19: '镜像后：`left = {left}`，`right = {right}`',
        20: lambda S, B, r: (f'`right = {S.right}` ≤ `next_n = {S.next_n}`：right 也在中点左侧（或正好中点）→ ==情形 3-1/3-2==' if S.right <= S.next_n else f'`right = {S.right}` > `next_n`：right 在中点右侧 → ==情形 3-3==，要看它的对手'),
        21: '枚举 left 左边晋级 `i` 人',
        22: '枚举 left、right 之间晋级 `j` 人',
        25: '下一轮：left 在第 `{next_left}` 位，right 在第 `{next_right}` 位（左边 `{i}` 人、中间 `{j}` 人晋级）→ 递归',
        27: '最早取更小：`f[{n}][{left}][{right}]` = f[下一轮] + 1 = =={f[n][left][right]}==',
        29: '最晚取更大：`g[{n}][{left}][{right}]` = g[下一轮] + 1 = =={g[n][left][right]}==',
        32: lambda S, B, r: ('`left + right > n + 1`：right 的对手跑到 left 左边了 → 再镜像一次' if S.left + S.right > S.n + 1 else '`left + right ≤ n + 1`：right 的对手在 left 右边，不用再镜像'),
        35: '`right` 的对手是第 `mirror_right = {mirror_right}` 位，它一定会被 right 淘汰',
        36: '`mirror_right` 到 `right` 之间 `{n - mirror_right * 2}` 人，无论如何淘汰一半，晋级 `mid_rest = {mid_rest}` 人',
        41: '下一轮：left 在第 `{next_left}` 位，right 在第 `{next_right}` 位（含 `{mid_rest}` 个中间晋级者）→ 递归',
        43: '最早取更小：`f[{n}][{left}][{right}]` = =={f[n][left][right]}==',
        45: '最晚取更大：`g[{n}][{left}][{right}]` = =={g[n][left][right]}==',
        47: '把结果也写到镜像状态 `({n - right + 1}, {n - left + 1})`，以后直接复用',
        48: '`g` 同理',
        6: '答案：`f` 是最早，`g` 是最晚 → =={ret}==',
    },
    skip=[21, 22, 23, 24, 26, 28, 37, 38, 39, 40, 42, 44],
    max_steps=60,
    cards=dict(
        one_liner='两位最强者互相等价、左右镜像等价：用 f 记最早、g 记最晚',
        complexity='时间 `O(n^4)`，空间 `O(n^3)`',
        problem=['`n` 人排成一排，每回合第 `i` 个对倒数第 `i` 个，奇数人时中间轮空',
                 '两位最强者在其他人面前必胜，其余人胜负可任意裁定，求他们相遇的最早与最晚回合',
                 '示例：`n=9`，位置 `3` 和 `5` → `[2, 4]`'],
        quote='f[n][left][right]表示现在还有n个运动员，其中最强的两个运动员分别在从左往右数的第left和right的位置上时，二人遭遇需要的最少轮次，g表示同样位置状况下二人遭遇需要的最多轮次。',
        quote_src='—— yiduobo 题解',
        idea=['`left + right = n + 1`：两人互为对手，这一轮就遇上，`f = g = 1`',
              '否则枚举 left 左侧、两人之间各有几人晋级，得到下一轮的 `next_left`、`next_right`',
              '利用对称性：`f[n][l][r] = f[n][n−r+1][n−l+1]`，只算一半'],
        summary=['时间 `O(n^4)`，空间 `O(n^3)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（共 3 处）',
                 '易错：`right` 在中点右侧时，它的对手 `mirror_right` 在 `left` 的左还是右，要先镜像调整',
                 '同类：灵神另有 `O(1)` 的分类讨论解法'],
    ),
)

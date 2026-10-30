NAMES = ['A', 'B', 'C', 'D']
TARGET = ['A', 'C', 'D']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'dis' not in S:
        return
    W = (x1 - x0 - 30) / 3
    cell = min(58, (W - 56) / 4)
    L = len(TARGET)
    i, j, nb = S.get('i'), S.get('j'), S.get('neibor')
    i_in = i is not None and 'f' in S and S.get('_line') is not None and S['_line'] >= 21
    specs = [('dis[i][j]', 'dis', '名字相同 0 / 不同 1'), ('f[i][j]', 'f', '最小编辑距离（∞ = 未算）'), ('prev[i][j]', 'prev', '上一步的城市')]
    for k, (title, var, sub) in enumerate(specs):
        gx = x0 + 15 + k * W + 44
        gy = y0 + 104
        cv.text((x0 + 15 + k * W + 6, y0 + 4), title, 26, T['text'], bold=True, mono=True)
        cv.text((x0 + 15 + k * W + 6, y0 + 38), sub, 19, T['muted'])
        data = S[var]
        for c in range(4):
            cv.text((gx + c * cell + cell / 2, gy - 6), NAMES[c], 20, T['muted'], anchor='mb', mono=True)
        for r in range(L):
            cv.text((gx - 8, gy + r * cell + cell / 2), TARGET[r], 20, T['muted'], anchor='rm', mono=True)
            for c in range(4):
                v = data[r][c] if r < len(data) else None
                fill = T['panel2']
                tc = T['text']
                if var == 'dis' and v == 0:
                    fill, tc = T['green'], T['bg']
                if var == 'f' and v is not None and v < 1000:
                    fill, tc = T['green'], T['bg']
                if var == 'prev' and v is not None:
                    fill, tc = T['purple'], T['bg']
                hot = (var != 'dis' and i is not None and (r, c) == (i, j) and 'neibor' in S and S.get('_line', 0) >= 21 and S.get('_line', 0) <= 29)
                if var == 'f' and nb is not None and i is not None and i > 0 and (r, c) == (i - 1, nb) and 21 <= S.get('_line', 0) <= 29:
                    fill, tc = T['pink'], T['bg']
                if var == 'dis' and v is not None and i is not None and (r, c) == (i, j) and 21 <= S.get('_line', 0) <= 29:
                    fill, tc = T['yellow'], T['bg']
                changed = var in ('f', 'prev') and B.get(var) is not None and r < len(B[var]) and B[var][r][c] != v
                X, Y = gx + c * cell, gy + r * cell
                cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6,
                        outline=T['yellow'] if (hot or changed) else T['border'], width=4 if (hot or changed) else 1)
                s_ = '·' if v is None else ('∞' if v >= 1000 else str(v))
                cv.text((X + cell / 2, Y + cell / 2), s_, 26, tc, anchor='mm', bold=True)


def _txt(S):
    if 'f' not in S or 'i' not in S or 'j' not in S:
        return '图：0-1，1-2，1-3；城市名 A B C D；目标路径 A → C → D'
    i, j = S['i'], S['j']
    if 'neibor' in S and i > 0:
        nb = S['neibor']
        return f"第 {i} 步走到 {j} 号城市，上一步在 {nb} 号：`f[{i-1}][{nb}] + dis[{i}][{j}]` = {S['f'][i-1][nb]} + {S['dis'][i][j]}"
    return f"第 {i} 步走到 {j} 号城市（{NAMES[j]}），目标是 {TARGET[i]}"


def _disc(S, i, j, v):
    if 'f' not in S:
        return 'green' if v == 0 else None
    return None


def _cap_cmp(S, B, ret):
    i, j, nb = S.i, S.j, S.neibor
    new = B.f[i - 1][nb] + S.dis[i][j]
    cur = B.f[i][j]
    if new < cur:
        return (f'走到城市 {j}，上一步在邻居 {nb}：`f[{i-1}][{nb}] + dis[{i}][{j}] = {B.f[i-1][nb]} + {S.dis[i][j]} = {new}` '
                f'< 当前 `f[{i}][{j}] = {cur}` → ==更新==，并记下上一步来自 {nb}')
    return f'走到城市 {j}，上一步在邻居 {nb}：`{B.f[i-1][nb]} + {S.dis[i][j]} = {new}` 不小于当前 `f[{i}][{j}] = {cur}` → 不更新'


CONFIG = dict(
    num=1548, title='图中最相似的路径', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='图上 DP · 记录前驱还原路径',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def mostSimilar(self, n, roads, names, targetPath):
        
        dis = []
        for target in targetPath:
            dis.append([])
            for name in names:
                if target == name:
                    dis[-1].append(0)
                else:
                    dis[-1].append(1)
        
        g = [[] for _ in range(n)]
        for x, y in roads:
            g[x].append(y)
            g[y].append(x)
        
        f = [[1000] * n for _ in range(len(targetPath))]
        prev = [[None] * n for _ in range(len(targetPath))]
        for i in range(len(targetPath)):
            if i == 0:
                for j in range(n):
                    f[i][j] = min(f[i][j], dis[i][j])
            else:
                for j in range(n):
                    for neibor in g[j]:
                        if f[i - 1][neibor] + dis[i][j] < f[i][j]:
                            f[i][j] = f[i - 1][neibor] + dis[i][j]
                            prev[i][j] = neibor
        
        mi = 1000
        p = None
        for j in range(n):
            if f[-1][j] < mi:
                mi = f[-1][j]
                p = j

        res = []
        for i in range(len(targetPath) - 1, 0, -1):
            res.append(p)
            p = prev[i][p]
        
        res.append(p)
        res.reverse()

        return res
''',
    call="Solution().mostSimilar(4, [[0,1],[1,2],[1,3]], ['A','B','C','D'], ['A','C','D'])",
    expect=[0, 1, 3],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='custom', draw=_draw, h=300),
    ],
    watch=['i', 'j', 'neibor', ('mi', 'mi', 'green'), 'p', 'res'],
    skip=['dis.append([])', 'for name in names', 'if target == name', 'dis[-1].append', 'g[x].append(y)', 'g[y].append(x)', 'for x, y in roads', 'f[i][j] = f[i - 1][neibor]', 'for j in range(n)', 'for neibor in g[j]', 'dis = []', 'p = None', 'res = []', 'mi = f[-1][j]'],
    max_steps=90,
    captions={
        'for target in targetPath': lambda S, B, r: (f'`dis`：目标城市 `{S.target}` 和每个城市名比一比，相同记 `0`，不同记 `1`——按==城市名==比，不是按字符'
                                                 if len(B.dis) < len(S.targetPath) else '`dis` 填完：每一行是一个目标城市，绿格 = 名字相同'),
        'f = [[1000]': '`f` 全部先填 `1000`（相当于无穷大），行数 = 目标路径长度',
        'prev = [[None]': '`prev` 记录路径：第 i 步到城市 j，上一步该从哪来',
        'if i == 0': lambda S, B, r: f'第 `{S.i}` 步' + ('：还没走边，起点可以是任意城市' if S.i == 0 else '：要从相邻城市转移过来'),
        'f[i][j] = min(f[i][j], dis[i][j])': '起点任选：`f[0][{j}] = dis[0][{j}] = {f[0][j]}`',
        'if f[i - 1][neibor] + dis[i][j] < f[i][j]': _cap_cmp,
        'f[i][j] = f[i - 1][neibor]': '`f[{i}][{j}] = {f[i][j]}`',
        'prev[i][j] = neibor': '`f[{i}][{j}]` 更新为 {f[i][j]}；`prev[{i}][{j}] = {neibor}`：以后倒推路径要回到城市 {neibor}',
        'for i in range(len(targetPath) - 1': lambda S, B, r: ('从最后一步往回：沿 `prev` 倒推路径，`res` 倒着收集' if not S.res else
                                                                       (f'继续倒推：现在是第 `{S.i}` 步' if len(S.res) < len(S.targetPath) - 1 else '倒推到第 1 步为止（第 0 步没有 `prev`），最后单独放入起点')),
        'mi = 1000': '在最后一行里找最小值，先设 `mi = 1000`',
        'if f[-1][j] < mi': lambda S, B, r: (f'`f[-1][{S.j}] = {S.f[-1][S.j]}` < `mi = {B.mi}` → ==更新最优终点==' if S.f[-1][S.j] < B.mi
                                              else f'`f[-1][{S.j}] = {S.f[-1][S.j]}` 不比 `mi = {B.mi}` 小 → 跳过'),
        'p = j': '新的最优终点：城市 `p = {p}`，`mi = {mi}`',
        'res.append(p)': '从终点往回走：把城市 `{p}` 放进 `res`',
        'p = prev[i][p]': '沿着 `prev` 跳到上一步的城市 `p = {p}`',
        'res.reverse()': '倒着收集的，翻转后得到从起点到终点的路径 `{res}`',
        'return res': '路径 `{res}`：编辑距离 {mi}',
    },
    cards=dict(
        one_liner='f[i][j]：走了 i 步、停在城市 j 的最小编辑距离',
        complexity='时间 `O(L·m)`（L = 路径长，m = 边数），空间 `O(L·n)`',
        problem=['给一张无向图和城市名，再给一条目标名字路径 `targetPath`',
                 '求一条同样长度、相邻城市有路的真实路径，使和目标==逐位名字不同的个数最少==',
                 '返回这条路径的城市编号；本视频：4 个城市、路径 `A→C→D`，答案 `[0,1,3]`'],
        quote='题目中对编辑距离的定义是==城市名粒度而不是字符粒度==的，在计算的时候不要弄混了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `dis[i][j]` 记下「第 i 步站在城市 j 要不要额外 +1」，省去反复比字符串',
              '`f[i][j] = min(f[i-1][邻居] + dis[i][j])`，哪个邻居最优就写进 `prev`',
              '最后一行取最小的终点，再沿 `prev` 倒推出完整路径'],
        summary=['时间 `O(L·m)`，空间 `O(L·n)`；数据规模小，`O(n^3)` 也行',
                 '`f` 初值 `1000` 当无穷大；`prev` 第 0 行用不到，所以倒推只走到 `i > 0`',
                 '易错：编辑距离按==城市名==算；倒推出来的路径要 `reverse`',
                 '原文已是 Python 3 可运行的写法，代码未做改动'],
    ),
)

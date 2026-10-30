_DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))
_NAME = ['向右 →', '向下 ↓', '向左 ←', '向上 ↑']


def _visited(S, i, j, v):
    return 'green' if v in S.get('ans', []) else None


def _info(S):
    if 'di' not in S:
        return '每一轮：朝当前方向==恰好走 `n` 步==，然后右转，`m, n = n, m - 1`'
    return f'方向 `di = {S["di"]}`：=={_NAME[S["di"]]}==　　这一轮步数 `n = {S["n"]}`　　剩余部分转过来看 `{S["m"]} × {S["n"]}`'



def _draw_list(name, cell_max=74):
    """数组视图的替代：引擎的 array 视图在空列表时会越界，这里自己画（空列表显示“空”）"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), name, 24, T['muted'], bold=True)
        vals = S.get(name)
        if vals is None:
            cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
            return
        if not vals:
            cv.text((x0 + 18, y0 + 44), '[ ]  空', 24, T['dim'], mono=True)
            return
        bvals = B.get(name) or []
        width = x1 - x0 - 40
        cell = min(cell_max, width / len(vals))
        ch = min(cell * 0.92, 68)
        top = y0 + 40
        for i, v in enumerate(vals):
            X = x0 + 20 + i * cell
            new = i >= len(bvals) or bvals[i] != v
            cv.rect((X + 3, top, X + cell - 3, top + ch), fill=T['panel2'], r=8,
                    outline=T['yellow'] if new else T['border'], width=3 if new else 1)
            cv.text((X + cell / 2, top + ch / 2), v, int(min(32, cell * 0.42)), T['text'], anchor='mm', bold=True)
            cv.text((X + cell / 2, top + ch + 6), i, 18, T['dim'], anchor='mt', mono=True)
    return draw

CONFIG = dict(
    num=54, title='螺旋矩阵', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='模拟 · 不标记（每轮精确走 n 步）',
    code='''
DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)  # 右下左上

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        size = m * n
        ans = []
        i, j, di = 0, -1, 0  # 从 (0, -1) 开始
        while len(ans) < size:
            dx, dy = DIRS[di]
            for _ in range(n):  # 走 n 步（注意 n 会减少）
                i += dx
                j += dy  # 先走一步
                ans.append(matrix[i][j])  # 再加入答案
            di = (di + 1) % 4  # 右转 90°
            m, n = n, m - 1  # 减少后面的循环次数（步数）
        return ans
''',
    call='Solution().spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])',
    expect=[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
    views=[
        dict(type='text', h=56, size=27, fn=_info),
        dict(type='grid', var='matrix', cell=110, h=420, color=_visited,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
        dict(type='custom', h=140, draw=_draw_list('ans')),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'di', ('m', 'm', 'cyan'), ('n', 'n', 'cyan'), ('size', 'size')],
    skip=['i += dx', 'j += dy', 'for _ in range(n)'],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'ans = []': '`ans` 按螺旋顺序收集答案',
        'size = m * n': '一共要收集 `size = {size}` 个数（`m`、`n` 后面会变，先存下来）',
        'i, j, di = 0, -1, 0': '从 `(0, -1)` 出发：==矩阵左边外面一格==。“先走一步再记录”，第一步正好落在 `(0, 0)`',
        'while len(ans) < size': lambda S, B, ret: (f'已收集 `{len(S["ans"])}/{S["size"]}` 个 → 继续' if len(S['ans']) < S['size']
                                                    else f'收集满 `{S["size"]}` 个，结束'),
        'dx, dy = DIRS[di]': lambda S, B, ret: f'方向 `DIRS[{S["di"]}] = ({S["dx"]}, {S["dy"]})`，=={_NAME[S["di"]]}==，这一轮==恰好走 n 步==（`n = {S["n"]}`），不用判断出界',
        'ans.append': '先走一步到 `({i}, {j})`，再把 `matrix[{i}][{j}] = {matrix[i][j]}` 加入答案',
        'di = (di + 1) % 4': lambda S, B, ret: f'右转 90°：`di = ({B["di"]} + 1) % 4 = {S["di"]}`，接下来{_NAME[S["di"]]}',
        'm, n = n, m - 1': lambda S, B, ret: (f'`m, n = n, m - 1 = {S["m"]}, {S["n"]}`：==撕掉刚走完的一排，剩下的部分转 90°==，看成 {S["m"]} 行 {S["n"]} 列，下一轮走 {S["n"]} 步'
                                              if S['n'] else f'`m, n = {S["m"]}, {S["n"]}`：已经没有剩下的格子了'),
        'return ans': '返回 `ans`',
    },
    max_steps=70,
    cards=dict(
        one_liner='每走完一排就把它“撕掉”，剩下的矩阵转 90° 再走一遍',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计）',
        problem=['给你 `m` 行 `n` 列的矩阵，按==顺时针螺旋顺序==返回所有元素',
                 '示例：`[[1,2,3,4],[5,6,7,8],[9,10,11,12]]`',
                 '→ `[1,2,3,4,8,12,11,10,9,5,6,7]`'],
        before=[dict(heading='步数的规律', lines=[
            '示例的 12 个数分成 5 组：`1→2→3→4`、`8→12`、`11→10→9`、`5`、`6→7`',
            '横着走的组：长度 `4, 3, 2`，从 `n` 开始递减',
            '竖着走的组：长度 `2, 1`，从 `m-1` 开始递减',
            '步数有规律 → ==精确控制每个方向走几步==，无需判断出界或重复访问']),
        ],
        quote='把 m,n 分别更新为 n,m−1，这样下一轮循环又可以走 n 步。相当于撕掉矩阵的第一行，把矩阵旋转 90° 后，对这个 n 行 m−1 列的新矩阵继续做同样的操作。',
        quote_src='—— 灵茶山艾府题解（方法二：不标记）',
        idea=['从 `(0, -1)` 出发，“先走一步，再加入答案”',
              '每轮朝当前方向走 `n` 步，然后右转：`di = (di + 1) % 4`',
              '每 4 轮剥掉最外一圈（像剥洋葱），行列各少 2，所以规律一直成立'],
        summary=['时间 `O(mn)`，空间 `O(1)`，==不修改原矩阵==',
                 '`size` 要提前算好：`m`、`n` 在循环里会变',
                 '易错：起点是 `(0, -1)` 而不是 `(0, 0)`，因为是“先走再记录”',
                 '方法一：走过的格子标成 `None`，出界或撞到 `None` 就右转，也是 `O(mn)`'],
    ),
)

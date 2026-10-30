_DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))
_NAME = ['向右 →', '向下 ↓', '向左 ←', '向上 ↑']


def _color(S, i, j, v):
    if not v:
        return None
    if v == S.get('val'):
        return 'yellow'
    return 'green'


def _info(S):
    if 'di' not in S:
        return '从 `(0, 0)` 出发，按==右下左上==的顺序走，撞墙或撞到已填的格子就右转'
    return f'当前方向 `di = {S["di"]}`：=={_NAME[S["di"]]}==　　`DIRS[{S["di"]}] = {_DIRS[S["di"]]}`'


def _next(S):
    x, y = S.get('x'), S.get('y')
    if x is None:
        return None
    return x, y


def _cap_if(S, B, ret):
    x, y, n, ans = S.x, S.y, S.n, S.ans
    if x < 0 or x >= n or y < 0 or y >= n:
        return f'下一步 `({x}, {y})` ==出界== → 必须右转（`or` 短路，不会访问越界的 `ans[x][y]`）'
    if ans[x][y]:
        return f'下一步 `({x}, {y})` 已经填了 `{ans[x][y]}` → ==撞到填过的格子==，右转'
    return f'下一步 `({x}, {y})` 在界内且还是 0 → 不用转，继续{_NAME[S.di]}'


CONFIG = dict(
    num=59, title='螺旋矩阵 II', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='模拟 · 方向数组 + 撞墙右转',
    tags=['字节30天', '热题173'],
    code='''
DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)  # 右下左上

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        ans = [[0] * n for _ in range(n)]
        i = j = di = 0
        for val in range(1, n * n + 1):  # 要填入的数
            ans[i][j] = val
            x, y = i + DIRS[di][0], j + DIRS[di][1]  # 下一步的位置
            # 如果 (x, y) 出界或者已经填入数字
            if x < 0 or x >= n or y < 0 or y >= n or ans[x][y]:
                di = (di + 1) % 4  # 右转 90°
            i += DIRS[di][0]
            j += DIRS[di][1]  # 走一步
        return ans
''',
    call='Solution().generateMatrix(3)',
    expect=[[1, 2, 3], [8, 9, 4], [7, 6, 5]],
    skip=['i += DIRS'],
    views=[
        dict(type='text', h=60, size=27, fn=_info),
        dict(type='grid', var='ans', cell=150, h=540, color=_color,
             label='ans（绿 = 已填，黄 = 刚填；蓝框 = 当前 (i,j)，粉框 = 试探的下一步 (x,y)）',
             cursors=[('i', 'j', 'blue'), ('x', 'y', 'pink')]),
    ],
    watch=[('val', 'val', 'green'), ('i', 'i', 'blue'), ('j', 'j', 'blue'), ('di', 'di', 'cyan'),
           ('x', 'x', 'pink'), ('y', 'y', 'pink')],
    captions={
        'ans = [[0]': '`{n} × {n}` 的矩阵，==先全填 0==：0 表示“还没填”，后面靠它判断撞没撞到',
        'i = j = di = 0': '从左上角 `(0, 0)` 出发，`di = 0` 表示一开始==向右==',
        'for val in range': lambda S, B, ret: (f'要填入的数 `val = {S.val}`' if S.get('val') != B.get('val')
                                               else f'`1` 到 `{S.n * S.n}` 都填完了'),
        'ans[i][j] = val': '把 `{val}` 填进当前位置 `({i}, {j})`',
        'x, y = i + DIRS': lambda S, B, ret: f'先==试探==下一步：`({S.i}, {S.j}) + DIRS[{S.di}]` = `({S.x}, {S.y})`',
        'if x < 0': _cap_if,
        'di = (di + 1) % 4': lambda S, B, ret: (f'右转 90°：`di = ({B.di} + 1) % 4 = {S.di}`，改为=={_NAME[S.di]}=='
                                                + ('（`% 4` 让 3 之后回到 0）' if B.di == 3 else '')),
        'j += DIRS[di][1]': lambda S, B, ret: (f'沿{_NAME[S.di]}走一步，来到 `({S.i}, {S.j})`' if S.val < S.n * S.n
                                               else f'沿{_NAME[S.di]}走一步（`{S.val}` 已是最后一个数，这一步无关紧要）'),
        'return ans': '`n²` 个数全部填完，返回 `ans`',
    },
    max_steps=60,
    cards=dict(
        one_liner='按右下左上走，出界或撞到已填的格子就右转',
        complexity='时间 `O(n²)`，空间 `O(1)`（返回值不计）',
        problem=['给你正整数 `n`，生成 `n × n` 的矩阵',
                 '按==顺时针螺旋==顺序依次填入 `1` 到 `n²`',
                 '示例：`n = 3` → `[[1,2,3],[8,9,4],[7,6,5]]`'],
        quote='向右转 90°，相当于把 di 增加 1，但在 di=3 时要回到 di=0。两种情况合二为一，把 di 更新为 (di+1) mod 4。',
        quote_src='—— 灵茶山艾府题解「实现细节」',
        idea=['方向数组 `DIRS = 右, 下, 左, 上`：移动就是 `i += DIRS[di][0]`，`j += DIRS[di][1]`',
              '每填一个数，先==试探==下一步：出界或已经填过（非 0）就右转',
              '矩阵初始全 0，正好用来标记“没填过”，不需要额外的 visited'],
        summary=['时间 `O(n²)`，空间 `O(1)`（返回值不计）',
                 '易错：判断“已填过”必须在==界内==才能访问 `ans[x][y]`，所以出界判断写在 `or` 前面（短路）',
                 '易错：右转后要用==新的方向==走这一步，所以先改 `di` 再移动',
                 '同款套路：54. 螺旋矩阵、874. 模拟行走机器人'],
    ),
)

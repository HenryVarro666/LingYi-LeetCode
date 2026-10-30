def _order(n):
    """题解的填充顺序：右上 -> 右下 -> 左下 -> 左上"""
    out = []

    def go(u, l, size):
        if size == 1:
            out.append((u, l))
            return
        m = size // 2
        go(u, l + m, m)
        go(u + m, l + m, m)
        go(u + m, l, m)
        go(u, l, m)
    go(0, 0, 1 << n)
    return out


ORDER = _order(2)
POS = {p: k for k, p in enumerate(ORDER)}


def _color(S, i, j, v):
    val = S.get('val')
    if val is None:
        return None
    k = POS[(i, j)]
    if k == val - 1:
        return 'yellow'
    if k < val:
        return 'green'
    u, l, size = S['_inner'].get('u'), S['_inner'].get('l'), S['_inner'].get('size')
    if u is not None and u <= i < u + size and l <= j < l + size:
        return 'blue'
    return None


def _quad(S):
    I = S['_inner']
    if I.get('size') is None:
        return ''
    u, l, size = I['u'], I['l'], I['size']
    return f'当前子矩阵：左上角 `({u}, {l})`，边长 `size = {size}`，已填到 `val = {S.get("val")}`'


CONFIG = dict(
    num=3537, title='填充特殊网格', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='分治 · 四象限递归（写法二）',
    tags=['灵神题单·链表树与回溯', '难度分 1542'],
    code='''
class Solution:
    def specialGrid(self, n: int) -> List[List[int]]:
        a = [[0] * (1 << n) for _ in range(1 << n)]
        val = 0

        def dfs(u: int, l: int, size: int) -> None:
            if size == 1:
                nonlocal val
                a[u][l] = val
                val += 1
                return
            m = size // 2
            dfs(u, l + m, m)
            dfs(u + m, l + m, m)
            dfs(u + m, l, m)
            dfs(u, l, m)

        dfs(0, 0, 1 << n)
        return a
''',
    call='Solution().specialGrid(2)',
    expect=[[15, 12, 3, 0], [14, 13, 2, 1], [11, 8, 7, 4], [10, 9, 6, 5]],
    views=[
        dict(type='text', fn=_quad, size=24, h=50),
        dict(type='grid', var='a', label='a（蓝 = 当前子矩阵，黄 = 刚填的，绿 = 已填好）', cell=96, h=420, color=_color),
        dict(type='calls', h=200),
    ],
    watch=[('val', 'val', 'green'), ('u', lambda S: S['_inner'].get('u'), 'blue'), ('l', lambda S: S['_inner'].get('l'), 'pink'),
           ('size', lambda S: S['_inner'].get('size'), 'cyan')],
    skip=['a = [[0]', 'val = 0', 'nonlocal val', '                return', 'val += 1'],
    max_steps=75,
    captions={
        'def dfs': '定义 `dfs(u, l, size)`：填充左上角 `(u, l)`、边长 `size` 的子矩阵',
        'if size == 1': lambda S, B, r: (f'`size == 1`：只剩一个格子 `({S.u}, {S.l})`，直接填数' if S.size == 1
                                         else f'`size = {S.size} > 1`：还能四等分，继续往下递归'),
        'a[u][l] = val': lambda S, B, r: f'`a[{S.u}][{S.l}] = {S.val}`，然后 `val` 加一：这个格子拿到当前最小的数，下一个格子填更大的数',
        'val += 1': '`val` 加一 → {val}，下一个格子填更大的数',
        'm = size // 2': '边长是 2 的幂，可以整除：半边长 `m = {m}`',
        'dfs(u, l + m, m)': '==先填右上角象限==：数字最小',
        'dfs(u + m, l + m, m)': '==再填右下角象限==：数字比右上大',
        'dfs(u + m, l, m)': '==再填左下角象限==：数字比右下大',
        'dfs(u, l, m)': '==最后填左上角象限==：数字最大',
        'dfs(0, 0, 1 << n)': '从整个矩阵 `dfs(0, 0, {1 << n})` 开始',
        'return a': '全部填完，返回 `a`',
    },
    cards=dict(
        one_liner='右上 → 右下 → 左下 → 左上，四象限依次递归填数',
        complexity='时间 `O(4^n)`，空间 `O(n)`（不含返回值）',
        problem=['用 `0 ~ 2^2N - 1` 填满 `2^N × 2^N` 网格，满足：右上 < 右下 < 左下 < 左上，且每个象限本身也满足',
                 '示例：`N = 1` → `[[3,0],[2,1]]`',
                 '本视频：`N = 2`，4×4 网格'],
        quote='按照从小到大的顺序，依次递归填充四个象限（四等分矩阵）：右上角、右下角、左下角、左上角。递归边界：如果 d-u=1，只有一个格子，填充 a[u][l]=val，然后把 val 加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['全局计数器 `val` 从 0 开始，按顺序发数',
              '大矩阵先递归右上、再右下、左下、左上 → 四个象限的数字天然满足大小关系',
              '写法二：子矩阵是正方形，`d = u + size`、`r = l + size`，只传 `u, l, size`',
              '递归到 `size == 1` 就填一个数，所以每个格子恰好填一次'],
        summary=['时间 `O(4^n)`：每个格子恰好访问一次',
                 '空间 `O(n)`：递归深度 n（返回的矩阵不计）',
                 '易错点：象限顺序是 ==右上、右下、左下、左上==，不是常见的 Z 字形',
                 '`val` 要用 `nonlocal`，否则在递归里改不了外层变量',
                 '写法一用 `dfs(u, d, l, r)` 四个参数，本质相同；扩展思考见 CF2093D'],
    ),
)

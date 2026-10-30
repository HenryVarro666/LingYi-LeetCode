G = [["B", "W", "B"], ["B", "W", "W"], ["B", "W", "B"]]


def _in(S, i, j):
    I, J = S.get('i'), S.get('j')
    if I is None or J is None:
        return False
    return I <= i <= I + 1 and J <= j <= J + 1


def _col(S, i, j, v):
    if not _in(S, i, j):
        return None
    return 'cyan' if v == 'B' else 'orange'


def _cnt(S):
    c = S.get('cnt')
    I, J = S.get('i'), S.get('j')
    if c is None or I is None:
        return ''
    return f"检查左上角 `({I},{J})` 的 2×2：B 出现 =={c.get('B', 0)}== 次，W 出现 =={c.get('W', 0)}== 次"


CONFIG = dict(
    num=3127, title='构造相同颜色的正方形', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='枚举 2×2 子矩形 · 计数', tags=[],
    code='''
class Solution:
    def canMakeSquare(self, grid: List[List[str]]) -> bool:
        def check(i: int, j: int) -> bool:
            cnt = defaultdict(int)
            cnt[grid[i][j]] += 1
            cnt[grid[i][j + 1]] += 1
            cnt[grid[i + 1][j]] += 1
            cnt[grid[i + 1][j + 1]] += 1
            return cnt['B'] != 2
        return check(0, 0) or check(0, 1) or check(1, 0) or check(1, 1)
''',
    call=f'Solution().canMakeSquare({G})',
    expect=True,
    views=[
        dict(type='grid', var='grid', h=380, cell=110, color=_col),
        dict(type='text', fn=_cnt, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cnt', "dict(cnt) if 'cnt' in S else ''", 'cyan')],
    captions={
        'def check': '`check(i, j)`：判断左上角在 `(i, j)` 的 2×2 是否能变纯色',
        'cnt = defaultdict': '`check({i}, {j})`：新建计数表，统计这个 2×2 里 B、W 各几个',
        'cnt[grid[i][j]]': '数入 `{grid[i][j]}`（左上）→ `{dict(cnt)}`',
        'cnt[grid[i][j + 1]]': '数入 `{grid[i][j + 1]}`（右上）→ `{dict(cnt)}`',
        'cnt[grid[i + 1][j]]': '数入 `{grid[i + 1][j]}`（左下）→ `{dict(cnt)}`',
        'cnt[grid[i + 1][j + 1]]': '数入 `{grid[i + 1][j + 1]}`（右下）→ `{dict(cnt)}`',
        "cnt['B'] != 2": lambda S, B, r: (f"B 有 {S.cnt.get('B', 0)} 个、W 有 {S.cnt.get('W', 0)} 个：" +
                                          ('刚好 2:2，改一个格子也凑不齐 → False' if S.cnt.get('B', 0) == 2 else '某色 ≥ 3 个，把另一个改色即可（或本来就纯色）→ True')),
        'return check(0, 0)': '依次检查四个 2×2：先 `check(0, 0)`，只要有一个返回 True，`or` 就短路，整题为 True',
    },
    skip=[],
    cards=dict(
        one_liner='3×3 里只有 4 个 2×2，逐个数一数 B 和 W',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['3×3 的黑白矩阵，至多改一个格子的颜色', '问能否得到一个 2×2 颜色完全相同的正方形',
                 '示例：`[[B,W,B],[B,W,W],[B,W,B]]` → `true`（改 `grid[0][2]`）'],
        quote='对于每个子矩形，统计 B 和 W 的个数，如果其中一个字母的出现次数 ≥ 3，则返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['4 个格子里某色 ≥ 3：最多改 1 个就纯色（4 个同色则不用改）',
              '两色必然都不到 3 个 ⇔ 恰好 2:2，所以判断 `cnt[\'B\'] != 2` 即可',
              '四个左上角 (0,0)(0,1)(1,0)(1,1) 全枚举'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '==2:2 是唯一不行的情况==；1:3、0:4 都行',
                 '`cnt[\'B\'] != 2` 与「某色 ≥ 3」等价，因为总数是 4',
                 '原文注：也可判断某字母出现次数 ≥ 3；还可只统计 ASCII 最低位代替字母'],
    ),
)

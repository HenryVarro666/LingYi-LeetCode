GRID = [[9, 1, 7], [8, 9, 2], [3, 4, 6]]


def _cells(S):
    g = S.get('grid')
    return g


def _color(S, i, j, v):
    if 'd1' not in S:
        return None
    return None


def _eq(S):
    if 'd1' not in S:
        return '每个数应出现一次；`a` 出现两次，`b` 一次都没出现'
    m = S['m']
    s = f"`d1` = 实际和 − 理论和 = `a − b` = =={S['d1']}=="
    if 'd2' in S:
        s += f"\n`d2` = 实际平方和 − 理论平方和 = `a² − b²` = =={S['d2']}=="
        s += f"\n`a + b` = d2 / d1 = {S['d2'] // S['d1']}"
    return s


CONFIG = dict(
    num=2965, title='找出缺失和重复的数字', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='数学 · 和与平方和',
    tags=['九、其他'],
    code='''
class Solution:
    def findMissingAndRepeatedValues(self, grid: List[List[int]]) -> List[int]:
        m = len(grid) ** 2
        # 注：两次遍历可以合并为一次遍历，这里只是为了方便实现用了两次遍历
        d1 = sum(x for row in grid for x in row) - m * (m + 1) // 2
        d2 = sum(x * x for row in grid for x in row) - m * (m + 1) * (m * 2 + 1) // 6
        return [(d2 // d1 + d1) // 2, (d2 // d1 - d1) // 2]
''',
    call=f'Solution().findMissingAndRepeatedValues({GRID})',
    expect=[9, 5],
    views=[
        dict(type='grid', var='grid', h=300, cell=90),
        dict(type='text', fn=_eq, size=28, h=190),
    ],
    watch=['m', 'd1', 'd2', ('a', 'ans', 'green')],
    captions={
        'm = len(grid)': '共 `n×n` 个格子，数值应是 `1..m`，`m = {m}`',
        'd1 =': '格子实际和 `{sum(x for row in grid for x in row)}` 减去 `1..{m}` 的和 `{m * (m + 1) // 2}`：`a` 多加一次、`b` 少加一次，所以 `d1 = a − b` = =={d1}==',
        'd2 =': '平方和同理：实际 `{sum(x * x for row in grid for x in row)}` 减去理论 `{m * (m + 1) * (m * 2 + 1) // 6}`，得 `d2 = a² − b²` = =={d2}==',
        'return [': '`a² − b² = (a+b)(a−b)`，所以 `a+b = d2 / d1 = {d2 // d1}`。解方程：`a = ({d2 // d1} + {d1}) / 2`，`b = ({d2 // d1} − {d1}) / 2` → `{ret}`',
    },
    cards=dict(
        after=[dict(heading='另外两种写法', lines=['方法一：`cnt` 数组计数，`O(n²)` 空间，最直观', '方法二：补上 `1..n²`，变成 260 题，用异或分组 `O(1)` 空间']),],
        one_liner='和与平方和各给一个方程，解出重复数 a 和缺失数 b',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['`n×n` 的网格，数值在 `1..n²`，一个数 `a` 出现两次，一个数 `b` 缺失',
                 '返回 `[a, b]`',
                 '示例：`[[9,1,7],[8,9,2],[3,4,6]]` → `[9,5]`'],
        quote='累加 grid 的所有元素（a 多加了一次，b 少加了一次），再减去 1 到 n² 的元素和，我们得到了 a-b。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['实际和 − 理论和 = `a − b`；平方和同理得 `a² − b²`',
              '平方差公式：`a² − b² = (a+b)(a−b)`，除以 `a−b` 得 `a+b`',
              '知道和与差，解方程得 `a`、`b`，只需 `O(1)` 额外空间'],
        summary=['时间 `O(n²)`，空间 `O(1)`',
                 '`a != b`，所以 `d1` 不为 0，可以做除法',
                 '先 `d2 // d1` 得 `a+b`，再加减 `d1` 后除以 2',
                 '方法一用 `cnt` 数组计数 `O(n²)` 空间；方法二转成 260 题用异或分组'],
    ),
)

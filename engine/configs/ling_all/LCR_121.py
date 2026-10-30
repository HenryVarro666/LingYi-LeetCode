PL = [[2, 3, 6, 8], [4, 5, 8, 9], [5, 9, 10, 12]]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if r == i and c == j:
        return 'yellow'
    if r < i or c > j:
        return 'purple'
    return None


def _dim(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return False
    return r < i or c > j


def _info(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or i >= len(S['plants']) or j < 0:
        return '从右上角出发：它是所在行最大、所在列最小，每次比较都能排除一整行或一整列'
    v = S['plants'][i][j]
    t = S['target']
    rel = '==等于==' if v == t else ('小于' if v < t else '大于')
    return f'`plants[{i}][{j}] = {v}` {rel} `target = {t}`'


CONFIG = dict(
    num='LCR 121', title='寻找目标值 - 二维数组', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='从右上角出发 · 排除一行或一列',
    tags=[],
    code='''
class Solution:
    def findTargetIn2DPlants(self, plants: List[List[int]], target: int) -> bool:
        if not plants:
            return False
        m, n = len(plants), len(plants[0])
        i, j = 0, n - 1  # 从右上角开始
        while i < m and j >= 0:  # 还有剩余元素
            if plants[i][j] == target:
                return True  # 找到 target
            if plants[i][j] < target:
                i += 1  # 这一行剩余元素全部小于 target，排除
            else:
                j -= 1  # 这一列剩余元素全部大于 target，排除
        return False
''',
    call='Solution().findTargetIn2DPlants([[2, 3, 6, 8], [4, 5, 8, 9], [5, 9, 10, 12]], 7)',
    expect=False,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='grid', var='plants', label='plants（黄 = 当前位置，紫 = 已排除的行/列）', h=330, cell=96,
             cursors=[('i', 'j', 'yellow', '(i,j)')], color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('target', 'target', 'yellow')],
    captions={
        'if not plants': '先处理空数组：没有元素，直接返回 False',
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'i, j = 0, n - 1': '从右上角 `({i}, {j})` 开始：它是==这一行最大、这一列最小==',
        'while i < m': lambda S, B, r: (f'`i = {S.i} < {S.m}` 且 `j = {S.j} ≥ 0`：还有剩余元素' if S.i < S.m and S.j >= 0
                                        else f'`i = {S.i}`、`j = {S.j}`：越界，剩余区域为空 → 找不到'),
        'if plants[i][j] == target': '`plants[{i}][{j}] = {plants[i][j]}`，是否等于 `target = {target}`？',
        'return True': '找到了 `target`',
        'if plants[i][j] < target': lambda S, B, r: (f'`{S.plants[S.i][S.j]} < {S.target}` 成立：这一行其余都更小' if S.plants[S.i][S.j] < S.target
                                                    else f'`{S.plants[S.i][S.j]} < {S.target}` 不成立：值更大，看这一列'),
        'i += 1': '当前值太小，这一行剩余元素都比它小 → 排除这一行，`i` → {i}',
        'j -= 1': '当前值太大，这一列剩余元素都比它大 → 排除这一列，`j` → {j}',
        'return False': '剩余矩阵排空都没找到，返回 =={ret}==',
    },
    cards=dict(
        one_liner='右上角是行最大、列最小，每次排除一整行或一整列',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['`m×n` 数组每行从左到右不减，每列从上到下不减，判断是否存在 `target`',
                 '示例：`[[2,3,6,8],[4,5,8,9],[5,9,10,12]]`, `target = 8` → `true`',
                 '本视频：同一数组，`target = 7` → `false`'],
        quote='从右上角开始 …… 这一行剩余元素全部小于 target，排除；这一列剩余元素全部大于 target，排除。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['右上角 `x` 是所在行最大值、所在列最小值',
              '`x < target`：这一行其余都更小，排除整行；`x > target`：这一列其余都更大，排除整列',
              '每步排除一行或一列，最多 `m + n` 步'],
        summary=['时间 `O(m+n)`，空间 `O(1)`',
                 '易错：先判 `not plants`，否则 `plants[0]` 越界',
                 '易错：循环条件是 `i < m and j >= 0`',
                 '也可以从左下角开始，方法类似'],
    ),
)

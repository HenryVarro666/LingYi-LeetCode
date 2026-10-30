M = [[1, -1], [-1, 1]]


def _bot(S):
    row = S.get('row')
    if row is None or 'matrix' not in S:
        return None
    for k, rw in enumerate(S['matrix']):
        if rw is row:
            return k
    return None


def _cell(S, r, c, v):
    i, b = S.get('i'), _bot(S)
    if i is None or b is None:
        return None
    return 'blue' if i <= r <= b else None


def _txt(S):
    i, b = S.get('i'), _bot(S)
    if i is None or b is None or 'col_sum' not in S:
        return '枚举上下边界 → 压成一行 `col_sum` → 套 560 题'
    return f'上边界 `{i}`，下边界 `{b}`：每列求和得 `col_sum = {S["col_sum"]}`'


CONFIG = dict(
    num=1074, title='元素和为目标值的子矩阵数量', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举上下边界 + 前缀和哈希表',
    tags=['前缀和与哈希表', '难度分 2189'],
    code='''
class Solution:
    # 560. 和为 K 的子数组
    def subarraySum(self, nums: List[int], k: int) -> int:
        ans = s = 0
        cnt = defaultdict(int)
        for x in nums:
            cnt[s] += 1
            s += x
            ans += cnt[s - k]
        return ans

    def numSubmatrixSumTarget(self, matrix: List[List[int]], target: int) -> int:
        n = len(matrix[0])
        ans = 0
        for i in range(len(matrix)):  # 上边界
            col_sum = [0] * n
            for row in matrix[i:]:  # 下边界
                for j, x in enumerate(row):
                    col_sum[j] += x
                ans += self.subarraySum(col_sum, target)
        return ans
''',
    call=f'Solution().numSubmatrixSumTarget({M}, 0)',
    expect=5,
    skip=['for j, x in enumerate(row)', 'for x in nums', 'ans = s = 0', 'n = len', 'ans = 0'],
    views=[
        dict(type='grid', var='matrix', label='matrix（蓝 = 当前上下边界之间的行）', cell=90, h=230, color=_cell),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='col_sum', label='col_sum（每列在上下边界内的和）', cell=90, h=150),
        dict(type='array', var='nums', label='nums（560 题的输入）', cell=90, h=140),
        dict(type='map', var='cnt', label='cnt（前缀和 → 次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=30),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'orange'), ('k', 'k'), ('ans', 'ans', 'green')],
    captions={
        'for i in range(len(matrix))': lambda S, B, r: (f'固定上边界 `i = {S.i}`' if 'i' not in B or S.i != B.i else '上边界也枚举完了'),
        'col_sum = [0] * n': '`col_sum` 记录第 i 行到下边界每一列的和，先清零',
        'for row in matrix[i:]': '下边界取下一行（没有下一行就换上边界）：上边界 `{i}` 到这一行是行范围',
        'ans += self.subarraySum': '子矩阵压成一维数组 `{col_sum}`，交给 560 题：数和为 `{target}` 的连续段',
        'cnt[s] += 1': '先把“更早的前缀和” `{s}` 记入 `cnt`，保证不会选出空子数组',
        's += x': '`x = {x}`，前缀和 `s` → {s}',
        'ans += cnt[s - k]': '要找左端前缀和 `s - k = {s - k}`，之前出现过 `{cnt[s - k]}` 次 → 就有这么多段和为 `{k}`',
        10: '这个一维数组里共有 `{ans}` 段和为 `{k}`，加到外层的 `ans`',
        21: '全部上下边界枚举完，答案 `{ans}`',
    },
    cards=dict(
        one_liner='枚举上下边界，把二维压成一维，再套 560 题',
        complexity='时间 `O(m²n)`，空间 `O(n)`',
        problem=['给矩阵 `matrix` 和 `target`，数元素和等于 `target` 的非空子矩阵个数',
                 '示例：`[[1,-1],[-1,1]]`，`target = 0` → `5`',
                 '两个 1x2、两个 2x1、一个 2x2'],
        quote='枚举子矩阵的上下边界，计算子矩阵每一列的元素和，我们可以得到一个一维数组……现在问题变成：在这个一维数组中，有多少个非空连续子数组，元素和等于 target？',
        quote_src='—— 灵茶山艾府题解',
        idea=['上边界 `i` 固定，下边界逐行下移，`col_sum` 随之累加',
              '子矩阵 = 上下边界 + 一段连续的列，即列和数组里的一段连续和',
              '一维问题就是 560 题：前缀和 + 哈希表，==先记入 cnt 再更新 s=='],
        summary=['时间 `O(m²n)`，空间 `O(n)`',
                 '`col_sum` 在每个上边界处重新清零，下边界下移时累加',
                 '560 题里 `cnt[s] += 1` 在 `s += x` 之前，初始 `s=0` 代表空前缀',
                 '同类题：560、974、525（前缀和 + 哈希表）'],
    ),
)

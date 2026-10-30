NUMS = [1, 2, 4, 6, 8, 9, 14, 15]
TARGET = 13


def _formula(S):
    if 'right' not in S:
        return f'有序数组里找两个数，和为 `target = {TARGET}`'
    l, r = S['left'], S['right']
    s = NUMS[l] + NUMS[r]
    rel = '>' if s > TARGET else '<' if s < TARGET else '=='
    return f"`numbers[{l}] + numbers[{r}] = {NUMS[l]} + {NUMS[r]} = {s}` {rel} `{TARGET}`"


def _mat(S):
    # 和矩阵 M[i][j] = numbers[i] + numbers[j]（行 i = 0..n-2，列 j = 1..n-1，只看 i < j）；已排除的行/列显示为 ·
    n = len(NUMS)
    l, r = (S['left'], S['right']) if 'right' in S else (0, n - 1)
    return [[NUMS[i] + NUMS[j] if i < j and l <= i and j <= r else None for j in range(1, n)] for i in range(n - 1)]


def _cap_if(S, B, ret):
    l, r, s = S.left, S.right, S.s
    if s > TARGET:
        return f'`{s} > {TARGET}`：`{NUMS[r]}` 加上==最小的== `{NUMS[l]}` 都太大 → 它和谁都凑不出 target'
    return f'`{s} < {TARGET}`：`{NUMS[l]}` 加上==最大的== `{NUMS[r]}` 都不够 → 它和谁都凑不出 target'


CONFIG = dict(
    num=167, title='两数之和 II - 输入有序数组', difficulty='Medium', category='双指针',
    author='灵茶山艾府', technique='相向双指针',
    tags=['面试经典150'],
    code='''
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while True:
            s = numbers[left] + numbers[right]
            if s == target:
                return [left + 1, right + 1]  # 题目要求下标从 1 开始
            if s > target:
                right -= 1
            else:
                left += 1
''',
    call=f'Solution().twoSum({NUMS}, {TARGET})',
    expect=[3, 6],
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='numbers', label='numbers（灰 = 已排除，不可能是答案）', cell=96, h=220,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else None) if 'right' in S else None),
        dict(type='table', var=_mat, label='和矩阵 numbers[i] + numbers[j]（i 行 j 列）：每步删掉一整行或一整列',
             rows=lambda S: list(range(len(NUMS) - 1)), cols=lambda S: list(range(1, len(NUMS))),
             cursors=[('left', 'right - 1', 'yellow')], cell=44, h=350,
             color=lambda S, i, j, v: 'green' if v == TARGET else None),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's'), ('target', 'target', 'green')],
    captions={
        'left = 0': '`left` 指向最小的数',
        'right = len': '`right = len(numbers) - 1 = {right}` 指向最大的数',
        'while True': lambda S, B, r: ('题目==保证答案一定存在== → 直接 `while True`，不用写 `left < right`' if 's' not in B
                                       else f'下一轮：候选区间缩小到 `[{S.left}, {S.right}]`'),
        's = numbers': '`s = {numbers[left]} + {numbers[right]} = {s}`',
        'if s == target': lambda S, B, r: (f'`{S.s} == {S.target}` → 找到了！' if S.s == S.target else f'`{S.s} ≠ {S.target}`，继续'),
        'return [left + 1': '找到：下标从 0 开始的 `({left}, {right})`，==返回时各加一== → `{ret}`',
        'if s > target': _cap_if,
        'right -= 1': '扔掉 `numbers[{B.right}] = {numbers[B.right]}`：`right` 左移到 {right}',
        'left += 1': '扔掉 `numbers[{B.left}] = {numbers[B.left]}`：`left` 右移到 {left}',
    },
    cards=dict(
        one_liner='和太大就扔掉最大的，和太小就扔掉最小的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`numbers` 已按==非递减顺序==排列，下标==从 1 开始==',
                 '找出两个数，使它们相加之和等于 `target`，返回 `[index1, index2]`',
                 '保证恰好有一个答案，只能用常数额外空间',
                 '本视频：`[1,2,4,6,8,9,14,15]`，`target = 13` → `[3,6]`'],
        quote='⚠注意：虽然题目说下标从 1 开始，但输入的 numbers 数组的下标仍然是从 0 开始的。我们应当==按照从 0 开始的下标写代码，只是在最后返回的时候，把下标加一==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s > target`：最大数加上==最小数==都超了 → 最大数和谁都不行，`right -= 1`',
              '`s < target`：最小数加上==最大数==都不够 → 最小数和谁都不行，`left += 1`',
              '每次 `O(1)` 地排除一个数，暴力要 `O(n²)` 才能知道的信息'],
        result='返回 `[3, 6]`：`4 + 9 = 13` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：返回 `[left + 1, right + 1]`，题目下标从 1 开始',
                 '题目保证有解才能写 `while True`；否则要写 `while left < right`',
                 '同类：15 三数之和、11 盛最多水的容器（相向双指针）'],
    ),
)

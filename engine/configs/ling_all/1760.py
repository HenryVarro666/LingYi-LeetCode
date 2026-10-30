NUMS = [7, 17]
OPS = 2


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'green'
    return None


def _ops(S):
    if 'm' in S and S['_line'] in (4, 5, 6, 7):
        m = S['m']
        return [(x - 1) // m for x in NUMS]
    return []


def _top(S):
    line = S['_line']
    if 'm' in S and line in (4, 5, 6, 7):
        m = S['m']
        os_ = [(x - 1) // m for x in NUMS]
        return f"每个袋子至多 `{m}` 球：操作 `{' + '.join(map(str, os_))}` = `{sum(os_)}` 次，要求 `≤ {OPS}`"
    if 'left' not in S:
        return f'最多操作 `{OPS}` 次：m 越大越省操作 → ==二分猜答案=='
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：里面 `{r - l - 1}` 个 m 还==不知道==行不行'
    return f'`left + 1 == right`：`{l}` 不行，`{r}` 可以 → 答案 =={r}=='


def _ret(S, B, ret):
    if ret:
        return f'`cnt = {S.cnt} ≤ maxOperations = {S.maxOperations}` → ==可以=='
    return f'`cnt = {S.cnt} > maxOperations = {S.maxOperations}` → ==不行==，操作次数超了'


CONFIG = dict(
    num=1760, title='袋子里最少数目的球', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 最小化最大值',
    tags=['灵神题单·二分算法', '难度分 1940'],
    code='''
class Solution:
    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        def check(m: int) -> bool:
            cnt = 0
            for x in nums:
                cnt += (x - 1) // m
            return cnt <= maxOperations

        left = 0  # 循环不变量 check(left) == False
        right = max(nums)  # 循环不变量 check(right) == True
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().minimumSize({NUMS}, {OPS})',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(max(NUMS) + 1)),
             label='候选上限 m（红 = 不行，绿 = 可以，灰 = 未知）',
             cell=48, index=False, color=_color, pointers={'left': 'red', 'mid': 'yellow', 'right': 'green'}, h=240),
        dict(type='array', var='nums', label='nums：每个袋子里的球数', cell=100, h=170),
        dict(type='array', var=_ops, label='每个袋子要的操作次数 (x−1)//m', cell=100, index=False, h=170),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'green'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'cyan'), 'maxOperations'],
    captions={
        'cnt = 0': '`cnt` 累计操作次数，从 0 开始',
        'cnt += (x': '`x = {x}`：分成每袋至多 `{m}` 球，需要 `(x − 1) // m = ({x} − 1) // {m} = {(x - 1) // m}` 次操作 → `cnt` = =={cnt}==',
        'return cnt <=': _ret,
        'left = 0': '`left = 0`：每袋 0 个球不可能，==恒为 False==',
        'right = max': '`right = max(nums) = {right}`：不用操作就满足，==恒为 True==',
        'while left + 1': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                          else f'`left + 1 == right = {S.right}`：开区间为空，==每个 m 都有结论=='),
        'mid = (left': '猜一个上限：`mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': '调用 `check({mid})`：每袋至多 `{mid}` 球，操作次数够不够？',
        'right = mid': '`mid` 够用，答案 ==≤ mid==：`right = {right}`，仍==恒为 True==',
        'left = mid': '`mid` 不够用，答案 ==> mid==：`left = {left}`，仍==恒为 False==',
        'return right': '`right` 是==最小的可行上限== → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='最小化最大值 → 先想二分：每袋球至多 m，要操作几次？',
        complexity='时间 `O(n log U)`，空间 `O(1)`，`U = max(nums)`',
        problem=['`nums[i]` 是第 `i` 个袋子里的球数；每次操作把一个袋子分成两个非空袋子',
                 '最多操作 `maxOperations` 次，使最大的袋子里球数（开销）最小',
                 '示例：`nums = [7, 17], maxOperations = 2` → `7`'],
        quote='假设最终每个袋子的球数都至多为 m，那么 m 越小，需要的袋子越多，操作次数也越多；m 越大，需要的袋子越少，操作次数也越少。有单调性，可以二分答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 个球分成 `k` 袋、每袋至多 `m`：`k·m ≥ x`，所以 `k ≥ ceil(x/m)`',
              '操作 `k − 1` 次得到 `k` 个袋子，所以一个袋子要 `ceil(x/m) − 1 = (x−1)//m` 次',
              '累加后和 `maxOperations` 比：`≤` 就更新 right，否则更新 left'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`ceil(x/m) − 1 = (x − 1) // m`，一步到位',
                 '别的语言要小心：`10^9` 个球 × 多个袋子累加会爆 32 位整数',
                 '另有 `bisect_left(range(max(nums)), True, 1, key=check)` 的库函数写法'],
    ),
)

NUMS = [2, 3, 1, 2, 4, 3]
TARGET = 7


def _cap_while(S, B, ret):
    s = B.s
    if s >= TARGET:
        return f'窗口和 `s = {s} ≥ {TARGET}`：==满足要求== → 记录长度，再试着缩小'
    return f'窗口和 `s = {s} < {TARGET}`：不满足要求 → 不再缩小，去扩展右端点'


def _info(S):
    if 's' not in S or 'right' not in S:
        return f'目标：子数组和 `≥ {TARGET}`，长度尽量小'
    l, r = S['left'], S['right']
    if l > r:
        return f'窗口为空，`s = {S["s"]}`'
    return f"窗口 `[{l}, {r}]` = `{S['nums'][l:r + 1]}`，和 `s = {S['s']}`，长度 `{r - l + 1}`"


CONFIG = dict(
    num='LCR 008', title='长度最小的子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口（循环内更新答案）',
    tags=[],
    code='''
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        ans = n + 1  # 也可以写 inf
        s = left = 0
        for right, x in enumerate(nums):
            s += x
            # while s - nums[left] >= target:
            #     s -= nums[left]
            #     left += 1
            # if s >= target:
            #     ans = min(ans, right-left+1)
            while s >= target:  # 满足要求
                ans = min(ans, right - left + 1)
                s -= nums[left]
                left += 1
        return ans if ans <= n else 0
''',
    call=f'Solution().minSubArrayLen({TARGET}, {NUMS})',
    expect=2,
    skip=['n = len'],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='nums', label='nums（青框 = 当前窗口 [left, right]）', h=250,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=lambda S: (f"最短长度 `ans = {S['ans']}`" + ('（还没找到，n + 1 代表无解）' if S['ans'] == len(NUMS) + 1 else ''))
             if 'ans' in S else '', size=28, h=70),
        dict(type='text', fn=lambda S: '枚举右端点 → 加进窗口；只要满足 `s ≥ target` 就==记录答案并右移左端点==', size=24, h=56),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('x', 'x'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = n + 1': '`ans = n + 1 = {ans}`：比任何合法长度都大，最后用它判断==有没有解==',
        's = left = 0': '窗口和 `s = 0`，左端点 `left = 0`',
        'for right, x in': lambda S, B, r: (f'枚举子数组右端点 `right = {S.right}`，新元素 `x = {S.x}`' if S.get('right') != B.get('right')
                                            else '右端点枚举完毕'),
        's += x': '`x = {x}` 进入窗口：`s = {B.s} + {x} = {s}`',
        'while s >= target': _cap_while,
        'ans = min(ans': '满足要求，用当前窗口长度更新：`ans = min({B.ans}, {right} − {left} + 1)` = =={ans}==',
        's -= nums[left]': '缩小窗口：`nums[{left}] = {B.s - s}` 离开，`s = {s}`',
        'left += 1': '左端点右移到 `{left}`：看看更短的窗口还满不满足',
        'return ans': lambda S, B, r: (f'`ans = {S.ans} ≤ n` → 找到了，返回 =={r}==' if S.ans <= len(NUMS) else '`ans = n + 1`：没有满足要求的子数组 → 返回 `0`'),
    },
    cards=dict(
        one_liner='枚举右端点，满足 s ≥ target 时记录答案并尽量右移左端点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定==正整数==数组 `nums` 和正整数 `target`',
                 '找出总和 `≥ target` 的==长度最小==的子数组，返回其长度；不存在返回 `0`',
                 '示例：`target = 7, nums = [2,3,1,2,4,3]` → `2`（子数组 `[4,3]`）'],
        quote='虽然写了个二重循环，但是==内层循环中对 left 加一的总执行次数不会超过 n 次==，所以总的时间复杂度为 O(n)。',
        quote_src='—— 灵茶山艾府题解（在 while 循环内更新答案的写法）',
        idea=['元素都是正数：窗口变长和变大，变短和变小 → ==单调性==，可以用滑动窗口',
              '枚举右端点 `right`，把 `x` 加进 `s`',
              '只要 `s ≥ target`：先用 `right − left + 1` 更新答案，再把 `nums[left]` 移出窗口'],
        summary=['时间 `O(n)`：left 和 right 都只右移，各最多 n 次',
                 '`ans` 初始 `n + 1`（或 inf），返回时判断 `ans <= n`，否则返回 0',
                 '写法一（注释里保留的）：`while s - nums[left] >= target` 先缩到最短，==循环结束后==再更新答案',
                 '思考题：有负数时单调性没了 → 862 题用前缀和 + 单调队列'],
    ),
)

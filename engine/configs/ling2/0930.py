NUMS = [1, 0, 1, 0, 1]
GOAL = 2


def _c1(S, i, v):
    if 'left1' not in S:
        return None
    return 'green' if i < S['left1'] else None


def _d1(S, i, v):
    return 'i' in S and i > S['i']


def _c2(S, i, v):
    if 'left2' not in S:
        return None
    return 'pink' if i < S['left2'] else None


def _text(S):
    if 'i' not in S or 'left2' not in S:
        return '恰好 `= goal` 的个数 = `≥ goal` 的个数 − `> goal` 的个数'
    i, a, b = S['i'], S['left1'], S['left2']
    if S.get('_line') in (12, 14, 15, 16, 17, 18):
        return f'右端点 `{i}`：左端点在 `[0, {a - 1}]` 和 ==≥ goal==，在 `[0, {b - 1}]` 和 ==> goal==' if a else f'右端点 `{i}`：还没有和 `≥ goal` 的子数组'
    return '恰好 `= goal` 的个数 = `≥ goal` 的个数 − `> goal` 的个数'


def _cap_w1(S, B, ret):
    if B.left1 <= B.i and B.sum1 >= GOAL:
        return f'`sum1 = {B.sum1} ≥ goal`：`[{B.left1}, {B.i}]` 满足要求 → 缩短窗口，左端点右移'
    if B.left1 > B.i:
        return '窗口空了，停止'
    if B.left1 == 0:
        return f'`sum1 = {B.sum1} < goal` → 停（以 `{B.i}` 结尾的子数组都还不够大）'
    return f'`sum1 = {B.sum1} < goal` → 停。`[{B.left1}, {B.i}]` 不满足，但更长的都满足'


def _cap_w2(S, B, ret):
    if B.sum2 > GOAL:
        return f'`sum2 = {B.sum2} > goal` → 左端点右移'
    return f'`sum2 = {B.sum2} ≤ goal` → 停'


def _cap_add(S, B, ret):
    if S.left1 == 0:
        return '`left1 = 0`：以 `i` 为右端点，还没有和 `≥ goal` 的子数组 → `ans += 0`'
    return (f'子数组==越长越合法==：左端点取 `0..{S.left1 - 1}` 都满足 `≥ goal`，'
            f'共 `{S.left1}` 个 → `ans = {S.ans}`')


def _cap_sub(S, B, ret):
    if S.left2 == 0:
        return f'`left2 = 0`：没有和 `> goal` 的 → `ans -= 0`，`ans = {S.ans}`'
    return f'左端点 `0..{S.left2 - 1}` 的和 `> goal`，减掉这 `{S.left2}` 个 → `ans = {S.ans}`'


CONFIG = dict(
    num=930, title='和相同的二元子数组', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='恰好型滑动窗口：≥ goal 减去 > goal',
    tags=['字节30天'],
    code='''
class Solution:
    def numSubarraysWithSum(self, nums: List[int], goal: int) -> int:
        ans = 0
        sum1 = sum2 = 0
        left1 = left2 = 0

        for i, x in enumerate(nums):
            sum1 += x
            while left1 <= i and sum1 >= goal:  # 避免 goal = 0 的情况下标越界
                sum1 -= nums[left1]
                left1 += 1
            ans += left1  # 先加上 >= goal 的子数组个数

            sum2 += x
            while sum2 > goal:
                sum2 -= nums[left2]
                left2 += 1
            ans -= left2  # 再减去 > goal 的，剩下的就是 = goal 的

        return ans
''',
    call=f'Solution().numSubarraysWithSum({NUMS}, {GOAL})',
    expect=4,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='窗口 1：和 ≥ goal（绿 = 能当左端点的位置，共 left1 个）', cell=110,
             pointers={'left1': 'green', 'i': 'blue'}, window=('left1', 'i'), color=_c1, dim=_d1, h=250),
        dict(type='array', var='nums', label='窗口 2：和 > goal（粉 = 要减掉的左端点，共 left2 个）', cell=110,
             pointers={'left2': 'pink', 'i': 'blue'}, window=('left2', 'i'), window_color='pink', color=_c2, dim=_d1, h=250),
    ],
    watch=[('i', 'i', 'blue'), ('sum1', 'sum1', 'green'), ('left1', 'left1', 'green'),
           ('sum2', 'sum2', 'pink'), ('left2', 'left2', 'pink'), ('ans', 'ans', 'yellow')],
    skip=['left1 = left2 = 0', 'sum1 += x', 'sum2 += x'],
    captions={
        'ans = 0': '`ans` 统计和恰好为 `goal = {goal}` 的子数组个数',
        'sum1 = sum2 = 0': '两个滑动窗口：窗口 1 数 ==和 ≥ goal==，窗口 2 数 ==和 > goal==',
        'for i, x in enumerate': lambda S, B, ret: (f'枚举右端点 `i = {S.i}`（`x = {S.x}`），两个窗口都把它加进来'
                                                    if 'i' not in B or B.i != S.i else '右端点枚举完毕'),
        'while left1 <= i': _cap_w1,
        'sum1 -= nums[left1]': '移出 `nums[{B.left1}]`：`sum1 = {sum1}`',
        'left1 += 1': '`left1` → {left1}',
        'ans += left1': _cap_add,
        'while sum2 > goal': _cap_w2,
        'sum2 -= nums[left2]': '移出 `nums[{B.left2}]`：`sum2 = {sum2}`',
        'left2 += 1': '`left2` → {left2}',
        'ans -= left2': _cap_sub,
        'return ans': '和恰好为 `goal` 的子数组共 =={ret}== 个',
    },
    cards=dict(
        one_liner='恰好 = goal 的个数 = (≥ goal 的个数) − (> goal 的个数)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二元数组 `nums`（只有 0 和 1），统计和为 `goal` 的==非空子数组==个数',
                 '示例 1：`nums = [1,0,1,0,1]`，`goal = 2` → `4`',
                 '`[1,0,1]`、`[1,0,1,0]`、`[0,1,0,1]`、`[1,0,1]`'],
        before=[dict(heading='灵神的类比', lines=[
            '某班有 10 个人至少 20 岁，3 个人至少 21 岁',
            '那么恰好 20 岁的人有多少个？',
            '「至少 20 岁」= 「恰好 20 岁」+「至少 21 岁」→ `10 − 3 = 7`',
        ])],
        quote='本题等价于如下两个问题：==元素和 ≥ goal== 的子数组个数。加到答案中。元素和 > goal 的子数组个数。从答案中减掉。',
        quote_src='—— 灵茶山艾府题解',
        idea=['没有负数 → 子数组==越长越合法==，是计数型滑窗：`ans += left`',
              '内层循环结束后 `[left, i]` 不满足，左端点在 `0..left-1` 的都满足',
              '同时跑两个窗口：`≥ goal` 的加上，`> goal` 的减掉'],
        summary=['时间 `O(n)`：两个 left 各自最多右移 `n` 次；空间 `O(1)`',
                 '易错：窗口 1 要判断 `left1 <= i`，否则 `goal = 0` 时下标越界',
                 '也可以转化成 `≤ goal` 减 `< goal`',
                 '本题和 560. 和为 K 的子数组相同，但没有负数，所以能用滑窗省掉哈希表'],
    ),
)

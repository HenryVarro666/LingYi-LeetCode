_N = [4, 2, 3, 6, 5, 7]


def _isp(v):
    return v > 1 and all(v % d for d in range(2, int(v ** 0.5) + 1))


def _pc(S, i, v):
    return 'green' if _isp(v) else None


def _eq(S):
    if 'i' not in S:
        return ''
    if not S.get('max_q') or not S.get('min_q'):
        return f"窗口 [{S['left']}, {S['i']}]：还没有质数"
    mx, mn = S['nums'][S['max_q'][0]], S['nums'][S['min_q'][0]]
    return f"窗口质数：最大 `{mx}` − 最小 `{mn}` = =={mx - mn}== （k = {S['k']}），`last2 − left + 1` = {S['last2']} − {S['left']} + 1 = =={S['last2'] - S['left'] + 1}=="


CONFIG = dict(
    num=3589, title='计数质数间隔平衡子数组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='不定长滑窗 + 双单调队列',
    tags=['单调队列', '滑动窗口', '难度分 2235'],
    setup='''
from math import isqrt
MX = 50_001
is_prime = [False] * 2 + [True] * (MX - 2)
for i in range(2, isqrt(MX) + 1):
    if is_prime[i]:
        for j in range(i * i, MX, i):
            is_prime[j] = False  # j 是质数 i 的倍数
''',
    code='''
class Solution:
    def primeSubarray(self, nums: List[int], k: int) -> int:
        min_q = deque()
        max_q = deque()
        last = last2 = -1
        ans = left = 0

        for i, x in enumerate(nums):
            if is_prime[x]:
                # 1. 入
                last2 = last
                last = i

                while min_q and x <= nums[min_q[-1]]:
                    min_q.pop()
                min_q.append(i)

                while max_q and x >= nums[max_q[-1]]:
                    max_q.pop()
                max_q.append(i)

                # 2. 出
                while nums[max_q[0]] - nums[min_q[0]] > k:
                    left += 1
                    if min_q[0] < left:
                        min_q.popleft()
                    if max_q[0] < left:
                        max_q.popleft()

            # 3. 更新答案
            ans += last2 - left + 1

        return ans
''',
    call='Solution().primeSubarray([4,2,3,6,5,7], 2)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 质数，蓝框 = 窗口 [left, i]）',
             pointers={'left': 'blue', 'i': 'pink', 'last2': 'orange'}, window=('left', 'i'), color=_pc, h=240),
        dict(type='queue', var='min_q', label='min_q（下标:值，队首 = 窗口质数最小值）', fmt=lambda i: f'{i}:{_N[i]}', h=110),
        dict(type='queue', var='max_q', label='max_q（下标:值，队首 = 窗口质数最大值）', fmt=lambda i: f'{i}:{_N[i]}', h=110),
        dict(type='text', fn=_eq, h=80),
    ],
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), ('last2', 'last2', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'last = last2 = -1': '`last`、`last2`：最近两个质数的下标，没有就是 −1',
        'ans = left = 0': '`ans` 累计答案；`left` 是窗口左端点',
        'for i, x in enumerate(nums)': '枚举右端点 `i = {i}`，`x = {x}`',
        'if is_prime[x]': lambda S, B, r: (f'`{S.x}` 是质数 → 要入窗口' if _isp(S.x) else f'`{S.x}` 不是质数 → 不影响极差，直接去算答案'),
        'last2 = last': '倒数第二个质数下标 `last2` = 原来的 `last` = {last2}',
        'last = i': '最新质数下标 `last = {last}`',
        'while min_q and x <= nums[min_q[-1]]': lambda S, B, r: (
            f'队尾 `{S.nums[S.min_q[-1]]} ≥ {S.x}`：新质数更小又更晚 → ==队尾没用了==' if S.min_q and S.x <= S.nums[S.min_q[-1]]
            else '队尾比 `x` 小（或队列空）→ 保留，停止'),
        'min_q.pop()': '弹掉 min_q 队尾',
        'min_q.append(i)': '`{i}` 入 min_q：值严格递增，==队首 = 最小质数==',
        'while max_q and x >= nums[max_q[-1]]': lambda S, B, r: (
            f'队尾 `{S.nums[S.max_q[-1]]} ≤ {S.x}`：新质数更大又更晚 → ==队尾没用了==' if S.max_q and S.x >= S.nums[S.max_q[-1]]
            else '队尾比 `x` 大（或队列空）→ 保留，停止'),
        'max_q.pop()': '弹掉 max_q 队尾',
        'max_q.append(i)': '`{i}` 入 max_q：值严格递减，==队首 = 最大质数==',
        'while nums[max_q[0]] - nums[min_q[0]] > k': lambda S, B, r: (
            f'极差 `{S.nums[S.max_q[0]]} − {S.nums[S.min_q[0]]} = {S.nums[S.max_q[0]] - S.nums[S.min_q[0]]} > {S.k}`：窗口太宽 → 缩左端点'
            if S.nums[S.max_q[0]] - S.nums[S.min_q[0]] > S.k
            else f'极差 `{S.nums[S.max_q[0]] - S.nums[S.min_q[0]]} ≤ {S.k}`：窗口合法'),
        'left += 1': '`left` 右移到 {left}，窗口收缩',
        'if min_q[0] < left': lambda S, B, r: ('min_q 队首已出窗口 → 出队' if S.min_q[0] < S.left else 'min_q 队首还在窗口里'),
        'if max_q[0] < left': lambda S, B, r: ('max_q 队首已出窗口 → 出队' if S.max_q[0] < S.left else 'max_q 队首还在窗口里'),
        'min_q.popleft()': 'min_q 队首出队',
        'max_q.popleft()': 'max_q 队首出队',
        'ans += last2 - left + 1': '右端点固定为 `{i}` 时，左端点可选 `[left, last2]`，共 `{last2} − {left} + 1` = =={last2 - left + 1}== 个（至少含两个质数）→ `ans` = {ans}',
        'return ans': '一共 =={ret}== 个质数间隔平衡子数组',
    },
    max_steps=130,
    cards=dict(
        one_liner='右端点固定时，合法左端点是 [left, 倒数第二个质数]',
        complexity='时间 `O(n)`（筛法预处理不计），空间 `O(n)`',
        problem=['子数组要==至少有两个质数==，且最大质数 − 最小质数 ≤ `k`',
                 '数出这样的子数组个数',
                 '本视频：`[4,2,3,6,5,7]`，`k = 2` → `7`'],
        quote='设 [0,i] 中的倒数第二个质数的下标为 last2。当窗口右端点固定为 i 时，合法子数组左端点的范围为 [left, last2]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['窗口越长，质数极差越大 → ==越短越合法==，可以用不定长滑窗',
              '用两个单调队列维护窗口内质数的最大值、最小值，极差超 `k` 就收左端点',
              '左端点还要保证窗口里至少两个质数，所以最多到 `last2`，个数 `last2 − left + 1`'],
        summary=['时间 `O(n)`；埃氏筛预处理 `is_prime`，不计入',
                 '`left ≤ last2 + 1` 恒成立，所以每次加的 `last2 − left + 1` 不会是负数',
                 '非质数不入队，但仍然要用 `last2` 统计答案',
                 '埃氏筛原写在类外面，视频里放在 `setup` 里执行（不逐行演示）',
                 '同类题：1438、3578'],
    ),
)

def _w(S):
    if 'left' not in S or 'i' not in S:
        return ''
    nums = S['nums']
    L, i = S['left'], S['i']
    if L > i:
        return ''
    seg = nums[L:i + 1]
    return f'窗口 `nums[{L}..{i}]`：最大 `{max(seg)}` − 最小 `{min(seg)}` = =={max(seg) - min(seg)}== （k = {S["k"]}）'


CONFIG = dict(
    num=3578, title='统计极差最大为 K 的分割方式数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 滑动窗口 + 单调队列',
    tags=['灵神题单·动态规划', '难度分 2033'],
    code='''
class Solution:
    def countPartitions(self, nums: List[int], k: int) -> int:
        MOD = 1_000_000_007
        n = len(nums)
        min_q = deque()
        max_q = deque()
        f = [0] * (n + 1)
        f[0] = 1
        sum_f = 0  # 窗口中的 f[i] 之和
        left = 0

        for i, x in enumerate(nums):
            # 1. 入
            sum_f += f[i]

            while min_q and x <= nums[min_q[-1]]:
                min_q.pop()
            min_q.append(i)

            while max_q and x >= nums[max_q[-1]]:
                max_q.pop()
            max_q.append(i)

            # 2. 出
            while nums[max_q[0]] - nums[min_q[0]] > k:
                sum_f -= f[left]
                left += 1
                if min_q[0] < left:
                    min_q.popleft()
                if max_q[0] < left:
                    max_q.popleft()

            # 3. 更新答案
            f[i + 1] = sum_f % MOD

        return f[n]
''',
    call='Solution().countPartitions([9,4,1,3,7], 4)',
    expect=6,
    skip=['MOD = 1_000', 'n = len(nums)', 'min_q = deque()', 'max_q = deque()', 'f = [0] * (n + 1)', 'left = 0', 'min_q.pop()', 'max_q.pop()'],
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 窗口 [left, i]，最后一段的左端点范围）', h=200, cell=80,
             pointers={'left': 'blue', 'i': 'pink'}, window=('left', 'i'),
             dim=lambda S, j, v: 'left' in S and 'i' in S and not (S['left'] <= j <= S['i'])),
        dict(type='text', fn=_w, size=24, h=70),
        dict(type='array', var='f', label='f（f[i] = 前 i 个数的分割方案数）', h=150, cell=80,
             color=lambda S, j, v: 'green' if 'i' in S and j == S['i'] + 1 and S.get('_line', 0) >= 33 else None),
        dict(type='queue', var='min_q', label='min_q（下标:值，队首 = 窗口最小）', h=110, fmt=lambda x: f'{x}', font=24),
        dict(type='queue', var='max_q', label='max_q（下标，队首 = 窗口最大）', h=110, fmt=lambda x: f'{x}', font=24),
    ],
    watch=[('i', 'i', 'pink'), ('left', 'left', 'blue'), ('sum_f', 'sum_f', 'green'), ('k', 'k')],
    captions={
        'f[0] = 1': '`f[0] = 1`：空数组算一种分割（递归到空 = 找到一个合法方案）',
        'sum_f = 0': '`sum_f` = 窗口内 `f[left..i]` 之和',
        'sum_f += f[i]': '右端点 `i = {i}` 入窗：`sum_f += f[{i}]` → =={sum_f}==（最后一段可以从 `i` 开始）',
        'x <= nums[min_q[-1]]': lambda S, B, r: (f'`x = {S.x}` ≤ 队尾值 `{S.nums[S.min_q[-1]]}`：队尾不可能再当最小 → ==弹出==' if S.min_q and S.x <= S.nums[S.min_q[-1]]
                                                 else '队尾比 x 小（或队空）→ 保持队列单调递增，停止弹出'),
        'min_q.append(i)': '`i = {i}` 入 `min_q`，队首就是窗口最小值的下标',
        'x >= nums[max_q[-1]]': lambda S, B, r: (f'`x = {S.x}` ≥ 队尾值 `{S.nums[S.max_q[-1]]}`：队尾不可能再当最大 → ==弹出==' if S.max_q and S.x >= S.nums[S.max_q[-1]]
                                                 else '队尾比 x 大（或队空）→ 保持队列单调递减，停止弹出'),
        'max_q.append(i)': '`i = {i}` 入 `max_q`，队首就是窗口最大值的下标',
        'while nums[max_q[0]]': lambda S, B, r: (f'最大 `{S.nums[S.max_q[0]]}` − 最小 `{S.nums[S.min_q[0]]}` = {S.nums[S.max_q[0]] - S.nums[S.min_q[0]]} > k = {S.k} → ==窗口不合法，要出==' if S.nums[S.max_q[0]] - S.nums[S.min_q[0]] > S.k
                                                 else f'最大 `{S.nums[S.max_q[0]]}` − 最小 `{S.nums[S.min_q[0]]}` = {S.nums[S.max_q[0]] - S.nums[S.min_q[0]]} ≤ k = {S.k} → 窗口合法，不再收缩'),
        'sum_f -= f[left]': '`left = {left}` 不能再作为最后一段的左端点：`sum_f -= f[{left}]` → {sum_f}',
        'left += 1': '`left` 右移到 {left}',
        'if min_q[0] < left': lambda S, B, r: (f'`min_q` 队首 `{S.min_q[0]}` < left = {S.left}：已滑出窗口 → 弹出' if S.min_q[0] < S.left else '`min_q` 队首还在窗口内'),
        'if max_q[0] < left': lambda S, B, r: (f'`max_q` 队首 `{S.max_q[0]}` < left = {S.left}：已滑出窗口 → 弹出' if S.max_q[0] < S.left else '`max_q` 队首还在窗口内'),
        'f[i + 1] = sum_f': '`f[{i+1}] = sum_f % MOD` = =={f[i+1]}==：最后一段左端点取 `[left, i]` 内任意位置，累加对应 `f[j]`',
        'return f[n]': '前 `{n}` 个数的分割方案数 `f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='划分型 DP：最后一段的左端点是一个滑动窗口，窗口内 f 求和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 切成若干连续非空子段，每段 ==最大值 − 最小值 ≤ k==，求方案数（对 `10^9+7` 取模）',
                 '示例：`nums = [9,4,1,3,7], k = 4` → `6`',
                 '本视频用同一个示例'],
        quote='子数组越长，最大值越大，最小值越小，最大最小的差值越可能大于 k。所以符合要求的左端点 j 一定在一个==连续区间== [L, i] 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i+1] = f[L] + … + f[i]`，边界 `f[0] = 1`',
              '`i` 越大 `L` 也越大 → ==滑动窗口==，用 `sum_f` 维护窗口内 f 之和',
              '窗口最大最小值用两个==单调队列==，入、出、更新答案三步走'],
        summary=['时间 `O(n)`：每个下标最多入队、出队各两次；空间 `O(n)`',
                 '易错：`f[i+1] = sum_f` 要取模；入窗用 `f[i]`，不是 `f[i+1]`',
                 '出队时要判断队首下标是否已 `< left`',
                 '也可写成 `O(n^2)` 暴力枚举 `j`；同类题：2762. 不间断子数组'],
    ),
)

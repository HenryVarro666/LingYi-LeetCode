def _inq(S, i):
    q = S.get('q')
    return q is not None and i in list(q)


def _txt(S):
    if 'q' not in S or 'i' not in S:
        return '`f[i]` = 从 0 跳到 i 的最大得分；队列里放 `f` 严格递减的下标'
    i, q = S['i'], list(S['q'])
    if not q:
        return ''
    lo = max(i - S['k'], 0)
    return f"窗口 `[{lo}, {i - 1}]` 里 f 最大的是队首下标 =={q[0]}==，`f[{q[0]}] = {S['f'][q[0]]}`"


CONFIG = dict(
    num=1696, title='跳跃游戏 VI', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='单调队列优化 DP',
    tags=['灵神题单·动态规划', '难度分 1954'],
    code='''
class Solution:
    def maxResult(self, nums: List[int], k: int) -> int:
        n = len(nums)
        f = [0] * n
        f[0] = nums[0]
        q = deque([0])
        for i in range(1, n):
            # 1. 出
            if q[0] < i - k:
                q.popleft()
            # 2. 转移
            f[i] = f[q[0]] + nums[i]
            # 3. 入
            while q and f[i] >= f[q[-1]]:
                q.pop()
            q.append(i)
        return f[-1]
''',
    call='Solution().maxResult([1,-1,-2,4,-7,3], 2)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', h=190, cell=84, pointers={'i': 'blue'}),
        dict(type='array', var='f', label='f（绿 = 在队列里，蓝 = 当前 i）', h=130, cell=84,
             color=lambda S, i, v: 'green' if _inq(S, i) else ('blue' if i == S.get('i') else None)),
        dict(type='queue', var='q', label='q（存下标，队首最大）', h=120),
        dict(type='text', fn=_txt, size=24, h=50),
    ],
    watch=[('i', 'i', 'blue'), 'k', ('q', lambda S: list(S['q']) if 'q' in S else None, 'green')],
    skip=['n = len', 'f = [0] * n'],
    captions={
        'f[0] = nums[0]': '起点：`f[0] = nums[0] = {f[0]}`',
        'q = deque': '队列只存下标，`f` 值从左到右严格递减',
        'for i in range': lambda S, B, r: ('下标都处理完了' if S.get('i') == B.get('i') else f'`i = {S.i}`：算 `f[{S.i}]`'),
        'if q[0] < i - k': lambda S, B, r: (f'队首 `{S.q[0]}` < `i-k = {S.i - S.k}`：已经跳不到 `{S.i}` → ==出队=='
                                              if S.q[0] < S.i - S.k else f'队首 `{S.q[0]}` ≥ `i-k = {S.i - S.k}`：还在窗口内，不用出队'),
        'q.popleft()': '队首离开窗口，弹出：`q = {list(q)}`',
        'f[i] = f[q[0]]': '队首就是窗口最大值：`f[{i}] = f[{q[0]}] + nums[{i}] = {f[q[0]]} + {nums[i]}` = =={f[i]}==',
        'while q and f[i]': lambda S, B, r: (f'`f[{S.i}] = {S.f[S.i]} ≥ f[{S.q[-1]}] = {S.f[S.q[-1]]}`：队尾又老又小，永远不会是最优 → ==弹出=='
                                             if S.q and S.f[S.i] >= S.f[S.q[-1]]
                                             else ('队列空了，停止弹出' if not S.q else f'`f[{S.i}] = {S.f[S.i]} < f[{S.q[-1]}] = {S.f[S.q[-1]]}`：队尾更大，保留，停止弹出')),
        'q.pop()': '弹出队尾：`q = {list(q)}`',
        'q.append(i)': '`i = {i}` 入队：`q = {list(q)}`（f 值保持递减）',
        'return f[-1]': '最后一个位置的最大得分：`f[{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='窗口内 f 的最大值，用单调队列 O(1) 取',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从下标 0 出发，每步最多往前跳 `k` 格，要走到 `n-1`',
                 '得分 = 经过的数之和，求最大得分',
                 '示例：`nums = [1,-1,-2,4,-7,3]`，`k = 2` → `7`'],
        quote='这是一个长度固定为 k 的滑动窗口最大值问题。……维护一个 f 值从左到右严格递减的单调队列。……本题 f[i] 不在要计算的最值中，所以是先获取最值，再入队。',
        quote_src='—— 灵茶山艾府题解',
        idea=['思考「最后一步」：从 `[i-k, i-1]` 里某个 `j` 跳来，`f[i] = max f[j] + nums[i]`',
              '朴素枚举 `j` 是 `O(nk)`；窗口最大值用单调队列',
              '每步三件事：==出==（队首过期）→ ==转移==（用队首）→ ==入==（弹掉不比它大的队尾）'],
        summary=['时间 `O(n)`：每个下标最多入队、出队各一次',
                 '易错：先转移后入队，因为 `f[i]` 不属于自己的窗口',
                 '入队弹出条件 `>=`：相等时旧的更早过期，没有保留价值',
                 '灵神还给了把 `f` 直接写进 `nums` 的空间优化写法，额外空间 `O(k)`',
                 '同类：239. 滑动窗口最大值、1425. 带限制的子序列和'],
    ),
)

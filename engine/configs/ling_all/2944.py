P0 = [26, 18, 6, 12, 49, 7, 45]


def _fml(S):
    if 'i' not in S or 'q' not in S:
        return '`f(i)` = 买第 i 个水果、并拿下 i 之后所有水果的最少金币'
    i, n = S['i'], S['n']
    if S['_line'] <= 8:
        return f'`i = {i}`：下一个购买的水果 `j` 在窗口 `[{i + 1}, {2 * i + 1}]` 里，取 ==窗口里 f 最小的==（队尾）'
    return f"`f({i}) = prices[{i - 1}] + 窗口最小 f` = `{S['prices'][i - 1]} + {S['q'][-1][1]}` = =={S['f']}=="


def _color(S, k, v):
    if 'i' not in S or 'q' not in S:
        return None
    i = S['i']
    if k == i - 1:
        return 'yellow'
    if i <= k <= 2 * i:
        return 'blue'
    if k > 2 * i:
        return None
    return None


def _cap_w1(S, B, ret):
    j = S.q[-1][0]
    if j > S.i * 2 + 1:
        return f'队尾下标 `{j} > {S.i * 2 + 1}` = 窗口右端 → ==右边离开窗口==，弹出'
    return f'队尾下标 `{j} ≤ {S.i * 2 + 1}`，仍在窗口内 → 队尾 `f = {S.q[-1][1]}` 就是窗口最小值'


def _cap_w2(S, B, ret):
    if S.f <= S.q[0][1]:
        return f'新 `f = {S.f} ≤ 队首 {S.q[0][1]}`：下标更小(留得更久)又不更大 → 队首 ==永远不会是最小值==，弹出'
    return f'新 `f = {S.f} > 队首 {S.q[0][1]}`：队首更小，保留，新的从左边入队'


CONFIG = dict(
    num=2944, title='购买水果需要的最少金币数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='倒序 DP · 单调队列优化',
    tags=['灵神题单·动态规划', '难度分 1709'],
    code='''
class Solution:
    def minimumCoins(self, prices: List[int]) -> int:
        n = len(prices)
        q = deque([(n + 1, 0)])  # 哨兵
        for i in range(n, 0, -1):
            while q[-1][0] > i * 2 + 1:  # 右边离开窗口
                q.pop()
            f = prices[i - 1] + q[-1][1]
            while f <= q[0][1]:
                q.popleft()
            q.appendleft((i, f))  # 左边进入窗口
        return q[0][1]
''',
    call=f'Solution().minimumCoins({P0})',
    expect=39,
    views=[
        dict(type='text', fn=_fml, size=24, h=60),
        dict(type='array', var='prices', label='prices（黄 = 第 i 个水果，蓝 = 下一个购买的候选 j ∈ [i+1, 2i+1]）', h=190, cell=84, color=_color),
        dict(type='queue', var='q', label='q：(下标 j, f(j))，队首在左；队尾 = 窗口最小值', h=130, fmt=lambda t: f'{t[0]}:{t[1]}'),
    ],
    watch=[('n', 'n', 'cyan'), ('i', 'i', 'blue'), ('窗口', "f'[{i+1}, {2*i+1}]'", 'pink'), ('f', 'f', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'q = deque': '队列里存 `(下标, f)`。哨兵 `(n+1, 0)`：下标越过末尾，==后面没有水果，代价 0==',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：倒着算，因为 `f(i)` 依赖更大的 `f(j)`' if 'i' in S and S.i != B.get('i') and S.i >= 1 else '所有水果都算完，`f(1)` 在队首'),
        'while q[-1][0]': _cap_w1,
        'f = prices[i - 1]': '`f({i}) = prices[{i-1}] + 窗口最小 = {prices[i-1]} + {q[-1][1]}` = =={f}==',
        'while f <= q[0][1]': _cap_w2,
        'q.pop()': '弹出队尾：下标已超出窗口，别的 j 不能再从它转移',
        'q.popleft()': '弹出队首：它被新的 f 取代了',
        'q.appendleft': '`({i}, {f})` 从左边进入窗口；队列保持 f 从左到右递减',
        'return q[0][1]': '队首就是 `f(1)`：买第 1 个水果的最少金币 = =={ret}==',
    },
    cards=dict(
        one_liner='f(i) 的转移范围是向左滑动的窗口 → 单调队列求窗口最小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`prices[i]` 是买第 `i+1` 个水果的价格；买第 `i` 个水果（从 1 起）可免费拿 `[i+1, 2i]`',
                 '免费拿到的水果仍可花钱买，以换取它的奖励',
                 '求拿到所有水果的最少金币',
                 f'示例：`prices = {P0}` → `39`'],
        quote='随着 i 的变小，j 的范围 [i+1,2i+1] 的左右边界也在变小，所以 [i+1,2i+1] 是一个向左的滑动窗口。计算 min f[j] 的过程本质上是在计算滑动窗口最小值。',
        quote_src='—— 灵茶山艾府题解（四、单调队列优化）',
        idea=['`dfs(i) = prices[i] + min(dfs(j))`，`j ∈ [i+1, 2i+1]`；先写记忆化搜索，再 1:1 翻译成递推',
              '倒着算，窗口 `[i+1, 2i+1]` 两端都向左移，是滑动窗口最小值',
              '队列存 `(下标, f)`：右边出窗口就弹队尾，新 `f` 不比队首大就弹队首'],
        summary=['时间 `O(n)`：每个下标入队出队各一次；朴素递推是 `O(n^2)`',
                 '易错：下标从 1 开始，取 `prices` 要减一；哨兵 `(n+1, 0)` 让后半段的 f 等于价格本身',
                 '队尾弹出条件是 `> 2i+1`；队首弹出条件是 `f <= 队首`（带等号）',
                 '题解还给了记忆化搜索和 `f[i-1] += min(f[i:2i+1])` 的递推写法'],
    ),
)

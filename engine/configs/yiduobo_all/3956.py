def _txt(S):
    q, g, s, ix = S.get('q'), S.get('g'), S.get('s'), S.get('index')
    h, t = S.get('head'), S.get('tail')
    if q is None or ix is None or h is None or h >= t:
        return '队列里是候选位置 p，`g[p] − s[p]` 递减；队首最优：`f[index] = g[p] + s[index] − s[p]`'
    p = q[h]
    return f"队首 `p = {p}`：`g[{p}] + s[{ix}] − s[{p}] = {g[p]} + {s[ix]} − {s[p]}` = =={g[p] + s[ix] - s[p]}=="


def _fcol(S, k, v):
    if S.get('index') == k and S.get('_line') in (22, 23, 24, 25, 26):
        return 'yellow'
    return None


CONFIG = dict(
    num=3956, title='M 个非重叠子数组最大和 I', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按个数分轮 DP + 单调队列选决策点',
    tags=['灵神题单·动态规划', '难度分 2061'],
    code='''
class Solution(object):
    def maximumSum(self, nums, m, l, r):
        
        n = len(nums)
        f = [0] * (n + 1)
        s = [0]
        for v in nums:
            s.append(s[-1] + v)

        res = None
        for _ in range(m):
            q = []
            head, tail = 0, 0

            g = f[:]
            f = [None] * (n + 1)

            for index in range(1, n + 1):
                if head < tail and index - q[head] > r:
                    head += 1

                if index >= l and g[index - l] is not None:
                    while tail > head and g[index - l] - s[index - l] > g[q[-1]] - s[q[-1]]:
                        q.pop()
                        tail -= 1
                    q.append(index - l)
                    tail += 1
                
                f[index] = f[index - 1]
                
                if head < tail and (f[index] is None or f[index] < g[q[head]] + s[index] - s[q[head]]):
                    f[index] = g[q[head]] + s[index] - s[q[head]]
        
        
            if res is None or res < f[-1]:
                res = f[-1]
            else:
                break

        return res
''',
    call='Solution().maximumSum([4,-5,2], 2, 1, 2)',
    expect=6,
    views=[
        dict(type='array', var='s', label='s（nums 的前缀和）', h=110, cell=70),
        dict(type='array', var='g', label='g（上一轮）', h=110, cell=70),
        dict(type='array', var='f', label='f（这一轮，· = None）', h=160, cell=70,
             pointers={'index': 'blue'}, color=_fcol),
        dict(type='array', var='q', label='q（候选位置 p）', h=190, cell=70,
             pointers={'head': 'pink'}, window=('head', 'tail - 1'), dim=lambda S, i, v: i < S.get('head', 0)),
        dict(type='text', fn=_txt, size=22, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('head', 'head', 'pink'), ('tail', 'tail', 'cyan'), ('res', 'res', 'green')],
    skip=['n = len', 'f = [0] * (n + 1)', 's = [0]', 'for v in nums', 's.append', 'q = []', 'head, tail = 0, 0', 'tail += 1', 'tail -= 1', 'head += 1', 'g = f[:]'],
    max_steps=90,
    captions={
        'res = None': '`res` 记录各个子数组个数下的最优，先为空',
        'for _ in range': lambda S, B, r: ('轮次做完' if S.get('_') is not None and S.get('_') == B.get('_') else '新的一轮：多选一个子数组；`q` 清空，`g` = 上一轮的 `f`（选 k−1 个）'),
        'g = f[:]': '`g` = 上一轮的结果（选 k−1 个）；`f` 重新开始',
        'f = [None] * (n + 1)': '`f[index]` = 前 index 个数里选 ==恰好 k 个==的最大和，`None` 表示不可能',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：算 `f[{S.index}]`' if S.get('index') != B.get('index') else '这一轮结束'),
        'if head < tail and index - q[head] > r': lambda S, B, r: (
            f'队首 `p = {S.q[S.head]}`，子数组长度 `{S.index - S.q[S.head]} > r = {S.r}` → ==过期，head 右移=='
            if S.head < S.tail and S.index - S.q[S.head] > S.r
            else ('队列空' if S.head >= S.tail else f'队首 `p = {S.q[S.head]}`，长度 `{S.index - S.q[S.head]} ≤ r`：仍可用')),
        'head += 1': '队首过期：`head` → {head}',
        'if index >= l and g[index - l]': lambda S, B, r: (
            f'最短长度 `l = {S.l}`：新决策点 `p = {S.index - S.l}` 刚好可用' + (
                '，且 `g[p]` 可行 → 考虑入队' if S.index >= S.l and S.g[S.index - S.l] is not None else '，但 `g[p]` 不可行（None）→ 跳过')
            if S.index >= S.l else f'`index = {S.index} < l`：还没有长度够的子数组'),
        'while tail > head and g[index - l]': lambda S, B, r: (
            f'新点 `{S.g[S.index - S.l] - S.s[S.index - S.l]}` > 队尾 `{S.g[S.q[-1]] - S.s[S.q[-1]]}`：更晚过期又更好 → ==淘汰队尾=='
            if S.tail > S.head and S.g[S.index - S.l] - S.s[S.index - S.l] > S.g[S.q[-1]] - S.s[S.q[-1]]
            else '队尾不比新点差（或队列空），停止弹出'),
        'q.pop()': '弹出队尾，`tail` 减 1 → {tail - 1}',
        'q.append(index - l)': '`p = {index - l}` 入队（`tail` 加 1）：`g[p] − s[p] = {g[index - l] - s[index - l]}`',
        'f[index] = f[index - 1]': '先取「不选 `nums[{index - 1}]`」：`f[{index}] = f[{index - 1}] = {f[index]}`',
        'if head < tail and (f[index] is None': lambda S, B, r: (
            '队列空，只能不选' if S.head >= S.tail else
            f'选以 `{S.index - 1}` 结尾的子数组：`{S.g[S.q[S.head]] + S.s[S.index] - S.s[S.q[S.head]]}` vs 不选 `{S.f[S.index]}`'),
        'f[index] = g[q[head]]': '选更大：`f[{index}] = g[{q[head]}] + s[{index}] − s[{q[head]}]` = =={f[index]}==',
        'if res is None or res < f[-1]': lambda S, B, r: (
            f'这一轮 `f[-1] = {S.f[-1]}`，之前最好 `{S.res}`' + ('：更大 → 更新' if S.res is None or S.res < S.f[-1] else '：没有变大 → ==提前结束==')),
        'res = f[-1]': '`res` → =={res}==',
        'break': '多选子数组不再变好（题解里的剪枝）→ 停',
        'return res': '至多 m 个子数组的最大和 =={ret}==',
    },
    cards=dict(
        one_liner='先按子数组个数分轮，每轮用单调队列挑最优左端点',
        complexity='时间 `O(nm)`，空间 `O(n)`',
        problem=['从 `nums` 里选至少 1 个、至多 `m` 个互不重叠的子数组',
                 '每个子数组长度在 `[l, r]`，使总和最大',
                 '示例：`[4,1,-5,2]`，`m=2`，`l=1`，`r=2` → `7`；本视频用 `[4,-5,2]` → `6`'],
        quote='对于两个决策点p和q，若满足p < q，且f[p][k - 1] - s[p] <= f[q][k - 1] - s[q]，那么p就不会再成为后续index的最优决策点了',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index][k]`：前 index 个元素选 k 个的最大和；不选 `nums[index-1]`，或枚举左端点 p',
              '转移 `f[p][k-1] + s[index] − s[p]`：`s[index]` 与 p 无关，找 `f[p][k-1] − s[p]` 最大的 p',
              'p 的范围是随 index 右移的窗口 → 单调队列；按 k 分轮，用滚动数组省掉 k 这一维'],
        summary=['时间 `O(nm)`，空间 `O(n)`（滚动 `f` / `g`）',
                 '用 `None` 表示不可能的状态，比较前要先判断',
                 '答案是各轮 `f[-1]` 的最大值（至少选一个、至多 m 个）',
                 '`else: break` 是原文代码里的剪枝：多选一个若没变好就停',
                 '对比灵神：他用 `-inf` 表示不可能，并用 `j` 从 `i*left` 开始的范围省掉判断'],
    ),
)

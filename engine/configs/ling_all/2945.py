def _cap_pop(S, B, ret):
    q, s, last, i = S.q, S.s, S.last, S.i
    if len(q) > 1:
        a = s[q[1]] + last[q[1]]
        if a <= s[i]:
            return f'队里第二个 `j={q[1]}`：`s[j]+last[j]` = `{a}` ≤ `s[{i}]` = {s[i]} → ==队首没用了==，弹出'
        return f'队里第二个 `j={q[1]}`：`s[j]+last[j]` = `{a}` > `s[{i}]` = {s[i]} → 它还接不上，==队首就是最大可用的 j=={q[0]}'
    return f'队里只剩一个，队首 `j={q[0]}` 就是转移来源'


def _cap_tail(S, B, ret):
    q, s, last, i = S.q, S.s, S.last, S.i
    if not q:
        return '队列空了，准备把 i 放进去'
    a, b = s[q[-1]] + last[q[-1]], s[i] + last[i]
    if a >= b:
        return f'队尾 `j={q[-1]}`：`{a}` ≥ 新的 `s[i]+last[i]` = `{b}` → 又靠前又更大，==永远用不上==，弹出'
    return f'队尾 `j={q[-1]}`：`{a}` < `{b}` → 保持严格递增，停止弹出'


def _fml(S):
    i = S.get('i')
    if i is None or S.get('_line', 0) < 11:
        return '`f[i]`：前 i 个数最多能切成几段；`last[i]`：此时最后一段的最小和'
    q = S['q']
    if not q:
        return f'`i = {i}`'
    j = q[0]
    return f'转移：`s[{i}] ≥ s[{j}] + last[{j}]` → `f[{i}] = f[{j}] + 1`，`last[{i}] = s[{i}] − s[{j}]`'


CONFIG = dict(
    num=2945, title='找到最大非递减数组的长度', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='单调队列优化 DP', tags=['动态规划', '单调队列优化 DP', '难度分 2943'],
    code='''
class Solution:
    def findMaximumLength(self, nums: List[int]) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        f = [0] * (n + 1)
        last = [0] * (n + 1)
        q = deque([0])
        for i in range(1, n + 1):
            # 1. 去掉队首无用数据（计算转移时，直接取队首）
            while len(q) > 1 and s[q[1]] + last[q[1]] <= s[i]:
                q.popleft()
            
            # 2. 计算转移
            f[i] = f[q[0]] + 1
            last[i] = s[i] - s[q[0]]
            
            # 3. 去掉队尾无用数据
            while q and s[q[-1]] + last[q[-1]] >= s[i] + last[i]:
                q.pop()
            q.append(i)
        return f[n]
''',
    call='Solution().findMaximumLength([6, 5, 1, 9])',
    expect=3,
    views=[
        dict(type='text', fn=_fml, size=24, h=50),
        dict(type='array', var='nums', label='nums（下标从 0）', h=120, cell=90, index=True,
             color=lambda S, k, v: 'blue' if S.get('i') is not None and k == S['i'] - 1 else None),
        dict(type='array', var='s', label='s 前缀和', h=130, cell=90, pointers={'i': 'blue', 'q[0]': 'green'}),
        dict(type='array', var='f', label='f', h=130, cell=90, pointers={'i': 'blue'}),
        dict(type='array', var='last', label='last', h=130, cell=90, pointers={'i': 'blue'}),
        dict(type='queue', var='q', h=130, fmt=lambda j: f'j={j}'),
    ],
    watch=[('i', 'i', 'blue'), ('队首 j', 'q[0]', 'green'), ('f[n]', 'f[-1]', 'green')],
    captions={
        'q = deque([0])': '队列里放转移来源 `j`，先放哨兵 `0`：`s[0] = 0, last[0] = 0`',
        'for i in range': '`i` 枚举前 `i` 个数（下标从 1 开始）',
        'while len(q) > 1 and s[q[1]]': _cap_pop,
        'f[i] = f[q[0]] + 1': '队首 `j = {q[0]}`：把 `nums[j..i-1]` 合成一段接在后面 → `f[{i}] = f[{q[0]}] + 1` = =={f[i]}==',
        'last[i] = s[i]': '最后一段的和 = `s[{i}] − s[{q[0]}]` = =={last[i]}==（j 越大越小，越利于后续转移）',
        'while q and s[q[-1]]': _cap_tail,
        'q.append(i)': '`i` 入队：队列里 `j` 和 `s[j]+last[j]` 都严格递增 → 队列 {list(q)}',
        'return f[n]': '最多能分成 `f[{n}]` = =={ret}== 段',
    },
    cards=dict(
        one_liner='把数组切成尽量多段，每段和不递减：DP + 单调队列找最大的 j',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次操作把一个子数组替换成它的和，求能得到的最长非递减数组长度',
                 '示例：`[4,3,2,6]` → `3`（把 `[3,2]` 合成 5）',
                 '本视频：`[6,5,1,9]` → `3`，即 `[6,6,9]`'],
        quote='考虑两个转移来源 j 和 k，如果 j<k 且 s[j]+last[j] >= s[k]+last[k]，……所以**永远不需要**从 f[j] 转移到 f[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心是错的：`[1,2,1,3,3]` 贪心得 `[1,2,7]`，正解 `[1,3,3,3]`',
              '`f[i]`、`last[i]`：切成最多段，且最后一段尽量小；条件 `s[i] ≥ s[j] + last[j]`',
              '队列里 `s[j]+last[j]` 严格递增：队首出队取最大可用 j，队尾弹出被压制的 j'],
        summary=['时间 `O(n)`：每个下标至多入队、出队各一次',
                 '`last` 不是单调的，所以滑窗优化 DP 是错的',
                 '`f` 非递减 + `j` 越大 `last` 越小，所以取最大的可用 `j`',
                 '同类：滑动窗口最大值 239（单调队列模板）；灵神另提供权值线段树做法'],
    ),
)

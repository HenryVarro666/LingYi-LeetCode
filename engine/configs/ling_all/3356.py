def _txt(S):
    if 'sum_d' not in S or 'i' not in S:
        return '差分数组 `diff` 的前缀和 `sum_d` = 当前下标 `i` 最多能被减掉的量'
    x, sd = S['x'], S['sum_d']
    if sd >= x:
        return f"`nums[{S['i']}] = {x}`，`sum_d = {sd}` ==够了=="
    return f"`nums[{S['i']}] = {x}`，`sum_d = {sd}`：==还差 {x - sd}==，要继续取询问"


CONFIG = dict(
    num=3356, title='零数组变换 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='双指针 + 差分数组',
    tags=['难度分 1913'],
    code='''
class Solution:
    def minZeroArray(self, nums: List[int], queries: List[List[int]]) -> int:
        diff = [0] * (len(nums) + 1)
        sum_d = k = 0
        for i, (x, d) in enumerate(zip(nums, diff)):
            sum_d += d
            while k < len(queries) and sum_d < x:  # 需要添加询问，把 x 减小
                l, r, val = queries[k]
                diff[l] += val
                diff[r + 1] -= val
                if l <= i <= r:  # x 在更新范围中
                    sum_d += val
                k += 1
            if sum_d < x:  # 无法更新
                return -1
        return k
''',
    call='Solution().minZeroArray([2,0,3,1], [[0,2,1],[1,3,1],[0,0,1],[2,3,2]])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=27),
        dict(type='array', var='nums', label='nums（要被减到 0）', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if 'sum_d' in S and i == S.get('i') and S['sum_d'] >= v else 'red' if 'sum_d' in S and i == S.get('i') else None)),
        dict(type='array', var='diff', label='diff（差分：区间 [l, r] 加 val）', pointers={'i': 'blue'}, h=200),
        dict(type='table', var='queries', label='queries [l, r, val]（按顺序取，粉 = 下一个要取的）', rows=lambda S: [f'#{j}' for j in range(len(S['queries']))],
             cols=['l', 'r', 'val'], h=240,
             color=lambda S, i, j, v: ('pink' if 'k' in S and i == S['k'] else 'green' if 'k' in S and i < S['k'] else None)),
    ],
    watch=['i', 'x', ('sum_d', 'sum_d', 'cyan'), ('k', 'k', 'green')],
    captions={
        'diff = [0]': '`diff` 长 `n + 1`：多一格，让 `diff[r + 1]` 在 `r = n - 1` 时不越界',
        'sum_d = k = 0': '`sum_d` 是 `diff` 的前缀和；`k` 是已经取用的询问个数（也就是答案）',
        'for i, (x, d)': lambda S, B, r: (f'看下标 `i = {S.i}`：`nums[i] = {S.x}`，要把它减到 0' if S.i != B.get('i') or 'k' not in B else '`nums` 遍历完，每个下标都减得够了'),
        'sum_d += d': '把 `diff[{i}] = {d}` 加进前缀和：`sum_d` {B.sum_d} → =={sum_d}==（前面询问对 `i` 的累计贡献）',
        'while k <': lambda S, B, r: (f'`sum_d = {S.sum_d} < x = {S.x}`，还有询问 `k = {S.k} < {len(S.queries)}` → 取下一个询问' if S.k < len(S.queries) and S.sum_d < S.x else (f'`sum_d = {S.sum_d} >= x = {S.x}`：减得够了，不用再取' if S.sum_d >= S.x else '询问已经取完了')),
        'l, r, val = queries': '取第 `{k}` 个询问：`[{l}, {r}]` 最多减 `{val}`',
        'diff[l] += val': '区间左端点 `diff[{l}]` += `{val}`',
        'diff[r + 1] -= val': '右端点后一位 `diff[{r + 1}]` -= `{val}`：差分只改两处',
        'if l <= i <= r': lambda S, B, r_: (f'`{S.l} <= {S.i} <= {S.r}`：`i` 在区间里 → 这个询问对 `nums[i]` 立刻生效' if S.l <= S.i <= S.r else f'`i = {S.i}` 不在 `[{S.l}, {S.r}]` 里：对当前位置没用，但对后面的位置有用，已记在 `diff`'),
        'sum_d += val': '`diff` 的前缀和 `sum_d` 是在枚举 `i` 之前算好的，这里要手动补上 `{val}` → `sum_d` = =={sum_d}==',
        'k += 1': '这个询问用掉了：`k` → =={k}==（再也不用回头处理）',
        'if sum_d < x': lambda S, B, r: (f'`sum_d = {S.sum_d} < x = {S.x}` 且询问用完 → 无法减到 0，返回 -1' if S.sum_d < S.x else f'`sum_d = {S.sum_d} >= x = {S.x}`：下标 `{S.i}` 搞定，看下一个'),
        'return k': '所有下标都满足 → 最少需要前 =={k}== 个询问',
    },
    skip=['sum_d = k = 0'],
    cards=dict(
        one_liner='从左到右扫 nums，不够减就继续取询问，k 只增不减',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['`queries[i] = [l, r, val]`：把 `nums[l..r]` 中每个数各自==最多==减 `val`',
                 '求最小的 `k`，使前 `k` 个询问按顺序处理后 `nums` 能变成全 0；不存在返回 `-1`',
                 '示例：`nums=[2,0,3,1]`，`queries=[[0,2,1],[1,3,1],[0,0,1],[2,3,2]]` → `4`'],
        quote='从左到右遍历 x=nums[i]，如果发现 x>sumD，那么就必须处理询问，直到 x≤sumD 为止。由于处理过的询问无需再处理，所以上述过程可以用双指针实现。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['每个下标最多能被减掉的量 = 覆盖它的询问的 `val` 之和，用==差分数组前缀和==得到',
              '`x` 比 `sum_d` 大就取下一个询问加进差分，取了就再也不用处理：`k` 是单调的',
              '若询问用完仍不够，说明无解 → `-1`'],
        summary=['时间 `O(n + q)`，空间 `O(n)`；比二分答案多快一个 `log`',
                 '`diff` 长度 `n + 1`，防止 `r + 1` 越界',
                 '取到的询问若包含当前 `i`，要手动 `sum_d += val`（因为这一格的 `d` 已经读过了）',
                 '另外两种写法：方法一 二分答案 + 差分检查（`O((n+q)log q)`）；方法二 Lazy 线段树',
                 '思考题：询问可任意顺序执行（`val = 1`）→ 3362 零数组变换 III'],
    ),
)

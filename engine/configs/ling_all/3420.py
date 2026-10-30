def _raised(S):
    nums, l, r = S['nums'], S.get('l'), S.get('r')
    if l is None or r is None or 'cnt' not in S:
        return ''
    out, m = [], 0
    for v in nums[l:r + 1]:
        m = max(m, v)
        out.append(m)
    return f'窗口 `[{l}, {r}]` = `{nums[l:r + 1]}` 抬成非递减：`{out}`，操作次数 =={S["cnt"]}== （k = {S["k"]}）'


def _qinfo(S):
    q = S.get('q')
    if not q:
        return '树：每棵树里的数都要变成树根的值'
    return '树（从窗口右到左）：' + '　'.join(f'根 {t[0]} × 大小 {t[1]}' for t in reversed(list(q)))


CONFIG = dict(
    num=3420, title='统计 K 次操作以内得到非递减子数组的数目', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='从右到左滑窗 + 单调栈建树',
    tags=['灵神题单·单调栈', '难度分 2855'],
    code='''
class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = cnt = 0
        q = deque()  # (根节点的值, 树的大小)
        r = n - 1
        for l in range(n - 1, -1, -1):
            # x 进入窗口
            x = nums[l]
            size = 1  # 统计以 x 为根的树的大小
            while q and x >= q[-1][0]:
                # 以 v 为根的树，现在合并到 x 的下面（x 和 v 连一条边）
                v, sz = q.pop()
                size += sz
                cnt += (x - v) * sz  # 树 v 中的数都变成 x
            q.append([x, size])

            # 操作次数太多，缩小窗口
            while cnt > k:
                # 操作次数的减少量，等于 nums[r] 所在树的根节点值减去 nums[r]
                tree = q[0]  # 最右边的树
                cnt -= tree[0] - nums[r]
                r -= 1
                # nums[r] 离开窗口后，树的大小减一
                tree[1] -= 1
                if tree[1] == 0:  # 这棵树是空的
                    q.popleft()

            ans += r - l + 1

        return ans
''',
    call='Solution().countNonDecreasingSubarrays([6,3,1,2,4,4], 7)',
    expect=17,
    max_steps=90,
    views=[
        dict(type='text', fn=_raised, size=24),
        dict(type='array', var='nums', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), h=240,
             dim=lambda S, i, v: 'l' in S and 'r' in S and not (S['l'] <= i <= S['r'])),
        dict(type='text', fn=_qinfo, size=24),
        dict(type='queue', var='q', label='q：[根的值, 树的大小]，队首 = 最右边的树', fmt=lambda t: f'{t[0]}×{t[1]}', h=200),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('cnt', 'cnt', 'orange'), ('k', 'k', 'cyan'), ('ans', 'ans', 'green')],
    skip=['n = len(nums)', 'ans = cnt = 0', 'r = n - 1', 'x = nums[l]', 'size = 1', 'tree = q[0]', 'r -= 1'],
    captions={
        'q = deque()': '`q` 里每个元素是一棵树 `[根的值, 树的大小]`：树里的数都要变成根的值',
        'while q and x >= q[-1][0]': lambda S, B, r: (
            f'`x = {S.x} ≥` 最左边那棵树的根 `{S.q[-1][0]}` → 这棵树挂到 x 下面，里面的数都要抬到 {S.x}'
            if S.q and S.x >= S.q[-1][0] else
            ('`q` 为空，x 自己成一棵树' if not S.q else f'`x = {S.x} <` 最左边树根 `{S.q[-1][0]}` → x 只能挂在它下面，不用合并')),
        'v, sz = q.pop()': '取出左边那棵树：根 `{v}`，大小 `{sz}`',
        'size += sz': '合并后 x 这棵树大小 = `{size}`',
        'cnt += (x - v) * sz': '这 `{sz}` 个数从 `{v}` 抬到 `{x}`：增加 `({x} − {v}) × {sz}` → `cnt = {cnt}`',
        'q.append': '新树 `[{x}, {size}]` 放到最左边，`q` = {list(q)}',
        'while cnt > k': lambda S, B, r: (
            f'`cnt = {S.cnt} > k = {S.k}` → 操作次数太多，==右端点 r 左移==缩小窗口'
            if S.cnt > S.k else f'`cnt = {S.cnt} ≤ k = {S.k}` → 窗口合法'),
        'cnt -= tree[0] - nums[r]': '队首 = 最右边的树 `[{tree[0]}, {tree[1]}]`，`nums[{r}] = {nums[r]}` 在其中，它离开后不用再抬到 `{tree[0]}`：少 `{tree[0]} − {nums[r]}` → `cnt = {cnt}`',
        'tree[1] -= 1': '`r` 左移到 `{r}`，这棵树大小减一 → `{tree[1]}`',
        'if tree[1] == 0': lambda S, B, r: ('树空了，从队首删除' if S.tree[1] == 0 else '树里还有数，保留'),
        'q.popleft()': '删掉空树，`q` = {list(q)}',
        'ans += r - l + 1': '左端点是 `{l}`，右端点取 `{l}..{r}` 都合法，共 `{r - l + 1}` 个 → `ans = {ans}`',
        'return ans': '共 `{ans}` 个子数组',
    },
    cards=dict(
        one_liner='把「变成树根的值」当成树：加数是合并树，缩窗是删叶',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次操作可让子数组里一个数加 1。问有多少个子数组，最多 `k` 次操作能变成非递减',
                 '贪心：每个数抬到它左边的最大值，操作次数 = Σ(前缀最大 − 自身)',
                 '示例：`nums = [6,3,1,2,4,4]`，`k = 7` → `17`'],
        quote='右端点 nums[r] 离开窗口时，操作次数的减少量，等于 nums[r] 所属那棵树的根节点的值，减去 nums[r]。同时，把 nums[r] 所属子树的大小减一。',
        quote_src='—— 灵茶山艾府题解（方法二：从右到左滑窗）',
        idea=['倒序枚举左端点 `l`，用单调队列存「树」`[根值, 大小]`',
              '`x` 进窗口：弹出所有 ≤ x 的树并到 x 下面，每个数从 `v` 抬到 `x`',
              '`cnt > k` 就缩右端点：减去「根值 − nums[r]」，树大小减一'],
        summary=['时间 `O(n)`（每棵树入队出队各一次），空间 `O(n)`',
                 '子数组越长操作越多，有单调性 → 滑动窗口；这里是 ==从右往左== 滑',
                 '`q` 队首是最右边的树，队尾是刚加入的最左边的树',
                 '方法一是从左到右滑窗，要建「左侧最近更大」的树再做删边，写法更繁，视频讲的是方法二',
                 '思考题：所有子数组最小操作次数之和 → 贡献法'],
    ),
)

NUMS, K = [2, 1, 2], 1


def _arr(S):
    return S.get('a') or S.get('nums') or []


def _f(S):
    f = S.get('f')
    if f is None:
        return []
    return ['∞' if v == float('inf') else v for v in f]


def _txt(S):
    if 'ops' not in S:
        if 'cnt' in S:
            return f'先数环形数组里已有的峰值：`cnt = {S["cnt"]}`，需要 `k = {S["k"]}` 个'
        return '环形数组至多 `n // 2` 个峰值；断开成普通数组后，首尾不能是峰值'
    left, i = S.get('left'), S.get('i')
    if left is None or i is None or S.get('_line', 0) < 14:
        return f'`ops[i-1]` = 把 `a[i]` 抬成峰值的代价：`ops = {S["ops"]}`'
    return (f'`f[{i + 1}]` = min(不选 `{S["f"][i]}`, 选 `f0 + ops[{i - 1}]` = `{S["f0"]} + {S["ops"][i - 1]}`)；`left = {left}`')


CONFIG = dict(
    num=3892, title='产生至少 K 个峰值的最少操作次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='环形拆成两个普通数组 + 选或不选 DP（空间优化）',
    tags=['动态规划', '难度分 2280'],
    code='''
class Solution:
    # 非环形版本
    def solve(self, a: List[int], k: int) -> int:
        n = len(a)
        # 避免在循环中反复计算操作次数
        ops = [max(max(a[i - 1], a[i + 1]) - a[i] + 1, 0) for i in range(1, n - 1)] 

        f = [0] * n
        for left in range(1, k + 1):
            f0, f1 = f[left * 2 - 2], f[left * 2 - 1]
            f[left * 2 - 1] = inf
            for i in range(left * 2 - 1, n - 1 - (k - left) * 2):
                # 选或不选
                not_choose = f[i]
                choose = f0 + ops[i - 1]
                f0 = f1
                f1 = f[i + 1]  # 保存旧数据
                f[i + 1] = min(not_choose, choose)
        return f[-1]

    def minOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if k > n // 2:
            return -1

        cnt = 0
        for i in range(n):
            if nums[i - 1] < nums[i] > nums[(i + 1) % n]:
                cnt += 1
        if cnt >= k:  # 优化：已经有至少 k 个峰值了，无需操作
            return 0

        # 如果 nums[0] 是峰值，那么 nums[-1] 不是峰值
        ans1 = self.solve([nums[-1]] + nums, k)
        # 如果 nums[0] 不是峰值
        ans2 = self.solve(nums + [nums[0]], k)
        return min(ans1, ans2)
''',
    call=f'Solution().minOperations({NUMS!r}, {K})',
    expect=1,
    skip=['n = len(', 'for i in range(n)', 'for left in range', 'for i in range(left', 'f0 = f1', 'f1 = f[i + 1]', 'cnt = 0', 'not_choose = f[i]', 'f = [0] * n'],
    max_steps=70,
    views=[
        dict(type='array', var=_arr, label='当前数组（solve 里是断开后的普通数组 a）', h=215, cell=84,
             pointers={'i': 'blue'}),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var=lambda S: S.get('ops') or [], label='ops：把 a[i] 变成峰值的代价（下标从 a[1] 起）', h=170, cell=84),
        dict(type='array', var=_f, label='f[i]：前缀里凑够 left 个峰值的最少操作（∞ = 不可能）', h=190, cell=84),
    ],
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), ('cnt', 'cnt', 'yellow'), ('ans1', 'ans1', 'green'), ('ans2', 'ans2', 'green')],
    captions={
        'if k > n // 2': '环形数组至多 `n // 2 = {n // 2}` 个峰值（峰值不相邻），`k = {k}` ==不超过它==才有解',
        'if nums[i - 1] < nums[i]': lambda S, B, r: (f'`nums[{S.i}]={S.nums[S.i]}` 比两侧 `{S.nums[S.i - 1]}`、`{S.nums[(S.i + 1) % S.n]}` =={"都大 → 是峰值" if S.nums[S.i - 1] < S.nums[S.i] > S.nums[(S.i + 1) % S.n] else "不是峰值"}==（下标取模，首尾相邻）'),
        'cnt += 1': '已有峰值 `cnt = {cnt}`',
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} ≥ k = {S.k}`：已经够了，==无需操作== → 返回 0' if S.cnt >= S.k else f'`cnt = {S.cnt} < k = {S.k}`：还要操作，把环拆成普通数组'),
        'ans1 = self.solve': '`nums[0]` 是峰值 → `nums[-1]` 不是：把 `nums[-1]` 放最左边，`a = {[nums[-1]] + nums}`',
        'ans2 = self.solve': '`nums[0]` 不是峰值：把 `nums[0]` 放最右边，`a = {nums + [nums[0]]}`',
        'ops = [': lambda S, B, r: f'`ops[i-1]` = `max(max(a[i-1], a[i+1]) - a[i] + 1, 0)`：把 `a[i]` 抬到比两侧都高，`ops = {S.ops}`',
        'f[left * 2 - 1] = inf': lambda S, B, r: f'`left = {S.left}`：凑 `{S.left}` 个峰值至少要 `{S.left * 2 - 1}` 个数，前面的位置不可能 → 设 ∞',
        'choose = f0 + ops': lambda S, B, r: f'选 `a[{S.i}]` 当峰值：`a[{S.i - 1}]` 不能是峰值，用旧的 `f0 = {S.f0}` 加代价 `ops[{S.i - 1}] = {S.ops[S.i - 1]}` → `choose = {S.choose}`',
        'f[i + 1] = min': lambda S, B, r: f'`f[{S.i + 1}] = min(不选 {S.not_choose}, 选 {S.choose})` = =={S.f[S.i + 1]}=='.replace('inf', '∞'),
        'return f[-1]': '`f[-1]` = 整个数组凑够 `k` 个峰值的最少操作：=={ret}==',
        'return min(ans1, ans2)': '两种拆法取更小：`min({ans1}, {ans2})` = =={ret}==',
    },
    cards=dict(
        one_liner='环形拆成普通数组，再「选或不选」做 DP',
        complexity='时间 `O(k(n-2k))`，空间 `O(n)`',
        problem=['循环数组 `nums`，下标 `i` 的值 ==严格大于两个相邻元素==（首尾相邻）就是峰值',
                 '每次操作可把某个数 `+1`，求使数组至少有 `k` 个峰值的==最少操作数==，不可能返回 `-1`',
                 '示例：`nums=[2,1,2], k=1` → `1`；`[3,7,3], k=2` → `-1`'],
        quote='普通数组的第一个数和最后一个数不能是峰值。如果 nums[0] 是峰值，那么 nums[n-1] 不能是峰值，可以放在普通数组的最左边……',
        quote_src='—— 灵茶山艾府题解',
        idea=['环形数组至多 `n // 2` 个峰值；已有 `≥ k` 个直接返回 0',
              '断开环：`nums[0]` 是峰值 → `[nums[-1]] + nums`；否则 → `nums + [nums[0]]`，取两者最小',
              '普通数组上「选或不选」：选 `a[i]` 当峰值则 `a[i-1]` 不能选，类似打家劫舍 II，代价 `ops`'],
        summary=['时间 `O(k(n-2k))`，空间 `O(n)`；先判 `k > n//2` 和已有峰值，剪枝很关键',
                 '易错：环形下标要取模；选了 `a[i]` 就要从 `i-2` 转移',
                 '前两种写法：记忆化搜索 `dfs(left, i)`、二维 `f[left][i]` 递推；本版是滚动数组，从 `f0/f1` 保存旧值',
                 '前置题：213. 打家劫舍 II'],
    ),
)

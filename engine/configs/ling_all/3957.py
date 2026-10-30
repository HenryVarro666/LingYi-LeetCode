def _f_vals(S):
    I = S.get('_inner', {})
    f = I.get('f')
    return None if f is None else [x[0] for x in f]


def _f_cnt(S):
    I = S.get('_inner', {})
    f = I.get('f')
    return None if f is None else [-x[1] for x in f]


def _txt(S):
    I = S.get('_inner', {})
    if 'k' in I and 'res' in I and I.get('_inner_fn') != 'x':
        pass
    if 'k' in I:
        return f"惩罚 `k = {I['k']}`：每选一个子数组，元素和先减去 {I['k']}；`f[i]` = 前 i 个数里的最大值，`cnt` = 此时选的个数"
    if 'left' in S:
        return f"二分惩罚值：开区间 `({S['left']}, {S['right']})`，`ans` = {S.get('ans')}；目标 `cnt ≤ m = {S['m']}`"
    return '`m` 个子数组太难直接算；没有 m 限制的 DP 很容易，用惩罚值 `k` 来「调控」选的个数'


CONFIG = dict(
    num=3957, title='M 个非重叠子数组最大和 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='WQS 二分（拉格朗日松弛）+ 单调队列优化 DP',
    tags=['动态规划', '难度分 2611'],
    code='''
max = lambda a, b: b if b > a else a  # 手写 max 更快
class Solution:
    def maximumSum(self, nums: list[int], m: int, l: int, r: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))  # nums 的前缀和
        # 没有 m 约束，但每选一个子数组就要把元素和减少 k
        def dp_without_limit(k: int) -> tuple[int, int]:
            f = [(0, 0)] * (n + 1)  # (DP 值, 子数组个数)，其中子数组个数取反，方便比大小
            q = deque()
            res = (-inf, 0)
            for i in range(l, n + 1):
                # 1. 入
                j = i - l
                v = (f[j][0] - s[j], f[j][1])
                while q and (f[q[-1]][0] - s[q[-1]], f[q[-1]][1]) <= v:
                    q.pop()
                q.append(j)
                # 2. 更新答案
                j = q[0]
                choose = (f[j][0] - s[j] + s[i] - k, f[j][1] - 1)  # 注意子数组个数取反了，加一变成减一
                # choose 保证我们至少选了一个子数组
                res = max(res, choose)  # DP 值相等时，子数组个数小的更优
                # 更新 DP
                f[i] = max(f[i - 1], choose)
                # 3. 出，下一轮循环队首离开窗口
                if j <= i - r:
                    q.popleft()
            return res[0], -res[1]
        res, cnt = dp_without_limit(0)
        if cnt <= m:  # 直接满足题目要求
            return res
        # 现在专注于解决「选恰好 m 个子数组」的问题
        ans = 0
        pos_sum = sum(x for x in nums if x > 0)  # nums 中的正数之和
        left, right = 0, pos_sum + 1
        while left + 1 < right:
            k = (left + right) // 2
            res, cnt = dp_without_limit(k)
            if cnt <= m:
                ans = res + m * k  # 见题解【细节 1】
                right = k
            else:
                left = k
        return ans
''',
    call='Solution().maximumSum([2, -1, 3, -1, 2], 2, 1, 2)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=80),
        dict(type='array', var=_f_vals, label='f[i]：扣掉惩罚后的最大值', h=150, cell=80, pointers={'i': 'pink'}),
        dict(type='array', var=_f_cnt, label='cnt[i]：f[i] 对应选了几个', h=150, cell=80),
        dict(type='queue', var=lambda S: S.get('_inner', {}).get('q'), label='q（单调队列，存下标 j）', h=110),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=['m', ('k', 'k', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('ans', 'ans', 'green'), 'cnt'],
    skip=['n = len', 's = list', 'f = [(0, 0)]', 'q = deque()', 'res = (-inf', 'j = i - l', 'v = (f[j]',
          'while q and', 'q.pop()', 'q.append', 'j = q[0]', 'res = max(res', 'choose = (', 'if j <= i - r', 'q.popleft', 'for i in range(l', 'pos_sum = sum', 'ans = 0', 'return res[0]'],
    captions={
        'res, cnt = dp_without_limit(0)': '先不加惩罚（`k = 0`）跑一遍没有 m 约束的 DP，看最优解会选几个子数组',
        'left, right = 0': '开区间二分惩罚值：`k` 越大，选得越少。`left = 0`（已知不行），`right = 正数之和 + 1 = {right}`',
        'k = (left + right) // 2': '试 `k = {k}`：每个子数组的收益先减去 {k}',
        'res, cnt = dp_without_limit(k)': '带惩罚 `k = {k}` 跑一遍 DP：逐个右端点算 `f[i]`，同时记录选了几个',
        'if cnt <= m': lambda S, B, r: (f'`cnt = {S.cnt}` > `m = {S.m}`：选多了 → 必须「恰好选 m 个」，用 WQS 二分调惩罚 k' if 'left' not in S and S.cnt > S.m
                                        else f'`cnt = {S.cnt}` ≤ `m = {S.m}`' if 'left' in S and S.cnt <= S.m
                                        else f'`cnt = {S.cnt}` > `m = {S.m}`：还是选多了，惩罚不够大' if 'left' in S
                                        else f'`cnt = {S.cnt}` ≤ `m = {S.m}`：没超过 m，直接返回'),
        'ans = res + m * k': '`cnt ≤ m`：这个 `k` 够大了，更新答案 `ans = res + m·k = {res} + {m}×{k}` = =={ans}==（把 m 个 k 加回来）',
        'right = k': '惩罚够大 → 往小试，`right = {right}`',
        'left = k': '惩罚太小，选多了 → 往大试，`left = {left}`',
        'return ans': '二分结束，答案 = =={ret}==',
        'f[i] = max(f[i - 1], choose)': '右端点 `{i}`：选一个以它结尾的子数组 → 值 `{choose[0]}`（已减 k），选了 `{-choose[1]}` 个；不选则沿用 `f[{i-1}] = {f[i-1][0]}`。取大者（并列取个数少的）→ `f[{i}]` = =={f[i][0]}==，此时共选 `{-f[i][1]}` 个',
        'for i in range(l, n + 1)': '枚举子数组右端点 `i`（前缀长度）',
    },
    cards=dict(
        one_liner='恰好选 m 个太难，给每个子数组加惩罚 k，二分 k 来调控个数',
        complexity='时间 `O(n log S)`，空间 `O(n)`',
        problem=['从 `nums` 中选至少 1 个、至多 `m` 个互不重叠的子数组，每个长度在 `[l, r]`',
                 '求所选元素之和的最大值',
                 '本视频：`nums=[2,-1,3,-1,2]`，`m=2`，`l=1`，`r=2` → `5`'],
        quote='每选一个子数组，就把元素和减少 k。k 越大，选的子数组越少；反之越多。这样，我们就能通过二分 k，让选的子数组个数恰好等于 m。',
        quote_src='—— 灵茶山艾府题解（大意）',
        idea=['`f(x)`：恰好选 x 个的最大和是凸函数。没有 m 限制时，用单调队列 `O(n)` 求解',
              '没有 m 限制的 DP 同时记录选了几个（`cnt` 取反方便比大小），并列时选个数少的',
              '先试 `k=0`；个数 > m 就二分 k，`cnt ≤ m` 时记录 `res + m·k`'],
        summary=['时间 `O(n log S)`，`S` 是正数之和；空间 `O(n)`',
                 '易错：并列时 `cnt` 可能 < m，答案仍用 `res + m·k`（细节 1）',
                 '`k` 的二分是开区间 `(0, S+1)`，`k = 0` 已提前检查过',
                 '依赖凸性：这就是 WQS 二分（拉格朗日松弛）的适用条件',
                 '本题至少选一个，若要「至少选 least 个」需允许 k 取负数'],
    ),
)

NUMS = [6, 3, 6, 0, 0, 0]
LINE_PRE = 12  # `pre[x] += 1` 所在行


def _j(S):
    """当前枚举的中间下标 j：pre 里的元素个数（pre[x] += 1 执行后已多一个）"""
    if 'pre' not in S or 'x' not in S:
        return None
    j = sum(S['pre'].values()) - (1 if S['_line'] == LINE_PRE else 0)
    return j if j < len(S['nums']) else None


def _color(S, i, v):
    j = _j(S)
    if j is None:
        return None
    if i == j:
        return 'blue'
    x2 = S['x'] * 2
    if S['_line'] == 11 and v == x2:
        return 'green'
    return 'cyan' if i < j else None


def _formula(S):
    if 'x' not in S or 'ans' not in S:
        return '枚举中间的 `j`：左边选一个 `nums[j]*2`，右边选一个 `nums[j]*2`，==左右互相独立=='
    j = _j(S)
    if j is None:
        return '所有 `j` 都枚举完了，答案累加在 `ans`'
    x2 = S['x'] * 2
    pre = S['pre'].get(x2, 0)
    suf = S['suf'].get(x2, 0)
    if S['_line'] == 11:
        return f'`j = {j}`，`nums[j] = {S["x"]}`：左边 `{pre}` 个 `{x2}` × 右边 `{suf}` 个 `{x2}` = =={pre * suf}=='
    return f'`j = {j}`，`nums[j] = {S["x"]}`，要找的数是 `nums[j] * 2 = {x2}`'


CONFIG = dict(
    num=3583, title='统计特殊三元组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间 · 前后缀计数 + 乘法原理',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1510'],
    code='''
class Solution:
    def specialTriplets(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        suf = Counter(nums)

        ans = 0
        pre = defaultdict(int)  # 比 Counter 快
        for x in nums:  # x = nums[j]
            suf[x] -= 1  # 撤销
            # 现在 pre 中的是 [0,j-1]，suf 中的是 [j+1,n-1]
            ans += pre[x * 2] * suf[x * 2]
            pre[x] += 1
        return ans % MOD
''',
    call=f'Solution().specialTriplets({NUMS})',
    expect=2,
    skip=['MOD = '],
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='nums', label='nums（蓝 = 中间 j，青 = 左边 [0,j-1]，绿 = 左右两边等于 nums[j]*2 的数）', cell=96,
             pointers={_j: 'blue'}, pointer_labels={_j: 'j'}, color=_color, h=230),
        dict(type='map', var=lambda S: {k: v for k, v in S['pre'].items() if v} if 'pre' in S else None,
             label='pre：[0, j-1] 里每个数出现几次', fmt=lambda k, v: f'{k}: {v}', h=120, font=30),
        dict(type='map', var='suf', label='suf：[j+1, n-1] 里每个数出现几次（先统计全部，再逐个撤销）',
             fmt=lambda k, v: f'{k}: {v}', h=120, font=30),
    ],
    watch=['x', ('x * 2', 'x * 2', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'suf = Counter(nums)': '`suf` 先统计整个数组每个数的次数：`{dict(suf)}`',
        'ans = 0': '`ans` 累加每个 `j` 对应的三元组个数',
        'pre = defaultdict': '`pre` 记录 `j` 左边每个数的次数，一开始是空的',
        'for x in nums': lambda S, B, ret: ('枚举完毕，所有中间下标 `j` 都算过了' if _j(S) is None
                                            else f'枚举中间的 `j = {_j(S)}`：`x = nums[j] = {S.x}`'),
        'suf[x] -= 1': '==撤销==：把 `nums[j]` 自己从 `suf` 里去掉，`suf[{x}]` → {suf[x]}。现在 `suf` 就是 `[j+1,n-1]` 的次数',
        'ans += pre[x * 2] * suf[x * 2]': ('要找 `nums[j]*2 = {x*2}`：左边 `pre[{x*2}] = {pre[x*2]}` 个，右边 `suf[{x*2}] = {suf[x*2]}` 个；'
                                           '左右各选一个 → 乘法原理 `+{pre[x*2]*suf[x*2]}`，`ans` = {ans}'),
        'pre[x] += 1': '`nums[j]` 处理完，归入左边：`pre[{x}]` → {pre[x]}，下一轮它就是 `[0,j-1]` 的一员',
        'return ans % MOD': '`ans = {ans}` 不超过 10^15，不会溢出，==只在最后取模==，返回 `{ans % 1000000007}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='三个下标先枚举中间的 j，左右两边互相独立，次数相乘',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums`，数三元组 `(i, j, k)`：`i < j < k`，且 `nums[i] = nums[k] = nums[j] * 2`',
                 '答案对 `10^9 + 7` 取模',
                 '示例：`[8,4,2,8,4]` → `2`',
                 '本视频：`[6,3,6,0,0,0]` → `2`（含 `0` 的特殊情况）'],
        quote='三变量问题，一般==枚举中间的变量==最简单。枚举 j，那么 i 和 k 自动被 j 隔开，互相独立，后续计算中无需关心 i 和 k 的位置关系。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `j`：左边 `nums[j]*2` 的次数 × 右边 `nums[j]*2` 的次数，就是以 `j` 为中间的三元组个数',
              '右边的次数：先统计整个数组，遍历到 `j` 时==撤销== `nums[j]`，剩下的就是 `[j+1,n-1]`',
              '左边的次数：一边遍历一边累加到 `pre`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`nums[j] = 0` 时 `nums[j]*2` 也是 0：先撤销 `suf[x]` 再算，才不会把 `j` 自己数进右边',
                 '答案不超过 `n * 10^5 * 10^5 ≤ 10^15`，Python 里只在返回时取模即可',
                 '另一种写法（枚举右，维护左）：一次遍历维护 `cnt1`、`cnt12` 两个哈希表，思路相同',
                 '同类题：2874、2552；套路见题单「枚举中间」'],
    ),
)

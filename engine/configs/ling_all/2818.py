def _om(x):
    c, d = 0, 2
    while d * d <= x:
        if x % d == 0:
            c += 1
            while x % d == 0:
                x //= d
        d += 1
    return c + (1 if x > 1 else 0)


def _info(S):
    if 'tot' in S:
        return f"当前取 `{S['v']}`：能当质数分数最高者的子数组有 `tot = {S['tot']}` 个，剩余操作次数 `k = {S['k']}`"
    if 'left' in S and S.get('_line', 0) <= 17:
        return '单调栈：栈内质数分数从底到顶不增；遇到分数更高的数就把栈顶的 right 定下来'
    return ''


CONFIG = dict(
    num=2818, title='操作使得分最大', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调栈贡献法 + 贪心 + 快速幂',
    tags=['灵神题单', '单调栈', '难度分 2397'],
    setup='''
MOD = 10 ** 9 + 7
MX = 10 ** 5 + 1
omega = [0] * MX
for i in range(2, MX):  # 预处理 omega
    if omega[i] == 0:  # i 是质数
        for j in range(i, MX, i):
            omega[j] += 1  # i 是 j 的一个质因子
''',
    code='''
class Solution:
    def maximumScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        left = [-1] * n  # 质数分数 >= omega[nums[i]] 的左侧最近元素下标
        right = [n] * n  # 质数分数 >  omega[nums[i]] 的右侧最近元素下标
        st = []
        for i, v in enumerate(nums):
            while st and omega[nums[st[-1]]] < omega[v]:
                right[st.pop()] = i
            if st: left[i] = st[-1]
            st.append(i)

        ans = 1
        for i, v, l, r in sorted(zip(range(n), nums, left, right), key=lambda z: -z[1]):
            tot = (i - l) * (r - i)
            if tot >= k:
                ans = ans * pow(v, k, MOD) % MOD
                break
            ans = ans * pow(v, tot, MOD) % MOD
            k -= tot  # 更新剩余操作次数
        return ans
''',
    call='Solution().maximumScore([19, 12, 14, 6, 10, 18], 3)',
    expect=4788,
    skip=['n = len(nums)', 'left = [-1]', 'right = [n]', 'st = []'],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, cell=90, h=170,
             color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='array', var=lambda S: [_om(v) for v in S['nums']], label='omega[nums[i]]：质数分数', cell=64, h=110, index=False),
        dict(type='stack', var='st', label='st（下标，底→顶）', h=110, font=26),
        dict(type='array', var='left', label='left：左边分数 >= 的最近下标', cell=70, h=100, index=False),
        dict(type='array', var='right', label='right：右边分数 > 的最近下标', cell=70, h=100, index=False),
        dict(type='text', fn=_info, size=22, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('v', 'v', 'yellow'), ('k', 'k', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'while st and omega[nums[st[-1]]] < omega[v]': lambda S, B, r: (
            f'栈顶 `{S.nums[S.st[-1]]}` 的分数 `{_om(S.nums[S.st[-1]])}` < 当前 `{_om(S.v)}`：右边第一个更高分的就是 `i = {S.i}` → 定下它的 `right`'
            if S.st and _om(S.nums[S.st[-1]]) < _om(S.v)
            else '栈空或栈顶分数不低于当前：不弹，栈顶就是当前数的左边界'),
        'right[st.pop()] = i': '弹出的这个数，右边第一个分数更高的就是 `i = {i}` → 它的 `right` = `{i}`',
        'if st: left[i] = st[-1]': lambda S, B, r: (f'栈顶 `{S.st[-1]}` 分数 ≥ 当前（含等于，保证取下标最小）→ `left[{S.i}] = {S.st[-1]}`' if S.st else '栈空：左边没有分数 ≥ 它的，`left` 保持 `-1`'),
        'st.append(i)': '`{i}` 入栈',
        'ans = 1': '初始分数 `ans = 1`；接下来按数值从大到小，看每个数能用几次',
        'for i, v, l, r in sorted': '取下一个最大的数：`nums[{i}] = {v}`，`left = {l}`，`right = {r}`',
        'tot = ': '子数组左端点 `({l}, {i}]`，右端点 `[{i}, {r})` → `tot = ({i} − {l}) × ({r} − {i})` = =={tot}==',
        'if tot >= k': lambda S, B, r: (f'`tot = {S.tot} ≥ k = {S.k}`：次数够了，只用 `k` 次' if S.tot >= S.k else f'`tot = {S.tot} < k = {S.k}`：次数用不完，全用上再看下一个数'),
        'ans = ans * pow(v, k, MOD) % MOD': '最后 `k` 次都乘 `{v}`：`ans × {v}^{k}` = =={ans}==',
        'ans = ans * pow(v, tot, MOD) % MOD': '乘上 `{v}^{tot}`（快速幂）→ `ans` = =={ans}==',
        'k -= tot': '用掉 `tot` 次，剩余 `k` → =={k}==',
        'return ans': '最大分数 =={ret}==',
    },
    cards=dict(
        one_liner='先数每个数能当几次「分数最高者」，再从大到小贪心',
        complexity='时间 `O(n log n)`，空间 `O(n)`（预处理 omega 另计）',
        problem=['每次选一个没选过的子数组，分数乘以其中「质数分数」最高的数（并列取下标最小）',
                 '质数分数 = 不同质因子的个数；至多操作 `k` 次，求最大分数 mod `10^9+7`',
                 '示例：`[19,12,14,6,10,18]`，`k = 3` → `4788`'],
        quote='请注意，我们不能在 i 左侧包含质数分数和 omega[nums[i]] 一样的数，否则不满足题目「如果多个元素质数分数相同且最高，选择下标最小的一个」的要求。所以对于左侧用【大于等于】。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums[i]` 作为分数最高者的子数组：左端点在 `(left, i]`，右端点在 `[i, right)`',
              '左边用 `>=`、右边用 `>`：并列时只算最左的那个',
              '数值大的优先用，每个数最多用 `tot` 次，快速幂 `pow(v, 次数, MOD)`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：左 `>=`、右 `>` 不能写反；`tot >= k` 时要 `break`',
                 '为了演示，质数分数表 `omega` 的预处理放在代码之外先运行（筛法，原文为模块级代码）',
                 '前置：贡献法 + 单调栈（907 题）'],
    ),
)

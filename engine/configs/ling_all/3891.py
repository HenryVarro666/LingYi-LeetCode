def _color(S, k, v):
    n = len(S['nums'])
    if not 0 < k < n - 1:
        return None
    ln = S.get('_line', 0)
    i = S.get('i', 0)
    if 'pre' not in S:
        return 'pink' if k % 2 == 0 and 'suf' in S else None
    if ln <= 15:
        return None
    if ln == 16:
        return 'blue' if k % 2 == 1 and k <= i else ('pink' if k % 2 == 0 and k >= i + 1 else None)
    return 'blue' if k % 2 == 1 and k <= i else ('pink' if k % 2 == 0 and k >= i + 3 else None)


def _cost(S, i):
    n = len(S['nums'])
    if not 0 < i < n - 1:
        return 0
    a = S['nums']
    return max(max(a[i - 1], a[i + 1]) - a[i] + 1, 0)


def _fml(S):
    if 'ans' not in S:
        return '特殊下标：比左右邻居都大。`cost(i) = max(max(左, 右) − nums[i] + 1, 0)`'
    return f"`pre` = ==${S['pre']}== 奇数下标（前缀）　`suf` = =={S['suf']}== 偶数下标（后缀）　`ans` = =={S['ans']}==".replace('$', '') if 'pre' in S else f"`suf` = =={S['suf']}==（偶数下标总代价）"


CONFIG = dict(
    num=3891, title='最大化特殊下标数目的最少增加次数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 间隔选下标',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1953'],
    code='''
class Solution:
    def minIncrease(self, nums: List[int]) -> int:
        n = len(nums)
        suf = 0
        for i in range(n - 2, 0, -2):
            suf += max(max(nums[i - 1], nums[i + 1]) - nums[i] + 1, 0)

        if n % 2 > 0:
            # 修改所有奇数下标
            return suf

        ans = suf  # 修改 [2,n-2] 中的所有偶数下标
        pre = 0
        # 枚举修改 [1,i] 中的奇数下标，以及 [i+3,n-2] 中的偶数下标
        for i in range(1, n - 1, 2):
            pre += max(max(nums[i - 1], nums[i + 1]) - nums[i] + 1, 0)
            suf -= max(max(nums[i], nums[i + 2]) - nums[i + 1] + 1, 0)  # 撤销 i+1，撤销后 suf 对应 [i+3,n-2]
            ans = min(ans, pre + suf)

        return ans
''',
    call='Solution().minIncrease([4, 6, 5, 2, 5, 5])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 前缀 pre 改奇数，粉 = 后缀 suf 改偶数）', h=240, cell=90, pointers={'i': 'blue'},
             color=_color),
        dict(type='text', h=80, size=26, fn=lambda S: (
            f"`pre` = =={S['pre']}==　`suf` = =={S['suf']}==　`pre + suf` = =={S['pre'] + S['suf']}==" if 'pre' in S and 'suf' in S
            else (f"`suf` = =={S['suf']}==（[2,n-2] 偶数下标的总代价）" if 'suf' in S else '特殊下标要比左右邻居都大；增大 `nums[i]` 到 `max(左, 右) + 1`'))),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'pre', 'cyan'), ('suf', 'suf', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`：偶数。特殊下标不能在两端、不能相邻，最多 `n/2 - 1` 个',
        'suf = 0': '`suf`：后缀里「修改偶数下标」的总操作数',
        'for i in range(n - 2': lambda S, B, r: (f'倒着枚举偶数下标 `i = {S.i}`' if S.get('i') != B.get('i') else '偶数下标都累加完了'),
        'suf += max': '增大 `nums[{i}]` 到 `max({nums[i-1]}, {nums[i+1]}) + 1`，代价 `{max(max(nums[i-1], nums[i+1]) - nums[i] + 1, 0)}` → `suf = {suf}`',
        'if n % 2 > 0': 'n 为奇数：特殊下标只能是所有奇数下标，`suf` 就是答案；这里 n 是偶数，继续',
        'ans = suf': '先假设修改 `[2, n-2]` 中所有偶数下标：`ans = {ans}`',
        'pre = 0': '`pre`：前缀里「修改奇数下标」的总操作数',
        'for i in range(1, n - 1, 2)': lambda S, B, r: (f'枚举分界：前缀改奇数下标 `[1..{S.i}]`，后缀改偶数下标 `[{S.i + 3}..n-2]`' if S.get('i') != B.get('i') else '所有分界都枚举完了'),
        'pre += max': '把奇数下标 `{i}` 加入前缀：代价 `{max(max(nums[i-1], nums[i+1]) - nums[i] + 1, 0)}` → `pre = {pre}`',
        'suf -= max': '偶数下标 `{i+1}` 不再属于后缀（挨着前缀，会冲突）→ 撤销它的代价，`suf = {suf}`，对应 `[{i+3}, n-2]`',
        'ans = min': '`ans = min({B.ans}, pre + suf = {pre} + {suf})` = =={ans}==',
        'return ans': '最少操作数 =={ret}==',
    },
    cards=dict(
        one_liner='特殊下标要间隔选：前面改奇数、后面改偶数，枚举分界线',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums[i]` 比左右邻居都大，下标 `i` 就是特殊的（不含两端）',
                 '每次操作可以让某个数 +1',
                 '先最大化特殊下标数，再最小化操作数，求最小操作数',
                 '示例：`[2,1,1,3]` → `2`'],
        quote='如果 n 是偶数，那么枚举修改 [1,i] 中的奇数下标，以及 [i+3,n-2] 中的偶数下标。',
        quote_src='—— 灵茶山艾府题解',
        idea=['修改 `nums[i]` 的代价：`max(max(左, 右) − nums[i] + 1, 0)`',
              'n 为奇数：只能改全部奇数下标；n 为偶数：多出一个空位，前缀改奇数、后缀改偶数',
              '后缀代价倒着算（类似后缀和），枚举分界时用 `suf -= ...` 撤销'],
        summary=['时间 `O(n)`；优化前用 `suf` 数组（空间 `O(n)`），优化后只留一个变量',
                 '易错：代价要和 0 取最大，已经是特殊下标时不用改',
                 '易错：撤销的是偶数下标 `i+1`，剩下的才是 `[i+3, n-2]`',
                 '这是前后缀分解 + 枚举分界线；也可以用状态机 DP 一次遍历'],
    ),
)

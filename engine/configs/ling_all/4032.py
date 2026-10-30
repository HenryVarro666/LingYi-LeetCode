def _pf(x):
    r, p = [], 2
    while p * p <= x:
        if x % p == 0:
            r.append(p)
            while x % p == 0:
                x //= p
        p += 1
    if x > 1:
        r.append(x)
    return r


def _win_r(S):
    return S.get('i')


def _txt(S):
    if 'i' not in S:
        return '预处理：`prime_factors[x]` = x 的所有质因子（埃氏筛，代码从略）'
    x = S['nums'][S['i']]
    s = f"`nums[{S['i']}] = {x}` 的质因子 {{{', '.join(map(str, _pf(x)))}}}"
    return s + f"；窗口内不同质因子 `len(cnt) = {len(S['cnt'])}`，上限 `k = {S['k']}`"


SETUP = '''
MX = 100_001
prime_factors = [[] for _ in range(MX)]
for i in range(2, MX):
    if not prime_factors[i]:  # i 是质数
        for j in range(i, MX, i):  # i 的倍数 j 有质因子 i
            prime_factors[j].append(i)
'''

CONFIG = dict(
    num=4032, title='至多 K 个不同质因数集合的最长子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='不定长滑动窗口 · 质因子计数',
    tags=['滑动窗口与双指针', '数学算法', '难度分 1759'],
    setup=SETUP,
    code='''
class Solution:
    def longestSubarray(self, nums: list[int], k: int) -> int:
        cnt = defaultdict(int)
        ans = left = 0
        for i, x in enumerate(nums):
            for p in prime_factors[x]:
                cnt[p] += 1
            while len(cnt) > k:
                for p in prime_factors[nums[left]]:
                    if cnt[p] > 1:
                        cnt[p] -= 1
                    else:
                        del cnt[p]  # 保证 len(cnt) 是窗口内的不同质因子个数
                left += 1
            ans = max(ans, i - left + 1)
        return ans
''',
    call='Solution().longestSubarray([7,6,10,12,11], 3)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, i]）', pointers={'left': 'pink', 'i': 'blue'},
             window=('left', _win_r), h=240, cell=96),
        dict(type='map', var='cnt', label='cnt：质因子 → 次数（键数 = 不同质因子数）', fmt=lambda k, v: f"{k}: {v}", h=150, font=30),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('left', 'left', 'pink'), ('len(cnt)', 'len(cnt)', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt` 统计窗口里每个质因子的出现次数，==键的个数就是不同质因子数==',
        'cnt[p] += 1': '`{x}` 含质因子 `{p}`，窗口里 `{p}` 的次数 → {cnt[p]}',
        'while len(cnt) > k': '`len(cnt) = {len(cnt)}`，`k = {k}`：{"不同质因子太多，窗口太长 → 收缩左端点" if len(cnt) > k else "没超过 k，窗口合法"}',
        'if cnt[p] > 1': '`{p}` 在窗口里有 `{cnt[p]}` 次：{"还有别的数含它，只减一次" if cnt[p] > 1 else "只剩这一次，要彻底删掉"}',
        'cnt[p] -= 1': '次数减一：`cnt[{p}]` = {cnt[p]}',
        'del cnt[p]': '`{p}` 不再出现，删键 → `len(cnt)` 才是真实的不同质因子数',
        'left += 1': '左端点右移：`left` → {left}',
        'ans = max': '窗口 `[{left}, {i}]` 合法，长度 `{i - left + 1}`，`ans = max({B.ans}, {i - left + 1}) = {ans}`',
        'return ans': '最长合法子数组长度 `{ans}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='越短越合法：右端点右移，不合法就收缩左端点',
        complexity='时间 `O(n log U)`，空间 `O(k)`（不计预处理）',
        problem=['给整数数组 `nums` 和整数 `k`，一个子数组的“质因数集合”是所有元素质因子的并集',
                 '求最长的子数组，使其质因数集合大小不超过 `k`',
                 '本视频：`[7,6,10,12,11]`，`k=3` → `3`（子数组 `[6,10,12]` 的质因子是 `{2,3,5}`）'],
        quote='子数组越短，越能满足要求；子数组越长，越不能满足要求。有这样的性质，可以用滑动窗口解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['质因子提前用埃氏筛预处理：枚举质数 `i`，把 `i` 追加到它所有倍数的列表里',
              '哈希表 `cnt` 记窗口里每个质因子的次数，`len(cnt)` 就是不同质因子个数',
              '出窗口时次数为 1 的要 `del`，保证键数没有“僵尸”键'],
        summary=['时间 `O(n log U)`，空间 `O(k)`，预处理不计入',
                 '视频里预处理在 `setup` 中执行，未单独演示；代码就是题解里的埃氏筛',
                 '易错：次数减到 0 必须 `del`，不能留 0，否则 `len(cnt)` 偏大',
                 '同类：不同数/不同字母个数不超过 k 的滑动窗口'],
    ),
)

def _h(v):
    return f'#{v % 1000:03d}'


CONFIG = dict(
    num=4033, title='有效 K 个不同元素子数组 I', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='异或哈希 + 两次滑窗（在线）',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·常用数据结构', '难度分 2314'],
    setup='''
import random
from random import randrange
random.seed(0)
''',
    code='''
class Solution:
    def validSubarrays(self, nums: list[int], k: int, queries: list[list[int]]) -> list[bool]:
        n = len(nums)
        s = [0] * (n + 1)
        # 把 nums[i] 映射成随机数
        # 不要在 [0, 2**L) 内随机，见 https://codeforces.com/blog/entry/153335
        mp = defaultdict(lambda: randrange(10 ** 18))
        for i, x in enumerate(nums):
            s[i + 1] = s[i] ^ mp[x]

        def calc_left(k: int) -> list[int]:
            lefts = [0] * n
            cnt = defaultdict(int)
            l = 0
            for i, x in enumerate(nums):
                cnt[x] += 1
                while len(cnt) >= k:
                    v = nums[l]
                    if cnt[v] > 1:
                        cnt[v] -= 1
                    else:
                        del cnt[v]  # 保证 len(cnt) 是窗口内的不同元素个数
                    l += 1
                lefts[i] = l
            return lefts

        l1 = calc_left(k + 1)
        l2 = calc_left(k)

        return [s[r + 1] == s[l] and l1[r] <= l < l2[r] for l, r in queries]
''',
    call='Solution().validSubarrays([1,2,2,1,3], 2, [[0,3],[1,2],[0,4],[0,1]])',
    expect=[True, False, False, False],
    views=[
        dict(type='array', var='nums', h=250, label='nums（蓝框 = 滑窗 [l, i]）',
             pointers={'l': 'blue', 'i': 'pink'}, window=('l', 'i'),
             color=lambda S, i, v: 'pink' if 'i' in S and 'lefts' in S and i == S['i'] else None),
        dict(type='array', var='lefts', h=170, label='lefts[i]：窗口内元素种类 < 参数 k 的最小左端点'),
        dict(type='map', var='cnt', h=120, label='cnt：窗口内每个数的出现次数', fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var='mp', h=120, label='mp：每个数映射到的随机数（只显示末三位）', fmt=lambda k, v: f'{k} → {_h(v)}'),
        dict(type='text', fn=lambda S: (f"`l1 = {S['l1']}`（>= k+1 种），`l2 = {S['l2']}`（>= k 种）" if 'l2' in S else f"`l1 = {S['l1']}`" if 'l1' in S else '')),
    ],
    skip=['n = len(nums)', 'cnt[v] -= 1', 'l += 1', 'cnt = defaultdict(int)', 'lefts = [0] * n'],
    max_steps=48,
    watch=['n', ('k', 'k', 'yellow'), ('l', 'l', 'blue'), ('i', 'i', 'pink'), ('l1', 'l1', 'cyan'), ('l2', 'l2', 'green')],
    captions={
        's = [0] * (n + 1)': '`s` 是随机数的前缀异或和：`s[i+1] = s[i] ^ ...`',
        'mp = defaultdict': '每个新数第一次出现时分配一个随机大整数；同一个数异或两次抵消',
        's[i + 1] = s[i] ^ mp[x]': '`s[{i+1}]` = `s[{i}]` 异或 `mp[{x}]`：子数组 `[l, r]` 的异或和就是 `s[r+1] ^ s[l]`',
        'lefts = [0] * n': '`lefts[i]`：右端点为 `i` 时，窗口内 ==种类数 < k== 的最小左端点',
        'cnt = defaultdict(int)': '`cnt` 记录窗口里每个数出现几次',
        'cnt[x] += 1': '右端点 `i = {i}` 把 `{x}` 放进窗口：`cnt[{x}] = {cnt[x]}`',
        'while len(cnt) >= k': lambda S, B, r: (
            f'窗口里有 `{len(S.cnt)}` 种数 >= `{S.k}`，种类太多 → 缩小左端' if len(S.cnt) >= S.k else f'窗口里只有 `{len(S.cnt)}` 种 < `{S.k}` → 不用再缩'),
        'v = nums[l]': '要移出左端 `nums[{l}] = {v}`（`l` 随后右移）',
        'if cnt[v] > 1': lambda S, B, r: (f'`cnt[{S.v}] = {S.cnt[S.v]} > 1`：还有别的 `{S.v}` 留在窗口里，种类不变' if S.cnt[S.v] > 1 else f'`cnt[{S.v}] = 1`：它是最后一个，移走后种类会减少'),
        'cnt[v] -= 1': '次数减一：`cnt[{v}] = {cnt[v]}`',
        'del cnt[v]': '次数为 1 → 直接删键，这样 `len(cnt)` 才是窗口的不同元素个数',
        'l += 1': '左端点右移：`l = {l}`',
        'lefts[i] = l': '右端点 `{i}` 时，让种类数 `< k` 的最小左端点是 `{l}`：左端点 `>= {l}` 的子数组种类都 < k',
        'return lefts': '返回 `lefts = {lefts}`',
        'l1 = calc_left(k + 1)': '先算 `l1`（参数 `k+1`）：`l1[r]` 之后的左端点，子数组种类数 `<= k`',
        'l2 = calc_left(k)': '再算 `l2`（参数 `k`）：`l2[r]` 之后种类数 `<= k-1`；所以 `[l1[r], l2[r])` 内恰好 k 种',
        'return [s[r + 1]': '逐个询问：异或和相等（偶数次）并且 `l1[r] <= l < l2[r]`（恰好 k 种）→ `{ret}`',
    },
    cards=dict(
        one_liner='异或哈希判偶数次，滑窗判恰好 k 种',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['给数组 `nums`、整数 `k` 和若干区间询问 `[l, r]`',
                 '区间有效：恰好 `k` 种不同数字，且每个数出现次数都是偶数',
                 '示例：`[1,2,2,1], k=2`，查询 `[0,3]` 有效，`[0,1]` 无效'],
        quote='本题实际上是两个独立的问题：如何判断子数组每个数的频率都是偶数？如何判断子数组恰好有 k 个不同元素？',
        quote_src='—— 灵茶山艾府题解',
        idea=['频率全为偶数：给每个数随机映射一个大整数，同一个数异或偶数次为 0 → ==子数组异或和为 0==（异或哈希，前缀异或 `s`）',
              '恰好 k 种：对每个右端点 `r`，用滑窗求出左端点范围 `[l1[r], l2[r])`',
              '`l1` 来自「种类 < k+1」，`l2` 来自「种类 < k」，询问只需判断 `l` 落在区间里'],
        after=[dict(heading='另一种写法：树状数组（离线）', lines=[
            '把询问按右端点分组，从左到右扫描',
            '每个数只在「最近一次出现」处记 1，区间和就是不同元素个数',
            '这样 `k` 可以每个询问都不同；时间 `O(n + q log n)`'])],
        summary=['时间 `O(n + q)`，滑窗内层 `l` 总共只右移 n 次',
                 '异或哈希有极小概率误判（q=10^5 时约 5.4e-15）',
                 '演示用固定随机种子 `random.seed(0)`，`randrange` 在 `setup` 里导入',
                 '`lefts` 用「种类 < k」定义，所以 `l1`（k+1）≤ `l2`（k）',
                 '题解还给了树状数组离线做法，可处理每个询问不同的 k'],
    ),
)

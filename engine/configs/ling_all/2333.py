CONFIG = dict(
    num=2333, title='最小差值平方和', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='差值排序，从大往下削平', tags=['灵神题单', '难度分 2011'],
    code='''
class Solution:
    def minSumSquareDiff(self, a: List[int], nums2: List[int], k1: int, k2: int) -> int:
        ans, k = 0, k1 + k2
        for i in range(len(a)):
            a[i] = abs(a[i] - nums2[i])
            ans += a[i] * a[i]
        if sum(a) <= k:
            return 0  # 所有 a[i] 均可为 0

        a.sort(reverse=True)
        a.append(0)  # 哨兵
        for i, v in enumerate(a):
            ans -= v * v  # 撤销上面的 ans += a[i] * a[i]
            j = i + 1
            c = j * (v - a[j])
            if c < k:
                k -= c
                continue
            v -= k // j
            return ans + k % j * (v - 1) * (v - 1) + (j - k % j) * v * v
''',
    call='Solution().minSumSquareDiff([11,1,10,5,2], [1,10,3,1,1], 4, 3)',
    expect=138,
    views=[
        dict(type='bars', var='a', label='a[i] = |nums1[i] − nums2[i]|', h=420,
             pointers={'i': 'blue'},
             color=lambda S, i, v: 'pink' if 'j' in S and i < S['j'] and i < len(S['a']) - 1 else None),
        dict(type='text', fn=lambda S: (f"前 `j={S['j']}` 个已削平到 `{S['a'][S['j']]}`；剩余操作 `k` = =={S['k']}==，削到下一级需 `c` = {S['c']}" if 'c' in S else f"剩余操作 `k` = =={S['k']}=="), size=30),
    ],
    skip=['ans += a[i] * a[i]'],
    watch=['k', ('ans', 'ans', 'green'), ('i', 'i if "i" in dir() else None', 'blue'), ('j', 'j if "j" in dir() else None', 'pink')],
    captions={
        'ans, k = 0': '`nums1` 加 1 等价于 `nums2` 减 1，所以操作合并：`k = k1 + k2 = {k}`',
        'a[i] = abs': '`a[{i}]` = `|nums1 − nums2|` = =={a[i]}==，同时累加它的平方到 `ans`',
        'if sum(a) <= k': '`sum(a) = {sum(a)}` 与 `k = {k}` 比：{"全都能削成 0，返回 0" if sum(a) <= k else "削不完，继续"}',
        'a.sort': '从大到小排序：大的先减，平方和降得最多：`a = {a}`',
        'a.append(0)': '末尾放个哨兵 0，这样 `a[i+1]` 不会越界',
        'ans -= v * v': '先撤销 `a[{i}]={v}` 的平方：`ans` → {ans}',
        'j = i + 1': '前 `j={j}` 个数现在都等于 `{v}`',
        'c = j * (v - a[j])': '把前 `{j}` 个都削到 `{a[j]}` 需要 `c = {j}×({v}−{a[j]}) = {c}`',
        'if c < k': '`c = {c}` 对 `k = {k}`：{"够，整体削平" if c < k else "不够，只能把 k 平分后结束"}',
        'k -= c': '用掉 `c`，剩余 `k` → =={k}==',
        'v -= k // j': '剩下 `k={k}` 平分给 `{j}` 个数：每个再减 `k//j = {k//j}`，`v` → {v}',
        'return ans': '其中 `k%j = {k%j}` 个数再多减 1（值 `v−1`），其余 `{j-k%j}` 个是 `v`：=={ret}==',
    },
    cards=dict(
        one_liner='把最大的差值一层层削平，平方和降得最快',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['两个数组，`nums1` 最多改 `k1` 次，`nums2` 最多改 `k2` 次，每次 ±1',
                 '求修改后 `(nums1[i]-nums2[i])^2` 之和的最小值',
                 '示例：`[1,4,10,12],[5,8,6,9],k1=1,k2=1` → `43`'],
        quote='在 nums1[i] 上 +1，等价于在 nums2[i] 上 -1，反之亦然。……对于 a 中的两个数，先把大的 -1 会更优。',
        quote_src='—— 灵茶山艾府题解',
        idea=['令 `a[i] = |nums1[i]-nums2[i]|`，`k = k1+k2`，问题变成：==a 做至多 k 次 -1，平方和最小==',
              '大的先减：从大到小排序，一层层把前面的数削到 `a[i+1]`',
              '需要 `c=(i+1)(a[i]-a[i+1])` 次；`c>=k` 时，k 平分给前 `i+1` 个，余数个多减 1'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：`k` 可达 `1e9`，不能逐次模拟，要按「整层」削平',
                 '易错：`sum(a) <= k` 时直接返回 0',
                 '末尾加哨兵 0，避免 `a[i+1]` 越界；`k % j` 个数多减 1'],
    ),
)

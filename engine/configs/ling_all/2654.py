CONFIG = dict(
    num=2654, title='使数组所有元素变成 1 的最少操作次数', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='最短 GCD 为 1 的子数组 + 1 向两边扩散',
    tags=['GCD', '难度分 1929'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        if gcd(*nums) > 1:
            return -1
        n = len(nums)
        cnt1 = nums.count(1)
        if cnt1:
            return n - cnt1

        min_size = n
        for i in range(n):
            g = 0
            for j in range(i, n):
                g = gcd(g, nums[j])
                if g == 1:
                    # 这里本来是 j-i+1，把 +1 提出来合并到 return 中
                    min_size = min(min_size, j - i)
                    break
        return min_size + n - 1
''',
    call='Solution().minOperations([2,6,3,4])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'), h=230,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', fn=lambda S: (
            f"窗口 `[{S['i']}..{S['j']}]` 的 GCD = ==`{S['g']}`==" + ('，长度 ' + str(S['j'] - S['i'] + 1) if S['g'] == 1 else '')
            if 'j' in S and 'g' in S and S['j'] >= S['i'] and S.get('_line', 0) >= 14 else
            ('有 1 就能向两边「感染」：答案 `n − cnt1`；没有 1，先造出一个 1' if 'cnt1' in S else ''))),
    ],
    watch=[('n', 'n', 'blue'), ('cnt1', 'cnt1', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'pink'),
           ('g', 'g', 'orange'), ('min_size', 'min_size', 'green')],
    captions={
        'if gcd(*nums) > 1': lambda S, B, r: (f'整个数组的 GCD 是 `{gcd(*S.nums)}`' +
            ('，大于 1 → ==无论怎么操作都得不到 1==，返回 -1' if gcd(*S.nums) > 1 else '，等于 1 → 一定能变成全 1，继续')),
        'n = len': '`n = {n}`',
        'cnt1 = nums': '数组里已有的 1：`cnt1 = {cnt1}`',
        'if cnt1': lambda S, B, r: ('已经有 1：从 1 向左右不断替换，每个非 1 的数各花 1 次，共 `n - cnt1` 次' if S.cnt1
                                    else '没有 1：要先花若干次操作，在某个子数组里造出一个 1'),
        'min_size = n': '`min_size`：GCD 为 1 的最短子数组长度（实际存 `长度-1`），先设成 `n`',
        'for i in range': '枚举子数组左端点 `i = {i}`',
        'g = 0': '`g` 从 0 开始，`gcd(0, x) = x`',
        'for j in range': '右端点 `j = {j}`',
        'g = gcd(g, nums[j])': '`gcd({B.g}, {nums[j]})` → 子数组 `[{i}..{j}]` 的 GCD = ==`{g}`==',
        'if g == 1': lambda S, B, r: (f'`g = {S.g}` ==等于 1== → 子数组 `[{S.i}..{S.j}]` 可以操作 `{S.j - S.i}` 次造出 1' if S.g == 1
                                      else f'`g = {S.g}` > 1，右端点继续右移'),
        'min_size = min': '`min_size = min({B.min_size}, {j} - {i})` = =={min_size}==（这里存的是 长度 − 1）',
        'break': '以 `i` 为左端点，再往右只会更长，不用看了',
        'return min_size': '`min_size + n − 1` = `{min_size} + {n} − 1` = =={ret}==：造 1 花 `{min_size}` 次，再扩散 `{n - 1}` 次',
        'return n - cnt1': '`n − cnt1` = `{n} − {cnt1}` = =={ret}==',
        'return -1': '无解，返回 -1',
    },
    cards=dict(
        one_liner='先造出一个 1，再让它感染整个数组',
        complexity='时间 `O(n(n+log U))`，空间 `O(1)`',
        problem=['每次选相邻两数，把其中一个换成它们的 GCD，问最少几次让==全部变成 1==，不行返回 -1',
                 '示例：`[2,6,3,4]` → `4`，`[2,10,6,14]` → `-1`'],
        quote='如果 nums 中有 1，那么从 1 向左向右不断替换就能把所有数变成 1。……如果没有 1，想办法花费尽量少的操作得出一个 1。找到最短的 GCD 为 1 的子数组，设其长度为 minSize，最终答案为 minSize + n - 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['整体 GCD > 1 → 无解；有 `cnt1` 个 1 → 每个非 1 的数各 1 次，答案 `n − cnt1`',
              '没有 1：1 一定来自某个连续子数组的 GCD，找最短的，造 1 花 `长度 − 1` 次',
              '再扩散 `n − 1` 次，合计 `minSize + n − 2`；代码把 `+1` 合并进 return'],
        summary=['时间 `O(n(n + log U))`，`n ≤ 50`',
                 '==三种情况顺序==：整体 GCD > 1 → -1；有 1 → `n - cnt1`；否则枚举',
                 '易错：`min_size` 存的是 `j - i`（长度 − 1），return 里是 `+ n - 1`',
                 '另一种写法：用 LogTrick 按 GCD 分组，可做到 `O(n log U)`'],
    ),
)

CONFIG = dict(
    num=2179, title='统计数组中好三元组数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='置换 + 枚举中间 + 值域树状数组',
    tags=['树状数组', '难度分 2272'],
    code='''
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.tree[i]
            i &= i - 1
        return res

class Solution:
    def goodTriplets(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        p = [0] * n
        for i, x in enumerate(nums1):
            p[x] = i

        ans = 0
        t = FenwickTree(n)
        for i, y in enumerate(nums2):
            y = p[y]
            less = t.pre(y)
            ans += less * (n - 1 - y - (i - less))
            t.update(y + 1, 1)
        return ans
''',
    call='Solution().goodTriplets([2,0,1,3], [0,1,2,3])',
    expect=1,
    views=[
        dict(type='array', var='nums1', label='nums1（置换后会变成 0,1,2,…）', h=150),
        dict(type='array', var='nums2', label='nums2', color=lambda S, i, v: 'blue' if i == (S.get('i') if S.get('_line', 0) >= 28 else (S['nums2'].index(S['p'].index(S['y'])) if 'y' in S else -1)) else None, h=150),
        dict(type='array', var='p', label='p[x] = x 在 nums1 中的位置（置换后的新名字）', h=170),
        dict(type='array', var='t.tree', label='树状数组 tree（下标 1..n，记录已出现的 y+1）',
             color=lambda S, i, v: 'yellow' if S.get('_line') in (9, 17) and i == S.get('i') else None, h=150),
        dict(type='text', fn=lambda S: (f"y = ==p[...]== = {S['y']}，左边比它小的 less = =={S['less']}==，右边比它大 = `{S['n']-1-S['y']-(S['i']-S['less'])}`，贡献 `{S['less']*(S['n']-1-S['y']-(S['i']-S['less']))}`" if S.get('_line') in (33, 34) else '【数 nums2 里的递增三元组：枚举中间数 y】'), h=70),
    ],
    watch=['i', 'y', 'less', ('ans', 'ans', 'green')],
    captions={
        'p[x] = i': '`p[{x}] = {i}`：值 {x} 在 nums1 里排第 {i} 位，==把 nums1 重命名成 0,1,2…==',
        'y = p[y]': '`nums2[{i}]` 的新名字：`y = p[..] = {y}`，换名后位置不变，公共子序列个数不变',
        'less = t.pre': '`less = t.pre({y})`：前面已出现的数里比 `{y}` 小的有 =={less}== 个',
        'ans += less': '中间是 `{y}`：左边 `{less}` 个比它小，右边比它大的有 `{n-1-y}-({i}-{less})` = `{n-1-y-(i-less)}` 个 → 乘法原理，`ans` = =={ans}==',
        't.update(y + 1, 1)': '把 `{y}` 记入树状数组（值域下标要 +1），之后的数就能查到它了',
        'self.tree = [0]': '树状数组，下标 1..n，初始全 0',
        'self.tree[i] += val': '`tree[{i}]` 加 `{val}`，这个格子管着一段区间',
        'i += i & -i': '`i += i & -i` → {i}：跳到下一个会管到当前位置的格子',
        'res += self.tree[i]': '累加 `tree[{i}]`，`res` = {res}',
        'i &= i - 1': '`i &= i - 1` → {i}：去掉最低位的 1，继续向左拼前缀和',
        'return res': '前缀和 = `{res}`',
        'return ans': '好三元组一共 `{ans}` 个',
    },
    skip=['self.tree = [0]', 'def ', 'while i < len', 'while i > 0', 'res = 0'],
    max_steps=90,
    cards=dict(
        one_liner='重命名 nums1 为 0..n-1，只数 nums2 里的递增三元组',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums1`、`nums2` 都是 `0..n-1` 的排列',
                 '好三元组：三个不同的值，在两个数组里出现顺序都一致',
                 '示例：`[2,0,1,3]` 与 `[0,1,2,3]` → `1`（只有 (0,1,3)）'],
        quote='置换不是排序，是映射（可以理解成重命名），原来的公共子序列在映射后，子序列元素的位置没变，只是数值变了，仍然是公共子序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 nums1 里的值按位置重命名成 `0,1,2…`，nums1 自然递增',
              '于是只看 nums2：数长为 3 的严格递增子序列，枚举中间数 `y`',
              '`less` 用值域树状数组查，右边更大的数由总数 `n-1-y` 减去左边更大的得到'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：树状数组下标从 1 开始，所以查 `pre(y)`（即 < y 的个数）、更新 `y+1`',
                 '右侧更大 = `n-1-y-(i-less)`：全局更大的减去左侧更大的',
                 '另一种写法：用 SortedList 的 `bisect_left` 代替树状数组（本视频未演示）',
                 '进阶：把 3 改成 k，需要做 k 层 DP 套树状数组'],
    ),
)

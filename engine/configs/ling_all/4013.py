CONFIG = dict(
    num=4013, title='按奇偶比统计子数组 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 值域树状数组',
    tags=['树状数组', '难度分 2156'],
    code='''
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 1
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def add(self, i: int) -> None:
        t = self.tree
        while i < len(t):
            t[i] += 1
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        t = self.tree
        res = 0
        while i > 0:
            res += t[i]
            i &= i - 1
        return res

class Solution:
    def countRatioSubarrays(self, nums: list[int], a: int, b: int) -> int:
        s = [0] * (len(nums) + 1)
        for i, x in enumerate(nums):
            s[i + 1] = s[i] + (a if x % 2 else -b)  # 奇数视作 a，偶数视作 -b

        # s 去重排序
        sorted_s = sorted(set(s))

        t = FenwickTree(len(sorted_s) + 1)
        ans = 0
        for x in s:
            x = bisect_left(sorted_s, x) + 1  # 离散化（从 1 开始）
            ans += t.pre(x)  # 计算在 s 左边有多少个 <= s 的数
            t.add(x)
        return ans
''',
    call='Solution().countRatioSubarrays([1,2,1], 3, 2)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（奇数 → +a，偶数 → -b）', h=120),
        dict(type='array', var='s', label='前缀和 s（要数 L<R 且 s[L] <= s[R]）', h=140),
        dict(type='array', var='sorted_s', label='sorted_s：去重排序（离散化，名次从 1 开始）', h=130),
        dict(type='array', var='t.tree', label='树状数组 tree：记录已出现的前缀和名次',
             color=lambda S, i, v: 'yellow' if S.get('_line', 0) >= 9 and S.get('_line', 0) <= 23 and i == S.get('_inner', {}).get('i') else None, h=140),
        dict(type='text', fn=lambda S: ('树状数组：add 沿 `i += i & -i` 向上更新，pre 沿 `i &= i - 1` 向左拼前缀和' if S.get('_line', 0) <= 23 and S.get('_line', 0) >= 9 else '【枚举右端点 R，数左边有多少个 s[L] <= s[R]】'), h=60),
    ],
    watch=['x', 'ans'],
    captions={
        's[i + 1] = s[i]': '`s[{i + 1}] = {s[i + 1]}`：`nums[{i}]` = {x}，{"奇数" if x % 2 else "偶数"} → 加 `{a if x % 2 else -b}`',
        'sorted_s = sorted': '前缀和去重排序：`sorted_s = {sorted_s}`，只保留相对大小',
        't = FenwickTree': '建值域树状数组，下标 1..len(sorted_s)',
        'x = bisect_left': lambda S, B, r: f"`s[R]` = {B.x} 的名次：`bisect_left + 1` = =={S.x}==",
        'ans += t.pre': lambda S, B, r: f"查名次 ≤ {B.x} 的个数，即左边有多少个 `s[L] <= s[R]`，每个 L 对应一个有效子数组",
        't.add(x)': lambda S, B, r: f"累加得 `ans` = =={B.ans}==；再把名次 {B.x} 记入树状数组，供后面的 R 查询",
        'self.tree = [0]': '树状数组，初始全 0',
        't[i] += 1': '`tree[{i}]` 加 1',
        'i += i & -i': '`i += i & -i` → {i}：跳到下一个会管到当前位置的格子',
        'res += t[i]': '累加 `tree[{i}]`，`res` = {res}',
        'i &= i - 1': '`i &= i - 1` → {i}：去掉最低位的 1，继续向左拼前缀和',
        'return res': '前缀和 = `{res}`',
        'return ans': '有效子数组共 `{ans}` 个',
    },
    skip=['for i, x in enumerate', 'for x in s', 'self.tree = [0]', 'def ', 'while i < len', 'while i > 0', 'res = 0', 't = self.tree', 'ans = 0'],
    max_steps=110,
    cards=dict(
        one_liner='奇数记 a，偶数记 -b：求和 >= 0 的子数组个数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums`，整数 `a`、`b`；子数组偶数个数 x，奇数个数 y',
                 '有效子数组：`y > 0` 且 `x / y <= a / b`，数有多少个',
                 '示例：`[1,2,1,2]`，`a=3, b=2` → `7`'],
        quote='x/y <= a/b 等价于 ay-bx >= 0 ……把 nums 中的奇数视作 a，偶数视作 -b ……类似逆序对，这可以用值域树状数组或归并排序计算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x/y <= a/b` 通分成 `ay - bx >= 0`；`y = 0` 时必为负，两个条件合并成一个',
              '奇数 → `a`，偶数 → `-b`，问题变成：元素和 >= 0 的子数组有多少个',
              '前缀和 `s[R] - s[L] >= 0`，枚举 R，数左边有多少个 `s[L] <= s[R]`，用值域树状数组'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`s` 要包含开头的 0；树状数组下标从 1 开始，所以名次要 `+1`',
                 '先查询（`pre`）再插入（`add`），保证 L < R',
                 '另有两种写法：SortedList 和归并排序，本视频演示树状数组',
                 '同类题：逆序对、315. 计算右侧小于当前元素的个数'],
    ),
)

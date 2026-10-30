CONFIG = dict(
    num=2426, title='满足不等式的数对数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='式子变形 + 离散化树状数组',
    tags=['树状数组', '难度分 2030'],
    code='''
class Solution:
    def numberOfPairs(self, a: List[int], nums2: List[int], diff: int) -> int:
        for i, x in enumerate(nums2):
            a[i] -= x
        b = sorted(set(a))  # 配合下面的二分，离散化

        ans = 0
        t = BIT(len(b) + 1)
        for x in a:
            ans += t.query(bisect_right(b, x + diff))
            t.add(bisect_left(b, x) + 1)
        return ans

class BIT:
    def __init__(self, n):
        self.tree = [0] * n

    def add(self, x):
        while x < len(self.tree):
            self.tree[x] += 1
            x += x & -x

    def query(self, x):
        res = 0
        while x > 0:
            res += self.tree[x]
            x &= x - 1
        return res
''',
    call='Solution().numberOfPairs([3,2,5,4], [2,2,1,3], 1)',
    expect=5,
    views=[
        dict(type='array', var='a', label='a[i] = nums1[i] - nums2[i]（要数 a[i] <= a[j] + diff，i < j）',
             h=150),
        dict(type='array', var='b', label='b = sorted(set(a))：离散化（树状数组下标 = 名次）', h=140),
        dict(type='array', var='t.tree', label='树状数组 tree（下标 1..len(b)，记录已出现的 a 值）',
             color=lambda S, i, v: 'yellow' if S.get('_line', 0) >= 17 and i == S.get('_inner', {}).get('x') else None, h=150),
        dict(type='text', fn=lambda S: (f"当前 `a[j]` = {S['x']}，`a[i] <= {S['x']} + diff` 的上限 = =={S['x'] + S['diff']}==；ans = {S['ans']}" if 9 <= S.get('_line', 0) <= 12 and 'x' in S and 'ans' in S and 'diff' in S else ('树状数组：add 沿 `x += x & -x` 向上更新，query 沿 `x &= x - 1` 向左拼前缀和' if S.get('_line', 0) > 12 else '【把 i<j 的二元条件变成「左边有多少个 <= 某个数」】')), h=70),
    ],
    watch=['x', 'ans'],
    captions={
        'a[i] -= x': '`a[{i}] = nums1[{i}] - nums2[{i}] = {a[i]}`：把下标相同的两项合并成一个数',
        'b = sorted': '去重排序得 `b = {b}`：只保留相对大小，值域再大也不怕',
        't = BIT': '建树状数组，大小 `len(b) + 1`，下标从 1 开始',
        'ans += t.query': lambda S, B, r: f"当前 `a[j] = {B.x}`：查前面有多少个 `a[i] <= {B.x} + {B.diff}`，即名次 ≤ {__import__('bisect').bisect_right(B.b, B.x + B.diff)} 的个数",
        't.add(bisect_left': lambda S, B, r: f"查到的累加进答案，`ans` = =={B.ans}==；再把 `{B.x}` 记入树状数组（名次 {__import__('bisect').bisect_left(B.b, B.x) + 1}），之后的 j 就能查到它",
        'ans = 0': '`ans` 累计满足条件的数对个数',
        'self.tree = [0]': '树状数组，初始全 0',
        'self.tree[x] += 1': '`tree[{x}]` 加 1：这个格子管着一段区间',
        'x += x & -x': '`x += x & -x` → {x}：跳到下一个会管到当前位置的格子',
        'res += self.tree[x]': '累加 `tree[{x}]`，`res` = {res}',
        'x &= x - 1': '`x &= x - 1` → {x}：去掉最低位的 1，继续向左拼前缀和',
        'return res': '前缀和 = `{res}`',
        'return ans': '满足条件的数对共 `{ans}` 对',
    },
    skip=['for i, x in enumerate', 'for x in a', 'self.tree = [0]', 'def ', 'while x < len', 'while x > 0', 'res = 0'],
    max_steps=110,
    cards=dict(
        one_liner='移项合并下标：a[i] <= a[j] + diff，变成逆序对类计数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两个数组 `nums1`、`nums2` 和整数 `diff`',
                 '数 `i < j` 且 `nums1[i]-nums1[j] <= nums2[i]-nums2[j]+diff` 的数对',
                 '示例：`[3,2,5]`、`[2,2,1]`、`diff=1` → `3`'],
        quote='本题用到的技巧是，合并下标相同的元素。……下面代码用的离散化树状数组，即使元素范围达到 10^9 也适用。',
        quote_src='—— 灵茶山艾府题解',
        idea=['式子移项：`nums1[i]-nums2[i] <= nums1[j]-nums2[j]+diff`，记 `a[i]` 为左边',
              '于是变成 `a[i] <= a[j] + diff`，和「逆序对」「右侧小于当前元素的个数」同一类',
              '枚举 j，用值域树状数组查左边有多少个 `a[i] <= a[j]+diff`，再把 `a[j]` 加进去'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：树状数组下标从 1 开始，查询用 `bisect_right`（含等于），更新用 `bisect_left + 1`',
                 '先查询、后插入，保证只数到 i < j 的数对',
                 '代码直接把 `nums1` 原地改成 `a`（参数名就叫 a）',
                 '另一种做法：归并排序（见 yiduobo 版）'],
    ),
)

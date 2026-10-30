def _wl(S):
    if 'l' not in S or 'r' not in S or S['l'] > S['r']:
        return None
    return S['l'] - 1


def _wr(S):
    if 'l' not in S or 'r' not in S or S['l'] > S['r']:
        return None
    return S['r'] - 1


def _txt(S):
    if 'v' not in S or 'ans' not in S:
        return '遥远 = 总数 − 不遥远；不遥远 ⇔ `v−goal−k < s[i] < v−goal+k`'
    return (f"`v = {S['v']}`：要数 `{S['v'] - S['goal'] - S['k']} < s[i] < {S['v'] - S['goal'] + S['k']}` 的前缀和个数，"
            f"当前 `ans = {S['ans']}`")


CONFIG = dict(
    num=4051, title='统计遥远子数组的数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 · 离散化 + 值域树状数组',
    tags=['常用数据结构', '前缀和', '难度分 2140'],
    code='''
# 模板来源 https://leetcode.cn/discuss/post/3583665/
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        t = self.tree
        while i < len(t):
            t[i] += val
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

    # 计算区间和 a[l] + ... + a[r]
    # 1 <= l <= r <= n
    # 时间复杂度 O(log n)
    def query(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return self.pre(r) - self.pre(l - 1)

class Solution:
    def distantSubarrays(self, nums: list[int], goal: int, k: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        sorted_s = sorted(set(s))

        ans = n * (n + 1) // 2
        t = FenwickTree(len(sorted_s))
        for v in s:
            # 离散化后的值加一，方便使用树状数组
            l = bisect_right(sorted_s, v - goal - k) + 1
            r = bisect_left(sorted_s, v - goal + k)
            ans -= t.query(l, r)
            t.update(bisect_left(sorted_s, v) + 1, 1)
        return ans
''',
    call='Solution().distantSubarrays([-3,1,2], 0, 3)',
    expect=2,
    views=[
        dict(type='array', var='s', label='s：前缀和（逐个当右端点 v）', cell=84, h=140),
        dict(type='array', var='sorted_s', label='sorted_s：离散化（框 = 满足条件的前缀和）', cell=84, h=190,
             window=(_wl, _wr)),
        dict(type='array', var='t.tree', label='t.tree：值域树状数组，下标 = 离散化位置 + 1（t[0] 不用）', cell=84, h=170),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    watch=[('v', 'v', 'blue'), ('l', 'l', 'cyan'), ('r', 'r', 'pink'), ('ans', 'ans', 'green')],
    skip=['self.tree = ', 't = self.tree', 'return self.pre(r)', 'while i < len(t)', 'while i > 0', 'res = 0', 'for v in s'],
    captions={
        'n = len': '`n = {n}`，数组长度',
        's = list(accumulate': '前缀和 `s = {s}`：子数组 `[i,j)` 的和 = `s[j] − s[i]`',
        'sorted_s = ': '去重排序，得到离散化用的 `sorted_s = {sorted_s}`',
        'ans = n * (n + 1)': '先假设全都遥远：总子数组数 `n(n+1)/2` = =={ans}==，再减去不遥远的',
        't = FenwickTree': '建一棵管 `{len(sorted_s)}` 个位置的值域树状数组，记录「见过的前缀和」',
        'l = bisect_right': '取 `v = {v}`。`s[i]` 要 `> v−goal−k = {v - goal - k}`：二分找第一个大于它的位置，+1 成树状数组下标 → `l = {l}`',
        'r = bisect_left': '`s[i]` 要 `< v−goal+k = {v - goal + k}`：第一个 ≥ 它的位置（下标从 1 起正好是最后一个小于它的）→ `r = {r}`',
        'ans -= t.query': '树状数组 `[{l}, {r}]` 内见过的前缀和有 `{t.query(l, r)}` 个，即以 `v` 结尾的 ==不遥远== 子数组 → `ans = {ans} − {t.query(l, r)}`',
        't.update(bisect_left': '把当前 `v = {v}` 登记进树状数组：下标 `{bisect_left(sorted_s, v) + 1}` 加 1',
        'if l > r': '`l > r` 说明范围为空，没有不遥远的',
        'return self.pre(r) - self.pre(l - 1)': '区间和 = `pre(r) − pre(l−1)`',
        'res += t[i]': '累加 `t[{i}]` = {t[i]}，`res` = {res}',
        'i &= i - 1': '去掉最低位的 1，跳到前面一段：`i` = {i}',
        'i += i & -i': '加上最低位，跳到父节点：`i` = {i}',
        't[i] += val': '`t[{i}] += 1`：这个节点管的区间包含当前前缀和',
        'return res': '`pre` 返回前缀和 `{res}`',
        'return ans': '遥远子数组共 `{ans}` 个',
    },
    cards=dict(
        one_liner='正难则反：总数 − 不遥远，不遥远是一个值域区间，用树状数组数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums` 与整数 `goal`、`k`；子数组和与 `goal` 的绝对差 `≥ k` 称为遥远',
                 '数出遥远子数组的个数（元素可为负）',
                 '示例：`nums=[-3,1,2]`，`goal=0`，`k=3` → `2`'],
        quote='用所有子数组个数减去不遥远的子数组个数，即为遥远的子数组个数。……用值域树状数组保存遍历过的 s[i] 的出现次数，即可 O(log n) 计算范围内的 s[i] 的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有负数不能滑窗，改用前缀和：不遥远 ⇔ `goal−k < s[j]−s[i] < goal+k`',
              '枚举 `j`，`s[i]` 落在 `(s[j]−goal−k, s[j]−goal+k)` 内，值域树状数组数个数',
              '前缀和很大，先 `sorted(set(s))` 离散化，两次二分找出区间的两端'],
        after=[dict(heading='另外两种写法', lines=['有序集合：`SortedList` 的 `bisect` 直接数区间内个数', '归并排序：像逆序对一样，用三指针统计满足条件的 `(i, j)`'])],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '开区间要 `bisect_right` / `bisect_left` 配合，易错点是下标 +1',
                 '先 `update` 再查询会把 `i = j` 算进去；这里先查后加',
                 '灵神另有有序集合、归并排序两种写法，本视频用树状数组'],
    ),
)

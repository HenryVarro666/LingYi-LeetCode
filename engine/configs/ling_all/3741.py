CONFIG = dict(
    num=3741, title='三个相等元素之间的最小距离 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='数组记上两次位置', tags=[],
    code='''
class Solution:
    def minimumDistance(self, nums: List[int]) -> int:
        n = len(nums)
        last = [-inf] * (n + 1)
        last2 = [-inf] * (n + 1)

        ans = n
        for i, x in enumerate(nums):
            ans = min(ans, i - last2[x])
            last2[x] = last[x]
            last[x] = i

        return -1 if ans == n else ans * 2
''',
    call='Solution().minimumDistance([1,1,2,3,2,1,2])',
    expect=8,
    views=[
        dict(type='array', var='nums', h=190, pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'x' in S and v == S['x'] and 'i' in S and i <= S['i'] else None),
        dict(type='array', var='last', h=170, label='last[x]：x 上一次出现的位置',
             fmt=lambda v: '-' if v == float('-inf') else str(v)),
        dict(type='array', var='last2', h=170, label='last2[x]：x 上上次出现的位置',
             fmt=lambda v: '-' if v == float('-inf') else str(v)),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'cyan'), ('ans', 'ans', 'green'), ('n', 'n', 'orange')],
    captions={
        'last = ': '`last[x]`：值 `x` 上一次出现的位置，`nums[i] ≤ n` 所以用数组代替哈希表',
        'last2 = ': '`last2[x]`：值 `x` 上上次出现的位置',
        'ans = n': '`ans = n`：最大可能的 `k−i` 也小于 n，所以 `n` 表示还没找到',
        'ans = min': lambda S, B, r: (f'`x={S.x}` 还没出现两次，`i − last2[x]` 是无穷大 → `ans` 不变 = {S.ans}' if S.last2[S.x] == float('-inf')
                                      else f'最右 `{S.i}`、最左 `{S.last2[S.x]}`：差 `{S.i - S.last2[S.x]}`；`ans = min({B.ans}, {S.i - S.last2[S.x]})` = =={S.ans}=='),
        'last2[x] = last[x]': '上一次变成上上次：`last2[{x}] = {last2[x]}`',
        'last[x] = i': '当前位置成为上一次：`last[{x}] = {i}`',
        'return': lambda S, B, r: f'`ans = {S.ans}` ≠ n：距离 = `{S.ans} × 2` = =={r}==（乘 2 放到最后再算）',
    },
    cards=dict(
        one_liner='距离是 2(k−i)：只看相同元素的连续三个位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找三个值相等的不同下标，距离 `|i−j|+|j−k|+|k−i|` 最小',
                 '没有这样的三元组返回 `-1`',
                 '示例：`[1,1,2,3,2,1,2]` → `8`（下标 2, 4, 6）'],
        quote='|i-j| + |j-k| + |k-i| 的几何意义是这三个下标中的最左最右下标绝对差的两倍。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数轴上三点，来回走一圈 = 最左到最右的距离 ×2',
              '同组元素里，枚举 ==连续三个== 下标 `i<j<k`，距离 `2(k−i)`',
              '优化：值域 `[1,n]` 用数组；只留上一次、上上次；乘 2 放最后'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '优化前：哈希表存每个值的下标列表，再枚举连续三个，同样 `O(n)`',
                 '`last` 初始化为 `-inf`，不足三次时 `i − last2[x]` 自动变大，不会更新答案',
                 '`ans = n` 作未找到的标记；最后才 `× 2`，别忘了'],
    ),
)

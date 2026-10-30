# sortedcontainers 不是标准库：配置加载时先注册一个等价实现，作者代码（含 import 行）一字不改
import sys, types
from bisect import bisect_left as _bl, insort as _ins


class SortedList(list):
    def __init__(self, iterable=()):
        super().__init__(sorted(iterable))

    def add(self, value):
        _ins(self, value)

    def bisect_left(self, value):
        return _bl(self, value)


_m = types.ModuleType('sortedcontainers')
_m.SortedList = SortedList
sys.modules['sortedcontainers'] = _m


def _vi(S):
    return len(S['sl']) - 3 if 'y' in S and 'sl' in S else None

def _yi(S):
    return len(S['sl']) - 3 + S['x'] if 'y' in S and 'sl' in S else None

CONFIG = dict(
    num=2817, title='限制条件下元素之间的最小绝对差', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='有序集合 · 二分找最接近的数',
    tags=[],
    code='''
from sortedcontainers import SortedList

class Solution:
    def minAbsoluteDifference(self, nums: List[int], x: int) -> int:
        ans = inf
        sl = SortedList((-inf, inf))  # 哨兵
        for v, y in zip(nums, nums[x:]):
            sl.add(v)
            j = sl.bisect_left(y)
            ans = min(ans, sl[j] - y, y - sl[j - 1])
        return ans
''',
    call='Solution().minAbsoluteDifference([8, 2, 13, 5, 10, 1], 2)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（粉 = 当前的 y，蓝 = 刚加入有序集合的 v）', cell=84, h=210,
             color=lambda S, i, v: ('blue' if i == _vi(S) else 'pink' if i == _yi(S) else None)),
        dict(type='array', var='sl', label='sl（有序集合，哨兵 ±inf；绿 = y 的左右邻居）', cell=84, h=210,
             index=False,
             color=lambda S, i, v: 'green' if 'j' in S and 'y' in S and S['_line'] >= 9 and i in (S['j'] - 1, S['j']) else None),
        dict(type='text', size=28, fn=lambda S: (f"`y = {S['y']}`：右邻居 `{S['sl'][S['j']]}`，左邻居 `{S['sl'][S['j'] - 1]}`" if 'j' in S and 'y' in S and S['_line'] >= 9 else '')),
    ],
    watch=['x', 'v', 'y', ('j', 'j', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '答案先设为无穷大，后面取最小',
        'sl = SortedList': '有序集合放两个哨兵 `-inf` 和 `inf`，保证二分后左右邻居一定存在',
        'for v, y in zip': lambda S, B, ret: ('所有 `(v, y)` 都配完了，循环结束' if len(S['sl']) - 2 == len(S['nums']) - S['x'] else f"`y = {S['y']}` 是 `nums[i]`，`v = {S['v']}` 是 `nums[i - x]`：恰好隔了 `x = {S['x']}` 个位置"),
        'sl.add': '`v = {v}` 离 `y` 已经至少 `x`，可以配对了，加入有序集合：`sl = {list(sl)}`',
        'j = sl.bisect_left': '二分找第一个 `>= y` 的位置：`j = {j}`，右邻居 `sl[j] = {sl[j]}`，左邻居 `sl[j-1] = {sl[j - 1]}`',
        'ans = min': '最接近 `y` 的只可能是这两个邻居：`min({B.ans}, {sl[j]} - {y}, {y} - {sl[j - 1]})` → `ans = {ans}`',
        'return ans': '所有 `y` 都处理完，最小差 =={ret}==',
    },
    cards=dict(
        one_liner='边走边把「够远」的数放进有序集合，二分找 y 的邻居',
        complexity='时间 `O((n-x) log(n-x))`，空间 `O(n-x)`',
        problem=['找下标距离至少为 `x` 的两个数，使差的绝对值最小',
                 '示例：`nums = [4,3,2,4], x = 2` → `0`',
                 '视频用 `[8,2,13,5,10,1], x = 2` → `1`'],
        quote='sl = SortedList((-inf, inf))  # 哨兵',
        quote_src='—— 灵茶山艾府题解代码注释（原文只有代码，没有文字说明）',
        idea=['枚举右边的 `y`，它能配对的是下标 `<= i - x` 的所有数',
              '这些数用有序集合维护，每步只加一个 `v = nums[i-x]`',
              '`bisect_left(y)` 之后，最接近 `y` 的只在 `sl[j]` 和 `sl[j-1]`'],
        summary=['时间 `O((n-x) log(n-x))`，空间 `O(n-x)`',
                 '易错点：哨兵 `-inf / inf` 不能少，否则 `sl[j]` 或 `sl[j-1]` 会越界',
                 '`zip(nums, nums[x:])` 一起前进，省掉下标运算',
                 '`SortedList` 来自第三方库 `sortedcontainers`，视频里用 `bisect.insort` 做了等价实现'],
    ),
)

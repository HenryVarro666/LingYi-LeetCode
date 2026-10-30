NUMS = [3, 1, 2, 1, 2, 4, 4]
_R = {}
for _i, _x in enumerate(NUMS):
    _R[_x] = _i
_SEG = []
_m = _mr = 0
for _i, _x in enumerate(NUMS):
    _SEG.append(_m)
    _mr = max(_mr, _R[_x])
    if _mr == _i:
        _m += 1


def _col(S, i, v):
    if 'm' not in S or 'i' not in S:
        return None
    if i <= S['i']:
        return 'cyan' if _SEG[i] % 2 == 0 else 'purple'
    return None


def _txt(S):
    if 'm' not in S:
        return '相同数字必须在同一段：先记下每个数最右边的位置 `r`'
    if 'i' not in S:
        return f"段数 `m = {S['m']}`，`max_r = {S['max_r']}`"
    return f"`i = {S['i']}`，这一段目前最远要延伸到 `max_r = {S['max_r']}`，已封口的段数 `m = {S['m']}`"


CONFIG = dict(
    num=2963, title='统计好分割方案的数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='合并区间 + 乘法原理',
    tags=['灵神题单·数学算法', '灵神题单·贪心与思维', '难度分 1985'],
    code='''
class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        r = {}
        for i, x in enumerate(nums):
            r[x] = i
        m = max_r = 0
        for i, x in enumerate(nums):
            max_r = max(max_r, r[x])
            if max_r == i:  # 区间无法延长
                m += 1
        return pow(2, m - 1, 1_000_000_007)
''',
    call='Solution().numberOfGoodPartitions([3,1,2,1,2,4,4])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=30, h=90),
        dict(type='array', var='nums', pointers={'i': 'blue', 'max_r': 'pink'}, color=_col, label='nums（青 / 紫 = 扫过的不可分割段，蓝箭头 = i，粉箭头 = max_r）', h=230),
        dict(type='map', var='r', fmt=lambda k, v: f'{k} → {v}', label='r：每个数最右边的下标', h=240),
    ],
    watch=['i', ('max_r', 'max_r', 'pink'), ('m', 'm', 'green')],
    captions={
        'r[x] = i': '`r[{x}] = {i}`：从左往右覆盖，最后留下的就是 {x} 最右边的下标',
        'm = max_r = 0': '`m` 记录合并后的区间个数，`max_r` 是当前区间必须延伸到的最右下标',
        'max_r = max': '`{x}` 的最右下标是 `r[{x}] = {r[x]}`，当前区间必须盖到它：`max_r = max({B.max_r}, {r[x]}) = {max_r}`',
        'if max_r == i': lambda S, B, ret: (f'`max_r = {S.max_r} == i = {S.i}`：区间到这里就伸不出去了 → ==这里可以切一刀==' if S.max_r == S.i else f'`max_r = {S.max_r} != i = {S.i}`：后面还有同样的数没放进来，不能切'),
        'm += 1': '又得到一个不可分割的区间：`m = {m}`',
        'return pow': '`m = {m}` 个区间，相邻之间 `m-1 = {m - 1}` 个加号选或不选 → `2^{m - 1}` = =={ret}==',
    },
    cards=dict(
        one_liner='把必须在一起的数合并成段，段之间的缝选切或不切',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把数组切成若干连续子数组，要求==任何数字只出现在一个子数组里==',
                 '求好分割方案数，对 `10^9+7` 取模',
                 '示例：`[1,2,1,3]` → `2`；本视频：`[3,1,2,1,2,4,4]` → `4`'],
        quote='所以两个 1 必须在同一个子数组，两个 2 也必须在同一个子数组。把该数组分到无法再分，得到 [3] + [1,2,1,2] + [4,4]，考虑每个 + 号选或不选。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一个数的首尾之间不能切 → 每个数对应一个区间，把重叠区间合并',
              '合并后有 `m` 段，段与段之间的 `m-1` 个位置各自「切 / 不切」→ ==乘法原理 `2^(m-1)`==',
              '写法二只需右端点：遍历时维护 `max_r`，`max_r == i` 就是一段结束'],
        after=[dict(heading='另一种写法', lines=['写法一：记录每个数的首、尾下标，按左端点排序后合并区间', '时间 `O(n log n)`，思路等同 56 题「合并区间」', '写法二不需要排序，一遍扫描就够，所以选它'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '答案是 `2^(m-1)`，不是 `2^m`：最后一段后面没有「加号」',
                 '`max_r == i` 才能封口：此时 i 之前的数在后面都不再出现',
                 '同类题：56 合并区间、55 跳跃游戏、2580 统计将重叠区间合并成组的方案数'],
    ),
)

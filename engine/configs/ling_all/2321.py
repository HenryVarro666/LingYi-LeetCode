A1 = [5, 3, 9, 2, 6]
A2 = [2, 8, 4, 7, 1]


def _ix(S):
    if 'x' not in S or 'nums1' not in S:
        return None
    for i, (a, b) in enumerate(zip(S['nums1'], S['nums2'])):
        if a == S['x'] and b == S['y']:
            return i
    return None


def _diff(S):
    return [b - a for a, b in zip(S['nums1'], S['nums2'])]


def _first(S):
    return S.get('nums1') == A1


def _text(S):
    if 'nums1' not in S:
        return '换一段后总和 = `S1 + diff[left] + … + diff[right]` → 对 `diff` 求最大子数组和'
    who = ('把 nums2 的一段换进 nums1' if S['nums1'] == A1 else '反过来：把 nums1 的一段换进 nums2')
    if 'f' in S and 'max_sum' in S:
        return f'{who}：`f` = =={S["f"]}==，`max_sum` = =={S["max_sum"]}=='
    return who


def _cap_f(S, B, ret):
    d = S.y - S.x
    if B.f > 0:
        return f'`diff = {S.y} − {S.x} = {d}`；上一段 `f = {B.f}` > 0，接着拼更赚 → `f = {S.f}`'
    return f'`diff = {S.y} − {S.x} = {d}`；上一段 `f = {B.f}` ≤ 0 是累赘，丢掉重新开始 → `f = {S.f}`'


def _cap_ms(S, B, ret):
    if S.max_sum > B.max_sum:
        return f'`f = {S.f}` 刷新最大增益：`max_sum` {B.max_sum} → =={S.max_sum}=='
    return f'`f = {S.f}` 没超过 `max_sum = {S.max_sum}`，不更新'


CONFIG = dict(
    num=2321, title='拼接数组的最大分数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='差分数组 + 最大子数组和',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1791'],
    code='''
class Solution:
    def solve(self, nums1: List[int], nums2: List[int]) -> int:
        max_sum = f = 0
        for x, y in zip(nums1, nums2):
            f = max(f, 0) + y - x
            max_sum = max(max_sum, f)
        return sum(nums1) + max_sum

    def maximumsSplicedArray(self, nums1: List[int], nums2: List[int]) -> int:
        return max(self.solve(nums1, nums2), self.solve(nums2, nums1))
''',
    call=f'Solution().maximumsSplicedArray({A1}, {A2})',
    expect=30,
    skip=['max_sum = f = 0'],
    views=[
        dict(type='text', fn=_text, size=26, h=70),
        dict(type='array', var='nums1', label='nums1', cell=96, h=190,
             pointers={_ix: 'blue'}, pointer_labels={_ix: 'x'},
             color=lambda S, i, v: 'blue' if _ix(S) == i else None),
        dict(type='array', var='nums2', label='nums2', cell=96, h=190,
             pointers={_ix: 'pink'}, pointer_labels={_ix: 'y'},
             color=lambda S, i, v: 'pink' if _ix(S) == i else None),
        dict(type='array', var=_diff, label='diff（辅助观察：nums2 − nums1）', cell=96, h=190,
             color=lambda S, i, v: 'green' if v > 0 else 'orange'),
    ],
    watch=['f', ('max_sum', 'max_sum', 'green'), ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'f = max(f, 0) + y - x': _cap_f,
        'max_sum = max(max_sum, f)': _cap_ms,
        'return sum(nums1) + max_sum': '`sum(nums1) + max_sum = {sum(nums1)} + {max_sum}` = =={ret}==（可以一段都不换，所以 max_sum 从 0 起步）',
        'return max(self.solve': '两个方向各算一次：`solve(nums1, nums2)` 和 `solve(nums2, nums1)`，取较大者',
    },
    cards=dict(
        one_liner='换一段 = 给 nums1 的和加上 diff 的一段子数组和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选 `left..right`，交换 `nums1`、`nums2` 对应的子数组（可以不换）',
                 '分数 = `max(sum(nums1), sum(nums2))`，求最大分数',
                 '本视频：`nums1=[5,3,9,2,6]`，`nums2=[2,8,4,7,1]` → `30`'],
        quote='定义 diff[i] = nums2[i]-nums1[i]，上式为 S1 + diff[left] + ... + diff[right]。为了最大化上式，我们需要最大化 diff 数组的最大子数组和。注意子数组可以为空，所以初始化 max_sum = 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['换完以后 `nums1` 的和 = `S1` + 这一段的 `diff` 之和',
              '于是变成 53 题：`f` 表示以当前位置结尾的最大子数组和，`f ≤ 0` 就扔掉重来',
              '对 `nums2` 同理，把参数反过来再算一遍，取较大值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`max_sum` 和 `f` 都从 0 起步：允许==一段都不换==（空子数组）',
                 '最后加的是 `sum(nums1)`（原数组和），不是换完之后的和',
                 '题解另给「手写 max」的写法，思路完全一样',
                 '同类题：53 最大子数组和'],
    ),
)

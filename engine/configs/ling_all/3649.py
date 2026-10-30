CONFIG = dict(
    num=3649, title='完美对的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='按绝对值排序 + 同向双指针',
    tags=['滑动窗口与双指针', '数学算法', '难度分 1716'],
    code='''
class Solution:
    def perfectPairs(self, nums: List[int]) -> int:
        nums.sort(key=abs)
        ans = left = 0
        for j, b in enumerate(nums):
            while abs(nums[left]) * 2 < abs(b):
                left += 1
            # a=nums[i]，其中 i 最小是 left，最大是 j-1，一共有 j-left 个
            ans += j - left
        return ans
''',
    call='Solution().perfectPairs([-3, 2, -1, 4, 7, -6])',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: (f"b = `{S['b']}`：左边 `[{S['left']}, {S['j'] - 1}]` 的数满足 `|a| ≤ |b| ≤ 2|a|`，共 =={S['j'] - S['left']}== 个" if 'j' in S and 'left' in S else '先按绝对值从小到大排序')),
        dict(type='array', var='nums', pointers={'left': 'blue', 'j': 'pink'}, window=('left', 'j'), h=300,
             color=lambda S, i, v: ('pink' if i == S['j'] else 'blue' if i == S['left'] else None) if 'j' in S and 'left' in S else None,
             dim=lambda S, i, v: 'j' in S and 'left' in S and not (S['left'] <= i <= S['j'])),
    ],
    watch=[('left', 'left', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort': '题目的第二个式子恒成立，第一个式子等价于 `|大| ≤ 2|小|`，与位置无关 → ==按绝对值排序==：`{nums}`',
        'ans = left = 0': '`left`：满足 `|b| ≤ 2|a|` 的最小下标 `a`',
        'for j, b': '枚举绝对值较大的 `b = nums[{j}] = {b}`，搭档 `a` 只能在它左边',
        'while abs(nums[left])': lambda S, B, ret: (f'`|nums[left]|×2 = {abs(S.nums[S.left])*2} < |b| = {abs(S.b)}`：`a` 太小，乘 2 也够不到 `b` → `left` 右移' if abs(S.nums[S.left]) * 2 < abs(S.b) else f'`|nums[left]|×2 = {abs(S.nums[S.left])*2} ≥ |b| = {abs(S.b)}`：`left` 这个数合格，停下'),
        'left += 1': '`left` → {left}：`|b|` 只增不减，被扔掉的 `a` 对后面的 `b` 更不可能合格',
        'ans += j - left': '`a` 的下标在 `[{left}, {j-1}]`，共 `{j} - {left}` = =={j-left}== 个 → `ans = {ans}`',
        'return ans': '完美对共 `{ans}` 个',
    },
    cards=dict(
        one_liner='化简成「大的绝对值 ≤ 小的绝对值 × 2」，排序后滑窗数个数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['下标对 `(i, j)`，`i < j`，满足两个绝对值不等式就是「完美对」',
                 '示例：`[0,1,2,3]` → `2`，`[-3,2,-1,4]` → `4`',
                 '本视频：`[-3,2,-1,4,7,-6]` → `8`'],
        quote='相当于绝对值大的那个数，不能超过绝对值小的那个数乘以 2。这与元素位置无关，所以可以排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `a`、`b`、`-b` 画在数轴上：`max(|a-b|,|a+b|) = |a|+|b|`，第二个式子恒成立',
              '`min(|a-b|,|a+b|) = ||a|-|b||`，第一个式子等价于 `|大| ≤ 2|小|`',
              '按绝对值排序，枚举大的 `b`，满足条件的 `a` 是一段连续区间，`left` 只增不减'],
        after=[dict(heading='另一种写法', lines=['先把每个数取绝对值再排序，循环里就不用再写 `abs`'])],
        summary=['时间 `O(n log n)`，瓶颈在排序；双指针本身 `O(n)`',
                 '易错：`<` 才是需要移动 `left` 的条件，`|b| = 2|a|` 仍然合格',
                 '窗口内个数是 `j - left`，不含 `j` 自己',
                 '同类题：2824 统计和小于目标的下标对数目'],
    ),
)

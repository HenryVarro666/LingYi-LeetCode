def _bits(S):
    o = S.get('or_')
    if o is None:
        return ''
    s = f"窗口 or_ = `{o:06b}`（{o}）"
    if 'x' in S and S.get('_line') is not None:
        s += f"　新数 x = `{S['x']:06b}`　`or_ & x` = =={S['or_'] & S['x']}=="
    return s


CONFIG = dict(
    num=2401, title='最长优雅子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='滑动窗口 · 按位或维护集合',
    tags=['位运算', '难度分 1750'],
    code='''
class Solution:
    def longestNiceSubarray(self, nums: List[int]) -> int:
        ans = left = or_ = 0
        for right, x in enumerate(nums):
            while or_ & x:  # 有交集
                or_ ^= nums[left]  # 从 or_ 中去掉集合 nums[left]
                left += 1
            or_ |= x  # 把集合 x 并入 or_ 中（这里 |= 也可以写成 ^=）
            ans = max(ans, right - left + 1)
        return ans
''',
    call='Solution().longestNiceSubarray([1,3,8,48,10])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = left，粉 = right，框 = 优雅窗口）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), h=260, cell=110),
        dict(type='text', h=90, size=30, fn=_bits),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('or_', 'or_', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = left = or_ = 0': '窗口为空：`left = 0`，`or_ = 0`（空集），`ans = 0`',
        'for right, x': '枚举右端点 `right = {right}`，新数 `x = {x}`',
        'while or_ & x': lambda S, B, r: (f'`or_ & x = {S.or_ & S.x}` ≠ 0：x 和窗口里某个数有==公共比特==，不能加入' if S.or_ & S.x
                                          else '`or_ & x = 0`：没有交集，x 可以加入窗口'),
        'or_ ^= nums[left]': '把 `nums[{B.left}] = {nums[B.left]}` 的比特从 `or_` 去掉（窗口里数两两无交集，所以异或等于去掉）→ `or_ = {or_}`',
        'left += 1': '`left` 右移到 {left}，窗口缩小',
        'or_ |= x': '`x` 并入集合：`or_ = {or_}`',
        'ans = max': '窗口长度 `{right} − {left} + 1` = {right - left + 1}，`ans = max({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '最长优雅子数组长度 `{ans}`',
    },
    cards=dict(
        one_liner='每个数看成比特集合，窗口里的集合两两无交集',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子数组中任意两个不同位置的数按位与都为 `0`，称为==优雅==子数组',
                 '求最长优雅子数组的长度，单个元素也算优雅',
                 '示例：`[1,3,8,48,10]` → `3`（`[3,8,48]`）'],
        quote='子数组中任意两个数按位与均为 0，意味着任意两个数对应的集合的交集为空。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把窗口里的数按位或起来，得到并集 `or_`',
              '新数 `x` 与 `or_` 有交集：不断从左边移出元素，直到交集为空',
              '右端点右移，窗口左端点只增不减，所以是线性时间'],
        summary=['时间 `O(n)`：`left` 只增不减，内层循环总共不超过 `n` 次',
                 '窗口内两两无交集，所以移出用 `^=` 就能精确去掉那些比特',
                 '另一种写法：暴力枚举右端点向左扩展，因优雅子数组长度不超过 30，复杂度 `O(n log U)`',
                 '易错：先移出到无交集，再把 `x` 并入，最后才更新答案'],
    ),
)

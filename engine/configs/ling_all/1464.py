CONFIG = dict(
    num=1464, title='数组中两元素的最大乘积', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='枚举右，维护左', tags=[],
    code='''
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        ans = mx = 0
        for x in nums:
            ans = max(ans, (mx - 1) * (x - 1))
            mx = max(mx, x)
        return ans
''',
    call='Solution().maxProduct([3,4,5,2])',
    expect=12,
    views=[
        dict(type='array', var='nums', pointers={}, h=260,
             color=lambda S, i, v: 'blue' if S.get('x') == v and False else None),
        dict(type='text', fn=lambda S: f"枚举右 `x`，左边已看过的最大值 `mx = {S.get('mx')}`，当前最优乘积 ==`{S.get('ans')}`=="),
    ],
    watch=[('x', 'x', 'blue'), ('mx', 'mx', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = mx = 0': '`mx` 维护左边出现过的最大值，`ans` 记录答案，都从 0 开始',
        'for x in nums': '枚举右边的数 `x = {x}`',
        'ans = max': '左边最大 `mx = {mx}`，和 `x = {x}` 配对：`({mx}-1) * ({x}-1) = {(mx-1)*(x-1)}`，`ans = {ans}`',
        'mx = max': '把 `x` 并入左边：`mx = max({B.mx}, {x}) = {mx}`',
        'return': '枚举完所有右端点，答案 =={ret}==',
    },
    cards=dict(
        one_liner='枚举右边的数，用一个变量维护左边的最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选两个 ==不同下标== 的数，求 `(nums[i]-1) * (nums[j]-1)` 的最大值',
                 '示例：`[3,4,5,2]` → `12`'],
        quote='枚举 j，我们需要知道左边 nums[i] 的最大值。这可以用一个变量维护。',
        quote_src='—— 灵茶山艾府题解（方法三：枚举右维护左）',
        idea=['暴力要枚举所有下标对 `(i, j)`，`i < j`',
              '固定右边的 `j`，左边只需要最大的那个数 → 用 `mx` 维护',
              '先配对再更新 `mx`，保证两个数下标不同'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '其他写法：方法一排序取最大两个（`O(n log n)`）；方法二维护最大、次大',
                 '易错点：先用 `mx` 算答案，再 `mx = max(mx, x)`，否则会把同一个数选两次',
                 '数都是正整数，所以最大值配最大值最优；模板见「枚举右，维护左」'],
    ),
)

CONFIG = dict(
    num=3867, title='数对的最大公约数之和', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 手写 gcd + 双指针配对',
    code='''
class Solution(object):
    def gcdSum(self, nums):
        
        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        ma = nums[0]
        pre = [nums[0]]
        for v in nums[1:]:
            ma = max(ma, v)
            pre.append(gcd(ma, v))
        
        pre.sort()
        res = 0
        left, right = 0, len(pre) - 1
        while left < right:
            res += gcd(pre[left], pre[right])
            left += 1
            right -= 1
        
        return res
''',
    call='Solution().gcdSum([3,6,2,8,4,9])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=170, label='nums'),
        dict(type='array', var='pre', pointers={'left': 'blue', 'right': 'pink'}, h=240, label='pre = prefixGcd',
             window=('left', 'right')),
    ],
    skip=['while y > 0', 'x, y = y, x % y', 'return x'],
    watch=[('v', 'v', 'blue'), ('ma', 'ma', 'orange'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'ma = nums[0]': '`ma` 记录前缀最大值，从 `nums[0]` 开始',
        'pre = [nums[0]]': '第 0 个：`gcd(nums[0], nums[0]) = nums[0]`，直接放入 `pre`',
        'ma = max': '先用 `v = {v}` 更新前缀最大值：`ma = {ma}`',
        'pre.append': '`pre` 加入 `gcd({ma}, {v}) = {__import__("math").gcd(ma, v)}`',
        'pre.sort()': '排序：`pre = {pre}`，接着首尾配对',
        'left, right = 0': '左右指针：`left = 0` 指最小，`right = {right}` 指最大',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}` → 还有数对' if S.left < S.right
                                               else f'`left = {S.left} >= right = {S.right}` → 配对结束，剩下的中间元素忽略'),
        'res += gcd': '`gcd({pre[left]}, {pre[right]}) = {__import__("math").gcd(pre[left], pre[right])}`，累加：`res = {B.res + __import__("math").gcd(pre[left], pre[right])}`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'return res': '所有数对的 gcd 之和 `res = {res}`',
    },
    cards=dict(
        one_liner='按描述逐步模拟：前缀 gcd、排序、两端向中间配对',
        complexity='时间 `O(n log U + n log n)`，空间 `O(n)`',
        problem=['`prefixGcd[i] = gcd(nums[i], max(nums[0..i]))`',
                 '排序后最小配最大，重复到不能配为止',
                 '返回每个数对 gcd 之和；n 为奇数时中间元素忽略'],
        quote='题目的描述比较复杂，但是其中并没有过份的要求，只需按照描述逐步模拟就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：`ma` 记前缀最大值，`gcd(ma, v)` 加入 `pre`',
              '排序后用 `left`、`right` 从两侧向中间扫',
              '每轮累加 `gcd(pre[left], pre[right])`，直到 `left >= right`'],
        summary=['时间 `O(n log U + n log n)`，空间 `O(n)`',
                 '`while left < right`：奇数个元素时中间那个不会被配对',
                 '原文自己手写了辗转相除的 `gcd`，没有改动',
                 '对比灵神：灵神用 `range(n // 2)` 一行求和，yiduobo 用双指针循环'],
    ),
)

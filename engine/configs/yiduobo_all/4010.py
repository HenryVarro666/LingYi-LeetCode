CONFIG = dict(
    num=4010, title='数对的最大强度', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='暴力枚举 + 手写辗转相除',
    tags=['灵神题单', '数学算法', '难度分 1216'],
    code='''
class Solution(object):
    def maxPairStrength(self, nums):
        
        res = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                x, y = nums[i], nums[j]
                while y > 0:
                    x, y = y, x % y
                
                res = max(res, nums[i] * nums[j] // x // x)
        
        return res
''',
    call='Solution().maxPairStrength([4,6,8])',
    expect=12,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, h=260),
        dict(type='text', fn=lambda S: (f"辗转相除：`x = {S['x']}`，`y = {S['y']}`" if 'x' in S and 'y' in S else ''), size=34),
    ],
    watch=['i', 'j', 'x', 'y', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录最大强度，初始为 0',
        'for i in range': lambda S, B, r: ('所有下标对都看完了，结束' if 'i' in B and B.i == S.i else f'固定第一个数 `nums[{S.i}]`'),
        'for j in range': lambda S, B, r: ('后面的数选完了，换下一个 `i`' if 'j' in B and B.j == S.j and B.i == S.i else f'再选后面的 `nums[{S.j}]`，每一对只看一次'),
        'x, y = nums[i], nums[j]': '取这一对：`x = {x}`，`y = {y}`，下面用辗转相除求它们的 gcd',
        'while y > 0': lambda S, B, r: (f'`y = {S.y}` > 0，继续' if S.y > 0 else f'`y = 0`：此时 `x = {S.x}` 就是这一对的 ==gcd=='),
        'x, y = y, x % y': '`({B.x}, {B.y})` → `({x}, {y})`',
        'res = max': lambda S, B, r: f'强度 = `{S.nums[S.i]} × {S.nums[S.j]} // {S.x} // {S.x}` = =={S.nums[S.i]*S.nums[S.j]//S.x//S.x}==，`res` = {S.res}',
        'return res': '所有数对里最大的强度 `{res}`',
    },
    cards=dict(
        one_liner='两两枚举，每对用辗转相除求 gcd，再按公式算强度',
        complexity='时间 `O(n² log U)`，空间 `O(1)`',
        problem=['选恰好一对下标，强度 = `nums[i] * nums[j] / gcd²`，求最大强度',
                 '示例：`[4,6,8]` → `12`（6 和 8，`48 / 4`）'],
        quote='按照题目描述两两遍历所有下标对，并计算对应的强度即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组不大，直接双重循环枚举所有下标对',
              '内层 `while y > 0` 手写辗转相除，结束时 `x` 就是 gcd',
              '强度 = 乘积 `// x // x`，用两次整除代替平方'],
        summary=['时间 `O(n² log U)`，空间 `O(1)`',
                 '辗转相除后 `x`、`y` 已被改写，所以乘积要重新用 `nums[i] * nums[j]` 算',
                 '没有剪枝，纯暴力；灵神版本靠排序和全体 GCD 提前跳出',
                 '原文代码已是 Python 3 可运行，未改动'],
    ),
)

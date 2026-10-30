CONFIG = dict(
    num=3289, title='数字小镇中的捣蛋鬼', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='和 + 平方和 · 解方程',
    code='''
class Solution:
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        n = len(nums) - 2
        a = -n * (n - 1) // 2
        b = -n * (n - 1) * (n * 2 - 1) // 6
        for x in nums:
            a += x
            b += x * x
        x = (a - isqrt(b * 2 - a * a)) // 2
        return [x, a - x]
''',
    call='Solution().getSneakyNumbers([0,3,2,1,3,2])',
    expect=[2, 3],
    views=[
        dict(type='array', var='nums', label='nums = [0..n-1] 再多出两个数', h=230,
             color=lambda S, i, v: ('blue' if S['_line'] in (7, 8) and 'x' in S and v == S['x'] else None)),
        dict(type='text', size=30, h=100,
             fn=lambda S: f"`a` = =={S['a']}==，`b` = =={S['b']}==（扫完后 a = x+y，b = x²+y²）" if 'b' in S else ''),
        dict(type='text', size=30, h=100,
             fn=lambda S: f"`a = {S['a']}`，`b = {S['b']}` → `2b − a² = {2*S['b']-S['a']**2}` = `(y−x)²`" if S['_line'] >= 9 and 'b' in S else ''),
    ],
    watch=['n', ('a', 'a', 'blue'), ('b', 'b', 'pink'), ('x', 'x', 'green')],
    captions={
        'n = len(nums) - 2': '多出两个数，所以 `n = len(nums) − 2 = {n}`，原本应是 `0..{n-1}`',
        'a = -n': '先减掉 `0+1+…+(n−1) = n(n−1)/2`，`a` 初始 = `{a}`',
        'b = -n': '再减掉 `0²+1²+…+(n−1)² = (n−1)n(2n−1)/6`，`b` 初始 = `{b}`',
        'a += x': '累加元素：`a` = `{B.a} + {x}` = {a}',
        'b += x * x': '累加平方：`b` = `{B.b} + {x}²` = {b}',
        'x = (a - isqrt': '设两数为 `x<y`：`y−x = √(2b−a²) = {round((b*2-a*a)**0.5)}`，`x = (a − (y−x)) / 2` = =={x}==',
        'return [x, a - x]': '另一个数 `y = a − x = {a - x}` → 答案 =={ret}==',
    },
    cards=dict(
        one_liner='和与平方和两个方程，解出多出来的两个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 本应是 `0..n-1` 各一次，但有两个数多出现了一次',
                 '找出这两个数，顺序任意',
                 '示例：`[0,3,2,1,3,2]` → `[2,3]`'],
        quote='设 nums 的元素和为 s，元素平方之和为 s2，那么有 x+y = s − (0+1+…+n−1) = a，x²+y² = s2 − (0²+1²+…+(n−1)²) = b。',
        quote_src='—— 灵茶山艾府题解（数学做法）',
        idea=['`nums = [0,1,…,n-1,x,y]`，减去标准和，剩下的就是 `x+y`',
              '同理平方和得到 `x²+y²`，联立两式',
              '`(y−x)² = 2b − a²`，开方后 `x = (a − √(2b−a²)) / 2`'],
        after=[dict(heading='另一种写法：位运算', lines=['灵神还给了异或做法：先把 `0..n-1` 和 `nums` 全部异或', '剩下 `x^y`，取最低位把数分两组，每组再异或出一个数', '同样 `O(n)` 时间、`O(1)` 空间，需要遍历两次'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`n = len(nums) − 2`，不是 `len(nums)`',
                 '易错点：用 `isqrt` 保持整数运算，`2b − a²` 一定是完全平方数',
                 '同类题：2965 找出缺失和重复的数字（同一套思路）'],
    ),
)

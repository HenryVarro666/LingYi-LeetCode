def _tri(S):
    n = S['nums']
    if 'a' not in S:
        return '先排序：最长的边一定在最后'
    a, b, c = S['a'], S['b'], S['c']
    return f'`a={a}`  `b={b}`  `c={c}`：较短两边之和 `{a}+{b}={a+b}`，最长边 `{c}`'


CONFIG = dict(
    num=3024, title='三角形类型', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='排序后只判最小两边',
    code='''
class Solution:
    def triangleType(self, nums: List[int]) -> str:
        nums.sort()
        a, b, c = nums
        if a + b <= c:
            return "none"
        if a == c:
            return "equilateral"
        if a == b or b == c:
            return "isosceles"
        return "scalene"
''',
    call='Solution().triangleType([6,4,4])',
    expect='isosceles',
    views=[
        dict(type='array', var='nums', label='nums（排序后 a ≤ b ≤ c）', h=300, cell=120,
             color=lambda S, i, v: (['blue', 'cyan', 'pink'][i] if 'a' in S else None)),
        dict(type='text', fn=_tri, size=34),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'cyan'), ('c', 'c', 'pink')],
    captions={
        'nums.sort()': '排序后 `nums = {nums}`，有 `a ≤ b ≤ c`，判断逻辑可以大大简化',
        'a, b, c = nums': '`a = {a}`，`b = {b}`，`c = {c}`（c 是最长边）',
        'if a + b <= c': lambda S, B, r: (f'`a + b = {S.a + S.b}` ≤ `c = {S.c}`：两短边加起来不够长 → ==无法构成三角形=='
                                          if S.a + S.b <= S.c else
                                          f'`a + b = {S.a + S.b}` > `c = {S.c}`：合法（另两个不等式 a+c>b、b+c>a 排序后自动成立）'),
        'if a == c': lambda S, B, r: (f'`a == c`（{S.a} = {S.c}）：最小等于最大，==三边全相等=='
                                      if S.a == S.c else f'`a ≠ c`（{S.a} ≠ {S.c}）：不是等边'),
        'if a == b or b == c': lambda S, B, r: (f'`a == b` 或 `b == c` 成立 → ==恰好两边相等=='
                                                if (S.a == S.b or S.b == S.c) else '`a ≠ b` 且 `b ≠ c`：三边互不相同'),
        'return "equilateral"': '返回 =="equilateral"==',
        'return "isosceles"': '返回 =="isosceles"==（等腰）',
        'return "scalene"': '其余情况三边互不相等，返回 =="scalene"==',
        'return "none"': '返回 =="none"==',
    },
    cards=dict(
        one_liner='排序之后，只需要比较最小两边之和与最大边',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['长度为 3 的数组 `nums` 是三条边的长度',
                 '不能构成三角形返回 `"none"`；否则按边相等情况返回 `equilateral` / `isosceles` / `scalene`',
                 '示例：`[3,4,5]` → `"scalene"`；本视频：`[6,4,4]` → `"isosceles"`'],
        quote='排序后 a+c > b 和 b+c>a 自动成立（注意数组元素都是正数），所以只需判断 a+b > c 是否成立。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后 `a ≤ b ≤ c`：另外两个不等式自动成立，只判 `a + b > c`',
              '`a == c` 就意味着 `a == b == c`，直接判等边',
              '`a == b` 或 `b == c` 是等腰，其余就是不等边'],
        after=[dict(heading='另一种写法：哈希集合', lines=['合法的前提下，`len(set(nums))` 是不同边长的个数',
                                                          '`1` → 等边，`2` → 等腰，`3` → 不等边',
                                                          '用下标 `len(set(nums)) - 1` 直接取结果字符串'])],
        summary=['时间 `O(1)`（数组长度固定为 3），空间 `O(1)`',
                 '易错：判合法要用 `a + b <= c`，等于也不行（退化成线段）',
                 '易错：先判合法再判类型，顺序不能反',
                 '不排序也可以，但要写三个不等式'],
    ),
)

CONFIG = dict(
    num=2475, title='数组中不等三元组的数目', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='哈希表 · 利用对称性',
    tags=[],
    code='''
class Solution:
    def unequalTriplets(self, nums: List[int]) -> int:
        ans, a, c = 0, 0, len(nums)
        for b in Counter(nums).values():
            c -= b
            ans += a * b * c
            a += b
        return ans
''',
    call='Solution().unequalTriplets([4,4,2,4,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（位置不重要，只看每种数出现几次）', h=170),
        dict(type='map', var=lambda S: {k: S['nums'].count(k) for k in dict.fromkeys(S['nums'])}, label='Counter(nums)：值 → 出现次数', fmt=lambda k, v: f'{k}: {v}', h=170),
        dict(type='text', h=130, size=30,
             fn=lambda S: (f"前面 a=`{S['a']}` 个，当前 b=`{S['b']}` 个，后面 c=`{S['c']}` 个  →  乘积 =={S['a']*S['b']*S['c']}==") if 'b' in S and 'c' in S else ''),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'yellow'), ('c', 'c', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans, a, c =': '`a = 0`：前面还没有数；`c = {c}`：一开始所有数都在“后面”',
        'for b in': '取下一种数，它出现了 `b = {b}` 次',
        'c -= b': '这种数从“后面”挪出来：`c = {B.c} - {b} = {c}`',
        'ans += a * b * c': '前 `{a}` 个 × 当前 `{b}` × 后 `{c}` = `{a*b*c}`，`ans` → =={ans}==。三组各取一个，必然两两不同',
        'a += b': '这种数处理完，归入“前面”：`a = {a}`',
        'return ans': '所有数值都处理完，三元组共 `{ans}` 个',
    },
    cards=dict(
        one_liner='位置不重要：按“数值分组”，中间组 × 前面组 × 后面组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums`，数 `(i, j, k)` 满足 `i<j<k` 且三个数两两不同，数有多少组',
                 '示例：`[4,4,2,4,3]` → `3`',
                 '三个数两两不同，就等于三个不同的数值各取一个'],
        quote='由于元素的位置是不重要的，我们可以直接用哈希表统计',
        quote_src='—— 灵茶山艾府题解（方法二：利用对称性）',
        idea=['每种数值当“中间那一组”：前面已遍历的数有 `a` 个，它有 `b` 个，剩下 `c` 个',
              '它对答案的贡献是 `a × b × c`，累加所有分组',
              '遍历完一组就把它并入 `a`，同时 `c` 先减去 `b`'],
        summary=['时间 `O(n)`，空间 `O(n)`（哈希表）',
                 '易错：`c -= b` 要在乘之前做，否则当前组会被算进“后面”',
                 '方法一：排序后按相同值分段，同样算 `a·b·c`，时间 `O(n log n)`',
                 '同类思路：先按值计数，再用组合计数代替暴力枚举'],
    ),
)

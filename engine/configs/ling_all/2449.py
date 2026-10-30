CONFIG = dict(
    num=2449, title='使数组相似的最少操作次数', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='奇偶分组 + 排序一一配对',
    tags=['贪心与思维', '双序列配对', '难度分 2076'],
    code='''
def f(a: List[int]) -> None:
    for i, x in enumerate(a):
        if x % 2: a[i] = -x  # 由于元素都是正数，把奇数变成相反数，这样排序后奇偶就自动分开了
    a.sort()

class Solution:
    def makeSimilar(self, nums: List[int], target: List[int]) -> int:
        f(nums)
        f(target)
        return sum(abs(x - y) for x, y in zip(nums, target)) // 4
''',
    call='Solution().makeSimilar([8,12,6,3,5], [2,14,10,7,1])',
    expect=3,
    views=[
        dict(type='array', var=lambda S: S['a'] if 'a' in S else S.get('nums'), label='nums（奇数取负后排序：负数是奇数组，非负是偶数组）', h=200,
             pointers={'i': 'blue'}, color=lambda S, i, v: 'orange' if isinstance(v, int) and v < 0 else None),
        dict(type='array', var=lambda S: S.get('target'), label='target', h=200,
             color=lambda S, i, v: 'orange' if isinstance(v, int) and v < 0 else None),
        dict(type='text', h=70, fn=lambda S: '橙色 = 已取负的奇数；排序后负数在前，奇偶自动分开' if 'a' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), 'x'],
    captions={
        'for i, x in enumerate': lambda S, B, r: ('这个数组的每个数都处理完了' if B.get('i') == S['i'] and B.get('x') == S['x'] else f"看第 `{S['i']}` 个数 `x = {S['x']}`"),
        'if x % 2': '`{x} % 2` = {x % 2}：{"奇数 → 取相反数" if x % 2 else "偶数 → 不动"}',
        'a.sort()': '排序后奇数（负）全在前、偶数在后，各自从小到大：`{a}`',
        'f(nums)': '处理 nums：奇偶分开并排序',
        'f(target)': '同样处理 target',
        'return sum': lambda S, B, r: f'逐位配对 `|x − y|` 求和，再除以 4（每次操作改变 4 的变化量）→ ==返回 {r}==',
    },
    cards=dict(
        one_liner='奇偶分组后排序配对，差的绝对值之和除以 4',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['一次操作：`nums[i] += 2`，`nums[j] -= 2`',
                 '两数组每个元素出现频率相同就叫相似，求最少操作次数',
                 '示例：`[8,12,6,3,5]` 变成 `[2,14,10,7,1]` → `3`'],
        quote='把所有奇数变成相反数，然后排序，奇偶就自动分开了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想简化版：改成 +1/−1，最小配最小、次小配次小，变化量之和最小（邻项交换法）',
              '+2/−2 不改变奇偶性，所以奇数、偶数分别配对',
              '总变化量里加和减各占一半，每次操作变化 4，除以 4 即答案'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（原地排序）',
                 '易错：必须按奇偶分开配对，不能直接整体排序',
                 '取负技巧依赖元素都是正数；负奇数 < 0 ≤ 偶数',
                 '最后是 `// 4`：总变化量（加+减）是操作数的 4 倍'],
    ),
)

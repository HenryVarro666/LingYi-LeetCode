def _txt(S):
    if 'q' not in S or 'n' not in S:
        return ''
    if S.get('_line', 0) < 11:
        return f"扫描中：最小值下标 `p = {S['p']}`，最大值下标 `q = {S['q']}`"
    p, q, n = S['p'], S['q'], S['n']
    return (f"前缀 `q+1 = {q+1}`；后缀 `n-p = {n-p}`；前缀+后缀 `p+1+n-q = {p+1+n-q}` → 取 ==最小=={min(q+1, n-p, p+1+n-q)}==")


CONFIG = dict(
    num=2091, title='从数组中移除最大值和最小值', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 三种删除策略',
    tags=['灵神题单', '难度分 1384'],
    code='''
class Solution:
    def minimumDeletions(self, nums: List[int]) -> int:
        n = len(nums)
        p = q = 0
        for i, x in enumerate(nums):
            if x < nums[p]:
                p = i
            elif x > nums[q]:
                q = i

        if p > q:
            p, q = q, p  # 保证 p <= q，方便下面计算
        return min(q + 1, n - p, p + 1 + n - q)
''',
    call='Solution().minimumDeletions([2,10,7,5,4,1,8,6])',
    expect=5,
    views=[
        dict(type='text', fn=_txt, size=28, h=130),
        dict(type='array', var='nums', pointers={'p': 'blue', 'q': 'pink', 'i': 'yellow'}, h=330,
             color=lambda S, i, v: ('blue' if i == S.get('p') else 'pink' if i == S.get('q') else None)),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), 'i', 'x'],
    captions={
        'n = len': '`n = {n}`',
        'p = q = 0': '`p` 记最小值下标，`q` 记最大值下标，先都指向 0',
        'for i, x': '看第 `{i}` 个数 `x = {x}`',
        'if x < nums[p]': '`x = {x}` 与当前最小值 `nums[{p}] = {nums[p]}` 比较 → ' + '{"更小，更新 p" if x < nums[p] else "不更小，看是不是最大"}',
        'p = i': '找到更小的数：`p = {p}`，最小值是 `{nums[p]}`',
        'elif x > nums[q]': '`x = {x}` 与当前最大值 `nums[{q}] = {nums[q]}` 比较 → ' + '{"更大，更新 q" if x > nums[q] else "也不更大，跳过"}',
        'q = i': '找到更大的数：`q = {q}`，最大值是 `{nums[q]}`',
        'if p > q': '`p = {p}`，`q = {q}`：最小值在最大值右边吗 → ' + '{"是，交换" if p > q else "否，不用交换"}',
        'p, q = q, p': '交换后 `p = {p} <= q = {q}`：==p 在左，q 在右==，三种策略的公式才成立',
        'return min': '三种方案取最小：前缀 `{q+1}`、后缀 `{n-p}`、两头 `{p+1+n-q}` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='两个目标只能从两头删：前缀、后缀、或前后各删一段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次只能删数组最前面或最后面的一个元素',
                 '求把最小值和最大值都删掉的最少次数',
                 '示例：`[2,10,7,5,4,1,8,6]` → `5`'],
        quote='设 nums 的长度为 n，其最小值的下标为 p，最大值的下标为 q。假设 p≤q（若不满足则交换）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先扫一遍找到 `p`、`q`，保证 `p <= q`',
              '删前缀到 `q`：`q+1` 次；删后缀到 `p`：`n-p` 次',
              '前面删到 `p`、后面删到 `q`：`p+1+n-q` 次',
              '三者取最小就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：交换 `p, q` 后才能用这三个公式；下标从 0 开始所以要 `+1`',
                 '只有一个元素时 `p = q = 0`，答案为 1',
                 '写法二：用 `nums.index(min(nums))` 和 `nums.index(max(nums))` 直接得到 p、q'],
    ),
)

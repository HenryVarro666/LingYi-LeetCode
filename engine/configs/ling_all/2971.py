def _idx(S):
    """当前 x 在排序后数组里的下标（由前缀和反推）"""
    if 's' not in S or S['s'] <= 0:
        return None
    t = 0
    for i, v in enumerate(S['nums']):
        t += v
        if t == S['s']:
            return i
    return None


def _info(S):
    i = _idx(S)
    if i is None:
        return '先排序，再从小到大累加前缀和'
    x = S['nums'][i]
    s = S['s']
    ok = s > 2 * x
    return f"最长边 `x = {x}`，其余边之和 `{s - x}`：{'==' if ok else ''}{s - x} {'>' if ok else '≤'} {x}{'==' if ok else ''}，当前周长候选 `{s}`"


CONFIG = dict(
    num=2971, title='找到最大周长的多边形', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 前缀和',
    tags=['灵神题单', '难度分 1521'],
    code='''
class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        nums.sort()
        ans = -1
        s = 0
        for x in nums:
            s += x
            if s > x * 2:  # s-x > x
                ans = s
        return ans
''',
    call='Solution().largestPerimeter([1,12,1,2,5,50,3])',
    expect=12,
    views=[
        dict(type='text', fn=_info, size=30),
        dict(type='array', var='nums', h=200, 
             
             color=lambda S, i, v: ('green' if _idx(S) is not None and i <= _idx(S) and S.get('ans', -1) > 0 and sum(S['nums'][:i + 1]) <= S['ans'] else ('blue' if i == _idx(S) else None)),
             dim=lambda S, i, v: _idx(S) is not None and i > _idx(S)),
    ],
    watch=[('x', 'x', 'blue'), ('s 前缀和', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '排序后，每个数左边都是不比它大的数：==枚举谁当最长边==就很方便 → `{nums}`',
        'for x in nums': '取出下一个数 `x`（从小到大）',
        'ans = -1': '`ans = -1`：还没找到任何合法多边形',
        's += x': '`s` 加上 `x = {x}`：`s` 是 ==以 x 为最长边的最大周长==，前缀和 `{s}`',
        'if s > x * 2': lambda S, B, r: f"`s > 2x`，即 `{S.s - S.x} > {S.x}`（其余边之和 > 最长边）→ " + ('成立，能围成多边形' if S.s > 2 * S.x else '不成立，x 太长'),
        'ans = s': '合法：`ans = {ans}`。==更晚的合法前缀和一定更大==，直接覆盖',
        'return ans': '没有更长的合法前缀了，返回 `{ans}`',
    },
    cards=dict(
        one_liner='排序后枚举最长边，周长就是某个前缀和',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['多边形：最长边 ==小于== 其余边之和，至少 3 条边',
                 '从 `nums` 里选边，求最大周长，不行就返回 `-1`',
                 '示例：`[1,12,1,2,5,50,3]` → `12`（1+1+2+3+5）'],
        quote='枚举 nums[i] 作为最长的那条边，那么 nums[i] 左边的数之和越大越好，这样才能尽可能地组成多边形，并且周长尽量长。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后固定最长边 `nums[i]`，左边的数全选，和最大',
              '所以周长只可能是某个前缀和 `s`，条件 `s - x > x`',
              '从左到右扫，==最后一个==满足条件的前缀和就是答案'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '条件写成 `s > x * 2`，避免再减一次',
                 '`ans` 初始 `-1`：一个多边形都凑不出时返回它',
                 '不用回头找：越靠后的合法前缀和越大'],
    ),
)

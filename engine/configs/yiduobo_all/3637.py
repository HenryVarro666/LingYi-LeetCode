def _col(S, j, v):
    a = S['nums']
    if 'p' not in S:
        return None
    p = S['p']
    if j <= p:
        return 'green'
    if 'q' not in S:
        return None
    q = S['q']
    if j <= q:
        return 'orange'
    if 'v' in S and 'pre' in S:
        k = a.index(S['pre'], q)
        return 'green' if j <= k else None
    return None


CONFIG = dict(
    num=3637, title='三段式数组 I', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='先找 p 再找 q · 最后检查第三段', tags=[],
    code='''
class Solution(object):
    def isTrionic(self, nums):
        
        p = 0
        while p + 1 < len(nums) and nums[p + 1] > nums[p]:
            p += 1
        
        if p == 0:
            return False
        
        q = p
        while q + 1 < len(nums) and nums[q + 1] < nums[q]:
            q += 1
        
        if q == p or q == len(nums) - 1:
            return False
        
        pre = nums[q]
        for v in nums[q + 1:]:
            if v <= pre:
                return False
            pre = v
            
        return True
''',
    call='Solution().isTrionic([1,3,5,4,2,6])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 第一段，橙 = 第二段）', h=300,
             pointers={'p': 'blue', 'q': 'pink'}, color=_col),
        dict(type='text', h=90, size=30, fn=lambda S: ('第三段：每个数必须比前一个大，`pre = ' + str(S['pre']) + '`') if 'pre' in S else ''),
    ],
    watch=['p', 'q', 'pre'],
    captions={
        'p = 0': '`p` 从 0 出发，向右走完「严格递增」的第一段',
        'while p + 1 < len(nums)': lambda S, B, r: (f'`nums[{S.p+1}] = {S.nums[S.p+1]} > nums[{S.p}] = {S.nums[S.p]}`？成立 → `p` 还能右移' if S.p + 1 < len(S.nums) and S.nums[S.p + 1] > S.nums[S.p]
                                                     else '递增走不下去了（下一个不更大或到头），第一段到 `p` 结束'),
        'p += 1': '`p` → =={p}==',
        'if p == 0': lambda S, B, r: ('`p` 一步都没动：根本没有递增的第一段 → 返回 False' if S.p == 0
                                      else f'`p = {S.p}`：第一段是 `nums[0..{S.p}]`，至少两个数，继续'),
        'q = p': '第二段从 `p` 开始（`p` 是第一段的终点，也是第二段的起点）：`q = {q}`',
        'while q + 1 < len(nums)': lambda S, B, r: (f'`nums[{S.q+1}] = {S.nums[S.q+1]} < nums[{S.q}] = {S.nums[S.q]}`？成立 → `q` 还能右移' if S.q + 1 < len(S.nums) and S.nums[S.q + 1] < S.nums[S.q]
                                                     else '递减走不下去了，第二段到 `q` 结束'),
        'q += 1': '`q` → =={q}==',
        'if q == p or': lambda S, B, r: ('`q == p`：没有递减段 → False' if S.q == S.p else
                                         '`q` 已在末尾：没留给第三段的数 → False' if S.q == len(S.nums) - 1
                                         else f'`q = {S.q}`：第二段 `nums[{S.p}..{S.q}]` 合法，后面还有数留给第三段'),
        'pre = nums[q]': '第三段从 `q` 起，`pre = nums[q] = {pre}`：后面每个数必须比前一个大',
        'for v in nums': lambda S, B, r: (f'检查第三段的下一个数 `v = {S.v}`' if S.v != B.get('v') or S.pre == S.nums[S.q] else '第三段的数都检查完了'),
        'if v <= pre': lambda S, B, r: (f'`{S.v} <= {S.pre}`：不是严格递增 → 返回 False' if S.v <= S.pre
                                        else f'`{S.v} > {S.pre}`：仍然严格递增'),
        'pre = v': '`pre` 更新为 `{pre}`',
        'return True': '三段都满足 → 返回 ==True==',
    },
    cards=dict(
        one_liner='用 p、q 两个指针从左往右依次走完三段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 要能分成：严格增 → 严格减 → 严格增',
                 '分界点满足 `0 < p < q < n - 1`',
                 '本视频：`[1,3,5,4,2,6]` → `true`'],
        quote='若p一步都没动过，说明不存在递增的第一段，直接返回false。否则就从p开始向后遍历，寻找对应的q。',
        quote_src='—— yiduobo 题解原文',
        idea=['三段要覆盖整个数组，所以从 0 开始顺着走：先找 `p`，再找 `q`',
              '`p` 没动或 `q` 没动，说明某一段不存在；`q` 到末尾说明没有第三段',
              '最后一段用 `pre` 记录上一个数，逐个检查严格递增'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`q` 从 `p` 开始而不是 `p + 1`，拐点同时属于两段',
                 '`q == len(nums) - 1` 表示第三段没有数，要返回 False',
                 '相等的数让 while 停下，后续检查会判 False',
                 '对比灵神：灵神用一次遍历数拐弯次数，yiduobo 分三段显式推进指针'],
    ),
)

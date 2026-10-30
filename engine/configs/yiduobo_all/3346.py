def _txt(S):
    if 'v' not in S or 'right' not in S or 'res' not in S:
        return '每个数 `x` 能变成 `[x−k, x+k]` 里任意值；候选目标只有 `x−k`、`x`、`x+k`'
    v, k = S['v'], S['k']
    m = S['right'] - S['left']
    c = S['cnt'].get(v, 0)
    return f'目标 `{v}`，窗口 `[{v - k}, {v + k}]` 有 {m} 个数（{c} 个本就是 {v}）→ `min({S["numOperations"]}, {m}−{c}) + {c}` = =={min(S["numOperations"], m - c) + c}=='


CONFIG = dict(
    num=3346, title='执行操作后元素的最高频率 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='候选目标 + 排序滑动窗口', tags=[],
    code='''
class Solution(object):
    def maxFrequency(self, nums, k, numOperations):
        
        cnt = {}
        num_set = set()
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            num_set.add(v)
            num_set.add(v - k)
            num_set.add(v + k)
        
        nums.sort()
        left = 0
        right = 0
        res = 0
        for v in sorted(list(num_set)):
            while right < len(nums) and nums[right] - k <= v:
                right += 1
            while nums[left] + k < v:
                left += 1
            
            res = max(res, min(numOperations, right - left - cnt.get(v, 0)) + cnt.get(v, 0))
        return res
''',
    call='Solution().maxFrequency([1,4,5], 1, 2)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=110, size=26),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, label='nums（排序后）',
             window=('left', 'right - 1') , h=170,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i < S['right'])),
        dict(type='set', var='num_set', label='候选目标 num_set', h=130),
        dict(type='map', var='cnt', label='cnt：每个值出现几次', h=130),
    ],
    watch=['k', 'numOperations', 'v', ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt[v] = ': '统计 `{v}` 出现次数：`cnt[{v}] = {cnt[v]}`',
        'num_set.add(v)': '`{v}` 自己：不操作时它可能就是==最多数相交的位置==',
        'num_set.add(v - k)': '`{v} − k = {v - k}`：把 {v} 往下调到最远，也可能是目标',
        'num_set.add(v + k)': '`{v} + k = {v + k}`：往上调到最远。每个数最多贡献 3 个候选，共 `3n` 个',
        'nums.sort()': '排序：之后「以 v 为中心的窗口覆盖哪些数」就是==滑动窗口==，`nums` = {nums}',
        'left = 0': '`left`、`right` 夹住的就是窗口 `nums[left:right]`',
        'for v in sorted': '按从小到大枚举候选目标 `v = {v}`（窗口只会往右滑）',
        'nums[right] - k <= v': lambda S, B, r: (f'`nums[{S.right}] − k = {S.nums[S.right] - S.k} <= {S.v}`：{S.nums[S.right]} 能调到 {S.v} → ==right 右移== 纳入窗口' if S.right < len(S.nums) and S.nums[S.right] - S.k <= S.v else ('`right` 已到末尾，不再右移' if S.right >= len(S.nums) else f'`nums[{S.right}] − k = {S.nums[S.right] - S.k} > {S.v}`：{S.nums[S.right]} 够不着 {S.v}，right 停下')),
        'right += 1': '`right` → {right}：窗口右端多纳入一个数',
        'nums[left] + k < v': lambda S, B, r: (f'`nums[{S.left}] + k = {S.nums[S.left] + S.k} < {S.v}`：{S.nums[S.left]} 再往上调也够不到 {S.v} → ==left 右移==' if S.nums[S.left] + S.k < S.v else f'`nums[{S.left}] + k = {S.nums[S.left] + S.k} >= {S.v}`：{S.nums[S.left]} 还能调到 {S.v}，left 停下'),
        'left += 1': '`left` → {left}：丢掉够不着的数',
        'res = max': lambda S, B, r: f'窗口 {S.right - S.left} 个数，其中 {S.cnt.get(S.v, 0)} 个本就等于 {S.v}；其余最多再操作 {S.numOperations} 次 → 频率 `{min(S.numOperations, S.right - S.left - S.cnt.get(S.v, 0)) + S.cnt.get(S.v, 0)}`，`res = {S.res}`',
        'return res': '最高频率 `{res}`',
    },
    skip=['cnt[v] = ', 'right = 0', 'res = 0'],
    max_steps=80,
    cards=dict(
        one_liner='最多区间相交的点，一定在某个区间的端点上',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums[i]` 可加上 `[-k, k]` 内整数，最多操作 `numOperations` 次（每个下标至多一次）',
                 '求操作后==出现次数最多==的元素出现了几次',
                 '示例：`nums=[1,4,5], k=1, numOperations=2` → `2`'],
        quote='对于区间重叠类的问题，一个经典的结论就是最多区间相交的下标一定处于某个区间的起点或者终点。',
        quote_src='—— yiduobo 题解原文',
        idea=['把 `nums[i]` 看成区间 `[nums[i]−k, nums[i]+k]`，求被最多区间覆盖的点',
              '候选点只有 `nums[i]`、`nums[i]−k`、`nums[i]+k`，共 `3n` 个',
              '反过来想：以 v 为中心扩 k，看能盖住几个数 → 排序后是滑动窗口',
              '窗口里本来等于 v 的不用操作，其余最多操作 `numOperations` 个'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：窗口里 `cnt[v]` 个数不消耗操作次数，答案是 `min(numOperations, m−cnt[v]) + cnt[v]`',
                 '易错：`left` 的条件是 `nums[left] + k < v`，不能写成 `<=`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（代码未改）',
                 '同题 3347 数据更大，同一思路（候选点 + 滑窗）'],
    ),
)

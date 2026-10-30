def _x(S):
    if 'x' not in S or 'cnt' not in S:
        return ''
    x = S['x']
    c = S['cnt'][x] if x in S['cnt'] else 0
    return f"当前 `x = {x}`，`cnt[{x}] = {c}`，答案 `ans = {S['ans']}`"


CONFIG = dict(
    num=350, title='两个数组的交集 II', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='哈希表计数 · 次数递减',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        cnt = Counter(nums1)
        ans = []
        for x in nums2:
            if cnt[x] > 0:
                cnt[x] -= 1
                ans.append(x)
        return ans
''',
    call='Solution().intersect([1,2,2,1,3], [2,2,2,1,4])',
    expect=[2, 2, 1],
    views=[
        dict(type='array', var='nums2', label='nums2', h=170,
             color=lambda S, i, v: ('yellow' if 'x' in S and v == S['x'] else None)),
        dict(type='map', var='cnt', h=230),
        dict(type='array', var='ans', label='ans', h=170),
        dict(type='text', fn=_x),
    ],
    watch=[('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '把 `nums1` 里每个数的出现次数记进哈希表：`cnt = {cnt}`',
        'ans = []': '`ans` 收集交集里的元素',
        'for x in nums2': '遍历 `nums2`，当前 `x = {x}`',
        'if cnt[x] > 0': lambda S, B, r: (f'`cnt[{S.x}] = {S.cnt[S.x]} > 0`：`nums1` 里还剩可配对的 {S.x} → 能配对'
                                           if S.cnt[S.x] > 0 else
                                           f'`cnt[{S.x}] = {S.cnt[S.x]}`：`nums1` 里的 {S.x} 已经用完（或没有）→ 不加入答案'),
        'cnt[x] -= 1': '配对成功，用掉一个：`cnt[{x}]` → =={cnt[x]}==',
        'ans.append(x)': '`{x}` 加入答案 → `ans = {ans}`',
        'return ans': '交集（含重复次数）是 `{ret}`',
    },
    cards=dict(
        one_liner='349 的哈希集合改成哈希表，value 记录还能配对几次',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['返回两个数组的交集，每个元素出现次数取两边较小值',
                 '示例：`[1,2,2,1]` 和 `[2,2]` → `[2,2]`',
                 '本视频：`[1,2,2,1,3]` 和 `[2,2,2,1,4]` → `[2,2,1]`'],
        quote='本题只需把哈希集合改成哈希表，其中哈希表的 value 表示 key 的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用 `Counter(nums1)` 统计 `nums1` 里每个数的次数',
              '遍历 `nums2`：次数大于 0 就加入答案，同时次数减一',
              '次数减到 0 后，后面遇到相同的数就不会再加入答案'],
        summary=['时间 `O(n+m)`，空间 `O(n)`；可以把较短的数组建哈希表，空间 `O(min(n,m))`',
                 '一遍扫描 `nums2`，所以 `nums2` 是流或在磁盘上也能处理',
                 '易错：必须先判断 `cnt[x] > 0` 再减，不能让次数变负',
                 '数组已排序时可用双指针，空间 `O(1)`（题解附录写法）'],
    ),
)

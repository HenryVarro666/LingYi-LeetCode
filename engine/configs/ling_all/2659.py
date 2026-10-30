CONFIG = dict(
    num=2659, title='将数组清空', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='按值排序 + 统计多走的整圈',
    tags=['树状数组', '难度分 2282'],
    code='''
class Solution:
    def countOperationsToEmptyArray(self, nums: List[int]) -> int:
        ans = n = len(nums)
        id = sorted(range(n), key=lambda x: nums[x])
        for k, (pre, i) in enumerate(pairwise(id), 1):
            if i < pre:  # 必须多走一整圈
                ans += n - k  # 减去前面删除的元素个数
        return ans
''',
    call='Solution().countOperationsToEmptyArray([2,4,1,3,5])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（按值从小到大依次删除）', pointers={'pre': 'blue', 'i': 'pink'}, h=210,
             dim=lambda S, i, v: 'id' in S and 'k' in S and i in S['id'][:S['k']] and i != S.get('i')),
        dict(type='array', var=lambda S: S.get('id'), label='id：按 nums 值排序后的下标（删除顺序）', pointers={'k': 'pink'}, h=190),
        dict(type='text', fn=lambda S: (f"第 {S['k']} 次删 `nums[{S['pre']}]={S['nums'][S['pre']]}`，第 {S['k']+1} 次删 `nums[{S['i']}]={S['nums'][S['i']]}`：" + ("==在左边，要多绕一整圈==" if S['i'] < S['pre'] else "在右边，顺着走就到") if 'pre' in S else ''), h=70),
    ],
    watch=['k', 'pre', 'i', ('ans', 'ans', 'green')],
    captions={
        'ans = n = len': '先把 `n = {n}` 次删除操作计入答案，后面只数「移动」次数',
        'id = sorted': '删除顺序 = 值从小到大；对==下标==排序（不能直接排 nums，位置很重要）：`id = {id}`',
        'for k, (pre, i)': '取相邻两个要删的位置：`pre = {pre}`（第 {k} 个）→ `i = {i}`（第 {k+1} 个）',
        'if i < pre': lambda S, B, ret: (f'`i = {S.i} < pre = {S.pre}`：下一个要删的在左边 → ==必须绕一整圈== ' if S.i < S.pre else f'`i = {S.i} > pre = {S.pre}`：在右边，顺着往后走，免费（删除已计入）'),
        'ans += n - k': '多走一整圈：`n - k = {n}-{k}` = {n-k}（前面已删的 {k} 个元素不用走）→ `ans` = =={ans}==',
        'return ans': '总操作数 `{ans}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='按值从小到大删：下一个在左边，就多绕一圈 n-k',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组元素互不相同，反复操作直到清空：',
                 '队首是最小值 → 删除；否则把队首挪到队尾',
                 '示例：`[3,4,-1]` → `5`；本视频：`[2,4,1,3,5]`'],
        quote='如果第 k 次要删除的元素在第 k-1 次要删除的元素的左侧，那么必须多走一整圈，移动次数为 n-k。累加，即为总的移动次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把操作想成一个下标在数组上反复绕圈：按值从小到大删',
              '先把 `n` 次删除计入答案；删除时那一步等于免费前进一格',
              '相邻两个删除位置 `pre → i`：`i < pre` 就多走一整圈，减去已删的 `k` 个，共 `n-k` 步'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '关键：只比较相邻删除位置的左右，不用模拟',
                 '枚举从 1 开始：`enumerate(pairwise(id), 1)` 使 `k` 恰为已删个数',
                 '方法一：树状数组统计区间内已删个数，同样 `O(n log n)`，本视频演示方法二'],
    ),
)

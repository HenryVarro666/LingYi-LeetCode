CONFIG = dict(
    num=3730, title='跳跃燃烧的最大卡路里', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 最大/最小交替', tags=['贪心', '排序'],
    code='''
class Solution(object):
    def maxCaloriesBurnt(self, heights):
        
        heights.sort()
        left, right = 0, len(heights) - 1
        res = 0
        pre = 0
        while left <= right:
            res += (heights[right] - pre) ** 2
            pre = heights[right]
            right -= 1
            if left <= right:
                res += (heights[left] - pre) ** 2
                pre = heights[left]
                left += 1
        
        return res
''',
    call='Solution().maxCaloriesBurnt([4,1,3,2,5])',
    expect=55,
    views=[
        dict(type='bars', var='heights', pointers={'left': 'blue', 'right': 'pink'}, h=380,
             dim=lambda S, i, v: 'right' in S and (i < S['left'] or i > S['right'])),
        dict(type='text', h=70, fn=lambda S: f"上一块高度 `pre = {S['pre']}`，累计卡路里 res = ==%s==" % S['res'] if 'pre' in S else ''),
    ],
    watch=['left', 'right', 'pre', ('res', 'res', 'green')],
    captions={
        'heights.sort()': '先从小到大排序：`{heights}`，最大的和最小的分列两端',
        'left, right': '`left = 0` 指最小，`right = {right}` 指最大',
        'pre = 0': '`pre` 是上一次所在高度；从地面起跳，所以起点是 `0`',
        'while left <= right': lambda S, B, r: (f'`left = {S.left} <= right = {S.right}`，还有方块没跳' if S.left <= S.right else f'`left = {S.left} > right = {S.right}`：方块跳完了'),
        'res += (heights[right]': '先跳最高的：`({heights[right]} - {B.pre})^2` = =={(heights[right]-B.pre)**2}==，`res = {res}`',
        'pre = heights[right]': '落在高度 `{pre}` 的方块上',
        'right -= 1': '最高的用掉了，`right` 左移到 {right}',
        'if left <= right': lambda S, B, r: ('还剩方块 → 接着跳最矮的' if S.left <= S.right else '指针错开，没有方块了'),
        'res += (heights[left]': '再跳最矮的，跨度最大：`({heights[left]} - {B.pre})^2` = =={(heights[left]-B.pre)**2}==，`res = {res}`',
        'pre = heights[left]': '落在高度 `{pre}` 的方块上',
        'left += 1': '最矮的用掉了，`left` 右移到 {left}',
        'return res': '最大总卡路里 `{res}`',
    },
    cards=dict(
        one_liner='最大、最小、最大、最小：每一步跨度都尽量大',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`heights[i]` 是第 `i` 个方块的高度，从地面出发，每个方块恰好跳一次',
                 '从高度 `a` 跳到 `b` 消耗 `(a-b)^2`，第一跳消耗 `x^2`（`x` 为目标高度）',
                 '求所有方块跳完后的最大总卡路里',
                 '本视频：`[4,1,3,2,5]`'],
        quote='直观感觉上就应该让每一步的跨度都尽可能大，所以应该将这些方块按照最大-最小-最大-最小的顺序排布。虽然不知道怎么给出严谨的证明，但是也没有找到反例。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序，两个指针 `left`、`right` 从两端向中间',
              '每一轮先跳 `right`（最高），再跳 `left`（最矮）',
              '地面当作高度 0，所以 `pre` 初值为 0'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`right` 跳完要再判断 `left <= right`：方块数为奇数时最后一块只跳一次',
                 '作者承认没有严格证明，只是没找到反例',
                 '`heights.sort()` 会原地改动输入'],
    ),
)

def _col(S, i, v):
    n = S.get('nums')
    if not n or 'm' not in S:
        return None
    if i == S['m']:
        return 'yellow'
    if 'index' in S and i == S['index']:
        return 'red' if v == n[S['m']] else 'blue'
    return None


CONFIG = dict(
    num=3978, title='唯一中间元素', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 · 找与中间值相同的其他位置', tags=[],
    code='''
class Solution(object):
    def isMiddleElementUnique(self, nums):
        
        m = len(nums) // 2
        for index, v in enumerate(nums):
            if v == nums[m] and index != m:
                return False
        
        return True
''',
    call='''Solution().isMiddleElementUnique([4, 2, 7, 5, 9, 6, 1])''',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"中间位置 `m = {S['m']}`，中间元素 `nums[m] = {S['nums'][S['m']]}`" if 'm' in S else ''), size=28),
        dict(type='array', var='nums', label='nums（黄 = 中间元素，蓝 = 正在检查的位置）', cell=90, color=_col, pointers={'m': 'yellow'}, h=240),
        dict(type='text', fn=lambda S: '只要别的位置出现同样的值，就返回 False', size=24),
    ],
    watch=[('m', 'm', 'yellow'), ('index', 'index', 'blue'), ('v', 'v', 'pink')],
    captions={
        'm = len': '`m = len(nums) // 2 = {m}`：奇数长度，正中间的下标',
        'for index': lambda S, B, ret: (f"检查下标 `{S.index}`，`v = {S.v}`" if S.get('index') is not None and S.get('v') is not None and ('index' not in B or S.index != B.get('index')) else '遍历结束，没发现重复'),
        'if v == nums[m]': lambda S, B, ret: (f"`v = {S.v}` 和 `nums[m] = {S.nums[S.m]}`：" + ('相等，但这正是中间位置本身，不算' if S.v == S.nums[S.m] and S.index == S.m else ('相等且不在中间 → ==有重复==' if S.v == S.nums[S.m] else '不相等，放过'))),
        'return False': '别的位置也有同样的值，中间元素不唯一 → `False`',
        'return True': '除了中间位置，没有别的元素等于它 → ==True==',
    },
    cards=dict(
        one_liner='除了正中间，只要有别的位置等于它就不唯一',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['奇数长度数组 `nums`，中间元素是否在数组中恰好出现一次',
                 '本视频：`[4,2,7,5,9,6,1]` → `true`',
                 '若中间值 2 在别处再出现，就是 `false`'],
        quote='中间元素恰好出现一次，就意味着除了正中间这个位置，其他位置上的元素都和这个中间元素不同。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算出中间下标 `m = len(nums) // 2`',
              '一趟遍历：遇到 `v == nums[m]` 且 `index != m` 立刻返回 `False`',
              '遍历完没发现，就返回 `True`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '必须排除 `index == m`，否则中间元素自己会把自己判成重复',
                 '原文用 `//` 取中点，无需改写',
                 '对比灵神：灵神一行 `count` 数次数，yiduobo 手写遍历并提前返回'],
    ),
)

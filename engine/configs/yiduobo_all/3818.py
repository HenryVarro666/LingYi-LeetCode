CONFIG = dict(
    num=3818, title='移除前缀使数组严格递增', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='倒序扫描，res 记后缀起点', tags=[],
    code='''
class Solution(object):
    def minimumPrefixLength(self, nums):
        
        res = len(nums) - 1
        pre = nums[-1]

        for v in nums[-2::-1]:
            if v >= pre:
                break
            res -= 1
            pre = v
        
        return res
''',
    call='Solution().minimumPrefixLength([3,1,5,6,2,7,8,9,10])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'res': 'blue'}, h=260,
             window=('res', 'len(nums) - 1')),
        dict(type='text', fn=lambda S: f"当前严格递增后缀从下标 =={S['res']}== 开始，要删的前缀长度 = {S['res']}" if 'res' in S else '', h=100),
    ],
    watch=['res', 'pre', 'v'],
    captions={
        'res = len': '先假设只有最后一个元素是递增后缀，那么要删前面 `{res}` 个',
        'pre = nums[-1]': '`pre` 是当前后缀的第一个元素，初始为最后一个 `{pre}`',
        'for v in': '从倒数第二个元素往前看 `v`',
        'if v >= pre': lambda S, B, r: (f'`v = {S.v}` ≥ `pre = {S.pre}` → 接不到后缀前面，后缀到此为止' if S.v >= S.pre else f'`v = {S.v}` < `pre = {S.pre}` → 可以并入严格递增后缀'),
        'break': '停止：再往前的元素都必须删掉',
        'res -= 1': '`v` 并入后缀，要删的前缀少一个：`res` → {res}',
        'pre = v': '后缀新的开头是 `{pre}`',
        'return res': '后缀从下标 `{res}` 开始，前缀 `nums[0..{res}-1]` 要删，长度 =={ret}==',
    },
    cards=dict(
        one_liner='前缀最短 = 递增后缀最长：从后往前找第一个断点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['恰好移除一个前缀（可为空），使剩余数组严格递增', '求被移除前缀的最小长度', '本视频：`[3,1,5,6,2,7,8,9,10]` → `4`'],
        quote='移除的前缀长度最小，就意味着剩下的单调递增的后缀长度最长。于是只需从后往前一趟遍历，找出第一个满足nums[index] >= nums[index + 1]的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['`res` 一开始是 `n-1`：只保留最后一个元素', '每遇到一个更小的 `v`，后缀变长，`res` 减 1', '遇到 `v >= pre` 就 `break`，此时 `res` 正是要删的前缀长度'],
        summary=['时间 `O(n)`，空间 `O(1)`', '易错点：严格递增，`v == pre` 也要 `break`', '`nums[-2::-1]` 是从倒数第二个往前遍历，原文无需修改',
                 '对比灵神：灵神直接用下标 `i` 返回，yiduobo 用 `res` 边扫边减'],
    ),
)

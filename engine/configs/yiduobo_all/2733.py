CONFIG = dict(
    num=2733, title='既不是最小值也不是最大值', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='一趟遍历找次小值', tags=['灵神题单', '贪心与思维', '难度分 1148'],
    code='''
class Solution(object):
    def findNonMinOrMax(self, nums):

        if len(nums) <= 2:
            return -1
        
        mi = nums[0]
        res = nums[1]
        if mi > res:
            res, mi = mi, res
        
        for v in nums[2:]:
            if v < mi:
                mi, res = v, mi
            elif v < res:
                res = v
            
        return res
''',
    call='Solution().findNonMinOrMax([5,3,8,2,6,4])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: ('最小值 `mi` = ' + str(S['mi']) + '，次小值 `res` = ' + str(S['res'])) if 'res' in S and 'mi' in S else '先排除长度 ≤ 2 的情况'),
        dict(type='array', var='nums', label='nums', h=320,
             pointers={'v': 'blue'} if False else {},
             color=lambda S, i, v: ('green' if 'mi' in S and v == S['mi'] else 'orange' if 'res' in S and v == S['res'] else None)),
        dict(type='text', fn=lambda S: '绿 = mi（最小），橙 = res（次小）', size=30),
    ],
    watch=['mi', ('res', 'res', 'orange'), 'v'],
    captions={
        'len(nums) <= 2': '`len(nums) = {len(nums)}`：长度 > 2 吗？只有 1、2 个数时每个数不是最小就是最大，这里条件不成立，继续',
        'return -1': '数组太短，没有「夹在中间」的数 → 返回 `-1`',
        'mi = nums[0]': '先拿前两个数当候选：`mi = {mi}`',
        'res = nums[1]': '`res = {res}`',
        'if mi > res': '`mi = {mi}`、`res = {res}`：保证 mi 是较小的、res 是较大的',
        'res, mi = mi, res': '`mi > res` 成立 → 交换，现在 `mi = {mi}`，`res = {res}`',
        'for v in': lambda S, B, r: (f'看下一个数 `v = {S.v}`' if S.get('v') != B.get('v') else '每个数都看过了，循环结束'),
        'if v < mi': '`v = {v}` 比最小值 `mi = {mi}` 还小？',
        'mi, res = v, mi': '新的最小值是 `{v}`，原最小值 `{res}` 退为次小值',
        'elif v < res': '`v = {v}` 夹在 `mi = {mi}` 和 `res = {res}` 之间？',
        'res = v': '`{v}` 比次小值更小 → `res` 更新为 =={res}==',
        'return res': '次小值 =={res}== 既不是最小也不是最大，返回它',
    },
    cards=dict(
        one_liner='长度大于 2 时，次小值一定既不是最小也不是最大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组中的数互不相同，返回任一个既不是最小也不是最大的数，没有就返回 `-1`',
                 '示例：`[3,2,1,4]` → `2` 或 `3`',
                 '本视频：`[5,3,8,2,6,4]` → `3`'],
        quote='对于数组长度大于2的情况，由于题目保证了数组中的每个数都互不相同，那么只需选择数组中的次小值就能满足题目要求。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理边界：长度 ≤ 2 直接 `-1`',
              '互不相同 → 次小值比最小值大，又比最大值小',
              '一趟遍历同时维护最小值 `mi` 和次小值 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：新最小值出现时，旧的最小值要退位成次小值',
                 '原文为 Python 2 写法，代码无需改动',
                 '对比灵神：灵神只看前三个数取中间值，`O(1)`；这里是通用的找次小值'],
    ),
)

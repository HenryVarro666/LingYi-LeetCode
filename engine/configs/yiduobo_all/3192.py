CONFIG = dict(
    num=3192, title='使二进制数组全部等于 1 的最少操作次数 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · reverse 标记后缀是否翻转',
    tags=['灵神题单', '贪心与思维', '难度分 1433'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        reverse = 0
        res = 0
        for v in nums:
            if v ^ reverse == 0:
                res += 1
                reverse ^= 1

        return res
''',
    call='Solution().minOperations([0,1,1,0,1])',
    expect=4,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"当前后缀 {'==已被翻转==' if S['reverse'] else '没有被翻转'}" + (f"，`v = {S['v']}` 实际是 =={S['v'] ^ S['reverse']}==" if 'v' in S else '')) if 'reverse' in S else ''),
        dict(type='array', var='nums', h=240, label='nums'),
    ],
    watch=[('reverse', 'reverse', 'blue'), ('res', 'res', 'green'), 'v'],
    captions={
        'reverse = 0': '`reverse` 记录当前后缀是否被翻转过：0 = 没有',
        'res = 0': '`res` 累计操作次数',
        'for v in nums': '看当前元素 `v = {v}`，它被翻转过吗？`reverse = {reverse}`',
        'if v ^ reverse == 0': lambda S, B, r: (f'`{S.v} ^ {S.reverse} = 0`：实际值是 0，需要修改' if S.v ^ S.reverse == 0 else f'`{S.v} ^ {S.reverse} = 1`：实际值已是 1，不用管'),
        'res += 1': '以当前下标为起点操作一次：`res` → {res}',
        'reverse ^= 1': '后面的后缀被翻转：`reverse` 取反 → {reverse}（不真的翻转数组）',
        'return res': '一共操作 `{res}` 次',
    },
    cards=dict(
        one_liner='不真翻转数组，用一个 reverse 标记后缀翻没翻',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选下标 `i`，把 `i` 到末尾的元素全部反转',
                 '求让 `nums` 变成全 1 的最少操作次数',
                 '示例：`[0,1,1,0,1]` → `4`'],
        quote='若当前元素需要修改，那么就以当前下标为起点执行操作。当然，在这里不需要真的反转数组的后缀，而是只需要使用一个变量reverse记录当前后缀是否被翻转过。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标 `i` 的操作至多一次（偶数次等于没做）',
              '下标 0 只能靠以 0 为起点的操作修改，后面每个位置同理 → 只能顺序处理',
              '`v` 为 0 且没翻转，或 `v` 为 1 且已翻转，实际值是 0 → 操作并让 `reverse` 取反'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`v ^ reverse == 0` 表示实际值为 0，需要操作',
                 '原文为 Python 2 风格，只删去了空行里的多余缩进，逻辑未改',
                 '对比灵神：灵神用次数 `k` 的奇偶，yiduobo 直接维护翻转标记'],
    ),
)

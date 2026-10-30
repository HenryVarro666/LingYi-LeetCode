CONFIG = dict(
    num=2419, title='按位与最大的最长子数组', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='AND 性质 · 最长连续最大值',
    tags=['灵神题单·位运算', '难度分 1496'],
    code='''
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        ans = mx = cnt = 0
        for x in nums:
            if x > mx:
                # 发现新的 mx，重新统计所有内容
                mx = x
                ans = cnt = 1
            elif x == mx:
                cnt += 1
                if cnt > ans:  # 手写 max 更快
                    ans = cnt
            else:
                cnt = 0  # 连续 mx 断开了，重新统计
        return ans
''',
    call='Solution().longestSubarray([1,2,3,3,2,2,3,3,3,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 等于当前 mx 的数）',
             color=lambda S, i, v: ('green' if 'mx' in S and v == S['mx'] else None)),
        dict(type='text', fn=lambda S: (f"当前最大值 `mx = {S['mx']}`，连续个数 `cnt = {S['cnt']}`，最长 `ans = {S['ans']}`" if 'mx' in S else ''), size=38),
    ],
    watch=[('x', 'x', 'blue'), ('mx', 'mx', 'purple'), ('cnt', 'cnt', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = mx = cnt = 0': '`mx` 最大值、`cnt` 当前连续个数、`ans` 最长长度，都先记 0',
        'for x in nums': '看下一个数 `x = {x}`',
        'if x > mx': lambda S, B, r: (f'`x = {S.x} > mx = {B.mx}`：出现更大的数' if S.x > B.mx else f'`x = {S.x}` 没超过 `mx = {B.mx}`'),
        'mx = x': '==AND 越算越小==，最大值只能是数组最大值。之前统计作废，`mx` → {mx}',
        'ans = cnt = 1': '新的 `mx` 只出现 1 次：`ans = cnt = 1`',
        'elif x == mx': lambda S, B, r: (f'`x = mx = {S.mx}`：和最大值相等，AND 后还是 `mx`' if S.x == S.mx else f'`x = {S.x} < mx = {S.mx}`：比最大值小'),
        'cnt += 1': '连续 `mx` 又多一个：`cnt` → {cnt}',
        'if cnt > ans': lambda S, B, r: (f'`cnt = {S.cnt} > ans = {S.ans}`：刷新最长长度' if S.cnt > S.ans else f'`cnt = {S.cnt}` 没超过 `ans = {S.ans}`，不更新'),
        'ans = cnt': '`ans` → {ans}',
        'cnt = 0': '遇到更小的数：AND 会把结果拉低，连续 `mx` 断开，`cnt` 清零',
        'return ans': '最长连续 `mx` 的长度是 `{ans}`',
    },
    cards=dict(
        one_liner='AND 只会变小，所以答案就是最大值连续出现的最长长度',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在 `nums` 的所有子数组里，找按位与结果最大的',
                 '返回得到这个最大值的最长子数组长度',
                 '示例：`[1,2,3,3,2,2]` → `2`（`[3,3]`）'],
        quote='AND（&）运算的性质是，==参与 AND 运算的元素越多，AND 结果越小==（不会变得更大）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['AND 的数越多只会更小，所以能得到的最大值就是 `max(nums)`',
              '多个 `mx` 相与还是 `mx`，混进一个更小的数就变小',
              '问题变成：只含 `mx` 的最长连续段；一次遍历边找最大边计数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '遇到更大的 `x`，`ans`、`cnt` 都要重置为 1，不是只改 `mx`',
                 '写法一：先 `max(nums)`，再遍历数连续个数；本视频是一次遍历的写法二',
                 '同类题：脑筋急转弯，先用 AND/OR 的单调性缩小问题'],
    ),
)

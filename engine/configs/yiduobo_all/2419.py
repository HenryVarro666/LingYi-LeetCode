CONFIG = dict(
    num=2419, title='按位与最大的最长子数组', difficulty='Medium', category='位运算',
    author='yiduobo', technique='一趟遍历 · 更新最大值和计数',
    tags=['灵神题单·位运算'],
    code='''
class Solution(object):
    def longestSubarray(self, nums):

        ma = 0
        res = 0
        cnt = 0
        for num in nums:
            if num == ma:
                cnt += 1
            elif num > ma:
                ma = num
                res = cnt = 1
            else:
                res = max(res, cnt)
                cnt = 0
        
        return max(res, cnt)
''',
    call='Solution().longestSubarray([1,2,3,3,2,2,3,3,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 等于当前 ma 的数）',
             color=lambda S, i, v: ('green' if 'ma' in S and v == S['ma'] else None)),
        dict(type='text', fn=lambda S: (f"最大值 `ma = {S['ma']}`，当前段长 `cnt = {S['cnt']}`，已记录 `res = {S['res']}`" if 'ma' in S else ''), size=38),
    ],
    watch=[('num', 'num', 'blue'), ('ma', 'ma', 'purple'), ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'ma = 0': '`ma` 记当前见过的最大值',
        'res = 0': '`res` 是答案',
        'for num in nums': '遍历到 `num = {num}`',
        'if num == ma': lambda S, B, r: (f'`num = ma = {S.ma}`：可以并入当前子数组' if S.num == S.ma else f'`num = {S.num}` 不等于 `ma = {S.ma}`'),
        'cnt += 1': '并入子数组，`cnt` 加 1 → {cnt}',
        'elif num > ma': lambda S, B, r: (f'`num = {S.num} > ma = {B.ma}`：之前统计的都不是真正的最大值' if S.num > B.ma else f'`num = {S.num} < ma = {S.ma}`：比最大值小'),
        'ma = num': '之前的统计作废，`ma` 更新为 `{ma}`',
        'res = cnt = 1': '新最大值的段长从 1 开始：`res = cnt = 1`',
        'res = max(res, cnt)': '`num < ma`：上一段结束了，用 `cnt = {cnt}` 更新答案 → `res = {res}`',
        'cnt = 0': lambda S, B, r: ('`cnt` 是当前等于 `ma` 的连续段长度' if S['_line'] == 6 else '`cnt` 清零，等下一段'),
        'return max(res, cnt)': '==最后一段还没用 cnt 结算==，所以取 `max(res, cnt)` = `{ret}`',
    },
    cards=dict(
        one_liner='与运算越算越小，答案就是最大值 ma 的最长连续段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找按位与结果最大的子数组，返回其中最长的长度',
                 '示例：`[1,2,3,3,2,2]` → `2`',
                 '本视频：`[1,2,3,3,2,2,3,3,3]` → `3`'],
        quote='两个正数按位与运算的结果必然是小于等于二者中的较大值，因此本题按位与的最大结果必然是数组中的最大值ma，那么题目就变成了求数组中等于ma的连续子数组的最大长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历：`num == ma` 段长加 1',
              '`num > ma` 说明之前的最大值是假的，重置 `ma`、`cnt`、`res`',
              '`num < ma` 段结束：用 `cnt` 结算答案并清零'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：遍历结束后还要用最后一段的 `cnt` 再取一次 max',
                 '遇到更大值时 `res` 也要重置成 1，旧答案不再有效',
                 '对比灵神：灵神每次 `cnt += 1` 就更新答案，所以不用最后补一次'],
    ),
)

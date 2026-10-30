CONFIG = dict(
    num=4065, title='移除不同值重排数组', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='计数 + 暴力模拟', tags=[],
    code='''
class Solution:
    def rearrangeArray(self, nums: list[int]) -> list[int]:
        mx = max(nums)
        cnt = [0] * (mx + 1)
        for x in nums:
            cnt[x] += 1

        n = len(nums)
        ans = []
        while len(ans) < n:
            for x, c in enumerate(cnt):
                if c > 0:
                    ans.append(x)
                    cnt[x] -= 1
        return ans
''',
    call='Solution().rearrangeArray([3,1,3,2,1,3])',
    expect=[1, 2, 3, 1, 3, 3],
    views=[
        dict(type='array', var='nums', label='nums', pointers={}, h=150),
        dict(type='array', var='cnt', label='cnt[x]：数值 x 还剩几个（下标 = 数值）', pointers={'x': 'blue'}, h=220,
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='array', var='ans', label='ans（每一轮把 cnt > 0 的数从小到大加入）', h=170),
    ],
    watch=[('x', 'x', 'blue'), ('c', 'c', 'cyan'), ('len(ans)', 'len(ans)', 'green')],
    captions={
        'cnt[x] += 1': '统计出现次数：`cnt[{x}]` → =={cnt[x]}==',
        'while len(ans) < n': lambda S, B, r: (f'`len(ans) = {len(S.ans)} < n = {S.n}`：还没凑够，再扫一轮' if len(S.ans) < S.n else f'`len(ans) = {len(S.ans)} = n`：凑够了，退出循环'),
        'if c > 0': lambda S, B, r: (f'`cnt[{S.x}] = {S.c} > 0`：这个数还剩 → ==这一轮要取一个==' if S.c > 0
                                     else f'`cnt[{S.x}] = 0`：这个数没有了（或没出现）→ 跳过'),
        'ans.append(x)': '按下标从小到大扫，天然是升序：`{x}` 加入 `ans` → {ans}',
        'cnt[x] -= 1': '每轮只移除一个：`cnt[{x}]` 减一 → =={cnt[x]}==',
        'return ans': '`ans` 长度已达 `n`，返回 `{ans}`',
    },
    cards=dict(
        one_liner='每一轮从小到大扫一遍计数数组，有剩的各取一个',
        complexity='时间 `O(nU)`，空间 `O(U)`',
        problem=['每轮把 `nums` 里每个不同的值各移除一个，按升序放进 `ans`，直到 `nums` 为空',
                 '示例：`[3,1,3,2,1,3]` → `[1,2,3,1,3,3]`'],
        quote='统计每个元素的出现次数 cnt。每轮循环，把 cnt 中出现次数大于 0 的数，从小到大加入答案，然后把这些数的出现次数都减少一。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['`cnt` 的下标就是数值，从左往右扫天然升序',
              '`cnt[x] > 0` 说明 x 还在 `nums` 里，取一个并减一',
              '重复到 `ans` 长度等于 `n`'],
        summary=['时间 `O(nU)`，`U = max(nums)`；空间 `O(U)`',
                 '易错：`cnt` 要开 `mx + 1` 大，下标才能直接用数值',
                 '另一种写法（方法二）：第 k 次出现的 x 放进第 k 层，各层排序后拼接，`O(n log n + U)`'],
    ),
)

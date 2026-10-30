CONFIG = dict(
    num=2393, title='严格递增的子数组个数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 递增段长度求和',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def countSubarrays(self, nums):

        last = 10 ** 6 + 1
        cnt = 0
        res = 0
        for num in nums:
            if last >= num:
                res += cnt * (cnt + 1) // 2
                cnt = 0
            
            last = num
            cnt += 1

        res += cnt * (cnt + 1) // 2
        return res
''',
    call='Solution().countSubarrays([1,3,2,4,6,5,7])',
    expect=12,
    views=[
        dict(type='array', var='nums', label='nums（蓝格 = 当前数 num）', h=250, cell=110,
             color=lambda S, i, v: 'blue' if 'num' in S and i == S['nums'].index(S['num']) else None),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"当前递增段长度 `cnt` = =={S['cnt']}==，能贡献 `{S['cnt']}×{S['cnt']+1}÷2` = =={S['cnt']*(S['cnt']+1)//2}== 个子数组"
                           if 'cnt' in S else '')),
    ],
    watch=[('last', 'last', 'cyan'), ('cnt', 'cnt', 'blue'), ('res', 'res', 'green')],
    captions={
        'last = 10 ** 6': '`last` 记录上一个数，先设成比任何数都大的 `{last}`，保证第一个数一定被当作新段开头',
        5: '`cnt`：当前严格递增段的长度',
        'res = 0': '`res` 累计答案',
        'for num in nums': '看下一个数 `num` = {num}',
        'if last >= num': lambda S, B, r: (f'`last >= num`（{S.last} >= {S.num}）→ ==不再严格递增==，上一段到此为止' if B.last >= S.num
                                           else f'`last >= num`（{S.last} >= {S.num}）→ 不成立，仍严格递增，当前段继续变长'),
        'res += cnt * (cnt + 1) // 2': lambda S, B, r: ('`cnt = 0`：还没有累积的段，贡献 0 个' if B.cnt == 0 else
                                                        f'长为 `{B.cnt}` 的递增段共有 `{B.cnt}×{B.cnt+1}÷2` = =={B.cnt*(B.cnt+1)//2}== 个子数组 → `res` = {S.res}'),
        10: '段已结算，`cnt` 清零，从当前数重新数起',
        'last = num': '`last` 更新为 {last}',
        'cnt += 1': '当前数加入当前段：`cnt` = {cnt}',
        'return res': '最后一段在循环外结算完毕，答案 `{res}`',
    },
    cards=dict(
        one_liner='长为 k 的递增段，恰好贡献 k(k+1)/2 个递增子数组',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个整数数组 `nums`，数出==严格递增==的子数组个数（长度为 1 的也算）',
                 '示例：`[1,3,5,4,4,6]` → `10`',
                 '本视频：`[1,3,2,4,6,5,7]` 的递增段 `[1,3]`、`[2,4,6]`、`[5,7]` 贡献 3、6、3 → `12`'],
        quote='对于一段长度为k的严格递增子数组，从里面可以拆分出k个长度为1的子数组，k - 1个长度为2的子数组，...，1个长度为k的子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，把数组切成若干条尽量长的严格递增段',
              '每段长度 `k` 贡献 `1+2+…+k = (1+k)×k/2` 个子数组，累加即可',
              '遇到 `last >= num` 就结算上一段，`cnt` 从 1 重新数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '相等也要断开：条件是 `last >= num`，不是 `>`',
                 '循环结束后最后一段还没结算，要再加一次',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)

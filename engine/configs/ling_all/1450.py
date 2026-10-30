CONFIG = dict(
    num=1450, title='在既定时间做作业的学生人数', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='zip 遍历 + 区间判断', tags=[],
    code='''
class Solution:
    def busyStudent(self, startTime: List[int], endTime: List[int], queryTime: int) -> int:
        return sum(s <= queryTime <= e for s, e in zip(startTime, endTime))
''',
    call='Solution().busyStudent([9,8,7,6,5,4,3,2,1], [10,10,10,10,10,10,10,10,10], 5)',
    expect=5,
    views=[
        dict(type='array', var='startTime', label='startTime', h=170, index=False,
             color=lambda S, i, v: 'green' if v <= S['queryTime'] <= S['endTime'][i] else 'red'),
        dict(type='array', var='endTime', label='endTime', h=170,
             color=lambda S, i, v: 'green' if S['startTime'][i] <= S['queryTime'] <= v else 'red'),
        dict(type='text', fn=lambda S: f"`queryTime = {S['queryTime']}`：绿色 = 区间 `[start, end]` 包含它（正在做作业）", size=28),
    ],
    watch=['queryTime'],
    captions={
        'return sum': lambda S, B, r: f'逐个学生判断 `s <= {S.queryTime} <= e`，成立记 1，其余记 0，共 =={r}== 人',
    },
    cards=dict(
        after=[dict(heading='这一行在算什么', lines=['`zip(startTime, endTime)` 把第 `i` 名学生的 `(s, e)` 配成一对',
                  '`s <= queryTime <= e` 是 Python 链式比较，等价于 `s <= q and q <= e`',
                  '本例 `queryTime = 5`：`(9,10) (8,10) (7,10) (6,10)` 都还没开始，记 0',
                  '`(5,10) (4,10) (3,10) (2,10) (1,10)` 都包含 5，记 1，总和 `5`',
                  '`sum` 对 True/False 求和，True 当 1，所以不需要 if 和计数变量'])],
        one_liner='逐个学生判断：查询时间是否落在 [开始, 结束] 里',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`startTime[i]`、`endTime[i]` 是第 `i` 名学生写作业的起止时间',
                 '求 `queryTime` 时正在写作业的人数（区间两端都含）',
                 '本视频：9 名学生，`queryTime = 5` → `5`'],
        quote='遍历 startTime 和 endTime，如果满足 startTime[i] <= queryTime <= endTime[i]，则答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['Python 支持链式比较：`s <= queryTime <= e`',
              '`zip` 把开始、结束时间配成对，`sum` 对布尔值求和'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '区间是闭区间，`s == queryTime` 或 `e == queryTime` 也算',
                 '思考题：多次查询可用差分数组 + 前缀和，或排序后二分'],
    ),
)

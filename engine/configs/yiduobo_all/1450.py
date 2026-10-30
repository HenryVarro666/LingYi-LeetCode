CONFIG = dict(
    num=1450, title='在既定时间做作业的学生人数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟扫描 · 逐个判断', tags=[],
    code='''
class Solution(object):
    def busyStudent(self, startTime, endTime, queryTime):

        n = len(startTime)
        res = 0
        for index in range(n):
            if queryTime >= startTime[index] and queryTime <= endTime[index]:
                res += 1
        
        return res
''',
    call='Solution().busyStudent([9,8,7,6,5,4,3,2,1], [10,10,10,10,10,10,10,10,10], 5)',
    expect=5,
    views=[
        dict(type='array', var='startTime', label='startTime', h=170, index=False, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('index') else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='array', var='endTime', label='endTime', h=170,
             color=lambda S, i, v: 'blue' if i == S.get('index') else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='text', fn=lambda S: f"`queryTime = {S['queryTime']}`，已统计 `res = {S.get('res', 0)}` 人", size=28),
    ],
    watch=[('index', 'index', 'blue'), 'queryTime', ('res', 'res', 'green')],
    captions={
        'n = len': '学生人数 `n = {n}`',
        'res = 0': '`res` 统计正在写作业的人数',
        'for index in range': '看第 `{index}` 名学生',
        'if queryTime >=': lambda S, B, r: (f'`{S.queryTime} >= {S.startTime[S.index]}` 且 `{S.queryTime} <= {S.endTime[S.index]}`：已开始、还没结束 → ==成立==' if S.startTime[S.index] <= S.queryTime <= S.endTime[S.index] else f'`queryTime = {S.queryTime}` 不在 `[{S.startTime[S.index]}, {S.endTime[S.index]}]` 内 → 不成立'),
        'res += 1': '这名学生在写作业：`res` → {res}',
        'return res': '一趟扫描结束，共 `{res}` 人',
    },
    cards=dict(
        one_liner='一趟扫描，看查询时间是否在每个学生的起止区间里',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给出每名学生写作业的起止时间和一个查询时间',
                 '返回查询时间正在写作业的学生人数（区间两端含）',
                 '本视频：9 名学生，`queryTime = 5` → `5`'],
        quote='比较基础的题目，直接一趟扫描，对于当前学生判断queryTime是否处于其起始和结束时间之内即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标 `index` 对应同一名学生的 `startTime` 与 `endTime`',
              '`startTime <= queryTime <= endTime` 就把 `res` 加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '两端都是闭区间，用 `>=` 和 `<=`',
                 '对比灵神：同样的判断，灵神用 zip + sum 一行写完；yiduobo 用下标循环计数',
                 '原文已是 Python 3 可运行写法，无需改动'],
    ),
)

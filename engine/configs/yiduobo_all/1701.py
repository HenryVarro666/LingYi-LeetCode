CONFIG = dict(
    num=1701, title='平均等待时间', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按顺序模拟',
    tags=[],
    code='''
class Solution(object):
    def averageWaitingTime(self, customers):

        now = 0
        res = 0
        for arr, time in customers:
            if now > arr:
                res += now - arr + time
                now += time
            else:
                res += time
                now = arr + time

        return res * 1.0 / len(customers)
''',
    call='Solution().averageWaitingTime([[1,2],[2,5],[4,3]])',
    expect=5.0,
    views=[
        dict(type='table', var='customers', rows=lambda S: [f'顾客{i}' for i in range(len(S['customers']))],
             cols=['arr', 'time'], h=250,
             color=lambda S, i, j, v: ('blue' if S.get('arr') is not None and S['customers'][i][0] == S['arr'] and S['customers'][i][1] == S['time'] and i == S.get('_k', i) else None)),
        dict(type='text', size=28, fn=lambda S: (f"厨师空闲时间点 `now = {S['now']}`；已累计等待 `res = {S['res']}`" if 'now' in S and 'res' in S else '')),
        dict(type='text', size=28, fn=lambda S: (f"当前顾客 `arr = {S['arr']}`，`time = {S['time']}`" if 'arr' in S else '')),
    ],
    watch=[('now', 'now', 'blue'), ('arr', 'arr', 'cyan'), ('time', 'time', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now`：做完上一位顾客订单的时间点，开始是 `0`',
        'res = 0': '`res`：所有顾客等待时间之和',
        'for arr, time': '下一位顾客：`{arr}` 时刻到，订单要做 `{time}`',
        'if now > arr': lambda S, B, r: (
            f'`now = {S.now} > arr = {S.arr}`：厨师还在忙，顾客要先排队 =={S.now - S.arr}==' if S.now > S.arr
            else f'`now = {S.now} ≤ arr = {S.arr}`：厨师已经空闲，顾客一到就开做'),
        'res += now - arr': '等待 = 排队 `{now - arr}`（now − arr）+ 制作 `{time}` → `res` = {res}',
        'now += time': '做完这单的时间点：`now = now + time` = {now}',
        'res += time': '不用排队，只等制作 `{time}` → `res` = {res}',
        'now = arr + time': '从到达时刻开做：`now = {arr} + {time}` = {now}',
        'return res': '总等待 `{res}` ÷ `{len(customers)}` 位顾客 = =={res * 1.0 / len(customers)}==',
    },
    cards=dict(
        one_liner='按到达顺序模拟，只记录厨师什么时候有空',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['餐厅只有一位厨师，顾客按到达时间 `arr` 排好，订单要做 `time`',
                 '必须按顺序做，做完一单才开始下一单',
                 '求顾客平均等待时间。示例：`[[1,2],[2,5],[4,3]]` → `5.0`'],
        quote='使用一个变量now记录完成上一个顾客订单后的时间点，然后遍历每个顾客。',
        quote_src='—— yiduobo 题解原文',
        idea=['顾客到时 `now > arr`：要排队，等待 = `now - arr + time`，`now += time`',
              '顾客到时 `now < arr`：立刻开做，等待 = `time`，`now = arr + time`',
              '没有什么规划可做，老老实实模拟'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '两种情况的区别只在要不要先排队，以及 `now` 怎么更新',
                 '最后 `res * 1.0` 避免整数除法，得到小数平均值',
                 'now 等于 arr 时走 else，两种写法结果一样'],
    ),
)

CONFIG = dict(
    num=1491, title='去掉最低工资和最高工资后的工资平均值', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟扫描求最值与和', tags=[],
    code='''
class Solution(object):
    def average(self, salary):

        tot = mi = ma = salary[0]
        for s in salary[1:]:
            tot += s
            mi = min(mi, s)
            ma = max(ma, s)

        tot -= mi + ma
        return tot * 1.0 / (len(salary) - 2)
''',
    call='Solution().average([8000,9000,2000,3000,6000,1000])',
    expect=4750.0,
    views=[
        dict(type='array', var='salary', label='salary（扫描中，蓝 = 当前 s）', cell=100, h=200,
             color=lambda S, i, v: ('blue' if 's' in S and i == S['salary'].index(S['s']) and S['_line'] in (5, 6, 7, 8) else None)),
        dict(type='text', fn=lambda S: (f"目前 `tot = {S['tot']}`，`mi = {S['mi']}`，`ma = {S['ma']}`" if 'tot' in S else ''), h=70),
    ],
    watch=['tot', ('mi', 'mi', 'red'), ('ma', 'ma', 'orange')],
    captions={
        'tot = mi = ma': '三个变量都从 `salary[0] = {salary[0]}` 起步：和、最小、最大',
        'for s in': lambda S, B, r: ('已扫完所有工资，循环结束' if B.get('s') == S.get('s') and 's' in B else f"取下一个工资 `s = {S.s}`"),
        'tot += s': '顺便累加：`tot` = {tot}',
        'mi = min': '最小值 `mi = min({B.mi}, {s}) = {mi}`',
        'ma = max': '最大值 `ma = max({B.ma}, {s}) = {ma}`',
        'tot -= mi + ma': '扫描完毕：`tot` 减去最小 `{mi}` 和最大 `{ma}` → =={tot}==',
        'return': '除以人数减二 `{len(salary)} - 2 = {len(salary)-2}`，平均 =={ret}==',
    },
    cards=dict(
        one_liner='扫一趟，同时记下和、最小值、最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['去掉最低和最高工资后，求剩下员工工资的平均值',
                 '示例：`[4000,3000,1000,2000]` → `2500.0`',
                 '本视频：`[8000,9000,2000,3000,6000,1000]` → `4750.0`'],
        quote='一趟扫描，找出其中的最小值和最大值，并在这个过程中顺便求和。最后将这个和减去最小值和最大值，然后除以总数减二即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['以 `salary[0]` 初始化和、最小、最大', '从第二个数开始，一边累加一边更新最值', '最后 `tot` 减去最值，除以 `len − 2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`tot * 1.0` 保证是浮点除法',
                 '对比灵神：灵神直接调用 sum/min/max 三次，思路相同但更短'],
    ),
)

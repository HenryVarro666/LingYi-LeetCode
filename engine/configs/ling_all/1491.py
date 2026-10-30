CONFIG = dict(
    num=1491, title='去掉最低工资和最高工资后的工资平均值', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='总和减最值', tags=[],
    code='''
class Solution:
    def average(self, salary: List[int]) -> float:
        s = sum(salary)
        m = min(salary)
        M = max(salary)
        n = len(salary)
        return (s - m - M) / (n - 2)
''',
    call='Solution().average([8000,9000,2000,3000,6000,1000])',
    expect=4750.0,
    views=[
        dict(type='array', var='salary', label='salary', cell=100, h=200,
             color=lambda S, i, v: ('red' if 'm' in S and v == S['m'] else 'orange' if 'M' in S and v == S['M'] else None)),
        dict(type='text', fn=lambda S: (f"剩下 `n−2` 人：`({S['s']} − {S['m']} − {S['M']}) / ({S['n']} − 2)`" if 'n' in S else '去掉一个最低、一个最高，剩下 n−2 个人'), h=70),
    ],
    watch=[('s', 's', 'blue'), ('m', 'm', 'red'), ('M', 'M', 'orange'), 'n'],
    captions={
        's = sum': '先求全部工资之和 `s = {s}`',
        'm = min': '最低工资 `m = {m}`（红色）',
        'M = max': '最高工资 `M = {M}`（橙色）',
        'n = len': '人数 `n = {n}`',
        'return': '去掉两端后总和 `{s} − {m} − {M} = {s-m-M}`，人数 `{n} − 2 = {n-2}`，平均 =={ret}==',
    },
    cards=dict(
        after=[dict(heading='手算一遍', lines=['`[8000,9000,2000,3000,6000,1000]`', '`s = 29000`，`m = 1000`，`M = 9000`', '去掉两端：`29000 − 1000 − 9000 = 19000`', '剩 4 人：`19000 / 4 = 4750.0`'])],
        one_liner='总和减去最小、最大，再除以 n−2',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['去掉最低和最高工资后，求剩下员工工资的平均值（工资互不相同）',
                 '示例：`[4000,3000,1000,2000]` → `2500.0`',
                 '本视频：`[8000,9000,2000,3000,6000,1000]` → `4750.0`'],
        quote='设 salary 的元素和为 s，最小值为 m，最大值为 M，那么剩下 n-2 个人的工资之和为 s-m-M。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用真的删元素：总和直接减去 `m` 和 `M`', '剩余人数是 `n−2`，所以平均值 = `(s−m−M)/(n−2)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '题目保证工资唯一且 `n ≥ 3`，所以 `n−2 ≥ 1`，不会除零',
                 '要用 `/` 得到小数，别用 `//`'],
    ),
)

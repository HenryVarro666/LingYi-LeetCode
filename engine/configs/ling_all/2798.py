CONFIG = dict(
    num=2798, title='满足目标工作时长的员工数目', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='一行 sum 计数',
    tags=[],
    code='''
class Solution:
    def numberOfEmployeesWhoMetTarget(self, hours: List[int], target: int) -> int:
        return sum(h >= target for h in hours)
''',
    call='Solution().numberOfEmployeesWhoMetTarget([0,1,2,3,4,1,5], 2)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: f"目标 `target = {S['target']}`：工作时长 ≥ target 的员工记 1 分", size=28),
        dict(type='array', var='hours', label='hours（绿 = 达标）', cell=100,
             color=lambda S, i, v: 'green' if v >= S['target'] else 'pink'),
        dict(type='text', fn=lambda S: '`h >= target` 逐个判断：' + ' '.join('1' if h >= S['target'] else '0' for h in S['hours']) + '　→ 求和 = ==' + str(sum(h >= S['target'] for h in S['hours'])) + '==', size=28),
    ],
    watch=[('target', 'target', 'blue'), ('达标数', 'sum(h >= target for h in hours)', 'green')],
    captions={
        'return sum': '`h >= target` 是布尔值，`True` 当 1 `False` 当 0，==`sum` 就是满足条件的个数==：达标 {ret} 人',
    },
    cards=dict(
        one_liner='布尔值 True 当 1，sum 一下就是个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`hours[i]` 是第 `i` 名员工的工作小时数',
                 '统计工作 ==至少 target 小时== 的员工人数',
                 '示例：`hours = [0,1,2,3,4]`，`target = 2` → `3`'],
        quote='return sum(h >= target for h in hours)',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['逐个判断 `h >= target`，结果是 `True` 或 `False`',
              'Python 里 `True == 1`，把一串布尔值求和就是计数',
              '一行代码代替了“循环 + 计数器 + if”'],
        after=[dict(heading='把生成器展开看看', lines=[
            '`hours = [0,1,2,3,4,1,5]`，`target = 2`',
            '`h >= target` 依次得到 `0 0 1 1 1 0 1`（False 当 0，True 当 1）',
            '`sum` 把它们加起来：`0+0+1+1+1+0+1 = 4`',
            '生成器一边判断一边累加，不用额外建列表，空间 `O(1)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：是==至少==（≥），不要写成 `>`',
                 '同样的技巧：`sum(条件 for x in arr)` 可用于任何计数题'],
    ),
)

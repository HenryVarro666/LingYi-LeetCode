CONFIG = dict(
    num=2798, title='满足目标工作时长的员工数目', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历计数',
    tags=[],
    code='''
class Solution(object):
    def numberOfEmployeesWhoMetTarget(self, hours, target):

        res = 0
        for h in hours:
            if h >= target:
                res += 1
        
        return res
''',
    call='Solution().numberOfEmployeesWhoMetTarget([0,1,2,3,4,1,5], 2)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: f"目标 `target = {S['target']}`，已有 ==`{S['res']}`== 人达标" if 'res' in S else f"目标 `target = {S['target']}`", size=28),
        dict(type='array', var='hours', label='hours（绿 = 达标，粉 = 不达标）', cell=100,
             color=lambda S, i, v: 'green' if v >= S['target'] else 'pink'),
    ],
    watch=[('h', 'h', 'blue'), ('target', 'target'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计达标人数，从 0 开始',
        'for h in hours': '看下一位员工：`h = {h}` 小时',
        'if h >= target': lambda S, B, r: (f'`{S.h} >= {S.target}` → ==达标==' if S.h >= S.target else f'`{S.h} < {S.target}` → 不达标，跳过'),
        'res += 1': '达标人数 `res` → {res}',
        'return res': '遍历完，一共 `{res}` 人达标',
    },
    cards=dict(
        one_liner='一趟遍历，大于等于 target 就计数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`hours[i]` 是第 `i` 名员工的工作小时数',
                 '统计工作 ==至少 target 小时== 的员工人数',
                 '本视频：`[0,1,2,3,4,1,5]`，`target = 2` → `4`'],
        quote='比较入门的题目。直接一趟遍历，统计数组中大于等于target的数的个数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`res` 作计数器，初始为 0',
              '遍历每个 `h`，`h >= target` 就 `res += 1`',
              '遍历结束，`res` 就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：条件是 `>=`，恰好等于 target 也算达标',
                 '原文为 Python 2 风格，在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神用一行 `sum(h >= target ...)` 完成同样的计数'],
    ),
)

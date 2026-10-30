JOBS = [5, 2, 4]
WORKERS = [1, 7, 5]

CONFIG = dict(
    num=2323, title='完成所有工作的最短时间 II', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序后一一配对',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minimumTime(self, jobs, workers):

        res = 0
        for j, w in zip(sorted(jobs), sorted(workers)):
            t = j // w
            if j % w != 0:
                t += 1
            
            res = max(res, t)
        
        return res
''',
    call=f'Solution().minimumTime({JOBS}, {WORKERS})',
    expect=2,
    skip=['res = 0'],
    views=[
        dict(type='array', var='jobs', label='jobs[i]：第 i 项工作需要的天数（工作量）', cell=80, h=150),
        dict(type='array', var='workers', label='workers[i]：第 i 个工人每天能完成的量', cell=80, h=150),
        dict(type='array', var=lambda S: sorted(S['jobs']), label='sorted(jobs)：从小到大', cell=80, h=150,
             color=lambda S, i, v: 'blue' if 'j' in S and v == S['j'] else None),
        dict(type='array', var=lambda S: sorted(S['workers']), label='sorted(workers)：从小到大，按位置一一配对', cell=80, h=150,
             color=lambda S, i, v: 'pink' if 'w' in S and v == S['w'] else None),
        dict(type='text', fn=lambda S: (f"当前配对：工作量 `{S['j']}` ÷ 能力 `{S['w']}` → 需要 ==`{S['t']}` 天==" if 't' in S and 'j' in S and S['_line'] in (6, 7, 8, 10) else (f"当前配对：工作量 `{S['j']}` ÷ 能力 `{S['w']}`" if 'j' in S and S['_line'] == 5 else '')), size=28),
    ],
    watch=[('j', 'j', 'blue'), ('w', 'w', 'pink'), ('t', 't', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for j, w in zip': lambda S, B, r: ('全部配对完了，答案是其中最长的天数' if (S.get('j'), S.get('w')) == (B.get('j'), B.get('w'))
                                            else f'排序后按位置配对：第 k 小的工作给第 k 小的工人（越难越交给能干的），这一对是 `({S.j}, {S.w})`'),
        't = j // w': '工作量 `{j}`，每天做 `{w}`：整除得到 `t = {t}` 天',
        'if j % w != 0': lambda S, B, r: (f'`{B.j} % {B.w} = {B.j % B.w}` ≠ 0：最后一天没做完，要多一天（向上取整）' if B.j % B.w
                                          else f'`{B.j} % {B.w} = 0`：刚好做完，不用多一天'),
        't += 1': '向上取整：`t` 加一，变成 `{t}` 天',
        'res = max': '所有工人同时开工，总时间取决于最慢的那个：`res = max({B.res}, {t}) = {res}`',
        'return res': '返回最长的一个 `res = {res}` 天',
    },
    cards=dict(
        one_liner='最难的工作交给最能干的工人，排序后一一配对',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`jobs[i]` 是第 `i` 项工作需要的天数，`workers[j]` 是第 `j` 个工人每天能完成的工作量',
                 '每项工作恰好分给一个工人，每个工人恰好一项',
                 '一个工人一天完成 `workers[j]`，求完成全部工作的==最少天数==（最慢的人决定）',
                 '示例：`jobs=[5,2,4]`、`workers=[1,7,5]` → `2`'],
        quote='就应该将最难的工作分配给最能干的工人。……只需要将workers以及jobs都按小从大排序，然后一一对应分配，计算所需时间并取其中的最大值作为最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['交换论证：设 `workers[i] > workers[j]`、`x > y`',
              '大工作 `x` 给弱的 `j` 要 `x/workers[j]`，比原方案里任意一项都大，不会更优',
              '所以两边都升序一一配对，天数 = 向上取整的 `j / w`，取最大值'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：天数要向上取整，原文用 `j % w != 0` 补一天',
                 '原文为 Python 2 写法，`j / w` 的整数除法已改为 `j // w`',
                 '题意：按 yiduobo 文章与原题（力扣 2323）整理，示例为官方示例'],
    ),
)

CONFIG = dict(
    num=826, title='安排工作以达到最大收益', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='筛掉无用工作 + 工人从强到弱',
    tags=['灵神题单', '双序列配对', '难度分 1709'],
    code='''
class Solution(object):
    def maxProfitAssignment(self, difficulty, profit, worker):

        work = sorted(zip(difficulty, profit), key=lambda d:(d[0], -d[1]))
        valuable_work = [work[0]]
        for index in range(1, len(work)):
            if work[index][1] > valuable_work[-1][1]:
                valuable_work.append(work[index])
        
        now = len(valuable_work) - 1
        res = 0
        for worker_ability in sorted(worker, key=lambda d:-d):
            while now >= 0 and valuable_work[now][0] > worker_ability:
                now -= 1
            if now < 0:
                return res
            res += valuable_work[now][1]
        
        return res
''',
    call='Solution().maxProfitAssignment([2,4,6,8], [10,5,30,20], [5,3,9,7])',
    expect=80,
    views=[
        dict(type='array', var='work', label='work：按难度排序的 (难度, 收益)；紫色 = 当前 index', h=200, cell=120,
             fmt=lambda v: f'{v[0]},{v[1]}' if isinstance(v, tuple) else str(v),
             color=lambda S, i, v: 'purple' if 'index' in S and 'now' not in S and i == S['index'] else None),
        dict(type='array', var='valuable_work', label='valuable_work：难度、收益都严格递增；粉色 = 当前 now', h=200, cell=120,
             fmt=lambda v: f'{v[0]},{v[1]}' if isinstance(v, tuple) else str(v),
             color=lambda S, i, v: 'pink' if 'now' in S and i == S['now'] else None),
        dict(type='text', h=70, fn=lambda S: f"当前工人能力 `{S['worker_ability']}`，已赚 `res = ` =={S['res']}==" if 'worker_ability' in S else ''),
    ],
    watch=['worker_ability', ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'work = sorted': '按难度升序排序，难度相同时收益高的在前：`{work}`',
        'valuable_work = [': '第一份工作先留下',
        'for index in range': lambda S, B, r: ('工作都看完了，筛选结束' if B.get('index') == S['index'] else f"看第 `{S['index']}` 份工作 `{S['work'][S['index']]}`"),
        'if work[index][1] >': lambda S, B, r: (f'收益 `{S.work[S.index][1]}` > 已留下的最后一份 `{S.valuable_work[-1][1]}`：难度更高收益也更高，值得留' if S.work[S.index][1] > S.valuable_work[-1][1]
                                               else f'收益 `{S.work[S.index][1]}` <= `{S.valuable_work[-1][1]}`：更难却不更赚，没必要做 → 筛掉'),
        'valuable_work.append': '留下 `{work[index]}`：`valuable_work = {valuable_work}`',
        'now = len': '`now` 指向能做的难度最大的工作，先指向最后一份',
        'res = 0': '`res` 累计收益',
        'for worker_ability': '工人从强到弱：`worker_ability = {worker_ability}`',
        'while now >= 0': lambda S, B, r: (f'`now` 指向的难度 `{S.valuable_work[S.now][0]}` > 能力 `{S.worker_ability}`：做不了，`now` 往前退' if S.now >= 0 and S.valuable_work[S.now][0] > S.worker_ability
                                           else f'难度 `{S.valuable_work[S.now][0]}` <= 能力 `{S.worker_ability}`：做得了，停下'),
        'now -= 1': '`now` → {now}。工人越来越弱，`now` 只会单调递减',
        'if now < 0': lambda S, B, r: '所有工作他都做不了' if S.now < 0 else '`now >= 0`，他有活可做',
        'res += valuable_work': '工人拿走收益最高的可做工作：`res` → =={res}==',
        'return res': '总收益 `{res}`',
    },
    cards=dict(
        one_liner='先筛掉又难又不赚的工作，再让强工人往前指针只退不进',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n)`',
        problem=['工作有难度和收益，工人只能做难度不超过自己能力的工作',
                 '一份工作可被多人重复完成',
                 '示例：难度 `[2,4,6,8]`，收益 `[10,5,30,20]`，工人 `[5,3,9,7]` → `80`'],
        quote='若完成难度一样，那么收益较低的那一份显然没有必要去做。于是可以先筛除掉这些没必要去做的工作，那么剩下的工作必然满足难度越大，收益越大。',
        quote_src='—— yiduobo 题解原文',
        idea=['工作可重复做，每个人的最优解就是力所能及中收益最大的',
              '排序后筛一遍：只保留收益严格变大的工作',
              '工人从强到弱，`now` 从后往前退，整个匹配是 `O(n)`'],
        summary=['时间 `O(n log n + m log m)`，空间 `O(n)`',
                 '易错：难度相同要让收益高的排前面（`-d[1]`），筛选才不会漏',
                 '`now < 0` 时后面更弱的工人也都做不了，可直接 return',
                 '与灵神对比：yiduobo 先筛选再倒着匹配，灵神正着扫并维护 max'],
    ),
)

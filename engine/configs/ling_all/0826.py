CONFIG = dict(
    num=826, title='安排工作以达到最大收益', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 双指针维护最大收益',
    tags=['贪心与思维', '双序列配对', '难度分 1709'],
    code='''
class Solution:
    def maxProfitAssignment(self, difficulty: List[int], profit: List[int], worker: List[int]) -> int:
        jobs = sorted(zip(difficulty, profit))
        worker.sort()
        ans = j = max_profit = 0
        for w in worker:
            while j < len(jobs) and jobs[j][0] <= w:
                max_profit = max(max_profit, jobs[j][1])
                j += 1
            ans += max_profit
        return ans
''',
    call='Solution().maxProfitAssignment([2,4,6,8], [10,5,30,20], [5,3,9,7])',
    expect=80,
    views=[
        dict(type='array', var='jobs', label='jobs：(难度, 收益) 按难度排序；绿色 = 已扫描', h=240, cell=120,
             fmt=lambda v: f'{v[0]},{v[1]}' if isinstance(v, tuple) else str(v),
             pointers={'j': 'blue'},
             color=lambda S, i, v: 'green' if 'j' in S and i < S['j'] else None),
        dict(type='array', var='worker', label='worker（已排序）', h=170,
             color=lambda S, i, v: 'yellow' if 'w' in S and v == S['w'] and i == S['worker'].index(v) else None),
        dict(type='text', h=70, fn=lambda S: f"当前工人能力 `w = {S['w']}`，能做的最高收益 `max_profit = ` =={S['max_profit']}==" if 'w' in S else ''),
    ],
    watch=['w', ('j', 'j', 'blue'), ('max_profit', 'max_profit', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'jobs = sorted': '工作按难度排序：`jobs = {jobs}`',
        'worker.sort()': '工人按能力排序：`worker = {worker}`，能力更强的人能做前面所有工作',
        'ans = j': '`j` 是工作指针，`max_profit` 是目前能做的最高收益，`ans` 累计总收益',
        'for w in worker': '轮到工人 `w = {w}`',
        'while j < len': lambda S, B, r: (f'难度 `{S.jobs[S.j][0]} <= {S.w}`：这份工作他能做，继续看' if S.j < len(S.jobs) and S.jobs[S.j][0] <= S.w
                                          else '后面的工作他做不了（或已扫完）→ 不再前进'),
        'max_profit = max': '`max_profit = max({B.max_profit}, {jobs[j][1]}) = {max_profit}`：他能做的工作里收益最高的',
        'j += 1': '这份工作已看过，下个工人也一定能做它，不用回头：`j` → {j}',
        'ans += max_profit': '这个工人拿到 `{max_profit}`：`ans` → =={ans}==',
        'return ans': '所有工人都安排好，总收益 `{ans}`',
    },
    cards=dict(
        one_liner='工人越强能做的工作越多：指针只前进不回头',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n)`',
        problem=['工作有难度和收益，工人只能做难度不超过自己能力的工作',
                 '一份工作可被多人重复完成，每人最多做一份',
                 '示例：难度 `[2,4,6,8]`，收益 `[10,5,30,20]`，工人 `[5,3,9,7]` → `80`'],
        quote='第 i 个工人能做的工作，他右边的（worker 值更大的）工人也能做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['工人排序后，后一个工人只需要额外看 `worker[i] < difficulty[j] <= worker[i+1]` 的工作',
              '双指针 `j` 扫过所有难度不超过 `w` 的工作，顺手维护最大收益',
              '每个工人拿到的就是 `max_profit`，累加即可'],
        summary=['时间 `O(n log n + m log m)`，瓶颈在排序；空间 `O(n)`',
                 '易错：`max_profit` 要跨工人保留，不能每个工人重置',
                 '难度高的工作收益不一定高，所以要取 max，不能直接取最后一个',
                 '与 yiduobo 对比：灵神不筛工作，直接维护 max_profit'],
    ),
)

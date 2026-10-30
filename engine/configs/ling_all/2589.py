TASKS = [[1, 3, 2], [5, 6, 1], [2, 6, 4], [4, 8, 2]]


def _cur(S):
    """index (in sorted tasks) of the task being processed"""
    if 'start' not in S or 'tasks' not in S:
        return None
    for k, t in enumerate(S['tasks']):
        if t[0] == S['start'] and t[1] == S['end']:
            return k
    return None


def _run_color(S, i, v):
    if v:
        return 'green'
    return None


def _info(S):
    if 'start' not in S or 'd' not in S:
        return '按右端点排序：右边的任务要么和它不相交，要么只盖住它的==后缀=='
    run = S['run']
    have = sum(run[S['start']:S['end'] + 1])
    return (f'当前任务 `[{S["start"]}, {S["end"]}]` 还差 =={S["d"]}== 个时间点（`d`）；'
            f'区间内已有 `{have}` 个点在运行；电脑共开 `{sum(run)}` 秒')


def _cap_d(S, B, ret):
    done = sum(S.run[S.start:S.end + 1])
    return (f'任务 `[{S.start}, {S.end}]` 需 `{S.d + done}` 个点，区间里已有 `{done}` 个在运行（白嫖）→ 还差 ==d = {S.d}==')


CONFIG = dict(
    num=2589, title='完成所有任务的最少时间', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='按右端点排序 + 贪心 + 从右往左补点',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构', '难度分 2381'],
    code='''
class Solution:
    def findMinimumTime(self, tasks: List[List[int]]) -> int:
        tasks.sort(key=lambda t: t[1])
        run = [False] * (tasks[-1][1] + 1)
        for start, end, d in tasks:
            d -= sum(run[start: end + 1])  # 去掉运行中的时间点
            if d <= 0:  # 该任务已完成
                continue
            # 该任务尚未完成，从后往前找没有运行的时间点
            for i in range(end, start - 1, -1):
                if run[i]:  # 已运行
                    continue
                run[i] = True  # 运行
                d -= 1
                if d == 0:
                    break
        return sum(run)
''',
    call=f'Solution().findMinimumTime({TASKS})',
    expect=4,
    views=[
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='array', var='tasks', label='tasks（排序后：[start, end, duration]，蓝 = 当前任务）', h=170, cell=140, index=False,
             color=lambda S, i, v: 'blue' if i == _cur(S) else None),
        dict(type='array', var='run', label='run[t]：时间点 t 电脑是否在运行（绿 = 运行中，框 = 当前任务区间 [start, end]）', h=300, cell=80,
             pointers={'i': 'pink'}, window=('start', 'end'), color=_run_color),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'cyan'), ('d', 'd', 'orange'), ('i', 'i', 'pink'), ('共运行', 'sum(run)', 'green')],
    captions={
        'tasks.sort': '==按右端点从小到大排序==：这样右边的任务只会和当前任务重叠一个后缀',
        'run = [False]': '`run[t]` 记录时间点 `t` 是否已开机，一共 `{len(run)}` 格（下标 0 不用）',
        'd -= sum(run': _cap_d,
        'if d <= 0': lambda S, B, r: ('`d <= 0`：已运行的点够用了，这个任务不用再开机' if S.d <= 0 else f'`d = {S.d} > 0`：还差 {S.d} 个点，要新开机'),
        'for i in range': lambda S, B, r: ('从区间==最右端== `i = {}` 开始往左找没开机的点：开在后缀上，后面的任务更可能蹭到'.format(S.i) if S.i == S.end
                                           else f'往左一格：`i = {S.i}`'),
        'if run[i]': lambda S, B, r: (f'`run[{S.i}]` 已经在运行 → 跳过，继续往左' if S.run[S.i] else f'`run[{S.i}]` 是关着的 → 往下，把它打开'),
        'run[i] = True': '开机 ==时间点 {i}==：电脑总运行时间 `{sum(run)}`',
        'd -= 1': '这个任务又完成 1 个点，还差 `d = {d}`',
        'if d == 0': lambda S, B, r: ('`d == 0`：这个任务凑够了，`break`' if S.d == 0 else f'`d = {S.d}`：还没凑够，继续往左'),
        'return sum(run)': '`run` 里 `True` 的个数就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='按右端点排序，缺的时间点尽量开在区间最右边',
        complexity='时间 `O(n log n + nU)`，空间 `O(U)`',
        problem=['每个任务 `[start, end, duration]`：在闭区间里运行 `duration` 个整数时间点（不必连续）',
                 '电脑可同时跑任意多个任务，求电脑最少要开机多少个时间点',
                 '本视频：`[[1,3,2],[5,6,1],[2,6,4],[4,8,2]]` → `4`'],
        quote='排序后，对于区间 tasks[i] 来说，它右侧的任务区间要么和它没有交集，要么包含它的一部分后缀。……尽量把新增的时间点安排在区间 [start,end] 的后缀上，这样下一个区间就能统计到更多已运行的时间点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先按 `end` 排序：处理当前任务时，右边的任务只会盖到它的==后缀==',
              '当前任务先数区间里已开机的点；不够，再==从右往左==补开',
              '补在最右边，后面区间能蹭到的概率最大——这就是贪心的依据',
              '本视频演示方法一（暴力）；题解方法二是 lazy 线段树，方法三是栈 + 二分，都是把「数点、补点」做快'],
        summary=['时间 `O(n log n + nU)`，空间 `O(U)`，`U = max(end)`',
                 '一定要先按 ==右端点== 排序，按左端点不对',
                 '补点要从 `end` 往 `start` 找，且跳过已经开机的点',
                 '线段树 / 栈优化后可到 `O(n log n)`，数据范围 2000 时暴力也够用'],
    ),
)

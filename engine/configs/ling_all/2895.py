CONFIG = dict(
    num=2895, title='最小处理时间', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='交换论证 · 排序配对',
    tags=['灵神题单', '难度分 1352'],
    code='''
class Solution:
    def minProcessingTime(self, processorTime: List[int], tasks: List[int]) -> int:
        processorTime.sort()
        tasks.sort(reverse=True)
        return max(p + t for p, t in zip(processorTime, tasks[::4]))
''',
    call='Solution().minProcessingTime([8,10], [2,2,3,1,8,7,4,5])',
    expect=16,
    views=[
        dict(type='array', var='processorTime', h=150, label='processorTime（空闲时间）',
             color=lambda S, i, v: 'blue'),
        dict(type='array', var='tasks', h=170, label='tasks（耗时）',
             color=lambda S, i, v: 'orange' if i % 4 == 0 and S['_line'] >= 5 else None),
        dict(type='text', h=80, fn=lambda S: ('每颗处理器的完成时间 = 空闲时间 + 它 4 个任务里最大的（`tasks[4i]`）：' + '，'.join(f"`{p}+{t}`={p+t}" for p, t in zip(S['processorTime'], S['tasks'][::4]))) if S['_line'] >= 5 else ''),
    ],
    watch=['processorTime', 'tasks'],
    captions={
        'processorTime.sort()': '处理器按空闲时间从小到大排：`{processorTime}`。越早空闲的，越该接大任务',
        'tasks.sort': '任务按耗时从大到小排：`{tasks}`。每 4 个一组，每组的最大值就是下标 `4i` 那个',
        'return max': lambda S, B, ret: f"`tasks[::4]` = `{S.tasks[::4]}`，每颗处理器拿最大的那个：最晚完成者 `max(p+t)` = =={ret}==",
    },
    skip=[],
    cards=dict(
        one_liner='空闲早的处理器接最大的任务，排序后一一配对',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`n` 颗处理器各 4 个核，共 `4n` 个任务，每核做一个',
                 '给出各处理器最早空闲时间和各任务耗时，求全部做完的最短时间',
                 '示例：`[8,10]`，`[2,2,3,1,8,7,4,5]` → `16`'],
        quote='处理器的空闲时间越早，应当处理 tasks 越大的任务；处理器的空闲时间越晚，应当处理 tasks 越小的任务。',
        quote_src='—— 灵茶山艾府题解（交换论证）',
        idea=['一颗处理器的完成时间只看它 4 个任务里的==最大值==',
              '交换论证：`p1≤p2`、`t1≤t2`，把 `t2` 给 `p1` 不会更差',
              '所以 `processorTime` 升序、`tasks` 降序，答案是 `p[i] + t[4i]` 的最大值'],
        after=[dict(heading='交换论证', lines=['设空闲 `p1 ≤ p2`，两组最大任务 `t1 ≤ t2`', '`t1→p1, t2→p2`：完成时间 `p2+t2`', '`t1→p2, t2→p1`：`max(p1+t2, p2+t1) ≤ p2+t2`，不会更差', '所以早空闲的处理器配大任务，总能不变差'])],
        summary=['时间 `O(n log n)`，瓶颈在两次排序',
                 '`tasks[::4]` 取每组最大的任务（降序后每 4 个一组）',
                 '易错：处理器升序、任务降序，方向要相反',
                 '交换论证法：证明相邻（或任意两个）交换不会变差，就可以直接排序'],
    ),
)

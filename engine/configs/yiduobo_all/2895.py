CONFIG = dict(
    num=2895, title='最小处理时间', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='早空闲的处理器干最耗时的活',
    tags=['灵神题单', '难度分 1352'],
    code='''
class Solution(object):
    def minProcessingTime(self, processorTime, tasks):

        processorTime.sort()
        tasks.sort(reverse=True)
        return max([processorTime[index] + tasks[index * 4] for index in range(len(processorTime))])
''',
    call='Solution().minProcessingTime([8,10], [2,2,3,1,8,7,4,5])',
    expect=16,
    views=[
        dict(type='array', var='processorTime', h=150, label='processorTime（空闲时间）',
             color=lambda S, i, v: 'blue'),
        dict(type='array', var='tasks', h=170, label='tasks（耗时）',
             color=lambda S, i, v: ('orange' if i % 4 == 0 else 'cyan') if S['_line'] >= 6 else None),
        dict(type='text', h=80, fn=lambda S: ('第 index 颗处理器：`processorTime[index] + tasks[index*4]` = ' + '，'.join(f"`{S['processorTime'][i]}+{S['tasks'][i*4]}`={S['processorTime'][i]+S['tasks'][i*4]}" for i in range(len(S['processorTime'])))) if S['_line'] >= 6 else '橙色=每组最耗时的任务，青色=紧跟着的 3 个'),
    ],
    watch=['processorTime', 'tasks'],
    captions={
        'processorTime.sort()': '处理器按空闲时间从小到大排：`{processorTime}`',
        'tasks.sort': '任务按耗时从大到小排：`{tasks}`。最耗时的先交给最早空闲的处理器，它后面紧跟的 3 个也一起交给它，不会拉高它的完成时间',
        'return max': lambda S, B, ret: f"第 `index` 颗处理器拿 `tasks[index*4]` 起的 4 个，耗时取最大那个：各自 `processorTime[index] + tasks[index*4]` 取最大 = =={ret}==",
    },
    cards=dict(
        one_liner='最耗时的任务，交给最早空闲的处理器',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`n` 颗处理器、`4n` 个任务，每个核心做一个任务',
                 '求所有任务做完的最小时间',
                 '本视频：`[8,10]`，`[2,2,3,1,8,7,4,5]` → `16`'],
        quote='应该让最早空闲的处理器来处理最耗时的任务，而确定了最耗时的任务用哪个处理器来处理后，此时剩余任务中耗时最大的前三个任务就应该也交给这个处理器。',
        quote_src='—— yiduobo 题解原文',
        idea=['最耗时的任务无论如何都要有人做：给最早空闲的处理器',
              '紧跟着最大的 3 个也给它：不抬高它的完成时间，还把小任务留给别人',
              '处理器升序、任务降序，4 个一组分下去'],
        after=[dict(heading='为什么紧跟的 3 个也给它', lines=['最耗时任务 `T` 已经定了处理器 `P`，`P` 的完成时间至少 `P+T`', '再塞 3 个不超过 `T` 的任务进去，完成时间不变', '剩下的更小任务留给后面更晚空闲的处理器，更容易处理'])],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '完成时间 = `processorTime[index] + tasks[index*4]` 的最大值',
                 '易错：任务要降序（`reverse=True`），处理器要升序',
                 '对比灵神：灵神用交换论证严格证明，yiduobo 用直觉式的「先安排最大任务」逐步推'],
    ),
)

CONFIG = dict(
    num=3476, title='最大化任务分配的利润', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按技能分组 + 取 top k', tags=['贪心', '哈希表'],
    code='''
class Solution(object):
    def maxProfit(self, workers, tasks):
        
        task_dict = {}
        for skill, profit in tasks:
            if skill not in task_dict:
                task_dict[skill] = []
            task_dict[skill].append(profit)
        
        skill_cnt = Counter(workers)
        addtional = 0
        res = 0
        for skill in task_dict:
            task_dict[skill].sort(reverse=True)
            res += sum(task_dict[skill][:skill_cnt[skill]])
            if skill_cnt[skill] < len(task_dict[skill]):
                addtional = max(addtional, task_dict[skill][skill_cnt[skill]])
        
        return res + addtional
''',
    call='Solution().maxProfit([1,2,2,3], [[1,5],[2,4],[2,7],[2,3],[3,6],[4,9]])',
    expect=31,
    views=[
        dict(type='map', var='task_dict', label='task_dict：技能 → 收益列表', fmt=lambda k, v: f'技能 {k}: {v}', h=250),
        dict(type='map', var='skill_cnt', label='skill_cnt：技能 → 工人数', fmt=lambda k, v: f'技能 {k}: {v} 人', h=200),
        dict(type='text', h=60, fn=lambda S: f"`res = {S['res']}`，额外工人候选 `addtional = {S['addtional']}`" if 'addtional' in S and 'res' in S else ''),
    ],
    watch=['skill', ('res', 'res', 'green'), ('addtional', 'addtional', 'yellow')],
    captions={
        'task_dict = {}': '`task_dict` 按技能要求给任务分组，存各任务的收益',
        'for skill, profit': lambda S, B, r: ('所有任务都分好组了' if 'profit' in B and B.profit == S.profit else f'看任务 `[{S.skill}, {S.profit}]`：技能 {S.skill}，收益 {S.profit}'),
        'if skill not in': lambda S, B, r: ('这个技能还没出现过 → 先建空列表' if S.skill not in S.task_dict else '这个技能已有分组，直接追加'),
        '.append(profit)': '`task_dict[{skill}]` 追加收益 {profit}：{task_dict[skill]}',
        'skill_cnt = Counter': '统计每种技能等级的工人数：`{skill_cnt}`（技能必须恰好相等才能接任务）',
        'addtional = 0': '`addtional` 记录没被分配的任务里最大收益，留给额外工人',
        'for skill in task_dict': lambda S, B, r: ('每个技能都处理完了' if 'skill' in B and 'res' in B and B.get('_line') == S.get('_line') and B.skill == S.skill else f'处理技能 `{S.skill}`：有 `{S.skill_cnt[S.skill]}` 个工人'),
        '.sort(reverse=True)': '收益从大到小：`{task_dict[skill]}`，工人该挑最前面的',
        'res += sum': '技能 {skill} 有 `{skill_cnt[skill]}` 个工人 → 取最大的 {skill_cnt[skill]} 个任务求和，`res = {res}`',
        'if skill_cnt[skill] <': lambda S, B, r: (f'工人只有 {S.skill_cnt[S.skill]} 个，任务有 {len(S.task_dict[S.skill])} 个 → 有任务剩下' if S.skill_cnt[S.skill] < len(S.task_dict[S.skill]) else '工人够多，没有任务剩下'),
        'addtional = max': '剩下的任务里收益最大的是 `{task_dict[skill][skill_cnt[skill]]}` → `addtional = {addtional}`',
        'return res': '工人分配 `{res}` + 额外工人 `{addtional}` = =={res + addtional}==',
    },
    cards=dict(
        one_liner='技能必须恰好相等：分组取 top k，再让额外工人捡漏',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`workers[i]` 是工人技能；`tasks[j] = [技能要求, 收益]`',
                 '每个工人最多做一个任务，且技能必须==恰好等于==要求；另有一名万能工人可做任何任务',
                 '求最大总收益',
                 '本视频：`workers=[1,2,2,3]`，6 个任务'],
        quote='对于每种技能等级中的任务，显然应该选择收益最大的任务来执行，而可以执行的任务数量就是技能等级恰好为这个技能要求的工人数量，相当于一个top k问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['按技能给任务分组，每组独立：工人数 `k`，就取收益最大的 `k` 个',
              '每组没被选中的任务里，最大的一个是万能工人的候选',
              '万能工人只有一个，取所有组候选里的最大值即可'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '作者直接排序取前 `k` 个，没有用堆',
                 '`skill_cnt[skill]` 对没有工人的技能返回 0（`Counter`），该组任务全部剩下',
                 '变量名 `addtional` 是原文拼写'],
    ),
)

CONFIG = dict(
    num=1860, title='增长的内存泄露', difficulty='Medium', category='模拟',
    author='yiduobo', technique='直接模拟（至多约 5 万秒）', tags=[],
    code='''
class Solution(object):
    def memLeak(self, memory1, memory2):

        now = 1
        while now <= max(memory1, memory2):
            if memory1 < memory2:
                memory2 -= now
            else:
                memory1 -= now
            now += 1
        
        return [now, memory1, memory2]
''',
    call='Solution().memLeak(8, 11)',
    expect=[6, 0, 4],
    views=[
        dict(type='bars', var=lambda S: [S['memory1'], S['memory2']], label='两个内存条剩余（左 = 内存条 1，右 = 内存条 2）', h=330, vmax=11, index=False, cell=160),
        dict(type='text', fn=lambda S: f"第 `{S['now']}` 秒要分配 `{S['now']}` 位；较多的一条剩 `{max(S['memory1'], S['memory2'])}` 位" , size=30),
    ],
    watch=[('now', 'now', 'blue'), ('memory1', 'memory1', 'pink'), ('memory2', 'memory2', 'orange')],
    captions={
        'now = 1': '从第 1 秒开始，每秒要分配 `now` 位',
        'while now <= max': lambda S, B, r: (f'`now = {S.now} <= max({S.memory1}, {S.memory2}) = {max(S.memory1, S.memory2)}`：最大的那条还装得下 → 继续' if S.now <= max(S.memory1, S.memory2)
                                             else f'`now = {S.now} > max({S.memory1}, {S.memory2}) = {max(S.memory1, S.memory2)}`：两条都不够 → 崩溃'),
        'if memory1 < memory2': lambda S, B, r: (f'`{S.memory1} < {S.memory2}`：内存条 2 剩得更多 → 分给它' if S.memory1 < S.memory2
                                                 else f'`{S.memory1} >= {S.memory2}`：内存条 1 不少于 2（相等也给 1）→ 分给它'),
        'memory2 -= now': '内存条 2 被占 `{now}` 位，剩 =={memory2}==',
        'memory1 -= now': '内存条 1 被占 `{now}` 位，剩 =={memory1}==',
        'now += 1': '第 `{B.now}` 秒结束，进入第 `{now}` 秒',
        'return': '第 `{now}` 秒无法分配，剩余 `{memory1}` 和 `{memory2}` → =={ret}==',
    },
    cards=dict(
        one_liner='数据很大，但至多约 5 万秒就崩，直接模拟',
        complexity='时间 `O(sqrt(M))`，空间 `O(1)`',
        problem=['两个内存条剩余 `memory1`、`memory2`，第 `i` 秒要占 `i` 位',
                 '每次占「剩得较多」的那条，相等占第一条；都不够 `i` 就崩溃',
                 '示例：`memory1=8, memory2=11` → `[6,0,4]`'],
        quote='到了k时刻，一共消耗的内存就是(1 + k) * k / 2……也就是说在50000秒能必然会以为退出。那么在这里完全可以从第1秒开始模拟整个分配的过程。',
        quote_src='—— yiduobo 题解原文',
        idea=['`0 <= memory <= 2^31-1` 看着吓人，但第 k 秒累计消耗 `k(k+1)/2`',
              '两条各取最大值也撑不过约 5 万秒，所以循环次数很小',
              '每秒：比较两条的剩余，把 `now` 扣在较多的一条上'],
        summary=['时间 `O(sqrt(M))`，M 为内存上限，空间 `O(1)`',
                 '`memory1 < memory2` 才给 2，相等给 1：和题意「相等给第一条」一致',
                 '循环条件 `now <= max(...)`：较多的一条都装不下 `now`，另一条更不行',
                 '返回的 `now` 就是崩溃的那一秒，不是最后成功的一秒',
                 '原文为 Python 2 风格，但在 Python 3 下同样可运行，代码未改动'],
    ),
)

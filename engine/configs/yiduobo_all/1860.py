CONFIG = dict(
    num=1860, title='增长的内存泄露', difficulty='Medium', category='模拟',
    author='yiduobo', technique='直接模拟',
    tags=[],
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
        dict(type='bars', var=lambda S: [S['memory1'], S['memory2']], h=330, label='剩余内存 [memory1, memory2]', vmax=11),
        dict(type='text', size=30, h=80, fn=lambda S: f"第 `{S['now']}` 秒：memory1 = `{S['memory1']}`，memory2 = `{S['memory2']}`" if 'now' in S else ''),
    ],
    watch=['now', ('memory1', 'memory1', 'blue'), ('memory2', 'memory2', 'pink')],
    captions={
        'now = 1': '从第 1 秒开始',
        'while now <= max': lambda S, B, r: (f'`now = {S.now}` ≤ `max({S.memory1}, {S.memory2})`：还有内存放得下 → 继续' if S.now <= max(S.memory1, S.memory2)
                                             else f'`now = {S.now}` > `max({S.memory1}, {S.memory2})`：两条都放不下 → 崩溃'),
        'if memory1 < memory2': '`{memory1} < {memory2}` → {"memory2 更多，分给它" if memory1 < memory2 else "memory1 不少于 memory2，分给 memory1"}',
        'memory2 -= now': '第 {now} 秒：memory2 → =={memory2}==',
        'memory1 -= now': '第 {now} 秒：memory1 → =={memory1}==',
        'now += 1': '`now` → {now}',
        'return': '第 `{now}` 秒崩溃，剩余 `{memory1}`、`{memory2}`：`{ret}`',
    },
    cards=dict(
        one_liner='数据范围虽大，但最多只会跑约 5 万秒，直接模拟',
        complexity='时间 `O(sqrt(m))`，空间 `O(1)`',
        problem=['第 `i` 秒要分配 `i` 位内存，给剩余较多的那条（相等给第一条）',
                 '两条都不足 `i` 位时程序崩溃，返回 `[崩溃秒, 剩余1, 剩余2]`',
                 '示例：`memory1 = 8, memory2 = 11` → `[6, 0, 4]`'],
        quote='题目的数据规模看上去很大，但是注意到每一时刻消耗的内存是逐步增大的，那么到了k时刻，一共消耗的内存就是(1 + k) * k / 2。',
        quote_src='—— yiduobo 题解原文',
        idea=['两条内存最大都是 `2^31 - 1`，由 `(1+k)k/2 >= 2^32 - 2` 得 `k < 50000`',
              '所以从第 1 秒开始一秒一秒模拟，直到没有内存放得下为止'],
        summary=['时间约 `O(sqrt(m))`（k 不超过 5 万），空间 `O(1)`',
                 '`memory1 < memory2` 才分给 2，相等时分给 1',
                 '循环条件看较大的那条：`now <= max(...)`',
                 '对比灵神：思路相同，yiduobo 额外用等差数列求和证明了循环次数'],
    ),
)

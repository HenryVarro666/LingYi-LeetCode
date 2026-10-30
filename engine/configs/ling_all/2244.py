CONFIG = dict(
    num=2244, title='完成所有任务需要的最少轮数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='计数 + 向上取整',
    tags=['贪心与思维', '数学贪心', '难度分 1372'],
    code='''
class Solution:
    def minimumRounds(self, tasks: List[int]) -> int:
        cnt = Counter(tasks)
        if 1 in cnt.values():
            return -1
        return sum((c + 2) // 3 for c in cnt.values())
''',
    call='Solution().minimumRounds([2,2,3,3,2,4,4,4,4,4])',
    expect=4,
    views=[
        dict(type='array', var='tasks', label='tasks（任务难度）', h=200),
        dict(type='map', var='cnt', label='cnt：每种难度的任务数', fmt=lambda k, v: f'难度{k}: {v}个', h=280),
        dict(type='text', h=120, size=30, fn=lambda S: ' + '.join(f"ceil({c}/3)={(c+2)//3}" for c in S['cnt'].values()) + f" = =={sum((c+2)//3 for c in S['cnt'].values())}==" if 'cnt' in S else ''),
    ],
    watch=[('cnt', 'dict(cnt)', 'cyan')],
    captions={
        'cnt = Counter': '先统计每种难度的任务数：`{dict(cnt)}`。不同难度互不相干，可以分开算',
        'if 1 in cnt.values()': lambda S, B, r: ('有难度只出现 1 次：每轮至少完成 2 个，永远凑不出 → 直接 -1' if 1 in S.cnt.values()
                                              else '没有只出现 1 次的难度，每种都能完成 → 继续'),
        'return -1': '某种难度只有 1 个任务，无法完成，返回 `-1`',
        'return sum': lambda S, B, r: f"每种 c 个任务最少 `ceil(c/3) = (c+2)//3` 轮：{' + '.join(str((c+2)//3) for c in S.cnt.values())} = =={r}==",
    },
    cards=dict(
    before=[dict(heading='先看一个例子', lines=['难度 `4` 有 5 个：`3 + 2 = 5`，需要 2 轮', '难度 `2` 有 3 个：1 轮；难度 `3` 有 2 个：1 轮', '合计 `1 + 1 + 2 = 4` 轮'])],
    after=[dict(heading='为什么余 1 也不用多算', lines=['`c = 4`：不能 3+1，但 `2 + 2` 两轮，`ceil(4/3) = 2`', '`c = 7`：`3 + 2 + 2` 三轮，`ceil(7/3) = 3`', '`c = 3k+1`（k≥1）：把一个 3 拆成两个 2，总数 `k+1` 轮', '`c = 3k+2`：多一轮装 2 个，同样 `k+1` 轮']),
           dict(heading='另一个写法与思考题', lines=['公式 `(c+2)//3` 就是向上取整，不必分三种情况写代码', '思考题：每轮可完成 a 或 b 个，哪些 c 凑不出来？', '提示：参考 小凯的疑惑（NOIP2017）'])],
        one_liner='c 个同难度任务，尽量三个一轮：最少 ceil(c/3) 轮',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每轮可完成 2 个或 3 个==相同难度==的任务，求完成全部任务的最少轮数，做不到返回 `-1`',
                 '示例：`[2,2,3,3,2,4,4,4,4,4]` → `4`'],
        quote='贪心地想，尽量多地使用「减少 3」，可以让轮数尽量少。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不同难度互不影响，用哈希表数出每种难度有 `c` 个',
              '`c = 1` 无解；`c = 3k` 用 k 轮；`c = 3k+1` 把一个 3 换成两个 2；`c = 3k+2` 加一轮 2',
              '三种情况合起来都是 `ceil(c/3) = (c+2)//3`，累加即可'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`c = 1` 必须先判无解，再用公式（公式对 c = 1 会给出 1）',
                 '`(c+2)//3` 就是向上取整 `c/3`',
                 '同类题：2870 使数组为空的最少操作次数（完全相同）；思考题：每轮 a 或 b 个'],
    ),
)

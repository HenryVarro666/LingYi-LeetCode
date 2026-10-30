def _txt(S):
    if 'level' not in S['_inner']:
        return '从首位 1–9 出发，每次在末尾接上「末位 ± 1」，==位数最多 10 位=='
    I = S['_inner']
    now, level = I['now'], I['level']
    inr = S['low'] <= now <= S['high']
    tag = '落在 [low, high] → ==收集==' if inr else ('超出 high，但搜索不会剪枝' if now > S['high'] else '还没到 low')
    return f'`now = {now}`（第 {level} 位）：{tag}'


CONFIG = dict(
    num=1215, title='步进数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='逐位搜索回溯',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countSteppingNumbers(self, low, high):

        global res
        res = []
        if low == 0:
            res.append(0)
        

        def dfs(now, level):
            if low <= now <= high:
                res.append(now)
            
            if level == 10:
                return
            
            last = now % 10
            if last > 0:
                dfs(now * 10 + last - 1, level + 1)
            if last < 9:
                dfs(now * 10 + last + 1, level + 1)

        for first in range(1, 10):
            dfs(first, 1)
        
        return sorted(res)
''',
    call='Solution().countSteppingNumbers(10, 21)',
    expect=[10, 12, 21],
    views=[
        dict(type='text', h=90, size=30, fn=_txt),
        dict(type='calls', h=520),
        dict(type='text', h=120, size=30, fn=lambda S: f"目标范围 `[{S['low']}, {S['high']}]`；步进数 = ==相邻两位相差 1==" if 'low' in S else ''),
    ],
    watch=['low', 'high', ('now', 'now', 'blue'), ('level', 'level', 'orange'), ('last', 'last', 'pink')],
    max_steps=62, max_events=80000,
    captions={
        'global res': '`res` 是全局列表，递归里的 `dfs` 也能往里加',
        'res = []': '`res` 收集所有落在 `[low, high]` 的步进数',
        'if low == 0': '`low = {low}`：只有 `low` 为 0 才需要把 `0` 单独加进去',
        'for first in range': '最高位只能取 1 到 9：`first = {first}`（不能是 0）',
        'if low <= now <= high': lambda S, B, r: (f'`{S.low} <= {S.now} <= {S.high}` 成立 → 收集' if S.low <= S.now <= S.high else f'`{S.low} <= {S.now} <= {S.high}` 不成立 → 不收集'),
        'res.append(now)': '`{now}` 是步进数且在范围内 → 加入 `res`',
        'if level == 10': lambda S, B, r: ('`level = 10`：已经 10 位，题目上限就是 10 位 → ==返回==' if S.level == 10 else f'`level = {S.level} < 10`：还可以继续接下一位'),
        'last = now % 10': '末位 `last = {now} % 10 = {last}`，下一位只能是 `last-1` 或 `last+1`',
        'if last > 0': lambda S, B, r: (f'`last = {S.last} > 0` → 可以接 `{S.last - 1}`' if S.last > 0 else '`last = 0` → 没法再减，跳过'),
        'if last < 9': lambda S, B, r: (f'`last = {S.last} < 9` → 可以接 `{S.last + 1}`' if S.last < 9 else '`last = 9` → 没法再加，跳过'),
        'dfs(now * 10 + last - 1': '接上 `{B.last - 1}`：新数 `{B.now * 10 + B.last - 1}`，进入下一层',
        'dfs(now * 10 + last + 1': '接上 `{B.last + 1}`：新数 `{B.now * 10 + B.last + 1}`，进入下一层',
        'dfs(first, 1)': '以 `{first}` 开头，从第 1 位开始搜',
        'return sorted': '搜索全部结束，排序后返回结果（`res` 里是 {ret}）',
    },
    cards=dict(
        one_liner='每位只有两种选择，直接从最高位向后搜索回溯',
        complexity='时间 `O(9·2^10)`，空间 `O(10)` 递归深度',
        problem=['步进数：==相邻两位数字之差恰好为 1==，如 `123`、`321`',
                 '给定 `low` 和 `high`（最多 10 位），按序返回范围内所有步进数',
                 '本视频：`low = 10, high = 21` → `[10, 12, 21]`'],
        quote='看上去应该是数位动态规划的问题，不过注意到low和high最多只有10位，而每一位在上一轮的基础上最多只有两种可行的选择，因此可以直接从最高位开始向后进行搜索回溯。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now, level)`：`now` 已有 `level` 位，末位 `last`',
              '下一位只能是 `last - 1`（`last > 0`）或 `last + 1`（`last < 9`）',
              '每个 `now` 都检查是否在 `[low, high]`；到 10 位就停',
              '视频只演示开头几步，后面的分支同理'],
        summary=['最多 `9 × 2^9` 个数，规模很小，不必写数位 DP',
                 '最高位只能取 1 到 9，所以外层 `range(1, 10)`',
                 '`low == 0` 时 `0` 是步进数，要单独加入',
                 '最后 `sorted(res)`：搜索顺序不是从小到大',
                 '本题代码本来就是 Python 3 写法，未做修改'],
    ),
)

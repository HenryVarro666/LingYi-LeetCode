def _txt(S):
    if 'tot' not in S:
        return ''
    tot = S['tot']
    if 'now' in S and 'index' in S and S['now'] is not None and S['_line'] >= 7:
        now = S['now']
        return f'全部得分 `tot = {tot}`　｜　`now = {now}` vs 剩下 `{tot - now}`　→　{"==Alice 更多==" if now > tot - now else "还不够"}'
    return f'全部关卡得分之和 `tot = {tot}`'


CONFIG = dict(
    num=3096, title='得到更多分数的最少关卡数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='总分固定 · 一趟前缀',
    tags=['前后缀分解'],
    code='''
class Solution(object):
    def minimumLevels(self, possible):

        tot = sum(possible) * 2 - len(possible)
        now = 0
        for index in range(len(possible) - 1):
            if possible[index] == 1:
                now += 1
            else:
                now -= 1
            
            if now > tot - now:
                return index + 1
        
        return -1
''',
    call='Solution().minimumLevels([1,0,1,1,1])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='possible', pointers={'index': 'blue'}, window=('0', 'index'), h=250,
             label='possible（1 = 简单，0 = 困难）',
             dim=lambda S, i, v: 'index' in S and i > S['index'],
             color=lambda S, i, v: ('green' if v else 'pink') if 'index' in S and i <= S['index'] else None),
    ],
    watch=['tot', 'now', ('index', 'index', 'blue')],
    max_steps=60,
    captions={
        'tot = sum': '设简单关 `x` 个，总分 = `x − (n − x)` = `x + x − n`，这里 `tot = {tot}`；==总分是固定的==',
        'now = 0': '`now`：Alice 已通过前缀的得分',
        'for index in range': '枚举 Alice 打到第 `{index}` 关；`range(n - 1)` 给 Bob 留下最后一关',
        'if possible[index] == 1': '`possible[{index}] = {possible[index]}` → {"简单关，+1" if possible[index] == 1 else "困难关，−1"}',
        'now += 1': '`now` +1 → =={now}==',
        'now -= 1': '`now` −1 → =={now}==',
        'if now > tot - now': '`now = {now}`，Bob 得 `tot − now = {tot - now}` → {"==Alice 更多==" if now > tot - now else "还没超过，继续多打一关"}',
        'return index + 1': '第一次出现 Alice 更多 → 通过关卡数 `{index + 1}`',
        'return -1': '没有任何前缀满足 → `-1`',
    },
    cards=dict(
        one_liner='总分固定，Bob 的得分 = 总分 − 前缀得分',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['简单关得 1 分，困难关扣 1 分；Alice 打一个前缀，Bob 打剩下的',
                 '求使 Alice 严格多于 Bob 的最短前缀长度，两人至少各打 1 关',
                 '示例：`[1,0,1,0]` → `1`；本视频：`[1,0,1,1,1]` → `4`'],
        quote='由于关卡的总得分是固定的，不妨设简单关卡一共有x个，那么困难关卡就是n - x个，因此通过所有关卡的分数之和就是x + x - n。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算好全部得分 `tot = x + x − n`',
              '一趟遍历累加 `now`，Bob 的分就是 `tot − now`',
              '第一次 `now > tot − now`，当前关卡数就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`range(len(possible) - 1)`：Bob 至少要打一关',
                 '这里的 `tot` 是真实总分（没有乘 2），所以和 `tot − now` 直接比',
                 '原文就是 Python 3 可运行写法，未做修改'],
    ),
)

def _top(S):
    if 'p' not in S:
        return ''
    b, r = S['boardingCost'], S['runningCost']
    p = S['p']
    if 'tmp' in S:
        return f"收尾：剩下 `p = {p}` 人，每轮至多 4 人，要再转 `p // 4 = {p // 4}` 轮，余 `{p % 4}` 人"
    return f"等待游客 `p = {p}`；满 4 人一轮赚 `{b}×4 − {r} = {b * 4 - r}`，不满 4 人赚 `{b}×p − {r}`"


def _prof(S):
    if 'now' not in S:
        return ''
    return f"累计收益 `now = {S['now']}`，历史最大 `max_v = {S['max_v']}`，对应转了 `res = {S['res']}` 轮"


CONFIG = dict(
    num=1599, title='经营摩天轮的最大利润', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 逐轮累计收益',
    tags=[],
    code='''
class Solution(object):
    def minOperationsMaxProfit(self, customers, boardingCost, runningCost):

        if boardingCost * 4 <= runningCost:
            return -1

        max_v = 0
        res = -1
        now = 0
        p = 0
        for index, c in enumerate(customers):
            p += c
            if p < 4:
                now += boardingCost * p - runningCost
                p = 0
            else:
                now += boardingCost * 4 - runningCost
                p -= 4
            if now > max_v:
                max_v = now
                res = index + 1

        tmp = len(customers)
        if p > 0:
            now += p // 4 * (boardingCost * 4 - runningCost)
            tmp += p // 4
            if boardingCost * (p % 4) > runningCost:
                now += boardingCost * (p % 4) - runningCost
                tmp += 1
        
        if now > max_v:
            res = tmp
        
        return res
''',
    call='Solution().minOperationsMaxProfit([8, 3], 5, 6)',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='array', var='customers', label='customers[i]：第 i 次转动前新来的游客', cell=130,
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='text', fn=_prof, size=24),
    ],
    watch=[('p', 'p', 'blue'), ('now', 'now', 'green'), ('max_v', 'max_v', 'orange'), ('res', 'res', 'pink')],
    captions={
        'if boardingCost * 4 <= runningCost': lambda S, B, ret: (
            f'满载一轮只赚 `{S.boardingCost}×4 = {S.boardingCost * 4}`，转一次成本 `{S.runningCost}` → 满载都亏，==不开业=='
            if S.boardingCost * 4 <= S.runningCost
            else f'满载一轮赚 `{S.boardingCost * 4}` > 成本 `{S.runningCost}`：有利可图，往下模拟'),
        'return -1': '每轮最多 4 人还抵不上成本 → 返回 `-1`',
        'max_v = 0': '`max_v` 记录历史最大收益，初始 0（亏本不算）',
        'res = -1': '`res` 记录取到最大收益时转的轮数，初始 `-1`',
        'now = 0': '`now` 是当前累计收益',
        'for index, c in enumerate': '第 `{index + 1}` 轮：新来 `c = {c}` 个游客',
        'p += c': '排队游客 `p` → =={p}==',
        'if p < 4': lambda S, B, ret: (f'`p = {S.p} < 4`：这一轮能把所有人送上去' if S.p < 4
                                       else f'`p = {S.p} >= 4`：只能上 4 个人，其余继续等'),
        'now += boardingCost * p': '不满 4 人：赚 `{boardingCost}×{B.p} − {runningCost}`，`now` → =={now}==',
        'p = 0': lambda S, B, ret: ('`p` 是还在排队的游客数' if S['_line'] < 11 else '所有人都上去了，`p` 清零'),
        'now += boardingCost * 4': '满 4 人：赚 `{boardingCost}×4 − {runningCost}`，`now` → =={now}==',
        'p -= 4': '送走 4 人，还剩 `p = {p}`',
        'if now > max_v': lambda S, B, ret: ((f'`now = {S.now} > max_v = {S.max_v}`：刷新最大收益' if S.now > S.max_v
                                              else f'`now = {S.now}` 没超过 `max_v = {S.max_v}`，不更新') if S['_line'] < 23 else
                                             (f'收尾后 `now = {S.now} > max_v = {S.max_v}`：最大收益出现在收尾阶段' if S.now > S.max_v
                                              else f'`now = {S.now}` 没超过 `max_v`，答案不变')),
        'max_v = now': '`max_v` → {max_v}',
        'res = index + 1': '最大收益暂时对应转了 `index + 1 =` =={res}== 轮',
        'tmp = len(customers)': '到访游客处理完，已转 `tmp = {tmp}` 轮；`tmp` 记录收尾后的总轮数',
        'if p > 0': lambda S, B, ret: (f'还有 `p = {S.p}` 人在排队，继续转' if S.p > 0 else '没人排队了，不用再转'),
        'now += p // 4': '再转 `p // 4 = {p // 4}` 轮，每轮满载赚 `{boardingCost * 4 - runningCost}`，`now` → =={now}==',
        'tmp += p // 4': '总轮数 `tmp` → {tmp}',
        'if boardingCost * (p % 4)': lambda S, B, ret: (
            f'余 `{S.p % 4}` 人：赚 `{S.boardingCost}×{S.p % 4} = {S.boardingCost * (S.p % 4)}` ' +
            (f'> 成本 `{S.runningCost}`，==值得再转一轮==' if S.boardingCost * (S.p % 4) > S.runningCost else f'<= 成本 `{S.runningCost}`，不转')),
        'now += boardingCost * (p % 4)': '再转一轮送走余下的人：`now` → =={now}==',
        'tmp += 1': '总轮数 `tmp` → {tmp}',
        'res = tmp': '`res = tmp = {res}`：转满 `{res}` 轮时收益最大',
        'return res': '返回最少轮数 `{res}`',
    },
    cards=dict(
        one_liner='逐轮模拟，每轮最多上 4 人，记下收益最高的那一轮',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['摩天轮有 4 个座位，转一圈费用 `runningCost`，每个上车游客付 `boardingCost`',
                 '`customers[i]` 是第 `i` 次转动前到达的新游客；==游客可以不下车就付票价==（转动后不管他们下没下）',
                 '求利润最大时的最少转动次数，利润始终非正则返回 `-1`',
                 '本视频：`customers=[8,3]`，`boardingCost=5`，`runningCost=6` → `3`'],
        quote='若每次收4个人的门票钱还抵不上转一次摩天轮的钱，那么就没有开业的必要了，直接返回-1。接下来则可以进行模拟。对于每一时刻，维护当前剩余游客的数目p。',
        quote_src='—— yiduobo 题解原文',
        idea=['先特判：`boardingCost*4 <= runningCost`，满载都亏就不开业',
              '每轮上 `min(p, 4)` 个人，收益加 `boardingCost*上车人数 − runningCost`，每轮后更新最大收益和轮数',
              '游客来完后若还有人排队：先成批转 `p // 4` 轮，余下 `p % 4` 人只在赚钱时才多转一轮'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只在收益==严格大于==历史最大时更新，这样才是最少轮数',
                 '易错：余下 `p % 4` 人要比较 `boardingCost*(p%4)` 与 `runningCost`，亏本就不转',
                 '`max_v` 从 0 起，利润始终不为正时 `res` 保持 `-1`',
                 '原文为 Python 2 写法，整数除法 `p / 4` 已改为 `p // 4`'],
    ),
)

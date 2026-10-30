CONFIG = dict(
    num=948, title='令牌放置', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 双指针贪心',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def bagOfTokensScore(self, tokens, P):

        sorted_tokens = sorted(tokens)

        l = 0
        r = len(sorted_tokens) - 1
        res = 0
        now = 0
        while l <= r:
            while l <= r and sorted_tokens[l] <= P:
                now += 1
                P -= sorted_tokens[l]
                l += 1

            res = max(res, now)
            if r > l and now > 0:
                P += sorted_tokens[r]
                r -= 1
                now -= 1
            else:
                break

        return res
''',
    call='Solution().bagOfTokensScore([300,100,400,200], 200)',
    expect=2,
    views=[
        dict(type='array', var='sorted_tokens', label='排序后的令牌（左：花能量得分；右：花分数换能量）', h=190, cell=90,
             pointers={'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: None,
             dim=lambda S, i, v: 'l' in S and 'r' in S and (i < S['l'] or i > S['r'])),
        dict(type='text', size=28, h=60, fn=lambda S: f"能量 `P = {S['P']}`，当前分数 `now = {S['now']}`，历史最高 `res = {S['res']}`" if 'now' in S and 'res' in S else ''),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('P', 'P', 'yellow'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'sorted_tokens = sorted': '令牌得分等价，所以先按能量从小到大排序：`{sorted_tokens}`',
        'l = 0': '`l` 指向最便宜的令牌',
        'r = len': '`r` 指向最贵的令牌（用来换能量）',
        'while l <= r:': lambda S, B, r: ('还有令牌没用，继续' if S.l <= S.r else '令牌用完，结束'),
        'while l <= r and sorted_tokens[l] <= P': lambda S, B, r: (f'`{S.sorted_tokens[S.l]} <= P = {S.P}`：买得起最便宜的，==能买就买==' if S.l <= S.r and S.sorted_tokens[S.l] <= S.P else '买不起最便宜的了，退出'),
        'now += 1': '花能量得 1 分：`now` = {now}',
        'P -= sorted_tokens[l]': '能量扣掉 `{sorted_tokens[l]}`：`P` = {P}',
        'l += 1': '最便宜的用掉了，`l` → {l}',
        'res = max': '此时分数是一个候选：`res = max({B.res}, {now})` = =={res}==',
        'if r > l and now > 0': lambda S, B, r: (f'还有别的令牌（`r > l`）且手里有分数 → ==花 1 分换最贵令牌的能量==' if S.r > S.l and S.now > 0 else '没令牌可换或没分数可花，再换也没意义 → 结束'),
        'P += sorted_tokens[r]': '换到最贵令牌的能量 `{sorted_tokens[r]}`：`P` = {P}（换大的最划算）',
        'r -= 1': '最贵的用掉了，`r` → {r}',
        'now -= 1': '花掉 1 分：`now` = {now}',
        'break': '无法继续，跳出循环',
        'return res': '最高分 `{ret}`',
    },
    cards=dict(
        one_liner='便宜的买分，贵的换能量，两头往中间夹',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['初始能量 `P`、分数 0。令牌 `t`：能量 `>= t` 可花 `t` 能量得 1 分；分数 `>= 1` 可花 1 分得 `t` 能量',
                 '每个令牌最多用一次，求能得到的最大分数',
                 '示例：`[300,100,400,200]`, `P=200` → `2`'],
        quote='尽量多的选取头部的令牌直到能量不足，此时可以用现有的令牌数去更新答案；此时应当使用一个令牌来换取最大的能量，也就是从排序后的另一侧开始进行交换。',
        quote_src='—— yiduobo 题解原文',
        idea=['得分时令牌等价，当然选能量最小的',
              '换能量时当然换最大的那一块',
              '所以排序后左指针买分、右指针换能量，直到不能再继续'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：先 `res = max(res, now)` 再换能量，因为换完分数会变少',
                 '`r > l` 才能换：最后一个令牌换能量没有意义',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)

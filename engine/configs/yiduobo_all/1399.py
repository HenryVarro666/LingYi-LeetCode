def _info(S):
    if 'cnt' in S:
        return f'在各组大小里找最大值：`cnt = {S["cnt"]}`，目前最大 `now_cnt = {S["now_cnt"]}`，计数 `res = {S["res"]}`'
    if 'now' not in S:
        return '对每个数求数位和 `s`，用字典 `s_dict` 记「数位和 → 有几个数」'
    return f'数 `{S["index"]}` 的数位和：还剩 `now = {S["now"]}`，已累加 `s = {S["s"]}`'


def _grp(S):
    d = S.get('s_dict')
    if not d:
        return ''
    return f'`{len(d)}` 个组，目前最大的组有 `{max(d.values())}` 个数'


CONFIG = dict(
    num=1399, title='统计最大组的数目', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='哈希表统计数位和',
    tags=['灵神题单', '数位 DP'],
    code='''
class Solution(object):
    def countLargestGroup(self, n):

        s_dict = {}
        for index in range(1, n + 1):
            now = index
            s = 0
            while now:
                s += now % 10
                now //= 10

            s_dict[s] = s_dict.get(s, 0) + 1
        
        res = 0
        now_cnt = 0
        for cnt in s_dict.values():
            if cnt > now_cnt:
                res = 1
                now_cnt = cnt
            elif cnt == now_cnt:
                res += 1
            
        return res
''',
    call='Solution().countLargestGroup(13)',
    expect=4,
    views=[
        dict(type='map', var='s_dict', label='s_dict（数位和 → 个数；黄框 = 刚更新）', fmt=lambda k, v: f'{k}: {v}', h=220, font=30),
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='text', fn=_grp, size=26, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'pink'), ('s', 's', 'yellow'), ('cnt', 'cnt', 'blue'),
           ('now_cnt', 'now_cnt', 'purple'), ('res', 'res', 'green')],
    max_steps=90,
    skip=['s_dict = {}', 'now = index', 's = 0', 'res = 0', 'now_cnt = 0', 'for cnt in s_dict.values()', 'while now', 'now //= 10'],
    captions={
        'for index in range': lambda S, B, r: (f'取下一个数 `index = {S.index}`，先算它的数位和' if S.index <= S.n and not (S.index == S.n and B.get('s_dict') and sum(S.s_dict.values()) == S.n) else '1 到 n 都分好组了'),
        'while now': lambda S, B, r: (f'`now = {S.now}` 还有数位 → 继续取末位' if S.now else '`now = 0`：数位都取完了'),
        's += now % 10': '取末位 `now % 10 = {now % 10}` 累加到 `s`：`s = {B.s} + {now % 10} = {s}`，再 `now //= 10` 去掉末位（原文 `/`）→ `{now // 10}`',
        'now //= 10': '去掉末位：`now` 变成 `{now}`（原文 `/`）',
        's_dict[s] =': '数位和 `{s}` 的组 +1：`s_dict[{s}] = {s_dict[s]}`',
        'if cnt > now_cnt': lambda S, B, r: (('分组完成，现在==在各组大小里找最大值==。' if S.get('now_cnt') == 0 and S.cnt > 0 and B.get('cnt') is None else '') +
                                             (f'`cnt = {S.cnt} > now_cnt = {S.now_cnt}`：遇到更大的组' if S.cnt > S.now_cnt
                                              else f'`cnt = {S.cnt}`，和最大值 `now_cnt = {S.now_cnt}` 比较')),
        'res = 1': '更大的组：计数重置，`res = 1`',
        'now_cnt = cnt': '最大值更新为 `now_cnt = {cnt}`',
        'elif cnt == now_cnt': lambda S, B, r: (f'`cnt = {S.cnt}` 等于最大值 → 并列最大' if S.cnt == S.now_cnt
                                                else f'`cnt = {S.cnt}` 小于最大值 `{S.now_cnt}`，忽略'),
        'res += 1': '又一个同样大的组：`res = {res}`',
        'return res': '最大的组有 `{now_cnt}` 个数，这样的组共 =={ret}== 个',
    },
    cards=dict(
        one_liner='先按数位和分组计数，再数最大组出现几次',
        complexity='时间 `O(n log n)`，空间 `O(log n)`',
        problem=['把 `1` 到 `n` 按==数位和==分组，求元素最多的组里有几个数的「并列组数」',
                 '即：有多少个组的大小等于最大组的大小',
                 '示例：`n = 13` → `4`（数位和 1~4 的组各 2 个）'],
        quote='对于每个数字，计算其各位上的和，然后使用哈希表来储存每个数值和出现的次数，接下来对于这些次数，选择其中的最大值，并统计这个最大值出现的数目，即为最终答案。',
        quote_src='—— yiduobo 题解',
        idea=['两步走：先分组计数，再对各组大小找最大值并数个数',
              '第一步：`while now` 反复取末位 `now % 10` 求数位和，哈希表计数',
              '第二步：遍历 `s_dict.values()`，更大就重置 `res = 1`，相等就 `res += 1`'],
        summary=['时间 `O(n log n)`：每个数求数位和要 `log n` 步；空间 `O(log n)` 个不同数位和',
                 '易错：更大的组出现时要把 `res` 重置为 `1`，不是累加',
                 '原文为 Python 2 写法，整数除法 `now /= 10` 已改为 `now //= 10`',
                 '`n` 很大时要改用数位 DP（灵神题解的方法二）'],
    ),
)

CONFIG = dict(
    num=1015, title='可被 K 整除的最小整数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='维护 N[l] 与 10^l 的余数 + 余数判环',
    tags=['数学算法', '链表、二叉树与回溯'],
    code='''
class Solution(object):
    def smallestRepunitDivByK(self, K):

        rem_set = set()
        remain = 1
        res = 0
        now = 0
        while True:
            res += 1
            now = (now + remain) % K
            if now == 0:
                return res
            if now in rem_set:
                break
            rem_set.add(now)
            remain = (remain * 10) % K

        return -1
''',
    call='Solution().smallestRepunitDivByK(13)',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"`N[{S['res']}]` = `{'1' * S['res']}`；`now` = N[{S['res']}] % {S['K']} = =={S['now']}==；`remain` = 10^{S['res'] - 1} % {S['K']} = {S['remain']}" if S.get('res') else ''), h=100),
        dict(type='set', var='rem_set', label='rem_set（出现过的余数）', fmt=lambda x: str(x), h=200),
    ],
    watch=['K', ('res', 'res', 'blue'), ('now', 'now', 'yellow'), ('remain', 'remain', 'cyan')],
    captions={
        'rem_set = set()': '`rem_set` 记录已经出现过的 `N[l] % K`',
        'remain = 1': '`remain` 表示 `10^l % K`，这里先存 `10^0 % K = 1`',
        'res = 0': '`res` 是当前全 1 数的位数 l',
        'now = 0': '`now` 表示 `N[l] % K`，从 0 开始累加',
        'while True': '不断加长全 1 数，直到整除或余数重复',
        'res += 1': '长度加一：现在考虑 `l = {res}` 位的全 1 数',
        'now = (now + remain)': '`N[l] = 10^(l-1) + N[l-1]`：`({B.now} + {remain}) % {K}` = =={now}==',
        'if now == 0': lambda S, B, r: (f'`now = 0` → {S.res} 位的全 1 数能被 {S.K} 整除，返回 {S.res}' if S.now == 0 else f'`now = {S.now} != 0` → 还没整除'),
        'if now in rem_set': lambda S, B, r: (f'`now = {S.now}` 以前出现过 → 余数进入循环，永远到不了 0 → 无解' if S.now in S.rem_set
                                              else f'`now = {S.now}` 没出现过 → 继续'),
        'rem_set.add': '记下余数 `{now}`，以后再遇到就说明进环了',
        'remain = (remain * 10)': '`10^l % K = (10^(l-1) % K) * 10 % K`：`{B.remain} * 10 % {K}` = =={remain}==，留给下一位用',
        'return res': '返回位数 =={res}==',
        'return -1': '无解',
    },
    cards=dict(
        one_liner='N[l] 的余数 = (10^(l-1) 的余数 + N[l-1] 的余数) % K',
        complexity='时间 `O(K)`，空间 `O(K)`',
        problem=['找最小的 `11...1`（只含数字 1）使它能被 `K` 整除，返回位数；没有则返回 `-1`',
                 '示例：`K=3` → `3`；`K=2` → `-1`',
                 '本视频：`K=13` → `6`（`111111 = 13 × 8547`）'],
        quote='若某一时刻N[l] % K在之前出现过，那么说明余数进入了一个循环，问题无解，于是返回-1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`N[l] = 10^(l-1) + N[l-1]`，所以 `N[l] % K` 由两个更小的余数相加',
              '`10^l % K` 也能从 `10^(l-1) % K` 乘 10 得到，因此维护 `now` 和 `remain` 两个余数',
              '余数最多 K 种，重复出现说明进环；用 set 判重来返回 -1'],
        summary=['时间 `O(K)`，空间 `O(K)`（rem_set）',
                 '易错点：先更新 `now` 再判断；`remain` 要留到下一轮才更新',
                 '余数一旦重复就一定不会再到 0，所以 set 判重等价于判无解',
                 '对比灵神：灵神直接 `x*10+1` 递推，并先排除 2、5 的倍数以省掉 set'],
    ),
)

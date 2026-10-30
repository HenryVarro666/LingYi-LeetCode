CONFIG = dict(
    num=2790, title='长度递增组的最大数目', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='排序 + 累计空闲数',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def maxIncreasingGroups(self, usageLimits):

        usageLimits.sort()
        now = usageLimits[0] - 1
        res = 1
        for index in range(1, len(usageLimits)):
            now += usageLimits[index]
            if now >= res + 1:
                now -= res + 1
                res += 1
            
        return res
''',
    call='Solution().maxIncreasingGroups([2, 1, 2, 5])',
    expect=3,
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"已能组成 `{S['res']}` 组（长度 1..{S['res']}），空闲的数字个数 `now = {S['now']}`；下一组需要 =={S['res'] + 1}== 个"
                           if 'now' in S and 'res' in S else '每个数字在每组最多出现一次，每组比上一组长')),
        dict(type='array', var='usageLimits', label='usageLimits（排序后；蓝 = 当前加入的数字可用次数）', cell=96, h=240,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('index') else None,
             dim=lambda S, i, v: i > S.get('index', 0) if 'index' in S else False),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'usageLimits.sort()': '从小到大排序：先用次数少的数字，次数多的留到后面的长组',
        'now = usageLimits[0] - 1': '最小的数字 `{usageLimits[0]}` 次：拿 1 次做第 1 组（长度 1），剩 `now = {now}` 个空闲',
        'res = 1': '至少能组 1 组：`res = 1`',
        'now += usageLimits[index]': '把 `usageLimits[{index}] = {usageLimits[index]}` 加进空闲数：`now` = {B.now} + {usageLimits[index]} = =={now}==',
        'if now >= res + 1': lambda S, B, r: (f'`now = {S.now} ≥ res + 1 = {S.res + 1}`：空闲数字够凑长度 {S.res + 1} 的新组 → 成立'
                                              if S.now >= S.res + 1 else
                                              f'`now = {S.now} < res + 1 = {S.res + 1}`：不够凑新组，留给后面'),
        'now -= res + 1': '新组用掉 `{B.res + 1}` 个数字：`now` = {now}',
        'res += 1': '组数 +1：`res = {res}`',
        'return res': '最多 `{res}` 组',
    },
    cards=dict(
        one_liner='排序后累计空闲次数，够凑“下一个长度”就多一组',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地排序）',
        problem=['`usageLimits[i]` 是数字 `i` 最多能用的总次数',
                 '造若干组：每组数字互不重复，且==每组比前一组严格更长==',
                 '求最多能造几组。示例：`[2,1,2,5]` → `3`'],
        quote='每次只需将新来的a[p]的数量加入到剩余可用数字的统计值中，若这些数字的量足够构成新的斜线，那么就进行构造。',
        quote_src='—— yiduobo 题解原文',
        idea=['理想形状是“三角形”：长度 1,2,3,… 的组，数字小的排在斜线上',
              '数量不够就向前“挤”一轮，多出来的可以留给后面',
              '鸽笼原理保证加入新数字最多新增一组，不会重复用同一个数'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：`now` 初始为 `usageLimits[0] - 1`，`res` 初始为 1（最小的数拿一次组成第一组）',
                 '一个数字加入后最多多一组，所以每个数字只判断一次 `if`',
                 '原文为 Python 2 风格，代码在 Python 3 下无需改动'],
    ),
)

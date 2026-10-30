CONFIG = dict(
    num=1403, title='非递增顺序的最小子序列', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='计数桶 · 从大到小取',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minSubsequence(self, nums):

        cnt_list = [0] * 101
        s = 0
        for num in nums:
            cnt_list[num] += 1
            s += num
        
        res = []
        now = 0
        for num in range(100, 0, -1):
            while cnt_list[num] > 0 and now + now <= s:
                now += num
                cnt_list[num] -= 1
                res.append(num)
        
            if now + now > s:
                break

        return res
''',
    call='Solution().minSubsequence([97,100,95,99,98,96])',
    expect=[100, 99, 98],
    max_steps=80,
    views=[
        dict(type='array', var='nums', label='nums', cell=80, h=150),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"总和 `s = {S['s']}`；已取 `now = {S['now']}`，`2 × now = {2 * S['now']}`，要 ==大于 {S['s']}==" if 'now' in S else
                           (f"总和 `s = {S['s']}`" if 's' in S else ''))),
        dict(type='array', var='res', label='res（已取的数，从大到小）', cell=80, h=170, color=lambda S, i, v: 'green'),
    ],
    watch=[('num', 'num', 'blue'), ('s', 's', 'orange'), ('now', 'now', 'green')],
    captions={
        'cnt_list = [0] * 101': '数值最多到 100：下标当桶，`cnt_list[x]` 记 `x` 出现几次，代替排序',
        's = 0': '`s` 累计所有数的总和',
        'for num in nums': lambda S, B, r: ('总和算完：`s = %d`' % S.s if S.s == sum(S.nums) else f'读入 `{S.num}`'),
        'cnt_list[num] += 1': '桶 `{num}` 计数加一 → `{cnt_list[num]}`',
        's += num': '总和 `s` → {s}',
        'res = []': '`res` 放选出来的数',
        'now = 0': '`now` 是 `res` 里数的和，要让它超过剩下的和',
        'for num in range(100, 0, -1)': lambda S, B, r: (f'从大到小扫描桶：现在是 `{S.num}`' if S.cnt_list[S.num] > 0 else f'桶 `{S.num}` 是空的，跳过'),
        'while cnt_list[num] > 0 and now + now <= s': lambda S, B, r: (
            f'桶里还有 `{S.num}` 且 `{S.now}+{S.now} = {2 * S.now}` ≤ `{S.s}`：和还没超过一半 → 继续取' if S.cnt_list[S.num] > 0 and S.now + S.now <= S.s
            else ('这个桶取完了' if S.cnt_list[S.num] <= 0 else f'`{2 * S.now}` > `{S.s}`：已经超过一半，不再取')),
        'now += num': '取走一个 `{num}`：`now` → =={now}==',
        'cnt_list[num] -= 1': '桶 `{num}` 剩 `{cnt_list[num]}` 个',
        'res.append(num)': '`{num}` 加入 `res` → `{res}`',
        'if now + now > s': lambda S, B, r: (f'`{2 * S.now} > {S.s}`：`res` 的和超过剩下的 → ==停止，已是最短=='
                                             if S.now + S.now > S.s else f'`{2 * S.now} ≤ {S.s}`：还不够，下一个桶'),
        'break': '结束扫描',
        'return res': '返回 `{res}`：和为 `{now}`，严格大于剩下的 `{s - now}`',
    },
    cards=dict(
        one_liner='要子序列尽量短、和超过一半：从大的数开始拿',
        complexity='时间 `O(n + U)`，空间 `O(U)`（U = 100）',
        problem=['从 `nums` 里取一个子序列，使它的和==严格大于==剩下元素的和',
                 '要求子序列元素个数最少；个数相同取和最大；按==非递增==顺序返回',
                 '本视频：`[97,100,95,99,98,96]` → `[100,99,98]`'],
        quote='为了选出值超过一半的子序列，同时要求序列最短，那么显然应该先选择数值较大的元素……由于这里的数值最多只有100，因此我选择的是类似桶排序的做法。',
        quote_src='—— yiduobo 题解原文',
        idea=['先拿大数，每拿一个数让和涨得最快 → 个数最少',
              '值域只有 1..100，用 `cnt_list` 当桶，从 100 往 1 扫就等价于降序排序',
              '`now + now > s`：我拿的和大于总和的一半，即严格大于剩下的'],
        summary=['时间 `O(n + U)`，空间 `O(U)`；也可以直接降序排序，`O(n log n)`',
                 '用 `now + now <= s` 判断，避免除法；相等时还要继续取（要严格大于）',
                 '桶是从 100 往下扫，所以 `res` 天然是非递增的',
                 '原文已是可直接运行的写法，无需改动'],
    ),
)

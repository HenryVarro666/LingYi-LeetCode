CONFIG = dict(
    num=2110, title='股票平滑下跌阶段的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='动态规划 · f[i] 滚动成变量',
    tags=['分组循环', '难度分 1408'],
    code='''
class Solution(object):
    def getDescentPeriods(self, prices):

        n = len(prices)
        res = 1
        now = 1
        for index in range(1, n):
            if prices[index] == prices[index - 1] - 1:
                now += 1
            else:
                now = 1
            
            res += now

        return res
''',
    call='Solution().getDescentPeriods([4,3,2,1,5,4,4,3])',
    expect=16,
    views=[
        dict(type='text', fn=lambda S: (f"`f[{S['index']}]` = now = =={S['now']}==：以 `prices[{S['index']}]` 结尾的平滑下跌阶段数；累计 `res` = {S['res']}") if 'index' in S and 'now' in S else '', size=28),
        dict(type='array', var='prices', pointers={'index': 'pink'},
             window=(lambda S: S['index'] - S['now'] + 1, 'index'), h=300, cell=90,
             dim=lambda S, k, v: 'index' in S and k > S['index']),
    ],
    watch=[('index', 'index', 'pink'), ('now', 'now (f[i])', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 1': '`f[0] = 1`：第一天自己是一个阶段，`res` 先记 ==1==',
        6: '`now` 就是 `f[i]`，现在 `f[0] = 1`',
        'if prices[index]': lambda S, B, r: (f"`{S.prices[S.index]} == {S.prices[S.index-1]} - 1` → 成立：可接在以前一天结尾的所有阶段后面" if S.prices[S.index] == S.prices[S.index-1] - 1
                                             else f"`{S.prices[S.index]}` 不等于 `{S.prices[S.index-1]} - 1` → 只能自己单独成阶段"),
        'now += 1': '`f[i] = f[i-1] + 1`：前一天结尾的 `{now-1}` 个阶段都能延长，再加上自己单独的 1 个 → ==`{now}`==',
        11: '`f[i] = 1`：只剩单独一天',
        'res += now': '累加 `f[{index}] = {now}`：`res` = {B.res} + {now} = =={res}==',
        'return res': '所有 `f[i]` 之和 = `{res}`',
    },
    cards=dict(
        one_liner='f[i] = 以 prices[i] 结尾的阶段数，累加所有 f[i]',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['平滑下跌阶段：连续几天，每天价格比前一天恰好少 1',
                 '单独一天也算，求阶段总数',
                 '示例：`[3,2,1,4]` → `7`；本视频：`[4,3,2,1,5,4,4,3]` → `16`'],
        quote='令 f[i] 表示以 prices[i] 结尾的平滑下跌阶段的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['满足 `prices[i] == prices[i-1] - 1`：`f[i] = f[i-1] + 1`',
              '否则只能单独成阶段：`f[i] = 1`',
              '`f[i]` 只依赖 `f[i-1]`，所以把数组换成一个变量 `now`，边遍历边累加'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 和 `now` 都从 1 开始：对应边界 `f[0] = 1`，循环从下标 1 起',
                 '易错：条件是恰好少 1，不是“比前一天小”',
                 '原文已是 Python 3 可运行，未做修改',
                 '对比灵神：同一个递推，灵神从“按右端点分组”理解，这里是显式 DP 状态'],
    ),
)

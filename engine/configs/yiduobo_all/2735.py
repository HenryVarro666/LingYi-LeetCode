CONFIG = dict(
    num=2735, title='收集巧克力', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='滚动数组 · 逐轮维护每个位置的最低价',
    tags=[],
    code='''
class Solution(object):
    def minCost(self, nums, x):
        n = len(nums)
        f = nums[:]
        res = sum(nums)
        for rnd in range(1, n):
            g = f[:]
            f = []
            for index in range(n):
                f.append(min(nums[(index + rnd) % n], g[index]))

            res = min(res, rnd * x + sum(f))

        return res
''',
    call='Solution().minCost([20,1,15,9], 5)',
    expect=19,
    views=[
        dict(type='array', var='nums', label='nums（原价；粉 = 这一轮新轮到 index 的价格）', h=170, pointers={'index': 'blue'},
             color=lambda S, i, v: 'pink' if 'index' in S and 'rnd' in S and i == (S['index'] + S['rnd']) % len(S['nums']) else None),
        dict(type='array', var='g', label='g（上一轮每个位置的最低价）', h=170, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f（本轮：绿 = 刚算出的最低价）', h=170,
             color=lambda S, i, v: 'green' if i == len(S['f']) - 1 and S['_line'] == 11 else None),
        dict(type='text', fn=lambda S: f"`rnd={S['rnd']}`：`rnd * x + sum(f) = {S['rnd']*S['x']} + {sum(S['f'])}` = =={S['rnd']*S['x']+sum(S['f'])}==" if 'rnd' in S and len(S.get('f', [])) == len(S['nums']) else ''),
    ],
    watch=[('rnd', 'rnd', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = nums[:]': '`f[j]` 表示第 `j` 类巧克力当前能取到的最低价，开始没操作就是原价 `{f}`',
        'res = sum(nums)': '一次都不操作：总价 `sum(nums) = {res}`，作为答案的初值',
        'for rnd in range': lambda S, B, r: ('`rnd` 轮次都试完了' if 'rnd' in B and S.rnd == B.rnd
                                             else f'第 `{S.rnd}` 轮替换：第 `j` 类可以买 `nums[j .. j+{S.rnd}]`（环形）里最便宜的'),
        'g = f[:]': '先把上一轮的 `f` 备份进 `g`，`f` 重新算（滚动数组）',
        'f.append': '`min(nums[({index}+{rnd})%n], g[{index}])` → `min({nums[(index + rnd) % n]}, {g[index]})` = =={f[-1]}==：多一轮就多一个候选价',
        'res = min(res': '操作 `{rnd}` 轮：`{rnd}×x + sum(f) = {rnd*x + sum(f)}`，`res = min({B.res}, …)` = =={res}==',
        'return res': '所有轮次试完，最小花费 `{res}`',
    },
    cards=dict(
        one_liner='f[i][j] = min(f[i-1][j], nums[(i+j)%n])：每轮只多一个候选价',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['`nums[i]` 是收集第 `i` 类巧克力的成本；花 `x` 操作一次，所有类型 `i → (i+1) mod n`',
                 '求收集全部类型的最小总成本',
                 '示例：`[20,1,15], x=5` → `13`；本视频用 `[20,1,15,9]`'],
        quote='令f[i][j]表示在进行了i次交换后，下标为j的巧克力可以取到的最便宜价格，那么就有f[i][j] = min(f[i - 1][j], nums[(i + j) % n])',
        quote_src='—— yiduobo 题解原文',
        idea=['替换次数必然小于 `n`，`n` 次相当于没操作',
              '第 `rnd` 轮后，每类巧克力是「前缀最小值」：在上一轮最低价和新轮到的价格里取小',
              '总花费 `rnd * x + sum(f)`，从 `sum(nums)` 起和每一轮取最小'],
        summary=['时间 `O(n²)`，空间 `O(n)`（滚动数组去掉 `i` 这一维）',
                 '`rnd` 从 1 到 `n-1`；`rnd=0` 的情况就是初值 `sum(nums)`',
                 '`g = f[:]` 先备份，保证新 `f` 只依赖上一轮',
                 '原文代码未改，只去掉了空行里的多余空白',
                 '对比灵神：灵神枚举区间端点累加 `s[k]`；yiduobo 逐轮维护最低价数组'],
    ),
)

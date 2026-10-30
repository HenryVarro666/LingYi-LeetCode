CONFIG = dict(
    num=1402, title='做菜顺序', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='排序 + 一边前缀和一边更新答案',
    tags=['灵神题单', '难度分 1679'],
    code='''
class Solution(object):
    def maxSatisfaction(self, satisfaction):

        now = 0
        res = 0
        s = 0
        for index, num in enumerate(sorted(satisfaction, reverse = True)):
            s += num
            now += s
            res = max(res, now)
        
        return res
''',
    call='Solution().maxSatisfaction([-1,-8,0,5,-9])',
    expect=14,
    views=[
        dict(type='array', var='sorted(satisfaction, reverse=True)', label='从大到小排好（蓝箭头 = 当前这道菜）', h=250, cell=100,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and i <= S['index'] and S['_line'] >= 10 else None),
        dict(type='text', size=32, fn=lambda S: (
            f"做 `{S['index'] + 1}` 道菜：`s`（前缀和）= {S['s']}，收益 `now` = =={S['now']}==，最好 `res` = =={S['res']}==" if 'index' in S
            else '先排序，再一边累加前缀和一边更新答案')),
    ],
    watch=['index', 'num', ('s', 's', 'cyan'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now`：当前做 `k` 道菜的收益 `v[k]`',
        'res = 0': '`res`：目前见过的最大收益；可以一道都不做，所以从 0 开始',
        's = 0': '`s`：前缀和 `a[0] + … + a[k]`',
        'for index, num': lambda S, B, r: ('遍历结束，所有菜都试过了' if B.get('index') == S.get('index') and 'index' in B else f'菜从满意度大到小取：这是第 `{S.index}` 个，`num = {S.num}`'),
        's += num': '前缀和 `s = {B.s} + ({num})` = =={s}==',
        'now += s': '`v[k+1] − v[k] = 前缀和`：`now = {B.now} + ({s})` = =={now}==',
        'res = max': '`res = max({B.res}, {now})` = =={res}==：{"更好，更新" if res != B.res else "没有更好，保持不变"}',
        'return res': '做若干道菜后最大的收益 =={ret}==',
    },
    cards=dict(
        one_liner='喜爱度大的放后面做；多做一道，收益增加前缀和',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['做每道菜用 1 单位时间，系数 = 完成时间 × 满意度', '可以选择顺序，也可以放弃一些菜，求最大总和', '示例：`[-1,-8,0,5,-9]` → `14`'],
        quote='对于喜爱度越高的菜应该放到越后面来做；做 k + 1 道菜与做 k 道菜的收益相减，v[k + 1] - v[k] = a[0] + a[1] + ... + a[k]，也就转化成了一个前缀和的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['做 `k` 道菜，一定选满意度最高的 `k` 道；交换相邻两道菜可证大的放后面', '从大到小排好后：`v[k] = a[0]·k + a[1]·(k-1) + … + a[k-1]`',
              '`v[k+1] − v[k] = a[0] + … + a[k]`：每多做一道，加一个前缀和', '一边加前缀和，一边用 `res = max(res, now)` 记录最大值'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 产生新数组）', '`res` 从 0 开始：全是负数时一道菜都不做', '与灵神的区别：不提前 break，而是遍历到底，用 `max` 取最大',
                 '原文只有这一种写法，没有改动'],
    ),
)

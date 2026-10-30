CONFIG = dict(
    num=2898, title='最大线性股票得分', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 按 price - index 分组', tags=[],
    code='''
class Solution(object):
    def maxScore(self, prices):

        cnt = {}
        for index, v in enumerate(prices):
            cnt[v - index] = cnt.get(v - index, 0) + v
        
        return max(cnt.values())
''',
    call='Solution().maxScore([1,5,3,7,8])',
    expect=20,
    views=[
        dict(type='array', var='prices', h=190, label='prices', pointers={'index': 'blue'},
             color=lambda S, i, v: None),
        dict(type='text', size=32, fn=lambda S: f"当前：`{S['v']} - {S['index']}` = ==键 {S['v']-S['index']}==" if 'index' in S and 'v' in S else ''),
        dict(type='map', var='cnt', h=230, fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v')],
    captions={
        'cnt = {}': '`cnt[key]` 存「price - index 等于 key」的所有价格之和',
        'for index, v': '看第 `{index}` 天，价格 `{v}`',
        'cnt[v - index]': '键 `v - index = {v} - {index} = {v - index}`：同键的天 ==price − index 相等== 能连成一条线性序列 → `cnt[{v - index}] = {cnt[v - index]}`',
        'return max': '各组之和里取最大，就是最大得分 =={ret}==',
    },
    cards=dict(
        one_liner='price − index 相等的天可以连成线性序列，按它分组求和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 `prices`，选递增下标序列，要求相邻两项 `prices[j]-prices[j-1] == j-(j-1)` 的下标差',
                 '得分是所选价格之和，求最大得分（只选一项也合法）',
                 '本视频：`[1,5,3,7,8]` → `20`'],
        quote='prices[indexes[j]] - indexes[j] = prices[indexes[j - 1]] - indexes[j - 1]，也就是说，如果将数组中每个数都减去自身的下标……',
        quote_src='—— yiduobo 题解原文',
        idea=['条件移项：`prices[j] - j` 在相邻两项间 ==相等==',
              '所以一条合法序列里每项 `price - index` 都相同',
              '按这个值分组，组内全部天都能选；每组价格求和，取最大'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '键是 `v - index`，累加的是 `v`，不是 index',
                 '价格都为正，同组全选总和最大',
                 '原文为 Python 2 风格写法，但无需修改即可运行；题意据文章与力扣原题写出'],
    ),
)

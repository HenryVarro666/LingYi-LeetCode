CONFIG = dict(
    num=458, title='可怜的小猪', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='信息论 · 每头猪表示 p/m+1 种状态',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def poorPigs(self, buckets, minutesToDie, minutesToTest):

        test_round = minutesToTest // minutesToDie + 1
        pigs = 0
        while test_round ** pigs < buckets:
            pigs += 1
        
        return pigs
''',
    call='Solution().poorPigs(125, 15, 60)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"每头猪 `{S['test_round']}` 种状态，`{S['pigs']}` 头猪能区分 `{S['test_round']}^{S['pigs']}` = =={S['test_round'] ** S['pigs']}== 种情况（要覆盖 `{S['buckets']}` 桶）" if 'pigs' in S and 'test_round' in S else ''), size=28),
        dict(type='bars', var=lambda S: [S['test_round'] ** k for k in range(5)] if 'test_round' in S else [], label='pigs = 0,1,2,… 头猪能区分的桶数（绿 = 够了）',
             pointers={'pigs': 'blue'}, h=420,
             color=lambda S, i, v: 'green' if 'buckets' in S and v >= S['buckets'] else None,
             dim=lambda S, i, v: 'pigs' in S and i > S['pigs']),
    ],
    watch=['buckets', 'minutesToDie', 'minutesToTest', ('test_round', 'test_round', 'cyan'), ('pigs', 'pigs', 'blue')],
    captions={
        'test_round =': '时间够测 `{minutesToTest} // {minutesToDie} = {minutesToTest // minutesToDie}` 轮；一头猪可能在第 1…{minutesToTest // minutesToDie} 轮死，或一直不死 → `test_round` = =={test_round}== 种状态',
        'pigs = 0': '从 0 头猪开始试：`pigs` 头猪能表示 `test_round ^ pigs` 种状态',
        'while test_round ** pigs < buckets': lambda S, B, r: (f'`{S.test_round}^{S.pigs} = {S.test_round ** S.pigs} < {S.buckets}`：状态数还不够区分每一桶 → ==再加一头猪==' if S.test_round ** S.pigs < S.buckets else f'`{S.test_round}^{S.pigs} = {S.test_round ** S.pigs} >= {S.buckets}`：状态数够了 → ==停止，不再加猪=='),
        'pigs += 1': '加一头猪：`pigs` → =={pigs}==',
        'return pigs': '最少需要 =={pigs}== 头猪',
    },
    max_steps=40,
    cards=dict(
        one_liner='一头猪能表达 p/m+1 种状态，k 头猪就是它的 k 次方',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`buckets` 桶水里恰有一桶有毒，猪喝了毒水 `minutesToDie` 分钟后死亡',
                 '总共有 `minutesToTest` 分钟，可以分多轮喝水，求最少几头猪能找出毒水',
                 '示例：`buckets=1000, 15, 60 → 5`；本视频用 `125, 15, 60 → 3`'],
        quote='换言之，一头猪可以表达p/m + 1种状态，于是k头猪就可以表达(p/m + 1) ^ k种状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['一头猪在 `p` 分钟内：第 1 轮就死、第 2 轮才死……第 `p/m` 轮才死，或者一直没死',
              '合起来是 `p/m + 1` 种状态，`k` 头猪的状态组合有 `(p/m+1)^k` 种',
              '每种组合对应一桶水，所以只要 `(p/m+1)^k >= n`，最小的 `k` 就是答案'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '状态数是 `p/m + 1`，别忘了 ==+1==（一直没死也是一种状态）',
                 '`>=` 才够：恰好等于 `n` 时已经能区分每一桶',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '本质：`k = ceil(log(n) / log(p/m + 1))`，用循环避开浮点误差'],
    ),
)

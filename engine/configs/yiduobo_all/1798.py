CONFIG = dict(
    num=1798, title='你能构造出连续值的最大数目', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='从小到大扩展区间', tags=['灵神题单', '贪心与思维', '难度分 1931'],
    code='''
class Solution(object):
    def getMaximumConsecutive(self, coins):

        ma = 0
        for coin in sorted(coins):
            if coin <= ma + 1:
                ma += coin
            else:
                break
        
        return ma + 1
''',
    call='Solution().getMaximumConsecutive([1,1,1,4,10])',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: f"覆盖区间 ==[0, {S['ma']}]==" if 'ma' in S else '', size=34),
        dict(type='array', var='coins', label='coins（按从小到大加入）', h=220),
        dict(type='text', fn=lambda S: f"新硬币 coin = {S['coin']}，需要 coin <= ma + 1 = {S['ma']+1}" if 'coin' in S else '', size=30),
    ],
    watch=[('ma', 'ma', 'cyan'), 'coin'],
    captions={
        'ma = 0': '区间 `[0, ma]` 现在只有 `0`',
        'for coin in sorted': '按从小到大取下一枚硬币 `coin = {coin}`',
        'if coin <= ma + 1': lambda S, B, r: (f'`{S.coin} <= {S.ma}+1`：`[coin, ma+coin]` 与 `[0, ma]` 能连成一段 → 成立' if S.coin <= S.ma + 1
                                              else f'`{S.coin} > {S.ma}+1`：中间断开，后面的数更大也补不上 → 走 else，不成立'),
        'ma += coin': '区间扩展为 `[0, ma+coin]` → `ma = {ma}`',
        'break': '区间不再连续，后续都 ≥ coin，也不行，退出',
        'return ma + 1': '`[0, {ma}]` 里一共有 `ma + 1 = {ret}` 个数',
    },
    cards=dict(
        one_liner='想让区间连续，硬币应尽量小：从小到大加',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`coins` 选一部分求和得到的值叫可构造；求从 `0` 起最多连续可构造多少个整数',
                 '示例：`[1,1,1,4]` → `8`',
                 '本视频：`[1,1,1,4,10]` → `8`'],
        quote='若当前的数值coin满足coin <= ma + 1，那么说明ma可以扩展到ma + coin。若不满足，那么在加入coin之和区间不再连续。',
        quote_src='—— yiduobo 题解原文',
        idea=['设已覆盖 `[0, ma]`，加入 `coin` 后变成 `[0, ma]` 并 `[coin, ma+coin]`',
              '要连续必须 `coin <= ma + 1`',
              '想流畅扩展，硬币应尽量小 → 排序后从小到大加',
              '一旦断开，后面更大的数也连不上，答案就是 `ma + 1`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：个数是 `ma + 1`（包含 0）',
                 '用 `sorted(coins)` 不改原数组',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)

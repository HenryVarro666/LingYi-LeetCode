CONFIG = dict(
    num=2178, title='拆分成最多数目的正偶数之和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='推导最大 k + 补最后一项',
    tags=['灵神题单', '难度分 1538'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def maximumEvenSplit(self, finalSum):

        if finalSum % 2 == 1:
            return []
        
        k = int(sqrt(finalSum))
        while k > 0 and k * (k + 3) >= finalSum:
            k -= 1
        
        res = []
        for index in range(k):
            res.append(index * 2 + 2)
        res.append(finalSum - k * (k + 1))
        return res
''',
    call='Solution().maximumEvenSplit(28)',
    expect=[2, 4, 6, 16],
    views=[
        dict(type='text', size=30, fn=lambda S: (f"拆 `k = {S['k']}` 个：`2+…+{2*S['k']} = {S['k']*(S['k']+1)}`，最后一项 `{S['finalSum']} − {S['k']*(S['k']+1)} = {S['finalSum']-S['k']*(S['k']+1)}`，需要 `> {2*S['k']}`：`{S['k']}×{S['k']+3} = {S['k']*(S['k']+3)}` " + ('`>= finalSum`，不满足' if S['k']*(S['k']+3) >= S['finalSum'] else '`< finalSum`，==满足==') if 'k' in S else '先判断 finalSum 的奇偶')),
        dict(type='array', var='res', h=260, label='res（拆出的偶数）',
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('finalSum', 'finalSum', 'cyan'), ('k', 'k', 'blue')],
    captions={
        'if finalSum % 2 == 1': lambda S, B, r: ('奇数：偶数之和必为偶数 → 无法拆分，返回空' if S.finalSum % 2 else '偶数，可以往下拆'),
        'k = int(sqrt': '`k` 是拆出的个数，先取上界 `√finalSum = {k}`',
        'while k > 0': lambda S, B, r: (f'`k = {S.k}`：`k*(k+3) = {S.k*(S.k+3)}`，与 `finalSum = {S.finalSum}` 比较 → ' + ('`>=`，最后一项不够大，==k 太大==' if S.k * (S.k + 3) >= S.finalSum else '`<`，条件满足，k 合适')),
        'k -= 1': '`k` 减 1 → `{k}`：少拆一个，让最后一项更大',
        'res = []': '`k` 确定了：前 `k` 个取 `2,4,…,2k`',
        'for index in range': lambda S, B, r: (f'取第 `{S.index+1}` 个偶数的下标 `index = {S.index}`' if S._line == 12 and 'index' in S and S.index != B.get('index', -1) or ('index' not in B) else '`2,4,…,2k` 都放好了'),
        'res.append(index': '第 `{index+1}` 个偶数：`index*2+2 = {index*2+2}`',
        'res.append(finalSum': '最后一项 `finalSum − k(k+1) = {finalSum} − {k*(k+1)} = {finalSum - k*(k+1)}`，==比 2k 大==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先推出最多拆几个，再把余数补到末尾',
        complexity='时间 `O(√finalSum)`，空间 `O(1)`',
        problem=['把 `finalSum` 拆成互不相同的正偶数之和，个数要最多',
                 '不能拆就返回空数组',
                 '示例：`28` → `[2,4,6,16]`'],
        quote='按2、4、6这样递增地拆分了k个偶数之后，剩下的最后一个偶数必然要大于2k，也就是 finalSum - (2 + 4 + ... + 2k) > 2k',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数无解；偶数则从小到大拆 `2,4,…`',
              '拆 `k` 个后剩下的最后一项必须大于 `2k`，否则会重复',
              '推出 `k(k+3) < finalSum`，找最大的 `k`，再补最后一项'],
        summary=['推导式：`finalSum > k(k+3)`，找最大的 `k`',
                 '`k` 从 `√finalSum` 往下减，次数很少；总体 `O(√finalSum)`',
                 '原文用了 `sqrt` 却没写 import，演示里补了 `from math import sqrt`',
                 '对比灵神：灵神边拆边减，yiduobo 先数学推出 `k` 再一次性构造'],
    ),
)

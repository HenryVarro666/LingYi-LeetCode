CONFIG = dict(
    num=950, title='按递增顺序显示卡牌', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='倒推构造 · 队列模拟',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def deckRevealedIncreasing(self, deck):

        sorted_deck = sorted(deck, reverse=True)
        q = [sorted_deck[0]]
        l = 0
        for num in sorted_deck[1:]:
            q.append(q[l])
            q.append(num)
            l += 1

        return q[l:][::-1]
''',
    call='Solution().deckRevealedIncreasing([17,13,11,2,3,5,7])',
    expect=[2, 13, 3, 11, 5, 17, 7],
    views=[
        dict(type='array', var='sorted_deck', label='sorted_deck（从大到小）', h=170, cell=90,
             color=lambda S, i, v: 'yellow' if 'num' in S and v == S['num'] else None),
        dict(type='array', var='q', label='q（倒着看的牌组；蓝框 = 当前队首 q[l..]）', h=240, cell=90,
             pointers={'l': 'blue'}, window=('l', 'len(q) - 1'),
             dim=lambda S, i, v: 'l' in S and i < S['l']),
        dict(type='text', size=26, h=56, fn=lambda S: f"牌组（从顶到底）= `{S['q'][S['l']:][::-1]}`" if 'q' in S and 'l' in S else ''),
    ],
    watch=['num', ('l', 'l', 'blue')],
    captions={
        'sorted_deck = sorted': '倒推：从最大的牌开始往牌组里放，先把牌从大到小排好 `{sorted_deck}`',
        'q = [sorted_deck[0]]': '最大的牌 `{q[0]}` 最后被翻开，它自己组成牌组',
        'l = 0': '`l` 指向队首：`q[l:]` 就是当前牌组（倒着放）',
        'for num in': '要放入的牌 `num = {num}`（当前最大的剩余牌）',
        'q.append(q[l])': '倒推操作一：把牌组的==最后一张==（这里是队首 `q[l]` = {q[l]}）挪回牌组顶，对应原操作里「翻开后把下一张放到底」',
        'q.append(num)': '倒推操作二：再把 `num = {num}` 放到最顶 —— 它是这一步被翻开的牌',
        'l += 1': '队首后移：`l` → {l}，`q[l:]` 就是新牌组',
        'return q[l:][::-1]': '`q[l:]` 是倒着放的，反转一下得到牌组顺序 `{ret}`',
    },
    cards=dict(
        one_liner='正着构造难，倒着一张张放回去就是队列操作',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['牌组从上往下依次：翻开顶牌，再把新顶牌放到底，重复',
                 '要求翻开的牌恰好是递增顺序，求初始牌组顺序',
                 '示例：`[17,13,11,2,3,5,7]` → `[2,13,3,11,5,17,7]`'],
        quote='直接正向构造是比较复杂的，那么可以先看看能否反向构造，即从后往前看，逐个将当前的最大值对应的卡牌加入到牌组当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮：把牌组末尾那张挪到顶部，再把当前最大值放到顶部',
              '倒着看牌组，就是「队首挪到队尾，再追加新牌」',
              '用数组 + 队首下标 `l` 当队列，不用 deque'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：返回前要取 `q[l:]` 再反转，前面 `l` 个已出队',
                 '原文是 Python 2 风格，本代码无需改动即可运行',
                 '同类：约瑟夫环式的队列模拟'],
    ),
)

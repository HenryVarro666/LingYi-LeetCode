def _txt(S):
    if 'flag' not in S:
        return '先看花色是否全相同，再数点数最多出现几次'
    if 'cnt_dict' not in S:
        return f"花色全相同？ `flag = {S['flag']}`"
    return f"点数计数 `max_cnt = {S['max_cnt']}`：≥3 三条，≥2 对子，否则高牌"


CONFIG = dict(
    num=2347, title='最好的扑克手牌', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='判花色 + 哈希表数点数',
    code='''
class Solution(object):
    def bestHand(self, ranks, suits):

        flag = True
        for index in range(4):
            if suits[index] != suits[index + 1]:
                flag = False
                break
        
        if flag:
            return 'Flush'
        
        cnt_dict = {}
        max_cnt = 0
        for rank in ranks:
            cnt_dict[rank] = cnt_dict.get(rank, 0) + 1
            max_cnt = max(max_cnt, cnt_dict[rank])
        
        if max_cnt >= 3:
            return 'Three of a Kind'
        elif max_cnt >= 2:
            return 'Pair'
        else:
            return 'High Card'
''',
    call='Solution().bestHand([4,4,2,4,9], ["d","a","a","b","c"])',
    expect='Three of a Kind',
    views=[
        dict(type='text', fn=_txt, size=30, h=90),
        dict(type='array', var='ranks', label='ranks（点数）', h=200, cell=96, pointers={},
             color=lambda S, i, v: 'yellow' if S.get('cnt_dict') and S['cnt_dict'].get(v, 0) >= 2 else None),
        dict(type='string', var='suits', label='suits（花色）', h=200, cell=96, pointers={'index': 'pink'}),
        dict(type='map', var='cnt_dict', label='cnt_dict（点数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=32),
    ],
    watch=['index', 'flag', 'rank', ('max_cnt', 'max_cnt', 'green')],
    captions={
        'flag = True': '`flag` 假设五张牌花色全相同',
        'for index in range(4)': '比较相邻两张的花色，一共 4 对：`index = {index}`',
        'if suits[index] !=': lambda S, B, r: f'`suits[{S.index}] = {S.suits[S.index]}` vs `suits[{S.index + 1}] = {S.suits[S.index + 1]}`：' + ('不同' if S.suits[S.index] != S.suits[S.index + 1] else '相同，继续比下一对'),
        'flag = False': '出现不同花色 → 不是同花，`flag = False`',
        'break': '已经确定不是同花，不用再比了',
        'if flag': lambda S, B, r: ('`flag` 为真：五张同花 → 返回 Flush' if S.flag else '`flag` 为假：不是同花，接着数点数'),
        "return 'Flush'": '五张花色相同 → ==Flush==（同花最大）',
        'cnt_dict = {}': '`cnt_dict` 统计每个点数出现的次数',
        'max_cnt = 0': '`max_cnt` 记录同一点数最多出现几次',
        'for rank in ranks': '取下一张牌的点数 `rank = {rank}`',
        'cnt_dict[rank] =': '点数 `{rank}` 现在出现 `{cnt_dict[rank]}` 次',
        'max_cnt = max': '`max_cnt = max({B.max_cnt}, {cnt_dict[rank]}) = {max_cnt}`',
        'if max_cnt >= 3': '`max_cnt = {max_cnt}`，`>= 3` ' + '→ 成立',
        "return 'Three": '有一个点数出现 ≥ 3 次 → ==Three of a Kind==',
        'elif max_cnt >= 2': '`max_cnt = {max_cnt}`，`>= 2` → 有对子',
        "return 'Pair'": '最多 2 张相同 → ==Pair==',
        "return 'High Card'": '五张点数互不相同 → ==High Card==',
    },
    cards=dict(
        one_liner='先判同花，不是再数点数最多出现几次',
        complexity='时间 `O(1)`（固定 5 张牌），空间 `O(1)`',
        problem=['给 5 张牌的点数 `ranks` 和花色 `suits`',
                 '手牌从好到坏：`Flush` > `Three of a Kind` > `Pair` > `High Card`',
                 '返回能组成的最好手牌类型',
                 '本视频：`[4,4,2,4,9]`，花色 `d,a,a,b,c` → `Three of a Kind`'],
        quote='首先遍历一趟花色，判断所有牌的花色是否相同。若相同，那么答案就是同花，否则就需要遍历一趟点数，统计同一点数最多出现多少次。',
        quote_src='—— yiduobo 题解原文',
        idea=['同花优先级最高：五张花色全相同就直接返回 `Flush`',
              '否则用哈希表数点数，记录最大出现次数 `max_cnt`',
              '`max_cnt >= 3` 是三条，`>= 2` 是对子，否则高牌'],
        summary=['时间 `O(1)`，空间 `O(1)`（只有 5 张牌）',
                 '返回的字符串要和题目大小写一致：`Three of a Kind`',
                 '判断顺序按「好 → 坏」：同花、三条、对子、高牌',
                 '原文为 Python 2 风格，在 Python 3 下无需改动'],
    ),
)

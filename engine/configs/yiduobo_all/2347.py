CONFIG = dict(
    num=2347, title='最好的扑克手牌', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='先判花色 · 再统计最大点数次数',
    tags=[],
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
    call="Solution().bestHand([10,10,2,12,9], ['a','b','c','a','d'])",
    expect='Pair',
    views=[
        dict(type='array', var='suits', label='suits（蓝 = 正在比较的相邻两张）', cell=90, h=170,
             color=lambda S, i, v: 'blue' if 'index' in S and 'cnt_dict' not in S and i in (S['index'], S['index'] + 1) else None),
        dict(type='array', var='ranks', label='ranks（黄 = 当前这张牌）', cell=90, h=170,
             color=lambda S, i, v: 'yellow' if 'rank' in S and v == S['rank'] else None),
        dict(type='map', var='cnt_dict', label='cnt_dict（点数 → 次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', h=80, size=30,
             fn=lambda S: f"同一点数最多出现 ==`{S['max_cnt']}`== 次" if 'max_cnt' in S else ''),
    ],
    watch=[('flag', 'flag', 'orange'), ('index', 'index', 'blue'), ('rank', 'rank'), ('max_cnt', 'max_cnt', 'green')],
    captions={
        'flag = True': '先假设五张牌花色全相同：`flag = True`',
        'for index in range(4)': '比较相邻两张的花色，一共比 4 次',
        'if suits[index] != suits[index + 1]': lambda S, B, r: (
            f'`suits[{S.index}] = {S.suits[S.index]!r}` 与 `suits[{S.index + 1}] = {S.suits[S.index + 1]!r}` '
            + ('不同 → 不是同花' if S.suits[S.index] != S.suits[S.index + 1] else '相同，继续比下一对')),
        'flag = False': '出现不同花色，`flag = False`，不用再比了',
        'break': '花色已经不全相同，跳出循环',
        'if flag': lambda S, B, r: ('`flag` 为真：五张花色相同' if S.flag else '`flag` 为假：不是同花，接着统计点数'),
        "return 'Flush'": '返回 `Flush`',
        'cnt_dict = {}': '准备数点数：`cnt_dict` 记每个点数出现几次',
        'max_cnt = 0': '`max_cnt` 记同一点数出现次数的最大值',
        'for rank in ranks': lambda S, B, r: (f'看下一张牌 `{S.rank}`' if 'rank' not in B or B.get('cnt_dict') is None or sum(B.cnt_dict.values()) < 5 else '5 张都数完了'),
        'cnt_dict[rank] =': '点数 `{rank}` 出现 `{cnt_dict[rank]}` 次',
        'max_cnt = max': '`max_cnt = max({B.max_cnt}, {cnt_dict[rank]})` = =={max_cnt}==',
        'if max_cnt >= 3': lambda S, B, r: (f'`max_cnt = {S.max_cnt} ≥ 3` → 三条' if S.max_cnt >= 3 else f'`max_cnt = {S.max_cnt} < 3`，不是三条'),
        'elif max_cnt >= 2': lambda S, B, r: (f'`max_cnt = {S.max_cnt} ≥ 2` → 对子' if S.max_cnt >= 2 else f'`max_cnt = {S.max_cnt} < 2`，没有对子'),
        "return 'Three of a Kind'": '返回 `Three of a Kind`',
        "return 'Pair'": '最多只有两张点数相同 → 返回 `Pair`',
        "return 'High Card'": '点数互不相同 → 返回 `High Card`',
    },
    cards=dict(
        one_liner='先比相邻花色判同花，再数点数看最大重复次数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['5 张牌，点数 `ranks`，花色 `suits`',
                 '同花 > 三条 > 对子 > 高牌，返回能组成的最好牌型',
                 '本视频：`[10,10,2,12,9]`，花色 `a,b,c,a,d` → `Pair`'],
        quote='首先遍历一趟花色，判断所有牌的花色是否相同。若相同，那么答案就是同花，否则就需要遍历一趟点数，统计同一点数最多出现多少次。',
        quote_src='—— yiduobo 题解原文',
        idea=['花色：相邻两张都相同 ⇔ 五张全相同，一发现不同就 `break`',
              '点数：用字典数次数，同时维护最大值 `max_cnt`',
              '`max_cnt ≥ 3` 三条，`≥ 2` 对子，否则高牌'],
        summary=['时间 `O(1)`，空间 `O(1)`：牌数固定为 5',
                 '易错：必须先判同花，再看点数',
                 '`max_cnt` 在每次计数后立即更新，不需要再扫一遍字典',
                 '代码未做修改（原文已可在 Python 3 运行）'],
    ),
)

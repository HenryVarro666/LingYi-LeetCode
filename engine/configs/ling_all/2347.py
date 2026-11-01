CONFIG = dict(
    num=2347, title='最好的扑克手牌', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数 · 提前返回（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def bestHand(self, ranks: List[int], suits: List[str]) -> str:
        if suits.count(suits[0]) == 5:
            return "Flush"
        cnt, pair = defaultdict(int), False
        for r in ranks:
            cnt[r] += 1
            if cnt[r] == 3:
                return "Three of a Kind"
            if cnt[r] == 2:
                pair = True
        if pair:
            return "Pair"
        return "High Card"
''',
    call='Solution().bestHand([4,2,4,9,4], ["a","a","b","c","d"])',
    expect='Three of a Kind',
    views=[
        dict(type='array', var='ranks', label='ranks（黄 = 当前这张牌的点数）', cell=90, h=170,
             color=lambda S, i, v: 'yellow' if 'r' in S and v == S['r'] else None),
        dict(type='array', var='suits', label='suits', cell=90, h=150),
        dict(type='map', var='cnt', label='cnt（点数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: ('`pair = ' + str(S['pair']) + '`：' + ('已经见过对子' if S['pair'] else '还没见过对子')) if 'pair' in S else ''),
    ],
    watch=[('r', 'r', 'blue'), ('pair', 'pair', 'orange')],
    captions={
        'suits.count(suits[0]) == 5': lambda S, B, r: (f'`suits` 里和 `{S.suits[0]!r}` 同花色的有 {S.suits.count(S.suits[0])} 张'
                                                      + (' → 五张同花' if S.suits.count(S.suits[0]) == 5 else ' → 不是同花，往下看点数')),
        'return "Flush"': '五张花色全相同 → 最好的牌型，直接返回 `Flush`',
        'cnt, pair = ': '`cnt` 统计每个点数出现几次；`pair` 记录是否已经出现过对子',
        'for r in ranks': '看下一张牌的点数 `r`',
        'cnt[r] += 1': '点数 `{r}` 出现次数 +1 → `{cnt[r]}`',
        'if cnt[r] == 3': lambda S, B, r: (f'`cnt[{S.r}] = 3`：凑够三张相同点数 → ==三条，提前返回==，不用看剩下的牌'
                                           if S.cnt[S.r] == 3 else f'`cnt[{S.r}] = {S.cnt[S.r]} ≠ 3`，还不是三条'),
        'return "Three of a Kind"': '三条比对子好，所以不必再往后找，返回 `Three of a Kind`',
        'if cnt[r] == 2': lambda S, B, r: (f'`cnt[{S.r}] = 2`：出现了对子，先记下来，但==还要继续看有没有三条==' if S.cnt[S.r] == 2
                                           else f'`cnt[{S.r}] = {S.cnt[S.r]}`，不是第二张'),
        'pair = True': '记下 `pair = True`',
        'if pair': lambda S, B, r: ('扫完 5 张没有三条；`pair` 为真 → 对子' if S.pair else '扫完 5 张没有对子'),
        'return "Pair"': '返回 `Pair`',
        'return "High Card"': '五张点数互不相同 → 返回 `High Card`',
    },
    cards=dict(
        one_liner='先看同花，再用哈希表数点数：凑到 3 张立刻返回，2 张只记个标记',
        complexity='时间 `O(1)`（只有 5 张牌），空间 `O(1)`',
        problem=['5 张牌，点数 `ranks[i]`，花色 `suits[i]`',
                 '牌型从好到坏：`Flush` > `Three of a Kind` > `Pair` > `High Card`',
                 '本视频：`[4,2,4,9,4]` + `a,a,b,c,d` → `Three of a Kind`'],
        quote='func bestHand(ranks []int, suits []byte) string { if bytes.Count(suits, suits[:1]) == 5 { return "Flush" } ...',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['数一数 `suits[0]` 出现几次，等于 5 就是同花',
              '遍历点数并计数：次数到 3 ==立刻返回==，到 2 只打 `pair` 标记',
              '遍历完看标记：有对子返回 `Pair`，否则 `High Card`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`bytes.Count` → `list.count`，`map` → `defaultdict`）',
                 '时间 `O(1)`，空间 `O(1)`：牌数固定为 5',
                 '易错：对子不能马上返回，后面可能还有第三张同点数的牌',
                 '同花优先级最高，必须先判断'],
    ),
)

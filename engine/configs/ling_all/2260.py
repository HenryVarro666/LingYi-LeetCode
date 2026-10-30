PTR_P = 'p if ok and _line >= 7 else None'


def _hit(S):
    """当前这个 v 之前出现过吗：p、ok 只在第 6 行之后才是本轮的值"""
    return 'ok' in S and S.get('_line', 0) >= 7 and S['ok']


def _wl(S):
    return S['p'] if _hit(S) else None


def _info(S):
    if 'pos' not in S:
        return ''
    ans, n = S['ans'], len(S['cards'])
    best = f'目前最短匹配段 = ==`{ans}`== 张' if ans <= n else '还没找到匹配的一对（`ans = n + 1` 表示无解）'
    if _hit(S):
        return f'`{S["v"]}` 上次在下标 `{S["p"]}` → 拿起 `cards[{S["p"]}..{S["i"]}]`，共 `{S["i"] - S["p"] + 1}` 张。' + best
    return best


CONFIG = dict(
    num=2260, title='必须拿起的最小连续卡牌数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 哈希表记最近下标（Go 原文转写）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1365'],
    code='''
class Solution:
    def minimumCardPickup(self, cards: List[int]) -> int:
        ans = len(cards) + 1
        pos = {}
        for i, v in enumerate(cards):
            p, ok = pos.get(v, 0), v in pos
            if ok and i - p + 1 < ans:  # 找最近出现的 v
                ans = i - p + 1
            pos[v] = i
        if ans <= len(cards):
            return ans
        return -1
''',
    call='Solution().minimumCardPickup([3, 4, 2, 3, 4, 7])',
    expect=4,
    views=[
        dict(type='array', var='cards', label='cards（蓝 = 当前牌 v，粉 p = v 上次出现处，青框 = 要拿起的牌）', cell=96, h=215,
             pointers={'i': 'blue', PTR_P: 'pink'},
             pointer_labels={PTR_P: 'p'},
             window=(_wl, 'i'),
             color=lambda S, i, v: 'blue' if i == S.get('i') else None),
        dict(type='map', var='pos', label='pos（牌面 → 最近一次出现的下标）', h=170, font=32),
        dict(type='text', fn=_info, size=28, h=110),
    ],
    watch=[('i', 'i', 'blue'), ('v', 'v'), ('p', 'p', 'pink'), ('ok', 'ok'), ('ans', 'ans', 'green')],
    skip=[],
    captions={
        'ans = len(cards) + 1': '`ans` 先设成 `len(cards) + 1 = {ans}`：比任何合法答案都大，最后还是它就说明==无解==',
        'pos = {}': '`pos` 记录每种牌==最近一次出现==的下标',
        'for i, v in enumerate(cards)': lambda S, B, r: (f'枚举右端点：`i = {S.i}`，这张牌是 `v = {S.v}`' if 'i' not in B or S.i != B.i
                                                         else '所有牌都看完了'),
        'p, ok = pos.get(v, 0)': lambda S, B, r: (f'`{S.v}` 之前在下标 `p = {S.p}` 出现过（`ok = True`）' if S.ok
                                                  else f'`{S.v}` 以前没出现过（`ok = False`）'),
        'if ok and': lambda S, B, r: (f'`ok` 为假 → `{S.v}` 没有同伴，跳过' if not S.ok else
                                      (f'拿起 `{S.p}..{S.i}`：`{S.i} - {S.p} + 1 = {S.i - S.p + 1}` < 当前 `ans = {S.ans}` → ==成立，更短=='
                                       if S.i - S.p + 1 < S.ans else
                                       f'拿起 `{S.p}..{S.i}`：`{S.i - S.p + 1}` ≥ 当前 `ans = {S.ans}` → 不更短，不更新')),
        'ans = i - p + 1': '`ans = {i} - {p} + 1` = =={ans}==：这一对匹配牌之间的牌都要拿起',
        'pos[v] = i': '把 `{v}` 的最近下标改成 `{i}`：之后再遇到 `{v}`，==只和最近的一张配对==才最短',
        'if ans <= len(cards)': lambda S, B, r: (f'`ans = {S.ans} ≤ n = {len(S.cards)}` → 找到过匹配的一对' if S.ans <= len(S.cards)
                                                 else f'`ans = {S.ans} > n` → 一对都没找到'),
        'return ans': '返回最少要拿起的牌数 =={ret}==',
        'return -1': '没有匹配的牌，返回 `-1`',
    },
    cards=dict(
        one_liner='枚举右端点，只和最近出现的同值牌配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['拿起一段==连续==的牌，要求其中有两张值相同（匹配）',
                 '求最少拿起几张；拿不出匹配的一对就返回 `-1`',
                 '示例：`cards = [3,4,2,3,4,7]` → `4`（拿起 `[3,4,2,3]`）'],
        quote='找最近出现的 v',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['最优的一段必然是==首尾两张牌相同==，中间没有这个值',
              '枚举右端点 `i`，用哈希表 `pos` 记下每个值最近一次出现的下标 `p`',
              '`i - p + 1` 就是以 `i` 结尾、含匹配对的最短长度，取最小；然后把 `pos[v]` 更新成 `i`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`p, ok := pos[v]` 对应 `pos.get(v, 0)` 和 `v in pos`）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：长度是 `i - p + 1`，别漏了 `+ 1`',
                 '易错：`pos[v]` 要无论是否更新答案都刷新，保证记的是最近一次',
                 '同类题：枚举右、维护左的哈希表套路，如两数之和'],
    ),
)

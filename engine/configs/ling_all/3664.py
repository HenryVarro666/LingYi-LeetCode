CARDS = ['ab', 'ab', 'ac', 'ba', 'ca', 'da', 'aa', 'aa', 'aa', 'aa']


def _col(S, i, v):
    x = S.get('x')
    if x is None:
        return None
    if v == x + x:
        return 'green'
    if v[0] == x:
        return 'blue'
    if v[1] == x:
        return 'pink'
    return None


def _legend(S):
    x = S.get('x', 'a')
    return (f'牌分三类：蓝 = `{x}?`（第一组），粉 = `?{x}`（第二组），绿 = ==`{x}{x}`==（两组都能用）')


def _ifxx(S, B, ret):
    if 'mn' not in S:
        return ('还有 `xx` 吗？`cnt_xx = {}` > 0 → 先把 xx 和剩下的牌配对'.format(S.cnt_xx) if S.cnt_xx > 0
                else '`cnt_xx = 0`，没有 xx，不用处理')
    return ('还剩 xx 吗？`cnt_xx = {}` > 0 → 再考虑撤销旧配对'.format(S.cnt_xx) if S.cnt_xx > 0
            else '`cnt_xx = 0`：xx 已经全部用掉')


CONFIG = dict(
    num=3664, title='两个字母卡牌游戏', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分组配对 · 数学公式 O(1) 处理 xx',
    tags=['灵神题单', '难度分 2158'],
    code='''
class Solution:
    # 计算这一组的得分（配对个数），以及剩余元素个数
    def calc(self, cnt: Dict[str, int]) -> Tuple[int, int]:
        sum_cnt = sum(cnt.values())
        max_cnt = max(cnt.values(), default=0)
        pairs = min(sum_cnt // 2, sum_cnt - max_cnt)
        return pairs, sum_cnt - pairs * 2

    def score(self, cards: List[str], x: str) -> int:
        cnt = Counter(cards)
        cnt_xx = cnt.pop(x + x, 0)
        cnt1 = {b: c for (a, b), c in cnt.items() if a == x}  # 统计 "x?" 中的 ? 的出现次数
        cnt2 = {a: c for (a, b), c in cnt.items() if b == x}  # 统计 "?x" 中的 ? 的出现次数

        pairs1, left1 = self.calc(cnt1)
        pairs2, left2 = self.calc(cnt2)
        ans = pairs1 + pairs2  # 不考虑 xx 时的得分

        # 把 xx 和剩下的 x? 和 ?x 配对
        # 每有 1 个 xx，得分就能增加一，但这不能超过剩下的 x? 和 ?x 的个数 left1+left2
        if cnt_xx > 0:
            mn = min(cnt_xx, left1 + left2)
            ans += mn
            cnt_xx -= mn

        # 如果还有 xx，就撤销之前的配对，比如 (ax,bx) 改成 (ax,xx) 和 (bx,xx)
        # 每有 2 个 xx，得分就能增加一，但这不能超过之前的配对个数 pairs1+pairs2
        # 由于这种方案平均每个 xx 只能增加 0.5 分，不如上面的，所以先考虑把 xx 和剩下的 x? 和 ?x 配对，再考虑撤销之前的配对
        if cnt_xx > 0:
            ans += min(cnt_xx // 2, pairs1 + pairs2)

        return ans
''',
    call="Solution().score(CARDS, 'a')",
    setup="CARDS = ['ab', 'ab', 'ac', 'ba', 'ca', 'da', 'aa', 'aa', 'aa', 'aa']",
    expect=5,
    views=[
        dict(type='text', fn=_legend, h=60),
        dict(type='array', var='cards', color=_col, h=130, cell=70),
        dict(type='map', var='cnt1', label='cnt1：x? 里 ? 的出现次数（组1 = [配对数, 剩余]）', fmt=lambda k, v: f'x{k}: {v}', h=110),
        dict(type='map', var='cnt2', label='cnt2：?x 里 ? 的出现次数（组2 = [配对数, 剩余]）', fmt=lambda k, v: f'{k}x: {v}', h=110),
    ],
    watch=[('ans', 'ans', 'green'), ('xx', 'cnt_xx', 'green'), ('组1', '[pairs1, left1]', 'blue'), ('组2', '[pairs2, left2]', 'pink')],
    captions={
        'cnt = Counter(cards)': '统计每种牌的张数',
        'cnt_xx = cnt.pop': '`xx` 两组都能用，先拿出来单独记数：`cnt_xx = {cnt_xx}`',
        'cnt1 =': '第一组 `x?`：只看第二个字母 `?`，次数 `{cnt1}`',
        'cnt2 =': '第二组 `?x`：只看第一个字母 `?`，次数 `{cnt2}`',
        'self.calc(cnt1)': '第一组交给 `calc`，求最多配几对、剩几张',
        'self.calc(cnt2)': '第二组同样交给 `calc`',
        'sum_cnt = sum': '这一组共 `{sum_cnt}` 张',
        'max_cnt = max': '出现最多的 `?` 有 `{max_cnt}` 张',
        'pairs = min': '配对数 = `min({sum_cnt}//2, {sum_cnt}-{max_cnt})` = =={pairs}==：要么两两配完，要么被最多的那种卡住',
        'return pairs, sum_cnt': '返回：配 `{pairs}` 对，剩 `{sum_cnt - pairs*2}` 张没配',
        'ans = pairs1 + pairs2': '不考虑 xx：`ans = {pairs1} + {pairs2}` = =={ans}==',
        'if cnt_xx > 0': _ifxx,
        'mn = min': '每个 xx 配一张剩牌就 +1 分：`mn = min({cnt_xx}, {left1}+{left2})` = =={mn}==',
        'ans += mn': '`ans` = {B.ans} + {mn} = =={ans}==',
        'cnt_xx -= mn': '用掉 {mn} 个 xx，还剩 `cnt_xx = {cnt_xx}`',
        'ans += min(cnt_xx': '剩下的 xx 要拆旧配对：每 2 个 xx 才 +1 分。`min({cnt_xx}//2, {pairs1}+{pairs2})` → `ans` = =={ans}==',
        'return ans': '最多得 =={ans}== 分',
    },
    cards=dict(
        one_liner='xx 两组都能用：先配剩牌，再拆旧配对',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['每张牌是两个字母，给定字母 `x`；每轮取两张都含 `x` 的牌，要求恰好一个位置不同，得 1 分',
                 '求最多能得几分',
                 '示例：`["aa","ab","ba","ac"], x="a"` → `2`'],
        quote='字符串 xx 在两组中都有。……每有 1 个 xx，得分就能增加一，但这不能超过剩下的字符串个数；如果还有 xx，就撤销之前的配对，每有 2 个 xx，得分就能增加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能选的牌分两组：`x?` 和 `?x`，两组互相独立，唯一的公共牌是 `xx`',
              '每组问题 = 「每次删两个不同元素」，最多 `min(n//2, n-m)` 次',
              '`xx` 先配剩下的牌（每个 +1 分），还有多就撤销旧配对（每 2 个 +1 分）'],
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '先 `pop` 掉 `xx`，两组才能独立计算',
                 '顺序不能反：配剩牌平均每个 xx 得 1 分，撤销旧配对只有 0.5 分',
                 '优化前的写法是枚举分给第一组多少个 xx，再取最大值'],
    ),
)

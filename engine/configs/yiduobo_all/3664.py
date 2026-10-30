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
    return f'卡牌分三类：蓝 = `xy`，粉 = `yx`，绿 = ==`xx`==（这里 x = `{x}`）'


def _case(S, B, ret):
    if S.tot_xy + S.tot_yx < S.xx:
        return f'`{S.tot_xy} + {S.tot_yx} < xx = {S.xx}`：xx 太多，配不完 → 答案就是 xy 与 yx 的总数'
    return f'`{S.tot_xy} + {S.tot_yx} ≥ xx = {S.xx}`：xx 不算多 → 先内部配对，xx 只作补位'


def _rest(S, B, ret):
    r = S.rest_xy + S.rest_yx
    if r > S.xx:
        return f'`rest = {r} > xx = {S.xx}`：xx 不够补完 → 额外只能配 `xx` 对'
    return f'`rest = {r} ≤ xx = {S.xx}`：xx 补完剩牌后，还能拆旧配对 → 额外 `({r} + {S.xx}) // 2` 分'


CONFIG = dict(
    num=3664, title='两个字母卡牌游戏', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='分类讨论 · xy / yx / xx',
    tags=['灵神题单', '贪心与思维', '难度分 2158'],
    code='''
class Solution(object):
    def score(self, cards, x):
        
        xx = 0
        xy = {}
        yx = {}
        for c in cards:
            if c[0] == x:
                if c[1] == x:
                    xx += 1
                else:
                    xy[c] = xy.get(c, 0) + 1
            elif c[1] == x:
                yx[c] = yx.get(c, 0) + 1

        def calc(cnt):
            tot = 0
            ma = 0
            for v in cnt.values():
                tot += v
                ma = max(ma, v)

            if tot - ma >= ma:
                pair = tot // 2
            else:
                pair = tot - ma
            rest = tot - pair * 2
            return tot, pair, rest

        tot_xy, pair_xy, rest_xy = calc(xy)
        tot_yx, pair_yx, rest_yx = calc(yx)

        if tot_xy + tot_yx < xx:
            return tot_xy + tot_yx
        
        res = pair_xy + pair_yx
        if rest_xy + rest_yx > xx:
            res += xx
        else:
            res += (rest_xy + rest_yx + xx) // 2
        
        return res
''',
    call="Solution().score(['aa', 'ab', 'aa', 'ab', 'ac', 'aa', 'ba', 'aa', 'ca', 'da'], 'a')",
    expect=5,
    views=[
        dict(type='text', fn=_legend, h=60),
        dict(type='array', var='cards', color=_col, h=130, cell=70),
        dict(type='map', var='xy', label='xy：每种牌的张数', fmt=lambda k, v: f'{k}: {v}', h=110),
        dict(type='map', var='yx', label='yx：每种牌的张数', fmt=lambda k, v: f'{k}: {v}', h=110),
    ],
    max_steps=80,
    watch=[('res', 'res', 'green'), ('xx', 'xx', 'green'), ('xy[总,对,剩]', '[tot_xy, pair_xy, rest_xy]', 'blue'),
           ('yx[总,对,剩]', '[tot_yx, pair_yx, rest_yx]', 'pink')],
    captions={
        'xx = 0': '`xx` 统计 `xx` 型卡牌的张数',
        'xy = {}': '`xy` 记录形如 `x?` 的牌各有几张',
        'yx = {}': '`yx` 记录形如 `?x` 的牌各有几张',
        'for c in cards': lambda S, B, r: ('牌都看完了，循环结束' if ('c' in B and B['c'] == S.c) else f'看一张牌 `{S.c}`'),
        'if c[0] == x': '第一个字母是不是 `{x}`？`{c[0]}` → {"是" if c[0] == x else "否"}',
        'elif c[1] == x': '第一个字母不是 x，看第二个：`{c[1]}` → {"是，这是 yx" if c[1] == x else "不是，不含 x，忽略"}',
        'if c[1] == x': '第一个字母是 x，再看第二个字母：`{c[1]}` → {"也是 x，这是 xx" if c[1] == x else "不是，这是 xy"}',
        'xx += 1': '`xx` → =={xx}==',
        'xy[c] =': '`xy[{c!r}]` = =={xy[c]}==',
        'yx[c] =': '`yx[{c!r}]` = =={yx[c]}==',
        'def calc': '`calc` 算一类牌的：总数、内部最多配几对、剩几张',
        'for v in cnt.values()': '轮到下一种牌：张数 `v = {v}`（取完就结束循环）',
        'tot = 0': '`tot` 记这类牌的总张数',
        'ma = 0': '`ma` 记张数最多的那种牌有几张',
        'tot += v': '累计总数 `tot` = {tot}',
        'ma = max': '出现最多的牌有 `{ma}` 张',
        'if tot - ma >= ma': lambda S, B, r: (f'`{S.tot} - {S.ma} = {S.tot - S.ma}` ≥ `{S.ma}`：最多的那种不占过半 → 可以两两配完' if S.tot - S.ma >= S.ma
                                             else f'`{S.tot} - {S.ma} = {S.tot - S.ma}` < `{S.ma}`：最多的那种超过一半 → 被它卡住'),
        'pair = tot // 2': '能两两配完：`pair = {tot} // 2` = =={pair}==',
        'pair = tot - ma': '被最多的卡住：它和其他牌一一配，`pair = {tot} - {ma}` = =={pair}==',
        'rest = tot': '没配上的 `rest = {tot} - {pair}×2` = =={rest}==，留给 xx 补位',
        'return tot, pair, rest': '返回 (总 {tot}，配 {pair} 对，剩 {rest})',
        'tot_xy, pair_xy, rest_xy = calc': '`xy` 类交给 calc',
        'tot_yx, pair_yx, rest_yx = calc': '`yx` 类同样交给 calc',
        'if tot_xy + tot_yx < xx': _case,
        'return tot_xy + tot_yx': '直接返回 xy 与 yx 的总数',
        'res = pair_xy + pair_yx': '先算内部配对：`res = {pair_xy} + {pair_yx}` = =={res}==',
        'if rest_xy + rest_yx > xx': _rest,
        'res += xx': '额外配对 `xx` 对，`res` → =={res}==',
        'res += (rest_xy': '额外配对 `({rest_xy} + {rest_yx} + {xx}) // 2`，`res` → =={res}==',
        'return res': '最多得 =={res}== 分',
    },
    cards=dict(
        one_liner='先在 xy、yx 内部配对，xx 只当补位的万能牌',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每张牌是两个字母，给定字母 `x`；每轮取两张都含 `x` 的牌，要求恰好一个位置不同，得 1 分',
                 '求最多能得几分',
                 '本视频：`["aa","ab","aa","ab","ac","aa","ba","aa","ca","da"]`，`x = "a"` → `5`'],
        quote='由于移除的牌对必须都包含x，因此可以直接忽略掉不包含x的卡牌。……形如xx的卡牌，其可以与任意xy或者yx形成牌对，但是不能与另一张xx形成牌对。',
        quote_src='—— yiduobo 题解原文',
        idea=['含 x 的牌分三类：`xy`、`yx`、`xx`；`xy` 只能和 `xy`（y 不同）或 `xx` 配',
              '内部配对：最多的那种牌不超过一半就两两配完，否则只能数量差',
              'xx 先补剩下的牌；xx 还多，就拆开旧配对，每 2 个 xx 多得 1 分'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`xx` 特别多（超过 `xy`+`yx` 总数）时，答案就是总数',
                 '`rest ≤ xx` 的分支里，`tot_xy + tot_yx ≥ xx` 保证拆得动',
                 '对比灵神：灵神先配剩牌再撤销配对，分两步写；yiduobo 合并成 `(rest + xx) // 2` 一步'],
    ),
)

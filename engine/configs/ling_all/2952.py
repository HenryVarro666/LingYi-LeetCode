def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tgt = S['target']
    cv.text((x0 + 18, y0 + 4), f'数轴 1 ~ target={tgt}：绿色 = 已经能凑出的金额 [1, s-1]', 24, T['muted'], bold=True)
    if 's' not in S:
        return
    s = S['s']
    L, R = x0 + 30, x1 - 30
    w = (R - L) / tgt
    top = y0 + 50
    h = 70
    for v in range(1, tgt + 1):
        X = L + (v - 1) * w
        ok = v <= s - 1
        fill = T['green'] if ok else (60, 66, 78)
        cv.rect((X + 1, top, X + w - 1, top + h), fill=fill, r=3)
        if tgt <= 24:
            cv.text((X + w / 2, top + h / 2), v, 22, T['bg'] if ok else T['dim'], anchor='mm', bold=True)
    if s <= tgt:
        X = L + (s - 1) * w + w / 2
        cv.tri_up(X, top + h + 22, 11, T['yellow'])
        cv.text((x0 + 30, top + h + 40), f'黄色箭头：s={s}，下一个要凑的金额', 22, T['yellow'], anchor='lt', bold=True)
    else:
        cv.text((L, top + h + 30), f's={s} > target：1~{tgt} 全部覆盖', 24, T['green'], bold=True)


CONFIG = dict(
    num=2952, title='需要添加的硬币的最小数量', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='归纳法 · 维护 [0, s-1]',
    tags=['贪心与思维', '难度分 1784'],
    code='''
class Solution:
    def minimumAddedCoins(self, coins: List[int], target: int) -> int:
        coins.sort()
        ans, s, i = 0, 1, 0
        while s <= target:
            if i < len(coins) and coins[i] <= s:
                s += coins[i]
                i += 1
            else:
                s *= 2  # 必须添加 s
                ans += 1
        return ans
''',
    call='Solution().minimumAddedCoins([4,1,10], 19)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=230),
        dict(type='array', var='coins', h=210, label='coins（排序后）', pointers={'i': 'blue'},
             color=lambda S, i, v: 'dim' if 'i' in S and i < S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i < S['i']),
    ],
    watch=[('s', 's', 'green'), ('i', 'i', 'blue'), ('ans', 'ans', 'yellow')],
    captions={
        'coins.sort()': '先排序：`coins = {coins}`，小面值先用',
        'ans, s, i =': '`s = 1`：已经能凑出 `[0, s-1] = [0, 0]`（空集和为 0），还缺 `s = 1`',
        'while s <= target': lambda S, B, r: (f'`s = {S.s} <= target = {S.target}`：还没覆盖到 `target`，继续' if S.s <= S.target
                                              else f'`s = {S.s} > target = {S.target}`：[1, target] 全部覆盖 → 结束'),
        'if i < len': lambda S, B, r: (f'`coins[{S.i}] = {S.coins[S.i]}` {"<=" if S.coins[S.i] <= S.s else ">"} `s = {S.s}`：' +
                                       ('不会断档 → ==用它扩展区间==' if S.coins[S.i] <= S.s else '凑不出 `s` → ==必须添加 s==')
                                       if S.i < len(S.coins) else f'硬币用完了，`s = {S.s}` 还凑不出 → ==必须添加 s=='),
        's += coins': '`[0, s-1]` 整体加上 `x = {coins[i]}` 得到 `[x, s+x-1]`，合并后 `[0, {s-1}]`：`s` → =={s}==',
        'i += 1': '这枚硬币用掉，`i` → {i}',
        's *= 2': '添加面值 `{B.s}` 的硬币：`[0, s-1]` 与 `[s, 2s-1]` 合并，`s` → =={s}==',
        'ans += 1': '添加了一枚，`ans` → =={ans}==',
        'return ans': '共添加 =={ret}== 枚硬币',
    },
    cards=dict(
        one_liner='维护能凑出 [0, s-1]，凑不出 s 就必须补一枚 s',
        complexity='时间 `O(n log n + log target)`，空间 `O(1)`',
        problem=['给定硬币面值 `coins` 和 `target`，最少添加多少枚任意面值硬币，使 `[1, target]` 内每个整数都能凑出',
                 '示例：`coins=[1,4,10], target=19` → `2`（补 2 和 8）',
                 '本视频：`[4,1,10], target=19` → `2`'],
        quote='假设现在得到了区间 [0,s-1] 中的所有整数，如果此时遍历到整数 x=coins[i]，那么把 [0,s-1] 中的每个整数都增加 x，我们就得到了区间 [x,s+x-1] 中的所有整数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后遍历，维护已凑出的区间 `[0, s-1]`',
              '`x <= s`：两个区间相连，合并成 `[0, s+x-1]`',
              '`x > s`：凑不出 `s`，必须补一枚 `s`（比 `s` 小的补了不够贪），区间翻倍为 `[0, 2s-1]`'],
        summary=['时间 `O(n log n + log target)`，`s` 至多翻倍 `log target` 次',
                 '把 0 也算作可取得的金额，区间写成 `[0, s-1]` 更顺',
                 '遍历完 `coins` 后还要继续翻倍补硬币，直到 `s > target`',
                 '同类题：330 按要求补齐数组、1798'],
    ),
)

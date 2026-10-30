N0 = 30


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'一堆石头（共 {N0} 个）：蓝 = Alice 拿走，粉 = Bob 拿走，灰 = 还剩下', 24, T['muted'], bold=True)
    cell = min(52, (x1 - x0 - 40) / 15)
    per_row = int((x1 - x0 - 40) // cell)
    sx = x0 + 20
    live = 'pick' in S
    rem = S['n'] if live else N0
    removed = N0 - rem
    owner = []
    p, who = 10, 0
    while len(owner) < removed:
        owner += [who] * p
        p -= 1
        who ^= 1
    for i in range(N0):
        r, c = divmod(i, per_row)
        X, Y = sx + c * cell, y0 + 60 + r * (cell + 6)
        if i < removed:
            fill = T['blue'] if owner[i] == 0 else T['pink']
            alpha = 255
        else:
            fill, alpha = (125, 133, 145), 200
        cv.rect((X + 2, Y, X + cell - 2, Y + cell - 4), fill=fill, r=6, alpha=alpha)
    yb = y0 + 60 + ((N0 - 1) // per_row + 1) * (cell + 6) + 20
    if live:
        who_next = 'Alice' if (10 - S['pick']) % 2 == 0 else 'Bob'
        cv.text((x0 + 20, yb), f'剩 {rem} 个，轮到 {who_next} 拿 {S["pick"]} 个', 30, T['text'], bold=True)
        if rem < S['pick']:
            cv.text((x0 + 20, yb + 46), f'{rem} < {S["pick"]}：{who_next} 拿不了 → {who_next} 输', 28, T['orange'], bold=True)


CONFIG = dict(
    num=3360, title='移除石头游戏', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='直接模拟', tags=[],
    code='''
class Solution:
    def canAliceWin(self, n: int) -> bool:
        pick = 10
        while n >= pick:
            n -= pick
            pick -= 1
        return (10 - pick) % 2 > 0
''',
    call='Solution().canAliceWin(30)',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=lambda S: (f'已经拿了 `{10 - S["pick"]}` 次（`10 − pick`）' if 'pick' in S else '规则：每次拿的数量比对方上一次少 1'), h=70, size=28),
    ],
    watch=['n', ('pick', 'pick', 'yellow')],
    captions={
        'pick = 10': 'Alice 第一次必须拿 10 个：`pick = 10` 表示==当前这一手要拿几个==',
        'while n >= pick': lambda S, B, r: (f'剩 `{S.n}` >= 要拿的 `{S.pick}` → 这一手拿得动，继续' if S.n >= S.pick else f'剩 `{S.n}` < 要拿的 `{S.pick}` → ==这个人拿不了，输了==，循环结束'),
        'n -= pick': '拿走 `{B.pick}` 个，石头剩 `{n}`',
        'pick -= 1': '下一个人要拿的比这一手少 1：`pick = {pick}`',
        'return': lambda S, B, r: f'一共拿了 `10 − {S.pick} = {10 - S.pick}` 次；次数是==奇数==说明最后拿的是 Alice，Bob 拿不动 → Alice 赢（`{r}`）',
    },
    cards=dict(
        one_liner='石头最多 50 个，直接模拟：谁先拿不动谁输',
        complexity='时间 `O(C)`，`C = 10`；空间 `O(1)`',
        problem=['Alice 先手，第一次拿 ==恰好 10 个==，之后每人拿「对方上一次数量 − 1」个',
                 '第一个拿不了的人输。给定石头数 `n`，求 Alice 是否获胜',
                 '示例：`n=12` → `true`；`n=1` → `false`；本视频用 `n=30`'],
        quote='两人交替操作，设两人一共操作了 x 次……如果 x 是奇数，Alice 胜，否则 Bob 胜。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`pick` 最多从 10 减到 1，循环至多 10 轮',
              '循环结束时 `pick` 是那个==拿不动的人==要拿的数',
              '已经成功拿了 `10 − pick` 次：奇数次 = 最后一次是 Alice → Alice 赢'],
        summary=['时间 `O(C)`，`C = 10`；空间 `O(1)`',
                 '易错：判断条件是 `10 - pick` 的奇偶，不是 `pick` 本身',
                 '灵神方法二：设操作 x 次，`(21−x)x/2 <= n`，解一元二次不等式得 x，x 为奇数则 Alice 赢，`O(1)`',
                 '先手 Alice 总在第 1、3、5…次拿'],
    ),
)

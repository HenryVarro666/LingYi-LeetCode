def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    full, empty, ex, res = S.get('full'), S.get('empty'), S.get('numExchange'), S.get('res')
    if full is None:
        return
    cell = 56
    cv.text((x0 + 18, y0 + 4), '蓝 = 没喝的满瓶，灰 = 手上的空瓶', 22, T['muted'], bold=True)
    sx = x0 + 40
    per = int((x1 - x0 - 80) // (cell + 8))
    y = y0 + 70
    for label, cnt, col, alpha in (('full', full, 'blue', 210), ('empty', empty, 'dim', 160)):
        cv.text((sx, y), f'{label} = {cnt}', 26, T['text'], bold=True)
        y += 40
        rows = max(1, (cnt + per - 1) // per)
        for k in range(cnt):
            r, c = divmod(k, per)
            cv.rect((sx + c * (cell + 8), y + r * (cell + 8), sx + c * (cell + 8) + cell, y + r * (cell + 8) + cell), fill=T[col], alpha=alpha, r=10)
        y += rows * (cell + 8) + 20
    ok = empty >= ex
    cv.text((sx, y + 6), f'换一瓶要 numExchange = {ex} 个空瓶；empty {">=" if ok else "<"} {ex}', 28, T['yellow'] if ok else T['pink'], bold=True)
    cv.text((sx, y + 60), f'已喝 res = {res}', 28, T['green'], bold=True)


CONFIG = dict(
    num=3100, title='换水问题 II', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · full / empty 两个计数',
    tags=[],
    code='''
class Solution(object):
    def maxBottlesDrunk(self, numBottles, numExchange):

        full = numBottles
        empty = 0
        res = 0
        while full > 0 or empty >= numExchange:
            if full > 0:
                empty += full
                res += full
                full = 0
            
            if empty >= numExchange:
                full += 1
                empty -= numExchange
                numExchange += 1
        
        return res
''',
    call='Solution().maxBottlesDrunk(10, 3)',
    expect=13,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['full', 'empty', 'numExchange', ('res', 'res', 'green')],
    max_steps=60,
    captions={
        'full = numBottles': '`full`：手上还没喝的满瓶，开始是 `{full}`',
        'empty = 0': '`empty`：手上的空瓶，开始为 0',
        'res = 0': '`res`：累计喝掉的瓶数',
        'while full > 0 or empty >= numExchange': lambda S, B, r: (
            f'`full = {S.full}`，`empty = {S.empty}`，换价 `{S.numExchange}` → 还有水可喝或还能换，继续' if (S.full > 0 or S.empty >= S.numExchange)
            else f'`full = 0` 且 `empty = {S.empty} < {S.numExchange}`：没水喝也换不了 → 结束'),
        'if full > 0': '`full = {full}` > 0：有满瓶就先喝掉',
        'empty += full': '喝完的 `{full}` 瓶变成空瓶：`empty` = =={empty}==',
        'res += full': '这 `{full}` 瓶计入答案：`res` = =={res}==',
        'full = 0': '满瓶清零，`full = 0`',
        'if empty >= numExchange': lambda S, B, r: (f'`empty = {S.empty} >= {S.numExchange}`：空瓶够 → ==换一瓶==' if S.empty >= S.numExchange
                                                    else f'`empty = {S.empty} < {S.numExchange}`：空瓶不够，不能换'),
        'full += 1': '换到 1 瓶满的：`full` = =={full}==',
        'empty -= numExchange': '付出 `{B.numExchange}` 个空瓶：`empty` = =={empty}==',
        'numExchange += 1': '按题目要求，换价 +1 → `numExchange` = =={numExchange}==',
        'return res': '一共喝了 `{res}` 瓶',
    },
    cards=dict(
        one_liner='喝光满瓶、攒空瓶、够了就换，换价每次 +1',
        complexity='时间 `O(√numBottles)`，空间 `O(1)`',
        problem=['`numBottles` 个满瓶，`numExchange` 个空瓶换 1 个满瓶，每换一次 `numExchange` 加 1',
                 '求最多能喝多少瓶',
                 '示例：`10, 3` → `13`'],
        quote='若手上还有没喝的，就全部喝掉，此时需要将full分别累加到答案和empty中，然后将full清零。',
        quote_src='—— yiduobo 题解原文',
        idea=['`full` 是没喝的、`empty` 是空瓶',
              '有 `full` 就全喝：加到 `res` 和 `empty`，`full` 清零',
              '`empty >= numExchange` 就换：`full` +1，`empty` 减去换价，换价 +1'],
        summary=['时间 `O(√numBottles)`，空间 `O(1)`；数据规模小，直接模拟',
                 '循环条件是 `full > 0 or empty >= numExchange`：换来的瓶子还得再喝',
                 '每次最多换 1 瓶，所以 `full += 1` 而不是批量换',
                 '原文就是 Python 3 可运行写法，未做修改'],
    ),
)

def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, e, ans = S.get('numBottles'), S.get('numExchange'), S.get('ans')
    if n is None:
        return
    cell = 64
    cv.text((x0 + 18, y0 + 4), '手里的满瓶（蓝），已喝掉的瓶数在 ans（绿）', 22, T['muted'], bold=True)
    sx, sy = x0 + 40, y0 + 70
    per = int((x1 - x0 - 80) // (cell + 8))
    for k in range(n):
        r, c = divmod(k, per)
        cv.rect((sx + c * (cell + 8), sy + r * (cell + 8), sx + c * (cell + 8) + cell, sy + r * (cell + 8) + cell), fill=T['blue'], alpha=200, r=10)
    rows = max(1, (n + per - 1) // per)
    yb = sy + rows * (cell + 8) + 30
    cv.text((sx, yb), f'本轮换水需要 numExchange = {e} 个空瓶；满瓶 {n} {">=" if n >= e else "<"} {e}', 28, T['yellow'] if n >= e else T['pink'], bold=True)
    cv.text((sx, yb + 56), f'已经喝掉 ans = {ans}', 28, T['green'], bold=True)


CONFIG = dict(
    num=3100, title='换水问题 II', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 每次换水价格 +1',
    tags=[],
    code='''
class Solution:
    def maxBottlesDrunk(self, numBottles: int, numExchange: int) -> int:
        ans = 0
        while numBottles >= numExchange:
            ans += numExchange  # 吨吨吨~
            numBottles -= numExchange - 1
            numExchange += 1
        return ans + numBottles
''',
    call='Solution().maxBottlesDrunk(10, 3)',
    expect=13,
    views=[dict(type='custom', draw=_draw, h=500)],
    watch=['numBottles', 'numExchange', ('ans', 'ans', 'green')],
    max_steps=40,
    captions={
        'ans = 0': '`ans` 记录已经喝掉的瓶数',
        'while numBottles >= numExchange': lambda S, B, r: (
            f'`{S.numBottles} >= {S.numExchange}`：喝光后空瓶够换一瓶 → ==继续换==' if S.numBottles >= S.numExchange
            else f'`{S.numBottles} < {S.numExchange}`：瓶数不够换了 → 结束'),
        'ans += numExchange': '吨吨吨~ 先把 `{numExchange}` 瓶喝掉，`ans` = =={ans}==',
        'numBottles -= numExchange - 1': '喝掉 `{numExchange}` 瓶，换回 1 瓶：净减少 `{numExchange - 1}` → `numBottles` = =={numBottles}==',
        'numExchange += 1': '题目规定：每换一次，兑换价 +1 → `numExchange` = =={numExchange}==',
        'return ans + numBottles': '剩下的 `{numBottles}` 瓶直接喝掉：`{ans} + {numBottles}` = =={ret}==',
    },
    cards=dict(
        one_liner='喝掉 e 瓶换回 1 瓶，等于净少 e−1 瓶，且 e 每次加 1',
        complexity='时间 `O(√numBottles)`，空间 `O(1)`',
        problem=['有 `numBottles` 个满瓶，喝完变空瓶；`numExchange` 个空瓶换 1 个满瓶，每换一次 `numExchange` 加 1',
                 '求最多能喝多少瓶',
                 '示例：`10, 3` → `13`'],
        quote='本题和 1518. 换水问题 几乎一样，唯一区别是每次循环要把 numExchange 加一。',
        quote_src='—— 灵茶山艾府题解（方法一：模拟）',
        idea=['能换水时，把 `numExchange` 个满瓶喝掉，换回 1 个满瓶',
              '所以满瓶数净减少 `numExchange - 1`，`ans` 加上 `numExchange`',
              '换完 `numExchange += 1`，直到满瓶不够为止，剩下的直接喝'],
        summary=['时间 `O(√numBottles)`：`numExchange = 1` 是最坏情况，约循环 √(2n) 次',
                 '灵神方法二：解二次不等式，`isqrt` 直接算出额外换到的瓶数 `k`，`O(1)`',
                 '易错点：循环里别漏了 `numExchange += 1`，也别忘了最后加上剩余的 `numBottles`',
                 '同类：1518. 换水问题'],
    ),
)

import math

N0, A0 = 6, 2   # 示例：6 个点，第一次拆成 2 + 4


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = N0
    cx, cy, R = (x0 + x1) / 2, y0 + 205, 135
    pts = [(cx + R * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + R * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    cv.text((x0 + 18, y0 + 4), f'完全图 K{n}：每对点连一条边，共 C({n},2) = {n * (n - 1) // 2} 条', 24, T['muted'], bold=True)
    for i in range(n):
        for j in range(i + 1, n):
            ina, inb = i < A0, j < A0
            if ina != inb:
                cv.line([pts[i], pts[j]], T['orange'], 4)      # 这次拆分断开的边
            else:
                cv.line([pts[i], pts[j]], T['border'], 2)
    for i, (px, py) in enumerate(pts):
        c = T['blue'] if i < A0 else T['pink']
        cv.d.ellipse((px - 22, py - 22, px + 22, py + 22), fill=c)
        cv.text((px, py), i + 1, 24, T['bg'], anchor='mm', bold=True)
    a, b = A0, n - A0
    rx = x0 + 40
    lines = [
        (f'拆成 A（蓝）{a} 个点 + B（粉）{b} 个点', T['text']),
        (f'代价 a·b = {a} × {b} = {a * b}：正好是 A、B 之间被断开的边（橙）', T['orange']),
        (f'A 内部还剩 C({a},2) = {a * (a - 1) // 2} 条边，递归处理', T['blue']),
        (f'B 内部还剩 C({b},2) = {b * (b - 1) // 2} 条边，递归处理', T['pink']),
        (f'合计 {a * b} + {a * (a - 1) // 2} + {b * (b - 1) // 2} = {n * (n - 1) // 2}', T['green']),
    ]
    for k, (t, c) in enumerate(lines):
        cv.text((rx, y0 + 385 + k * 52), t, 26, c, bold=(k == 4))


CONFIG = dict(
    num=3857, title='拆分到 1 的最小总代价', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='等价转化 · 断边计数',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def minCost(self, n: int) -> int:
        return n * (n - 1) // 2
''',
    call=f'Solution().minCost({N0})',
    expect=15,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['n'],
    captions={
        'return': '任意拆分方案的总代价都是 `C(n,2)`：`{n} * ({n} - 1) // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='把拆分看成断边：任意方案的总代价都是 n(n-1)/2',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把整数 `x` 拆成正整数 `a + b`，代价 `a * b`',
                 '求把 `n` 拆成 `n` 个 `1` 的最小总代价',
                 '示例：`n = 3` → `3`，`n = 4` → `6`；本视频：`n = 6` → `15`'],
        quote='对于任意划分（拆分）方案，得到的答案都是 n(n-1)/2。所以我觉得这题很神奇，只要你的代码最终能拆分成 n 个 1，计算结果就是对的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['想象 `n` 个点的完全图，共 `C(n,2)` 条边',
              '把点分成 `a`、`b` 两组，断开两组之间的 `a·b` 条边——正好是这次的代价',
              '再递归处理两组；直到每组只剩 1 个点，所有边都断开了',
              '每条边恰好被断一次 → 总代价就是边数'],
        after=[dict(heading='附：记忆化搜索', lines=[
            '题解还给了 `dfs(n) = min(dfs(a) + dfs(b) + a*b)`，枚举 `a`，`O(n²)`',
            '所有拆法结果相同，所以把 min 换成 max，答案也不变',
            '这里的视频只演示 `O(1)` 公式写法'])],
        result='`6 × 5 // 2 = 15`，与怎么拆无关 ✓',
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：是 `n * (n - 1) // 2`，别写成 `n * n // 2`',
                 '最大总代价也是同一个值',
                 '同类思路：把操作转化成“每个对象恰好处理一次”再计数'],
    ),
)

def _rows_needed(a):
    r = 1
    while r * (r + 1) // 2 < a:
        r += 1
    return r


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n', 0)
    ans = S.get('ans', 0)
    mx = S.get('max_n', 0)
    old = B.get('ans', ans) if B else ans
    cv.text((x0 + 18, y0 + 4), f'盒子上限 max_n（目标 n = {n}）', 24, T['muted'], bold=True)
    W = x1 - x0 - 60
    by = y0 + 50
    cv.rect((x0 + 30, by, x0 + 30 + W, by + 40), fill=T['panel2'], r=10, outline=T['border'])
    fr = min(1.0, mx / n) if n else 0
    if fr > 0:
        cv.rect((x0 + 30, by, x0 + 30 + W * fr, by + 40), fill=T['blue'], r=10, alpha=200)
    cv.text((x0 + 40, by + 20), f'max_n = {mx}', 24, T['text'], anchor='lm', bold=True)
    cv.text((x0 + 30 + W - 10, by + 20), f'n = {n}', 24, T['yellow'] if mx >= n else T['muted'], anchor='rm', bold=True)
    cv.text((x0 + 18, by + 70), f'接触地面的盒子 ans = {ans}（地板上按 1,2,3… 的阶梯排）', 24, T['muted'], bold=True)
    rows = max(4, _rows_needed(max(ans, 1)))
    cell = min(64, (y1 - (by + 130) - 20) / rows, (x1 - x0 - 80) / rows)
    k = 0
    for r in range(1, rows + 1):
        for c in range(r):
            X = x0 + 40 + c * cell
            Y = by + 120 + (r - 1) * cell
            if k < ans:
                fill = T['yellow'] if k >= old else T['green']
                cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=8)
            else:
                cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), outline=T['border'], r=8, width=2)
            k += 1
        cv.text((x0 + 40 + r * cell + 14, by + 120 + (r - 1) * cell + cell / 2), f'第 {r} 行 · {r} 个', 18, T['dim'], anchor='lm')


def _p1(S, B, ret):
    i, ans, mx = S.i, S.ans, S.max_n
    return f'先问：把地面再加 `{i}` 个（变成 `{ans + i}`），上限 `{mx} + {ans + i} = {mx + ans + i}` 还 `<= {S.n}` 吗？' + ('==成立，整层铺满==' if mx + ans + i <= S.n else '==不成立，整层放不下==')


CONFIG = dict(
    num=1739, title='放置盒子', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='阶梯堆叠 · 先整层后补行',
    tags=['灵神题单', '难度分 2198'],
    code='''
class Solution:
    def minimumBoxes(self, n: int) -> int:
        ans = max_n = 0
        i = j = 1
        while max_n + ans + i <= n:
            ans += i
            max_n += ans
            i += 1
        while max_n < n:
            ans += 1
            max_n += j
            j += 1
        return ans
''',
    call='Solution().minimumBoxes(7)',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['n', ('ans', 'ans', 'green'), ('max_n', 'max_n', 'blue'), 'i', 'j'],
    captions={
        'ans = max_n = 0': '`ans` 是接触地面的盒子数，`max_n` 是此时最多能放多少个盒子，都从 0 开始',
        'i = j = 1': '`i` 是下一层要加的地面盒子数，`j` 是补行时的计数，都从 1 开始',
        'while max_n + ans + i <= n': _p1,
        'ans += i': '整层加入：地面多 `{i}` 个，`ans` = =={ans}==',
        'max_n += ans': '新的最大盒子数：旧上限加上当前地面数 `{ans}` → `max_n` = =={max_n}==（对应 `i(i+1)(i+2)/6`）',
        'i += 1': '下一层要加的地面盒子数 `i` → {i}',
        'while max_n < n': lambda S, B, r: (f'整层放不下了，`max_n = {S.max_n} < n = {S.n}` → 还差 {S.n - S.max_n} 个，进入补行' if S.max_n < S.n else f'`max_n = {S.max_n} >= n = {S.n}`：够放 n 个盒子 → 结束'),
        'ans += 1': '再多放 1 个地面盒子：`ans` = =={ans}==',
        'max_n += j': '第 `{j}` 个新增地面盒子，让上限多出 `1+2+…+j` 的最后一项 `{j}` → `max_n` = =={max_n}==',
        'j += 1': '下一个新增地面盒子能多撑 `{j}` 个',
        'return ans': '接触地面的盒子最少 =={ans}== 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='墙角堆成阶梯：地面 1,2,3… 个，上面逐层叠',
        complexity='时间 `O(n^(1/3))`，空间 `O(1)`',
        problem=['立方房间里放 `n` 个单位盒子；盒子 `x` 放在 `y` 上面时，`y` 的四个侧面都要有盒子或墙',
                 '求接触地面的盒子最少有几个',
                 '示例：`n=3 → 3`，`n=4 → 3`，`n=10 → 6`；本视频用 `n=7`'],
        quote='接触地面的盒子 ans 等于 1+2+3+⋯+i 时，对应的盒子上限 maxN 为 1+(1+2)+(1+2+3)+⋯+i(i+1)(i+2)/6',
        quote_src='—— 灵茶山艾府题解',
        idea=['先放满整层阶梯：地面 `1+2+…+i`，总数上限是四面体数 `i(i+1)(i+2)/6`',
              '放不下整层时，再往地面一个个补：补第 `j` 个能多撑 `j` 个盒子',
              '代码把 `x` 和 `y` 直接加进 `ans`：第一个循环加整层，第二个循环补行'],
        summary=['时间 `O(n^(1/3))`：`i`、`j` 至多是 n 的立方根量级',
                 '第一个循环的条件是「整层放得下」：`max_n + ans + i <= n`，别写成 `<`',
                 '灵神还给了 `O(1)` 写法：用 `floor(cbrt(6n))` 直接算 `x`，再解 `y(y+1)/2 >= N`；这里演示更直观的循环版（`cbrt` 在 Python 3.10 没有）'],
    ),
)

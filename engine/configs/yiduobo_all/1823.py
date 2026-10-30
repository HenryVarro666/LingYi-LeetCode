K = 3


def _size(S, B=None):
    if 'index' not in S:
        return 1
    if S.get('_line') == 6 or (B is not None and B.get('index') == S['index']):
        return S['index']
    return S['index'] - 1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S['n']
    s = _size(S, B)
    res = S['res']
    cv.text((x0 + 18, y0 + 4), f'当前 {s} 个人围成一圈（绿 = 幸存者 f，红框 = 这一轮报到 k 的人，他被淘汰）', 22, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    ys = y0 + 120
    ch = cell * 0.85
    out = (K - 1) % s + 1
    for i in range(n):
        X = sx + i * cell
        if i >= s:
            cv.rect((X + 5, ys, X + cell - 5, ys + ch), fill=T['bg'], outline=T['border'], r=10)
            cv.text((X + cell / 2, ys + ch / 2), i + 1, 30, T['dim'], anchor='mm', bold=True, mono=True)
            continue
        fill = T['green'] if i + 1 == res else T['panel2']
        cv.rect((X + 5, ys, X + cell - 5, ys + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), i + 1, 38, T['bg'] if fill == T['green'] else T['text'], anchor='mm', bold=True, mono=True)
        if i + 1 == out and s > 1:
            cv.rect((X + 1, ys - 4, X + cell - 1, ys + ch + 4), outline=T['red'], width=5, r=12)
    cv.text((sx + (res - 1) * cell + cell / 2, ys + ch + 14), f'f({s}) = {res}', 24, T['green'], anchor='mt', bold=True)
    if 'index' in S and S.get('_line') == 6 and s > 1:
        yb = ys + ch + 90
        cv.text((x0 + 18, yb), f"上一轮 {s - 1} 人时幸存者是 {B['res']} 号 → 淘汰 {out} 号后重新编号，在 {s} 人时对应 ({B['res']} + {K} − 1) % {s} + 1 = {res}", 22, T['text'], bold=True)


CONFIG = dict(
    num=1823, title='找出游戏的获胜者', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='约瑟夫环 · 递推映射',
    tags=[],
    code='''
class Solution(object):
    def findTheWinner(self, n, k):

        res = 1
        for index in range(2, n + 1):
            res = (res + k - 1) % index + 1
        return res
''',
    call='Solution().findTheWinner(7, 3)',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', fn=lambda S: '递推：`f[n] = (f[n-1] + k - 1) % n + 1`，`f[1] = 1`', size=30, h=80),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 1': '`f[1] = 1`：只有 1 个人，幸存者就是 1 号',
        'for index in': lambda S, B, r: (f'`index` 已经到 `n = {S.index}`，循环结束' if B.get('index') == S.index else f'人数增加到 `index = {S.index}`，由 `f[{S.index - 1}]` 推出 `f[{S.index}]`'),
        'res = (res': '`f[{index}] = ({B.res} + {k} - 1) % {index} + 1` = =={res}==：上一轮的编号要整体平移 `k` 位，再绕回一圈',
        'return res': '`n = {n}` 个人时，幸存者是 =={res}== 号',
    },
    cards=dict(
        one_liner='n 个人淘汰一个变成 n−1 个人，编号整体平移 k 位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 个人围成一圈，从 1 号开始报数，数到 `k` 的人出局，下一人重新从 1 报起',
                 '求最后留下的人的编号（约瑟夫环）',
                 '示例：`n = 7, k = 3` → `4`'],
        quote='令f[n]表示n个人时最终幸存者的编号，那么在执行一轮之后，就有新的f[n - 1]号对应的是原来n个人中(f[n - 1] + m - 1) % n + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['淘汰一人后剩 `n-1` 人，新的 1 号是原来被淘汰者的下一位',
              '所以 `n-1` 人时的编号 `f` 对应 `n` 人时的 `(f + m - 1) % n + 1`',
              '其中 `m = k % n`，模 `n` 的部分可以并进去，得 `(f + k - 1) % n + 1`，从 `f[1] = 1` 递推'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先 `-1` 再 `% index` 最后 `+1`：编号从 1 开始，要换成 0 起点再换回',
                 '循环从 `index = 2` 开始，`f[1] = 1` 是初值',
                 '原文还提了跳过整段“连续加 k”的优化，但没有实现'],
    ),
)

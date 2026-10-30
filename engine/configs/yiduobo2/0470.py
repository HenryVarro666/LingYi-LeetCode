GROUP = [(88, 166, 255), (247, 120, 186), (63, 185, 80), (188, 140, 255), (57, 197, 207),
         (227, 179, 65), (255, 166, 87), (130, 150, 255), (120, 200, 150), (230, 130, 120)]


def _ab(tmp):
    return (tmp - 1) // 7 + 1, (tmp - 1) % 7 + 1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '7×7 = 49 种等概率结果：行 = 第 1 次 rand7()，列 = 第 2 次 rand7()', 22, T['muted'], bold=True)
    size = min(62, (y1 - y0 - 150) / 7)
    sx = x0 + 120
    sy = y0 + 104
    tmp = S.get('tmp') if S.get('_line', 0) >= 8 else None
    for c in range(7):
        cv.text((sx + c * size + size / 2, sy - 8), c + 1, 20, T['muted'], anchor='mb', mono=True)
    for r in range(7):
        cv.text((sx - 12, sy + r * size + size / 2), r + 1, 20, T['muted'], anchor='rm', mono=True)
    cv.text((sx + 3.5 * size, sy - 36), '第 2 次 rand7() →', 18, T['dim'], anchor='mb')
    cv.text((sx - 44, sy + 3.5 * size), '第1次', 18, T['dim'], anchor='rm')
    for r in range(7):
        for c in range(7):
            v = r * 7 + c + 1
            X, Y = sx + c * size, sy + r * size
            if v <= 40:
                g = (v - 1) // 4
                cv.rect((X + 2, Y + 2, X + size - 2, Y + size - 2), fill=GROUP[g], r=6, alpha=200)
                cv.text((X + size / 2, Y + size / 2 + 2), g + 1, int(size * 0.42), T['bg'], anchor='mm', bold=True)
            else:
                cv.rect((X + 2, Y + 2, X + size - 2, Y + size - 2), fill=(40, 45, 53), r=6)
                cv.text((X + size / 2, Y + size / 2 + 2), '×', int(size * 0.42), T['dim'], anchor='mm', bold=True)
            cv.text((X + 5, Y + 4), v, 12, T['bg'] if v <= 40 else T['dim'], mono=True)
    if tmp is not None:
        r, c = (tmp - 1) // 7, (tmp - 1) % 7
        X, Y = sx + c * size, sy + r * size
        col = T['yellow'] if tmp <= 40 else T['red']
        cv.rect((X - 3, Y - 3, X + size + 3, Y + size + 3), outline=col, width=6, r=8)
    # legend on the right
    lx = sx + 7 * size + 50
    cv.text((lx, sy - 8), 'tmp → 结果', 22, T['muted'], anchor='lb', bold=True)
    for g in range(10):
        Y = sy + 10 + g * (size * 7 - 20) / 10
        cv.rect((lx, Y, lx + 26, Y + 26), fill=GROUP[g], r=5)
        lo, hi = g * 4 + 1, g * 4 + 4
        hot = tmp is not None and lo <= tmp <= hi
        cv.text((lx + 38, Y + 13), f'{lo}~{hi} → {g + 1}', 21, T['yellow'] if hot else T['text'], anchor='lm', mono=True, bold=hot)
    hot = tmp is not None and tmp > 40
    cv.text((lx, sy + 7 * size + 10), '41~49 → 拒绝重来', 21, T['red'] if hot else T['muted'], anchor='lt', bold=hot)


def _formula(S):
    if 'tmp' not in S or S.get('_line', 0) < 8:
        return '连续调用两次 `rand7()`：一共 `7 × 7 = 49` 种可能，==每种概率相同=='
    a, b = _ab(S['tmp'])
    t = S['tmp']
    tail = '　→ ==接受==' if t <= 40 else '　→ ==拒绝=='
    return f'`tmp = ({a} − 1) × 7 + {b} = {t}`{tail}'


def _tmp(S, B, ret):
    a, b = _ab(S.tmp)
    return f'两次 `rand7()` 得到 `{a}`、`{b}`：`tmp = ({a}−1)×7+{b} = {S.tmp}`，1~49 ==等概率=='


CONFIG = dict(
    num=470, title='用Rand7()实现Rand10()', difficulty='Medium', category='数学',
    author='yiduobo', technique='拒绝采样 · 49 取 40',
    tags=['热题173'],
    code='''
# The rand7() API is already defined for you.
# def rand7():
# @return a random integer in the range 1 to 7

class Solution(object):
    def rand10(self):
        while True:
            tmp = (rand7() - 1) * 7 + rand7()
            if tmp <= 40:
                return (tmp - 1) // 4 + 1
''',
    setup='''
_seq = iter([7, 6, 3, 5, 6, 5, 5, 7])  # 演示用：固定 rand7() 的输出
def rand7():
    return next(_seq)
''',
    call='''sol = Solution()
[sol.rand10(), sol.rand10(), sol.rand10()]''',
    expect=[5, 10, 9],
    views=[
        dict(type='text', size=28, h=64, fn=_formula),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('tmp', 'tmp', 'yellow'), ('第1次', lambda S: _ab(S['tmp'])[0]), ('第2次', lambda S: _ab(S['tmp'])[1])],
    captions={
        'while True': lambda S, B, r: ('上一次落在 41~49 被拒绝 → ==再连续调用两次 rand7()==' if 'tmp' in S
                                       else '`rand10()`：一直尝试，直到落在前 40 个格子里'),
        'tmp = (rand7() - 1) * 7 + rand7()': _tmp,
        'if tmp <= 40': lambda S, B, r: ('`40 ≤ 40`：边界也要接受，`1~40` 正好 40 种' if S.tmp == 40 else
                                         f'`{S.tmp} ≤ 40`：落在前 40 种可能里 → 接受' if S.tmp <= 40
                                         else f'`{S.tmp} > 40`：恰好是剩下的 9 种可能 → ==拒绝，重来=='),
        'return (tmp - 1) // 4 + 1': '40 种可能分给 10 个结果，每个 4 种：`({tmp}−1)//4+1 = {ret}`',
    },
    cards=dict(
        one_liner='两次 rand7 造出 49 个等概率格子，只留前 40 个',
        complexity='期望调用 rand7 `2 × 49/40 ≈ 2.45` 次，空间 `O(1)`',
        problem=['已有 `rand7()`：等概率返回 `1~7`；只用它实现 `rand10()`：等概率返回 `1~10`',
                 '不能使用系统的随机函数',
                 '本视频固定了 rand7 的输出：`7,6 | 3,5 | 6,5 | 5,7` → 返回 `5, 10, 9`'],
        quote='经典的拒绝采样的题目，在这里连续调用两次Rand7()，那么一共有7 * 7 = 49种可能性。==我们可以取其中的40种可能，分配给rand10()的10种可能==。若恰好遇到剩下的9种可能，那么就再连续调用两次Rand7()。',
        quote_src='—— yiduobo 题解原文',
        idea=['`(a−1)×7 + b` 把两次结果 `(a, b)` 一一映射到 `1~49`，==每个数概率都是 1/49==',
              '只接受 `1~40`：每个结果对应 4 个数，概率相同',
              '`41~49` 直接丢掉重来，不会破坏均匀性'],
        summary=['每轮接受概率 `40/49`，期望 `49/40` 轮，每轮 2 次 rand7',
                 '易错：`rand7() + rand7()` 不是均匀分布（和为 8 的概率最大），必须用 `(a−1)×7+b`',
                 '易错：`rand7() * rand7()` 也不均匀，且取不到 11 这种质数',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去了类型说明文档字符串'],
    ),
)

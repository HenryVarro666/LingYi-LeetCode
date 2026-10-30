def _t1(S):
    x, y, z = S['x'], S['y'], S['z']
    return f'`x = {x}` 个 AA，`y = {y}` 个 BB，`z = {z}` 个 AB'


def _t2(S):
    x, y, z = S['x'], S['y'], S['z']
    m = min(x, y)
    extra = 1 if x != y else 0
    return (f'AA、BB 交替：`min(x,y)×2 + [x≠y] = {m}×2 + {extra}` = =={m * 2 + extra}== 个\n'
            f'AB 全部能塞进去：`+ z = {z}` → =={m * 2 + extra + z}== 个字符串，每个长 2')


def _t3(S):
    x, y, z = S['x'], S['y'], S['z']
    return f'答案 `({min(x, y) * 2} + {int(x != y)} + {z}) × 2 = {(min(x, y) * 2 + (x != y) + z) * 2}`'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y, z = S['x'], S['y'], S['z']
    cv.text((x0 + 18, y0 + 4), '拼接方案（蓝 = BB，粉 = AA，绿 = AB）', 24, T['muted'], bold=True)
    # 构造一个合法方案：BB AA BB AA ... ，AB 紧跟第一个 BB 之后
    seq = []
    m = min(x, y)
    if y > x:
        seq = ['BB'] + ['AA', 'BB'] * m
        seq = seq[:1] + ['AB'] * z + seq[1:]
    elif x > y:
        seq = ['AA', 'BB'] * m + ['AA']
        seq = ['AB'] * z + seq if m == 0 else seq[:2] + ['AB'] * z + seq[2:]
    else:
        seq = ['AA', 'BB'] * m
        seq = seq[:2] + ['AB'] * z + seq[2:]
    n = len(seq)
    cell = min(110, (x1 - x0 - 40) / max(n, 1))
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    top = y0 + 80
    col = {'AA': T['pink'], 'BB': T['blue'], 'AB': T['green']}
    for i, s in enumerate(seq):
        X = sx + i * cell
        cv.rect((X + 3, top, X + cell - 3, top + 90), fill=col[s], r=8, alpha=200)
        cv.text((X + cell / 2, top + 45), s, 34, T['bg'], anchor='mm', bold=True)
    cv.text(((x0 + x1) / 2, top + 130), ''.join(seq), 30, T['text'], anchor='mm', mono=True, bold=True)
    cv.text(((x0 + x1) / 2, top + 180), f'共 {n} 个字符串，长度 {2 * n}，没有 AAA / BBB', 26, T['muted'], anchor='mm')


CONFIG = dict(
    num=2745, title='构造最长的新字符串', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='AB 不影响 · AA/BB 交替',
    tags=['贪心与思维', '难度分 1607'],
    code='''
class Solution:
    def longestString(self, x: int, y: int, z: int) -> int:
        return (min(x, y) * 2 + (x != y) + z) * 2
''',
    call='Solution().longestString(2, 5, 1)',
    expect=12,
    views=[
        dict(type='text', fn=_t1, size=30, h=60),
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=lambda S: 'AA 后面只能接 BB；BB 后面能接 AA 或 AB；AB 后面能接 AA 或 AB', size=26, h=60),
    ],
    watch=['x', 'y', 'z', ('ans', '(min(x, y) * 2 + (x != y) + z) * 2', 'green')],
    captions={
        'return': '`min(x, y) × 2 + (x ≠ y) + z` = `{min(x, y)} × 2 + {int(x != y)} + {z}` = =={min(x, y) * 2 + (x != y) + z}== 个串，×2 = =={ret}== 个字符',
    },
    cards=dict(
        one_liner='AB 不影响 AA/BB 交替，一行公式搞定',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给 `x` 个 `"AA"`、`y` 个 `"BB"`、`z` 个 `"AB"`，挑一些拼成新字符串',
                 '新字符串不能含子串 `"AAA"` 或 `"BBB"`，求最大长度',
                 '示例：`x=2, y=5, z=1` → `12`'],
        quote='如果有 AB，它可以与自身连接，且只能插在 BB 和 AA 之间，即 BB + (ABABAB...) + AA。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先不看 AB：AA 和 BB 只能交替连接，个数最多 `min(x,y)×2 + [x≠y]`',
              'AB 可以和自己连成 `ABAB…`，插在 BB 与 AA 之间，或接在末尾 BB 后、放在开头 AA 前',
              '所以 AB 不改变上限，直接 `+ z`，每个串长 2，最后 `×2`'],
        result='`(2×2 + 1 + 1) × 2 = 12`，和示例一致',
        after=[dict(heading='另一种写法：记忆化搜索', lines=[
            '`dfs(x,y,z,k)`：`x,y,z` 是剩余个数，`k` = 上一个串是 AA / BB / AB',
            'AA 后只能接 BB；BB 后可接 AA 或 AB；AB 后可接 AA 或 AB',
            '类似状态机 DP，取 `max(dfs(…,0), dfs(…,1))`，结果和公式一致'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：`x ≠ y` 时可以多放一个（多的那一种放在两端）；`x = y` 时不能多',
                 '另一种写法：记忆化搜索 `dfs(x,y,z,k)`，`k` 表示上一个串是 AA/BB/AB 的状态机 DP',
                 '思维题套路：从特殊（没有 AB）到一般（加入 AB）'],
    ),
)

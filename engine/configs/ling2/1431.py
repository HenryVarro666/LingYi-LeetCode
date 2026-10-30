CANDIES, EXTRA = [2, 3, 5, 1, 3], 3


def _draw(cv, S, B, box, T):
    """柱高 = candies[i]；虚线 mx = 最大值，虚线 k = mx − extraCandies：柱子够到 k 线就是 true"""
    x0, y0, x1, y1 = box
    c = CANDIES
    mx = max(c)
    k = S.get('k')
    ans = [v >= k for v in c] if (k is not None and S.get('_line') == 4) else None
    cv.text((x0 + 18, y0 + 4), 'candies（柱高 = 糖果数）', 24, T['muted'], bold=True)
    n = len(c)
    slot = (x1 - x0 - 200) / n
    base = y1 - 120
    top = y0 + 70
    unit = (base - top) / (mx + 1)
    sx = x0 + 150
    # 参考线
    ym = base - mx * unit
    cv.dashed((sx - 20, ym), (x1 - 30, ym), T['orange'], 3)
    cv.text((sx - 28, ym), f'mx = {mx}', 22, T['orange'], anchor='rm', bold=True)
    if k is not None:
        yk = base - k * unit
        cv.dashed((sx - 20, yk), (x1 - 30, yk), T['green'], 3)
        cv.text((sx - 28, yk), f'k = {k}', 22, T['green'], anchor='rm', bold=True)
        cv.text((x1 - 30, (ym + yk) / 2), f'差 {EXTRA}', 20, T['muted'], anchor='rm')
    for i, v in enumerate(c):
        X = sx + i * slot + slot * 0.2
        W = slot * 0.6
        ok = k is not None and v >= k
        fill = (T['green'] if ok else (90, 96, 106)) if k is not None else T['blue']
        cv.rect((X, base - v * unit, X + W, base), fill=fill, r=6)
        cv.text((X + W / 2, base - v * unit - 6), v, 26, T['text'], anchor='mb', bold=True)
        cv.text((X + W / 2, base + 8), f'孩子 {i}', 20, T['dim'], anchor='mt')
        if ans is not None:
            cv.text((X + W / 2, base + 40), 'true' if ans[i] else 'false', 24,
                    T['green'] if ans[i] else T['red'], anchor='mt', bold=True)
    cv.line([(sx - 20, base), (x1 - 30, base)], T['border'], 2)


CONFIG = dict(
    num=1431, title='拥有最多糖果的孩子', difficulty='Easy', category='普通数组',
    author='灵茶山艾府', technique='先算阈值 k = mx − extraCandies',
    tags=['字节30天'],
    code='''
class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        k = max(candies) - extraCandies
        return [c >= k for c in candies]
''',
    call=f'Solution().kidsWithCandies({CANDIES}, {EXTRA})',
    expect=[True, True, True, False, True],
    views=[
        dict(type='custom', h=520, draw=_draw),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"`k = max(candies) - extraCandies = {max(CANDIES)} - {EXTRA} = {S['k']}`" if 'k' in S
                           else '先求最大值 `mx`')),
    ],
    watch=[('extraCandies', 'extraCandies'), ('k', 'k', 'green')],
    captions={
        'k = max(candies)': '`mx = max(candies) = {max(candies)}`，阈值 `k = mx - extraCandies` = =={k}==',
        'return [c >= k': lambda S, B, ret: (f'逐个判断 `c >= k`：柱子够到 ==k 线== 的就是 true → `{ret}`'),
    },
    cards=dict(
        one_liner='把 candies[i] + extra ≥ mx 移项成 candies[i] ≥ mx − extra',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['`candies[i]` 是第 `i` 个孩子的糖果数，另有 `extraCandies` 个额外糖果',
                 '把额外糖果==全部==给第 `i` 个孩子后，他是不是拥有最多糖果的（可以并列）？',
                 '示例：`candies = [2,3,5,1,3], extraCandies = 3` → `[true,true,true,false,true]`'],
        quote='代码实现时，为简化判断，可以计算出 ==k = mx − extraCandies==，这样只要 candies[i] ≥ k 那么 ans[i] 就是 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['额外糖果全给第 `i` 个孩子：别人不变，最多的还是 `mx`（或者他自己）',
              '条件 `candies[i] + extraCandies >= mx`',
              '移项：`candies[i] >= mx - extraCandies = k`，循环里少做一次加法'],
        result='柱子够到 `k = 2` 线的孩子都是 true：`[true,true,true,false,true]` ✓',
        after=[dict(heading='为什么只和原来的 mx 比？', lines=[
            '把糖果给第 `i` 个孩子，只有他的糖果数变了',
            '其他孩子的最大值 ≤ `mx`；他自己变大了也不影响「是否最多」',
            '所以只需判断 `candies[i] + extraCandies >= mx`，允许并列所以是 `>=`'])],
        summary=['时间 `O(n)`：一次求最大值 + 一次遍历',
                 '注意是 `>=`：并列最多也算 true',
                 '先算出阈值 `k`，列表推导式里只剩一次比较',
                 '同类：先预处理一个全局量（最大值/总和），再逐个判断'],
    ),
)

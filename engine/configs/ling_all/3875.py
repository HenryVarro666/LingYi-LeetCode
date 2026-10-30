
NUMS = [2, 7, 4, 3]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a = NUMS
    odd = [v for v in a if v % 2]
    x = odd[0] if odd else None
    cv.text((x0 + 20, y0 + 8), 'nums1 = %s' % a, 28, T['text'], bold=True)
    if x is None or len(odd) == len(a) or not any(v % 2 == 0 for v in a):
        cv.text((x0 + 20, y0 + 60), '同奇偶：每个位置都选 nums2[i] = nums1[i]', 26, T['green'])
        return
    cv.text((x0 + 20, y0 + 56), f'奇偶都有：选奇数 x = {x}，偶数 − x 变成奇数，奇数保持不变', 26, T['muted'])
    cell = min(110, (x1 - x0 - 40) / len(a))
    sx = x0 + 20
    for i, v in enumerate(a):
        X = sx + i * cell
        ev = v % 2 == 0
        cv.rect((X + 4, y0 + 130, X + cell - 4, y0 + 210), fill=T['orange'] if ev else T['blue'], r=8, alpha=200)
        cv.text((X + cell / 2, y0 + 170), v, 34, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 222), '偶' if ev else '奇', 22, T['muted'], anchor='mt')
        nv = v - x if ev else v
        cv.text((X + cell / 2, y0 + 280), '↓', 30, T['dim'], anchor='mm')
        cv.rect((X + 4, y0 + 310, X + cell - 4, y0 + 390), fill=T['green'], r=8, alpha=220)
        cv.text((X + cell / 2, y0 + 350), nv, 34, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 402), '奇', 22, T['green'], anchor='mt', bold=True)
        cv.text((X + cell / 2, y0 + 438), f'{v} − {x}' if ev else '不变', 20, T['muted'], anchor='mt')
    cv.text((x0 + 20, y0 + 480), 'nums2 全是奇数 → true', 28, T['green'], bold=True)


CONFIG = dict(
    num=3875, title='构造奇偶一致的数组 I', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='恒为 true · 偶减奇得奇', tags=['灵神题单', '难度分 1200'],
    code='''
class Solution:
    def uniformArray(self, _) -> bool:
        return True
''',
    call='Solution().uniformArray([2, 7, 4, 3])',
    expect=True,
    views=[dict(type='custom', draw=_draw, h=540)],
    watch=[],
    captions={
        'return True': '全奇或全偶：直接 `nums2[i] = nums1[i]`；奇偶混合：偶数减一个奇数变奇数，其余奇数不动 → 两种情况都能做到，恒返回 ==True==',
    },
    cards=dict(
        one_liner='偶数减奇数得奇数，所以答案恒为 true',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给 `nums1`（互不相同），构造 `nums2`，要求元素全奇或全偶',
                 '每个位置可取 `nums1[i]`，或 `nums1[i] − nums1[j]`（`j != i`）',
                 '示例：`[2,3]` → `true`；`[4,6]` → `true`'],
        quote='偶数减去奇数等于奇数，那么随便选一个奇数 x，把每个偶数都减去 x（第二种操作），即可让所有偶数都变成奇数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['全奇或全偶：只用第一种操作原样复制',
              '奇偶都有：随便选一个奇数 `x`，==每个偶数减去 x 变奇数==',
              '原来的奇数不动，于是 `nums2` 全是奇数，所以一定可行'],
        after=[dict(heading='看一个混合例子', lines=['`[2,7,4,3]`：奇数有 `7`、`3`，偶数有 `2`、`4`',
                '取 `x = 7`：`2 − 7 = −5`，`4 − 7 = −3`，都是奇数',
                '`7`、`3` 原样保留 → `nums2 = [-5,7,-3,3]`，全奇'])],
        summary=['时间 `O(1)`，空间 `O(1)`，函数体只有一行 `return True`',
                 '易错点：不用真的构造数组，证明存在即可',
                 '「互不相同」保证 `j != i` 时总能挑到另一个奇数',
                 '相似题：2396 严格回文的数字、877 石子游戏（同样是恒定答案）'],
    ),
)

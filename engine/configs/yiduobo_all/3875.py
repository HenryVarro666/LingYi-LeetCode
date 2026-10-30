
NUMS = [6, 5, 8, 9]


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
    author='yiduobo', technique='分类讨论 · 全同奇偶或奇偶混合', tags=['灵神题单', '贪心与思维', '难度分 1200'],
    code='''
class Solution(object):
    def uniformArray(self, nums1):
        
        return True
''',
    call='Solution().uniformArray([6, 5, 8, 9])',
    expect=True,
    views=[dict(type='custom', draw=_draw, h=540)],
    watch=[],
    captions={
        'return True': '先看全奇/全偶：原样复制就行；再看奇偶混合：保持奇数不变，每个偶数减某个奇数 → 全变奇数。无论哪种，答案必为 ==True==',
    },
    cards=dict(
        one_liner='分两种情形都构造得出来，答案必然是 true',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['长度为 n 的 `nums1` 元素互不相同，构造 `nums2` 使其元素全奇或全偶',
                 '每个下标选 `nums1[i]`，或 `nums1[i] − nums1[j]`（`j != i`）',
                 '本视频：`[6,5,8,9]` → `true`'],
        quote='若其中既有奇数也有偶数，那么在这里就可以保持所有的奇数不变，而对于所有偶数，都让这个偶数与某个奇数做减法。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看 `nums1` 本身：全奇或全偶，复制一遍就是答案',
              '既有奇又有偶：奇数不动，偶数减去某个奇数得奇数',
              '所以 `nums2` 可以全为奇数，答案无条件为 ==true=='],
        after=[dict(heading='延伸：3876 题', lines=['多了限制：`nums1[i] − nums1[j] >= 1`，数据也更大',
                '偶数只能减最小奇数 `mi_o`，要求最小偶数 `mi_e > mi_o`',
                '全奇或全偶时直接 true；否则返回 `mi_e > mi_o`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：这是 I 题，没有「差必须 ≥ 1」的限制，所以才恒为 true',
                 '原文还给了 3876（II）：要求 `nums1[i] − nums1[j] >= 1`，需比较最小偶数与最小奇数',
                 '对比灵神：灵神只讲 I 题；yiduobo 把 I、II 放在一起对照'],
    ),
)

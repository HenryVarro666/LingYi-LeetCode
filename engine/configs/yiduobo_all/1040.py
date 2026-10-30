def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st = S['stones']
    lo, hi = min(st), max(st)
    N = hi - lo + 1
    n = len(st)
    cell = min(90, (x1 - x0 - 40) / N)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * N) / 2
    ys, ch = y0 + 100, 90
    cv.text((x0 + 18, y0 + 4), '数轴（蓝 = 石子，空格 = 空位；粉框 = 起点在 stones[l]、长为 n 的区间）', 22, T['muted'], bold=True)
    pos = set(st)
    for p in range(lo, hi + 1):
        X = sx + (p - lo) * cell
        if p in pos:
            cv.rect((X + 2, ys, X + cell - 2, ys + ch), fill=T['blue'], r=8)
            cv.text((X + cell / 2, ys + ch / 2), p, 28, T['bg'], anchor='mm', bold=True)
        else:
            cv.rect((X + 2, ys, X + cell - 2, ys + ch), outline=T['border'], r=8)
            cv.text((X + cell / 2, ys + ch + 8), p, 18, T['dim'], anchor='mt', mono=True)
    if 'l' in S and 'r' in S and 'mi' in S and S['l'] < n:
        a = st[S['l']]
        b = a + n - 1
        b2 = min(b, hi)
        cv.rect((sx + (a - lo) * cell - 3, ys - 8, sx + (b2 - lo + 1) * cell + 3, ys + ch + 8), outline=T['pink'], width=5, r=10)
        cv.text((sx + (a - lo) * cell, ys - 14), f'区间 [{a}, {b}]（长 {n}）', 22, T['pink'], anchor='lb', bold=True)
        cnt = S['r'] - S['l'] + 1
        cv.text((x0 + 20, ys + ch + 70), f'区间内石子 {cnt} 个 → 其余 {n - cnt} 个要搬进来', 26, T['text'], bold=True)


def _txt(S, B):
    if 'mi' in S and 'l' in S:
        return f"当前最小次数 `mi = {S['mi']}`，最大次数 `ma = {S['ma']}`"
    if 'ma' in S:
        return f"最大次数 `ma = {S['ma']}`：总空位数 − 首次移动浪费的空位"
    return '先算最大，再分特殊情况算最小'


CONFIG = dict(
    num=1040, title='移动石子直到连续 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='最大看空位 · 最小滑窗找最密区间',
    tags=['灵神题单', '难度分 2456'],
    code='''
class Solution(object):
    def numMovesStonesII(self, stones):

        stones = sorted(stones)
        n = len(stones)

        ma = stones[-1] - stones[0] + 1 - n - min(stones[1] - stones[0] + 1 - 2, stones[-1] - stones[-2] + 1 - 2)

        if stones[-1] - stones[0] + 1 == n:
            mi = 0
        elif stones[-2] - stones[0] + 1 == (n - 1) and stones[-1] - stones[-2] > 2:
            mi = 2
        elif stones[-1] - stones[1] + 1 == (n - 1) and stones[1] - stones[0] > 2:
            mi = 2
        else:
            mi = ma
            l = r = 0
            while l < n:
                while r + 1 < n and stones[r + 1] - stones[l] + 1 <= n:
                    r += 1
                mi = min(mi, n - (r - l + 1))
                l += 1
        
        return [mi, ma]
''',
    call='Solution().numMovesStonesII([7,4,9,1,2])',
    expect=[2, 4],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='stones', label='stones（排序后）', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), cell=84, h=190),
        dict(type='text', h=70, size=28, fn=_txt),
    ],
    watch=[('n', 'n', 'cyan'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mi', 'mi', 'green'), ('ma', 'ma', 'orange')],
    captions={
        'stones = sorted': '先排序，石子从左到右排好',
        'ma = ': '最大次数：总空位 `{stones[-1] - stones[0] + 1 - n}` 减去首次移动浪费的空位（取小的一侧）→ `ma = {ma}`',
        'if stones[-1] - stones[0] + 1 == n': '总长度恰好等于 `n` 吗？{"是，已经连续，0 步" if stones[-1] - stones[0] + 1 == n else "不是，继续判断特殊情况"}',
        'elif stones[-2] - stones[0]': '特殊情况 2：左边 `n-1` 颗已连续，最右孤立且隔 `>1` 个空位 → {"成立，需要 2 步" if (stones[-2] - stones[0] + 1 == (n - 1) and stones[-1] - stones[-2] > 2) else "不成立"}',
        'elif stones[-1] - stones[1]': '特殊情况 2 的镜像：右边 `n-1` 颗连续，最左孤立 → {"成立，需要 2 步" if (stones[-1] - stones[1] + 1 == (n - 1) and stones[1] - stones[0] > 2) else "不成立"}',
        'mi = ma': '一般情况：先让 `mi` 取大值，再用滑动窗口找最小',
        'l = r = 0': '窗口 `[l, r]`：起点 `stones[l]`，长度不超过 `n` 的区间里的石子',
        'while l < n': '{"枚举区间起点 `l = " + str(l) + "`" if l < n else "起点枚举完毕"}',
        'while r + 1 < n and': '{"`stones[r+1] - stones[l] + 1 = " + str(stones[r + 1] - stones[l] + 1) + "` 与 `n = " + str(n) + "`：" if r + 1 < n else "`r` 已是最后一颗："}{"还装得下，r 右移" if (r + 1 < n and stones[r + 1] - stones[l] + 1 <= n) else "装不下了，r 停下"}',
        'r += 1': '`r` 右移到 {r}',
        'mi = min': '区间内有 `{r - l + 1}` 颗石子，其余 `{n - (r - l + 1)}` 颗各搬一步：`mi = min({B.mi}, {n - (r - l + 1)}) = {mi}`',
        'l += 1': '起点右移，`l` → {l}',
        'return [mi, ma]': '最少 `{mi}` 步，最多 `{ma}` 步',
    },
    cards=dict(
        one_liner='最大：算能浪费多少空位；最小：找最密的长为 n 的区间',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数轴上 `n` 颗石子，每次把端点石子移到空位，移完不再是端点',
                 '直到石子连续，返回 `[最小次数, 最大次数]`',
                 '示例：`[7,4,9]` → `[1,2]`；本视频：`[7,4,9,1,2]` → `[2,4]`'],
        quote='若stones是形如样例2这种，只有一个端点不连续，其这个端点与最近点之间的空格数大于1的，那么答案为2',
        quote_src='—— yiduobo 题解原文',
        idea=['最大：首次移动端点会浪费一段空位，浪费少的那侧留下最多的空位，之后每轮滚动一格',
              '最小：终点是长 `n` 的连续区间，找涵盖最多石子的区间，其余各搬一次',
              '先排除两种特殊情况：已连续 → 0；只有一个端点孤立 → 2'],
        summary=['时间 `O(n log n)`，排序是瓶颈；空间 `O(1)`',
                 '特殊情况要判两边：最右孤立、最左孤立都会让答案变 2',
                 '窗口条件 `stones[r+1] - stones[l] + 1 <= n`：区间长度不超过 n',
                 '对比灵神：灵神用 `e1, e2` 判特殊情况，yiduobo 直接比较区间长度'],
    ),
)

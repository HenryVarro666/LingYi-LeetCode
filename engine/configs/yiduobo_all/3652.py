P, ST, K = [2, 6, 3, 1, 7, 4], [1, -1, 1, 0, -1, 1], 4


def _win(S):
    """返回 (lo, mid, hi)：[lo, mid-1] 已改成 0，[mid, hi] 已改成 1；按当前行精确计算"""
    if 'index' not in S:
        return None
    ln, i, k = S['_line'], S['index'], S['k']
    h = k // 2
    if ln in (7, 8, 9, 10, 12):
        hi = i - 1 if ln == 7 else i
        return 0, h, hi
    if ln in (13, 14, 15, 16, 17, 18):
        lo, mid, hi = i - k, i - k + h, i - 1
        if ln >= 14:
            lo += 1
        if ln >= 15:
            mid += 1
        if ln >= 16:
            hi = i
        return lo, mid, hi
    return None


def _color(S, i, v):
    w = _win(S)
    if not w:
        return None
    lo, mid, hi = w
    if lo <= i < mid and i <= hi:
        return 'cyan'
    if mid <= i <= hi:
        return 'orange'
    return None


def _now(S):
    if 'now' not in S:
        return '`now`：当前窗口位置下的利润；`res`：见过的最大利润'
    w = _win(S)
    cur = list(S['strategy'])
    if w:
        lo, mid, hi = w
        for j in range(lo, hi + 1):
            cur[j] = 0 if j < mid else 1
    return f"当前策略 `{cur}`　→　`now = {S['now']}`　`res = {S.get('res', '-')}`"


CONFIG = dict(
    num=3652, title='按策略买卖股票的最佳时机', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='长为 k 的窗口直接维护利润',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1557'],
    code='''
class Solution(object):
    def maxProfit(self, prices, strategy, k):

        now = sum([p * s for p, s in zip(prices, strategy)])
        res = now

        for index in range(k):
            now -= prices[index] * strategy[index]
            if index >= k // 2:
                now += prices[index]

        res = max(res, now)
        for index in range(k, len(prices)):
            now += prices[index - k] * strategy[index - k]
            now -= prices[index - k + k // 2]
            now -= prices[index] * strategy[index]
            now += prices[index]
            res = max(res, now)

        return res
''',
    call=f'Solution().maxProfit({P}, {ST}, {K})',
    expect=14,
    views=[
        dict(type='array', var='prices', label='prices（青 = 改成 0，橙 = 改成 1）', h=190,
             pointers={'index': 'blue'}, color=_color),
        dict(type='array', var='strategy', label='strategy（原策略）', h=190, color=_color),
        dict(type='text', h=90, size=28, fn=_now),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = sum(': '先算不修改的利润（点积）`now = {now}`',
        'res = now': '不修改也是一种选择：`res = {res}`',
        'for index in range(k)': lambda S, B, r: (('前 k 天都处理完，窗口 `[0, k−1]` 就位' if B.get('index') == S.index else f'先把窗口放在开头 `[0, k−1]`：处理第 `{S.index}` 天')),
        8: '第 `{index}` 天先从利润里扣掉原来的 `{prices[index]}×{strategy[index]}` → `now = {now}`',
        'if index >= k // 2': lambda S, B, r: (f'`{S.index} ≥ k//2`：在窗口==后半==，要改成卖出' if S.index >= S.k // 2
                                               else f'`{S.index} < k//2`：在窗口==前半==，改成 0，什么都不加'),
        10: '卖出得 `{prices[index]}` → `now = {now}`',
        12: '窗口 `[0, {k - 1}]` 的利润 `{now}` → `res = {res}`',
        'for index in range(k, len': lambda S, B, r: ('窗口已滑到数组末尾，结束' if B.get('index') == S.index
                                                 else f'窗口右边界移到 `{S.index}`，整个窗口变成 `[{S.index - S.k + 1}, {S.index}]`'),
        'now += prices[index - k] * strategy[index - k]': '① 第 `{index - k}` 天离开窗口：0 变回原策略，加回 `{prices[index - k]}×{strategy[index - k]}` → `now = {now}`',
        'now -= prices[index - k + k // 2]': '② 第 `{index - k + k // 2}` 天从后半挪到前半：1 → 0，少卖 `{prices[index - k + k // 2]}` → `now = {now}`',
        16: '③ 第 `{index}` 天进入窗口：先扣掉原来的 `{prices[index]}×{strategy[index]}` → `now = {now}`',
        17: '再按卖出加上 `{prices[index]}` → `now = {now}`',
        18: '窗口 `[{index - k + 1}, {index}]` 利润 `{now}` → `res = {res}`',
        'return res': '最大利润 =={res}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='窗口每滑一步，只有 ==3 个位置== 的策略发生变化',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['利润 = `Σ strategy[i] × prices[i]`（-1 买、0 持有、1 卖）',
                 '最多一次：选连续 `k` 个，前 `k/2` 改成 0，后 `k/2` 改成 1，求最大利润',
                 '示例：`prices = [4,2,8], strategy = [-1,0,1], k = 2` → `10`',
                 '本视频：`prices = [2,6,3,1,7,4], strategy = [1,-1,1,0,-1,1], k = 4` → `14`'],
        quote='可以理解成使用一个长度为k的窗口从数组头部开始向后滑动。对于最开始的k个元素，可以先将strategy[:k]与prices[:k]的点积从利润中减去，然后再将prices[k//2 : k]累加到利润中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 直接表示「窗口在当前位置」时的==完整利润==',
              '右移一步：左端离开（恢复原策略）、中点从 1 变 0、右端进入（变成 1）',
              '每移一步用 `now` 更新 `res`，`res` 初值是不修改的利润'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：中间那天是 ==从 1 变 0==，所以减 `prices[index − k + k//2]`',
                 '`res` 一开始取不修改的点积，覆盖“不修改”的情况',
                 '原文的 Python 2 风格代码可直接在 Python 3 运行，未做改动',
                 '对比灵神：灵神维护“额外利润” extra，yiduobo 直接维护修改后的总利润'],
    ),
)

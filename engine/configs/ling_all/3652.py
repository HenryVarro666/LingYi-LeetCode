P, ST, K = [3, 7, 2, 6, 1, 5], [1, -1, 0, -1, 1, 0], 4


def _half(S, i):
    """0 = 前半窗口（改成 0），1 = 后半窗口（改成 1），None = 不在窗口里；按当前执行到的行精确计算"""
    if 'i' not in S or 'm' not in S:
        return None
    ln, cur, m, k = S['_line'], S['i'], S['m'], S['k']
    if ln == 25:
        return None
    if ln in (5, 6, 7, 8):  # 本轮还没入窗：显示上一轮出窗之后的状态
        cur -= 1
        out = cur >= k - 1
        lo, hi_b, lo_b = (cur - k + 2 if out else 0), cur, cur - m + 1 + out
    else:
        lo, lo_b, hi_b = max(0, cur - k + 1), cur - m + 1, cur
        if ln == 11:
            hi_b = cur - 1
        if ln in (22, 23):
            lo += 1 if cur - k + 1 >= 0 else 0
        if ln == 23:
            lo_b += 1
    if cur < m:
        return None
    if lo <= i <= cur - m:
        return 0
    if lo_b <= i <= hi_b:
        return 1
    return None


def _color(S, i, v):
    h = _half(S, i)
    return 'cyan' if h == 0 else 'orange' if h == 1 else None


def _txt(S):
    if 'extra' not in S:
        return '`total`：不修改时的利润；`extra`：修改窗口带来的==额外==利润'
    return (f"`total = {S['total']}`　`extra = {S['extra']}`　"
            f"`max_extra = {S['max_extra']}`")


CONFIG = dict(
    num=3652, title='按策略买卖股票的最佳时机', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='两个紧挨的定长滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1557'],
    code='''
class Solution:
    def maxProfit(self, prices: List[int], strategy: List[int], k: int) -> int:
        total = extra = max_extra = 0
        m = k // 2
        for i, (s, p) in enumerate(zip(strategy, prices)):
            total += s * p
            if i < m:
                continue

            # 1. 入
            extra -= strategy[i - m] * prices[i - m]  # 前 k/2 个元素的窗口
            extra += (1 - s) * p  # 后 k/2 个元素的窗口

            left = i - k + 1
            if left < 0:  # 尚未形成第一个窗口
                continue

            # 2. 更新
            max_extra = max(max_extra, extra)

            # 3. 出（计算方式和入相反）
            extra += strategy[left] * prices[left]  # 前 k/2 个元素的窗口
            extra -= (1 - strategy[left + m]) * prices[left + m]  # 后 k/2 个元素的窗口

        return total + max_extra
''',
    call=f'Solution().maxProfit({P}, {ST}, {K})',
    expect=10,
    views=[
        dict(type='array', var='prices', label='prices（青 = 前半窗口→改成 0，橙 = 后半窗口→改成 1）', h=190,
             pointers={'i': 'blue'}, color=_color),
        dict(type='array', var='strategy', label='strategy（原策略）', h=190, color=_color),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('left', 'left', 'pink'), ('total', 'total'), ('extra', 'extra', 'orange'),
           ('max_extra', 'max_extra', 'green')],
    skip=['total = extra = max_extra = 0'],
    captions={
        'm = k // 2': '两个小窗口，每个长 `m = k // 2 = {m}`',
        'for i, (s, p)': '第 `{i}` 天：`strategy = {s}`，`price = {p}`',
        'total += s * p': '不修改的利润累加 `{s} × {p}` → `total = {total}`',
        'if i < m': lambda S, B, r: (f'`i = {S.i} < m`：后半窗口还没有元素' if S.i < S.m
                                     else f'`i = {S.i} ≥ m`：第 `{S.i - S.m}` 天进==前半==，第 `{S.i}` 天进==后半=='),
        'continue': '先跳过',
        'extra -= strategy[i - m]': '第 `{i - m}` 天进入前半窗口：策略 `{strategy[i - m]}` → `0`，利润变化 `−({strategy[i - m]}×{prices[i - m]})` → `extra = {extra}`',
        'extra += (1 - s) * p': '第 `{i}` 天进入后半窗口：策略 `{s}` → `1`，利润多 `(1−{s})×{p}` → `extra = {extra}`',
        'left = i - k + 1': '整个窗口左端点 `left = {left}`',
        'if left < 0': lambda S, B, r: (f'`left = {S.left} < 0`：窗口还不满 k 个' if S.left < 0
                                        else f'窗口 `[{S.left}, {S.i}]` 满 `k = {S.k}` 个，可以更新答案'),
        'max_extra = max': '修改 `[{left}, {i}]` 能多赚 `{extra}` → `max_extra = {max_extra}`',
        'extra += strategy[left]': '第 `{left}` 天离开窗口：从 `0` 恢复原策略，`extra` 加回 `{strategy[left]}×{prices[left]}` → `{extra}`',
        'extra -= (1 - strategy[left + m])': '第 `{left + m}` 天离开后半窗口（下一轮它进前半）：撤销 `(1−{strategy[left + m]})×{prices[left + m]}` → `extra = {extra}`',
        'return total': '答案 = 不修改的利润 `{total}` + 最大额外利润 `{max_extra}` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='不算修改后的总利润，只算修改==多赚了多少==',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['利润 = `Σ strategy[i] × prices[i]`（-1 买、0 持有、1 卖）',
                 '最多一次：选连续 `k` 个，前 `k/2` 改成 0，后 `k/2` 改成 1，求最大利润',
                 '示例：`prices = [4,2,8], strategy = [-1,0,1], k = 2` → `10`',
                 '本视频：`prices = [3,7,2,6,1,5], strategy = [1,-1,0,-1,1,0], k = 4` → `10`'],
        quote='枚举修改的位置，视作两个长度均为 k/2 的==定长滑动窗口==紧挨着同时向右滑动。计算修改操作可以让总利润相比 total ==额外增加多少==。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['前半窗口：策略变成 0，利润增加 `(0 − strategy[i]) × prices[i]`',
              '后半窗口：策略变成 1，利润增加 `(1 − strategy[i]) × prices[i]`',
              '每轮：==入 → 更新 max_extra → 出==，答案 `total + max_extra`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`max_extra` 初始为 0，相当于“不修改”这一选项',
                 '易错：出窗口时要撤销第 `left+m` 天的后半贡献，下一轮它以 0 ==重新进入前半==',
                 '方法一：两个前缀和 `s`、`s_sell`，枚举修改区间右端点，空间 `O(n)`'],
    ),
)

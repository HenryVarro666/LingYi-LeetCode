def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'max_now' not in S:
        return
    upd = 'num' in S and 'max_now' in B and (B['max_now'], B['min_now']) != (S['max_now'], S['min_now'])
    cv.text((x0 + 18, y0 + 4), '滚动变量（左 = 更新前，右 = 更新后）' if upd else '滚动变量（当前值）', 24, T['muted'], bold=True)
    bw, bh = 230, 72
    lx, rx = x0 + 80, x1 - 80 - bw
    ty = y0 + 60
    by = ty + bh + 56

    def tile(x, y, name, val, c):
        cv.rect((x, y, x + bw, y + bh), fill=T['panel2'], outline=c, width=3, r=12)
        cv.text((x + 16, y + bh / 2), name, 22, T['muted'], anchor='lm', mono=True)
        cv.text((x + bw - 18, y + bh / 2), str(val), 36, c, anchor='rm', bold=True)

    left = B if upd else S
    tile(lx, ty, 'max_now', left['max_now'], T['green'])
    tile(lx, by, 'min_now', left['min_now'], T['pink'])
    if not upd:
        return
    tile(rx, ty, 'max_now', S['max_now'], T['green'])
    tile(rx, by, 'min_now', S['min_now'], T['pink'])
    num = S['num']
    a0, a1 = (lx + bw + 12, ty + bh / 2), (lx + bw + 12, by + bh / 2)
    b0, b1 = (rx - 12, ty + bh / 2), (rx - 12, by + bh / 2)
    if num >= 0:
        cv.arrow(a0, b0, T['blue'], 4, 16)
        cv.arrow(a1, b1, T['blue'], 4, 16)
        msg = f'num = {num} ≥ 0：最大接最大，最小接最小'
        c = T['blue']
    else:
        cv.arrow(a1, b0, T['orange'], 4, 16)
        cv.arrow(a0, b1, T['orange'], 4, 16)
        msg = f'num = {num} < 0：交叉！最小 × num → 最大，最大 × num → 最小'
        c = T['orange']
    cv.text(((x0 + x1) / 2, by + bh + 22), msg, 24, c, anchor='mt', bold=True)
    cv.text(((x0 + x1) / 2, by + bh + 58), '（两边都还要和 num 单独成段比一比）', 20, T['muted'], anchor='mt')


def _formula(S):
    if 'num' not in S:
        return '`f` = 以当前数结尾的最大乘积（`max_now`），`g` = 最小乘积（`min_now`）'
    n = S['num']
    if n >= 0:
        return f'`{n}` ≥ 0：`max_now` ← max(`max_now`×{n}, {n})，`min_now` ← min(`min_now`×{n}, {n})'
    return f'`{n}` < 0：`max_now` ← max(==min_now==×{n}, {n})，`min_now` ← min(==max_now==×{n}, {n})'


CONFIG = dict(
    num=152, title='乘积最大子数组', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='最大 / 最小乘积双状态 + 滚动变量',
    code='''
class Solution(object):
    def maxProduct(self, nums):
        if not nums:
            return 0

        res = max_res = min_now = max_now = nums[0]
        for num in nums[1:]:
            if num >= 0:
                max_now, min_now = max(max_now * num, num), min(min_now * num, num)
            else:
                max_now, min_now = max(min_now * num, num), min(max_now * num, num)

            res = max(res, max_now)

        return res
''',
    call='Solution().maxProduct([-2, 3, -4, -1, 0, 2])',
    expect=24,
    views=[
        dict(type='text', fn=_formula, h=66, size=26),
        dict(type='array', var='nums', label='nums（黄 = 当前 num，暗 = 已处理）', cell=100,
             color=lambda S, k, v: 'yellow' if 'num' in S and v == S['num'] else None,
             dim=lambda S, k, v: 'num' in S and k < S['nums'].index(S['num'])),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('num', 'num', 'yellow'), ('max_now', 'max_now', 'green'), ('min_now', 'min_now', 'pink'),
           ('res', 'res', 'green')],
    captions={
        'if not nums': '空数组返回 0（本例非空）',
        'res = max_res': '初始：以 `nums[0]` 结尾的最大、最小乘积都是 `{nums[0]}`，`res = {res}`',
        'for num in': lambda S, B, ret: ('扫描结束' if 'num' in B and B.num == S.num
                                        else f'下一个数 `num = {S.num}`'),
        'if num >= 0': lambda S, B, ret: (f'`{S.num} ≥ 0`：乘上它大小关系不变 → ==老样子==，最大接最大、最小接最小'
                                          if S.num >= 0 else
                                          f'`{S.num} < 0`：乘上它大小颠倒 → ==用最小去更新最大，用最大去更新最小=='),
        'max(max_now * num, num)': '`max_now = max({B.max_now}×{num}, {num})` = {max_now}，`min_now = min({B.min_now}×{num}, {num})` = {min_now}',
        'max(min_now * num, num)': '`max_now = max({B.min_now}×{num}, {num})` = =={max_now}==，`min_now = min({B.max_now}×{num}, {num})` = {min_now}',
        'res = max(res': '`res = max({B.res}, {max_now})` = =={res}==',
        'return res': '返回 =={ret}==（子数组 `[-2, 3, -4]`）',
    },
    cards=dict(
        one_liner='再维护一个最小乘积：遇到负数，最大最小互换角色',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，求==乘积最大==的非空连续子数组，返回该乘积',
                 '示例：`[2,3,-2,4]` → `6`；`[-2,0,-1]` → `0`',
                 '演示：`[-2,3,-4,-1,0,2]` → `24`（子数组 `[-2,3,-4]`）'],
        before=[dict(heading='第一想法：照搬最大子段和？', lines=[
            '设 `f[i]` 为以 `nums[i]` 结尾的最大乘积，像 53 题那样转移',
            '反例 `[-2, 3, -4]`：`f[0] = -2`，`f[1] = 3`',
            '但 `f[2]` 应该是 `24`，==已经无法从之前的状态中得到了==（负负得正）',
        ])],
        quote='于是我们可以再维护一个数组g，其中g[i]表示以nums[i]为结尾的最小乘积。那么==当nums[i]小于零时，就用g[i - 1]来更新f[i]，使用f[i - 1]来更新g[i]==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[i] ≥ 0`：老样子，`f` 由 `f[i-1]` 更新，`g` 由 `g[i-1]` 更新',
              '`nums[i] < 0`：==交叉更新==——最小 × 负数变最大，最大 × 负数变最小',
              '`f`、`g` 只与上一轮有关 → 不用数组，`max_now` / `min_now` 两个变量滚动'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：两个变量要==同时更新==（元组赋值），否则 `min_now` 用到新的 `max_now`',
                 '原文为 Python 2 风格：只删了 docstring；`max_res` 没用到，原样保留',
                 '对比灵神：不分正负，`max`/`min` 各取三项，效果相同'],
    ),
)

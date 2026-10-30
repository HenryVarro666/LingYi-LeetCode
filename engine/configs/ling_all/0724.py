NUMS = [1, 7, 3, 6, 5, 6]


def _side(S, i, v):
    # i 左边 = 左侧和（蓝），i 本身 = 候选中心（黄），i 右边 = 右侧和（粉）
    if 'i' not in S:
        return None
    c = S['i']
    if S.get('_line') == 8:  # x 已经累加进左侧
        return 'blue' if i <= c else 'pink'
    return 'blue' if i < c else ('yellow' if i == c else 'pink')


def _eq(S):
    if 'x' not in S:
        return '左侧和 = 右侧和 ⇔ `leftS = s − nums[i] − leftS` ⇔ `2·leftS == s − nums[i]`'
    a, b = S['left_s'] * 2, S['s'] - S['x']
    if S.get('_line') == 8:
        return f'`x = {S["x"]}` 已累加进 `left_s = {S["left_s"]}`，准备检查下一个下标'
    tag = '==相等，找到中心下标==' if a == b else '不相等'
    return f'`2 × left_s = 2 × {S["left_s"]} = {a}`　`s − x = {S["s"]} − {S["x"]} = {b}`　→ {tag}'


def _draw(cv, S, B, box, T):
    # 两根横条：左侧和 vs 右侧和（以 i 为中心）
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '以下标 i 为中心：左侧和 vs 右侧和', 24, T['muted'], bold=True)
    if 'i' not in S:
        cv.text((x0 + 18, y0 + 56), f'总和 s = {sum(NUMS)}', 26, T['dim'], bold=True)
        return
    i = S['i'] + (1 if S.get('_line') == 8 else 0)  # 累加之后，看的是下一个候选
    if i >= len(NUMS):
        return
    left, right = sum(NUMS[:i]), sum(NUMS[i + 1:])
    if i != S['i']:
        cv.text((x1 - 20, y0 + 6), f'（下一个候选 i = {i}）', 22, T['muted'], anchor='ra')
    full = max(1, sum(NUMS))
    L, R = x0 + 250, x1 - 120
    rows = [('左侧和 leftS', left, T['blue']), ('右侧和 s−x−leftS', right, T['pink'])]
    for k, (name, v, c) in enumerate(rows):
        Y = y0 + 60 + k * 74
        cv.text((x0 + 24, Y + 22), name, 24, c, anchor='lm', bold=True)
        cv.rect((L, Y, R, Y + 44), fill=T['panel2'], r=8)
        w = (R - L) * max(0, v) / full
        if w > 0:
            cv.rect((L, Y, L + w, Y + 44), fill=c, r=8)
        cv.text((L + w + 12, Y + 22), str(v), 28, T['text'], anchor='lm', bold=True)
    ok = left == right
    cv.text(((x0 + x1) / 2, y0 + 220), '左右相等 → 天平平衡' if ok else f'差 {abs(left - right)}，不平衡',
            26, T['green'] if ok else T['muted'], anchor='mt', bold=True)


CONFIG = dict(
    num=724, title='寻找数组的中心下标', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='前缀和 · 2·leftS = s − nums[i]',
    tags=['labuladong', '灵神题单·动态规划'],
    code='''
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        s = sum(nums)
        left_s = 0
        for i, x in enumerate(nums):
            if left_s * 2 == s - x:
                return i
            left_s += x
        return -1
''',
    call=f'Solution().pivotIndex({NUMS})',
    expect=3,
    views=[
        dict(type='text', fn=_eq, h=90, size=28),
        dict(type='array', var='nums', label='nums（蓝 = 左侧，黄 = 当前 i，粉 = 右侧）', pointers={'i': 'yellow'},
             color=_side, h=230),
        dict(type='custom', draw=_draw, h=280),
    ],
    watch=[('i', 'i', 'yellow'), 'x', ('s', 's', 'purple'), ('left_s', 'left_s', 'blue')],
    captions={
        's = sum': '先求总和 `s = {s}`：有了它，右侧和就是 ==`s − nums[i] − leftS`==，不用再算',
        'left_s = 0': '`left_s`：下标 i ==左侧==元素之和，一开始左边没有元素，为 0',
        'for i, x': lambda S, B, r: (f'看下标 `i = {S.i}`，`x = nums[{S.i}] = {S.x}`'
                                     if 'i' not in B or B.i != S.i else '遍历结束'),
        'if left_s * 2': lambda S, B, r: (
            f'`2 × {S.left_s} == {S.s} − {S.x}` 成立：左侧和 {S.left_s} = 右侧和 {S.s - S.x - S.left_s}'
            if S.left_s * 2 == S.s - S.x else
            f'`2 × {S.left_s} = {S.left_s * 2}` ≠ `{S.s} − {S.x} = {S.s - S.x}`：左 {S.left_s}、右 {S.s - S.x - S.left_s}，==不是中心=='),
        'return i': '返回 `{i}`：从左往右==第一个==满足的下标，就是最靠左的中心下标',
        'left_s += x': '==检查完再累加==：`left_s = {B.left_s} + {x} = {left_s}`，作为下一个下标的左侧和',
        'return -1': '没有下标满足等式，返回 `-1`',
    },
    cards=dict(
        one_liner='左侧和 = 右侧和 ⇔ 2·leftS = s − nums[i]：一次遍历搞定',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['中心下标：其==左侧元素和 = 右侧元素和==（最左端的左侧和视为 0，右端同理）',
                 '有多个返回最靠左的；不存在返回 `-1`',
                 '示例：`[1,7,3,6,5,6]` → `3`（1+7+3 = 5+6 = 11）'],
        quote='设中心下标为 i，其左侧元素和为 leftS，那么右侧元素和为 s − nums[i] − leftS。……所以有 ==2·leftS = s − nums[i]==',
        quote_src='—— 灵茶山艾府题解',
        idea=['先求总和 `s`，右侧和不必单独求：`s − nums[i] − leftS`',
              '左右相等整理成 `2·leftS == s − nums[i]`，只需维护一个 `leftS`',
              '从左到右，==每次累加前==检查等式，满足就返回 `i`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：==先判断再累加==，判断时 leftS 不含 nums[i] 本身',
                 '乘 2 代替除 2：`s − nums[i]` 是奇数时也不会出错',
                 '本题与 1991 题相同；思考题：把数组分成和相等的 3 段有几种方案？'],
    ),
)

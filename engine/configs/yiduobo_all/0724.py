NUMS = [2, 3, -1, 8, 4]


def _color(S, i, v):
    # 已累加进 now 的元素（绿），正在检查的元素（黄）
    if 'index' not in S:
        return None
    c = S['index']
    if i < c or (i == c and S.get('_line') == 12):
        return 'green'
    return 'yellow' if i == c else None


def _draw(cv, S, B, box, T):
    # yiduobo 的判断式：s − num  对比  now + now
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '判断式两边：s − num  vs  now + now', 24, T['muted'], bold=True)
    if 'num' not in S or S.get('_line') == 12:
        cv.text((x0 + 18, y0 + 56), '（每看一个元素，比较一次两边）', 24, T['dim'])
        return
    a, b = S['s'] - S['num'], S['now'] * 2
    full = max(1, S['s'] - min(NUMS), max(NUMS) * 2)
    L, R = x0 + 230, x1 - 110
    for k, (name, v, c) in enumerate([('s − num', a, T['purple']), ('now + now', b, T['green'])]):
        Y = y0 + 60 + k * 74
        cv.text((x0 + 24, Y + 22), name, 26, c, anchor='lm', bold=True, mono=True)
        cv.rect((L, Y, R, Y + 44), fill=T['panel2'], r=8)
        w = (R - L) * max(0, v) / full
        if w > 0:
            cv.rect((L, Y, L + w, Y + 44), fill=c, r=8)
        cv.text((L + w + 12, Y + 22), str(v), 28, T['text'], anchor='lm', bold=True)
    ok = a == b
    cv.text(((x0 + x1) / 2, y0 + 220), '两边相等 → 当前下标就是答案' if ok else '两边不等 → 把 num 累加进 now，看下一个',
            26, T['green'] if ok else T['muted'], anchor='mt', bold=True)


CONFIG = dict(
    num=724, title='寻找数组的中心下标', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='总和 + 一趟累加',
    tags=['labuladong', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def pivotIndex(self, nums):

        if not nums:
            return -1

        s = sum(nums)
        now = 0
        for index, num in enumerate(nums):
            if s - num == now + now:
                return index
            now += num

        return -1
''',
    call=f'Solution().pivotIndex({NUMS})',
    expect=3,
    views=[
        dict(type='text', h=90, size=28, fn=lambda S: (
            f"左边累加和 `now = {S['now']}`，右边 = `s − num − now = {S['s'] - S['num'] - S['now']}`"
            if 'num' in S and S.get('_line') != 12 else '中心下标：左边之和 = 右边之和')),
        dict(type='array', var='nums', label='nums（绿 = 已累加进 now，黄 = 正在检查）', pointers={'index': 'yellow'},
             color=_color, h=230),
        dict(type='custom', draw=_draw, h=280),
    ],
    watch=[('index', 'index', 'yellow'), 'num', ('s', 's', 'purple'), ('now', 'now', 'green')],
    captions={
        'if not nums': '先特判空数组（新版题面保证长度 ≥ 1）',
        's = sum': '先算出元素总和 `s = {s}`',
        'now = 0': '`now`：从头往后的==累加和==，也就是当前下标左边之和',
        'for index, num': lambda S, B, r: (f'看下标 `{S.index}`，元素 `num = {S.num}`'
                                           if 'index' not in B or B.index != S.index else '遍历结束'),
        'if s - num == now + now': lambda S, B, r: (
            f'`{S.s} − {S.num} = {S.s - S.num}`，`{S.now} + {S.now} = {S.now * 2}`：==相等==，左右两边都是 {S.now}'
            if S.s - S.num == S.now * 2 else
            f'`s − num = {S.s - S.num}` ≠ `now + now = {S.now * 2}`：左边 {S.now}，右边 {S.s - S.num - S.now}，不平衡'),
        'return index': '左 = 右 → 返回下标 `{index}`；从头扫描，所以是==最靠左==的那个',
        'now += num': lambda S, B, r: (f'不是答案 → 把 `{S.num}` 累加进 `now`：{B.now} + '
                                       f'{S.num if S.num >= 0 else f"({S.num})"} = =={S.now}=='),
        'return -1': '扫完都不满足，返回 `-1`',
    },
    cards=dict(
        one_liner='右边之和 = 总和 − 当前元素 − 左边之和，所以只要检查 s − num == now + now',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找数组的==中心下标==：它左边所有元素之和等于右边所有元素之和',
                 '边界外的和视为 0；有多个返回最左边的，没有返回 `-1`',
                 '示例：`[1,7,3,6,5,6]` → `3`；`[2,1,-1]` → `0`',
                 f'本视频：`{NUMS}` → `3`（2+3−1 = 4 = 右边的 4）'],
        quote='首先计算出数组中元素的总和，然后从头开始往后遍历同时进行累加，若==当前的累加和乘以2等于元素总和减去当前元素值==，那么当前下标即为答案',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` = 当前下标左边之和；右边之和 = `s − num − now`',
              '左 = 右 ⇔ `now = s − num − now` ⇔ `s − num == now + now`',
              '不满足就把当前元素累加进 `now`，继续往后扫'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '判断要放在 `now += num` 之前：此时 now 还==不含==当前元素',
                 '有负数也没关系：只比较和是否相等，不依赖单调性',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动即可在 Python 3 运行'],
    ),
)

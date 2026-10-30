NUMS = [1, 1, 4, 6, 3, 3, 2, 5, 8, 4]


def _classify(a):
    """每段 (i-1 → i) 的类别：flat / new（方向改变或第一次有方向）/ same"""
    out = [None]
    d = 0
    for i in range(1, len(a)):
        x = a[i] - a[i - 1]
        if x == 0:
            out.append('flat')
        elif d == 0 or (d > 0) != (x > 0):
            out.append('new')
            d = x
        else:
            out.append('same')
    return out


SEG = _classify(NUMS)
FIRST_NEW = SEG.index('new')


def _cur(S):
    line = S.get('_line')
    if line == 23:
        return len(NUMS), False
    idx = S.get('index')
    if idx is None:
        return 1, False
    return idx, True


def _picked(S):
    """已经确定被选中的点"""
    cur, live = _cur(S)
    line = S.get('_line')
    pts = {0}
    for i in range(1, min(cur + 1, len(NUMS))):
        if SEG[i] != 'new' or i == FIRST_NEW:
            continue
        if i < cur or (i == cur and line in (17, 18, 20, 21)):
            pts.add(i - 1)
    if line == 23:
        pts.add(max(i for i in range(len(NUMS)) if i == 0 or SEG[i] != 'flat'))
    return pts


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a = NUMS
    n = len(a)
    cur, live = _cur(S)
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), 'nums 折线（绿 = 换方向的一段，灰 = 同向，虚线 = 相等跳过；绿圈 = 选中的拐点）', 22, T['muted'], bold=True)
    L, R = x0 + 70, x1 - 50
    top, bot = y0 + 70, y1 - 70
    lo, hi = min(a), max(a)

    def P(i):
        return L + i * (R - L) / (n - 1), bot - (a[i] - lo) / max(1, hi - lo) * (bot - top)
    for i in range(1, n):
        p0, p1 = P(i - 1), P(i)
        if live and i == cur:
            cv.line([p0, p1], T['yellow'], 8)
            continue
        if i < cur:
            kind = SEG[i]
            if kind == 'flat':
                cv.dashed(p0, p1, T['red'], 4)
            elif kind == 'new':
                cv.line([p0, p1], T['green'], 6)
            else:
                cv.line([p0, p1], T['muted'], 5)
        else:
            cv.line([p0, p1], T['border'], 3)
    picked = _picked(S)
    for i in range(n):
        X, Y = P(i)
        if i in picked:
            cv.d.ellipse((X - 17, Y - 17, X + 17, Y + 17), outline=T['green'], width=4)
        c = T['text'] if (i <= cur) else T['dim']
        cv.d.ellipse((X - 8, Y - 8, X + 8, Y + 8), fill=c)
        cv.text((X, Y - 24), a[i], 24, c, anchor='mb', bold=True)
        cv.text((X, bot + 44), i, 18, T['dim'], anchor='mt', mono=True)
    if 0 in picked:
        X, Y = P(0)
        cv.text((X, Y + 22), '起点', 18, T['green'], anchor='mt', bold=True)


def _dir(v):
    return '上升' if v > 0 else ('下降' if v < 0 else '无方向')


def _text(S):
    if 'diff' not in S:
        return ''
    d = S['diff']
    nd = S.get('now_diff')
    s = f"上一段方向 `diff = {d}`（{_dir(d)}）"
    if nd is not None and S.get('_line') not in (6, 7):
        s += f"，这一段 `now_diff = {nd}`（{_dir(nd) if nd else '相等'}）"
    return s


def _cap_nd(S, B, ret):
    i = S.index
    return f'看第 `{i - 1}` → `{i}` 段：`now_diff = {S.nums[i]} − {S.nums[i - 1]} = {S.now_diff}`'


def _cap_e1(S, B, ret):
    if S.diff > 0 and S.now_diff < 0:
        return '上一段==上升==，这一段==下降== → 出现拐点'
    return '不是「升 → 降」'


def _cap_e2(S, B, ret):
    if S.diff < 0 and S.now_diff > 0:
        return '上一段==下降==，这一段==上升== → 出现拐点'
    w = '上升' if S.diff > 0 else '下降'
    best = '最大' if S.diff > 0 else '最小'
    return f'方向没变（都是{w}）：单调区间里只能选一个，选=={best}==的那个 → `res` 不变'


CONFIG = dict(
    num=376, title='摆动序列', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='贪心 · 统计拐点',
    tags=['字节30天'],
    code='''
class Solution(object):
    def wiggleMaxLength(self, nums):
        if len(nums) < 2:
            return len(nums)

        diff = 0
        res = 1

        for index in range(1, len(nums)):
            now_diff = nums[index] - nums[index - 1]
            if now_diff == 0:
                continue
            if diff == 0:
                diff = now_diff
                res += 1
            elif diff > 0 and now_diff < 0:
                res += 1
                diff = now_diff
            elif diff < 0 and now_diff > 0:
                res += 1
                diff = now_diff

        return res
''',
    call=f'Solution().wiggleMaxLength({NUMS})',
    expect=5,
    skip=['for index in range'],
    max_steps=70,
    views=[
        dict(type='text', fn=_text, h=56),
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='nums', label='nums', cell=80, pointers={'index': 'yellow'},
             color=lambda S, i, v: 'green' if i in _picked(S) else None),
    ],
    watch=[('index', 'index', 'yellow'), 'now_diff', ('diff', 'diff', 'cyan'), ('res', 'res', 'green')],
    captions={
        'if len(nums) < 2': '`len(nums) = {len(nums)}` ≥ 2，正常处理',
        'diff = 0': '`diff`：上一段==非零==的差值，记录折线当前的方向；0 表示还没有方向',
        'res = 1': '`res = 1`：最初的起点一定选',
        'now_diff = ': _cap_nd,
        'if now_diff == 0': lambda S, B, r: ('相邻两数相同：连续相同的数字==最多只能选一个==' if S.now_diff == 0
                                             else f'`now_diff = {S.now_diff} ≠ 0`，有方向'),
        'continue': '跳过它，相当于先对连续相同的数字去重',
        'if diff == 0': lambda S, B, r: ('`diff = 0`：这是第一段有方向的折线' if S.diff == 0 else f'已有方向 `diff = {S.diff}`'),
        14: '记下第一段的方向：`diff = {diff}`（{"上升" if diff > 0 else "下降"}）',
        15: '方向第一次确定：这段{"上升" if diff > 0 else "下降"}区间里会再选一个数 → `res = {res}`',
        'elif diff > 0 and now_diff < 0': _cap_e1,
        17: '`nums[{index - 1}] = {nums[index - 1]}` 是上升段的==最大值==，选它当拐点 → `res = {res}`',
        18: '方向改为下降：`diff = {diff}`',
        'elif diff < 0 and now_diff > 0': _cap_e2,
        20: '`nums[{index - 1}] = {nums[index - 1]}` 是下降段的==最小值==，选它当拐点 → `res = {res}`',
        21: '方向改为上升：`diff = {diff}`',
        'return res': '拐点个数 + 起点 = =={ret}==：选出 `[1, 6, 2, 8, 4]`',
    },
    cards=dict(
        one_liner='去掉连续重复后，答案 = 起点 + 折线拐点的个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['相邻元素的差==严格地在正负之间交替==的序列称为摆动序列',
                 '求 `nums` 中作为摆动序列的==最长子序列==的长度',
                 '示例：`[1,7,4,9,2,5]` → `6`；`[1,17,5,10,13,15,10,5,16,8]` → `7`',
                 '本视频：`[1,1,4,6,3,3,2,5,8,4]` → `5`'],
        quote='对于单调上升区间，应该选择==最大的那一个数==，而对于单调下降区间，则应该选择最小的那一个数，原因是之后的区间必须满足单调性相反。',
        quote_src='—— yiduobo 题解原文',
        idea=['连续相同的数字最多只能选一个，先跳过（相当于去重）',
              '剩下的数构成上下起伏的折线：一个单调区间除起点外只能再选一个数',
              '选区间的最大 / 最小值，有助于后面形成更多区间 → 恰好是==拐点==',
              '于是只需统计拐点数目，再加上最初的起点'],
        result='`res = 5`：起点 1 + 拐点 6、2、8 + 终点 4',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`diff` 只在方向改变时更新，记录的是==上一段非零==的方向',
                 '易错：相等的相邻元素必须跳过，否则会把 0 当成方向',
                 '长度小于 2 时直接返回长度',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)

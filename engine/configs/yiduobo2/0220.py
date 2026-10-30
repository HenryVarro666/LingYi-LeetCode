NUMS = [2, 9, 15, 3, 7, 5]
K, T_ = 2, 3
NB = 4  # buckets 0..3 cover 0..15


def _win(S):
    """index range of the numbers currently stored in pos_dict"""
    ln, i = S.get('_line'), S.get('index')
    if i is None or ln is None or ln < 8:
        return None
    if ln == 21:
        lo, hi = i - K + 1, i
    elif ln in (18, 20):
        lo, hi = max(0, i - K), i
    else:
        lo, hi = max(0, i - K), i - 1
    return (lo, hi) if lo <= hi else None


def _buckets(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = S.get('pos_dict')
    cv.text((x0 + 20, y0 + 10), '桶（宽 t + 1 = 4）：黄框 = 当前数的桶，蓝框 = 正在比较的相邻桶', 22, T['muted'])
    if d is None:
        return
    bd = B.get('pos_dict') or {}
    ln, pos = S.get('_line'), S.get('pos')
    gap = 24
    w = (x1 - x0 - 40 - gap * (NB - 1)) / NB
    top, bot = y0 + 50, y1 - 14
    for b in range(NB):
        X = x0 + 20 + b * (w + gap)
        outline, width = T['border'], 2
        if pos is not None and ln in range(9, 19):
            if b == pos:
                outline, width = T['yellow'], 5
            elif (ln == 13 and b == pos - 1) or (ln == 15 and b == pos + 1):
                outline, width = T['blue'], 5
        has = b in d
        fill = T['panel2']
        if has and (b not in bd or bd.get(b) != d[b]):
            fill = T['green']
        elif not has and b in bd:
            fill = T['red']
        cv.rect((X, top, X + w, bot), fill=fill, outline=outline, width=width, r=12)
        tc = T['bg'] if fill != T['panel2'] else T['text']
        mc = T['bg'] if fill != T['panel2'] else T['muted']
        cv.text((X + w / 2, top + 14), f'桶 {b}', 24, tc, anchor='mt', bold=True)
        cv.text((X + w / 2, top + 46), f'[{4 * b}, {4 * b + 3}]', 20, mc, anchor='mt', mono=True)
        if has:
            cv.text((X + w / 2, (top + 76 + bot) / 2), str(d[b]), 44, tc, anchor='mm', bold=True)
        elif b in bd:
            cv.text((X + w / 2, (top + 76 + bot) / 2), f'{bd[b]} 出窗', 26, tc, anchor='mm', bold=True)


def _text(S):
    ln = S.get('_line')
    if 'pos' not in S or ln is None:
        return '每个桶装宽度为 `t + 1` 的值域：==同一个桶里的两个数，差一定 ≤ t=='
    num, pos = S['num'], S['pos']
    if ln == 9:
        return f'`pos = {num} // (t + 1) = {num} // 4` = =={pos}=='
    return f'当前 `nums[{S["index"]}] = {num}` → 桶 {pos}；窗口内只保留下标 ≥ `index − k` 的数'


def _cap_for(S, B, ret):
    if S.get('index') == B.get('index'):
        return '扫描结束'
    return f"`index = {S['index']}`，`num = {S['num']}`"


def _gone(S, b):
    i = S.index
    for j in range(i - 1, -1, -1):
        if S.nums[j] // (S.t + 1) == b:
            return f'（`{S.nums[j]}` 已出窗：下标差 {i - j} > k）'
    return ''


def _cap_same(S, B, ret):
    d, p = S.pos_dict, S.pos
    if p in d:
        return f'桶 {p} 里已有 `{d[p]}` → ==同桶，差值必 ≤ t=='
    return f'桶 {p} 里没有数' + _gone(S, p)


def _cap_left(S, B, ret):
    d, p, n, t = S.pos_dict, S.pos, S.num, S.t
    if p - 1 not in d:
        return f'左邻桶 {p - 1} 为空' + _gone(S, p - 1)
    v = d[p - 1]
    ok = '≤' if n - v <= t else '>'
    return f'左邻桶 {p - 1} 有 `{v}`：`{n} − {v} = {n - v} {ok} t = {t}`' + (' → 找到' if n - v <= t else ' → 不行')


def _cap_right(S, B, ret):
    d, p, n, t = S.pos_dict, S.pos, S.num, S.t
    if p + 1 not in d:
        return f'右邻桶 {p + 1} 为空' + _gone(S, p + 1)
    v = d[p + 1]
    ok = '≤' if v - n <= t else '>'
    return f'右邻桶 {p + 1} 有 `{v}`：`{v} − {n} = {v - n} {ok} t = {t}`' + (' → 找到' if v - n <= t else ' → 不行')


def _cap_ge(S, B, ret):
    if S.index >= S.k:
        return f'`index = {S.index} ≥ k = {S.k}` → 窗口超长，最左边的数要移出桶'
    return f'`index = {S.index} < k = {S.k}` → 窗口还没满，不用移除'


def _cap_pop(S, B, ret):
    j = S.index - S.k
    v = S.nums[j]
    return f'移出 `nums[{j}] = {v}`（桶 {v // (S.t + 1)}）：它和后面的数下标差会超过 `k`'


CONFIG = dict(
    num=220, title='存在重复元素 III', difficulty='Hard', category='滑动窗口',
    author='yiduobo', technique='按 t+1 分桶 + 滑动窗口',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def containsNearbyAlmostDuplicate(self, nums, k, t):
        if k < 0 or t < 0:
            return False

        pos_dict = {}

        for index, num in enumerate(nums):
            pos = num // (t + 1)

            if pos in pos_dict:
                return True
            if pos - 1 in pos_dict and num - pos_dict[pos - 1] <= t:
                return True
            if pos + 1 in pos_dict and pos_dict[pos + 1] - num <= t:
                return True

            pos_dict[pos] = num

            if index >= k:
                pos_dict.pop(nums[index - k] // (t + 1))

        return False
''',
    call=f'Solution().containsNearbyAlmostDuplicate({NUMS}, {K}, {T_})',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='array', var='nums', label='nums（青框 = 桶里存着的数 = 滑动窗口）', pointers={'index': 'orange'},
             window=(lambda S: (_win(S) or (None, None))[0], lambda S: (_win(S) or (None, None))[1]),
             color=lambda S, i, v: 'orange' if i == S.get('index') and S.get('_line') in range(9, 18) else None,
             dim=lambda S, i, v: S.get('index') is not None and i > S['index'], cell=100, h=230),
        dict(type='custom', draw=_buckets, h=260),
    ],
    watch=[('index', 'index', 'orange'), ('num', 'num', 'orange'), ('pos', 'pos', 'yellow'), 'k', 't'],
    captions={
        'if k < 0 or t < 0': '`k = {k}`、`t = {t}` 都非负 → 不用特判',
        'pos_dict = {}': '`pos_dict`：桶编号 → 桶里的数（只存窗口内的数）',
        'for index, num': _cap_for,
        'pos = num // (t + 1)': '分桶：`{num} // {t + 1}` = 桶 =={pos}==；同桶两数差一定 ≤ `t`',
        'if pos in pos_dict': _cap_same,
        'if pos - 1 in pos_dict': _cap_left,
        'if pos + 1 in pos_dict': _cap_right,
        'pos_dict[pos] = num': '`{num}` 放进桶 {pos}（每个桶最多一个数，否则早就返回了）',
        'if index >= k': _cap_ge,
        'pos_dict.pop': _cap_pop,
        'return True': '下标差 ≤ `k`、值差 ≤ `t` 的两个数找到了 → =={ret}==',
        'return False': '没有符合条件的一对数 → =={ret}==',
    },
    cards=dict(
        one_liner='按 t+1 分桶：同桶必满足，再看相邻桶；窗口外的数移出桶',
        complexity='时间 `O(n)`，空间 `O(min(n, k))`',
        problem=['数组 `nums` 和整数 `k`、`t`：是否存在两个不同下标 `i`、`j`',
                 '满足 `|i − j| ≤ k` 且 `|nums[i] − nums[j]| ≤ t`（新版参数名 `indexDiff`、`valueDiff`）',
                 '示例：`[1,2,3,1], k = 3, t = 0` → `true`',
                 '本视频：`[2,9,15,3,7,5], k = 2, t = 3` → `true`'],
        before=[dict(heading='朴素做法：O(nt)', chapter='② 思路', lines=[
            '上一题（219）的加强版：差值不必为 0，只要在 `t` 之内',
            '用 dict 记每个数上一次出现的位置',
            '查 `num − t` 到 `num + t` 的每个数，下标差是否 ≤ `k` → `O(nt)`，效率低',
        ])],
        quote='受164题最大间隔的启发，在这里也可以使用分桶的做法……如果a整除(t + 1)等于b整除(t + 1)，那么a和b之间的差一定小于等于t。',
        quote_src='—— yiduobo 题解原文',
        idea_heading='分桶 + 滑动窗口',
        idea=['桶编号 `num // (t + 1)`：桶里已有数 → 差值 ≤ t，直接返回 `True`',
              '差值 ≤ t 也可能分在==相邻桶==（如 2 和 6 按 5 分桶），再比 `x − 1`、`x + 1` 号桶',
              '超出左边界 `index − k` 的数移出桶，就==不用再判断下标差=='],
        summary=['时间 `O(n)`，空间 `O(min(n, k))`：每个桶最多一个数',
                 '原文为 Python 2 写法，整除 `/` 已改为 `//`，并删去类型说明文档字符串',
                 'Python 的 `//` 向下取整，负数也能正确分桶（C++/Java 的 `/` 要特殊处理）',
                 '顺序：先查三个桶 → 再入桶 → 最后移出 `nums[index − k]`',
                 '相邻桶要再比一次真实差值：例子里 `15 − 9 = 6 > 3`'],
    ),
)

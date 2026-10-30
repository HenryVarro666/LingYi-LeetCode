INTERVALS = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16], [17, 19]]
NEW = [4, 8]
LO, HI = 0, 20


def _fates(upto):
    """前 upto 个区间的去向：'res' 原样进答案 / 'merged' 被并进 a"""
    a, fin, out = list(NEW), False, []
    for b in INTERVALS[:upto]:
        if fin or a[1] < b[0]:
            fin = True
            out.append('res')
        elif a[0] > b[1]:
            out.append('res')
        else:
            a = [min(a[0], b[0]), max(a[1], b[1])]
            out.append('merged')
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    L, R = x0 + 190, x1 - 50

    def X(v):
        return L + (v - LO) / (HI - LO) * (R - L)

    def bar(a, b, y, c, h=22):
        cv.rect((X(a), y, max(X(b), X(a) + 8), y + h), fill=c, r=h // 2)

    ivs = S.get('intervals') or INTERVALS
    idx = S.get('index')
    ended = S.get('_line') in (18, 19, 21) or (S.get('_line') == 5 and idx is not None and idx == B.get('index'))
    fates = _fates(len(ivs) if ended else (idx or 0))
    y = y0 + 6
    cv.text((x0 + 18, y), 'intervals（b；暗绿 = 原样进答案，暗橙 = 并进了 a）', 22, T['muted'], bold=True)
    y += 38
    for k, (a, b) in enumerate(ivs):
        cur = k == idx and 'interval' in S and not ended
        if cur:
            c = T['yellow']
        elif k < len(fates):
            c = (60, 120, 80) if fates[k] == 'res' else (150, 100, 60)
        else:
            c = T['blue']
        cv.text((x0 + 30, y + 13), f'[{a},{b}]', 21, T['yellow'] if cur else T['text'], anchor='lm', mono=True)
        bar(a, b, y, c, 26)
        y += 38
    y += 10
    a_now = S.get('newInterval') or NEW
    a_old = B.get('newInterval')
    fin = S.get('finish_flag')
    cv.text((x0 + 18, y), '待插入区间 a = newInterval' + ('（已插入）' if fin else ''), 22, T['orange'], bold=True)
    y += 36
    cv.text((x0 + 30, y + 13), f'[{a_now[0]},{a_now[1]}]', 20, T['orange'], anchor='lm', mono=True)
    if a_old and list(a_old) != list(a_now):
        cv.rect((X(a_old[0]), y - 3, max(X(a_old[1]), X(a_old[0]) + 8), y + 29), outline=T['text'], width=2, r=14)
    bar(a_now[0], a_now[1], y, T['orange'] if not fin else (150, 100, 60), 26)
    y += 50
    cv.text((x0 + 18, y), 'res（答案）', 22, T['green'], bold=True)
    y += 36
    bres = B.get('res') or []
    for k, (a, b) in enumerate(S.get('res') or []):
        new = k >= len(bres)
        cv.text((x0 + 30, y + 13), f'[{a},{b}]', 21, T['yellow'] if new else T['green'], anchor='lm', mono=True)
        bar(a, b, y, T['green'], 26)
        if new:
            cv.rect((X(a) - 3, y - 3, max(X(b), X(a) + 8) + 3, y + 29), outline=T['yellow'], width=3, r=14)
        y += 38
    ay = y1 - 30
    cv.line([(L, ay), (R, ay)], T['border'], 2)
    for v in range(LO, HI + 1):
        if v % 2 == 0:
            cv.line([(X(v), ay - 4), (X(v), ay + 4)], T['dim'], 2)
            cv.text((X(v), ay + 6), str(v), 17, T['dim'], anchor='mt')


def _for_cap(S, B, ret):
    if 'index' in S and S.index != B.get('index'):
        return f'扫描第 {S.index} 个区间 b = `{S.interval}`'
    return '所有区间扫描完毕'


def _fin_cap(S, B, ret):
    if S.finish_flag:
        return 'a ==已经插入完毕== → b 直接加入答案，不用再比较'
    return '`finish_flag = False`：a 还没插入，需要比较 a 和 b'


def _left_cap(S, B, ret):
    a, b = S.newInterval, S.interval
    if a[1] < b[0]:
        return f'`a.right = {a[1]} < b.left = {b[0]}`：a 和 b 不重叠，==a 在 b 左侧== → a 最终就在 b 前面'
    return f'`a.right = {a[1]} ≥ b.left = {b[0]}`：a 不在 b 左侧'


def _right_cap(S, B, ret):
    a, b = S.newInterval, S.interval
    if a[0] > b[1]:
        return f'`a.left = {a[0]} > b.right = {b[1]}`：==a 在 b 右侧==，b 对 a 无影响 → b 先进答案，a 继续往后比'
    return f'`a.left = {a[0]} ≤ b.right = {b[1]}`：a 与 b ==部分重叠== → 合并'


CONFIG = dict(
    num=57, title='插入区间', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='一趟扫描 · 三种位置关系',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def insert(self, intervals, newInterval):
        res = []
        finish_flag = False
        for index, interval in enumerate(intervals):
            if finish_flag:
                res.append(interval)
            elif newInterval[1] < interval[0]:
                res.append(newInterval)
                res.append(interval)
                finish_flag = True
            elif newInterval[0] > interval[1]:
                res.append(interval)
            else:
                newInterval[0] = min(newInterval[0], interval[0])
                newInterval[1] = max(newInterval[1], interval[1])

        if not finish_flag:
            res.append(newInterval)

        return res
''',
    call=f'Solution().insert({INTERVALS}, {NEW})',
    expect=[[1, 2], [3, 10], [12, 16], [17, 19]],
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('index', 'index', 'yellow'), ('b = interval', 'interval', 'yellow'), ('a = newInterval', 'newInterval', 'orange'),
           ('finish_flag', 'finish_flag', 'purple')],
    captions={
        'res = []': '`res` 存放答案区间',
        'finish_flag = False': '`finish_flag` 表示新区间 a ==是否已经插入==进答案',
        'for index, interval': _for_cap,
        'if finish_flag': _fin_cap,
        7: 'b = `{interval}` 直接加入答案',
        'elif newInterval[1] < interval[0]': _left_cap,
        9: '先把 a = `{newInterval}` 加入答案',
        10: '再把 b = `{interval}` 加入答案',
        'finish_flag = True': 'a 插入完毕：`finish_flag = True`',
        'elif newInterval[0] > interval[1]': _right_cap,
        13: 'b = `{interval}` 加入答案',
        'newInterval[0] = min': lambda S, B, ret: f'合并：`a.left = min({B.newInterval[0]}, {S.interval[0]}) = {S.newInterval[0]}`',
        'newInterval[1] = max': lambda S, B, ret: (f'合并：`a.right = max({B.newInterval[1]}, {S.interval[1]}) = {S.newInterval[1]}`'
                                                   f' → a 变成 `{S.newInterval}`，继续和后面的 b 比较'),
        'if not finish_flag': lambda S, B, ret: ('a 始终没插入 → 它应该加到答案==末尾==' if not S.finish_flag
                                                 else '`finish_flag = True`：a 已经插入过了，不用补'),
        19: 'a = `{newInterval}` 加到答案末尾',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='从左往右扫描：a 在左就插入，a 在右就跳过，重叠就合并',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['给你按起点排序、互不重叠的区间列表 `intervals`，插入新区间 `newInterval`',
                 '插入后仍要==有序且不重叠==（必要时合并区间）',
                 '示例：`[[1,2],[3,5],[6,7],[8,10],[12,16]]` 插入 `[4,8]` → `[[1,2],[3,10],[12,16]]`',
                 '本视频在末尾多加了 `[17,19]`，用来演示 a 插入之后的情况'],
        before=[dict(heading='a 与 b 的三种关系', lines=[
            '1、a 与 b 不重叠，且 a 在 b 左侧：`a.right < b.left`',
            '2、a 与 b 不重叠，且 a 在 b 右侧：`a.left > b.right`',
            '3、部分重叠：合并，`a.left = min(..)`，`a.right = max(..)`'])],
        quote='如果a未插入完毕，且a在b的左侧，那么说明a最终的位置就是在b的左侧，此时将a与b加入答案即可。……==如果a始终都未插入进来，那么说明a应该加入到答案的末尾==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`finish_flag` 记录 a 是否已插入；插入后剩下的 b 原样加入答案',
              'a 在 b 右侧：b 先进答案，a ==还要和后面的 b 继续比较==',
              '重叠：把 b 合并进 a（a 变大），也先不放进答案'],
        result='运行结束，返回 `[[1,2],[3,10],[12,16],[17,19]]`：a 吞掉了 `[3,5][6,7][8,10]`',
        summary=['时间 `O(n)`：每个区间只看一次',
                 '易错：a 可能一直没插入（比所有区间都靠右或和最后一个合并），循环后要补到末尾',
                 '代码会==原地修改 newInterval==，合并后的 a 就是同一个列表',
                 '与 56 题合并区间同一类：都是判断左右端点的大小关系',
                 '原文为 Python 2 风格，只删去了 docstring，代码未改'],
    ),
)

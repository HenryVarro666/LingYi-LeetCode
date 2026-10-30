_DONE_LINES = (16, 17, 20)      # 这几行执行后 tmp 表示“这一位写下的数字”
_RES_LINES = (17, 18, 20, 21)   # 这几行执行后，黄框停在刚写好的那一位


def _draw(cv, S, B, box, T):
    """竖式加法：a、b 右对齐，黄框 = 当前这一位，tmp 写在这一列上方"""
    x0, y0, x1, y1 = box
    a, b = S.get('a'), S.get('b')
    if a is None or b is None:
        return
    cv.text((x0 + 18, y0 + 4), '高精度加法（模 2），黄框 = 正在算的这一位', 24, T['muted'], bold=True)
    res = S.get('res') or ''
    line = S.get('_line')
    n = max(len(a), len(b)) + 1
    cw = min(100, (x1 - x0 - 260) / n)
    right = x0 + (x1 - x0) / 2 + n * cw / 2 + 40
    ys = dict(tmp=y0 + 62, a=y0 + 122, b=y0 + 216, res=y0 + 338)

    def X(c):
        return right - (c + 1) * cw

    cur = len(res) - 1 if line in _RES_LINES else len(res)
    live = 'pos_a' in S and line not in (26, 27, 29)
    if live and 0 <= cur < n:
        cv.rect((X(cur) - 4, ys['tmp'] - 8, X(cur) + cw + 4, ys['res'] + cw * 0.9 + 8), fill=T['yellow'], alpha=28, r=12)
        cv.rect((X(cur) - 4, ys['tmp'] - 8, X(cur) + cw + 4, ys['res'] + cw * 0.9 + 8), outline=T['yellow'], width=3, r=12)
    for name, s, c0, pos in (('a', a, T['blue'], 'pos_a'), ('b', b, T['pink'], 'pos_b')):
        y = ys[name]
        cv.text((X(n - 1) - 30, y + cw * 0.45), name, 30, c0, anchor='rm', bold=True)
        p = S.get(pos)
        for k, ch in enumerate(s):
            c = len(s) - 1 - k
            hit = live and k == p and line not in (23, 24)
            fill = c0 if hit else T['panel2']
            done = c < len(res) and not hit
            cv.rect((X(c) + 4, y, X(c) + cw - 4, y + cw * 0.9), fill=fill, r=8, outline=T['border'])
            cv.text((X(c) + cw / 2, y + cw * 0.45), ch, 36, T['bg'] if hit else (T['dim'] if done else T['text']),
                    anchor='mm', bold=True)
    cv.text((X(n - 1) + cw / 2, ys['b'] + cw * 0.45), '+', 40, T['muted'], anchor='mm', bold=True)
    ly = ys['b'] + cw * 0.9 + 18
    cv.line([(X(n - 1) - 10, ly), (right + 10, ly)], T['muted'], 3)
    tmp = S.get('tmp')
    tc = len(res) - 1 if line in _DONE_LINES else len(res)
    if tmp is not None and 0 <= tc < n and line not in (29,):
        cv.d.ellipse((X(tc) + cw / 2 - 20, ys['tmp'] - 2, X(tc) + cw / 2 + 20, ys['tmp'] + 38),
                     fill=T['orange'] if tmp else T['panel2'], outline=T['orange'], width=2)
        cv.text((X(tc) + cw / 2, ys['tmp'] + 18), tmp, 26, T['bg'] if tmp else T['orange'], anchor='mm', bold=True)
    cv.text((X(n - 1) - 30, ys['tmp'] + 18), 'tmp', 24, T['orange'], anchor='rm', bold=True)
    cv.text((X(n - 1) - 30, ys['res'] + cw * 0.45), 'res', 30, T['green'], anchor='rm', bold=True)
    bres = B.get('res') or ''
    for k, ch in enumerate(res):
        c = len(res) - 1 - k
        just = k == 0 and len(res) > len(bres)
        cv.rect((X(c) + 4, ys['res'], X(c) + cw - 4, ys['res'] + cw * 0.9), fill=T['green'] if just else T['panel2'], r=8,
                outline=T['yellow'] if just else T['border'], width=3 if just else 1)
        cv.text((X(c) + cw / 2, ys['res'] + cw * 0.45), ch, 36, T['bg'] if just else T['text'], anchor='mm', bold=True)
    cv.text((x0 + 22, y1 - 30), "res 是字符串：新的一位拼在最前面  str(tmp) + res", 22, T['muted'], anchor='lm')


def _cap_while(S, B, ret):
    if B.pos_a > -1 or B.pos_b > -1:
        return f'`pos_a = {B.pos_a}`，`pos_b = {B.pos_b}`：还有数位没加完 → 继续'
    return '`pos_a`、`pos_b` 都变成 -1 → 两个串都加完了，退出循环'


CONFIG = dict(
    num=67, title='二进制求和', difficulty='Easy', category='数学',
    author='yiduobo', technique='高精度加法（模 2）',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def addBinary(self, a, b):
        pos_a = len(a) - 1
        pos_b = len(b) - 1

        tmp = 0
        res = ''

        while pos_a > -1 or pos_b > -1:
            if pos_a > -1:
                tmp += int(a[pos_a])
            if pos_b > -1:
                tmp += int(b[pos_b])

            if tmp >= 2:
                tmp -= 2
                res = str(tmp) + res
                tmp = 1
            else:
                res = str(tmp) + res
                tmp = 0

            pos_a -= 1
            pos_b -= 1

        if tmp:
            res = '1' + res

        return res
''',
    call='Solution().addBinary("111", "10")',
    expect='1001',
    skip=['pos_a -= 1', 'pos_b -= 1'],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('pos_a', 'pos_a', 'blue'), ('pos_b', 'pos_b', 'pink'), ('tmp', 'tmp', 'orange'), ('res', 'res', 'green')],
    captions={
        'pos_a = len(a) - 1': '从低位（最右边）开始：`pos_a = {pos_a}`',
        'pos_b = len(b) - 1': '`pos_b = {pos_b}`',
        6: '`tmp` 一身两用：先装==这一位的和==，写完答案后变成==进位==',
        "res = ''": '`res` 是答案字符串，从右往左一位一位拼出来',
        'while pos_a > -1': _cap_while,
        'if pos_a > -1': lambda S, B, r: (f'a 还有数位：`a[{S.pos_a}]` 存在' if S.pos_a > -1 else 'a 已经加完，跳过'),
        'tmp += int(a[pos_a])': '加上 `a[{pos_a}] = {a[pos_a]}`：`tmp` = {B.tmp} + {a[pos_a]} = =={tmp}==',
        'if pos_b > -1': lambda S, B, r: (f'b 还有数位：`b[{S.pos_b}]` 存在' if S.pos_b > -1 else 'b 已经加完（更短），跳过'),
        'tmp += int(b[pos_b])': '加上 `b[{pos_b}] = {b[pos_b]}`：`tmp` = {B.tmp} + {b[pos_b]} = =={tmp}==',
        'if tmp >= 2': lambda S, B, r: (f'`tmp = {S.tmp} ≥ 2`：==满 2 进 1==' if S.tmp >= 2 else f'`tmp = {S.tmp} < 2`：不用进位'),
        'tmp -= 2': '减去 2 得到这一位：`tmp` = {tmp}',
        'tmp = 1': '向高位进 1：`tmp = 1`，带到下一位去加',
        21: '没有进位：`tmp = 0`',
        'res = str(tmp) + res': '这一位写 `{tmp}`，拼到 `res` ==最前面==：`res = "{res}"`',
        'if tmp:': lambda S, B, r: ('循环结束时 `tmp = 1`：==最高位还有进位==，别漏掉' if S.tmp else '最高位没有进位'),
        "res = '1' + res": '在最前面补上进位 `1`：`res = "{res}"`',
        'return res': '返回 =={ret}==（7 + 2 = 9）',
    },
    cards=dict(
        one_liner='高精度加法的二进制版：每位模 2，最后别漏了最高位进位',
        complexity='时间 `O(max(n, m))`，空间 `O(max(n, m))`',
        problem=['给两个二进制字符串 `a` 和 `b`，以二进制字符串的形式返回它们的和',
                 '示例：`a = "11", b = "1"` → `"100"`；`"1010" + "1011"` → `"10101"`',
                 '本视频：`"111" + "10"`（7 + 2）→ `"1001"`（9）'],
        quote='高精度加法二进制版本，依然是==从低位到高位一位一位相加==，不过这里每位的和应该是模2而不是模10，最后也需要注意==最高位进位==的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个下标从末尾往前走，`tmp` 先累加这一位的数字（还有上一位的进位）',
              '`tmp >= 2` 就减 2 写下这一位，再把 `tmp` 置 1 当进位',
              '循环只看两个串，所以结束后要单独检查 `tmp`'],
        summary=['时间 `O(max(n, m))`',
                 '易错：循环条件不含进位，结束后必须 `if tmp: res = \'1\' + res`',
                 '`res = str(tmp) + res` 每次新建字符串，最坏 `O(n^2)`；灵神用列表 append 再反转',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)

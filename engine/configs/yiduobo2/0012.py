_F = [['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
      ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
      ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'],
      ['', 'M', 'MM', 'MMM']]
_NAMES = ('个位', '十位', '百位', '千位')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'f[pos][k]：从低位往高位，pos 位上的数字 k 怎么写', 23, T['muted'], bold=True)
    hx = 110
    cell = min(64, (x1 - x0 - 40 - hx) / 10)
    sx = x0 + 20 + hx + ((x1 - x0 - 40 - hx) - cell * 10) / 2
    sy = y0 + 70
    rh = 52
    for d in range(10):
        cv.text((sx + d * cell + cell / 2, sy - 8), d, 20, T['muted'], anchor='mb', mono=True)
    pos = S.get('pos')
    num = S.get('num')
    line = S.get('_line')
    # the cell being read: on the `res = f[pos]...` line use the values before it ran
    hit = None
    if line == 11 and isinstance(B.get('pos'), int):
        hit = (B['pos'], B['num'] % 10)
    for p in range(4):
        Y = sy + p * rh
        cur = isinstance(pos, int) and p == pos
        done = isinstance(pos, int) and p < pos
        c = T['yellow'] if cur else (T['muted'] if done else T['dim'])
        cv.text((sx - 12, Y + rh / 2 - 3), f'f[{p}] {_NAMES[p]}', 20, c, anchor='rm', bold=True)
        if cur:
            cv.rect((sx - 4, Y - 2, sx + cell * len(_F[p]) + 4, Y + rh - 4), outline=T['yellow'], width=2, r=8)
        for d in range(len(_F[p])):
            X = sx + d * cell
            h = hit == (p, d)
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + rh - 8), fill=T['green'] if h else T['panel2'], r=6,
                    outline=T['yellow'] if h else T['border'], width=3 if h else 1)
            s = _F[p][d] or "''"
            fs = 20 if len(s) <= 3 else 17
            cv.text((X + cell / 2, Y + (rh - 6) / 2), s, fs, T['bg'] if h else (T['dim'] if not _F[p][d] else T['text']),
                    anchor='mm', mono=True, bold=True)
    if num is None:
        return
    y = sy + 4 * rh + 24
    cv.line([(x0 + 20, y - 10), (x1 - 20, y - 10)], T['border'], 2)
    # num as digits, lowest digit highlighted
    s = str(num) if num > 0 else '0'
    cv.text((x0 + 30, y + 30), 'num', 26, T['muted'], anchor='lm', mono=True)
    cw = 62
    for i, ch in enumerate(s):
        X = x0 + 110 + i * cw
        last = i == len(s) - 1 and num > 0
        cv.rect((X, y + 4, X + cw - 6, y + 56), fill=T['yellow'] if last else T['panel2'], r=8, outline=T['border'])
        cv.text((X + (cw - 6) / 2, y + 30), ch, 30, T['bg'] if last else T['text'], anchor='mm', bold=True, mono=True)
    if num > 0:
        cv.text((x0 + 110 + len(s) * cw + 10, y + 30), f'← 最低位 num % 10 = {num % 10}', 22, T['yellow'], anchor='lm')
    else:
        cv.text((x0 + 180, y + 30), '所有数位都处理完了', 22, T['muted'], anchor='lm')
    # res
    y += 90
    res = S.get('res', '')
    cv.text((x0 + 30, y + 30), 'res', 26, T['muted'], anchor='lm', mono=True)
    bres = B.get('res')
    new = res[:len(res) - len(bres)] if isinstance(bres, str) and res.endswith(bres) and len(res) > len(bres) else ''
    X = x0 + 110
    if not res:
        cv.text((X, y + 30), "''（空串）", 26, T['dim'], anchor='lm', mono=True)
    for i, ch in enumerate(res):
        isnew = i < len(new)
        cv.rect((X, y + 4, X + 50, y + 56), fill=T['green'] if isnew else T['panel2'], r=8, outline=T['border'])
        cv.text((X + 25, y + 30), ch, 28, T['bg'] if isnew else T['text'], anchor='mm', bold=True, mono=True)
        X += 56
    if new:
        cv.text((X + 10, y + 30), f'← "{new}" 拼在最前面', 22, T['green'], anchor='lm')


def _cap_res(S, B, ret):
    p, k = B.pos, B.num % 10
    piece = _F[p][k]
    if not piece:
        return f'{_NAMES[p]}是 `0`：`f[{p}][0]` 是空串，什么都不拼'
    why = '（低位先算，高位要放左边）' if p == 0 else ''
    return f'{_NAMES[p]}是 `{k}` → 查表 `f[{p}][{k}] = \'{piece}\'`，==拼在 res 前面=={why} → `res = \'{S.res}\'`'


CONFIG = dict(
    num=12, title='整数转罗马数字', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按位打表 · 从低位往高位拼',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def intToRoman(self, num):
        f = [['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
             ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
             ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'],
             ['', 'M', 'MM', 'MMM']]

        res = ''
        pos = 0
        while num > 0:
            res = f[pos][num % 10] + res
            num //= 10
            pos += 1

        return res
''',
    call='Solution().intToRoman(1994)',
    expect='MCMXCIV',
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('num', 'num', 'yellow'), ('num % 10', 'num % 10'), ('pos', 'pos', 'cyan'), ('res', 'res', 'green')],
    captions={
        "res = ''": '表 `f` 打好了：`f[pos][k]` = 第 `pos` 位数字为 `k` 时的写法；`res` 从空串开始',
        'pos = 0': '`pos = 0`：先处理个位',
        'while num > 0': lambda S, B, ret: (f'`num = {B.num} > 0`：还有数位没处理' if B.num > 0
                                            else '`num = 0`：所有数位都拼好了 → 结束'),
        'res = f[pos]': _cap_res,
        'num //= 10': '`num //= 10` → `{num}`：扔掉已处理的最低位',
        'pos += 1': lambda S, B, ret: f'`pos` → `{S.pos}`：下一轮处理{_NAMES[S.pos] if S.pos < 4 else "更高位"}',
        'return res': '返回 =={ret}==',
    },
    skip=[3, 4, 5, 6],
    cards=dict(
        one_liner='每一位的写法和其他位无关：按位打表，从低位往高位拼到前面',
        complexity='时间 `O(1)`（最多 4 位），空间 `O(1)`',
        problem=['把整数 `num`（`1 ≤ num ≤ 3999`）转成罗马数字',
                 '符号：`I=1 V=5 X=10 L=50 C=100 D=500 M=1000`；4、9 开头用==减法形式==（`IV IX XL XC CD CM`）',
                 '示例：`3749` → `"MMMDCCXLIX"`；本视频 `1994` → `"MCMXCIV"`'],
        quote='由于==每一位上的数字表示方法实际上和其他位上没什么关系==，所以最快的应该是按位打表。另外还需要注意高低位的顺序不要弄反了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num % 10` 取出最低位，`f[pos][k]` 查出它的写法',
              '先算出来的是低位，高位应该在左边 → `res = 片段 + res`（==拼到前面==）',
              '`num //= 10` 扔掉最低位，`pos += 1` 换下一张表'],
        result='`1994` → `M` + `CM` + `XC` + `IV` = `MCMXCIV` ✓',
        after=[dict(heading='原文的另一种写法：正经按位来做', lines=[
            '设当前位数字为 `x`，单位一/五/十分别是 `one[pos]` / `five[pos]` / `ten[pos]`',
            '`x ≤ 3`：`x` 个单位一；`x = 4`：单位一 + 单位五',
            '`x = 9`：单位一 + 单位十；`5 ≤ x ≤ 8`：单位五 + `x − 5` 个单位一',
            '打表就是把这 10 种情况提前写好，代码更短'])],
        summary=['时间、空间都是 `O(1)`：最多循环 4 次',
                 '易错：低位先算，必须 `res = f[...] + res`，写反会得到 `IVXCCMM`',
                 '`f[pos][0]` 是空串，数位是 0 时自动跳过',
                 '原文为 Python 2 写法，`num /= 10` 已改为 `num //= 10`；删去了文档字符串和注释掉的旧写法',
                 '对比灵神：灵神直接用 `num // 1000` 等公式一次拼出，yiduobo 用循环逐位取'],
    ),
)

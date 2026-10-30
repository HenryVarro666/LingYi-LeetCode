import sys as _sys

EMAIL, PHONE = 'AB@qq.com', '86-(10)12345678'


def _up(name, test, depth=16):
    # 取调用栈上层的局部变量（custom 视图只拿到当前这一步的 S；这里取全部关键帧，用来数“处理到第几个字符”）
    f = _sys._getframe(2)
    for _ in range(depth):
        if f is None:
            return None
        v = f.f_locals.get(name)
        if v is not None and test(v):
            return v
        f = f.f_back
    return None


_cache = {}


def _history():
    vid = _up('self', lambda x: hasattr(x, 'keys') and hasattr(x, 'draw_viz'))
    if vid is None:
        return []
    if _cache.get(id(vid), (None,))[0] is not vid:  # 存下 vid 本身，避免对象 id 被复用后拿到旧缓存
        order, seen = [], set()
        for stt, _, _ in vid.keys:
            S_ = stt.get('_S')
            if S_ is None or id(S_) in seen:
                continue
            seen.add(id(S_))
            order.append(S_)
        _cache[id(vid)] = (vid, order)
    return _cache[id(vid)][1]


def _cursor(S):
    """当前处理的是输入串的第几个字符（电话：从右往左；邮箱：域名部分从左往右）"""
    hist = _history()
    idx = next((i for i, h in enumerate(hist) if h is S), None)
    if idx is None:
        return None
    s = S['S']
    if S['_line'] == 8:
        n = sum(1 for h in hist[:idx + 1] if h.get('S') == s and h['_line'] == 8)
        return len(s) - n
    if S['_line'] in (9, 10, 11, 12, 13, 14, 15):
        n = sum(1 for h in hist[:idx + 1] if h.get('S') == s and h['_line'] == 8)
        return len(s) - n
    if S['_line'] in (36, 38):
        n = sum(1 for h in hist[:idx + 1] if h.get('S') == s and h['_line'] in (36, 38))
        return s.index('@') + n
    return None


def _cells(cv, T, x, y, text, cw, colors, size=30):
    for i, ch in enumerate(text):
        fill, tc, oc = colors(i, ch)
        cv.rect((x + i * cw + 3, y, x + (i + 1) * cw - 3, y + 54), fill=fill, outline=oc, width=3 if oc != T['border'] else 1, r=8)
        cv.text((x + i * cw + cw / 2, y + 27), ch, size, tc, anchor='mm', mono=True, bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S.get('S')
    if s is None:
        return
    phone = '@' not in s
    cur = _cursor(S)
    cv.text((x0 + 18, y0 + 4), f"输入 S（{'电话号码：从右往左扫描' if phone else '邮箱地址：按 @ 分成两部分'}）", 24, T['muted'], bold=True)
    cw = min(64, (x1 - x0 - 40) / max(len(s), 1))
    sx = x0 + 20 + (x1 - x0 - 40 - cw * len(s)) / 2

    def col_in(i, ch):
        oc = T['border']
        if phone:
            fill = T['panel2'] if ch.isdigit() else (40, 45, 53)
            tc = T['text'] if ch.isdigit() else T['dim']
            if cur is not None and i > cur:
                tc = T['muted']
        else:
            at = s.index('@')
            fill = (52, 40, 70) if i < at else ((30, 55, 60) if i > at else T['panel2'])
            tc = T['text']
            if 'parts' in S and i in (0, at - 1) and S['_line'] in (20, 21, 23, 27, 28, 30):
                oc = T['yellow']
        if cur is not None and i == cur:
            fill, tc = T['blue'], T['bg']
        return fill, tc, oc
    _cells(cv, T, sx, y0 + 46, s, cw, col_in)
    if phone and 'cnt' in S:
        # 每个数字下面标出它是倒数第几个数字
        k = 0
        for i in range(len(s) - 1, -1, -1):
            if s[i].isdigit():
                k += 1
                if cur is not None and i >= cur:
                    c = T['yellow'] if k in (5, 8, 11) else T['muted']
                    cv.text((sx + i * cw + cw / 2, y0 + 108), k, 18, c, anchor='mt', mono=True)
        cv.text((x0 + 18, y0 + 136), '数字下方 = 第几个数字（cnt）；黄色 = 5、8、11：在它前面加 -', 19, T['dim'])
    elif not phone and 'parts' in S:
        at = s.index('@')
        cv.text((sx + at * cw / 2, y0 + 108), f"parts[0] = '{s[:at]}'", 20, T['purple'], anchor='mt', bold=True)
        cv.text((sx + (at + 1) * cw + (len(s) - at - 1) * cw / 2, y0 + 108), f"parts[1] = '{s[at + 1:]}'", 20, T['cyan'], anchor='mt', bold=True)
    # 结果 res
    res = S.get('res')
    cv.text((x0 + 18, y0 + 180), 'res', 24, T['muted'], bold=True)
    if res is None:
        cv.text((x0 + 18, y0 + 222), '（尚未创建）', 22, T['dim'])
        return
    bres = B.get('res') if B.get('S') == s else None
    cw2 = min(56, (x1 - x0 - 40) / max(len(res), 16))
    rx = x0 + 20

    def col_out(i, ch):
        new = False
        if isinstance(bres, str):
            if phone:
                new = i < len(res) - len(bres)          # 电话：新字符加在最前面
            else:
                new = i >= len(bres)                    # 邮箱：新字符加在最后面
        elif bres is None:
            new = True
        fill = T['panel2']
        tc = T['orange'] if ch == '*' else (T['cyan'] if ch in '-+@' else T['text'])
        return fill, tc, (T['yellow'] if new else T['border'])
    _cells(cv, T, rx, y0 + 214, res, cw2, col_out, size=28)
    rule = ('电话：只留最后 4 位，其余数字变 `*`；==第 5、8、11 个数字前加 -==，超过 10 位加 `+`' if phone else
            '邮箱：全部转小写，名字只留==首尾字母==，中间换成 5 个 `*`')
    cv.rich(x0 + 22, y0 + 300, rule, x1 - x0 - 40, size=24)


def _digit(S, B, ret):
    if S.char >= '0' and S.char <= '9':
        return f"`'{S.char}'` 是数字 → 它是倒数第 `{S.cnt + 1}` 个数字"
    return f"`'{S.char}'` 不是数字（分隔符）→ 直接丢掉"


CONFIG = dict(
    num=831, title='隐藏个人信息', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按 @ 分割 · 电话从后往前数数字',
    tags=['字节30天'],
    code='''
class Solution(object):
    def maskPII(self, S):
        parts = S.split('@')
        if len(parts) == 1:
            cnt = 0
            res = ''
            for char in S[::-1]:
                if char >= '0' and char <= '9':
                    cnt += 1
                    if cnt == 5 or cnt == 8 or cnt == 11:
                        res = '-' + res
                    if cnt <= 4:
                        res = char + res
                    else:
                        res = '*' + res

            if cnt > 10:
                res = '+' + res
        else:
            if parts[0][0] >= 'A' and parts[0][0] <= 'Z':
                res = chr(ord(parts[0][0]) + 32)
            else:
                res = parts[0][0]

            res += '*' * 5

            if parts[0][-1] >= 'A' and parts[0][-1] <= 'Z':
                res += chr(ord(parts[0][-1]) + 32)
            else:
                res += parts[0][-1]

            res += '@'

            for char in parts[1]:
                if char >= 'A' and char <= 'Z':
                    res = res + chr(ord(char) + 32)
                else:
                    res = res + char

        return res
''',
    call=f"(Solution().maskPII('{EMAIL}'), Solution().maskPII('{PHONE}'))",
    expect=('a*****b@qq.com', '+**-***-***-5678'),
    skip=['for char in S[::-1]', 'cnt += 1', 'if cnt == 5 or', 'if cnt <= 4', 'for char in parts[1]',
          "if char >= 'A' and char <= 'Z'"],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=lambda S: (f"`res = '{S['res']}'`" + (f"　`cnt = {S['cnt']}`" if 'cnt' in S else '')) if 'res' in S else '',
             size=28, h=60),
    ],
    watch=[('S', 'S'), ('char', 'char', 'blue'), ('cnt', 'cnt', 'yellow')],
    captions={
        "parts = S.split('@')": lambda S, B, r: (f"用 `@` 分割：`parts = {S.parts}`"
                                                  + ('：只有一部分 → ==电话号码==' if len(S.parts) == 1 else '：两部分 → ==邮箱地址==')),
        'if len(parts) == 1': lambda S, B, r: ('分割后只有一个部分 → 按电话号码处理' if len(S.parts) == 1 else
                                               '分割后有两个部分 → 按邮箱处理'),
        'cnt = 0': '`cnt` 数==已经扫过几个数字==',
        "res = ''": '从后往前扫，`res` 从前面一个个拼',
        "if char >= '0' and char <= '9'": _digit,
        "res = '-' + res": lambda S, B, r: f"`cnt = {S.cnt}`（5、8 或 11）→ 先在前面加 `-`",
        'res = char + res': lambda S, B, r: f"`cnt = {S.cnt} ≤ 4`：最后 4 位==保留==，加上 `'{S.char}'`",
        "res = '*' + res": lambda S, B, r: f"`cnt = {S.cnt} > 4`：不是最后 4 位 → 加 `*`",
        'if cnt > 10': lambda S, B, r: (f"`cnt = {S.cnt} > 10`：有国家代码 → ==国际号码==" if S.cnt > 10 else
                                        f"`cnt = {S.cnt}`：本地号码，不加 `+`"),
        "res = '+' + res": '最前面再加 `+` → `{res}`',
        "if parts[0][0] >= 'A'": lambda S, B, r: (f"名字首字母 `'{S.parts[0][0]}'` 是大写 → 要转小写"
                                                   if 'A' <= S.parts[0][0] <= 'Z' else f"名字首字母 `'{S.parts[0][0]}'` 已是小写"),
        'res = chr(ord(parts[0][0]) + 32)': "`ord + 32` 把大写转成小写：`res = '{res}'`",
        'res = parts[0][0]': "`res = '{res}'`",
        "res += '*' * 5": '中间==固定加 5 个 *==（不管名字多长）',
        "if parts[0][-1] >= 'A'": lambda S, B, r: (f"名字末字母 `'{S.parts[0][-1]}'` 是大写 → 转小写"
                                                    if 'A' <= S.parts[0][-1] <= 'Z' else f"名字末字母 `'{S.parts[0][-1]}'` 已是小写"),
        'res += chr(ord(parts[0][-1]) + 32)': "加上小写的末字母 → `'{res}'`",
        "res += '@'": '加上 `@`，接下来处理域名',
        'res = res + chr(ord(char) + 32)': lambda S, B, r: f"域名字符 `'{S.char}'` 是大写 → 转小写后加入",
        'res = res + char': lambda S, B, r: f"域名字符 `'{S.char}'` 不是大写字母 → 原样加入",
        'return res': lambda S, B, r: f"返回 =={r}==",
    },
    max_steps=70,
    cards=dict(
        one_liner='先按 @ 分割；电话从后往前数数字，邮箱首尾字母加 5 个 *',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`S` 是邮箱或电话号码，按规则隐藏信息：',
                 '邮箱：全部小写，名字只留首尾字母，中间变 `*****`：`AB@qq.com` → `a*****b@qq.com`',
                 '电话：去掉分隔符，只留最后 4 位：`***-***-XXXX`；有国家代码再加 `+**-`',
                 '示例：`86-(10)12345678` → `+**-***-***-5678`'],
        quote='若分割后只有一个部分，说明S是一个电话号码，此时可以==从后往前遍历S==……当cnt为5、8或11时，应该加上-；当cnt小于等于4时，就将当前数字加入到答案中，否则应该在答案中加入*。',
        quote_src='—— yiduobo 题解',
        idea=['直接按照题目要求进行处理即可：先通过 `@` 分割判断类型',
              '电话：==从后往前==数数字，第几个数字决定是保留、打 `*` 还是先加 `-`',
              '邮箱：首字母、5 个 `*`、末字母、`@`、域名，逐个转小写拼起来'],
        result="两个示例都对 ✓：`a*****b@qq.com`、`+**-***-***-5678`",
        summary=['时间 `O(n)`；字符串前插 `res = x + res` 每次复制，长度很短可以接受',
                 '为什么从后往前？最后 4 位和分组位置都是==从右往左数==的，国家代码长度不定',
                 '分隔符 `+ - ( ) 空格` 都不是数字，扫描时直接跳过',
                 '`chr(ord(c) + 32)` 是手写的转小写，等价于 `c.lower()`',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)

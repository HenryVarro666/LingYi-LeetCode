from math import comb as _comb

LEFT, RIGHT = 10, 15
PR = [2, 3, 5, 7, 11, 13, 17, 19]

CODE = '''
primes = [2, 3, 5, 7, 11, 13, 17, 19]

class Solution:
    def calc(self, high: int) -> int:
        # 转换成计算 < high + 1 的合法正整数个数
        # 这样转换可以方便下面的代码把 high 也算进来
        high += 1
        res = ones = 0
        for i in range(high.bit_length() - 1, -1, -1):
            if high >> i & 1 == 0:
                continue
            # 如果这一位填 0，那么后面可以随便填
            # 问题变成在 i 个位置中填 k 个 1 的方案数，满足 ones + k 是质数
            for p in primes:
                k = p - ones  # 剩余需要填的 1 的个数
                if k > i:
                    break
                if k >= 0:
                    res += comb(i, k)
            # 这一位填 1，继续计算
            ones += 1
        return res

    def countPrimeSetBits(self, left: int, right: int) -> int:
        return self.calc(right) - self.calc(left - 1)
'''
_LINES = CODE.strip('\n').split('\n')


def _src(S):
    ln = S.get('_line', 0)
    return _LINES[ln - 1] if 0 < ln <= len(_LINES) else ''


def _calc(h):
    """复刻 calc，返回 (结果, 每次累加的 (i, k, C) 列表)"""
    h += 1
    res = ones = 0
    log = []
    for i in range(h.bit_length() - 1, -1, -1):
        if h >> i & 1 == 0:
            continue
        for p in PR:
            k = p - ones
            if k > i:
                break
            if k >= 0:
                res += _comb(i, k)
                log.append((i, k, _comb(i, k)))
        ones += 1
    return res, log


R1, _ = _calc(RIGHT)
R2, _ = _calc(LEFT - 1)
IN_P = ('for p in', 'k = p', 'if k > i', 'break', 'if k >= 0', 'res += comb')


def _loop_done(S, B):
    src = _src(S)
    if 'return res' in src:
        return True
    return 'for i in' in src and B.get('i') == 0 and S.get('i') == 0


def _cell(cv, T, x, y, s, size, fill, col, out=None, w=66):
    cv.rect((x, y, x + w - 6, y + w - 6), fill=fill, outline=out, width=3, r=8)
    cv.text((x + (w - 6) / 2, y + (w - 6) / 2), s, size, col, anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'high' not in S:
        cv.text((x0 + 18, y0 + 4), '差分：[left, right] 的答案 = calc(right) − calc(left − 1)', 24, T['muted'], bold=True)
        return
    high = S['high']
    src = _src(S)
    cv.text((x0 + 18, y0 + 4), f'calc({high - 1})：统计 ≤ {high - 1}，即 < high = {high} 的合法正整数', 24,
            T['muted'], bold=True)
    nb = high.bit_length()
    i = S.get('i')
    done = _loop_done(S, B)
    if done:
        i = None
    w = 70
    bx = x0 + 190
    # 第 1 行：high 的二进制
    y = y0 + 52
    cv.text((x0 + 30, y + 30), f'high = {high}', 28, T['text'], anchor='lm', bold=True)
    for j in range(nb):
        pos = nb - 1 - j
        bit = high >> pos & 1
        _cell(cv, T, bx + j * w, y, bit, 30, T['panel2'], T['text'] if bit else T['dim'],
              T['yellow'] if pos == i else None)
        cv.text((bx + j * w + 32, y + 70), f'i={pos}', 18, T['yellow'] if pos == i else T['dim'], anchor='mt', mono=True)
    # 第 2 行：这一位填 0、后面随便填
    y2 = y0 + 168
    ones = S.get('ones', 0)
    bit_i = (high >> i & 1) if i is not None else 0
    show_tpl = i is not None and bit_i == 1 and 'continue' not in src and 'for i in' not in src
    if show_tpl:
        fill1 = 'ones += 1' in src
        cv.text((x0 + 30, y2 + 30), '填 1 照抄' if fill1 else '这一位填 0', 26, T['green'] if fill1 else T['yellow'],
                anchor='lm', bold=True)
        for j in range(nb):
            pos = nb - 1 - j
            if pos > i or (pos == i and fill1):
                bit = high >> pos & 1
                _cell(cv, T, bx + j * w, y2, bit, 30, T['panel'], T['green'] if bit else T['dim'], T['border'])
            elif pos == i:
                _cell(cv, T, bx + j * w, y2, 0, 30, T['yellow'], T['bg'])
            else:
                _cell(cv, T, bx + j * w, y2, '?', 30, T['panel2'], T['blue'], T['blue'])
        xr = bx + nb * w + 20
        if fill1:
            cv.text((xr, y2 + 30), f'前缀和 high 一样，ones = {ones}', 24, T['green'], anchor='lm', bold=True)
        else:
            cv.text((xr, y2 + 16), f'左边照抄 high：已有 ones = {ones} 个 1', 22, T['green'], anchor='lm', bold=True)
            cv.text((xr, y2 + 46), f'右边 i = {i} 个 ? 随便填 → 必然 < high', 22, T['blue'], anchor='lm', bold=True)
    elif i is not None and bit_i == 0 and 'continue' in src or ('if high >>' in src and bit_i == 0):
        cv.text((x0 + 30, y2 + 30), f'high 第 {i} 位是 0：只能填 0（填 1 就超过 high 了），没有「填 0 随便填」分支', 24,
                T['muted'], anchor='lm', bold=True)
    elif done:
        cv.text((x0 + 30, y2 + 30), f'所有位处理完：calc({high - 1}) = {S.get("res")}', 28, T['green'], anchor='lm', bold=True)
    # 第 3 行：枚举质数 p
    y3 = y0 + 290
    cv.text((x0 + 30, y3 + 26), '质数 p', 26, T['text'], anchor='lm', bold=True)
    inp = any(t in src for t in IN_P) and 'p' in S and i is not None
    pw = 64
    for j, p in enumerate(PR):
        cur = inp and p == S['p']
        tooBig = inp and p - ones > i and p > S['p']
        _cell(cv, T, bx + j * pw, y3, p, 24 if p < 10 else 22, T['purple'] if cur else T['panel2'],
              T['bg'] if cur else (T['dim'] if tooBig else T['text']), w=pw)
    if inp and 'k' in S and 'for p in' not in src:
        k = S['k']
        if k > i:
            msg = f'k = {S["p"]} − {ones} = {k} > i = {i}：位置不够 → break'
            col = T['red']
        elif k < 0:
            msg = f'k = {k} < 0：前面的 1 已经多于 p'
            col = T['red']
        else:
            msg = f'k = p − ones = {S["p"]} − {ones} = {k}：方案数 C({i}, {k}) = {_comb(i, k)}'
            col = T['cyan']
        cv.text((x0 + 30, y3 + 90), msg, 26, col, anchor='lm', bold=True)


def _res_text(S):
    if 'high' not in S or 'res' not in S:
        return '`res`：所有「某一位填 0、后面随便填」的方案数之和'
    _, log = _calc(S['high'] - 1)
    acc, parts = 0, []
    for (i, k, c) in log:
        if acc >= S['res']:
            break
        acc += c
        parts.append(f'C({i},{k})')
    if not parts:
        return '`res = 0`'
    return '`res = ' + ' + '.join(parts) + f' =` =={S["res"]}=='


def _ans_text(S):
    first = S.get('high') == RIGHT + 1 if 'high' in S else True
    if 'high' not in S or first:
        return f'答案 = `calc({RIGHT}) − calc({LEFT - 1})` = `? − ?`'
    return f'答案 = `calc({RIGHT}) − calc({LEFT - 1})` = `{R1} − ?`（`calc({RIGHT}) = {R1}` 已算出）'


def _for_i(S, B, ret):
    if _loop_done(S, B):
        return '所有位都处理完了'
    i, h = S['i'], S['high']
    if 'i' not in B:
        return f'从最高位往低位看：`high = {h:b}`，先看第 `i = {i}` 位'
    return f'看下一位 `i = {i}`'


def _if_bit(S, B, ret):
    i, h = S['i'], S['high']
    if h >> i & 1 == 0:
        return f'high 第 `{i}` 位是 0 → 只能照抄 0，没有「填 0 随便填」分支 → `continue`'
    return f'high 第 `{i}` 位是 1 → 分两种：==这一位填 0==（后面 `{i}` 位随便填）或填 1 继续往下'


def _ifk(S, B, ret):
    k, i = S['k'], S['i']
    if k > i:
        return f'`k = {k} > i = {i}`：剩下的位置放不下；质数递增，后面的 p 更放不下 → ==break=='
    return f'`k = {k} ≤ i = {i}`，放得下（且 `k ≥ 0`）'


def _ifk0(S, B, ret):
    if S['k'] >= 0:
        return f"`k = {S['k']} ≥ 0` → 合法"
    return f"`k = {S['k']} < 0`：前面已有的 1 比 `p` 还多 → 这个 p 不行"


CONFIG = dict(
    num=762, title='二进制表示中质数个计算置位', difficulty='Easy', category='技巧',
    author='灵茶山艾府', technique='组合数学 · 试填 + 组合计数',
    tags=['字节3个月', '字节6个月'],
    code=CODE,
    call=f'Solution().countPrimeSetBits({LEFT}, {RIGHT})',
    expect=5,
    skip=['if k >= 0', 'continue', 'break'],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_res_text, h=60, size=26),
        dict(type='text', fn=_ans_text, h=60, size=26),
    ],
    watch=[('high', 'high'), ('i', 'i', 'yellow'), ('ones', 'ones', 'green'), ('p', 'p', 'purple'),
           ('k', 'k', 'cyan'), ('res', 'res', 'orange')],
    captions={
        'return self.calc(right)': '差分：`[{left}, {right}]` 的个数 = `calc({right}) − calc({left - 1})`，`calc(x)` 统计 `[1, x]`',
        'high += 1': '转换成统计 ==`< high`== 的数：`high = {high}`（二进制 `{high:b}`），这样原来的 high 也被算进来',
        'res = ones = 0': '`ones`：左边==照抄 high== 已经填了几个 1',
        'for i in range': _for_i,
        'if high >> i & 1 == 0': _if_bit,
        'continue': '跳过这一位，`ones` 不变',
        'for p in primes': lambda S, B, r: (f"枚举质数 `p = {S['p']}`：要求总共 `p` 个 1" if S['p'] == 2 else f"下一个质数 `p = {S['p']}`"),
        'k = p - ones': '还需填 `k = {p} − {ones} = {k}` 个 1',
        'if k > i': _ifk,
        'break': 'break：不用再试更大的质数',
        'if k >= 0': _ifk0,
        'res += comb(i, k)': lambda S, B, r: (f"在 `{S['i']}` 个 ? 里选 `{S['k']}` 个放 1：`C({S['i']},{S['k']}) = "
                                              f"{_comb(S['i'], S['k'])}` → `res = {S['res']}`"),
        'ones += 1': '这一位填 1（和 high 一样），`ones = {ones}`，继续看更低位',
        'return res': lambda S, B, r: f"`calc({S['high'] - 1}) = {r}`：`[1, {S['high'] - 1}]` 中有 {r} 个合法数",
    },
    max_steps=80,
    cards=dict(
        one_liner='试填：某一位比上界小，后面就能随便填 → 组合数',
        complexity='时间 `O(log² R / log log R)`，空间 `O(1)`',
        problem=['统计 `[left, right]` 中二进制里 1 的个数为==质数==的整数个数',
                 '例：`21 = 10101` 有 3 个 1，3 是质数',
                 '示例：`left = 10, right = 15` → `5`（10~14，15 有 4 个 1）'],
        quote='如果这一位填 0，那么后面可以随便填。问题变成在 i 个位置中填 k 个 1 的方案数，满足 ones + k 是质数。',
        quote_src='—— 灵茶山艾府题解（方法三：组合数学，代码注释）',
        idea=['差分：答案 = `calc(right) − calc(left − 1)`',
              '从高到低试填：high 这一位是 1 时，填 0 就==一定比 high 小==',
              '后面 `i` 位随便填，选 `k = p − ones` 个 1：贡献 `C(i, k)`'],
        summary=['时间 `O(log² R / log log R)`（预处理组合数后），空间 `O(1)`',
                 '`high += 1` 把「≤ high」变成「< high」，high 自己也被统计到',
                 '易错：`k < 0` 要跳过；`k > i` 可以直接 break（质数递增）',
                 '灵神还给了暴力枚举 `bit_count()` 和上下界数位 DP `O(log² R)` 两种写法',
                 '同类：数位 DP / 试填法，如 357、600、1012'],
    ),
)

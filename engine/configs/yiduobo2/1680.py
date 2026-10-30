CODE = '''
class Solution(object):
    def concatenatedBinary(self, n):
        mod = 10 ** 9 + 7
        l = [2]
        now = 2
        while now * 2 - 1 <= n:
            l.extend([now + now] * now)
            now += now

        l.extend([now + now] * (n - now + 1))

        res = 0
        for num in range(n):
            res = (res * l[num] + num + 1) % mod

        return res
'''
_LINES = CODE.strip('\n').split('\n')
L_FOR = next(i + 1 for i, l in enumerate(_LINES) if 'for num in' in l)
L_RES = next(i + 1 for i, l in enumerate(_LINES) if 'res = (res' in l)
L_RET = next(i + 1 for i, l in enumerate(_LINES) if 'return res' in l)
N = 12
MOD = 10 ** 9 + 7


def _done(S, B):
    """已经拼进 res 的数字个数"""
    if S.get('_line') == L_RET:
        return N
    if 'num' not in S:
        return 0
    if S.get('_line') == L_RES:
        return S['num'] + 1
    if 'num' in B and B['num'] == S['num']:  # for 循环结束
        return N
    return S['num']


def _cur(S, B):
    """正在拼接的下标 num（0-based）"""
    if 'num' not in S or S.get('_line') == L_RET:
        return None
    if S.get('_line') == L_FOR and 'num' in B and B['num'] == S['num']:
        return None
    return S['num']


def _ptr(S):
    return S.get('num') if S.get('_line') != L_RET else None


def _chips(cv, S, B, box, T):
    """1..n 的二进制表示依次排开：绿 = 已拼进 res，黄 = 正在拼"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '1..n 的二进制依次拼接（绿 = 已拼进 res，黄 = 正在拼）', 24, T['muted'], bold=True)
    done, cur = _done(S, B), _cur(S, B)
    x, y = x0 + 24, y0 + 48
    cw, ch = 19, 52
    for k in range(1, N + 1):
        b = bin(k)[2:]
        w = len(b) * cw + 22
        if x + w > x1 - 16:
            x, y = x0 + 24, y + ch + 34
        i = k - 1
        if i == cur:
            fill, oc, tc = T['yellow'], T['yellow'], T['bg']
        elif i < done:
            fill, oc, tc = (35, 90, 50), T['green'], T['text']
        else:
            fill, oc, tc = T['panel2'], T['border'], T['dim']
        cv.rect((x, y, x + w, y + ch), fill=fill, outline=oc, width=2, r=8)
        cv.text((x + w / 2, y + ch / 2), b, 30, tc, anchor='mm', bold=True, mono=True)
        cv.text((x + w / 2, y + ch + 4), k, 18, T['muted'], anchor='mt', mono=True)
        x += w + 10


def _formula(S, B):
    if 'num' not in S:
        if 'l' in S:
            return '`l[i]` = 数字 `i+1` 的二进制有几位，就是 2 的几次方（拼接时要乘的数）'
        return '递推：==s[i] = s[i−1] × 2^(i 的位数) + i=='
    d = _done(S, B)
    if d == 0:
        return '还没有拼接任何数字'
    real = int(''.join(bin(k)[2:] for k in range(1, d + 1)), 2)
    if real < MOD:
        return f'拼接 1~{d}：真实值 `{real}`，没超过 `10^9+7`，`res` = =={real}=='
    return f'拼接 1~{d}：真实值 `{real}` ==超过 10^9+7==，`res` 只保存余数 `{real % MOD}`'


def _while_cap(S, B, ret):
    now = B.now
    if now * 2 - 1 <= B.n:
        bits = now.bit_length()
        return f'`{now} ~ {2 * now - 1}` 都 ≤ n = {B.n}：这一整段 {now} 个数都是 {bits} 位，可以整段填进 `l`'
    return f'`{2 * now - 1} > n = {B.n}`：最后一段 `{now} ~ {B.n}` 不完整，跳出循环单独处理'


def _res_cap(S, B, ret):
    k = B.num + 1
    m = B.l[B.num]
    raw = B.res * m + k
    bits = k.bit_length()
    s = f'拼上 `{k}`（{bin(k)[2:]}，{bits} 位）：`{B.res} × {m} + {k}`'
    if raw >= MOD:
        return s + f' = {raw}，==取模== → `res` = {S.res}'
    return s + f' = =={S.res}=='


CONFIG = dict(
    num=1680, title='连接连续二进制数字', difficulty='Medium', category='数学',
    author='yiduobo', technique='递推 s[i] = s[i−1]·2^位数 + i',
    tags=['字节3个月', '字节6个月'],
    code=CODE,
    call=f'Solution().concatenatedBinary({N})',
    expect=505379714,
    max_steps=70,
    views=[
        dict(type='array', var='l', label='l[num]：拼接数字 num+1 时 res 要乘的数（= 2^位数）', cell=76, h=190,
             pointers={_ptr: 'blue'}, pointer_labels={_ptr: 'num'}, color=lambda S, i, v: 'green' if 'num' in S and i < S['num'] else None),
        dict(type='custom', draw=_chips, h=260),
        dict(type='text', fn=_formula, size=26, h=90),
    ],
    watch=[('n', 'n'), ('now', 'now', 'pink'), ('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'mod = 10': '结果可能很大，要对 `10^9+7` 取模',
        'l = [2]': '`l[i]`：拼接数字 `i+1` 时要乘的倍数；1 只有 1 位 → `l[0] = 2`',
        'now = 2': '`now` 是当前这段位数的第一个数：2 是 2 位二进制数的开头',
        'while now * 2 - 1': _while_cap,
        'l.extend([now + now] * now)': '`{B.now}` 个 {B.now.bit_length()} 位数，每个都要乘 `2^{B.now.bit_length()}` = {2 * B.now} → `l` 追加 {B.now} 个 {2 * B.now}',
        'now += now': '下一段从 `{now}` 开始：位数多 1，个数翻倍（k 位数有 `2^(k−1)` 个）',
        'l.extend([now + now] * (n': '最后一段只有 `{n} − {now} + 1` = {n - now + 1} 个数，乘数都是 {2 * now}',
        'res = 0': '`l` 预处理完毕；`res` 就是递推里的 `s`，只保留当前值，不需要数组',
        'for num in range': lambda S, B, ret: (f'开始拼接第 {S.num + 1} 个数 `{S.num + 1}`' if _cur(S, B) is not None
                                               else '1~n 全部拼接完毕'),
        'res = (res': _res_cap,
        'return res': '返回 1~{n} 拼接后的值对 `10^9+7` 取模：=={ret}==',
    },
    cards=dict(
        one_liner='在 s[i−1] 的二进制后面接上 i：左移 i 的位数，再加 i',
        complexity='时间 `O(n)`，空间 `O(n)`（`l` 数组）',
        problem=['把 1 到 n 的二进制表示依次连接，返回对应十进制数对 `10^9+7` 取余',
                 '示例：`n = 3` → `"1"+"10"+"11"` = `"11011"` → `27`',
                 '示例：`n = 12` → 37 位二进制 → 取余后 `505379714`'],
        quote='将i拼接在s[i - 1]后面就相当于将s[i - 1]左移了…位，然后再加上i本身，于是就有s[i] = s[i - 1] * 2^l[i] + i。',
        quote_src='—— yiduobo 题解',
        idea=['`s[i]` 只和 `s[i−1]` 有关 → 只维护一个 `res`，不需要数组',
              '位数有规律：1 位数 1 个、2 位数 2 个、3 位数 4 个……==k 位数有 2^(k−1) 个==',
              '按这个规律整段扩展出乘数数组 `l`，再一趟扫描递推'],
        summary=['时间 `O(n)`，空间 `O(n)`；把 `l` 换成 `i.bit_length()` 可降到 `O(1)`',
                 '每一步都要取模：先乘后加再 `% mod`，中途取模不影响结果',
                 '`l` 里存的是 `2^位数`（乘数），不是位数本身',
                 'yiduobo 也推了按位数分组的等比数列公式（`O(log²n)`），但没往下实现',
                 '原文为 Python 2 写法，已删去文档字符串，逻辑未改'],
    ),
)

NUM = 50000115
SUF = ['', ' Thousand', ' Million', ' Billion']


def _groups(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'suffix_pos' not in S:
        return
    pos = S['suffix_pos']
    cv.text((x0 + 18, y0 + 4), '按千分割（从低位往高位处理；黄 = 当前段）', 24, T['muted'], bold=True)
    w = (x1 - x0 - 60) / 4
    for k, i in enumerate(range(3, -1, -1)):
        X = x0 + 20 + k * (w + 6)
        x = NUM // 10 ** (i * 3) % 1000
        on = i == pos and S.get('num', 0) > 0
        done = i < pos
        fill = T['yellow'] if on else T['panel2']
        cv.rect((X, y0 + 44, X + w, y0 + 124), fill=fill, r=12, outline=T['border'])
        tc = T['bg'] if on else (T['dim'] if done else T['text'])
        cv.text((X + w / 2, y0 + 84), f'{x:03d}', 40, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + w / 2, y0 + 136), f'suffix[{i}]', 20, T['yellow'] if on else T['muted'], anchor='mt', mono=True)
        cv.text((X + w / 2, y0 + 164), repr(SUF[i]), 20, T['dim'], anchor='mt', mono=True)


def _strs(S):
    if 'res' not in S:
        return ''
    pr = S.get('part_res')
    a = f"part_res = `{pr!r}`" if pr is not None else ''
    return a + ('\n' if a else '') + f"res = `{S['res']!r}`"


def _cap_while(S, B, ret):
    if B.num:
        return f'`num = {B.num}` ≠ 0 → 还有没处理的段'
    return '`num = 0`：所有段都处理完了'


def _cap_tmp0(S, B, ret):
    if S.tmp == 0:
        return '十位和个位都是 0 → 这部分是空串'
    return f'`tmp = {S.tmp}` 不为 0 → 要翻译十位和个位'


def _cap_lt20(S, B, ret):
    if S.tmp < 20:
        return f'`{S.tmp} < 20`：在 20 以内，==有特有的单词==与之对应'
    return f'`{S.tmp} ≥ 20`：按十位与个位分割'


def _cap_if_tmp(S, B, ret):
    if S.tmp:
        return f'个位 `{S.tmp}` 不为 0 → 接在后面'
    return '个位是 0 → ==0 不会表示在结果中==，什么也不加'


def _cap_hund(S, B, ret):
    if S.hundred > 0:
        return f'`hundred = {S.hundred}` > 0 → 前面还要加 `"{["Zero","One","Two","Three","Four","Five","Six","Seven","Eight","Nine"][S.hundred]} Hundred"`'
    return '没有百位'


def _cap_pr_inner(S, B, ret):
    if S.part_res:
        return '后两位不为空 → `Hundred` 后面==要加空格==再接上'
    return '后两位是空串 → `Hundred` 后面==不能多出空格=='


def _cap_pr_outer(S, B, ret):
    if S.part_res:
        return f'这一段非空：`"{S.part_res}"` → 带上单位拼进 `res`'
    return '这一段是空串（三位全是 0）→ 整段跳过，连单位都不加'


def _cap_if_res(S, B, ret):
    if S.res:
        return f'`res` 已经有低位的内容 → 新的一段放==前面==，中间加一个空格'
    return '`res` 还是空的 → 不用加空格'


CONFIG = dict(
    num=273, title='整数转换英文表示', difficulty='Hard', category='字符串',
    author='yiduobo', technique='按千分割，从低位往高位拼',
    tags=['字节30天'],
    code='''
class Solution(object):
    def numberToWords(self, num):
        suffix = ['', ' Thousand', ' Million', ' Billion']
        suffix_pos = 0

        single = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
                  'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        ten = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

        res = ''
        while num:
            tmp = num % 1000
            part_res = ''

            hundred = tmp // 100
            tmp %= 100

            if tmp == 0:
                part_res = ''
            else:
                if tmp < 20:
                    part_res = single[tmp]
                else:
                    part_res = ten[tmp // 10]
                    tmp %= 10
                    if tmp:
                        part_res = part_res + ' ' + single[tmp]

            if hundred > 0:
                if part_res:
                    part_res = single[hundred] + ' Hundred ' + part_res
                else:
                    part_res = single[hundred] + ' Hundred'

            if part_res:
                if res:
                    res = part_res + suffix[suffix_pos] + ' ' + res
                else:
                    res = part_res + suffix[suffix_pos]

            num //= 1000
            suffix_pos += 1

        if not res:
            return single[0]

        return res
''',
    call=f'Solution().numberToWords({NUM})',
    expect='Fifty Million One Hundred Fifteen',
    views=[
        dict(type='text', fn=lambda S: f"`num = {S['num']}`（原数 `{NUM:,}`）" if 'num' in S else '', h=60),
        dict(type='custom', draw=_groups, h=210),
        dict(type='text', fn=_strs, h=130, size=30, lines=2),
    ],
    watch=['num', ('tmp', 'tmp', 'yellow'), 'hundred', 'suffix_pos'],
    skip=['suffix_pos = 0', 'suffix_pos += 1', 13],
    captions={
        'suffix = [': '`suffix`：每段后面的单位；注意==自带前导空格==',
        'single = [': '`single`：0～19 都有==特有的单词==',
        'ten = [': '`ten`：二十、三十……九十',
        10: '`res` 从空串开始，==从低位段往高位段==拼',
        'while num': _cap_while,
        'tmp = num % 1000': '按千分割：取最低的三位 `tmp = {tmp}`',
        'hundred = tmp // 100': '先把百位分离出来：`hundred = {hundred}`',
        'tmp %= 100': '剩下十位和个位：`tmp = {tmp}`',
        'if tmp == 0': _cap_tmp0,
        19: '`part_res = ""`',
        'if tmp < 20': _cap_lt20,
        'part_res = single[tmp]': '`part_res = "{part_res}"`',
        'part_res = ten[tmp // 10]': '十位：`ten[{B.tmp // 10}] = "{part_res}"`',
        'tmp %= 10': '个位：`tmp = {tmp}`',
        'if tmp:': _cap_if_tmp,
        "part_res = part_res + ' ' + single[tmp]": '`part_res = "{part_res}"`',
        'if hundred > 0': _cap_hund,
        30: _cap_pr_inner,
        "part_res = single[hundred] + ' Hundred ' + part_res": '`part_res = "{part_res}"`',
        "part_res = single[hundred] + ' Hundred'": '`part_res = "{part_res}"`',
        35: _cap_pr_outer,
        'if res:': _cap_if_res,
        "res = part_res + suffix[suffix_pos] + ' ' + res": '`"{part_res}"` + `"{suffix[suffix_pos]}"` + 空格 + 旧 `res`：高位段拼在==前面==',
        'res = part_res + suffix[suffix_pos]': '`"{part_res}"` + `"{suffix[suffix_pos]}"` → `res = "{res}"`',
        'num //= 1000': '`num //= 1000` → `{num}`：去掉处理完的三位，单位升一级',
        'if not res': '`res` 非空，说明 `num` 不是 0',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='按千分割，每段先分离百位，20 以内查表，否则拆十位个位',
        complexity='时间 `O(1)`（最多 4 段），空间 `O(1)`',
        problem=['把非负整数 `num`（`≤ 2^31 - 1`）转成英文表示',
                 '示例：`12345` → `"Twelve Thousand Three Hundred Forty Five"`',
                 '演示：`50000115` → `"Fifty Million One Hundred Fifteen"`'],
        quote='按照英语的表示习惯，数字都是==按照千来进行分割==的。对于分割下来的部分，首先将百分离出来，然后对于十位和个位，如果在20以内，那么有特有的单词与之对应，否则就按十位与个位分割即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num % 1000` 取最低一段，`num //= 1000` 再处理下一段，单位依次升级',
              '新的一段（更高位）拼在 `res` 的==前面==',
              '原文提醒：==除了 num 为 0，其他时候 0 都不会出现在结果中==；还要注意空格衔接'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '空格细节：`suffix` 自带前导空格；`Hundred` 后、段与段之间按需加空格',
                 '整段为 0（如 `000`）时不加单位；`num = 0` 最后返回 `"Zero"`',
                 '原文为 Python 2 写法，`tmp / 100`、`tmp / 10`、`num /= 1000` 已改为 `//`',
                 '对比灵神：从高位往低位追加，单词放进列表，最后过滤空串再 join'],
    ),
)

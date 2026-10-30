N = 3


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    res = S.get('res')
    n = S.get('n', N)
    cv.text((x0 + 18, y0 + 4), 'res（二进制 / 十进制；绿 = 这一轮新接上的后半部分）', 24, T['muted'], bold=True)
    if res is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    old = B.get('res')
    L = len(old) if isinstance(old, list) and len(old) < len(res) else len(res)
    total = 2 ** n
    rowh = min(64, (y1 - y0 - 70) / total)
    fs = int(min(34, rowh * 0.6))
    w = S.get('weight')
    cx = (x0 + x1) / 2
    bx = cx - 150
    for i, v in enumerate(res):
        y = y0 + 52 + i * rowh
        new = i >= L
        mirror = 2 * L - 1 - i if new else None
        fill = T['green'] if new else T['panel2']
        cv.rect((bx, y + 3, bx + 300, y + rowh - 3), fill=fill, alpha=200 if new else 255, r=8,
                outline=T['border'], width=1)
        bits = format(v, f'0{n}b')
        # 逐位画：新行的最高位（weight 那一位）黄色
        hi = len(bits) - w.bit_length() if isinstance(w, int) and w > 0 and new else -1
        for k, ch in enumerate(bits):
            c = T['yellow'] if k == hi else (T['bg'] if new else T['text'])
            cv.text((bx + 40 + k * fs * 0.9, y + rowh / 2), ch, fs, c, anchor='mm', bold=True, mono=True)
        cv.text((bx + 280, y + rowh / 2), f'= {v}', fs, T['bg'] if new else T['text'], anchor='rm', bold=True)
        cv.text((bx - 16, y + rowh / 2), i, 20, T['dim'], anchor='rm', mono=True)
        if new:
            my = y0 + 52 + mirror * rowh + rowh / 2
            cv.text((bx + 320, y + rowh / 2), f'← res[{mirror}] + {w}', 24, T['yellow'], anchor='lm', bold=True)
    for i in range(len(res), total):
        y = y0 + 52 + i * rowh
        cv.rect((bx, y + 3, bx + 300, y + rowh - 3), outline=T['border'], width=1, r=8)
    if L < len(res):
        y = y0 + 52 + L * rowh
        cv.dashed((bx - 60, y), (bx + 360, y), T['yellow'], 3)
        cv.text((bx - 70, y), '镜像轴', 22, T['yellow'], anchor='rm', bold=True)


CONFIG = dict(
    num=89, title='格雷编码', difficulty='Medium', category='技巧',
    author='yiduobo', technique='镜像反射 · 前半补 0、倒序后补 1',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def grayCode(self, n):
        res = [0]

        for index in range(n):
            if index == 0:
                weight = 1
            else:
                weight += weight
            res.extend([res[pos] + weight for pos in range(len(res) - 1, -1, -1)])

        return res
''',
    call=f'Solution().grayCode({N})',
    expect=[0, 1, 3, 2, 6, 7, 5, 4],
    views=[
        dict(type='text', fn=lambda S, B: (
            f"上一轮 `{B['res']}` ==倒过来==、每个 `+ {S['weight']}` 接在后面" if isinstance(B.get('res'), list)
            and len(S.get('res', [])) > len(B['res'])
            else (f"`weight = {S['weight']}` = 二进制 `1{'0' * (S['weight'].bit_length() - 1)}`：这一轮新增的最高位"
                  if isinstance(S.get('weight'), int) else '`n` 位格雷码 = 由 `n-1` 位格雷码「镜像」得到')), size=30),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('index', 'index', 'blue'), ('weight', 'weight', 'yellow'), ('len(res)', 'len(res)', 'green')],
    captions={
        'res = [0]': '0 位格雷码只有一个：`[0]`，后面每一轮==长度翻倍==',
        'for index in range(n)': lambda S, B, ret: (
            f'第 `{S.index}` 轮：把 `{S.index}` 位格雷码扩展成 `{S.index + 1}` 位'
            if S.get('index') != B.get('index') or 'index' not in B
            else f'`{S.n}` 轮做完，`res` 就是 `{S.n}` 位格雷码'),
        'if index == 0': lambda S, B, ret: ('第一轮：最高位的值从 `1` 开始' if S.index == 0
                                            else f'`index = {S.index} ≠ 0` → 最高位的值翻倍'),
        'weight = 1': '`weight = 1`：新最高位是第 0 位，值为 `2^0`',
        'weight += weight': '`weight` 翻倍为 `{weight}`：==新最高位==的值就是 `2^{index}`',
        'res.extend': lambda S, B, ret: (
            f'前半 = 原来的 `{B.res}`（最高位补 0，值不变）；后半 = ==倒序== 再加 `{S.weight}` → '
            f'`{S.res[len(B.res):]}`'),
        'return res': '`{n}` 位格雷码：`{res}`，相邻两项只差一位',
    },
    max_steps=40,
    cards=dict(
        one_liner='格雷码倒着写依然合法：前半照抄补 0，后半倒序补 1',
        complexity='时间 `O(2^n)`，空间 `O(1)`（不计返回值）',
        problem=['`n` 位格雷码序列：`2^n` 个整数，从 `0` 开始，每个数在 `[0, 2^n - 1]` 中只出现一次',
                 '==相邻两个数（含首尾）的二进制恰好只有一位不同==',
                 '示例：`n = 2` → `[0,1,3,2]`（00 → 01 → 11 → 10）',
                 f'本视频：`n = {N}` → `[0,1,3,2,6,7,5,4]`'],
        quote='对于k位格雷码来说，可以在最高位上补0，看做k + 1位的格雷码作为前半部分，然后==将这个k位格雷码反过来，在最高位补1==作为k + 1位格雷码的后半部分。',
        quote_src='—— yiduobo 题解原文',
        idea=['原理：合法的格雷码==反过来写也一定合法==（相邻关系不变）',
              '前半补 0：数值不变，直接保留；后半倒序补 1：每个数 `+ weight`',
              '接缝处是同一个数补 0 / 补 1，只差最高位 → 仍然合法；首尾同理'],
        summary=['时间 `O(2^n)`：每轮长度翻倍，总共生成 `2^n` 个数',
                 '后半一定要==倒序==（`range(len(res) - 1, -1, -1)`），正序接上去接缝处会差多位',
                 '`weight` 每轮翻倍，等价于 `1 << index`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '公式法：第 `i` 个格雷码 = `i ^ (i >> 1)`'],
    ),
)

S0 = '00111'
N = len(S0)
# 左段长度为 l = k + 1 时的关键量 2·cnt_zero − l（只依赖左段）
KEY = [2 * S0[:k + 1].count('0') - (k + 1) for k in range(N - 1)]


def _done(S):
    """已经算出关键量的分割位置个数"""
    ln = S.get('_line')
    if 'index' not in S:
        return 0
    if ln >= 16:          # 循环结束之后
        return N - 1
    return S['index'] + (1 if ln in (13, 14) else 0)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    idx = S.get('index')
    ln = S.get('_line')
    after = ln >= 16
    cell = min(120, (x1 - x0 - 120) / N)
    sx = x0 + 60 + ((x1 - x0 - 120) - cell * N) / 2
    ys = y0 + 110
    ch = cell * 0.8
    cv.text((x0 + 18, y0 + 4), 's（左段 = 下标 0..index；左段里的 0 绿色、1 粉色）', 22, T['muted'], bold=True)
    split = None if idx is None or after else idx + 1
    for i, c in enumerate(S0):
        X = sx + i * cell
        if after:
            fill = T['blue'] if c == '1' and (i < N - 1 or ln >= 17) else T['panel2']   # 1 的总数
        elif split is not None and i < split and (i < idx or ln >= 8):
            fill = T['green'] if c == '0' else T['pink']
        else:
            fill = T['panel2']
        cv.rect((X + 5, ys, X + cell - 5, ys + ch), fill=fill, r=10, outline=T['yellow'] if i == idx and not after else T['border'],
                width=4 if i == idx and not after else 1)
        cv.text((X + cell / 2, ys + ch / 2), c, 38, T['bg'] if fill != T['panel2'] else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 10), i, 18, T['dim'], anchor='mt', mono=True)
    if idx is not None and not after:
        X = sx + idx * cell + cell / 2
        cv.tri_up(X, ys + ch + 36, 10, T['yellow'])
        cv.text((X, ys + ch + 52), 'index', 20, T['yellow'], anchor='mt', bold=True)
        Xs = sx + (idx + 1) * cell
        cv.line([(Xs, ys - 20), (Xs, ys + ch + 20)], T['yellow'], 4)
        cv.text((Xs, ys - 24), f'左段长 l = {idx + 1}', 20, T['yellow'], anchor='mb', bold=True)
    if after:
        cv.text((sx + (N - 0.5) * cell, ys - 24), '最后一位单独补进 cnt_one', 20, T['blue'], anchor='mb', bold=True)
    # 关键量表
    yb = ys + ch + 130
    cv.text((x0 + 18, yb - 8), '每种分割的 2·cnt_zero − l（得分 = 它 + 1 的总数；橙 = res）', 22, T['muted'], bold=True)
    done = _done(S)
    best = max(KEY[:done]) if done else None
    for k in range(N - 1):
        X = sx + (k + 1) * cell
        known = k < done
        hot = known and KEY[k] == best
        cv.rect((X - cell / 2 + 10, yb + 30, X + cell / 2 - 10, yb + 30 + cell * 0.66),
                fill=T['orange'] if hot else ((52, 60, 72) if known else T['panel2']), r=8, outline=T['border'])
        cv.text((X, yb + 30 + cell * 0.33), KEY[k] if known else '?', 30, T['bg'] if hot else (T['text'] if known else T['dim']),
                anchor='mm', bold=True)
        cv.text((X, yb + 38 + cell * 0.66), f'l = {k + 1}', 17, T['dim'], anchor='mt', mono=True)


def _text(S):
    if 'index' not in S:
        return '得分 = 左 0 + 右 1 = `cnt_zero + (cnt_one − (l − cnt_zero))` = `2·cnt_zero − l` + ==1 的总数=='
    if S['_line'] >= 16:
        return f"1 的总数 `cnt_one = {S['cnt_one']}`，最大得分 = `res + cnt_one`"
    i, z = S['index'], S['cnt_zero']
    if S['_line'] in (13, 14):
        return f"左段 `s[0..{i}]`：`2·cnt_zero − l = 2×{z} − {i + 1}` = =={2 * z - i - 1}==（`res = {S['res']}`）"
    return f"左段 `s[0..{i}]`，长度 `l = index + 1 = {i + 1}`"


def _cap_res_if(S, B, ret):
    i, z = S.index, S.cnt_zero
    v = 2 * z - (i + 1)
    if B.res is None:
        return f'`res` 还是 `None`：第一种分割（左段只有 1 个字符）先拿来初始化'
    if B.res < v:
        return f'`{B.res} < {v}`：这个分割更好 → 更新'
    return f'`{v}` 不比 `res = {B.res}` 大 → 不更新'


CODE = '''
class Solution(object):
    def maxScore(self, s):
        cnt_one = 0
        cnt_zero = 0
        res = None
        for index in range(len(s) - 1):
            char = s[index]
            if char == '0':
                cnt_zero += 1
            else:
                cnt_one += 1

            if res is None or res < cnt_zero + cnt_zero - (index + 1):
                res = cnt_zero + cnt_zero - (index + 1)

        if s[-1] == '1':
            cnt_one += 1

        return res + cnt_one
'''

CONFIG = dict(
    num=1422, title='分割字符串的最大得分', difficulty='Easy', category='子串',
    author='yiduobo', technique='得分公式变形 · 一趟扫描',
    tags=['List.md'],
    code=CODE,
    call=f'Solution().maxScore("{S0}")',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=60, size=26),
        dict(type='custom', draw=_draw, h=540),
    ],
    watch=[('index', 'index', 'yellow'), ('cnt_zero', 'cnt_zero', 'green'), ('cnt_one', 'cnt_one', 'pink'),
           ('res', 'res', 'orange')],
    skip=['cnt_zero = 0'],
    captions={
        'cnt_one = 0': '一趟扫描：`cnt_one` 统计 ==所有== 1，`cnt_zero` 统计左段的 0',
        'res = None': '`res = None`：答案要从「左段长度为 1」这种分割初始化，不能随便给 0',
        'for index in range': lambda S, B, r: ('扫描到 `len(s) − 2` 为止，循环结束' if B.get('index') == S.index else
                                               f'左段扩到 `s[0..{S.index}]`' + ('（index 只到 `len(s) − 2`，保证右段非空）' if 'index' not in B else '')),
        'char = s[index]': '`char = s[{index}] = \'{char}\'`',
        "if char == '0'": lambda S, B, r: ('是 0 → `cnt_zero` 加一' if S.char == '0' else '是 1 → `cnt_one` 加一'),
        'cnt_zero += 1': '`cnt_zero = {cnt_zero}`',
        11: '`cnt_one = {cnt_one}`（左段的 1 也计入总数）',
        'if res is None or': _cap_res_if,
        'res = cnt_zero': '`res = 2×{cnt_zero} − {index + 1}` = =={res}==：`cnt_one` 是常量，只比这一项',
        "if s[-1] == '1'": lambda S, B, r: ("循环没碰最后一位：`s[-1] = '1'` → 也要计入 1 的总数" if S.s[-1] == '1'
                                            else "最后一位是 0，不影响 1 的总数"),
        17: '`cnt_one = {cnt_one}`：现在是整个串里 1 的个数',
        'return res + cnt_one': '最大得分 = `res + cnt_one = {res} + {cnt_one}` = =={ret}==',
    },
    cards=dict(
        one_liner='得分 = 2·cnt_zero − l + 1 的总数，总数是常量，只需让前一项最大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 01 字符串 `s` 分成==非空==的左、右两段',
                 '得分 = 左段里 `0` 的个数 + 右段里 `1` 的个数，求最大得分',
                 '示例：`"011101"` → `5`；本视频：`"00111"` → `5`（`"00" | "111"`）'],
        quote='设所有1的数目cnt_one，那么对于长度为l的左侧字符串中，若有cnt_zero个0……此时的得分就是 ==cnt_zero * 2 - l + cnt_one==。由于这里的cnt_one是常量，为了使得得分最高，实际上就是要让cnt_zero * 2 - l 这一项最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['左段 1 的个数 = `l − cnt_zero`，右段 1 的个数 = 总数 − 左段 1',
              '代入得分：`cnt_zero + 总数 − (l − cnt_zero)` = `2·cnt_zero − l + 总数`',
              '一趟扫描求 `2·cnt_zero − l` 的最大值，==顺便==把 1 的总数统计出来'],
        summary=['时间 `O(n)`，空间 `O(1)`，只扫一遍',
                 '易错（原文提醒）：两段都非空 → 答案从左段长 1 初始化（`res = None`），只算到 `len(s) − 2`',
                 '易错：循环没扫最后一位，==别忘了用 s[-1] 更新 cnt_one==',
                 '对比灵神写法一：先 `count` 出 1 的总数再移动分割线；这里把两遍合成一遍（灵神写法三同理）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)

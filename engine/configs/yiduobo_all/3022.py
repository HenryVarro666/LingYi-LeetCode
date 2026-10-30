def _sim(nums, prefix):
    """按原文逻辑模拟：每个数 -> (tmp, 区间按位与结果或 None, 是否 need_merge += 1)"""
    out = []
    ip = None
    for v in nums:
        tmp = prefix & v
        counted = False
        if tmp:
            ip = tmp if ip is None else ip & tmp
            if ip:
                counted = True
            else:
                ip = None
            out.append((tmp, 0 if not ip else ip, counted, tmp != 0 and not counted))
        else:
            ip = None
            out.append((0, None, False, False))
    return out


def _cur(S):
    if 'v' not in S or 'prefix' not in S or 'interval_prefix' not in S:
        return None
    if S.get('_line') in (6, 7, 8, 9, 10):
        return None
    return S['nums'].index(S['v']) if S['v'] in S['nums'] else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    W = max(nums).bit_length()
    prefix = S.get('prefix', 0)
    idx = S.get('index', -1)
    cur = _cur(S)
    sim = _sim(nums, prefix) if 'prefix' in S else None
    cell = 64
    colx = lambda j: x0 + 190 + (W - 1 - j) * cell
    rx = colx(-1) + 70
    cv.text((x0 + 18, y0 + 4), '二进制视图：青色列 = prefix 里要「消成 0」的位', 22, T['muted'], bold=True)
    yh = y0 + 52
    for j in range(W - 1, -1, -1):
        cv.text((colx(j) + cell / 2, yh), f'2^{j}', 22, T['yellow'] if j == idx else T['dim'], anchor='mm', bold=True, mono=True)
    cv.text((rx + 10, yh), '区间按位与', 22, T['dim'], anchor='lm', bold=True)
    ym = yh + 34
    cv.text((x0 + 20, ym + 26), 'prefix（要消的位）', 18, T['cyan'], anchor='lm', bold=True)
    for j in range(W - 1, -1, -1):
        on = (prefix >> j) & 1
        cv.rect((colx(j) + 4, ym, colx(j) + cell - 4, ym + 52), fill=T['cyan'] if on else T['panel2'], r=8, outline=T['border'])
        cv.text((colx(j) + cell / 2, ym + 26), on, 28, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
    cv.line([(x0 + 14, ym + 66), (x1 - 14, ym + 66)], T['border'], 2)
    yr = ym + 82
    rh = 66
    for i, v in enumerate(nums):
        Y = yr + i * rh
        if cur == i:
            cv.rect((x0 + 8, Y - 2, x1 - 8, Y + 56), outline=T['pink'], width=4, r=10)
        cv.text((x0 + 20, Y + 27), f'nums[{i}] = {v}', 24, T['text'] if (cur is None or i <= cur) else T['muted'], anchor='lm', bold=True, mono=True)
        for j in range(W - 1, -1, -1):
            bit = (v >> j) & 1
            seen = (prefix >> j) & 1
            if bit and seen:
                fill, tc = T['orange'], T['bg']
            elif bit:
                fill, tc = (60, 66, 76), T['dim']
            else:
                fill, tc = T['panel2'], T['dim']
            cv.rect((colx(j) + 4, Y, colx(j) + cell - 4, Y + 54), fill=fill, r=8)
            cv.text((colx(j) + cell / 2, Y + 27), bit, 28, tc, anchor='mm', bold=True, mono=True)
        shown = sim is not None and cur is not None and (i < cur or (i == cur and S.get('_line', 0) >= 17))
        if shown:
            tmp, ip, counted, zeroed = sim[i]
            if ip is None and tmp == 0:
                cv.text((rx + 10, Y + 27), 'tmp=0：断开区间', 22, T['green'], anchor='lm', bold=True)
            elif counted:
                cv.text((rx + 10, Y + 27), f'and={ip:0{W}b}', 22, T['text'], anchor='lm', bold=True, mono=True)
                cv.text((rx + 150, Y + 27), 'need_merge +1', 22, T['pink'], anchor='lm', bold=True)
            else:
                cv.text((rx + 10, Y + 27), f'and=0{"0" * (W - 1)}', 22, T['text'], anchor='lm', bold=True, mono=True)
                cv.text((rx + 150, Y + 27), '合成 0，区间结束', 22, T['green'], anchor='lm', bold=True)
    yb = yr + len(nums) * rh + 8
    if 'need_merge' in S and 'k' in S:
        ok = S['need_merge'] <= S['k']
        cv.text((x0 + 20, yb + 8), f"need_merge = {S['need_merge']}   k = {S['k']}", 26, T['green'] if ok else T['red'], bold=True)


def _txt(S):
    if 'index' not in S:
        return '高位优先：先看这一位能不能被「与」成 0'
    return f"第 {S['index']} 位 · prefix = {S['prefix']:b}（青色 = 想消成 0 的位）"


CONFIG = dict(
    num=3022, title='给定操作次数内使剩余元素的或值最小', difficulty='Hard', category='位运算',
    author='yiduobo', technique='高位优先 · 贪心消除 + 区间合并计数',
    tags=['灵神题单·位运算', '难度分 2918'],
    code='''
class Solution(object):
    def minOrAfterOperations(self, nums, k):
        prefix = 0
        ma = max(nums)
        length = len(bin(ma)) - 2
        for index in range(length - 1, -1, -1):
            prefix |= (1 << index)
            need_merge = 0
            interval_prefix = None
            for v in nums:
                tmp = prefix & v
                if tmp:
                    if interval_prefix is None:
                        interval_prefix = tmp
                    else:
                        interval_prefix &= tmp
                    if interval_prefix:
                        need_merge += 1
                    else:
                        interval_prefix = None
                else:
                    interval_prefix = None
            if need_merge > k:
                prefix ^= (1 << index)
        return ((1 << length) - 1) ^ prefix
''',
    call='Solution().minOrAfterOperations([5,2,3,6], 2)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=28, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    skip=[10],
    watch=[('index', 'index', 'yellow'), ('prefix', 'prefix', 'cyan'), ('need_merge', 'need_merge', 'pink'),
           ('interval_prefix', 'interval_prefix', 'orange')],
    captions={
        'prefix = 0': '`prefix` 记录「已确定可以被消成 0 的位」，从空开始',
        'ma = max': '最大值决定要处理多少位',
        'length = len': '二进制位数 `length = {length}`，从最高位 `{length - 1}` 开始往下试',
        'for index in range': lambda S, B, r: ('每一位都试完了，退出循环' if 'index' in B and B.index == S.index
                                                else f'==高位优先==：第 `{S.index}` 位能不能被消成 0？'),
        'prefix |= (1 << index)': '假设第 `{index}` 位可以消掉：`prefix` → =={prefix:b}==',
        'need_merge = 0': '统计要把 prefix 里的 1 全消掉，至少要合并几次',
        9: 'None 表示「当前没有进行中的区间」',
        'tmp = prefix & v': '`tmp = {prefix} & {v}` = =={tmp}==：`{v}` 里需要被消掉的位',
        'if tmp:': lambda S, B, r: (f'`tmp = {S.tmp}` 非零：这个数里还有 1 没消掉，必须靠区间里的与运算来消'
                                    if S.tmp else '`tmp = 0`：这个数本来就是 0，自己就是一个区间，不用花操作'),
        'if interval_prefix is None': '区间是否刚开始？{"是，新开一个区间" if B.interval_prefix is None else "否，已经在区间里"}',
        'interval_prefix = tmp': '新区间开始：`interval_prefix` = =={interval_prefix}==',
        'interval_prefix &= tmp': '区间继续：与运算后 `interval_prefix` = =={interval_prefix}==',
        'if interval_prefix:': lambda S, B, r: (f'`interval_prefix = {S.interval_prefix}` 仍不为 0：还要再合并一个数 → 花一次操作'
                                                if S.interval_prefix else '`interval_prefix = 0`：这一段已经与成 0，省下这次操作'),
        'need_merge += 1': '`need_merge` → =={need_merge}==（m 个数要合并 m 次）',
        22: '区间结束，`interval_prefix` 重置为 None',
        20: '区间已经与成 0：`interval_prefix` 重置为 None，下个数重新开始',
        'if need_merge > k': lambda S, B, r: (f'`need_merge = {S.need_merge} > k = {S.k}`：消不掉这一位'
                                              if S.need_merge > S.k else f'`need_merge = {S.need_merge} ≤ k = {S.k}`：操作够，这一位可以为 0'),
        'prefix ^= (1 << index)': '消不掉就把这一位从 `prefix` 拿掉：`prefix` → =={prefix:b}==',
        'return': '答案 = 全 1 异或 `prefix` = `{(1 << length) - 1}` ^ `{prefix}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='高位优先：能消掉的位记进 prefix，答案取反',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['一次操作：把相邻两数换成它们的按位与',
                 '至多 `k` 次操作，让剩下所有数的按位或最小',
                 '演示：`[5,2,3,6]`，`k = 2` → `2`'],
        quote='若tmp本来就为0，那么说明一个区间结束了；若tmp不为0，且interval_prefix为None，说明这是一个新区间的开始，否则说明此时处于区间中，需要将tmp按位与到interval_prefix中。',
        quote_src='—— yiduobo 题解原文',
        idea=['某一位要为 0，就得把所有「这一位是 1」的数用与运算消掉',
              '一段连续区间与成 0，省下最后一次合并：m 个数只花 m−1 次',
              '`prefix` 里存「想消成 0」的位，操作不够就把这一位拿掉'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`interval_prefix` 一旦与成 0 就置 None，从下一个数重新开始',
                 '最后答案是 `((1 << length) - 1) ^ prefix`：没被消掉的位',
                 '原文为 Python 2 风格，本题代码无需改动，仅去掉空行',
                 '对比灵神：灵神用 mask 去掉不可消位，yiduobo 用 prefix 记可消位，最后取反'],
    ),
)

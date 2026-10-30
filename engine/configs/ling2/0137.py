NUMS = [5, 3, 5, 5]
BITS = 3

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _done(S):
    """已经完整“加进” a、b 的数的个数"""
    k = _k(S)
    if k is None:
        return len(NUMS) if 'x' in S else 0
    return k + 1 if S.get('_line') == 6 else k


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a, b, x = S.get('a'), S.get('b'), S.get('x')
    if a is None:
        cv.text((x0 + 18, y0 + 4), 'a、b 两个比特合起来表示每一位的「1 的个数 mod 3」', 24, T['muted'], bold=True)
        return
    k, done = _k(S), _done(S)
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), '按位看：(a, b) = 00 → 01 → 10 → 00 表示 0 → 1 → 2 → 0', 24, T['muted'], bold=True)
    hx, cw, rh = 330, 130, 54
    sx = x0 + (x1 - x0 - hx - cw * BITS) / 2
    y = y0 + 52
    for j in range(BITS):
        cv.text((sx + hx + j * cw + cw / 2, y), f'第 {BITS - 1 - j} 位', 22, T['muted'], anchor='mt', bold=True)
    y += 36
    seen = NUMS[:done]
    rows = []
    if x is not None and k is not None:
        rows.append((f'x = {x}', [x >> (BITS - 1 - j) & 1 for j in range(BITS)], T['blue'], False))
    rows.append((f'b = {b}' + ('（新）' if line in (5, 6) else ''), [b >> (BITS - 1 - j) & 1 for j in range(BITS)], T['green'], line == 5))
    rows.append((f'a = {a}' + ('（新）' if line == 6 else ''), [a >> (BITS - 1 - j) & 1 for j in range(BITS)], T['pink'], line == 6))
    rows.append(('2a + b（状态）', [2 * (a >> (BITS - 1 - j) & 1) + (b >> (BITS - 1 - j) & 1) for j in range(BITS)], T['yellow'], False))
    rows.append((f'前 {done} 个数中 1 的个数', [sum(v >> (BITS - 1 - j) & 1 for v in seen) for j in range(BITS)], T['muted'], False))
    cv.text((sx + hx + cw * BITS / 2, y + len(rows) * rh + 4), '每一位：状态 = 1 的个数 mod 3', 22, T['yellow'], anchor='mt')
    for r, (name, vals, c, hot) in enumerate(rows):
        Y = y + r * rh
        if hot:
            cv.rect((sx - 8, Y - 4, sx + hx + cw * BITS + 8, Y + rh - 8), fill=T['panel2'], r=8)
        cv.text((sx + hx - 16, Y + rh / 2 - 6), name, 24, c, anchor='rm', bold=True)
        for j, v in enumerate(vals):
            X = sx + hx + j * cw
            txt = str(v)
            if r == len(rows) - 1:
                cv.text((X + cw / 2, Y + rh / 2 - 6), txt, 30, T['muted'], anchor='mm', bold=True)
            else:
                cv.text((X + cw / 2, Y + rh / 2 - 6), txt, 30, c if (v or r == len(rows) - 2) else T['dim'], anchor='mm', bold=True)


def _cap_b(S, B, ret):
    head = f'`b = ({B.b:03b} ^ {S.x:03b}) & ~{S.a:03b}` = =={S.b:03b}=='
    if _k(S) == 0:
        return head + '：`b ^ x` 翻转，`& ~a` 让 ==a 为 1 的位 b 保持 0=='
    return head + '（先更新 b，下一行再用新 b 更新 a）'


def _cap_a(S, B, ret):
    k = _k(S)
    head = f'`a = ({B.a:03b} ^ {S.x:03b}) & ~{S.b:03b}` = =={S.a:03b}=='
    if k == 0:
        return head + '：用==新的 b==，b 为 1 的位 a 保持 0'
    moves = []
    for j in range(BITS - 1, -1, -1):
        if S.x >> j & 1:
            c0 = sum(v >> j & 1 for v in NUMS[:k]) % 3
            moves.append(f'第{j}位 {c0}→{(c0 + 1) % 3}' + ('（归零）' if c0 == 2 else ''))
    return head + '：' + '，'.join(moves)


CONFIG = dict(
    num=137, title='只出现一次的数字 II', difficulty='Medium', category='技巧',
    author='灵茶山艾府', technique='位运算 · 模 3 加法',
    tags=['面试经典150'],
    code='''
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        a = b = 0
        for x in nums:
            b = (b ^ x) & ~a
            a = (a ^ x) & ~b
        return b
''',
    setup=TRACK,
    call=f'Solution().singleNumber(TList({NUMS}))',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（暗 = 已加进 a、b）', cell=100, h=215,
             pointers={_k: 'blue'}, pointer_labels={_k: 'x'},
             dim=lambda S, i, v: i < _done(S)),
        dict(type='custom', draw=_draw, h=400),
    ],
    watch=[('x', 'x', 'blue'), ('b', 'b', 'green'), ('a', 'a', 'pink')],
    captions={
        'a = b = 0': '每一位的计数都从 0 开始：`(a, b) = (0, 0)`',
        'for x in nums': lambda S, B, ret: (f'把 `x = {S.x}`（二进制 `{S.x:03b}`）按位做==模 3 加法==' if _k(S) is not None
                                            else '所有数都加完了：出现 3 次的数在每一位上都模 3 归零'),
        'b = (b ^ x) & ~a': _cap_b,
        'a = (a ^ x) & ~b': _cap_a,
        'return b': '每一位模 3 后只剩 0 或 1，正好存在 b 里 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='用两个比特 a、b 让每一位做模 3 加法，出现三次的数自动归零',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `nums` 中，除某个元素只出现==一次==外，其余每个元素都恰好出现==三次==',
                 '找出只出现一次的元素；要求==线性时间、常数空间==',
                 '示例：`[2,2,3,2]` → `3`，`[0,1,0,1,0,1,99]` → `99`',
                 f'本视频：`{NUMS}` → `3`'],
        before=[dict(heading='暴力思路：统计每个比特位上 1 的个数', chapter='② 思路', lines=[
            '设答案为 `x`：若 `x` 的某位是 0，所有数在这一位上 1 的个数是 ==3 的倍数==',
            '若 `x` 的某位是 1，这一位上 1 的个数 ==除 3 余 1==',
            '所以每一位的 `cnt1 % 3` 就是答案这一位的值',
            '问题：能不能不统计个数，直接用位运算算出 `cnt1 % 3`？'])],
        quote='模 3 加法就是在 0,1,2 之间不断转换……由于 0,1,2 需要两个比特才能表示，设这两个比特分别为 a 和 b。',
        quote_src='—— 灵茶山艾府题解「位运算的魔法：模 3 加法」',
        idea=['`(a,b)`：`00` 表示 0，`01` 表示 1，`10` 表示 2，循环 `00 → 01 → 10 → 00`',
              '大部分转换是翻转，用异或；==两个例外用 `&` 加约束==：a 为 1 时 b 不变',
              '先算 b 再算 a：新 b 为 1 时 a 保持 0 → `a = (a ^ x) & ~b`',
              '位运算按位并行，所有比特一起做模 3 加法；最后结果在 b 里'],
        result='每一位都模 3：只剩 `3 = 011` → 返回 `3` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '更新顺序不能乱：==先 b 后 a==，a 的公式用的是新的 b',
                 '同时更新版：`a, b = (a ^ x) & (a | b), (b ^ x) & ~a`',
                 '暴力：逐位统计 `cnt1 % 3`，`O(n·32)`；负数要单独处理符号位',
                 '进阶：其余出现 5 次 → 用 3 个比特表示 0~4'],
    ),
)

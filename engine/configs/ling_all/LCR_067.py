NUMS = [3, 10, 5]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    W = max(nums).bit_length()
    i = S.get('i')
    mask = S.get('mask', 0)
    live = i is not None
    cv.text((x0 + 18, y0 + 4), '每个数的二进制（低于第 i 位的比特被 mask 置 0，画成灰点）', 22, T['muted'], bold=True)
    cell, rh = 54, 52
    lab = 120
    sx = x0 + 24 + lab
    top = y0 + 78
    for b in range(W):
        bit = W - 1 - b
        X = sx + b * cell
        hot = live and bit == i
        cv.text((X + cell / 2, top - 8), f'{bit}', 20, T['orange'] if hot else T['dim'], anchor='mb', mono=True, bold=hot)
    if live:
        X = sx + (W - 1 - i) * cell
        cv.rect((X, top - 2, X + cell, top + rh * len(nums) + 2), outline=T['orange'], width=3, r=6)
    x = S.get('x')
    raw = S.get('_line') == 9
    mx = (x if raw else x) if x is not None else None
    partner = None
    if live and S.get('_line') == 11 and x is not None and 'new_ans' in S:
        partner = S['new_ans'] ^ x
    for k, n in enumerate(nums):
        Y = top + k * rh
        v = n if (not live or raw or x is None) else n & mask
        cur = x is not None and ((n == x) if raw else ((n & mask) == x)) and live
        par = partner is not None and (n & mask) == partner
        if cur:
            cv.rect((x0 + 14, Y, x1 - 14, Y + rh - 4), outline=T['yellow'], width=3, r=8)
        elif par:
            cv.rect((x0 + 14, Y, x1 - 14, Y + rh - 4), outline=T['blue'], width=3, r=8)
        cv.text((x0 + 30, Y + (rh - 4) / 2), f'{n}', 26, T['text'], anchor='lm', bold=True)
        for b in range(W):
            bit = W - 1 - b
            X = sx + b * cell
            kept = (not live) or bit >= i
            ch = str((n >> bit) & 1) if kept else '·'
            col = (T['green'] if (n >> bit) & 1 else T['text']) if kept else T['dim']
            cv.text((X + cell / 2, Y + (rh - 4) / 2), ch, 30, col, anchor='mm', mono=True, bold=kept)
    y = top + rh * len(nums) + 16
    for name, val in (('mask', S.get('mask')), ('ans', S.get('ans')), ('new_ans', S.get('new_ans'))):
        if val is None:
            continue
        cv.text((x0 + 30, y), name, 24, T['muted'], anchor='lm', mono=True)
        for b in range(W):
            bit = W - 1 - b
            X = sx + b * cell
            one = (val >> bit) & 1
            cv.text((X + cell / 2, y), str(one), 30, T['yellow'] if (name == 'new_ans' and live and bit == i) else (T['green'] if one else T['dim']),
                    anchor='mm', mono=True, bold=bool(one))
        cv.text((sx + W * cell + 14, y), f'= {val}', 24, T['muted'], anchor='lm', mono=True)
        y += 44


def _b(v):
    return format(v, 'b')


def cap_ni(S, B, ret):
    return f'假设第 `{S.i}` 位能变成 1：`new_ans = ans | (1 << {S.i})` = `{_b(S.new_ans)}`（{S.new_ans}）。==要找两个数异或得到它=='


def cap_mask(S, B, ret):
    return f'`mask` 加上第 `{S.i}` 位 → `{_b(S.mask)}`：只看从最高位到第 `{S.i}` 位'


def cap_and(S, B, ret):
    return f'`x &= mask`：低于第 `{S.i}` 位清零，`{B.x}` → ==`{S.x}`=='


def cap_if(S, B, ret):
    t = S.new_ans ^ S.x
    if t in S.seen:
        return f'需要的另一个数 `new_ans ^ x = {S.new_ans} ^ {S.x} = {t}` ==已经在 seen 里==：这两个数异或能得到 `new_ans`'
    return f'需要的另一个数 `new_ans ^ x = {S.new_ans} ^ {S.x} = {t}`，seen 里没有 → 先把 `{S.x}` 记下'


CONFIG = dict(
    num='LCR 067', title='数组中两个数的最大异或值', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='从高位到低位试填 + 哈希表（两数之和）',
    code='''
class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        ans = mask = 0
        high_bit = max(nums).bit_length() - 1
        for i in range(high_bit, -1, -1):  # 从最高位开始枚举
            mask |= 1 << i
            new_ans = ans | (1 << i)  # 这个比特位可以是 1 吗？
            seen = set()
            for x in nums:
                x &= mask  # 低于 i 的比特位置为 0
                if new_ans ^ x in seen:
                    ans = new_ans  # 这个比特位可以是 1
                    break
                seen.add(x)
        return ans
''',
    call=f'Solution().findMaximumXOR({NUMS})',
    expect=15,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='set', var='seen', label='seen（已见过的 x & mask）', fmt=lambda x: f'{x}', h=150),
    ],
    watch=[('i', 'i', 'orange'), ('x', 'x', 'yellow'), ('ans', 'ans', 'green'), ('new_ans', 'new_ans')],
    captions={
        'ans = mask = 0': '`ans` 从 0 开始，一位一位地往上添 1；`mask` 是「当前要看的高位」',
        'high_bit =': lambda S, B, r: f'最大数 `{max(S.nums)}` 的二进制有 {max(S.nums).bit_length()} 位 → 最高位是第 `{S.high_bit}` 位',
        'for i in range': lambda S, B, r: ('==从最高位往低位==：现在处理第 `{}` 位（高位对「最大」更重要）'.format(S.i)
                                           if B.get('i') != S.i else '第 `0` 位也试完了 → 循环结束'),
        'mask |= 1 << i': cap_mask,
        'new_ans = ans | (1 << i)': cap_ni,
        'seen = set()': '新建哈希表：和「两数之和」一样，一边遍历一边查',
        'for x in nums': lambda S, B, r: (f'取下一个数 `x = {S.x}`' if not (B.get('x') == S.x and B.get('_line') != 8)
                                          else '所有数都看过了，这一位无法是 1：`ans` 保持不变'),
        'x &= mask': cap_and,
        'if new_ans ^ x in seen': cap_if,
        'ans = new_ans': '找到了！第 `{i}` 位可以是 1：`ans` 继承后得到 ==`{ans}`==（`{ans:b}`）',
        'break': '这一位已经确定，不用再看别的数，进入下一位',
        'seen.add(x)': '记下 `{x}`，供后面的数来配对',
        'return ans': '从高到低每一位都试过了：最大异或值 ==`{ans}`==（`{ans:b}`）',
    },
    max_steps=110,
    cards=dict(
        one_liner='从最高位开始，逐位试：这一位能不能是 1？',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['数组 `nums`，求 `nums[i] XOR nums[j]` 的最大值',
                 '示例：`[3,10,5,25,2,8]` → `28`（`5 XOR 25`）',
                 '本视频：`[3,10,5]` → `15`（`5 XOR 10`）',
],
        quote='请注意，ans 继承了上一位算出的内容，后面比特位的计算不是只看当前位，之前算过的高位也得满足。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案想最大：==高位优先==，能让高位是 1 就一定要',
              '试探 `new_ans = ans + 2^i`：是否存在两个数异或等于它（低于 `i` 的位当作 0）',
              '`a ^ b = new_ans` ⇔ `a = new_ans ^ b`：用哈希表，像两数之和一样一遍扫'],
        summary=['时间 `O(n log U)`，空间 `O(n)`',
                 '易错：必须从最高位开始，从低位开始高位可能只能是 0',
                 '易错：`ans` 继承高位结果，所以 `new_ans` 是在 `ans` 上加一位，不是只看当前位',
                 '`x &= mask` 把低位清零，只比较当前已确定的前缀'],
    ),
)

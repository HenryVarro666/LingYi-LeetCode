NUMS = [5, 2, 3, 6]


def _sim(nums, mask):
    """按代码逻辑模拟一遍：每个数合并后 (and_res, 是否计一次操作)"""
    out = []
    ar = -1
    for x in nums:
        ar &= x & mask
        if ar:
            out.append((ar, True))
        else:
            out.append((0, False))
            ar = -1
    return out


def _cur(S):
    """当前正在处理 nums 的哪个下标（None = 不在遍历中）"""
    if 'x' not in S or 'cnt' not in S or 'mask' not in S:
        return None
    ln = S.get('_line')
    if ln in (LN_MASK, LN_CNT, LN_AND0, LN_FOR_B):
        return None
    return S['nums'].index(S['x']) if S['x'] in S['nums'] else None


LN_FOR_B, LN_MASK, LN_CNT, LN_AND0 = 4, 5, 6, 7


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    W = max(nums).bit_length()
    mask = S.get('mask', 0)
    b = S.get('b', -1)
    ans = S.get('ans', 0)
    cur = _cur(S)
    sim = _sim(nums, mask) if 'mask' in S else None
    cell = 64
    colx = lambda j: x0 + 190 + (W - 1 - j) * cell          # 第 j 位的列
    rx = colx(-1) + 70                                       # 右侧结果列
    cv.text((x0 + 18, y0 + 4), '二进制视图：亮 = 当前 mask 看的位，暗 = 已确定 / 暂不看的位', 22, T['muted'], bold=True)
    # 列头
    yh = y0 + 52
    for j in range(W - 1, -1, -1):
        c = T['yellow'] if j == b else T['dim']
        cv.text((colx(j) + cell / 2, yh), f'2^{j}', 22, c, anchor='mm', bold=True, mono=True)
    cv.text((rx + 10, yh), '合并结果', 22, T['dim'], anchor='lm', bold=True)
    # ans 行
    ya = yh + 34
    cv.text((x0 + 20, ya + 26), 'ans（已定的 1）', 19, T['green'], anchor='lm', bold=True)
    for j in range(W - 1, -1, -1):
        on = (ans >> j) & 1
        cv.rect((colx(j) + 4, ya, colx(j) + cell - 4, ya + 52), fill=T['green'] if on else T['panel2'], r=8, outline=T['border'])
        cv.text((colx(j) + cell / 2, ya + 26), on, 28, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
    # mask 行
    ym = ya + 64
    cv.text((x0 + 20, ym + 26), 'mask（看哪些位）', 20, T['cyan'], anchor='lm', bold=True)
    for j in range(W - 1, -1, -1):
        on = (mask >> j) & 1
        cv.rect((colx(j) + 4, ym, colx(j) + cell - 4, ym + 52), fill=T['cyan'] if on else T['panel2'], r=8, outline=T['border'])
        cv.text((colx(j) + cell / 2, ym + 26), on, 28, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
    cv.line([(x0 + 14, ym + 66), (x1 - 14, ym + 66)], T['border'], 2)
    # 数字行
    yr = ym + 82
    rh = 66
    for i, v in enumerate(nums):
        Y = yr + i * rh
        is_cur = (cur == i)
        if is_cur:
            cv.rect((x0 + 8, Y - 2, x1 - 8, Y + 56), outline=T['pink'], width=4, r=10)
        cv.text((x0 + 20, Y + 27), f'nums[{i}] = {v}', 24, T['text'] if (cur is None or i <= cur) else T['muted'], anchor='lm', bold=True, mono=True)
        for j in range(W - 1, -1, -1):
            bit = (v >> j) & 1
            seen = (mask >> j) & 1
            if bit and seen:
                fill, tc = T['orange'], T['bg']
            elif bit:
                fill, tc = (60, 66, 76), T['dim']
            else:
                fill, tc = T['panel2'], T['dim']
            cv.rect((colx(j) + 4, Y, colx(j) + cell - 4, Y + 54), fill=fill, r=8)
            cv.text((colx(j) + cell / 2, Y + 27), bit, 28, tc, anchor='mm', bold=True, mono=True)
        # 合并结果
        shown = sim is not None and cur is not None and (i < cur or (i == cur and S.get('_line', 0) >= LN_AND_UPD))
        if shown:
            ar, counted = sim[i]
            txt = f'{ar:0{W}b}'
            cv.text((rx + 10, Y + 27), 'and=' + txt, 22, T['text'], anchor='lm', bold=True, mono=True)
            if counted:
                cv.text((rx + 150, Y + 27), '+1 次', 24, T['pink'], anchor='lm', bold=True)
            else:
                cv.text((rx + 150, Y + 27), '清零！换下一段', 22, T['green'], anchor='lm', bold=True)
    yb = yr + len(nums) * rh + 8
    if 'cnt' in S and 'k' in S:
        ok = S['cnt'] <= S['k']
        cv.text((x0 + 20, yb + 8), f"本轮操作次数 cnt = {S['cnt']}   k = {S['k']}", 26, T['green'] if ok else T['red'], bold=True)


LN_AND_UPD = 9


def _bit_txt(S):
    if 'b' not in S:
        return '从高位到低位，逐位问：答案的这一位能不能是 0？'
    return f"正在问：答案第 {S['b']} 位能不能是 0？  当前 mask = {S['mask']:b}"


CONFIG = dict(
    num=3022, title='给定操作次数内使剩余元素的或值最小', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='试填法 · 从高到低逐位合并',
    tags=['灵神题单·位运算', '难度分 2918'],
    code='''
class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        ans = mask = 0
        for b in range(max(nums).bit_length() - 1, -1, -1):
            mask |= 1 << b
            cnt = 0  # 操作次数
            and_res = -1  # -1 的二进制全为 1
            for x in nums:
                and_res &= x & mask
                if and_res:
                    cnt += 1  # 合并 x，操作次数加一
                else:
                    and_res = -1  # 准备合并下一段
            if cnt > k:
                ans |= 1 << b  # 答案的这个比特位必须是 1
                mask ^= 1 << b  # 后面不考虑这个比特位
        return ans
''',
    call='Solution().minOrAfterOperations([5,2,3,6], 2)',
    expect=2,
    views=[
        dict(type='text', fn=_bit_txt, size=28, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    skip=[8],
    watch=[('b', 'b', 'yellow'), ('mask', 'mask', 'cyan'), 'cnt', ('and_res', 'and_res', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = mask = 0': '`ans` 存答案，`mask` 存「这一轮要看的位」，都从 0 开始',
        'for b in range': lambda S, B, r: ('所有位都试完了，退出循环' if 'b' in B and B.b == S.b else f'==从最高位往低位试填==：这一位（第 `{S.b}` 位）能不能让答案取 0？'),
        'mask |= 1 << b': '把第 `{b}` 位加入 mask：只看 `mask = {mask:b}` 里的位，其余位先忽略',
        'cnt = 0': '统计「把 mask 内的 1 全部消掉」至少要几次操作',
        7: '`-1` 二进制全是 1，当作「还没合并任何数」的初始值',
        'and_res &= x & mask': '`and_res = {B.and_res} & ({x} & mask)` = =={and_res}==：把 `{x}` 并进当前这一段',
        'if and_res': lambda S, B, r: (f'`and_res = {S.and_res}` 不为 0 → 这段还有 1 没消掉，要再多合并一个数（多花一次操作）'
                                       if S.and_res else '`and_res = 0` → 这一段已经合并成 0，不用再花操作'),
        'cnt += 1': '合并 `{x}` 花一次操作：`cnt` → =={cnt}==',
        13: '这一段合并成 0 了，重置为 -1，从下一个数开始新的一段',
        'if cnt > k': lambda S, B, r: (f'`cnt = {S.cnt} > k = {S.k}`：做不到把这一位消成 0 → 答案这位必须是 1'
                                        if S.cnt > S.k else f'`cnt = {S.cnt} ≤ k = {S.k}`：操作次数够 → 这一位可以是 0'),
        'ans |= 1 << b': '答案第 `{b}` 位填 1：`ans` = =={ans:b}==',
        'mask ^= 1 << b': '这一位已经认定为 1，从 mask 里去掉：后面的位不必再管它',
        'return ans': '所有位试完，最小或值 = ==`{ans}`==（二进制 `{ans:b}`）',
    },
    cards=dict(
        one_liner='从高位到低位试填：这一位能不能消成 0？',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['一次操作：把相邻的 `nums[i]`、`nums[i+1]` 换成它们的按位与',
                 '至多 `k` 次操作，让剩下所有数的按位或最小',
                 '示例：`[5,2,3,6]`，`k = 2` → `2`（演示用，作者文中的例子）'],
        quote='多次操作，相当于把一段连续子数组合并成 0。尝试从左到右合并（忽略低位和必须是 1 的位），如果合并出 0，就开始合并下一段。',
        quote_src='—— 灵茶山艾府题解提示 2',
        idea=['答案某一位要为 0，所有数这一位都得被「与」消掉 → 从高到低逐位试',
              '多次操作 = 把连续一段合并；合并出 0 就开新的一段，每个数最多花一次操作',
              '总操作 `cnt ≤ k` → 这一位填 0；否则填 1，并从 mask 里去掉'],
        summary=['时间 `O(n log U)`：每一位扫一遍数组',
                 '`and_res = -1` 表示全 1；合并成 0 就清回 -1，开始下一段',
                 '易错点：已确定为 1 的位要从 mask 去掉（`mask ^= 1 << b`），后面不能再要求它是 0',
                 '整个数组都合并不成 0 时 `cnt` 会等于 n，题目保证 n > k，无需特判'],
    ),
)

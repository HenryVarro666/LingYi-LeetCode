NUMS = [1, 1, 2, 2, 3, 3]
N = len(NUMS)
SIDE = sum(NUMS) // 4


def _stat(S):
    return S.get('now_stat')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st = _stat(S)
    cv.text((x0 + 18, y0 + 4), f'火柴（绿 = now_stat 里已用的；二进制第 i 位 = 第 i 根）', 24, T['muted'], bold=True)
    unit = 46
    for i, v in enumerate(NUMS):
        Y = y0 + 48 + i * 40
        used = st is not None and st >> i & 1
        trying = S.get('index') == i and S.get('_line') in (30, 31) and st is not None and not used
        c = T['green'] if used else (T['yellow'] if trying else T['panel2'])
        cv.text((x0 + 40, Y + 14), f'{i}', 20, T['dim'], anchor='mm', mono=True)
        cv.rect((x0 + 60, Y, x0 + 60 + v * unit, Y + 28), fill=c, r=6, outline=T['border'])
        cv.text((x0 + 70 + v * unit, Y + 14), str(v), 20, T['text'], anchor='lm', bold=True)
    if st is not None:
        cv.text((x0 + 40, y0 + 48 + N * 40 + 10), f'now_stat = {st} = 0b{st:0{N}b}（从右往左是第 0..{N - 1} 根）', 22, T['code'], mono=True)
    # 正方形：已完成的边 + 正在拼的边
    cx, cy, L = x0 + 690, y0 + 70, 240
    cv.text((cx - 20, y0 + 4), f'正方形（边长 target_len = {SIDE}）', 24, T['muted'], bold=True)
    used_len = sum(v for i, v in enumerate(NUMS) if st is not None and st >> i & 1)
    full, part = divmod(used_len, SIDE)
    sides = [((cx, cy), (cx + L, cy)), ((cx + L, cy), (cx + L, cy + L)),
             ((cx + L, cy + L), (cx, cy + L)), ((cx, cy + L), (cx, cy))]
    for k, (p0, p1) in enumerate(sides):
        cv.line([p0, p1], T['border'], 6)
        frac = 1 if k < full else (part / SIDE if k == full else 0)
        if frac > 0:
            q = (p0[0] + (p1[0] - p0[0]) * frac, p0[1] + (p1[1] - p0[1]) * frac)
            cv.line([p0, q], T['green'] if frac == 1 else T['yellow'], 10)
    cv.text((cx + L / 2, cy + L + 30), f'已拼好 {min(full, 4)} 条边，当前边 {part}/{SIDE}', 22, T['text'], anchor='mt', bold=True)


def _memo(S):
    f = S.get('f')
    if not isinstance(f, list):
        return None
    return {f'{k:0{N}b}': v for k, v in enumerate(f) if v is not None}


def _cap_fit(S, B, ret):
    i, st, t = S.index, S.now_stat, S.target_len
    cur = S.sum_now % t
    if NUMS[i] + cur <= t:
        return f'当前边已拼 `{S.sum_now} % {t} = {cur}`，第 {i} 根：`{NUMS[i]} + {cur} ≤ {t}` → 放得下'
    return f'第 {i} 根：`{NUMS[i]} + {cur} > {t}` → ==放不下=='


def _cap_enter(S, B, ret):
    return f'选第 `{B.index}` 根，递归到新状态 `0b{B.now_stat + (1 << B.index):0{N}b}`（`f` 里没记过）'


def _cap_loop(S, B, ret):
    u = sorted(S.unused_set)
    if B.index == S.index and S.index == u[-1] and len(u) > 1:
        return '没用过的火柴都试完了，没有一根能成功'
    if S.index == u[0]:
        return (f'逐位检查 now_stat：已用总长 `sum_now = {S.sum_now}`，没用过的 `unused_set = {u}`；'
                f'先试 `index = {S.index}`')
    return f'换下一根：`index = {S.index}`'


CONFIG = dict(
    num=473, title='火柴拼正方形', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状态压缩 · 记忆化搜索',
    tags=['字节30天'],
    code='''
class Solution(object):
    def makesquare(self, nums):
        if not nums:
            return False

        sum_len = sum(nums)
        if sum_len % 4 != 0:
            return False

        f = [None] * (1 << len(nums))

        return self.dfs(0, nums, sum_len // 4, f)

    def dfs(self, now_stat, nums, target_len, f):
        if f[now_stat] is not None:
            return f[now_stat]
        if now_stat + 1 == 1 << len(nums):
            f[now_stat] = True
            return f[now_stat]

        sum_now = 0
        unused_set = set()
        for index, num in enumerate(nums):
            if now_stat & (1 << index):
                sum_now += num
            else:
                unused_set.add(index)

        for index in unused_set:
            if nums[index] + sum_now % target_len <= target_len:
                if self.dfs(now_stat + (1 << index), nums, target_len, f):
                    f[now_stat] = True
                    return True

        f[now_stat] = False
        return False
''',
    call=f'Solution().makesquare({NUMS})',
    expect=True,
    skip=['for index, num in enumerate', 'if now_stat & (1 << index)', 'sum_now += num', 'else:', 'unused_set.add', 'sum_now = 0',
          'unused_set = set()', 'if not nums', 15, 17, 'return True'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='map', var=_memo, label='f（只列出已算过的状态：二进制 → 能否拼成）', h=110, font=22),
        dict(type='calls', h=150, hide=('nums', 'f', 'target_len')),
    ],
    watch=[('now_stat', 'now_stat'), ('sum_now', 'sum_now'), ('unused_set', 'unused_set'), ('index', 'index', 'yellow')],
    max_steps=60,
    captions={
        'sum_len = sum(nums)': '火柴总长 `sum_len = {sum_len}`',
        'if sum_len % 4 != 0': '`{sum_len}` 是 4 的倍数，边长 `target_len = {sum_len} // 4 = {sum_len // 4}`',
        'f = [None] * (1 << len(nums))': '`f[状态]`：用过的火柴集合是这个状态时，剩下的能否拼完；`None` = 还没算（共 `2^{len(nums)}` 个状态）',
        'return self.dfs(0': '从「一根都没用」的状态 `0` 开始搜索',
        'if f[now_stat] is not None': lambda S, B, r: (f'状态 `0b{S.now_stat:0{N}b}` 算过了 → 直接返回'
                                                       if S.f[S.now_stat] is not None else
                                                       f'进入状态 `0b{S.now_stat:0{N}b}`：没算过，继续'),
        'if now_stat + 1 == 1 << len(nums)': lambda S, B, r: ('`now_stat + 1 == 2^n`：==所有火柴都用上了== → 成功'
                                                              if S.now_stat + 1 == 1 << N else '还有火柴没用'),
        16: '直接返回记忆的结果 `{ret}`，不用重新搜索',
        18: '`now_stat + 1 == 2^n`：==所有火柴都用上了==，四条边都拼满 → `f[0b{now_stat:06b}] = True`',
        19: '返回 `True`',
        32: '子状态成功 → `f[0b{now_stat:06b}] = True`',
        'for index in unused_set': _cap_loop,
        'if nums[index] + sum_now % target_len': _cap_fit,
        'if self.dfs(': _cap_enter,
        'return True': '返回 True，一层层往上传',
        'f[now_stat] = False': '所有选择都失败 → 记下 `f[0b{now_stat:06b}] = False`，==以后再遇到直接返回==',
        'return False': '返回 False，==回溯==到上一层换一根试',
    },
    cards=dict(
        one_liner='用二进制记下哪些火柴用过了；当前边长 = 已用总长 % 边长，记忆化搜索',
        complexity='时间 `O(n · 2^n)`，空间 `O(2^n)`',
        problem=['`matchsticks[i]` 是第 `i` 根火柴的长度，==每根都要用且只能用一次==，不能折断',
                 '问能否拼成一个正方形；`1 <= n <= 15`',
                 '示例：`[1,1,2,2,2]` → `true`；`[3,3,3,3,4]` → `false`',
                 '本视频：`[1,1,2,2,3,3]`，边长 3 → `true`'],
        quote='获取到目前拿了哪些火柴之后，可以将这些火柴的长度相加，然后==对target_len取模==，就可以得到当前正在拼的这条边目前拼好的长度l。接下来枚举没有使用过的火柴，若其长度加上l小于等于target_len，那么就尝试选择这根火柴。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 15` → 用一个整数的二进制位表示每根火柴==用没用过==（状态压缩）',
              '已用总长 `% target_len` 就是正在拼的那条边的长度，不用单独记边',
              '`f[状态]` 记忆化：同一个火柴集合不管什么顺序选出来，结果都一样'],
        result='所有火柴都用上了：返回 `True`',
        summary=['时间 `O(n · 2^n)`：`2^n` 个状态，每个状态枚举 `n` 根火柴；空间 `O(2^n)`',
                 '易错：总长不是 4 的倍数直接 `False`',
                 '关键：只在「放得下」时才往下搜，所以每条边都恰好拼满',
                 '原文为 Python 2 写法：`sum_len / 4` 已改为 `sum_len // 4`，并删去了文档字符串'],
    ),
)

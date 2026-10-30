NUM = '4321'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    num = NUM
    n = len(num)
    pl = S.get('pos_list')
    ni = S.get('num_index') or [0] * 10
    now = S.get('now_pos') or 1
    res = S.get('res')
    if not isinstance(res, list):
        res = []
    if pl is None:
        return
    sp = S.get('swap_pos') if S.get('swap_num') is not None else None
    used = set()
    for d in range(10):
        used.update(pl[d][:ni[d]])
    cell = min(100, (x1 - x0 - 40) / (2 * n))
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * 2 * n) / 2
    ys = y0 + 90
    ch = cell * 0.82
    cv.text((x0 + 18, y0 + 4), '2n 个格子：前 n 格放结果，原数字从第 n+1 格开始排队', 22, T['muted'], bold=True)
    for p in range(1, 2 * n + 1):
        X = sx + (p - 1) * cell
        txt, fill, tc = '_', T['panel2'], T['dim']
        if p <= n:
            if p < now:
                txt, fill, tc = res[p - 1], T['green'], T['bg']
        else:
            i = p - n - 1
            if p in used:
                txt, fill, tc = '', (46, 52, 62), T['dim']
            else:
                txt, fill, tc = num[i], T['blue'], T['bg']
        if p == sp:
            fill, tc = T['pink'], T['bg']
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), txt, 36, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 10), p, 18, T['dim'], anchor='mt', mono=True)
    if now <= n:
        X = sx + (now - 1) * cell + cell / 2
        cv.tri_up(X, ys + ch + 40, 10, T['yellow'])
        cv.text((X, ys + ch + 54), f'now_pos={now}', 20, T['yellow'], anchor='mt', bold=True)
    if sp is not None and sp > n:
        X = sx + (sp - 1) * cell + cell / 2
        cv.tri_up(X, ys + ch + 40, 10, T['pink'])
        cv.text((X, ys + ch + 54 + (26 if sp == now else 0)), f'swap_pos={sp}', 20, T['pink'], anchor='mt', bold=True)
    cv.text((x0 + 20, ys + ch + 120),
            f"剩余步数 k = {S.get('k')}　　绿 = 已确定的高位　蓝 = 还没用的数字　粉 = 本轮候选", 22, T['text'])


def _cap_step(S, B, ret):
    d, k = S.swap_num, S.k
    cost = S.step
    if cost <= k:
        return f'移动数字 `{d}` 要跨过 `{cost}` 个数字：`{cost} <= k = {k}` → ==换得起=='
    return f'移动数字 `{d}` 要跨过 `{cost}` 个数字：`{cost} > k = {k}` → ==换不起==，试更大的数字'


CONFIG = dict(
    num=1505, title='最多K次交换相邻数位后得到的最小整数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='贪心 · 树状数组数前面还剩几个数',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution(object):
    def minInteger(self, num, k):

        n = len(num)
        pos_list = [[] for _ in range(10)]
        suffix_array = [0] * (n + n + 1)
        for index, char in enumerate(num):
            pos_list[int(char)].append(index + n + 1)
            self.add(index + n + 1, n + n, suffix_array, 1)

        n = len(num)
        num_index = [0] * 10
        now_pos = 1
        res = []
        while now_pos <= n:
            for swap_num in range(10):
                if num_index[swap_num] < len(pos_list[swap_num]):
                    swap_pos = pos_list[swap_num][num_index[swap_num]]
                    step = self.sum(swap_pos - 1, suffix_array) - now_pos + 1
                    if step <= k:
                        res.append(str(swap_num))
                        k -= step
                        self.add(now_pos, n + n, suffix_array, 1)
                        self.add(swap_pos, n + n, suffix_array, -1)
                        num_index[swap_num] += 1
                        break

            now_pos += 1

        return ''.join(res)
    
    def add(self, now, max_n, suffix_array, delta):
        while now <= max_n:
            suffix_array[now] += delta
            now += now & -now
        
    def sum(self, now, suffix_array):
        res = 0
        while now:
            res += suffix_array[now]
            now -= now & -now
        
        return res
''',
    call=f'Solution().minInteger({NUM!r}, 4)',
    expect='1342',
    skip=['suffix_array[now] += delta', 'now += now & -now', 'res += suffix_array[now]', 'now -= now & -now',
          'while now <=', 'while now:', 'return res', 'res = 0', 'pos_list[int(char)].append', 'for index, char', 'for swap_num in range',
          'if num_index[swap_num] <'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='suffix_array', label='suffix_array（树状数组：数每个位置之前还剩几个数）', h=200, cell=60,
             index=True),
    ],
    watch=[('now_pos', 'now_pos', 'yellow'), ('swap_num', 'swap_num', 'pink'), ('step', 'step', 'orange'),
           ('k', 'k', 'blue'), ('res', "''.join(res)", 'green')],
    captions={
        4: '`n = {n}`：先把原数字整体后移 n 格，前 n 格留给答案',
        11: '`n = {n}`',
        'pos_list = [[]': '`pos_list[d]`：数字 `d` 在排队序列里的所有位置（从小到大）',
        'res = []': '`res` 存放最终答案的每一位',
        'break': '这一位定下来了，不再试更大的数字',
        'suffix_array = [0]': '`suffix_array` 是树状数组，下标 1..2n',
        'self.add(index + n + 1': '把数字 `{char}` 放到第 `{index + n + 1}` 格，树状数组该位置 `+1`',
        'num_index = [0] * 10': '`num_index[d]`：数字 `d` 已经用掉几个（同一数字永远先用靠前的）',
        'now_pos = 1': '`now_pos`：当前要确定答案的第几位',
        'while now_pos <= n': lambda S, B, r: (f'`now_pos = {S.now_pos}`：要为第 `{S.now_pos}` 位挑一个数字' if S.now_pos <= S.n else f'`now_pos = {S.now_pos} > n`：每一位都定好了 → 结束'),
        'swap_pos = pos_list': '数字 `{swap_num}` 最靠前的那个在第 `{swap_pos}` 格',
        'step = self.sum': '用树状数组数第 `{swap_pos-1}` 格之前还剩几个数，再减去前面已确定的 `{now_pos-1}` 格 → ==代价 = 它前面还没用的数字个数==',
        'if step <= k': _cap_step,
        'res.append(str(swap_num))': '数字 `{swap_num}` 放到答案第 `{now_pos}` 位：`res = {res}`',
        'k -= step': '花掉 `{step}` 次交换：`k = {B.k} - {step} = {k}`',
        'self.add(now_pos': '第 `{now_pos}` 格被填上：`+1`',
        'self.add(swap_pos': '原来的第 `{swap_pos}` 格被取走：`-1`',
        'num_index[swap_num] += 1': '`{swap_num}` 的下一个候选后移',
        'now_pos += 1': '处理下一位：`now_pos` → {now_pos}',
        "return ''.join": '拼起来：==`{ret}`==',
    },
    max_steps=80,
    cards=dict(
        one_liner='从高位开始，把换得起的最小数字挪到当前位',
        complexity='时间 `O(10·n·log n)`，空间 `O(n)`',
        problem=['给你数字串 `num` 和整数 `k`，每次可以交换==相邻==两位',
                 '最多交换 `k` 次，求能得到的==最小整数==（返回字符串）',
                 '本视频：`num = "4321"`，`k = 4` → `"1342"`'],
        quote='从高位开始向后逐位处理，每次将可以交换到这个位置上的最小的数交换过来。……存在两个相同的最小数都可以交换，此时应该将最靠前……的那个交换到最高位上。',
        quote_src='—— yiduobo 题解原文',
        idea=['小数要尽量换到高位，但每换一格要花 1 次交换：代价 = 要跨过的数字个数',
              '逐位枚举 `0~9`，第一个 `代价 <= k` 的就是这一位的答案；相同数字取最靠前的',
              '把原数字整体后移 n 格，“移到最前”就不会错位；用树状数组数中间还剩几个数'],
        summary=['时间 `O(10·n·log n)`，空间 `O(n)`',
                 '易错：代价是跨过的==剩余==数字个数，已经取走的不再算（树状数组里要 `-1`）',
                 '易错：同一数字永远先取最靠前的那个，这样花的步数最少',
                 '每一位至少有一个数字代价为 0（最靠前的剩余数字），所以不会卡死',
                 '同类题：重排队、逆序对类的树状数组计数'],
    ),
)

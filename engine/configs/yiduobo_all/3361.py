S0, T0 = 'leet', 'coee'
NC = [1 + j % 3 for j in range(26)]
PC = [1 + (j + 1) % 2 for j in range(26)]


def _idx(S):
    """当前处理的是第几对 (s[i], t[i])：这个例子里每一对都不同，用 (sc, tc) 反查"""
    if 'sc' not in S or 'tc' not in S:
        return None
    for i, (a, b) in enumerate(zip(S['s'], S['t'])):
        if a == S['sc'] and b == S['tc']:
            return i
    return None


def _live(S):
    """index_s / index_t 已经是当前这一对的值，并且正在算代价（第 19～36 行）"""
    return 'index_t' in S and 19 <= S['_line'] <= 36 and S['sc'] != S['tc']


def _case(S):
    return S['index_s'] < S['index_t']


def _terms(S):
    """返回 (next 数组的 加项, 减项, prev 数组的 加项, 减项)，下标集合，和代码里 if 的分支一一对应"""
    s, t = S['index_s'], S['index_t']
    ln = S['_line']
    npl, nmi, ppl, pmi = set(), set(), set(), set()
    if s < t:
        if ln >= 20:
            npl.add(t - 1)
        if ln >= 22 and s > 0:
            nmi.add(s - 1)
        if ln >= 24:
            ppl.add(0)
            pmi.add(s + 1)
        if ln >= 26 and t < 25:
            ppl.add(t + 1)
    else:
        if ln >= 28:
            npl.add(25)
            nmi.add(s - 1)
        if ln >= 30 and t > 0:
            npl.add(t - 1)
        if ln >= 32:
            ppl.add(t + 1)
        if ln >= 34 and s < 25:
            pmi.add(s + 1)
    return npl, nmi, ppl, pmi


def _ncolor(S, i, v):
    if not _live(S):
        return None
    npl, nmi, _, _ = _terms(S)
    return 'green' if i in npl else ('pink' if i in nmi else None)


def _pcolor(S, i, v):
    if not _live(S):
        return None
    _, _, ppl, pmi = _terms(S)
    return 'green' if i in ppl else ('pink' if i in pmi else None)


def _text(S, B):
    if not _live(S):
        if 'sc' in S and S['_line'] in (14, 15, 16):
            return f"`sc = '{S['sc']}'`，`tc = '{S['tc']}'`：" + ('==相同，不用切换，代价 0==' if S['sc'] == S['tc'] else '不同，要算向后 / 向前哪个更省')
        return '`next_s[i]` = nextCost 的==前缀和==；`prev_s[i]` = previousCost 的==后缀和==。区间和 = 两个前缀（后缀）和相减'
    s, t = S['index_s'], S['index_t']
    if s < t:
        return (f'`{s} < {t}`：向后直接走 `[{s}, {t - 1}]`；向前要==绕圈==：`prev[{s}..0]` + `prev[25..{t + 1}]`')
    return (f'`{s} > {t}`：向前直接走 `[{t + 1}, {s}]`；向后要==绕圈==：`next[{s}..25]` + `next[0..{t - 1}]`')


CONFIG = dict(
    num=3361, title='两个字符串的切换距离', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 后缀和 · 分情况讨论',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def shiftDistance(self, s, t, nextCost, previousCost):
        
        next_s = [nextCost[0]]
        for v in nextCost[1:]:
            next_s.append(next_s[-1] + v)
        
        prev_s = [previousCost[-1]]
        for v in previousCost[-2::-1]:
            prev_s.append(prev_s[-1] + v)
        prev_s.reverse()

        res = 0
        for sc, tc in zip(s, t):
            if sc == tc:
                continue
            index_s = ord(sc) - 97
            index_t = ord(tc) - 97
            if index_s < index_t:
                next_cost = next_s[index_t - 1]
                if index_s > 0:
                    next_cost -= next_s[index_s - 1]

                prev_cost = prev_s[0] - prev_s[index_s + 1]
                if index_t  < 25:
                    prev_cost += prev_s[index_t + 1]
            else:
                next_cost = next_s[-1] - next_s[index_s - 1]
                if index_t > 0:
                    next_cost += next_s[index_t - 1]

                prev_cost = prev_s[index_t + 1]
                if index_s < 25:
                    prev_cost -= prev_s[index_s + 1]

            res += min(next_cost, prev_cost)
        
        return res
''',
    setup=f'NC = {NC}\nPC = {PC}',
    call=f'Solution().shiftDistance({S0!r}, {T0!r}, NC, PC)',
    expect=54,
    skip=['next_s.append', 'prev_s.append', 'for v in nextCost', 'for v in previousCost'],
    views=[
        dict(type='text', fn=_text, h=95, size=24),
        dict(type='string', var='s', label='s（蓝 = 当前这一位）', cell=60, index=False,
             color=lambda S, k, v: 'blue' if k == _idx(S) else None, h=100),
        dict(type='string', var='t', label='t（粉 = 目标字母）', cell=60, index=False,
             color=lambda S, k, v: 'pink' if k == _idx(S) else None, h=100),
        dict(type='array', var='next_s', label='next_s：nextCost 的前缀和（绿 = 加，粉 = 减）', cell=36,
             color=_ncolor, h=130),
        dict(type='array', var='prev_s', label='prev_s：previousCost 的后缀和（绿 = 加，粉 = 减）', cell=36,
             color=_pcolor, h=130),
    ],
    watch=[('index_s', 'index_s', 'blue'), ('index_t', 'index_t', 'pink'),
           ('next_cost', 'next_cost', 'green'), ('prev_cost', 'prev_cost', 'orange'), ('res', 'res', 'yellow')],
    captions={
        'next_s = [': '`next_s` 记 nextCost 的==前缀和==：`next_s[i] = nextCost[0] + … + nextCost[i]`，先放第一项，后面的循环逐项累加 `next_s[-1] + v`（25 次，这里一步带过）',
        'prev_s = [': '`prev_s` 记 previousCost 的==后缀和==，从最后一项倒着累加，先放最后一项，后面的循环同样累加 25 次（一步带过）',
        'prev_s.reverse()': '倒着累加出来的要翻回来：`prev_s[i] = previousCost[i] + … + previousCost[25]`',
        'res = 0': '`res` 累计每一位的最小代价（各位互相独立）',
        'for sc, tc in zip': lambda S, B, r: (f"第 {_idx(S)} 对：`s[{_idx(S)}] = '{S.sc}'` 要变成 `t[{_idx(S)}] = '{S.tc}'`" if 'sc' in S and 'sc' in B and (S.sc, S.tc) != (B.sc, B.tc) or 'sc' not in B
                                              else '`s`、`t` 都处理完了，退出循环'),
        'if sc == tc': lambda S, B, r: (f"`'{S.sc}' == '{S.tc}'`：已经相同，==不用切换，代价 0== → `continue`" if S.sc == S.tc
                                        else f"`'{S.sc}' != '{S.tc}'`：要切换"),
        'continue': '跳过这一位，`res` 不变',
        'index_s = ': "`index_s = ord('{sc}') - 97 = {index_s}`",
        'index_t = ': "`index_t = ord('{tc}') - 97 = {index_t}`",
        'if index_s < index_t': lambda S, B, r: (f'`{S.index_s} < {S.index_t}`：s 在 t 前面 → ==向后直接走，向前要绕圈==' if S.index_s < S.index_t
                                                 else f'`{S.index_s} > {S.index_t}`：s 在 t 后面 → ==向前直接走，向后要绕圈=='),
        'next_cost = next_s[index_t - 1]': '向后直接走 `[{index_s}, {index_t - 1}]`：先取前缀和 `next_s[{index_t - 1}]` = {next_cost}',
        'if index_s > 0': lambda S, B, r: (f'`index_s = {S.index_s} > 0`：要减去 `next_s[{S.index_s - 1}]` = {S.next_s[S.index_s - 1]}' if S.index_s > 0
                                           else '`index_s = 0`：前缀和本身就是从 0 开始的，不用减'),
        'next_cost -= next_s[index_s - 1]': '减掉 `[0, {index_s - 1}]` 这段 → `next_cost` = {next_cost}',
        'prev_cost = prev_s[0] - prev_s[index_s + 1]': '向前绕圈的前半段：从 `s` 走到 `a`，即 `prev[0..{index_s}]` = `prev_s[0] − prev_s[{index_s + 1}]` = {prev_cost}',
        'if index_t  < 25': lambda S, B, r: (f'`index_t = {S.index_t} < 25`：还要补上 z 走到 t 的这段' if S.index_t < 25
                                             else '`index_t = 25`：t 就是 z，没有这段'),
        'prev_cost += prev_s[index_t + 1]': '补上从 `z` 走到 `t` 的 `prev[25..{index_t + 1}]` = `prev_s[{index_t + 1}]` → `prev_cost` = {prev_cost}',
        'next_cost = next_s[-1] - next_s[index_s - 1]': '向后绕圈的前半段：从 `s` 走到 `z`，即 `next[{index_s}..25]` = `next_s[-1] − next_s[{index_s - 1}]` = {next_cost}',
        'if index_t > 0': lambda S, B, r: (f'`index_t = {S.index_t} > 0`：还要补上 a 走到 t 的这段' if S.index_t > 0
                                           else '`index_t = 0`：t 就是 a，没有这段'),
        'next_cost += next_s[index_t - 1]': '补上从 `a` 走到 `t` 的 `next[0..{index_t - 1}]` = `next_s[{index_t - 1}]` → `next_cost` = {next_cost}',
        'prev_cost = prev_s[index_t + 1]': '向前直接走 `[{index_t + 1}, {index_s}]`：先取后缀和 `prev_s[{index_t + 1}]` = {prev_cost}',
        'if index_s < 25': lambda S, B, r: (f'`index_s = {S.index_s} < 25`：要减去 `prev_s[{S.index_s + 1}]` = {S.prev_s[S.index_s + 1]}' if S.index_s < 25
                                            else '`index_s = 25`：后缀和从 s 开始就是 s 到 z，没有多余的，不用减'),
        'prev_cost -= prev_s[index_s + 1]': '减掉 `[{index_s + 1}, 25]` 这段 → `prev_cost` = {prev_cost}',
        'res += min': lambda S, B, r: (f'`min({S.next_cost}, {S.prev_cost})` = =={min(S.next_cost, S.prev_cost)}=='
                                       f'（{"向后" if S.next_cost < S.prev_cost else "向前"}更省）→ `res` = {B.res} + {min(S.next_cost, S.prev_cost)} = =={S.res}=='),
        'return res': '每一位的最小代价加起来：`{res}`',
    },
    cards=dict(
        one_liner='每一位独立算：两个方向的代价都能用前缀和 / 后缀和拿到',
        complexity='时间 `O(n + 26)`，空间 `O(26)`',
        problem=['把 `s` 的每个字母切换成 `t` 的对应字母，求最少总代价',
                 '向后一步（`z` 后是 `a`）花 `nextCost[j]`，向前一步花 `previousCost[j]`',
                 '示例：`"leet"→"code"` 代价全是 1 → `31`；本视频：`"leet"→"coee"` → `54`'],
        quote='可以发现，上面的式子中出现了nextCost的区间和、previousCost的前缀和以及后缀和……我在这里计算的是nextCost的前缀和以及previousCost的后缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['各位互相独立：一趟遍历，每位算 `s[i]→t[i]` 的最小代价再累加',
              '`s < t`：向后直接走一段；向前要绕圈 `s→a`、`z→t`',
              '`s > t`：向前直接走一段；向后要绕圈 `s→z`、`a→t`',
              '这些全是区间 / 前缀 / 后缀和：预处理 `next_s` 前缀和、`prev_s` 后缀和，`O(1)` 取值'],
        result='三对不同的字母分别花 13、20、21，`"e"` 不用动 → 总代价 `54` ✓',
        summary=['时间 `O(n + 26)`，空间 `O(26)`',
                 '易错：边界下标，`index_s > 0` 才能减 `next_s[index_s - 1]`，`index_t < 25` 才能加 `prev_s[index_t + 1]`',
                 '相同字母要先 `continue`，否则会落进 else 分支，`index_s - 1` 可能是 -1',
                 '原文是 Python 2 风格写法，但在 Python 3 下可直接运行，代码未做改动',
                 '对比灵神：灵神把数组延长一倍变成直线，不用分环绕 / 不环绕的多种情况'],
    ),
)

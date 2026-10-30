def _col(S, i, v):
    s, t = S['s'], S['t']
    if s[i] == t[i]:
        return None
    return 'cyan' if s[i] == '0' else 'orange'


CONFIG = dict(
    num=3800, title='使二进制字符串相等的最小成本', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先 swap 互补位 · 再 cross+swap 同向位', tags=['灵神题单', '难度分 1841'],
    code='''
class Solution(object):
    def minimumCost(self, s, t, flipCost, swapCost, crossCost):
        
        zero = 0
        one = 0
        for cs, ct in zip(s, t):
            if cs != ct:
                if cs == '0':
                    zero += 1
                else:
                    one += 1
        
        if flipCost * 2 <= swapCost:
            return flipCost * (zero + one)
        
        res = swapCost * min(zero, one)
        r = abs(zero - one)
        if flipCost * 2 > swapCost + crossCost:
            res += r // 2 * (swapCost + crossCost)
        else:
            res += r // 2 * flipCost * 2
        
        r %= 2
        return res + r * flipCost
''',
    call='Solution().minimumCost("01000", "10111", 10, 2, 2)',
    expect=16,
    skip=['for cs, ct'],
    views=[
        dict(type='string', var='s', label='s', h=170, cell=80, color=_col),
        dict(type='string', var='t', label='t', h=170, cell=80, color=_col),
        dict(type='text', fn=lambda S: f"不匹配位置：`s` 为 0 的有 zero = =={S['zero']}==，`s` 为 1 的有 one = =={S['one']}==" if 'zero' in S else '青 = s 为 0 的不匹配位置，橙 = s 为 1 的不匹配位置', size=26, h=110),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`" + (f"，同向剩余 `r = {S['r']}`" if 'r' in S else '') if 'res' in S else '', size=28, h=100),
    ],
    watch=['zero', 'one', ('res', 'res', 'green'), ('r', 'r', 'yellow')],
    captions={
        'zero = 0': '`zero`：`s[i]=0` 的不匹配位置个数',
        'one = 0': '`one`：`s[i]=1` 的不匹配位置个数',
        'if cs != ct': lambda S, B, r: (f'`{S.cs}` ≠ `{S.ct}`：这个下标不匹配，需要修' if S.cs != S.ct else f'`{S.cs}` = `{S.ct}`：已经相同，跳过'),
        "if cs == '0'": lambda S, B, r: ('`s` 这一位是 0（对应 t 是 1）→ 计入 `zero`' if S.cs == '0' else '`s` 这一位是 1（对应 t 是 0）→ 计入 `one`'),
        'zero += 1': '`zero` = =={zero}==',
        'one += 1': '`one` = =={one}==',
        'if flipCost * 2 <= swapCost': lambda S, B, r: (f'`2×flip = {2 * S.flipCost} ≤ swap = {S.swapCost}`：交换不划算，全翻转' if S.flipCost * 2 <= S.swapCost
                                                        else f'`2×flip = {2 * S.flipCost} > swap = {S.swapCost}`：交换一对互补位比翻转两次便宜'),
        'res = swapCost': '先 swap 互补位：对数 `min(zero, one) = {min(zero, one)}`，`res` = =={res}==',
        'r = abs': '剩下同向的不匹配位 `r = |zero − one|` = =={r}==',
        'if flipCost * 2 > swapCost + crossCost': lambda S, B, r: (f'`2×flip = {2 * S.flipCost} > swap+cross = {S.swapCost + S.crossCost}`：cross 配 swap 比翻转两次便宜' if S.flipCost * 2 > S.swapCost + S.crossCost
                                                                  else f'`2×flip = {2 * S.flipCost} ≤ swap+cross = {S.swapCost + S.crossCost}`：还是翻转更便宜'),
        'res += r // 2 * (swapCost': '每 2 个同向位用 cross + swap：`{r // 2}` 组 × `{swapCost + crossCost}`，`res` = =={res}==',
        'res += r // 2 * flipCost': '每 2 个同向位翻转 2 次：`res` = =={res}==',
        'r %= 2': '同向位为奇数时，落单的 `r = {r}` 个必须翻转',
        'return res': '`{res} + {r} × {flipCost}` = =={res + r * flipCost}==',
    },
    cards=dict(
        one_liner='互补位 swap 消除，同向位 cross+swap 或翻转',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`、`t` 等长，可翻转一位、串内交换两位、同下标跨串交换',
                 '各有一个成本，求让两串相等的最小总成本',
                 '示例：`s=01000, t=10111`，成本 `10, 2, 2` → `16`'],
        quote='cross操作可以与swap搭配执行。对于两个同向的不匹配位置，先对其中一个位置执行cross操作，这样一来这两个不匹配位置就变成了一组互补的不匹配位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['flip 修一个不匹配位；swap 同时修一对==互补==的不匹配位',
              'cross 本身没用，但能把一对同向位变成互补位，再用 swap：共 `swap+cross` 修两个',
              '先把互补位全 swap；剩下 `|zero−one|` 个同向位，比较 `2×flip` 与 `swap+cross`',
              '同向位若为奇数，最后落单一个只能翻转'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`flipCost × 2 <= swapCost` 时 swap 毫无用处，直接全翻转',
                 '易错：同向位成对处理，落单的那个要加一次 flip',
                 '对比灵神：灵神把三种情况算出来取 `min`，yiduobo 按成本大小直接分支',
                 '整数除法本来就是 `//`，代码无需改动'],
    ),
)

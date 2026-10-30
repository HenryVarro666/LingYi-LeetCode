CODE = '''
class Solution(object):
    def racecar(self, target):

        power = [0]
        while power[-1] < target:
            power.append(power[-1] + power[-1] + 1)
        
        f = [None] * (target + 1)
        f[0] = 0
        for now in range(1, target + 1):
            p = 0
            while power[p] < now:
                p += 1
            if now == power[p]:
                f[now] = p
            else:
                f[now] = f[power[p] - now] + p + 1
                for index in range(p):
                    f[now] = min(f[now], f[now - power[p - 1] + power[index]] + p + index + 1)
        
        return f[-1]
'''
_L = CODE.split('\n')
_E = next(i for i, l in enumerate(_L) if 'f[now] = f[power[p] - now]' in l)
_M = next(i for i, l in enumerate(_L) if 'f[now] = min' in l)
SRC = f"(power[p] - now) if _line == {_E} else ((now - power[p - 1] + power[index]) if _line == {_M} else None)"


def _fx(S):
    if 'now' not in S or 'p' not in S or 'f' not in S:
        return '`2^k − 1`：连续 k 次 A 走的距离（速度 1,2,4,…）'
    now, p, power, f = S['now'], S['p'], S['power'], S['f']
    ln = S.get('_line')
    if ln is not None and ln >= _M and 'index' in S:
        i = S['index']
        src = now - power[p - 1] + power[i]
        return (f'先 A 走 {p - 1} 步到 `{power[p - 1]}`，转向，再 A {i} 步退 `{power[i]}`，转向 → 还差 `{src}`：'
                f' `f[{src}] + {p} + {i} + 1`')
    if ln is not None and ln >= _E:
        return f'冲到 `{power[p]}` 再倒车：A×{p}，R，然后从 0 走 `{power[p]} − {now} = {power[p] - now}`'
    return ''


CONFIG = dict(
    num=818, title='赛车', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 冲过头倒车 / 少冲一步再回头',
    tags=['图论算法'],
    code=CODE,
    call='Solution().racecar(6)',
    expect=5,
    views=[
        dict(type='array', var='power', label='power[k] = 2^k − 1：连续 A 走 k 次的距离', pointers={'p': 'blue'}, h=215, cell=110),
        dict(type='array', var='f', label='f[x] = 从 0 走到 x 的最少指令数', cell=110,
             pointers={'now': 'pink', SRC: 'green'}, pointer_labels={SRC: '借用'}, h=270,
             color=lambda S, i, v: 'pink' if S.get('now') == i else None),
        dict(type='text', fn=_fx, size=24),
    ],
    watch=[('now', 'now', 'pink'), ('p', 'p', 'blue'), ('index', lambda S: (S.get('_inner') or {}).get('index'), 'purple'),
           ('f[now]', lambda S: S['f'][S['now']] if 'f' in S and 'now' in S else None, 'green')],
    skip=['power = [0]', 'while power[-1] < target', 'power.append', 'f[0] = 0', 'for now in range', 'p = 0', 'while power[p] < now', 'p += 1',
          'for index in range(p)'],
    captions={
        'f = [None] * (target + 1)': '`power` 是 `2^k − 1`：连续 A 走 k 次就走了这么远。`f[0] = 0`，其余先空着，从小到大填（`f[x]` 要用到更小的 `f`）',
        'if now == power[p]': lambda S, B, r: (
            f'走到 `x = {S.now}`：最小的 `power[p] ≥ {S.now}` 是 `power[{S.p}] = {S.power[S.p]}`，' + (
                '正好相等 → 直接 A 到底' if S.now == S.power[S.p] else '冲过头了，要分两种走法')),
        'f[now] = p': '`x = 2^p − 1`：A 连按 `{p}` 次就到 → `f[{now}] = {p}`',
        'f[now] = f[power[p] - now] + p + 1': '走法一：冲到 `{power[p]}`（A×{p}），转向 R（1 次），再从 0 走回 `{power[p]} − {now} = {power[p] - now}`，→ `f[{now}] = f[{power[p] - now}] + {p} + 1` = =={f[now]}==',
        'f[now] = min(': lambda S, B, r: (
            f'走法二：只走 `{S.p - 1}` 步到 `{S.power[S.p - 1]}`（不冲过头），转向，倒退 `{S.index}` 步，再转向，剩 `{S.now - S.power[S.p - 1] + S.power[S.index]}` → '
            f'指令数 `{S.f[S.now - S.power[S.p - 1] + S.power[S.index]]} + {S.p} + {S.index} + 1`；取较小的，现在 `f[{S.now}]` = =={S.f[S.now]}=='),
        'return f[-1]': '`f[target]` = =={ret}==：例如 `AAARA`（走到 7，倒车，再进 1 步到 6）',
    },
    max_steps=100,
    cards=dict(
        one_liner='f[x] 表示走到 x 的最少指令：要么冲过头倒车，要么少冲一步再回头',
        complexity='时间 `O(n log n)`（n = target），空间 `O(n)`',
        problem=['赛车从 0 出发，速度 `+1`。`A`：位置加速度，速度翻倍；`R`：速度变成 `-1`（或 `+1`）',
                 '求到达位置 `target` 的最短指令序列长度',
                 '本视频：`target = 6` → ==5==（`AAARA`）'],
        quote='每次速度翻倍，那么在当前方向上累积走的距离就是2^k - 1。……令f[x]表示从0开始走到x需要的最少操作次数',
        quote_src='—— yiduobo 题解原文',
        idea=['`x = 2^k − 1`：一路 A 到底，`f[x] = k`',
              '否则取最小的 `2^p − 1 > x`：先冲过头再 R，剩 `2^p − 1 − x`，`f[x] = f[2^p−1−x] + p + 1`',
              '或者只走 `p − 1` 步，R 后倒退 index 步再 R，再从 0 前进，枚举 index'],
        summary=['时间 `O(n log n)`：每个 x 枚举 `p` 个 index',
                 '倒车后速度重置为 1，所以==后面的子问题和从 0 出发一样==，才能用 `f` 递推',
                 '第二种走法要 R 两次：第一次转向回头，第二次转回正方向',
                 '原文是 Python 2 风格，但无需改动即可运行']
    ),
)

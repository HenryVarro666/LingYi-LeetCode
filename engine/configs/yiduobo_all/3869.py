def _lv(S):
    v = S['_inner'].get('level')
    return v if isinstance(v, int) and v < len(S['r']) else None


def _flag(S):
    I = S['_inner']
    if 'state' not in I:
        return 'f[level][s][last][state]：5 位二进制状态 = 贴上界 | 贴下界 | 前导零 | 递减 | 递增'
    st = I['state']
    names = [(16, '贴上界'), (8, '贴下界'), (4, '前导0'), (2, '递减'), (1, '递增')]
    on = ' '.join(n for b, n in names if st & b) or '无'
    return f"level=`{I['level']}`  state=`{st:05b}`（=={on}==）"


CONFIG = dict(
    num=3869, title='统计区间内奇妙数的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 5 位二进制状态',
    tags=['灵神题单', '数位 DP', '难度分 2255'],
    code='''
class Solution(object):
    def countFancy(self, l, r):
        
        r = [int(x) for x in str(r)]
        l = [int(x) for x in str(l)]
        n = len(r)
        l = [0] * (n - len(l)) + l
        
        ma = 9 * n
        g = [True] * (ma + 1)
        for v in range(10, min(99, ma) + 1):
            if v % 10 == v // 10:
                g[v] = False
        for v in range(100, ma + 1):
            if v // 10 % 10 < 2 or v % 10 <= v // 10 % 10:
                g[v] = False
        
        f = [[[[None] * 32 for _ in range(10)] for _ in range(ma + 1)] for _ in range(n)]
        def calc(level, s, last, state, f):
            if level == n:
                if (state & 3) > 0 or g[s]:
                    return 1
                return 0
            
            if f[level][s][last][state] is None:
                f[level][s][last][state] = 0
                st = state & 3
                prefix_zero = state & 4
                low_bound = state & 8
                high_bound = state & 16

                start, end = 0, 9
                if low_bound:
                    start = l[level]
                if high_bound:
                    end = r[level]
                
                for d in range(start, end + 1):
                    if prefix_zero == 4:
                        if d == 0:
                            nxt_state = 4
                        else:
                            nxt_state = 3
                    else:
                        if (st & 1) == 1 and last + 1 <= d:
                            nxt_state = 1
                        elif (st & 2) == 2 and last - 1 >= d:
                            nxt_state = 2
                        else:
                            nxt_state = 0
                    
                    if low_bound and d == l[level]:
                        nxt_state |= 8
                    if high_bound and d == r[level]:
                        nxt_state |= 16
                    
                    f[level][s][last][state] += calc(level + 1, s + d, d, nxt_state, f)
            
            return f[level][s][last][state]
        
        return calc(0, 0, 0, 28, f)
''',
    call='Solution().countFancy(8, 12)',
    expect=5,
    views=[
        dict(type='text', fn=_flag, h=80),
        dict(type='array', var=lambda S: S.get('r') if isinstance(S.get('r'), list) else None, label='上界 r = 12 的数位（蓝箭头 = level）', pointers={_lv: 'blue'},
             pointer_labels={_lv: 'level'}, cell=70, h=190),
        dict(type='array', var=lambda S: S.get('l') if isinstance(S.get('l'), list) else None, label='下界 l = 8，补前导 0 对齐', pointers={_lv: 'pink'},
             pointer_labels={_lv: 'level'}, cell=70, h=190),
        dict(type='calls', hide=('f',), h=230),
    ],
    watch=[('level', "_inner.get('level')", 'blue'), ('s', "_inner.get('s')", 'orange'),
           ('last', "_inner.get('last')", 'pink'), ('state', "_inner.get('state')", 'purple'),
           ('start', "_inner.get('start')", 'cyan'), ('end', "_inner.get('end')", 'cyan')],
    skip=[11, 12, 13, 14, 15, 16, 26, 27, 28, 29, 30, 32, 33],
    max_steps=46,
    captions={
        'if level == n': lambda S, B, r: ('`level = n`：数位填完，开始判断' if S['_inner']['level'] == S.n else '`level < n`，还有数位要填'),
        'if (state & 3) > 0 or g[s]': lambda S, B, r: (
            f"`state & 3 = {S.state & 3}`，`g[{S.s}] = {S.g[S.s]}`："
            + ('数位单调（递增或递减）→ ==奇妙数==' if S.state & 3 else ('数位和是好数 → ==奇妙数==' if S.g[S.s] else '数位不单调且数位和不是好数 → 不是'))),
        'return 1': '返回 1：找到一个奇妙数',
        'return 0': '返回 0',
        'ma = 9': '数位和最多 `9 × n = {ma}`，只需预处理到这里',
        'g = [True]': '`g[v]`：数位和 `v` 是不是好数；先假设都是，再把不是的划掉（循环快进）',
        'f = [[[[None]': '建记忆化表 `f[level][s][last][state]`，`None` = 还没算过',
        'is None': '`f[level][s][last][state]` 还没算过 → 现在算；算过就直接用',
        'start = l[level]': '贴着下界：这一位不能比 `l[level]` 小 → `start = {start}`',
        'end = r[level]': '贴着上界：这一位不能比 `r[level]` 大 → `end = {end}`',
        'for d in range': '枚举这一位填 `d`，范围 `[{start}, {end}]`',
        'nxt_state = 4': '前导 0 状态下填 0：继续是前导 0，`nxt_state = 4`',
        'nxt_state = 3': '前导 0 状态下填了非零数：它同时算==递增==和==递减==，`nxt_state = 3`',
        'nxt_state = 1': '递增状态且 `last+1 <= d` → 保持递增，`nxt_state = 1`',
        'nxt_state = 2': '递减状态且 `last-1 >= d` → 保持递减，`nxt_state = 2`',
        'nxt_state = 0': '递增、递减都被破坏 → `nxt_state = 0`，只能靠数位和判断',
        'nxt_state |= 8': '`d` 恰好等于下界这一位 → 下一位仍贴下界：置位 8',
        'nxt_state |= 16': '`d` 恰好等于上界这一位 → 下一位仍贴上界：置位 16',
        'f[level][s][last][state] += calc': '填 `d = {d}`：递归算 `level+1`，数位和加 `d`，上一位变成 `d`，结果累加到当前状态',
        'return f[level][s][last][state]': '这个状态的方案数是 `{f[level][s][last][state]}`，缓存起来并返回',
        'return calc(0': '入口 `state = 28 = 11100`：贴上界、贴下界、处于前导 0',
    },
    cards=dict(
        one_liner='把贴界、前导零、递增、递减全塞进一个 5 位二进制 state',
        complexity='时间约 `O(10 · n · 9n · 10 · 32)`，空间同量级',
        problem=['数位严格递增或递减的数是好数；数本身或数位和是好数 → 奇妙数',
                 '统计 `[l, r]` 内奇妙数的个数，`r ≤ 10^15`',
                 '本视频：`l = 8, r = 12` → `5`'],
        quote='state 为 5 位的二进制数：最高位表示是否紧贴着上界 r 的前缀，次高位表示是否紧贴着下界 l 的前缀，第三位表示是否依然处于前导 0 的状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['先预处理 1 到 135 的好数表 `g`：数位和最大 `9 × 15 = 135`',
              '把 `l` 补前导 0 到和 `r` 一样长，用 `state` 位运算记录所有标记',
              '`f[level][s][last][state]` 记忆化：填满后看 `state & 3` 或 `g[s]`'],
        summary=['数位和 ≤ `9n`，所以只要预处理 `g[0..9n]`',
                 '前导 0 状态下首个非零数同时算递增和递减（`state = 3`）',
                 '易错点：`d == l[level]` 才保留贴下界，`d == r[level]` 才保留贴上界',
                 '对比灵神：灵神用 0~3 的单调状态机 + `limit_low/limit_high` 布尔，yiduobo 全部压进一个整数'],
    ),
)

VALS = [3, 22, 5, 12, 4]
PAR = [-1, 0, 1, 1, 0]
KIDS = [[] for _ in PAR]
for _i in range(1, len(PAR)):
    KIDS[PAR[_i]].append(_i)


def _digits(v):
    s = set()
    for ch in str(v):
        if ch in s:
            return None
        s.add(ch)
    return ''.join(sorted(s))


def _ms(mask):
    return '{' + ','.join(str(d) for d in range(10) if mask >> d & 1) + '}' if mask else '{}'


_POS = {}


def _layout():
    cnt = [0]
    def go(u, d):
        if not KIDS[u]:
            xs = cnt[0]
            cnt[0] += 1
        else:
            xs = sum(go(c, d + 1) for c in KIDS[u]) / len(KIDS[u])
        _POS[u] = (xs, d)
        return xs
    go(0, 0)
    return cnt[0]


_NL = _layout()


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '树（节点里是 vals[i]，黄 = 当前 x，青 = 刚返回的儿子 y，红 = 数位重复不能选）', 21, T['muted'], bold=True)
    w, h = x1 - x0 - 120, y1 - y0 - 120
    def P(u):
        xs, d = _POS[u]
        return (x0 + 60 + (xs + 0.5) / _NL * w, y0 + 80 + d * h / 2)
    x = S.get('x')
    y = S.get('y')
    for u in range(1, len(PAR)):
        cv.line([P(PAR[u]), P(u)], T['border'], 3)
    for u in range(len(PAR)):
        px, py = P(u)
        bad = _digits(VALS[u]) is None
        fill = T['yellow'] if u == x else T['cyan'] if u == y else T['panel2']
        r = 36
        cv.rect((px - r - 14, py - r, px + r + 14, py + r), fill=fill, outline=T['red'] if bad else T['border'], width=4 if bad else 2, r=r)
        cv.text((px, py - 6), VALS[u], 32, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py + 22), f'#{u} {_ms(sum(1 << int(c) for c in set(str(VALS[u]))))}' if not bad else f'#{u} 重复', 16,
                T['bg'] if fill != T['panel2'] else T['dim'], anchor='mm', mono=True)


def _fmt(k, v):
    return f'{_ms(k)}→{v}'


CONFIG = dict(
    num=3575, title='最大好子树分数', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树形 DP + 数位集合状压 + 启发式合并',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 2360'],
    code='''
class Solution:
    def goodSubtreeSum(self, vals: List[int], par: List[int]) -> int:
        n = len(par)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[par[i]].append(i)

        ans = 0

        def dfs(x: int) -> (Dict[int, int], List[Tuple[int, int]]):
            f = defaultdict(int)
            single = []

            # 计算 vals[x] 的数位集合 mask
            mask = 0
            v = val = vals[x]
            while v:
                v, d = divmod(v, 10)
                if mask >> d & 1:
                    break
                mask |= 1 << d
            else:  # 没有中途 break
                f[mask] = val
                single.append((mask, val))

            for y in g[x]:
                fy, single_y = dfs(y)

                # 启发式合并
                if len(single_y) > len(single):
                    single, single_y = single_y, single
                    f, fy = fy, f

                single += single_y

                # 把子树 y 中的 mask 和 val 一个一个地加到 f 中
                for msk, v in single_y:
                    if v <= f[msk]:
                        continue
                    nf = f.copy()
                    nf[msk] = v
                    for msk2, s2 in f.items():
                        if msk & msk2 == 0:
                            nf[msk | msk2] = max(nf[msk | msk2], v + s2)
                    f = nf

            if f:
                nonlocal ans
                ans += max(f.values())
            return f, single

        dfs(0)
        return ans % 1_000_000_007
''',
    call='Solution().goodSubtreeSum([3, 22, 5, 12, 4], [-1, 0, 1, 1, 0])',
    expect=62,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='f', label='f：x 子树里「数位集合 → 最大分数」', h=170, fmt=_fmt, font=24),
        dict(type='text', fn=lambda S: f"`ans` = {S['ans']}" + (f"   x = {S['x']}（vals = {VALS[S['x']]}）" if 'x' in S else '') if 'ans' in S else '', size=28, h=60),
    ],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'cyan'), ('mask', 'mask', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '儿子表 `g = {g}`；`ans` 累加每个节点的最大好子集分数',
        'dfs(0)': '从根 `0` 开始 DFS',
        'v = val = vals[x]': lambda S, B, r: (f'==节点 {S.x}==，`vals = {S.val}`：数位 `{sorted(set(str(S.val)))}`' + ('，有重复数位 → ==不能选==，`f` 保持空' if _digits(S.val) is None else f'，互不相同 → 集合 `{_ms(sum(1 << int(c) for c in set(str(S.val))))}`')),
        'f[mask] = val': lambda S, B, r: f'没有重复数位：`f[{_ms(S.mask)}] = {S.val}`，同时记入 `single`（单个节点的 mask 和值）',
        'fy, single_y = dfs(y)': lambda S, B, r: (f'进入儿子 `y = {S.y}`，先算它的子树' if S['_inner'].get('x') == S.y else f'儿子 `{S.y}` 返回：`fy = {dict(S.fy)}`，`single_y = {S.single_y}`'),
        'if len(single_y) > len(single)': '`len(single_y) = {len(single_y)}`，`len(single) = {len(single)}`：{"儿子那边更大 → 交换" if len(single_y) > len(single) else "x 这边不小于儿子 → 不换"}。==小的并进大的==，这是启发式合并',
        'single, single_y = single_y, single': '交换 `single` 和 `f`：大的当底，小的 `{single_y}` 去合并',
        'if v <= f[msk]': lambda S, B, r: f'子树 y 里的 `{_ms(S.msk)}` 值 `{S.v}`；`f` 里这个集合已有 `{B.f.get(S.msk, 0)}`：' + ('不能让最大值变大 → 跳过' if S.v <= B.f.get(S.msk, 0) else '更大 → 要加入，并和不相交的集合合并'),
        'nf[msk | msk2] = max': lambda S, B, r: f'`{_ms(S.msk)}` 与 `{_ms(S.msk2)}` 不相交 → 并成 `{_ms(S.msk | S.msk2)}`：`{S.v} + {S.s2}` → `nf[{_ms(S.msk | S.msk2)}]` 变成 =={S.nf[S.msk | S.msk2]}==',
        'f = nf': '合并完成：新的 `f` 有 `{len(f)}` 个状态，最大值 `{max(f.values())}`',
        'ans += max(f.values())': '`maxScore[{x}] = {max(f.values())}` → 加进答案：`ans = {ans}`',
        'return ans % ': '所有节点的 maxScore 之和 `{ans}`，取模后 =={ret}==',
    },
    skip=[3, 4, 5, 6, 11, 12, 15, 17, 18, 19, 20, 21, 24, 26, 32, 34, 37, 40, 41, 42, 43, 47, 50],
    max_steps=140,
    cards=dict(
        one_liner='数位集合当状态，子树之间一个个地合并',
        complexity='时间 `O(n log n · 2^D)`，空间 `O(n · 2^D)`，`D = 10`',
        problem=['无向树，根 `0`，每个点有值 `vals[i]`；子树里选一些点，数位 0–9 每个数字至多出现一次才是好子集',
                 '`maxScore[u]` = `u` 子树里好子集的最大值之和，求所有 `maxScore` 的总和（模 `10^9+7`）',
                 '本视频：`vals=[3,22,5,12,4]`，`par=[-1,0,1,1,0]` → `62`'],
        quote='题目要求转化成：从子树中选择若干没有交集的集合，对应的 vals[i] 之和越大越好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `vals[i]` 的数位存成集合 `V_i`（用 10 位二进制 `mask`），数位重复的数不能选',
              '`f[mask]` = 子树里选若干互不相交的集合、并集恰为 `mask` 的最大分数',
              '合并儿子：不相交的 `mask` 才能相加，哈希表只存有用的状态',
              '启发式合并：把小的 `single` 一个个并进大的，每个点只被「并到更大」O(log n) 次'],
        summary=['方法一枚举子集 `O(n·3^D)` 会超时；方法二合并整张表 `O(n·4^D)`；本视频演示方法三',
                 '数位重复的数（如 22）不能选，`while ... else` 里 `else` 只在没有 `break` 时执行',
                 '`f[msk]` 用的是 `defaultdict`，读取会插入 0，所以才要 `v <= f[msk]` 判断',
                 '答案累加每个节点的 `max(f.values())`，最后才取模'],
    ),
)

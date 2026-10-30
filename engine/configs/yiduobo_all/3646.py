N = 2332


def _build(n):
    f = [0]
    for state in range(1, 512):
        for d in range(1, 10):
            if state & (1 << (d - 1)):
                f.append(f[state ^ (1 << (d - 1))] + d)
                break
    length = len(str(n))
    order = []          # [(state, [finals in search order])]
    for state in range(1, 512):
        if f[state] in (length, length + 1):
            ds = [d for d in range(1, 10) if state >> (d - 1) & 1]
            if sum(d % 2 for d in ds) > 1:
                continue
            mid = ''
            half = []
            for d in ds:
                if d % 2:
                    mid = str(d)
                half.extend([str(d)] * (d // 2))
            perms = sorted(set(itertools.permutations(half)))
            order.append((state, [(p, int(''.join(p) + mid + ''.join(p[::-1]))) for p in perms]))
    return order


_ORDER = _build(N)
_LEAVES = [v for _, ls in _ORDER for _, v in ls]
L_GEN = 60      # generate(num_list) 调用所在行（见 --steps）
L_UPD = 23      # res = final 所在行


def _res_at(S):
    """全局变量 res 在当前这一步的值（global 不在局部变量里，按搜索顺序推算）。"""
    done = 0
    line = S.get('_line') or 0
    if 'final' in S and S['final'] is not None:
        try:
            i = _LEAVES.index(int(S['final']))
            done = i + (1 if line > L_UPD or line == L_UPD else 0)
        except ValueError:
            done = 0
    elif 'state' in S and 'num_list' in S:
        before = 0
        for st, ls in _ORDER:
            if st == S['state']:
                if 'now' in S and 'half_list' in S:
                    now = tuple(S['now'])
                    k = sum(1 for p, _ in ls if p[:len(now)] < now)
                    before += k
                elif line > L_GEN:
                    before += len(ls)
                break
            before += len(ls)
        done = before
    elif 'state' in S and S.get('state') == 511:
        done = len(_LEAVES)
    ok = [v for v in _LEAVES[:done] if v > N]
    return min(ok) if ok else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    res = _res_at(S)
    cv.text((x0 + 18, y0 + 4), f'找 > {N} 的最小特殊数：长度只可能是 {len(str(N))} 或 {len(str(N)) + 1}', 24, T['muted'], bold=True)
    # 数字集合
    ys = y0 + 56
    cv.text((x0 + 18, ys), '当前状态 state 对应的数字集合（亮 = 选中）', 21, T['muted'], bold=True)
    cell = min(74, (x1 - x0 - 40) / 9)
    sx = x0 + 20
    cy = ys + 36
    st = S.get('state') if 'num_list' in S or 'f' in S else None
    on = [d for d in range(1, 10) if st is not None and st >> (d - 1) & 1] if st else []
    for x in range(1, 10):
        X = sx + (x - 1) * cell
        sel = x in on
        fill = (T['orange'] if x % 2 else T['blue']) if sel else T['panel2']
        cv.rect((X + 4, cy, X + cell - 4, cy + cell - 10), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, cy + (cell - 10) / 2), x, 34, T['bg'] if sel else T['dim'], anchor='mm', bold=True, mono=True)
    if st and 'f' in S and st < len(S['f']):
        cv.text((x0 + 18, cy + cell + 2), f'state = {st:09b}　数位总数 f[state] = {S["f"][st]}', 22, T['text'], bold=True)
    # half_list 与 now
    yp = cy + cell + 56
    cv.text((x0 + 18, yp), '左半的数位 half_list（每个数字取一半）与已排好的前缀 now', 21, T['muted'], bold=True)
    half = S.get('half_list')
    now = S.get('now') or []
    mid = S.get('mid')
    cw = 58
    if half is not None:
        for i, d in enumerate(half):
            X = x0 + 20 + i * (cw + 8)
            used = S.get('vis') is not None and i in S['vis']
            cv.rect((X, yp + 36, X + cw, yp + 36 + cw), fill=(52, 60, 72) if used else T['panel2'], r=8, outline=T['border'])
            cv.text((X + cw / 2, yp + 36 + cw / 2), d, 30, T['dim'] if used else T['text'], anchor='mm', bold=True, mono=True)
        xs = x0 + 20 + len(half) * (cw + 8) + 30
        cv.text((xs - 18, yp + 36 + cw / 2), '→', 30, T['dim'], anchor='mm')
        for i, d in enumerate(now):
            X = xs + i * (cw + 8)
            cv.rect((X, yp + 36, X + cw, yp + 36 + cw), fill=T['pink'], r=8)
            cv.text((X + cw / 2, yp + 36 + cw / 2), d, 30, T['bg'], anchor='mm', bold=True, mono=True)
    # 回文
    yq = yp + 36 + 58 + 36
    cv.text((x0 + 18, yq), '拼出的回文 final = 左半 + 中心 + 左半倒序', 21, T['muted'], bold=True)
    fin = S.get('final')
    if fin is not None:
        cv.text((x0 + 22, yq + 28), str(fin), 46, T['text'], bold=True, mono=True)
    cv.text((x0 + 22, yq + 84), '当前最优 res = ' + ('None' if res is None else str(res)), 26, T['yellow'], bold=True)


def _res_s(S):
    r = _res_at(S)
    return r


def _gen_cap(S, B, r):
    return f'数字集合 `{S.num_list}`：奇数最多一个，放正中间 `mid = \'{S.mid if "mid" in S else ""}\'`'


CONFIG = dict(
    num=3646, title='下一个特殊回文数', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='状压 DP 算数位和 + 回溯全排列',
    tags=['数学算法', '贪心与思维', '难度分 2445'],
    code='''
class Solution(object):
    def specialPalindrome(self, n):
        
        f = [0]
        for state in range(1, 512):
            for d in range(1, 10):
                if state & (1 << (d - 1)) == (1 << (d - 1)):
                    f.append(f[state ^ (1 << (d - 1))] + d)
                    break

        global res
        res = None

        def search(now, vis, half_list, mid):
            if len(now) == len(half_list):
                left = ''.join(now)
                right = ''.join(now[::-1])
                final = left + mid + right
                final = int(final)
                if final > n:
                    global res
                    if res is None or res > final:
                        res = final
                return

            for index in range(len(half_list)):
                if index in vis:
                    continue
                if index == 0 or index - 1 not in vis or half_list[index] != half_list[index - 1]:
                    vis.add(index)
                    now.append(half_list[index])
                    search(now, vis, half_list, mid)
                    now.pop()
                    vis.remove(index)

        def generate(num_list):
            mid = ''
            half_list = []
            for d in num_list:
                if d % 2 == 1:
                    mid = str(d)
                half_list.extend([str(d)] * (d // 2))
            
            vis = set()
            now = []
            search(now, vis, half_list, mid)

        length = len(str(n))
        for state in range(1, 512):
            if f[state] == length or f[state] == length + 1:
                num_list = []
                odd = 0
                for d in range(1, 10):
                    if state & (1 << (d - 1)) == (1 << (d - 1)):
                        if d % 2 == 1:
                            odd += 1
                        num_list.append(d)
                
                if odd <= 1:
                    generate(num_list)
        
        return res
''',
    call=f'Solution().specialPalindrome({N})',
    expect=4444,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='calls', h=120, hide=('search',)),
    ],
    watch=[('n', 'n', 'blue'), ('state', 'state', 'cyan'), ('final', 'final', 'green'), ('res', _res_s, 'yellow')],
    skip=[15, 26, 29, 32, 33, 56, 57, 5, 6, 7, 8, 9, 11, 16, 17, 19, 21, 24, 27, 28, 30, 34, 37, 38, 39, 40, 44, 45, 49, 50, 52, 53, 54, 55],
    captions={
        4: '先用状态压缩 DP 算出每个数字集合 `state` 拼出的数位总数 `f[state]`（如 {2,3} 共 2+3 = 5 位）；511 个状态，这里直接快进',
        12: '`res` 记录目前找到的最小特殊数（全局变量），初值 `None`',
        48: '`n = {n}` 有 `{length}` 位 → 只看数位总数是 `{length}` 或 `{length + 1}` 的集合',
        51: lambda S, B, r: f'集合 `state = {S.state:09b}`，数位总数 `f[state] = {S.f[S.state]}` ∈ {{{S.length}, {S.length + 1}}} → 有可能，取出它的数字',
        56: '`{d}` 是奇数，奇数个数 `odd = {odd}`',
        57: '数字 `{d}` 加入 `num_list = {num_list}`',
        59: lambda S, B, r: (f'`odd = {S.odd} ≤ 1`：奇数至多一个，可以放回文中心' if S.odd <= 1 else f'`odd = {S.odd} > 1`：奇数放不下回文中心，这个集合不行'),
        60: '对集合 `{num_list}` 回溯，找出它能形成的所有特殊数',
        41: '`{d}` 是奇数，要放回文中心：`mid = \'{mid}\'`',
        42: '数字 `{d}` 出现 {d} 次，左半只放一半 `{d // 2}` 个 → `half_list = {half_list}`',
        46: '回溯排列：每次从 `half_list` 选一个没用过的数字接在 `now` 后面，排满就是回文的左半',
        15: lambda S, B, r: (f'`now` 已排满 {len(S.half_list)} 位 → 可以生成回文' if len(S.now) == len(S.half_list) else f'`now = {S.now}` 还没排满，继续选下一位'),
        18: '左半排满了 → 回文 = 左半 `{left}` + 中心 `\'{mid}\'` + 左半倒序 `{right}` = =={final}==',
        20: lambda S, B, r: (f'`final = {S.final} > n = {S.n}` → 满足「严格大于 n」，再和 `res` 比较' if int(S.final) > S.n else f'`final = {S.final}` 不大于 `n = {S.n}` → 丢弃'),
        22: lambda S, B, r: (f'`res = {_res_s(S)}`：还没有答案，`{S.final}` 先当作答案' if _res_at(S) is None else f'`res = {_res_at(S)}` 与 `{S.final}` 比：' + ('新的更小 → 更新' if _res_at(S) > int(S.final) else '已有的更小 → 不更新')),
        23: '`res` 更新为 `{final}`',
        26: lambda S, B, r: ('`half_list` 里的数字都试完了，回到上一层' if (B.get('_inner') or {}).get('index') == S['_inner'].get('index')
                              else (f'`half_list[{S.index}]` 已经在 `now` 里了，跳过' if S.index in S.vis else f'试着用 `half_list[{S.index}]`')),
        29: lambda S, B, r: (f'`half_list[{S.index}] = {S.half_list[S.index]}`：可用' if (S.index == 0 or S.index - 1 not in S.vis or S.half_list[S.index] != S.half_list[S.index - 1])
                              else f'`half_list[{S.index}]` 与前一个相同且前一个没用 → 会产生重复排列，跳过'),
        31: '`now` 末尾加入 `{half_list[index]}` → `now = {now}`',
        32: '递归：继续排下一位',
        33: '回溯：把刚选的数字拿掉，换一个再试',
        62: '所有集合都看完了，返回最小的特殊数 `{ret}`',
    },
    max_steps=54,
    cards=dict(
        one_liner='先算每个数字集合的位数，再对合适的集合回溯全排列',
        complexity='时间约 `O(2^9 + K·(m/2)!·m)`，空间 `O(m)`',
        problem=['回文数，且每个数字 `k` 恰好出现 `k` 次，叫==特殊数==',
                 '给定 `n ≤ 10^15`，返回==严格大于== `n` 的最小特殊数',
                 '示例：`n = 33` → `212`；本视频用 `n = 2332`'],
        quote='对于一个整数n，若其长度为m，那么大于n的最小特殊数，其长度要么为m，要么为m + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字只有 1~9，集合共 `2^9` 种；先用==状态压缩 DP== 算出每个集合拼出的数位总数 `f[state]`',
              '只看 `f[state]` 等于 `m` 或 `m+1` 的集合，且奇数至多一个（放回文中心）',
              '每种数字只取一半，回溯出左半的全部不重复排列，复制成回文，取大于 `n` 的最小值'],
        summary=['`f[state]` 用「去掉最低位的那个数字」递推：`f[state] = f[state ^ lowbit] + d`',
                 '`search` 里用 `index - 1 not in vis` 跳过重复数字，避免重复排列',
                 '`res` 是全局变量（`global res`），画面上的 `res` 按搜索顺序推算得到',
                 '原文已是 Python 3 可运行，没有改动',
                 '对比灵神：灵神只在每个集合里找「第一个大于 n」的排列并剪枝，yiduobo 全部枚举再取最小'],
    ),
)

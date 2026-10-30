S1, S2 = 'a2b', '1b2'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        return
    m, n = len(S1), len(S2)
    ln = S.get('_line', 0)
    inner = S.get('_inner', {})
    ci, cj = inner.get('i'), inner.get('j')
    bf = B.get('f')
    cv.text((x0 + 18, y0 + 4), 'f[i][j] = 可能的差 k（s1 比 s2 多的字符数）；黄框 = 正在展开，绿框 = 刚写入', 21, T['muted'], bold=True)
    lw, top = 70, y0 + 110
    cw = min(200, (x1 - x0 - lw - 40) / (n + 1))
    chh = min(120, (y1 - top - 20) / (m + 1))
    for j in range(n + 1):
        X = x0 + lw + j * cw
        cv.text((X + cw / 2, top - 14), f'j={j}', 20, T['pink'], anchor='mb', bold=True, mono=True)
        cv.text((X + cw / 2, top - 40), S2[j - 1] if j else '', 22, T['pink'], anchor='mb', bold=True, mono=True)
    for i in range(m + 1):
        Y = top + i * chh
        cv.text((x0 + lw - 10, Y + chh / 2 - 12), f'i={i}', 20, T['blue'], anchor='rm', bold=True, mono=True)
        cv.text((x0 + lw - 10, Y + chh / 2 + 14), S1[i - 1] if i else '', 22, T['blue'], anchor='rm', bold=True, mono=True)
        for j in range(n + 1):
            X = x0 + lw + j * cw
            cur = (i, j) == (ci, cj) and ln >= 12
            changed = bf is not None and sorted(bf[i][j]) != sorted(f[i][j])
            cv.rect((X + 3, Y + 3, X + cw - 3, Y + chh - 3), fill=T['panel2'], r=8,
                    outline=T['yellow'] if cur else (T['green'] if changed else T['border']), width=4 if (cur or changed) else 1)
            vals = sorted(f[i][j])
            txt = ', '.join(str(v) for v in vals[:5]) + (' …' if len(vals) > 5 else '')
            cv.text((X + cw / 2, Y + chh / 2), txt if vals else '', 24, T['green'] if changed else T['text'], anchor='mm', mono=True, bold=changed)



def _cap_w(name):
    def f(S, B, r):
        t = S[name]
        p, lim = S['p'], len(t)
        base = S['j'] if name == 's2' else S['i']
        if p < lim and p < base + 3 and '1' <= t[p] <= '9':
            return f'`{name}[{p}] = {t[p]}` 是数字，且读的位数没超过 3 → 并入数值'
        why = '已经到串尾' if p >= lim else ('已经连读了 3 位' if p >= base + 3 else f'`{name}[{p}] = {t[p]}` 是字母')
        return f'不能再读数字了：{why}'
    return f


CONFIG = dict(
    num=2060, title='同源字符串检测', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[i][j] 保存差值集合的 DP',
    tags=['其他线性 DP', '难度分 2804'],
    code='''
class Solution(object):
    def possiblyEquals(self, s1, s2):

        m = len(s1)
        n = len(s2)
        f = [[set() for _ in range(n + 1)] for _ in range(m + 1)]
        f[0][0].add(0)

        for i in range(m + 1):
            for j in range(n + 1):
                for k in f[i][j]:
                    if k > 0:
                        p = j
                        now = 0
                        while p < n and p < j + 3 and s2[p] >= '1' and s2[p] <= '9':
                            now = now * 10 + int(s2[p])
                            f[i][p + 1].add(k - now)
                            p += 1
                    
                        if j < n and (s2[j] < '1' or s2[j] > '9'):
                            f[i][j + 1].add(k - 1)

                    elif k < 0:
                        p = i
                        now = 0
                        while p < m and p < i + 3 and s1[p] >= '1' and s1[p] <= '9':
                            now = now * 10 + int(s1[p])
                            f[p + 1][j].add(k + now)
                            p += 1
                        
                        if i < m and (s1[i] < '1' or s1[i] > '9'):
                            f[i + 1][j].add(k + 1)

                    else:
                        if i < m and j < n and s1[i] == s2[j] and k == 0:
                            f[i + 1][j + 1].add(0)
                        
                        p = i
                        now = 0
                        while p < m and p < i + 3 and s1[p] >= '1' and s1[p] <= '9':
                            now = now * 10 + int(s1[p])
                            f[p + 1][j].add(now)
                            p += 1
                        
                        p = j
                        now = 0
                        while p < n and p < j + 3 and s2[p] >= '1' and s2[p] <= '9':
                            now = now * 10 + int(s2[p])
                            f[i][p + 1].add(-now)
                            p += 1

        return 0 in f[m][n]
''',
    call=f'Solution().possiblyEquals({S1!r}, {S2!r})',
    expect=True,
    skip=['for i in range(m + 1)', 'for j in range(n + 1)', 'for k in f[i][j]', 'p += 1', 'now = 0', 'p = j', 'p = i',
          'now = now * 10'],
    max_steps=90,
    views=[
        dict(type='string', var='s1', label='s1', h=165, cell=80,
             color=lambda S, k, v: 'blue' if k == S.get('_inner', {}).get('i') and S.get('_line', 0) >= 12 else None),
        dict(type='string', var='s2', label='s2', h=165, cell=80,
             color=lambda S, k, v: 'pink' if k == S.get('_inner', {}).get('j') and S.get('_line', 0) >= 12 else None),
        dict(type='custom', draw=_draw, h=400),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange'), ('now', 'now'), ('p', 'p')],
    captions={
        15: _cap_w('s2'), 26: _cap_w('s1'), 40: _cap_w('s1'), 47: _cap_w('s2'),
        'f[i][j + 1].add(k - 1)': 's2 的字母补掉 s1 多出的 1 个字符：差 `{k} → {k - 1}`，写入 `f[{i}][{j + 1}]`',
        'f[i + 1][j].add(k + 1)': 's1 的字母补掉 s2 多出的 1 个字符：差 `{k} → {k + 1}`，写入 `f[{i + 1}][{j}]`',
        'f[i + 1][j + 1].add(0)': '字母对上，两边各前进 1 格，差仍是 0，写入 `f[{i + 1}][{j + 1}]`',
        'm = len(s1)': '`m = {m}`，s1 = `{s1!r}`',
        'n = len(s2)': '`n = {n}`，s2 = `{s2!r}`',
        'f = [[set()': '`f[i][j]` 是一个集合：s1 前 i 个、s2 前 j 个字符对应的原串长度之差 k（s1 − s2）的所有可能',
        'f[0][0].add(0)': '起点：两边都还没读，长度差 `0`',
        'if k > 0': lambda S, B, r: (f'格子 `f[{S.i}][{S.j}]` 里取到差 `k = {S.k}`：`k > 0` → s1 多出 {S.k} 个字符，要由 s2 往后补' if S.k > 0
                                    else f'格子 `f[{S.i}][{S.j}]` 里取到差 `k = {S.k}`，不大于 0 → 看下一个分支'),
        'if j < n and (s2[j]': lambda S, B, r: (f'`s2[{S.j}] = {S.s2[S.j]}` 是字母，可以补 s1 的 1 个字符 → 下一行写入 `f[{S.i}][{S.j + 1}]`：`k − 1 = {S.k - 1}`'
                                               if S.j < S.n and not ('1' <= S.s2[S.j] <= '9') else '`s2[j]` 是数字（上面已按数值处理）或已读完，不能当字母补位'),
        'elif k < 0': lambda S, B, r: (f'`k = {S.k} < 0`：s2 多出 {-S.k} 个字符，要由 s1 往后补' if S.k < 0 else '`k = 0`，也不小于 0 → 进入 else（两边刚好等长）'),
        'if i < m and (s1[i]': lambda S, B, r: (f'`s1[{S.i}] = {S.s1[S.i]}` 是字母，补 s2 的 1 个字符 → 下一行写入 `f[{S.i + 1}][{S.j}]`：`k + 1 = {S.k + 1}`'
                                               if S.i < S.m and not ('1' <= S.s1[S.i] <= '9') else '`s1[i]` 是数字（上面已按数值处理）或已读完，不能当字母补位'),
        'else:': '`k = 0`：两边长度刚好相等，可以三选一：字母对字母、s1 读数字、s2 读数字',
        'if i < m and j < n and s1[i] == s2[j]': lambda S, B, r: (f'`s1[{S.i}] = {S.s1[S.i]}` == `s2[{S.j}]` → 两个字母==一一对上==，下一行写入 `f[{S.i + 1}][{S.j + 1}]`：差 0'
                                                                  if S.i < S.m and S.j < S.n and S.s1[S.i] == S.s2[S.j]
                                                                  else '不是两个相同的字母，不能直接对上'),
        'f[i][p + 1].add(k - now)': '把 `s2[{j}..{p}]` 读成数 `{now}`：s2 对应的原串多了 {now} 个字符，差变成 `{k} − {now}` = =={k - now}==，写入 `f[{i}][{p + 1}]`',
        'f[p + 1][j].add(k + now)': '把 `s1[{i}..{p}]` 读成数 `{now}`：差变成 `{k} + {now}` = =={k + now}==，写入 `f[{p + 1}][{j}]`',
        'f[p + 1][j].add(now)': 'k = 0 时 s1 读数 `{now}`：s1 多出 {now} 个字符，差 = =={now}==，写入 `f[{p + 1}][{j}]`',
        'f[i][p + 1].add(-now)': 'k = 0 时 s2 读数 `{now}`：s2 多出 {now} 个字符，差 = =={-now}==，写入 `f[{i}][{p + 1}]`',
        'return 0 in': lambda S, B, r: f'`f[{S.m}][{S.n}] = {sorted(S.f[S.m][S.n])}`，{"含有 0 → 两个串能还原成同一个原串" if r else "没有 0 → 不可能同源"}，返回 =={r}=='
    },
    cards=dict(
        one_liner='f[i][j] 存差值集合：k 只往 0 的方向补',
        complexity='时间约 `O(m·n·K)`（K = 差值个数，约 1000），空间同阶',
        problem=['`s1`、`s2` 是编码后的串：字母原样，数字表示一段被压缩的任意字母（连续数字最多 3 位）',
                 '问两个串能否由==同一个原字符串==编码得到',
                 '示例：`s1 = "internationalization", s2 = "i18n"` → `true`',
                 '本视频演示：`s1 = "a2b", s2 = "1b2"` → `true`（都是 4 个字符）'],
        quote='因为k最终是奔着0去的，因此在某一时刻k大于等于0时，这些数字始终是要被s2中的字符匹配掉的，因此在这里没必要继续考虑往里面添加s1的字符。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j][k]`：s1 前 i 个、s2 前 j 个，s1 比 s2 多 k 个可用字符是否出现；用集合存 k',
              '`k > 0`：只让 s2 往后补（字母补 1 个，或读 1~3 位数字）；`k < 0` 对称，只让 s1 补',
              '`k = 0`：字母对字母，或任一边读数字；最后看 `0 in f[m][n]`'],
        summary=['时间/空间：状态 `m·n` 个集合，每个集合差值最多约 2000 个',
                 '易错：数字读法最多 3 位，`now = now * 10 + int(c)` 逐位累积，每一位都是一个新状态',
                 '易错：`k = 0` 时两边都能读数字；字母对字母要求 `s1[i] == s2[j]`',
                 '原文本身已是 Python 3 可运行写法（函数内无 `/`、`xrange`），无需改动'],
    ),
)

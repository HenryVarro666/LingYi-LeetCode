def _txt(S):
    ch, k = S.get('choose'), S.get('k')
    if ch is None or k is None or not ch:
        return '把 26 个字母按「出现几次」分组：`choose[i]` 个字母各出现 `k-i` 次'
    parts = [f'{c} 个字母×{k - i}次' for i, c in enumerate(ch)]
    return '当前分配：' + '，'.join(parts)


CONFIG = dict(
    num='LCP 25', title='古董键盘', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='dfs 枚举次数分布 + 组合数 + 多重集排列',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def keyboard(self, k, n):

        C = [[0] * 27 for _ in range(27)]
        C[0][0] = C[1][0] = C[1][1] = 1
        mod = 10 ** 9 + 7
        for i in range(2, 27):
            C[i][0] = C[i][i] = 1
            for j in range(1, i):
                C[i][j] = C[i - 1][j] + C[i - 1][j - 1]
                if C[i][j] >= mod:
                    C[i][j] -= mod
        self.res = 0

        def quick_pow(base, p):
            if p == 0:
                return 1
            elif p == 1:
                return base
            else:
                tmp = quick_pow(base, p // 2)
                tmp = tmp * tmp % mod
                if p % 2 == 1:
                    tmp = tmp * base % mod
                return tmp

        rev_fac_pow = [[], [1], [1], [1], [1], [1]]
        fac = 1
        for index in range(1, k + 1):
            fac *= index
            rev_fac_pow[index].append(quick_pow(fac, mod - 2))
            p = 2
            while p * index <= n:
                rev_fac_pow[index].append(rev_fac_pow[index][-1] * rev_fac_pow[index][1] % mod)
                p += 1
        
        def dfs(choose, level, rest_alpha, rest_n):
            if level == k - 1:
                if rest_alpha < rest_n:
                    return
                now = 1
                tot = 26
                choose.append(rest_n)
                for index in range(k):
                    now = now * C[tot][choose[index]] % mod
                    now = now * rev_fac_pow[k - index][choose[index]] % mod
                    tot -= choose[index]

                for index in range(1, n + 1):
                    now = now * index % mod
                
                self.res += now
                choose.pop()
                return
            
            cnt = 0
            while cnt <= rest_alpha and cnt * (k - level) <= rest_n:
                choose.append(cnt)
                dfs(choose, level + 1, rest_alpha - cnt, rest_n - choose[-1] * (k - level))
                cnt += 1
                choose.pop()
        
        choose = []
        dfs(choose, 0, 26, n)
        return self.res % mod
''',
    call='Solution().keyboard(2, 3)',
    expect=17550,
    views=[
        dict(type='array', var=lambda S: S['_inner'].get('choose', S.get('choose', [])) if isinstance(S.get('choose', []), list) else [],
             label='choose：choose[i] 个字母各出现 k−i 次', cell=84, h=150),
        dict(type='text', fn=_txt, size=28, h=90),
        dict(type='calls', hide=('choose',), h=240),
    ],
    watch=[('level', 'level', 'blue'), ('rest_alpha', 'rest_alpha'), ('rest_n', 'rest_n'), 'now', ('res', 'self.res', 'green')],
    max_steps=110,
    skip=['C[i][0] = C[i][i] = 1', 'for j in range(1, i)', 'C[i][j] =', 'if C[i][j] >= mod', 'C[i][j] -= mod',
          'for i in range(2, 27)', 'if p == 0', 'return 1', 'elif p == 1', 'return base', 'tmp = quick_pow', 'tmp = tmp * tmp % mod',
          'if p % 2 == 1', 'tmp = tmp * base % mod', 'return tmp', 'mod = 10', 'for index in range(1, n + 1)',
          'C[0][0] =', 'p = 2', 'self.res = 0', 'p += 1', 'tot -= choose', 'fac *= index', 'tot = 26', 'now = 1', 'fac = 1', 'cnt = 0', 'choose = []'],
    captions={
        'C = [[0]': '预处理组合数表 `C[i][j]`（`i ≤ 26`，杨辉三角递推，视频里略过）；`self.res` 累计各分布的方案数',
        'rev_fac_pow = ': '`rev_fac_pow[m][c]` = `(m!)^(-c)`：重复字母要除以 `m!^c`，用逆元代替除法',
        'for index in range(1, k + 1)': lambda S, B, r: ('阶乘逆元准备好了' if B.get('index') == S.index else f'`index = {S.index}`：准备「出现 {S.index} 次的字母」的阶乘逆元'),
        'rev_fac_pow[index].append(quick_pow': '`fac = {index}! = {fac}`，它的逆元 = `fac^(mod-2)`，快速幂求得（视频里略过递归）',
        'while p * index <= n': lambda S, B, r: (f'`{S.p} × {S.index} = {S.p * S.index}`，' + ('≤ n，还有这么多个这种字母的可能 → 继续' if S.p * S.index <= S.n else '> n，不会有这么多个 → 结束')),
        'rev_fac_pow[index].append(rev_fac_pow': '逆元的 `{p}` 次方：上一项再乘一次 `rev_fac_pow[{index}][1]`',
        'if level == k - 1': lambda S, B, r: (f'`level = {S.level}`：到最后一层了，剩下的字母各出现 1 次，不用再枚举' if S.level == S.k - 1
                                              else f'`level = {S.level}`：还要枚举「出现 {S.k - S.level} 次的字母有几个」'),
        'if rest_alpha < rest_n': lambda S, B, r: (f'字母不够：`{S.rest_alpha} < {S.rest_n}`，剩下 {S.rest_n} 次出现需要 {S.rest_n} 个不同字母 → 返回' if S.rest_alpha < S.rest_n
                                                   else f'`{S.rest_alpha} ≥ {S.rest_n}`：够用，剩下 {S.rest_n} 个位置各用一个不同字母（出现 1 次）'),
        'choose.append(rest_n)': '最后一档：出现 1 次的字母 `{rest_n}` 个 → `choose = {choose}`',
        'for index in range(k)': lambda S, B, r: ('每一档都算完了' if B.get('index') == S.index else f'第 `{S.index}` 档：算选字母的方案数，并除掉重复排列'),
        'now = now * C[tot]': '选字母：从剩下 `{tot}` 个字母里选 `{choose[index]}` 个 → `C({tot}, {choose[index]})`，`now = {now}`',
        'now = now * rev_fac_pow': '这 `{choose[index]}` 个字母各出现 `{k - index}` 次：除以 `({k - index}!)^{choose[index]}` → `now = {now}`；这一档用掉后还剩 `{tot - choose[index]}` 个字母',
        'now = now * index': '`now × {index}`：累乘出 `n! = {n}!`（n 个位置全排列）→ {now}',
        'self.res += now': '这种次数分布共 `{now}` 种字符串，累加 → `self.res = {self.res}`',
        'choose.pop()': '回溯：撤销最后一档',
        'while cnt <= rest_alpha': lambda S, B, r: (f'`cnt = {S.cnt}`：令 {S.k - S.level} 次的字母有 {S.cnt} 个，占 `{S.cnt * (S.k - S.level)}` 个位置，是否 ≤ 剩余 `{S.rest_n}`：' + ('可以' if S.cnt <= S.rest_alpha and S.cnt * (S.k - S.level) <= S.rest_n else '超了，枚举结束')),
        'choose.append(cnt)': '选定这一档字母数 `{cnt}` → `choose = {choose}`',
        'dfs(choose, level + 1': '进入下一档：剩余字母 `{rest_alpha - cnt}`，剩余位置 `{rest_n - choose[-1] * (k - level)}`',
        'cnt += 1': '这一档试下一个数：`cnt → {cnt}`',
        'dfs(choose, 0, 26, n)': '从第 0 档开始：26 个字母，n = {n} 个位置',
        'return self.res': '答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='先枚举「各出现几次」的字母分布，再算选字母和排列',
        complexity='时间约 `O(分布数 × k)`（`k ≤ 5`），空间 `O(k)`',
        problem=['键盘有 26 个字母键，每个键==最多只能按 k 次==（总共）',
                 '依次按 `n` 次，求能得到的不同字符串个数，模 `10^9+7`',
                 '示例：`k=1, n=2` → `650`；本视频：`k=2, n=3` → `17550`'],
        quote='设置一个长度为k的数组choose，满足 choose[0] * k + choose[1] * (k - 1) + ... + choose[k - 1] = n，即最终的排列中，有choose[0]个字母出现了k次，choose[1]个字母出现了k - 1次，以此类推。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 很小，先 dfs 枚举所有「出现 k 次的字母几个、k-1 次的几个……」',
              '选字母：`C(26, c0) × C(26-c0, c1) × …`',
              '排列：`n!` 除以 `∏ (m!)^{choose}`（重复字母去重），除法用乘法逆元'],
        summary=['dfs 里 `rest_alpha`、`rest_n` 同时约束字母数和位置数',
                 '最后一档（出现 1 次）不用枚举，直接 `choose.append(rest_n)`，字母要够：`rest_alpha ≥ rest_n`',
                 '预处理 `C[i][j]` 和 `rev_fac_pow`，查表求值；记得每步取模',
                 '原文为 Python 2 写法，`quick_pow` 里的整数除法 `p / 2` 已改为 `p // 2`；题意按 LeetCode 原题（每个键最多按 k 次）'],
    ),
)

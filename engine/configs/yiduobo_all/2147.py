CONFIG = dict(
    num=2147, title='分隔长廊的方案数', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='逐段扫描 · 植物数加一相乘',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·数学算法', '难度分 1915'],
    code='''
class Solution(object):
    def numberOfWays(self, corridor):

        res = 1
        n = len(corridor)
        p = 0
        now = 0
        mod = 10 ** 9 + 7
        while p < n:
            res = res * (now + 1) % mod
            now = 0
            while p < n:
                if corridor[p] == 'S':
                    now += 1
                p += 1
                
                if now == 2:
                    break
            
            if now != 2:
                return 0
            
            now = 0
            while p < n and corridor[p] == 'P':
                now += 1
                p += 1
        
        return res
''',
    call='Solution().numberOfWays("SPSPPPSSPSS")',
    expect=8,
    views=[
        dict(type='string', var='corridor', pointers={'p': 'blue'}, h=260, cell=70,
             color=lambda S, i, v: ('yellow' if v == 'P' and S['_line'] in (24, 25, 26) and S['p'] - S['now'] <= i < S['p'] else 'green' if v == 'S' and i < S['p'] else None) if 'p' in S else None,
             dim=lambda S, i, v: v == 'P' and 'p' in S and not (S['_line'] in (24, 25, 26) and S['p'] - S['now'] <= i < S['p'])),
        dict(type='text', h=90, size=34, fn=lambda S: (f"已读到 `p` = =={S['p']}==，当前段座位 `{S['now']}`，方案数 `res` = =={S['res']}==" if 'p' in S and 'res' in S else '')),
    ],
    max_steps=90,
    watch=[('p', 'p', 'blue'), ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 1': '`res = 1`：方案数是每段分界处选法数的乘积',
        'p = 0': '`p`：从左往右扫描的位置',
        7: '`now`：先当作"当前段座位数"，后面又用来数两段之间的植物数',
        9: lambda S, B, r: (f"`p = {S.p} < {S.n}`：还有没处理的位置，开始处理下一段" if S.p < S.n else f"`p = {S.p}`：走廊扫完了 → 结束"),
        'res = res * (now + 1)': '上一段结束后有 `{now}` 株植物可分给前后两段 → 有 `{now}+1 = =={now+1}==` 种分法，`res` → =={res}==',
        11: '`now` 清零，重新数这一段的座位',
        23: '`now` 清零，改用来数后面连续的植物',
        12: lambda S, B, r: (f"`p = {S.p} < {S.n}`：继续往右找座位" if S.p < S.n else f"`p = {S.p}`：走廊走完了，这一段没凑够 2 个座位"),
        'if corridor[p] ==': lambda S, B, r: (f"`corridor[{S.p}] = 'S'` → 是座位" if S.corridor[S.p] == 'S' else f"`corridor[{S.p}] = 'P'` → 植物，不计数"),
        'now += 1': lambda S, B, r: (f"座位数 `now` → {S.now}" if S.corridor[S.p] == 'S' else f"植物数 `now` → {S.now}"),
        'p += 1': '`p` → {p}',
        'if now == 2': lambda S, B, r: (f"`now = {S.now}`：凑够 2 个座位，这一段结束 → 跳出" if S.now == 2 else f"`now = {S.now}`：还没凑够 2 个座位，继续往右"),
        'break': '这一段的两个座位到手，跳出内层循环',
        'if now != 2': lambda S, B, r: (f"`now = {S.now} != 2`：走廊走完也凑不够 2 个座位 → 无解，返回 0" if S.now != 2 else "`now = 2`：这一段合法"),
        'while p < n and corridor[p]': lambda S, B, r: (f"`corridor[{S.p}] = 'P'` → 紧跟着的植物，属于可以左右分配的部分" if S.p < S.n and S.corridor[S.p] == 'P' else "遇到座位或走廊尽头，植物数完了"),
        'return res': '方案数 `{res}`',
    },
    cards=dict(
        one_liner='每段取两个座位，段间的 k 株植物有 k+1 种分法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`corridor` 里 `S` 是座位、`P` 是植物，用屏风分段',
                 '每段恰好 2 个座位，植物数不限，求方案数（模 `10^9+7`）',
                 '本视频：`SPSPPPSSPSS` → `8`'],
        quote='设这些植物的数量为k，那么就有(0, k), (1, k - 1), ..., (k, 0)这k + 1中划分方案，因此需要将答案乘上k + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['座位总数为奇数必然无解；否则每次划走两个座位',
              '划分点只能在"第 2 个座位"和"下一段第 1 个座位"之间的植物里挪动',
              '这 `k` 株植物有 `k+1` 个切点，把 `k+1` 乘进答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '第一段前面没有可挪的植物，`now = 0` → 乘 1，不影响答案',
                 '最后一段后面的植物归最后一段，不再乘',
                 '座位不足 2 个的尾巴 → `now != 2` → 返回 0',
                 '对比灵神：灵神用"下标差"，k+1 恰好等于两个座位的下标差'],
    ),
)

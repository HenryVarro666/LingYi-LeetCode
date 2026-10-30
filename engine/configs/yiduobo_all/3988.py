def _cnt(g):
    m, n = len(g), len(g[0])
    f = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if g[i][j] == '.':
                f[i][j] = 1 if i == j == 0 else (f[i - 1][j] if i else 0) + (f[i][j - 1] if j else 0)
    return f


def _gc(S, i, j, v):
    return 'green' if v == '.' else None


def _cur(S):
    for name in ('rev_res', 'res'):
        g = S.get(name)
        if isinstance(g, list) and g and not (name == 'res' and S.get('rev') and 'rev_res' in S):
            return g
    return None


def _txt(S):
    if S.get('rev') and 'rev_res' in S and S.get('_line') not in (None,) and 'res' in S and S['res']:
        pass
    g = S.get('rev_res') if S.get('rev_res') is not None and S.get('_line', 0) >= 34 else S.get('res')
    if not g:
        return '目标：`m×n` 网格里，从左上到右下恰好 `k` 条路径'
    g = [''.join(r) for r in g]
    return f"这张网格的路径数 = =={_cnt(g)[-1][-1]}==（目标 k = {S['k']}）"


def _tab(S):
    g = S.get('rev_res') if S.get('rev_res') is not None and S.get('_line', 0) >= 34 else S.get('res')
    if not g:
        return None
    return _cnt([''.join(r) for r in g])


CONFIG = dict(
    num=3988, title='创建一个恰好有 K 条路径的网格图 I', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='两行 DP 构造 + 转置',
    tags=['灵神题单', '贪心与思维', '难度分 2055'],
    code='''
class Solution(object):
    def createGrid(self, m, n, k):
        
        rev = False
        if m > n:
            m, n = n, m
            rev = True
        
        if m == 1:
            if k == 1:
                res = ['.' * n]
            else:
                res = []
        
        elif n >= k:
            res = ['.' * n, '#' * (n - k) + '.' * k]
            res.extend(['#' * (n - 1) + '.'] * (m - 2))
        
        elif m == 2:
            res = []
        
        elif m == 3:
            res = ['..#', '...', '#..']
        
        if not res:
            return res
            
        if rev:
            rev_res = [['.'] * m for _ in range(n)]
            for i in range(m):
                for j in range(n):
                    rev_res[j][i] = res[i][j]
            
            return [''.join(line) for line in rev_res]
        
        return res
''',
    call='Solution().createGrid(4, 3, 3)',
    expect=['.##', '..#', '..#', '...'],
    skip=['for j in range(n)', 'for i in range(m)'],
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='grid', var=lambda S: [list(r) for r in S['res']] if S.get('res') else None,
             label='res（先按 m ≤ n 构造，绿 = 空格）', cell=84, h=230, color=_gc),
        dict(type='grid', var=lambda S: S['rev_res'] if S.get('rev_res') else None,
             label='rev_res（转置后的答案）', cell=84, h=290, color=_gc),
        dict(type='table', var=_tab, label='每格路径数', cell=70, h=290),
    ],
    watch=['m', 'n', 'k', 'rev'],
    captions={
        'rev = False': '`rev` 记录是否交换过行列',
        'if m > n': lambda S, B, r: (f'`m = {B.m} > n = {B.n}`：行比列多 → 交换，先按 `m ≤ n` 构造，最后再转置'
                                     if B.m > B.n else '`m ≤ n`，不用交换'),
        'm, n = n, m': '交换后 `m = {m}`，`n = {n}`',
        'if m == 1': '`m = {m}`：不是单行，继续',
        'elif n >= k': '`n = {n} ≥ k = {k}`：列数够 → 前两行构造出 `k` 条路径',
        "res = ['.' * n,": '第一行全空；第二行前 `n-k` 格障碍、后 `k` 格空 → 第二行末 `k` 格路径数依次为 1、2、…、`k`',
        'res.extend': '后面 `m-2` 行只留最后一列：从 `(1,n-1)` 只能一路向下，路径数定格在 =={k}==',
        'if not res': '`res` 非空，有解',
        'if rev': '`rev = {rev}`：之前交换过 → 需要转置回来',
        'rev_res = [': '准备 `n × m` 的新网格（行列对调）',
        'rev_res[j][i] = res[i][j]': '`rev_res[{j}][{i}] = res[{i}][{j}]`：转置',
        "return [''.join": '转置完，每行拼成字符串返回',
    },
    cards=dict(
        one_liner='两行空网格能凑出 k 条路，其余行用最后一列“锁住”',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['构造 `m×n` 网格，`.` 空、`#` 障碍；只能向右/向下，左上到右下恰好 `k` 条路径',
                 '无解返回空数组；`m,n ≤ 10`，`k ≤ 4`',
                 '本视频：`m=4, n=3, k=3`'],
        quote='若n >= k，那么可以将前两行构造为第一行全空格，第二个前n - k个为障碍，最后k个为空格，那么就会得到恰好是k条路径。',
        quote_src='—— yiduobo 题解原文',
        idea=['先假设 `m ≤ n`；否则交换，最后转置',
              '两行 DP：第二行末 `k` 格路径数 1、2、…、`k`',
              '后面各行只留最后一列，路径数不再变化；漏网的 `2×2, 2×3, 3×3` 单独处理'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：`m=1` 只有 `k=1` 有解；`m=2, n<k` 无解；`3×3, k=4` 要手工构造 `["..#","...","#.."]`',
                 '原文为 Python 2 风格，代码在 Python 3 下无需改动',
                 '对比灵神：灵神用 `k×2` 空区域 + 第一列/最后一行；yiduobo 用前两行 + 最后一列，再靠转置'],
    ),
)

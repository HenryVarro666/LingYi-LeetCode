def _txt(S):
    I = S['_inner']
    if 'now' not in I:
        return '`f[x]` = 当前 `x` 分时，最终得分 ≤ N 的概率'
    now, N, K, W = I['now'], I['N'], I['K'], I['W']
    if now >= K:
        return f'`{now} ≥ K = {K}`：停牌。`{now} ≤ N = {N}` 才算成功' + ('，`f = 1`' if now <= N else '：超过 N，`f = 0`')
    if now == K - 1:
        return f'`x = K − 1 = {now}`：不能用差分递推，按原始式子数一数'
    return f'`f[x] = f[x+1] + (f[x+1] − f[x+W+1]) / W`，`x = {now}`，`W = {W}`'


CONFIG = dict(
    num=837, title='新 21 点', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='概率 DP · 记忆化 + 差分化简滑窗和',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2350'],
    code='''
class Solution(object):
    def new21Game(self, N, K, W):

        f = [None] * (K + W)
        return self.dfs(0, N, K, W, f)

    def dfs(self, now, N, K, W, f):
        if f[now] is None:
            if now >= K:
                if now <= N:
                    f[now] = 1.0
                else:
                    f[now] = 0.0
            elif now == K - 1:
                tmp = 0
                for index in range(1, W + 1):
                    if now + index <= N:
                        tmp += 1
                f[now] = tmp * 1.0 / W
            else:
                f[now] = self.dfs(now + 1, N, K, W, f) + (self.dfs(now + 1, N, K, W, f) - self.dfs(now + W + 1, N, K, W, f)) / W
            
        return f[now]
''',
    call='Solution().new21Game(5, 4, 3)',
    expect=0.802469135802469,
    skip=['else:', 'if now <= N', 'tmp = 0', 'if now + index <= N', 'tmp += 1', 'for index in range'],
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='f', label='f[x]（· = 还没算；黄 = 当前 x）', h=190, cell=92, pointers={'now': 'yellow'}),
        dict(type='calls', h=300),
    ],
    watch=[('now', 'now', 'yellow'), ('N', 'N', 'cyan'), ('K', 'K', 'orange'), ('W', 'W', 'pink')],
    captions={
        'f = [None] * (K + W)': '`f[x]`：从 `x` 分出发的成功概率；最大只会走到 `K−1+W`，开 `K+W` 格，`None` = 未算（记忆化）',
        'return self.dfs(0': '答案是 `f[0]`：从 0 分开始',
        'if f[now] is None': lambda S, B, r: f'`f[{S.now}]` ' + ('还没算 → 往下算' if S.f[S.now] is None else '算过了 → 直接用，==记忆化=='),
        'if now >= K': lambda S, B, r: f'`now = {S.now}` {"≥" if S.now >= S.K else "<"} `K = {S.K}`：' + ('已经停牌' if S.now >= S.K else '还要继续抽'),
        'f[now] = 1.0': '`{now} ≤ N = {N}`：停牌时分数没爆 → `f[{now}] = 1`',
        'f[now] = 0.0': '`{now} > N = {N}`：停牌时已超过 N → `f[{now}] = 0`',
        'elif now == K - 1': lambda S, B, r: f'`now = {S.now}` {"==" if S.now == S.K - 1 else "≠"} `K − 1 = {S.K - 1}`：' + ('==边界==，`f[K]` 不符合差分式' if S.now == S.K - 1 else '用差分递推'),
        'f[now] = tmp * 1.0 / W': '抽 `1..{W}` 中有 `{tmp}` 个点数使得 `{now}+点数 ≤ {N}` → `f[{now}] = {tmp}/{W}` = =={f[now]:.4f}==',
        'f[now] = self.dfs(now + 1': lambda S, B, r: (f'要算 `f[{B.now}]`：先递归求 `f[{B.now+1}]` 和 `f[{B.now+B.W+1}]`。'
                                                     '公式 `f[x] = f[x+1] + (f[x+1] − f[x+W+1]) / W`（相邻两项相减，滑窗和被差分掉）'),
        'return f[now]': lambda S, B, r: f'返回 `f[{S.now}]` = =={r:.4f}==',
    },
    cards=dict(
        one_liner='f[x] 是平均值，相邻两项一减，滑窗和就消掉了',
        complexity='时间 `O(K+W)`，空间 `O(K+W)`',
        problem=['爱丽丝从 0 分起，分数 `< K` 就抽牌，每次等概率得 `1..W` 分，`≥ K` 就停',
                 '求最终分数 `≤ N` 的概率',
                 '示例：`N=21, K=17, W=10` → `0.73278`；本视频：`N=5, K=4, W=3` → `0.8025`'],
        quote='f[x] = (f[x + 1] + f[x + 2] + ... + f[x + w]) / w ……下式减去上式就有 f[x + 1] - f[x] = (f[x + w + 1] - f[x + 1]) / w ……化简后可得 f[x] = f[x + 1] + (f[x +1] - f[x + w + 1]) / w',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[x]`：当前 `x` 分，最终成功的概率；`x ≥ K` 停牌，`≤ N` 为 1，否则 0',
              '`x < K`：等概率抽 `1..W`，`f[x]` 是后面 `W` 项的平均数',
              '写出 `f[x+1]` 再相减，中间项全抵消，只剩 `f[x]`、`f[x+1]`、`f[x+W+1]`',
              '`x = K−1` 时 `f[K]` 不符合上式，要按定义直接数'],
        summary=['时间 `O(K+W)`，空间 `O(K+W)`（记忆化数组 + 递归栈）',
                 '易错：`x = K−1` 要单独算；数组大小 `K+W` 才不越界',
                 '这里用记忆化递归，同一层里重复调用 `dfs(now+1)` 靠 `f` 缓存，不会重复计算',
                 '原文为 Python 2 风格，但除法都已是浮点（`1.0`），语法在 Python 3 下可直接运行，代码未改动',
                 '对比灵神：灵神倒序递推 + 定长滑窗维护窗口和；yiduobo 用差分直接化简成 O(1) 递推'],
    ),
)

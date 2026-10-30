def _sieve(S):
    f = S.get('f')
    n = S.get('n')
    return f[:n + 1] if f is not None and n else [0]


def _col(S, i, v):
    if S.get('p') is None or S.get('q') is None:
        return 'green' if v is True and i >= 2 else ('red' if v is False and i >= 1 else None)
    return 'green' if v is True and i >= 2 else ('red' if v is False and i >= 1 else None)


def _info(S):
    n = S.get('n')
    if S.get('res') is not None:
        return f"p = {S['p']} 个质数位置，q = {S['q']} 个合数位置：`{S['p']}! × {S['q']}!` ，当前 res = =={S['res']}=="
    if S.get('p') is not None:
        return f"已数出：质数 p = =={S['p']}==，非质数 q = =={S['q']}=="
    if S.get('now') is not None:
        return f"筛法：绿 = 质数候选，红 = 已被划掉的合数（1 也不是质数）"
    return ''


CONFIG = dict(
    num=1175, title='质数排列', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='筛质数 + 阶乘相乘',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numPrimeArrangements(self, n):

        f = [True] * 101
        f[1] = False
        now = 2
        while now * now <= n:
            tmp = now + now
            while tmp <= n:
                f[tmp] = False
                tmp += now
            
            now += 1
        
        p = q = 0
        for index in range(1, n + 1):
            if f[index]:
                p += 1
            else:
                q += 1

        now = 1
        res = 1
        mod = 10 ** 9 + 7
        for index in range(2, max(p, q) + 1):
            now = now * index % mod
            if index == p:
                res = res * now % mod
            if index == q:
                res = res * now % mod
        
        return res
''',
    call='Solution().numPrimeArrangements(10)',
    expect=17280,
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='array', var=_sieve, pointers={'now': 'blue', 'tmp': 'pink', 'index': 'yellow'},
             color=_col, h=300, label='f[i]：i 是不是质数'),
        dict(type='text', fn=lambda S: (f"阶乘 `now = {S['now']}` = {S['index']}!" if S.get('res') is not None and S.get('index') else ''), h=60),
    ],
    watch=['now', 'tmp', 'p', 'q', 'index', ('res', 'res', 'green')],
    captions={
        'f = [True]': '先假设 1 到 100 全是质数，`f[i] = True` 表示 i 还可能是质数',
        'f[1] = False': '1 不是质数，先划掉',
        'while now * now <= n': lambda S, B, r: (f'`{S.now}×{S.now} = {S.now*S.now} <= {S.n}`：还要用 `{S.now}` 去划它的倍数' if S.now * S.now <= S.n else f'`{S.now}×{S.now} > {S.n}`：更大的数不会再划掉新合数，筛完'),
        'tmp = now + now': '从 `{now}` 的 2 倍开始：`tmp = {tmp}`',
        'while tmp <= n': lambda S, B, r: (f'`tmp = {S.tmp} <= {S.n}`，还在范围内' if S.tmp <= S.n else f'`tmp = {S.tmp} > {S.n}`，`{S.now}` 的倍数划完'),
        'f[tmp] = False': '`{tmp}` 是 `{now}` 的倍数 → ==合数==，划掉',
        'tmp += now': '下一个倍数：`tmp = {tmp}`',
        'now += 1': '换下一个 `now = {now}`',
        'p = q = 0': '`p` 数质数，`q` 数非质数，都从 0 开始',
        'for index in range(1, n + 1)': '扫描 1..n，数每个数是质数还是合数',
        'if f[index]': lambda S, B, r: (f'`f[{S.index}]` 为真：{S.index} 是==质数==' if S.f[S.index] else f'`f[{S.index}]` 为假：{S.index} 不是质数'),
        'p += 1': '质数个数 `p = {p}`',
        'q += 1': '非质数个数 `q = {q}`',
        'now = 1': '开始算阶乘：`now` 表示当前的 `index!`',
        'res = 1': '`res` 存答案 = `p! × q!`',
        'mod = 10': '结果要对 `10^9 + 7` 取模',
        'for index in range(2, max(p, q) + 1)': '`index` 从 2 到 max(p, q)：一趟同时拿到 p! 和 q!',
        'now = now * index % mod': '`now = {B.now} × {index}` → =={now}== 即 `{index}!`',
        'if index == p': '`index == p`：此刻 `now` 恰好是 `p!`，乘进答案',
        'if index == q': '`index == q`：此刻 `now` 恰好是 `q!`，乘进答案',
        'res = res * now % mod': '`res` = `{B.res} × {now}` = =={res}==',
        'return res': lambda S, B, r: f'质数放质数位置 `{S.p}!`，合数放合数位置 `{S.q}!`，相乘得 {r}',
    },
    cards=dict(
        one_liner='质数只能放在质数下标，合数放合数下标：p! × (n−p)!',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['把 `1..n` 排成排列，要求质数必须放在质数下标（下标从 1 起）上',
                 '求这样的排列有多少种，答案对 `10^9 + 7` 取模',
                 '示例：`n = 5` → `12`；本视频：`n = 10` → `17280`'],
        quote='设1-n中一共有p个质数，那么合数的数量为n - p。这p个质数可以在p个质数索引上任意放置，因此一共有p！种放置方法。',
        quote_src='—— yiduobo 题解原文',
        idea=['质数只能互相换位置：`p!` 种；其余数只能在合数位置里排：`(n−p)!` 种',
              '两部分互不影响，答案 = ==`p! × (n−p)!`==',
              '所以先用筛法数出 `p`，再求阶乘'],
        summary=['时间 `O(n log log n)`（筛法），空间 `O(n)`',
                 '1 不是质数，要单独设为 False',
                 '一次循环同时拿到 `p!` 和 `q!`：到 `index == p` 或 `q` 时乘进答案；p = q 时乘两次',
                 '原文数组固定开 101，因为 `n <= 100`'],
    ),
)

def _txt(S):
    if 'res' not in S or 'k' not in S:
        return '`f[i]`：i 个数交替排列的方案数'
    return f'还要跳过的名次 `k = {S["k"]}`；已填 `res = {S["res"]}`'


def _col(S, i, v):
    x = S.get('x')
    if x is not None and i == x and S.get('_line', 0) in (18, 19, 20, 21, 22, 36, 37, 38, 39, 40):
        return 'yellow'
    return None


CONFIG = dict(
    num=3470, title='全排列 IV', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='康托展开式逐位填充',
    tags=['组合数学', '难度分 2474'],
    code='''
class Solution(object):
    def permute(self, n, k):
        
        f = [1]
        for index in range(1, n + 1):
            f.append(f[-1] * ((index + 1) // 2))

        if n % 2 == 0:
            if f[-1] * 2 < k:
                return []
            step = 1
        else:
            if f[-1] < k:
                return []
            step = 2
        
        choose = None
        res = []
        used = [False] * (n + 1)
        for x in range(1, n + 1, step):
            if k > f[n - 1]:
                k -= f[n - 1]
            else:
                choose = x
                break
            
        res.append(choose)
        used[choose] = True

        for r in range(2, n):
            if res[-1] % 2 == 0:
                start = 1
            else:
                start = 2
            choose = None
            for x in range(start, n + 1, 2):
                if not used[x]:
                    if k > f[n - r]:
                        k -= f[n - r]
                    else:
                        choose = x
                        break
            
            res.append(choose)
            used[choose] = True
        
        for x in range(1, n + 1):
            if not used[x]:
                res.append(x)
                break
        
        return res
''',
    call='Solution().permute(5, 7)',
    expect=[3, 4, 1, 2, 5],
    skip=['f.append', 'for index in range', 'break', 'choose = None', 'step = ', 'if res[-1] % 2 == 0', 'start = ', 'used = [False]', 'res = []'],
    max_steps=70,
    views=[
        dict(type='array', var='f', label='f[i]：i 个数的交替排列数（奇数位、偶数位各自全排）', h=150, cell=80),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='used', label='used[x]：数字 x 是否已填（下标 0 不用）', h=170, cell=80,
             color=_col, dim=lambda S, i, v: i == 0),
        dict(type='array', var='res', label='res：已确定的前缀', h=150, cell=80),
    ],
    watch=[('x', 'x', 'pink'), ('k', 'k', 'yellow'), ('r', 'r', 'blue')],
    captions={
        'f.append': '`f[{index}] = {f[-1]}`',
        'if f[-1] * 2 < k': '偶数长度开头奇偶皆可，总数 `f[n] × 2` 不到 `k` → 空',
        'if f[-1] < k': lambda S, B, r: (f'`f[{S.n}] = {S.f[-1]}` ≥ `k = {S.k}`，奇数长度只能奇数开头 → 有解' if S.f[-1] >= S.k
                                          else '总数不够 `k` → 返回空数组'),
        'return []': '不够 `k` 个 → 空数组',
        'for x in range(1, n + 1, step)': '枚举第一位：奇数长度只能填奇数（步长 2）',
        'if k > f[n - 1]': lambda S, B, r: (f'`k = {S.k} > f[{S.n - 1}] = {S.f[S.n - 1]}`：以 `{S.x}` 开头的方案全在第 k 名前面 → 跳过' if S.k > S.f[S.n - 1]
                                             else f'`k = {S.k} ≤ f[{S.n - 1}] = {S.f[S.n - 1]}`：第 k 名就在以 `{S.x}` 开头的这一组里'),
        'k -= f[n - 1]': '跳过整组：`k` 减去 `{f[n - 1]}` → =={k}==',
        24: '第一位 = =={x}==',
        41: '这一位 = =={x}==',
        'res.append(choose)': lambda S, B, r: f'确定 `{S.choose}`，`res` = {S.res}',
        'used[choose] = True': '标记 `{choose}` 已用',
        'for r in range(2, n)': lambda S, B, r: (f'填第 `{S.r}` 位（前面一位是{"偶" if S.res[-1] % 2 == 0 else "奇"}数，这一位必须是{"奇" if S.res[-1] % 2 == 0 else "偶"}数）' if S.r != B.get('r') or 'r' not in B else '前 n−1 位都定了，最后一位只剩一个数'),
        'for x in range(start': '从小到大枚举同奇偶性、未用的数 `x`',
        'if not used[x]': lambda S, B, r: (f'`{S.x}` 还没用 → 作为候选' if not S.used[S.x] else f'`{S.x}` 已经用过，换下一个'),
        'if k > f[n - r]': lambda S, B, r: (f'`k = {S.k} > f[{S.n - S.r}] = {S.f[S.n - S.r]}`：以 `{S.x}` 开头的方案都排在前面 → 跳过' if S.k > S.f[S.n - S.r]
                                             else f'`k = {S.k} ≤ f[{S.n - S.r}] = {S.f[S.n - S.r]}`：第 k 名就在这一组 → 选 `{S.x}`'),
        'k -= f[n - r]': '跳过整组：`k` 减去 `{f[n - r]}` → =={k}==',
        47: lambda S, B, r: ('最后一位：从 1 开始找唯一没用过的数' if S.x == 1 else f'检查 `{S.x}`'),
        'return res': '答案 =={ret}==',
    },
    cards=dict(
        one_liner='逐位填充：整组整组地跳过，`k` 落在哪组就选谁',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['交替排列：前 `n` 个正整数的排列，相邻两数奇偶性不同',
                 '求字典序第 `k` 个，不存在返回空数组',
                 '本视频：`n = 5, k = 7` → `[3,4,1,2,5]`'],
        quote='对于这类计算排列第k大的问题，一种常见的处理方法是利用康拓展开，具体做法可以理解成从高位到低位逐位进行填充……若这个排列数大于等于k，说明当前为就应该填充当前枚举到的元素……反之，说明当前填充的元素过小，需要尝试下一个元素，同时将k减去之前计算出的排列数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i] = f[i-1] × ceil(i/2)`：剩 i 位时，奇、偶两类数各自全排',
              '每一位按从小到大试：`k > f[…]` 就整组跳过并 `k -= f[…]`，否则选它',
              '奇数长度第一位只能是奇数（步长 2），之后每位奇偶由前一位决定'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '原文本来就是 Python 3 也能运行的写法，代码未改动',
                 '易错：偶数 n 时总方案数是 `f[n] × 2`，第一位步长为 1',
                 '最后一位无需枚举，剩下那个数字直接放',
                 '对比灵神：灵神用 `divmod` 一步算出组号，这里是逐个减'],
    ),
)

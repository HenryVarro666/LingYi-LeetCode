N = 3


def _bits(s, n=N):
    return '{' + ', '.join(str(j + 1) for j in range(n) if s >> j & 1) + '}'


def _color(S, k, v):
    inner = S.get('_inner', {})
    now = inner.get('now')
    if now is not None and k == now:
        return 'yellow'
    return None


def _txt(S):
    inner = S.get('_inner', {})
    now = inner.get('now')
    if now is None:
        return '`f[now]` = 剩下的数为 `now` 时可行的排列数；`now` 的第 `num-1` 位为 1 表示数字 `num` 还没用'
    rn = inner.get('rest_num')
    if rn is None:
        return f'`now = {now:0{N}b}` = =={_bits(now)}==：从最后一位往前填'
    k = len(rn)
    return f'剩下 {sorted(rn)}，共 `k = {k}` 个 → 要填排列的第 ==`{k}`== 位'


def _cap_if(S, B, ret):
    k = len(S.rest_num)
    num = S.num
    if k % num == 0 or num % k == 0:
        return f'`{k} % {num} = {k % num}`，`{num} % {k} = {num % k}`：整除 → ==能把 {num} 放在第 {k} 位=='
    return f'`{k}` 与 `{num}` 互不整除 → 不能放第 {k} 位'


CONFIG = dict(
    num=526, title='优美的排列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状压 DP · 从最后一位往前选（记忆化）',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def countArrangement(self, N):

        f = [None] * (1 << N)
        return self.dfs((1 << N) - 1, N, f)

    def dfs(self, now, N, f):
        if f[now] is not None:
            return f[now]
        if now == 0:
            f[now] = 1
            return 1

        rest_num = set()
        for num in range(N):
            if now & (1 << num):
                rest_num.add(num + 1)
        
        f[now] = 0
        for num in rest_num:
            if len(rest_num) % num == 0 or num % len(rest_num) == 0:
                f[now] += self.dfs(now - (1 << num - 1), N, f)
        
        return f[now]
''',
    call=f'Solution().countArrangement({N})',
    expect=3,
    max_steps=110,
    skip=['f = [None]', 'for num in range(N)', 'rest_num = set()', 'rest_num.add', 'if now & (1 << num)'],
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var=lambda S: S['_inner'].get('f') or S.get('f'), label='f[now]（下标 = 剩下数字集合的二进制，黄 = 当前 now，空 = 还没算）',
             cell=64, h=170, color=_color),
        dict(type='calls', h=300, hide=('f',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'yellow'),
           ('rest_num', lambda S: sorted(S['_inner']['rest_num']) if 'rest_num' in S['_inner'] else None, 'blue'),
           ('num', lambda S: S['_inner'].get('num'), 'pink')],
    captions={
        'return self.dfs((1 << N) - 1': '从全集 `now = {(1 << N) - 1}` 出发：所有数都还没用',
        'if f[now] is not None': lambda S, B, r: (f'`f[{S.now}] = {S.f[S.now]}` 算过了 → ==直接返回备忘录=='
                                                  if S.f[S.now] is not None else f'`f[{S.now}]` 还没算 → 往下算'),
        'if now == 0': lambda S, B, r: ('没有数可放了：恰好构成一个排列，`f[0] = 1`' if S.now == 0
                                        else f'`now = {S.now}` 还有数没放，继续'),
        'f[now] = 0': '`f[{now}]` 先清零，下面把各种放法累加进来',
        'for num in rest_num': lambda S, B, r: (f'枚举还没用的数：试着把 `{S.num}` 放在第 `{len(S.rest_num)}` 位'
                                                if S.get('_inner', {}).get('num') in S.rest_num else '枚举完了'),
        'if len(rest_num) % num': _cap_if,
        'f[now] += self.dfs': '把 `{num}` 放在第 `{len(rest_num)}` 位 → 子问题 `now - 2^({num}-1)`（去掉 {num}）',
        'return f[now]': '`f[{now}]` = =={ret}==',
    },
    cards=dict(
        one_liner='n ≤ 15，用二进制表示还剩哪些数；从最后一位往前选',
        complexity='时间 `O(n·2^n)`，空间 `O(2^n)`',
        problem=['`1..n` 的排列 `perm`，每个位置满足 `perm[i] % i == 0` 或 `i % perm[i] == 0` 就是优美排列',
                 '求优美排列的个数，`n ≤ 15`',
                 '示例：`n = 2` → `2`；本视频：`n = 3` → `3`'],
        quote='看到排列和n小于等于15，立马就想到了状态压缩动态规划。使用1 << (num - 1)来表示数字num……',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[now]`：剩下的数是 `now` 时的排列数；剩 `k` 个数，就是要填第 `k` 位',
              '从这 `k` 个数里选 `num` 放在第 `k` 位，要求 `k % num == 0` 或 `num % k == 0`',
              '`f[now] = Σ f[去掉 num 后]`，`f[全集]` 就是答案；这里用记忆化搜索写'],
        summary=['时间 `O(n·2^n)`，空间 `O(2^n)`',
                 '先用 `rest_num` 数出还剩几个数，再枚举其中的 `num`',
                 '`f` 初值用 `None` 区分“没算过”和“算出来是 0”',
                 '原文已是 Python 3 可运行，无需修改（文档字符串本就没有）',
                 '对比灵神：灵神用 `bit_count` 和递推（也有 `@cache`），yiduobo 用集合统计剩余数'],
    ),
)

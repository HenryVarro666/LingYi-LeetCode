def _f(S):
    inn = S.get('_inner') or S
    f = S.get('f')
    if f is None:
        return [[]]
    return [['-' if x is None else ('赢' if x else '输') for x in f]]


def _cur(S):
    inn = S.get('_inner') or {}
    return inn.get('now')


def _color(S, r, c, v):
    now = _cur(S)
    if now is None:
        return None
    if c == now:
        return 'yellow'
    return 'green' if v == '赢' else ('pink' if v == '输' else None)


def _info(S):
    inn = S.get('_inner') or {}
    M = S.get('maxChoosableInteger')
    now = inn.get('now')
    if now is None or M is None:
        return '`f[now]`：已选数字集合 `now` 时，轮到的人能不能赢（二进制第 k 位 = 数字 k+1 被选过）'
    chosen = [k + 1 for k in range(M) if now >> k & 1]
    s = f' = {"+".join(map(str, chosen))}' if chosen else ''
    return f'`now = {now:0{M}b}`：已选 `{chosen}`，累计 =={sum(chosen)}=={s}，目标 `{S["desiredTotal"]}`'


def _cap_rec(S, B, ret):
    return f'选数字 `{S.num + 1}` → 状态变成 `{S.now + (1 << S.num):0{S.maxChoosableInteger}b}`，看对手在那个状态能不能赢'


CONFIG = dict(
    num=464, title='我能赢吗', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状压 DP（记忆化博弈）',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def canIWin(self, maxChoosableInteger, desiredTotal):

        if desiredTotal == 0:
            return True
        if (1 + maxChoosableInteger) * maxChoosableInteger // 2 < desiredTotal:
            return False

        f = [None] * (1 << maxChoosableInteger)
        return self.dfs(0, maxChoosableInteger, desiredTotal, f)

    def dfs(self, now, maxChoosableInteger, desiredTotal, f):
        if f[now] is not None:
            return f[now]
        unused_set = set()
        sum_now = 0
        for num in range(maxChoosableInteger):
            if now & (1 << num):
                sum_now += num + 1
            else:
                unused_set.add(num)

        if sum_now >= desiredTotal:
            f[now] = False
            return False

        for num in unused_set:
            if not self.dfs(now + (1 << num), maxChoosableInteger, desiredTotal, f):
                f[now] = True
                return True

        f[now] = False
        return False
''',
    call='Solution().canIWin(3, 4)',
    expect=False,
    skip=['for num in range(maxChoosableInteger)', 'if now & (1 << num)', 'sum_now += num + 1', 'unused_set.add', 'else:', 'f[now] = False', 'f[now] = True',
          'unused_set = set()', 'sum_now = 0'],
    max_steps=60,
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='table', var=_f, label='f[now]：这个状态下，轮到的人能赢吗（黄 = 当前状态，绿 = 赢，红 = 输）', h=230, cell=100,
             rows=['f'], cols=lambda S: [f'{k:0{S["maxChoosableInteger"]}b}' for k in range(1 << S['maxChoosableInteger'])], color=_color),
        dict(type='calls', h=330, hide=('f', 'maxChoosableInteger', 'desiredTotal')),
    ],
    watch=[('now', 'now', 'yellow'), ('sum_now', 'sum_now', 'cyan'), ('unused_set', 'unused_set', 'blue'), ('num', 'num', 'pink')],
    captions={
        'if desiredTotal == 0': '目标和为 0：先手什么都不用选，已经达到 → ==直接赢==；否则继续',
        '(1 + maxChoosableInteger)': '`1..{maxChoosableInteger}` 全选的和是 `{(1 + maxChoosableInteger) * maxChoosableInteger // 2}`，不到 `{desiredTotal}` 就谁也赢不了 → 先手输',
        'f = [None]': '`f[now]`：最多 20 个数 → 用 `{1 << maxChoosableInteger}` 个状态记忆，`None` = 还没算',
        'return self.dfs(0': '从「谁都没选」的状态 `now = 0` 开始搜索',
        'if f[now] is not None': lambda S, B, r: (f'`f[{S.now}]` 已经算过：{"赢" if S.f[S.now] else "输"} → 直接返回，不再重复搜索' if S.f[S.now] is not None
                                                 else f'状态 `{S.now:0{S.maxChoosableInteger}b}` 第一次来，需要展开'),
        'if sum_now >= desiredTotal': lambda S, B, r: (f'已选累计 `{S.sum_now}` ≥ `{S.desiredTotal}`：==上一个人已经达标，轮到的人输了==' if S.sum_now >= S.desiredTotal
                                                       else f'累计 `{S.sum_now}` < `{S.desiredTotal}`，游戏还没结束，枚举没选过的数 `{sorted(S.unused_set)}`'),
        'if not self.dfs(': '选数字 `{B.num + 1}`：进入新状态 `{B.now + (1 << B.num):0{B.maxChoosableInteger}b}`，看对手在那里能不能赢（对手输了我就赢）',
        'for num in unused_set': lambda S, B, r: (f'试着选没选过的数字 `{S.num + 1}`' if S.get('num') != B.get('num')
                                                  else '没选过的数都试完了，没有一个能让对手输'),
        'return True': '对手输了：找到必胜选择 → `f[{now}] = True`（赢），不用再试其它数',
        'return False': lambda S, B, r: (f'累计已达标，上一个人赢了 → `f[{S.now}] = False`（输）' if S.sum_now >= S.desiredTotal
                                         else f'所有选择都会让对手赢 → `f[{S.now}] = False`（输）'),
    },
    cards=dict(
        one_liner='数字最多 20 个，选没选过用一位二进制表示，记忆化博弈',
        complexity='时间 `O(2^n · n)`，空间 `O(2^n)`',
        problem=['两人轮流从 `1~maxChoosableInteger` 里选一个数，==不能重复选==，累计和先达到 `desiredTotal` 的人赢',
                 '问先手能否必胜（两人都按最优策略）',
                 '本视频：`maxChoosableInteger = 3, desiredTotal = 4` → `False`'],
        quote='注意到题目保证可选的数最多不超过20，那么如果将每个数选或者没选按照01进行编码，那么20个数最多有2^20 = 1048576种状态，于是可以在这上面进行状态压缩动态规划。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：状态为 `i` 时，轮到的人能不能赢',
              '选 `x` 后状态变成 `i + (1<<x)`；只要有一个 `x` 使 `f[新状态]` 为 False，当前就是必胜',
              '找不到这样的 `x` → 必败；先特判目标和为 0，以及全选都凑不到目标'],
        summary=['时间 `O(2^n · n)`，空间 `O(2^n)`',
                 '易错：目标和 `desiredTotal == 0` 先手直接赢；全部数加起来都不够则先手输',
                 '`sum_now >= desiredTotal` 说明==上一个人==已经赢了，所以当前状态为输',
                 '原文为 Python 2 写法，整数除法 `/ 2` 已改为 `// 2`'],
    ),
)

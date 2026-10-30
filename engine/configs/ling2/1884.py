N = 10


def _f_table(m):
    f = [0] * (m + 1)
    for i in range(1, m + 1):
        f[i] = min(max(j, f[i - j] + 1) for j in range(1, i + 1))
    return f


F = _f_table(N)  # 只用于画图：dfs(0..N) 的值


def _cur(S):
    return S.get('i')


def _known(S):
    """到这一步为止已经算出来（存进 @cache）的 dfs 值"""
    i = _cur(S)
    if i is None:
        return set()
    ks = set(range(i))
    if (S.get('_line') == RET_LINE and i >= 2) or S.get('_line') == RET0_LINE:
        ks.add(i)
    return ks


def _table(S):
    ks = _known(S)
    return [list(range(N + 1)), [F[i] if i in ks else None for i in range(N + 1)]]


def _table_color(S, r, c, v):
    i = _cur(S)
    if r == 1 and i is not None and S.get('_line') == RET_LINE and i >= 2 and 1 <= i - c <= i:
        return 'purple'  # 被枚举到的 dfs(i - j)
    if c == i:
        return 'yellow'
    return None


def _cands(S):
    i = _cur(S)
    if i is None or i < 2 or S.get('_line') != RET_LINE:
        return None
    return [list(range(1, i + 1)), [max(j, F[i - j] + 1) for j in range(1, i + 1)]]


def _cand_color(S, r, c, v):
    cs = _cands(S)
    if not cs:
        return None
    best = min(cs[1])
    return 'green' if cs[1][c] == best else None


def _text(S):
    i = _cur(S)
    if i is None:
        return ''
    if S.get('_line') == RET_LINE and i >= 2:
        cs = [max(j, F[i - j] + 1) for j in range(1, i + 1)]
        bj = cs.index(min(cs)) + 1
        return (f'第一枚蛋在 `j = {bj}` 层扔：碎了再试 `{bj - 1}` 次，共 `{bj}` 次；'
                f'没碎变成 `dfs({i - bj}) + 1 = {F[i - bj] + 1}` → 取 `max` = =={min(cs)}==')
    return f'`dfs(i) = min(max(j, dfs(i−j)+1))`，`j = 1…i`'


def _if_cap(S, B, ret):
    i = S.i
    if i == 0:
        return '`i = 0`：没有楼层，`f` 一定是 0 → 递归边界'
    return f'询问 `n = {S.n}` → `dfs({i})`：{i} 层楼，枚举第一枚蛋在第 `j` 层扔'


def _ret_cap(S, B, ret):
    i = B.i
    if ret is None:
        return f'`dfs({i})` 要用到 `dfs(0)`，它还没算过 → 递归进去'
    cs = [max(j, F[i - j] + 1) for j in range(1, i + 1)]
    bj = [str(j + 1) for j, c in enumerate(cs) if c == ret]
    where = f'`j = {bj[0]}` 时' if len(bj) == 1 else f'`j = {", ".join(bj)}` 都能'
    return f'子问题都已在缓存里：{where}取到最小 → `dfs({i})` = =={ret}=='


CODE = '''
@cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
def dfs(i: int) -> int:
    if i == 0:
        return 0
    return min(max(j, dfs(i - j) + 1) for j in range(1, i + 1))

class Solution:
    def twoEggDrop(self, n: int) -> int:
        return dfs(n)
'''
_LINES = CODE.strip('\n').split('\n')
RET_LINE = next(k + 1 for k, l in enumerate(_LINES) if 'return min(' in l)
RET0_LINE = next(k + 1 for k, l in enumerate(_LINES) if 'return 0' in l)

CONFIG = dict(
    num=1884, title='鸡蛋掉落-两枚鸡蛋', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索（@cache）',
    tags=['字节30天'],
    code=CODE,
    call=f'[Solution().twoEggDrop(n) for n in range(1, {N + 1})]',
    expect=[1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
    views=[
        dict(type='text', fn=lambda S: (f"依次询问 `n = 1, 2, …, {N}`（多组数据共享同一个 `@cache`），当前 `n = {S['n']}`"
                                        if 'n' in S else ''), size=24, h=56),
        dict(type='grid', var=_table, label='dfs(i) 的值（已存进缓存的才显示；黄 = 当前 i，紫 = 本次用到的子问题）',
             rows=['i', 'dfs'], cell=80, h=230, color=_table_color),
        dict(type='grid', var=_cands, label='第一枚蛋在第 j 层扔 → 最坏操作次数 max(j, dfs(i−j)+1)（绿 = 最小）',
             rows=['j', '次数'], cell=80, h=230, color=_cand_color),
        dict(type='text', fn=_text, size=25, h=90, lines=2),
    ],
    watch=[('n', 'n'), ('i', 'i', 'yellow')],
    skip=['return dfs(n)'],
    captions={
        'if i == 0': _if_cap,
        'return 0': '`dfs(0) = 0`，存进缓存',
        'return min(': _ret_cap,
    },
    cards=dict(
        one_liner='dfs(i) = 枚举第一枚蛋扔在第 j 层，碎与不碎取最坏，再对 j 取最好',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['两枚相同的鸡蛋，`n` 层楼；存在楼层 `f`：高于 `f` 扔下会碎，不高于则不碎',
                 '每次可以扔一枚没碎的蛋，求==确定 f 的最少操作次数==（最坏情况）',
                 '示例：`n = 2` → `2`；`n = 100` → `14`'],
        quote='这两种情况取最大值，因为在扔之前，我们不知道鸡蛋是否会碎。==为了保证无论在何种情况下，我们都可以确定 f 的值，所以要取最大值。==',
        quote_src='—— 灵茶山艾府题解（方法一：动态规划）',
        idea=['第一枚蛋在第 `j` 层扔：碎了 → 第二枚从 1 楼逐层试，共 `j` 次；没碎 → `dfs(i−j) + 1`',
              '两种情况取 `max`，再对 `j = 1…i` 取 `min`：`dfs(i) = min(max(j, dfs(i−j)+1))`',
              '边界 `dfs(0) = 0`；`@cache` 记忆化，每个状态只算一次'],
        result=f'`[dfs(1), …, dfs({N})] = {F[1:]}`：答案为 1 的 1 个，为 2 的 2 个，为 3 的 3 个……',
        after=[dict(heading='方法二：数学', lines=[
            '反过来：如果只能扔 `x` 次，第一次最高只能在 `x` 楼扔（碎了还要试 `x−1` 次）',
            '没碎再往上 `x−1` 层、`x−2` 层…… → `n` 最大是 `x + (x−1) + … + 1`',
            '`x(x+1)/2 ≥ n` → `x = ceil((sqrt(8n+1) − 1) / 2)`，即 `ceil(sqrt(n*8+1)) // 2`'])],
        summary=['记忆化搜索 `O(n²)`：`n` 个状态，每个枚举 `O(n)` 个 `j`',
                 '递归边界 `dfs(0) = 0`；把 `dfs` 写在类外，多组数据共享缓存',
                 '可 1:1 翻译成递推 `f[i] = min(max(j, f[i−j]+1))`',
                 '数学法 `O(1)`；`k` 枚鸡蛋见 887. 鸡蛋掉落'],
    ),
)

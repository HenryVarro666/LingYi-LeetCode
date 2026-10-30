import math
T = 'AABC'
CB = math.comb


def _src(S):
    return S['j'] - S['k'] if 'k' in S and S.get('_line') in (9, 10) else None


def _formula(S):
    if 'k' not in S or S.get('_line') not in (9, 10):
        return '`f[j]` = 已处理的字母种类能拼出的长为 `j` 的序列数；`f[0] = 1`（空序列）'
    j, k = S['j'], S['k']
    return f'`f[{j}] += f[{j-k}] × C({j},{k})` ：从 `{j}` 个位置里选 `{k}` 个放本种字母'


def _cap(S, B, ret):
    j, k = S['j'], S['k']
    return (f'本种字母选 `{k}` 个：在 `{j}` 个位置里挑 `{k}` 个放它，有 `C({j},{k}) = {math.comb(j, k)}` 种；'
            f'剩下 `{j-k}` 个位置用前面的字母拼，`f[{j-k}] = {B.f[j-k]}` → `f[{j}]` = =={S["f"][j]}==')


CONFIG = dict(
    num=1079, title='活字印刷', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='分组背包式计数 DP · 组合数',
    tags=['难度分 1741'],
    code='''
class Solution:
    def numTilePossibilities(self, tiles: str) -> int:
        f = [1] + [0] * len(tiles)
        n = 0
        for cnt in Counter(tiles).values():  # 枚举第 i 种字母
            n += cnt  # 常数优化：相比从 len(tiles) 开始要更快
            for j in range(n, 0, -1):  # 枚举序列长度 j
                # 枚举第 i 种字母选了 k 个，注意 k=0 时的方案数已经在 f[j] 中了
                for k in range(1, min(j, cnt) + 1):
                    f[j] += f[j - k] * comb(j, k)  # comb 也可以预处理，见其它语言的实现
        return sum(f[1:])
''',
    call=f'Solution().numTilePossibilities({T!r})',
    expect=34,
    setup='from math import comb',
    skip=['for k in range', 'for j in range'],
    views=[
        dict(type='string', var='tiles', label='tiles', cell=70, h=120),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='array', var='f', label='f[j]：长为 j 的序列数（粉 = 正在更新，蓝 = 它依赖的 f[j-k]）', cell=84, h=210,
             pointers={'j': 'pink', _src: 'blue'}, pointer_labels={_src: 'j-k'},
             color=lambda S, i, v: ('pink' if i == S.get('j') else 'blue' if i == _src(S) else None) if 'j' in S else None),
        dict(type='text', fn=lambda S: f"已处理 `n = {S['n']}` 个字母的容量；本种字母出现 `cnt = {S['cnt']}` 次" if 'cnt' in S else '', size=24, h=60),
    ],
    watch=[('cnt', 'cnt', 'blue'), ('n', 'n'), ('j', 'j', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'f = [1] + [0]': '`f[0] = 1`：空序列有 1 种；其余长度先是 0。`f` 长 `{len(f)}`',
        'for cnt in Counter': '加入下一种字母，它有 `{cnt}` 个（相同字母不区分）',
        'n += cnt': '前面所有字母加起来最长 `{n}`，`j` 只需从 `{n}` 开始，更大的状态没意义',
        'f[j] += f[j - k]': _cap,
        'return': '长度 1..n 的方案数全加起来（不含空序列）= =={ret}==',
    },
    cards=dict(
        one_liner='相同字母只算一种：选 k 个位置放它，剩下的子问题更小',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`tiles` 是若干字母字模，每个只能用一次，求能印出的==非空==字母序列数',
                 '相同字母的字模不区分，例如 `"AAB"` → `8`',
                 '本视频演示 `tiles = "AABC"`'],
        quote='这等价于在 5 个位置中选 2 个位置放 C，其余位置放 AAB。……剩余要解决的问题为，用 AAB 构造长为 3 的序列的数目。这是一个与原问题相似，且规模更小的子问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]` = 前 `i` 种字母构造长为 `j` 的序列数，第 `i` 种选 `k` 个：`f[i-1][j-k] × C(j, k)`',
              '和 0-1 背包一样去掉第一维：`j` ==倒序==遍历，旧值才不会被提前覆盖',
              '`k` 从 1 开始，因为 `k = 0` 的方案已经在 `f[j]` 里'],
        summary=['时间 `O(n^2)`：固定 `j` 时内层循环总次数约等于字母总数',
                 '易错：`j` 必须倒序；答案要 `sum(f[1:])`，去掉空序列',
                 '题解先给了二维版本 `f[i][j]`，上面是空间优化后的一维版本',
                 '`comb` 需要 Python 3.8+，也可预处理杨辉三角'],
    ),
)

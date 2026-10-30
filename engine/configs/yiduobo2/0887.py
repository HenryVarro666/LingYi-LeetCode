K, N = 3, 6


def _vals(S):
    flag, j, now, f = S.get('flag'), S.get('j'), S.get('now'), S.get('f')
    if None in (flag, j, now, f) or now > j:
        return None
    return f[flag ^ 1][now - 1], f[flag][j - now]


def _gcolor(S, r, c, v):
    flag, j, now = S.get('flag'), S.get('j'), S.get('now')
    if flag is None or j is None or now is None or S.get('_line') not in (10, 11, 12):
        return None
    if (r, c) == (flag, j) and S.get('_line') == 12:
        return 'yellow'
    if (r, c) == (flag ^ 1, now - 1):
        return 'pink'
    if (r, c) == (flag, j - now):
        return 'blue'
    return None


def _rows(S):
    flag, i = S.get('flag'), S.get('i')
    if flag is None:
        return ['f[0]', 'f[1]']
    eggs_cur = (i + 1) if i is not None else 1
    out = ['', '']
    out[flag] = f'{eggs_cur}蛋'
    out[flag ^ 1] = f'{eggs_cur - 1}蛋' if i is not None else ''
    return out


def _info(S):
    v = _vals(S)
    if v is None or S.get('_line') not in (10, 11, 12):
        if S.get('flag') is not None and S.get('i') is not None:
            return f'当前算 `{S["i"] + 1}` 颗蛋（写在 `f[{S["flag"]}]`），上一行 `f[{S["flag"] ^ 1}]` 是 `{S["i"]}` 颗蛋'
        return '`f[i][j]`：i 颗蛋、j 层楼，最坏情况下最少要试几次（两行滚动数组）'
    a, b = v
    return (f'在第 `now = {S["now"]}` 层扔：碎了 → ==粉== `f[上一行][{S["now"] - 1}] = {a}`，'
            f'没碎 → ==蓝== `f[本行][{S["j"] - S["now"]}] = {b}`')


def _cap_while(S, B, ret):
    flag, j, now, f = B.flag, B.j, B.now, B.f
    if now >= j:
        return f'`now = {now}` 已经等于 `j`，不能再往上了 → 决策点就是 `{now}`'
    cur = max(f[flag ^ 1][now - 1], f[flag][j - now])
    nxt = max(f[flag ^ 1][now], f[flag][j - now - 1])
    if cur >= nxt:
        return f'在 `{now}` 层扔最坏 `{cur}`，在 `{now + 1}` 层扔最坏 `{nxt}` → ==不变差==，决策点右移'
    return f'在 `{now}` 层扔最坏 `{cur}`，在 `{now + 1}` 层扔最坏 `{nxt}` → 再往上就变差了，==停在 now = {now}=='


CONFIG = dict(
    num=887, title='鸡蛋掉落', difficulty='Hard', category='多维动态规划',
    author='yiduobo', technique='DP + 滚动数组 + 决策单调性',
    tags=['字节30天'],
    code='''
class Solution(object):
    def superEggDrop(self, K, N):
        f = [list(range(N + 1)), [0] * (N + 1)]
        flag = 0

        for i in range(1, K):
            flag ^= 1
            now = 1
            for j in range(1, N + 1):
                while now < j and max(f[flag ^ 1][now - 1], f[flag][j - now]) >= max(f[flag ^ 1][now], f[flag][j - now - 1]):
                    now += 1
                f[flag][j] = max(f[flag ^ 1][now - 1], f[flag][j - now]) + 1

        return f[flag][-1]
''',
    call=f'Solution().superEggDrop({K}, {N})',
    expect=3,
    skip=['for j in range'],
    views=[
        dict(type='text', h=96, size=24, fn=_info, lines=2),
        dict(type='grid', var='f', label='f 两行滚动（列 = 楼层 j，黄 = 正在算，右侧未算 = 旧值）', rows=_rows,
             cols=list(range(N + 1)), cell=96, h=300, color=_gcolor),
        dict(type='text', h=130, size=24, lines=3, fn=lambda S: (
            '转移：`f[i][j] = min over k of max(f[i−1][k−1], f[i][j−k]) + 1`'
            '　决策点 `now` 随 `j` 增大==只增不减==，所以均摊 `O(1)`')),
    ],
    watch=[('i', 'i'), ('flag', 'flag', 'cyan'), ('j', 'j', 'yellow'), ('now', 'now', 'pink')],
    captions={
        'f = [list(range(N + 1))': '`f[0][j] = j`：==1 颗蛋==只能从下往上一层层试；`f[1]` 先全 0',
        'flag = 0': '`flag` 指向当前蛋数那一行：现在 `f[0]` 表示 1 颗蛋',
        'for i in range(1, K)': lambda S, B, ret: (f'计算 `{S.i + 1}` 颗蛋：由 `{S.i}` 颗蛋那一行推出' if S.get('i') != B.get('i') or 'i' not in B
                                                   else '所有蛋数都算完了'),
        'flag ^= 1': '`flag ^= 1` → `{flag}`：新一行写在 `f[{flag}]`，上一行是 `f[{flag ^ 1}]`（==滚动数组==）',
        'now = 1': '决策点 `now`（第一次在几楼扔）从 1 开始',
        'while now < j and': _cap_while,
        'now += 1': '`now` → {now}：楼层变多，最优的扔蛋楼层==只会往上移==',
        'f[flag][j] = max(': lambda S, B, ret: (
            f'`f[{S.flag}][{S.j}]` = `max({S.f[S.flag ^ 1][S.now - 1]}, {S.f[S.flag][S.j - S.now]}) + 1` = =={S.f[S.flag][S.j]}==：'
            f'`{S.i + 1}` 颗蛋 `{S.j}` 层最少试 `{S.f[S.flag][S.j]}` 次'),
        'return f[flag][-1]': '返回 `f[flag][N] = {ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='f[蛋][楼] 取最坏情况的最小值，决策点随楼层单调右移',
        complexity='时间 `O(KN)`（决策点均摊 `O(1)`），空间 `O(N)`',
        problem=['`K` 枚相同的鸡蛋、`N` 层楼，存在 `F`：高于 `F` 层扔下会碎，否则不碎',
                 '碎了的蛋不能再用；求确定 `F` 的==最坏情况下的最小操作次数==',
                 f'示例：`K = 2, N = 6` → `3`；本视频 `K = {K}, N = {N}` → `3`'],
        quote='对于f[i][j]，我们可以从1到j - 1枚举当前在哪一楼进行尝试……f[i][j] = min(max(f[i - 1][k - 1], f[i][j - k]) + 1)……f[i][j +1]的决策点k\'必然大于等于f[i][j]的决策点k。',
        quote_src='—— yiduobo 题解',
        idea=['在第 k 层扔：碎了 → `i−1` 颗蛋查下面 `k−1` 层；没碎 → `i` 颗蛋查上面 `j−k` 层',
              '取两者较大（最坏），再对 k 取最小：朴素 `O(KN²)`',
              '优化：只依赖上一轮 → 滚动数组；`j` 增大时最优 `k` 不减 → 从上次的 `now` 接着找'],
        summary=['时间 `O(KN)`，空间 `O(N)`',
                 '易错：`max(碎, 没碎)` 先关于 k 递减后递增，要在==第一次变大时停下==',
                 '原文为 Python 2：`range(N + 1)` 在 Python 3 是不可写的 range 对象，已改为 `list(range(N + 1))`，删去 docstring',
                 '对比灵神：灵神反过来求“i 次操作 j 枚蛋能确定几层”，转移只需加法'],
    ),
)

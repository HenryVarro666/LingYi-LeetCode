TILES = [2, 3, 3, 3, 4]


def _st(S):
    return S['_inner'].get('state')


def _fcell(S, i, j, v):
    I, st = S['_inner'].get('i'), S['_inner'].get('state')
    if I is None:
        return None
    if i == I and j == st:
        return 'yellow'
    if i == I - 1 and 'last_state' in S['_inner'] and j == S['_inner']['last_state']:
        return 'blue'
    if i < I:
        return 'cyan' if v else None
    return None


def _txt(S):
    if 'cnt_info' not in S:
        return '先把牌按点数聚合：`(点数, 张数)`，再按点数从小到大排好'
    ci = S['cnt_info']
    base = '牌 `' + ' '.join(f'{t}×{c}' for t, c in ci) + '`'
    I = S['_inner'].get('i')
    st = S['_inner'].get('state')
    if I is not None and st is not None:
        base += f'　|　`i = {I}`（点数 {ci[I][0]}），`state = {st}`：以 {ci[I - 1][0]} 结尾的顺子 ==`{st // 3}`== 组，以 {ci[I][0]} 结尾的 ==`{st % 3}`== 组'
    return base


def _state_cap(S, B, r):
    if B.get('state') is not None and B.get('state') == S._inner.get('state'):
        return '9 个 `state` 都算完了'
    I, st, ci = S._inner.get('i'), S._inner.get('state'), S.cnt_info
    if I is None or st is None:
        return ''
    now, last = st % 3, st // 3
    cnt = ci[I][1]
    head = f'`state = {st}`：以 {ci[I - 1][0]} 结尾的顺子 {last} 组，以 {ci[I][0]} 结尾的 {now} 组'
    if now > cnt:
        return head + f' → 当前牌只有 {cnt} 张，凑不出 {now} 组，==无效=='
    if now + last > ci[I - 1][1]:
        return head + f' → 点数 {ci[I - 1][0]} 只有 {ci[I - 1][1]} 张，不够 {now}+{last} 个顺子用，==无效=='
    if now > 0 and (ci[I][0] != ci[I - 1][0] + 1 or ci[I - 1][0] != ci[I - 2][0] + 1):
        return head + ' → 三种牌点数不连续，==无效=='
    if all(two + last + now > ci[I - 2][1] for two in range(3)):
        return head + f' → 点数 {ci[I - 2][0]} 只有 {ci[I - 2][1]} 张，不够 {last}+{now} 个顺子用，==无效=='
    return head + ' → ==有效==，枚举以前两种牌结尾的顺子数'


CONFIG = dict(
    num='LCP 36', title='最多牌组数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状态压缩 DP（顺子数量三进制）',
    tags=['灵神题单·动态规划'],
    code='''
import functools
class Solution(object):
    def maxGroupNumber(self, tiles):

        cnt_dict = {}
        for tile in tiles:
            cnt_dict[tile] = cnt_dict.get(tile, 0) + 1
        
        cnt_info = sorted(cnt_dict.items(), key=lambda d:d[0])
        if len(cnt_info) <= 2:
            res = 0
            for tile, cnt in cnt_info:
                res += cnt // 3
            return res
        
        n = len(cnt_info)
        f = [[0] * 9 for _ in range(n)]
        f[0][0] = cnt_info[0][1] // 3
        f[1][0] = f[0][0] + cnt_info[1][1] // 3
        for i in range(2, n):
            tile, cnt = cnt_info[i]
            for state in range(9):
                now_straight = state % 3
                last_straight = state // 3
                if now_straight > cnt:
                    continue
                if now_straight + last_straight > cnt_info[i - 1][1]:
                    continue
                if now_straight > 0 and (cnt_info[i][0] != cnt_info[i - 1][0] + 1 or cnt_info[i - 1][0] != cnt_info[i - 2][0] + 1):
                    continue

                for two_round_straight in range(3):
                    if two_round_straight + last_straight + now_straight > cnt_info[i - 2][1]:
                        continue
                    last_state = two_round_straight * 3 + last_straight
                    tmp = f[i - 1][last_state] + now_straight + (cnt - now_straight) // 3
                    if (cnt_info[i - 1][1] - last_straight) % 3 < now_straight:
                        tmp -= 1
                    if (cnt_info[i - 2][1] - last_straight - two_round_straight) % 3 < now_straight:
                        tmp -= 1
                    f[i][state] = max(f[i][state], tmp)

        return max(f[-1])
''',
    call=f'Solution().maxGroupNumber({TILES})',
    expect=1,
    skip=['if now_straight > cnt', 'if now_straight + last_straight >', 'if now_straight > 0 and', 'continue', 'for two_round_straight', 'last_state =', 'if two_round_straight + last_straight', 'import functools', 'cnt_dict = {}', 'for tile in tiles', 'cnt_dict[tile] =', 'now_straight = state', 'last_straight = state', 'tile, cnt = cnt_info[i]'],
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='grid', var='f', label='f[i][state]：前 i+1 种牌最多牌组数（黄 = 正在算，蓝 = 转移来源）',
             cell=60, h=250, color=_fcell, rows=lambda S: [t for t, c in S['cnt_info']] if 'cnt_info' in S else None,
             cols=['0', '1', '2', '3', '4', '5', '6', '7', '8']),
        dict(type='text', fn=lambda S: '`state = 高位×3 + 低位`：高位 = 以前一种牌结尾的顺子数，低位 = 以当前这种牌结尾的顺子数（各 ≤ 2 组）', h=70),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('state', lambda S: S['_inner'].get('state'), 'yellow'),
           ('tmp', lambda S: S['_inner'].get('tmp'), 'green'), ('last_state', lambda S: S['_inner'].get('last_state'), 'blue')],
    captions={
        'cnt_info = sorted': '聚合后按点数排序：`cnt_info = {cnt_info}`，每项是 `(点数, 张数)`',
        'if len(cnt_info)': '不到 3 种牌不可能有顺子，只数刻子；这里有 `{len(cnt_info)}` 种，走 DP',
        'n = len': '`n = {n}` 种牌；`f[i][state]` 是 `n × 9` 的表',
        'f = [[0]': '`state` 是两位三进制（0..8），表先全设 0',
        'f[0][0] =': '前两种牌凑不出顺子：`f[0][0] = {f[0][0]}` 就是点数 {cnt_info[0][0]} 的刻子数 `{cnt_info[0][1]} // 3`',
        'f[1][0] =': '`f[1][0]` = 前两种牌的刻子数之和 = `{f[1][0]}`',
        'for i in range': lambda S, B, r: '所有牌都处理完，答案在最后一行 `f[n-1]`' if S.get('i') == B.get('i') and S.get('i') is not None else f'从第 `{S._inner.get("i")}` 种牌（点数 {S.cnt_info[S._inner.get("i")][0]}，共 {S.cnt_info[S._inner.get("i")][1]} 张）开始 DP' if S._inner.get('i') is not None else '前两种牌已处理完，DP 从 `i = 2` 开始，到最后一种牌结束',
        'for state in range': _state_cap,
        'tmp = f[i - 1]': lambda S, B, r: (f'来自 `f[{S.i - 1}][{S.last_state}] = {S.f[S.i - 1][S.last_state]}`，加 `{S.state % 3}` 个顺子，'
                                           f'再加剩下 `{S.cnt - S.state % 3}` 张的刻子 `{(S.cnt - S.state % 3) // 3}` 个 → `tmp = {S.tmp}`'),
        'tmp -= 1': lambda S, B, r: ('顺子要用掉点数 %d 的牌，但它们剩下的零散牌不够（余数 < 顺子数）→ ==拆开一个刻子==，`tmp = %d`' % (
            S.cnt_info[S.i - 1][0] if S._line == 38 else S.cnt_info[S.i - 2][0], S.tmp)),
        'if (cnt_info[i - 1][1]': '点数 {cnt_info[i - 1][0]}：扣掉 last 顺子后剩 `{cnt_info[i - 1][1] - last_straight}` 张，三张一组后余 `{(cnt_info[i - 1][1] - last_straight) % 3}` 张；够凑 `{now_straight}` 个顺子吗？',
        'if (cnt_info[i - 2][1]': '点数 {cnt_info[i - 2][0]}：扣掉 last 和 two 之后余 `{(cnt_info[i - 2][1] - last_straight - two_round_straight) % 3}` 张；够凑 `{now_straight}` 个顺子吗？',
        'f[i][state] = max': '`f[{i}][{state}] = max(旧值, {tmp})` = =={f[i][state]}==',
        'return max': '最后一种牌的所有 `state` 里取最大：`max(f[-1]) = {ret}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='顺子最多 2 组，3 组同样的顺子不如拆成刻子',
        complexity='时间 `O(9n)`，空间 `O(9n)`',
        problem=['`tiles` 是一堆牌的点数，三张相同的点数是一个==刻子==，三张连续的点数是一个==顺子==',
                 '每张牌最多用一次，求最多能组成几组',
                 '本视频：`[2,3,3,3,4]` → `1`'],
        quote='计算3组123就不如分别计算3个1、2、3来得方便，那么在这里就可以默认，以k结尾的k - 2、k - 1、k形成的顺子不会超过两组。',
        quote_src='—— yiduobo 题解原文',
        idea=['先聚合排序，`f[i][state]`：`state` 是两位三进制数，高位 = 以第 `i-1` 种结尾的顺子数，低位 = 以第 `i` 种结尾的顺子数',
              '转移时再枚举「以第 `i-2` 种结尾的顺子数」，检查三种牌的张数够不够',
              '当前这种牌：`now_straight` 个顺子 + `(cnt − now_straight) // 3` 个刻子'],
        summary=['时间 `O(9n)`，状态里只需记最近两种牌的顺子数',
                 '点数不连续（差不为 1）时，不能形成顺子，`state` 对应低位必须为 0',
                 '凑顺子要占用前两种牌；占用后可能拆散之前的刻子，所以要 `tmp -= 1`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`state // 3`、`cnt // 3` 等共 5 处）'],
    ),
)

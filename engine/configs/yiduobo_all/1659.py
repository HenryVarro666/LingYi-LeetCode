M, N, IC, EC = 2, 1, 1, 1
WHO = {0: '空', 1: '内向', 2: '外向'}


def _prev(S):
    if 'last_i' not in S or 'intro' not in S or 'extro' not in S:
        return None
    return S['f'][S['last_i']][S['last_j']][S['intro']][S['extro']]


def _cur(S):
    if 'intro' not in S or 'extro' not in S:
        return None
    return S['f'][S['i']][S['j']][S['intro']][S['extro']]


def _txt(S):
    if 'state' not in S or 'upper_state' not in S:
        return '`state`：三进制，每一位表示一个格子 —— 0 空，1 内向，2 外向'
    u, l = S['upper_state'], S['left_state'] if 'left_state' in S else 0
    s = f"`state = {S['state']}`：上方格子 =={WHO[u]}=="
    if S.get('j', 0) > 0:
        s += f'，左边格子 =={WHO[l]}=='
    return s


def _tmp_cap(who):
    def fn(S, B, ret):
        base = 120 if who == 1 else 40
        parts = [f'自己 {base}']
        for name, st, ok in (('上方', S.upper_state, S.i > 0), ('左边', S.left_state, S.j > 0)):
            if ok and st > 0:
                if who == 1:
                    parts.append(f'{name}{WHO[st]}：自己 −30，对方 ' + ('−30' if st == 1 else '+20'))
                else:
                    parts.append(f'{name}{WHO[st]}：自己 +20，对方 ' + ('−30' if st == 1 else '+20'))
        key = S.base_state + who
        return f'放{WHO[who]}的人：' + '；'.join(parts) + f' → 新增 `tmp = {S.tmp}`，`f[..][{key}] = {S.f[S.i][S.j][S.intro][S.extro][key]}`'
    return fn


CONFIG = dict(
    num=1659, title='最大化网格幸福感', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='轮廓线状态压缩 DP（三进制 state）',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def getMaxGridHappiness(self, m, n, introvertsCount, extrovertsCount):

        max_state = 3 ** n
        upper_divisor = max_state // 3
        f = [[[[[-1] * max_state for _ in range(extrovertsCount + 1)] for _ in range(introvertsCount + 1)] for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    f[i][j][0][0][0] = 0
                    if introvertsCount > 0:
                        f[i][j][1][0][1] = 120
                    if extrovertsCount > 0:
                        f[i][j][0][1][2] = 40
                else:
                    if j == 0:
                        last_i, last_j = i - 1, n - 1
                    else:
                        last_i, last_j = i, j - 1

                    for intro in range(introvertsCount + 1):
                        if intro > i * n + j + 1:
                            break
                        for extro in range(extrovertsCount + 1):
                            if intro + extro > i * n + j + 1:
                                break

                            for state in range(max_state):
                                upper_state = state // upper_divisor
                                left_state = state % 3
                                base_state = (state % upper_divisor) * 3
                                f[i][j][intro][extro][base_state] = max(f[i][j][intro][extro][base_state], f[last_i][last_j][intro][extro][state])
                                if intro >= 1 and f[last_i][last_j][intro - 1][extro][state] >= 0:
                                    tmp = 120
                                    if i > 0 and upper_state > 0:
                                        tmp -= 30
                                        if upper_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    if j > 0 and left_state > 0:
                                        tmp -= 30
                                        if left_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    f[i][j][intro][extro][base_state + 1] = max(f[i][j][intro][extro][base_state + 1], f[last_i][last_j][intro - 1][extro][state] + tmp)
                                
                                if extro >= 1 and f[last_i][last_j][intro][extro - 1][state] >= 0:
                                    tmp = 40
                                    if i > 0 and upper_state > 0:
                                        tmp += 20
                                        if upper_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    if j > 0 and left_state > 0:
                                        tmp += 20
                                        if left_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    f[i][j][intro][extro][base_state + 2] = max(f[i][j][intro][extro][base_state + 2], f[last_i][last_j][intro][extro - 1][state] + tmp)
        
        res = 0
        for i in range(m):
            for j in range(n):
                for intro in range(introvertsCount + 1):
                    for extro in range(extrovertsCount + 1):
                        for state in range(max_state):
                            res = max(res, f[i][j][intro][extro][state])

        return res
''',
    call=f'Solution().getMaxGridHappiness({M}, {N}, {IC}, {EC})',
    expect=150,
    views=[
        dict(type='array', var=_prev, label='上一格 f[last][intro][extro][state]（下标 = state，−1 = 不可达）', cell=100, h=190,
             color=lambda S, i, v: 'blue' if i == S.get('state') else None),
        dict(type='array', var=_cur, label='当前格 f[i][j][intro][extro][新 state]（黄 = 刚更新）', cell=100, h=190,
             color=lambda S, i, v: 'yellow' if S.get('_line') in (32, 49, 67) and i == S.get('base_state', -9) + {32: 0, 49: 1, 67: 2}[S['_line']] else None),
        dict(type='text', size=26, h=70, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('intro', 'intro', 'pink'), ('extro', 'extro', 'green'),
           ('state', 'state', 'yellow'), ('res', 'res', 'green')],
    skip=['for i in range(m)', 'for j in range(n)', 'for intro in range', 'for extro in range', 'for state in range',
          'if intro > i * n', 'if intro + extro >', 'break', 'upper_state = state', 'left_state = state', 'base_state = (state',
          'tmp = 120', 'tmp = 40', 'tmp -= 30', 'tmp += 20', 'tmp += 20', 'if upper_state == 1', 'if left_state == 1',
          'if introvertsCount > 0', 'if extrovertsCount > 0', 'if j == 0:', 'if i > 0 and upper_state', 'if j > 0 and left_state',
          'res = 0', 'last_i, last_j = i, j - 1', 'res = max('],
    captions={
        'max_state = 3 ** n': '`state` 是 ==n 位三进制数==：每位一个格子，0 空 / 1 内向 / 2 外向；只记最近 n 个格子，共 `3^n = {max_state}` 种',
        'upper_divisor': '`upper_divisor = 3^(n-1) = {upper_divisor}`：`state // upper_divisor` 取出最高位 = 当前格==上方==那格',
        'f = [[[[[-1]': '`f[i][j][k][l][state]`：填到格子 (i,j)，用了 k 个内向、l 个外向、近 n 格状态为 state 时的最大幸福感；`-1` = 不可达',
        'f[i][j][0][0][0] = 0': '第一个格子，什么人都不放：`f[0][0][0][0][0] = 0`',
        'f[i][j][1][0][1] = 120': '第一个格子放 1 个内向的人：幸福感 120，state = 1',
        'f[i][j][0][1][2] = 40': '第一个格子放 1 个外向的人：幸福感 40，state = 2',
        'last_i, last_j = i - 1, n - 1': '`j == 0`：前一个格子是上一行最后一格 `({last_i},{last_j})`',
        'f[i][j][intro][extro][base_state] = max': lambda S, B, r: (
            f'`state = {S.state}`（上方=={WHO[S.upper_state]}==）→ 移位成 `base_state = {S.base_state}`；'
            f'==当前格不放人==：`f[..][{S.base_state}]` = =={S.f[S.i][S.j][S.intro][S.extro][S.base_state]}=='),
        'if intro >= 1 and f': lambda S, B, r: (
            (f'`intro = {S.intro} ≥ 1`，且上一格 `f[..][{S.intro - 1}][{S.extro}][{S.state}] = {S.f[S.last_i][S.last_j][S.intro - 1][S.extro][S.state]} ≥ 0` → ==可以放内向的人==')
            if S.intro >= 1 and S.f[S.last_i][S.last_j][S.intro - 1][S.extro][S.state] >= 0
            else f'没有内向的人可放，或上一格的该状态不可达（−1）→ 跳过'),
        'f[i][j][intro][extro][base_state + 1]': _tmp_cap(1),
        'if extro >= 1 and f': lambda S, B, r: (
            (f'`extro = {S.extro} ≥ 1`，且上一格 `f[..][{S.intro}][{S.extro - 1}][{S.state}] = {S.f[S.last_i][S.last_j][S.intro][S.extro - 1][S.state]} ≥ 0` → ==可以放外向的人==')
            if S.extro >= 1 and S.f[S.last_i][S.last_j][S.intro][S.extro - 1][S.state] >= 0
            else f'没有外向的人可放，或上一格的该状态不可达（−1）→ 跳过'),
        'f[i][j][intro][extro][base_state + 2]': _tmp_cap(2),
        'return res': '枚举所有格子、人数、state 取最大的 `f`：=={ret}==（内向在上、外向在下，或反过来，都是 150）',
    },
    max_steps=44,
    cards=dict(
        one_liner='逐格填表，state 只记最近 n 个格子的三进制状态',
        complexity='时间 `O(m·n·I·E·3^n)`，空间同量级',
        problem=['`m × n` 网格，最多安排 `introvertsCount` 个内向、`extrovertsCount` 个外向的人（可以不住满）',
                 '内向：基础 120，每个邻居 −30；外向：基础 40，每个邻居 +20',
                 '邻居的影响是==双向==的，要同时算对方的变化',
                 '本视频：`m=2, n=1, 内向 1, 外向 1` → `150`'],
        quote='state并不需要储存所有格子的状态，而是只需要储存从[i - 1, j]到[i, j - 1]这些格子的状态就好了。这样一来state的规模里面就缩减到了3^n，上限最多就是3^5了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j][k][l][state]`：填到 (i,j)，用 k 个内向、l 个外向，近 n 格状态为 state',
              '新格子只和上方（state 最高位）、左边（state 最低位）有关',
              '转移时去掉最高位、左移一位，再把当前格（0/1/2）填在最低位'],
        result='填完所有格子，取最大值 `150` ✓',
        summary=['时间 `O(m·n·I·E·3^n)`，n ≤ 5，所以 `3^n ≤ 243`',
                 '易错：两个人相邻，要同时加上对方被影响的幸福感',
                 '易错：`f` 初值为 −1 表示不可达，转移前要判断 `>= 0`',
                 '示例取 `2×1` 是为了让步数可控；`n ≥ 2` 时左边格子也会参与（`left_state`）',
                 '原文为 Python 2 写法，`/` 为整数除法，已改为 `//`（`upper_divisor`、`upper_state`）'],
    ),
)

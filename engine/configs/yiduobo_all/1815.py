BS = 3
GROUPS = [3, 1, 1, 2]


def _q(S):
    q = S.get('q')
    if q is None:
        return '把各数按 `% batchSize` 分组，只记「每种余数还剩几个」作为状态'
    l = S.get('l', 0)
    wait = ' '.join(f'{tuple(t)}' for t, r in q[l:][:6])
    cur = ''
    if 'now_tuple' in S:
        cur = f'当前 `{S["now_tuple"]}`，已选数之和余 `{S["now_rem"]}`；'
    return f'{cur}队列里等着：{wait or "无"}'


CONFIG = dict(
    num=1815, title='得到新鲜甜甜圈的最多组数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按余数分组 + 状态 BFS（元组做状态）',
    tags=['难度分 2559'],
    code='''
class Solution(object):
    def maxHappyGroups(self, batchSize, groups):

        cnt_list = [0] * batchSize
        for num in groups:
            cnt_list[num % batchSize] += 1
        
        q = [[tuple(cnt_list[1:]), 0]]
        l = 0
        r = 1
        f = {}
        f[q[0][0]] = 0
        while l < r:
            now_tuple, now_rem = q[l]
            if now_rem == 0:
                delta = 1
            else:
                delta = 0
            l += 1
            now_list = list(now_tuple)
            for index in range(batchSize - 1):
                if now_list[index] > 0:
                    now_list[index] -= 1
                    next_tuple = tuple(now_list)
                    next_rem = (now_rem + index + 1) % batchSize
                    now_list[index] += 1
                    if next_tuple not in f:
                        f[next_tuple] = f[now_tuple] + delta
                        q.append([next_tuple, next_rem])
                        r += 1
                    else:
                        f[next_tuple] = max(f[next_tuple], f[now_tuple] + delta)
        
        return f[tuple([0] * (batchSize - 1))] + cnt_list[0]
''',
    call=f'Solution().maxHappyGroups({BS}, {GROUPS})',
    expect=3,
    skip=['for num in groups', 'for index in range', 'l += 1', 'now_list = list', 'r += 1', 'if now_list[index] > 0', 'now_list[index] -= 1',
          'now_list[index] += 1', 'q = [[', 'l = 0', 'r = 1', 'f = {}'],
    views=[
        dict(type='array', var='cnt_list', label='cnt_list[r]：模 batchSize 余 r 的组数', h=170, cell=90),
        dict(type='map', var='f', label='f[状态]：到这个状态最多已开心的组数（状态 = 余1、余2… 还剩几个）',
             fmt=lambda k, v: f'{tuple(k)} → {v}', h=300, font=28),
        dict(type='text', fn=_q, size=26, h=110),
    ],
    watch=[('l', 'l'), ('r', 'r'), ('now_tuple', 'now_tuple', 'blue'), ('now_rem', 'now_rem', 'orange'), ('delta', 'delta', 'pink')],
    captions={
        'cnt_list[num % batchSize] += 1': '`{num}` 模 `{batchSize}` 余 `{num % batchSize}`，计数：`cnt_list = {cnt_list}`',
        'f[q[0][0]] = 0': '初始状态 `{q[0][0]}`（余 1、余 2…各剩几个），已开心 0',
        'while l < r': lambda S, B, ret: ('队列还有状态，取出一个' if S.l < S.r else '队列空了，所有状态都处理完'),
        'now_tuple, now_rem = q[l]': '取出状态 `{now_tuple}`，已选数之和模 batchSize = `{now_rem}`',
        'if now_rem == 0': lambda S, B, ret: ('余数为 0：上一组刚好卖完，==下一组会开心==，`delta = 1`' if S.now_rem == 0
                                              else f'余数 `{S.now_rem}` ≠ 0：下一组拿到的是剩下的，不开心'),
        'delta = 1': '`delta = 1`：这一步新开的一组开心',
        'delta = 0': '`delta = 0`',
        'next_tuple = tuple(now_list)': '选一个余 `{index + 1}` 的数后，状态变成 `{next_tuple}`',
        'next_rem = ': '`next_rem = ({now_rem} + {index + 1}) % {batchSize}` = `{next_rem}`',
        'if next_tuple not in f': lambda S, B, ret: ('新状态，还没到过' if S.next_tuple not in B.f else '这个状态已经到过，要取更大的值'),
        'f[next_tuple] = f[now_tuple] + delta': '新状态 `{next_tuple}`：`f = {f[now_tuple]} + {delta}` = =={f[next_tuple]}==，入队（带上余数 `{next_rem}`）',
        'q.append': '入队',
        'f[next_tuple] = max': '`f[{next_tuple}] = max(旧值, {f[now_tuple]} + {delta})` = =={f[next_tuple]}==（选数的顺序不同，可能到达同一状态）',
        'return f[': '全部选完 `f[(0,…)]` = `{f[tuple([0] * (batchSize - 1))]}`，再加上余 0 的 `{cnt_list[0]}` 组 → =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='余 0 的组自成一家，其余按「各余数还剩几个」做状态 BFS',
        complexity='时间约 `O(状态数 × batchSize)`，状态数不到 4 万',
        problem=['每批烤 `batchSize` 个甜甜圈；一批顾客的第一位拿到的不是上一组剩下的，这组就开心',
                 '任意安排各组顺序，求最多有多少组开心',
                 '本视频：`batchSize = 3, groups = [3,1,1,2]` → `3`'],
        quote='将这些数先按照对batchSize取模的值分组。模batchSize等于0的这一组显然是自成一派的，不需要与其他数组合',
        quote_src='—— yiduobo 题解原文',
        idea=['问题等价：把 groups 分成 k 段，前 k−1 段的和都是 batchSize 的倍数，求最大 k',
              '余 0 的组单独成段；余 1…batchSize−1 各剩几个，用 tuple 当状态，30 分成 8 份最多不到 4 万种',
              '`now_rem` 是已选数之和的余数：为 0 说明刚好卖完一批，下一组开心（`delta = 1`）'],
        summary=['状态数约 4 万，BFS 每个状态枚举 `batchSize − 1` 种选法',
                 '同一状态可由不同顺序到达，所以要用 `max` 更新 `f`',
                 '最后别忘了加上余 0 的 `cnt_list[0]` 组',
                 '原文在 Python 3 下可直接运行，没有改动',
                 '对比灵神：灵神先把 `x` 和 `m−x` 配对，再用记忆化 DFS；yiduobo 不配对，直接 BFS 全状态'],
    ),
)

def _inn(S, k):
    return S['_inner'].get(k)


def _txt(S):
    now, prev, t = _inn(S, 'now'), _inn(S, 'prev'), _inn(S, 't')
    if t is None or now is None or S.get('_line') not in (9, 11, 12):
        return '`f[now]`：到第 `t` 天结束时位于城市 `now` 的最大点数；`g` 是前一天的 `f`'
    if S.get('_line') == 9:
        return f'留下：`g[{now}] + stayScore[{t}][{now}]` = {S["g"][now]} + {S["stayScore"][t][now]} = =={S["f"][now]}=='
    if prev is None or prev == now:
        return f'枚举从哪座城市 `prev` 赶来（`prev != now`）'
    return f'从 `{prev}` 过来：`g[{prev}] + travelScore[{prev}][{now}]` = {S["g"][prev]} + {S["travelScore"][prev][now]} = =={S["g"][prev] + S["travelScore"][prev][now]}=='


def _fcol(S, i, v):
    now = _inn(S, 'now')
    return 'yellow' if now == i and S.get('_line') in (9, 11, 12) and 'g' in S else None


CONFIG = dict(
    num=3332, title='旅客可以得到的最多点数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按天 DP · 滚动数组',
    tags=['灵神题单·动态规划', '难度分 1828'],
    code='''
class Solution(object):
    def maxScore(self, n, k, stayScore, travelScore):
        
        f = [0] * n
        for t in range(k):
            g = f[:]
            f = [0] * n
            for now in range(n):
                f[now] = g[now] + stayScore[t][now]
                for prev in range(n):
                    if prev != now:
                        f[now] = max(f[now], g[prev] + travelScore[prev][now])
        
        return max(f)
''',
    call='Solution().maxScore(3, 2, [[3, 4, 2], [2, 1, 2]], [[0, 2, 1], [2, 0, 4], [3, 2, 0]])',
    expect=8,
    skip=['for prev in range', 'for now in range'],
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var=lambda S: S.get('g', [0] * S['n']) if 'g' in S else [0] * S['n'], label='g（前一天的 f）', cell=90, h=185,
             pointers={"_inner.get('prev', -1)": 'pink'}, pointer_labels={"_inner.get('prev', -1)": 'prev'},
             color=lambda S, i, v: 'pink' if _inn(S, 'prev') == i and S.get('_line') in (11, 12) else None),
        dict(type='array', var='f', label='f（第 t 天结束时位于各城市的最大点数）', cell=90, h=185,
             pointers={"_inner.get('now', -1)": 'blue'}, pointer_labels={"_inner.get('now', -1)": 'now'}, color=lambda S, i, v: _fcol(S, i, v)),
        dict(type='table', var='travelScore', label='travelScore[prev][now]', h=210, cell=60,
             rows=lambda S: [f'从{c}' for c in range(S['n'])], cols=lambda S: [f'去{c}' for c in range(S['n'])],
             color=lambda S, r, c, v: ('yellow' if (r, c) == (_inn(S, 'prev'), _inn(S, 'now')) and S.get('_line') in (11, 12) else None)),
    ],
    watch=[('t', 't', 'yellow'), ('now', 'now', 'blue'), ('prev', 'prev', 'pink')],
    captions={
        'for t in range': lambda S, B, r: (f'第 `{S.t}` 天' if S.get('t') != B.get('t') or 'g' not in S else '`k` 天都过完了'),
        'g = f[:]': '把前一天的 `f` 拷贝成 `g`，`f` 重新开始算今天',
        'f = [0] * n': lambda S, B, r: (f'`f` 清零，准备算第 `{S.t}` 天' if S.get('g') is not None else '`f[now]`：当天位于城市 `now` 的最大点数；起点任选，所以一开始全是 0'),
        'f[now] = g[now]': '情况 1：昨天就在城市 `{now}`，今天留下 → `g[{now}] + stayScore[{t}][{now}]` = {g[now]} + {stayScore[t][now]} = =={f[now]}==',
        'if prev != now': lambda S, B, r: (f'情况 2：今天才从别的城市来；枚举 `prev = {S.prev}`' + ('，就是 `now` 自己，跳过' if S.prev == S.now else '')),
        'f[now] = max(f[now], g[prev]': lambda S, B, r: (f'从 `{S.prev}` 过来得 `{S.g[S.prev]} + {S.travelScore[S.prev][S.now]}` = {S.g[S.prev] + S.travelScore[S.prev][S.now]}，'
                                                        f'与当前 `{B.f[S.now]}` 取大 → `f[{S.now}]` = =={S.f[S.now]}=='),
        'return max(f)': '任意城市结束都行：`max(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='f[now]：第 t 天到城市 now 的最大点数，留下或从别处来',
        complexity='时间 `O(kn^2)`，空间 `O(n)`',
        problem=['`n` 座城市两两直达，旅客旅游==恰好 k 天==，起点任选',
                 '每天二选一：留在原地得 `stayScore[t][now]`，或从 `prev` 去 `now` 得 `travelScore[prev][now]`',
                 '示例：`n=3, k=2` → `8`'],
        quote='令f[t][now]表示第t天旅客位于城市now时可以得到的最大点数，那么对于f[t][now]：1、旅客可能是在时刻t - 1已经在now，然后选择留在now……',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[t][now]` 两种来源：昨天就在 `now`（留下）；昨天在别的城市 `prev`（今天赶来）',
              '只依赖前一天，所以用 `g` 保存昨天、`f` 算今天，省掉 `t` 这一维',
              '答案：`max(f)`，最后一天可以在任何城市'],
        summary=['时间 `O(kn^2)`，空间 `O(n)`（滚动数组）',
                 '易错：`g = f[:]` 要拷贝，不能直接 `g = f`；`prev != now` 才算“旅行”',
                 '原文用 `f[t][now]` 讲思路，代码已经是滚动数组；原文是 Python 2 风格但无需修改',
                 '对比灵神：他倒着从最后一天往前推，起点最后取 max；这里正着推，终点取 max'],
    ),
)

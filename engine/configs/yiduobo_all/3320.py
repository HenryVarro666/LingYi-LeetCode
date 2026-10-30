S0 = 'FW'
N = len(S0)
POKE = 'FWE'


def _mat(d):
    return [[d.get(p, {}).get(sc, 0) for p in POKE] for sc in range(-N, N + 1)]


def _both(S):
    f = S.get('f')
    if f is None or 'poke' not in S:
        return None
    g = S.get('g')
    gm = _mat(g) if g is not None else [[0, 0, 0] for _ in range(2 * N + 1)]
    fm = _mat(f)
    return [a + b for a, b in zip(gm, fm)]


def _rows(S):
    return [str(s) for s in range(-N, N + 1)]


def _col(S, r, c, v):
    if 'prev' not in S or 'now' not in S:
        return None
    if 'score' in S and S.get('_line', 0) >= 28:
        if c < 3 and POKE[c] == S['prev'] and r == S['score'] + N:
            return 'blue'
        if c >= 3 and POKE[c - 3] == S['now'] and 'now_score' in S and r == S['now_score'] + N:
            return 'yellow'
    return None


def _txt(S):
    if 'g' not in S:
        return '`f[出招][净胜分]`：Bob 最后一轮出什么、当前净胜几分 → 方案数'
    if 'prev' in S and 'now' in S and 'c' in S:
        return f'Alice 本轮出 `{S["c"]}`；Bob 上一轮 `{S["prev"]}` → 这一轮 `{S["now"]}`（不能相同）'
    return '左 = 上一轮 `g`，右 = 这一轮 `f`；行 = 净胜分，列 = Bob 最后一轮出招'


CONFIG = dict(
    num=3320, title='统计能获胜的出招序列数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='字典 DP：出招 × 净胜分',
    tags=['灵神题单', '难度分 2153'],
    code='''
class Solution(object):
    def countWinningSequences(self, s):
        
        n = len(s)
        f = {'F': {}, 'W': {}, 'E': {}}
        delta = {'F': {'F': 0, 'W': -1, 'E': 1},
                 'W': {'F': 1, 'W': 0, 'E': -1},
                 'E': {'F': -1, 'W': 1, 'E': 0}
        }

        poke = ['F', 'W', 'E']
        for p in poke:
            f[p][delta[p][s[0]]] = 1

        mod = 10 ** 9 + 7
        for c in s[1:]:
            g = copy.deepcopy(f)
            f = {'F': {}, 'W': {}, 'E': {}}
            for prev in poke:
                for now in poke:
                    if prev == now:
                        continue
                    for score in g[prev]:
                        now_score = score + delta[now][c]
                        f[now][now_score] = (f[now].get(now_score, 0) + g[prev][score]) % mod

        res = 0
        for p in poke:
            for score in f[p]:
                if score > 0:
                    res = (res + f[p][score]) % mod
        
        return res
''',
    setup='import copy',
    call=f'Solution().countWinningSequences({S0!r})',
    expect=2,
    max_steps=75,
    skip=['n = len(s)', 'delta = {', 'poke = [', 'mod = 10', 'res = 0', 'for p in poke:', 'continue', 'for score in g[prev]', 'for score in f[p]', "'W': {'F': 1", "'E': {'F': -1"],
    views=[
        dict(type='text', fn=_txt, size=22, h=60),
        dict(type='string', var='s', label='s：Alice 的出招', cell=80, h=130),
        dict(type='table', var=_both, label='左 = g（上一轮，蓝 = 来源）　右 = f（这一轮，黄 = 刚累加）', h=420, cell=70,
             rows=_rows, cols=lambda S: ['旧' + c for c in POKE] + ['新' + c for c in POKE], color=_col),
    ],
    watch=[('c', 'c', 'cyan'), ('prev', 'prev', 'blue'), ('now', 'now', 'yellow'), 'score', 'now_score', 'res'],
    captions={
        "f = {'F': {}, 'W': {}, 'E': {}}": lambda S, B, r: ('`f[出招][净胜分]`：Bob 最后一轮出这招、净胜这么多分的方案数，先全空' if 'g' not in S else '新开一层 `f`，旧的在 `g` 里'),
        'f[p][delta[p][s[0]]] = 1': '第一轮没有「上一轮」的限制：Bob 出 `{p}`、Alice 出 `{s[0]}` → 净胜 `{delta[p][s[0]]}` 分，方案 1 种',
        'for c in s[1:]': lambda S, B, r: (f'Alice 这一轮出 `{S.c}`：由上一轮 `g` 推出这一轮 `f`' if S.get('c') != B.get('c') else '所有轮次都推完了'),
        'g = copy.deepcopy(f)': '`g` = 上一轮的 `f` 的深拷贝（`copy.deepcopy`），然后清空 `f`',
        'if prev == now': lambda S, B, r: (f'`prev = {S.prev}`，`now = {S.now}`：相同 → ==不能连续出同一招==，跳过' if S.prev == S.now else f'`prev = {S.prev}` ≠ `now = {S.now}`：可以接'),
        'now_score = score': '净胜分 `{score}` + `delta[{now}][{c}] = {delta[now][c]}`（Bob 出 `{now}` 对 Alice 的 `{c}`）= =={now_score}==',
        'f[now][now_score] =': '`f[{now}][{now_score}]` 累加 `g[{prev}][{score}] = {g[prev][score]}` → =={f[now][now_score]}==',
        'if score > 0': lambda S, B, r: (f'`f[{S.p}][{S.score}]`：净胜 `{S.score}` > 0 → Bob 严格领先 → ==计入答案==' if S.score > 0 else f'`f[{S.p}][{S.score}]`：净胜 `{S.score}` ≤ 0 → 没赢，不计'),
        'res = (res + f[p][score])': '`res` += `f[{p}][{score}] = {f[p][score]}` → =={res}==',
        'return res': '把所有「净胜分 > 0」的方案加起来：`res` = =={ret}==',
    },
    cards=dict(
        one_liner='f[最后一招][净胜分]：枚举上一招和这一招，不能相同',
        complexity='时间 `O(n^2 · 9)`（净胜分最多 `2n+1` 种），空间 `O(n)`',
        problem=['Alice 的出招 `s` 已知，Bob ==不能连续出同一招==',
                 '每轮胜者得 1 分，平手不得分；Bob 总分更高才算赢',
                 '数出 Bob 的可行出招序列数，对 `10^9+7` 取余；示例 `"FFF"` → `3`',
                 '本视频演示 `s = "FW"` → `2`'],
        quote='令f[i][t][s]表示前i轮，最后一轮bob的出招为t，且bob的净胜分为s时的可行出招序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['用字典 `f[出招][净胜分]` 存方案数，净胜分是==键==，没出现过的就不存',
              '每轮：枚举上一轮出招 `prev`、这一轮 `now`，`prev ≠ now`，净胜分加上 `delta[now][c]`',
              '最后把所有 ==净胜分 > 0== 的方案相加'],
        summary=['时间 `O(n^2)`（常数 9），空间 `O(n)`（滚动，只留 `g` 和 `f` 两层）',
                 '易错：每轮要先深拷贝 `f` 到 `g`，再清空 `f`，否则边读边写会乱',
                 '易错：答案只算净胜分严格大于 0 的方案',
                 '代码用到 `copy.deepcopy`，原文没写 `import copy`，视频里在 setup 补了 `import copy`',
                 '对比灵神：灵神用数组 `f[i][j][ban]` + 剪枝；yiduobo 用字典只存出现过的净胜分'],
    ),
)

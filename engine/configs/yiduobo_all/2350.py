def _segs(rolls, k):
    seen, out, cur = set(), [], 0
    for x in rolls:
        out.append(cur)
        seen.add(x)
        if len(seen) == k:
            seen = set()
            cur += 1
    return out


def _rcol(S, i, v):
    if 'res' not in S:
        return None
    seg = _segs(S['rolls'], S['k'])
    if seg[i] >= S['res'] - 1:
        return None
    return ['blue', 'purple', 'cyan', 'orange'][seg[i] % 4]


def _text(S):
    if 'res' not in S:
        return '`f[p]`：凑齐 1..k 的最短前缀；每凑齐一次，答案 +1'
    return f'`num_set` 已有 {len(S["num_set"])} / {S["k"]} 种；凑齐 {S["res"] - 1} 次，当前 `res = {S["res"]}`'


CONFIG = dict(
    num=2350, title='不可能得到的最短骰子序列', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='递推 f[p] · 集合凑齐 k 种就清空',
    tags=['灵神题单', '难度分 1961'],
    code='''
class Solution(object):
    def shortestSequence(self, rolls, k):

        num_set = set()
        res = 1
        for num in rolls:
            num_set.add(num)
            if len(num_set) == k:
                res += 1
                num_set = set()
        
        return res
''',
    call='Solution().shortestSequence([4,2,1,2,3,3,2,4,1], 4)',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var='rolls', label='rolls（同色 = 已凑齐的一轮）', color=_rcol, h=200),
        dict(type='set', var='num_set', label='num_set：本轮出现过的数', fmt=lambda x: str(x), h=200),
    ],
    watch=[('res', 'res', 'green'), ('num', 'num', 'blue'), ('len(num_set)', 'len(num_set)', 'yellow'), 'k'],
    captions={
        4: '`num_set` 记录当前这一轮出现过的数字',
        'res = 1': '`res` 从 1 开始：答案至少是 1',
        10: '这一轮凑齐了：清空集合，开始下一轮',
        'for num in rolls': '看下一个数 `num = {num}`',
        'num_set.add(num)': '加入集合：`num_set = {sorted(num_set)}`（{len(num_set)} 种）',
        'if len(num_set) == k': lambda S, B, r: (f'`len = {len(S.num_set)} == k = {S.k}`：1..k 全齐 → 又得到一个 f[p]' if len(S.num_set) == S.k
                                                 else f'`len = {len(S.num_set)} < k = {S.k}`：还缺数字，继续往后扫'),
        'res += 1': '凑齐一轮 → 能保证任意长为 `{res-1}` 的序列都出现，答案至少 `res = {res}`',
        'return res': '最后一轮没凑齐 `1..k`，说明某个长为 `{res}` 的序列不存在 → `{ret}`',
    },
    cards=dict(
        one_liner='扫描时集合凑齐 k 种数就换新一轮，答案 = 轮数 + 1',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['`k` 面骰子扔 `n` 次得到 `rolls`；求==不是 rolls 子序列==的最短骰子序列长度',
                 '示例：`rolls=[4,2,1,2,3,3,2,4,1], k=4` → `3`'],
        quote='现在已知f[p]，那么f[p + 1]就是rolls[f[p] + 1]到rolls[n - 1]之间，1到k第一次出现位置的最大值。若其中某个数字没有出现过，那么说明f[p + 1]不存在，p + 1就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['令 `f[i]` = 能包含所有长为 `i` 序列的最短前缀；答案是第一个不存在的 `f`',
              '`f[1]`：1..k 都出现的最短前缀；`f[p+1]` 从 `f[p]` 之后重新数一遍',
              '实现：用集合记录本轮出现的数，满 `k` 个就 `res += 1` 并清空'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '初始 `res = 1`：连长度 1 都凑不齐时答案就是 1',
                 '清空要重新 `set()`，不能忘记',
                 '原文无 Python 2 专有写法，未做修改',
                 '对比灵神：灵神用 `mark[v]` 存段号避免清空；yiduobo 直接重建集合'],
    ),
)

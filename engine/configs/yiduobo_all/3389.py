def _top(S):
    if 't' not in S:
        return '先数出每个字母的出现次数 `cnt`'
    t = S['t']
    if 'index' not in S:
        return f'枚举最终每种字母出现 `t = {t}` 次：每种字母要么变成 {t} 个，要么全部去掉'
    i = S['index']
    return (f"`t = {t}`；`f` = 第 {i} 个字母调成 {t} 个，`g` = 第 {i} 个字母调成 0 个"
            f"（`f = {S['f']}`，`g = {S['g']}`）")


def _roll(S, B, r):
    i, t = S.index, S.t
    c, p = S.cnt[i], S.cnt[i - 1]
    f0, g0 = B.f, B.g
    head = f'处理第 {i} 个字母（`cnt[{i}] = {c}`，上一个 `cnt[{i-1}] = {p}`）：'
    if c >= t:
        body = f'`cnt ≥ t`，不接受别人变来，多的删掉 → `f = min({f0}, {g0}) + {c - t} = {S.new_f}`'
    else:
        d = t - c
        base = min(f0, g0) + d
        if p > t and S.new_f < base:
            body = f'缺 `d = {d}` 个；上一个多出 `{p - t}` 个，==变过来补缺口== → `f = {S.new_f}`（直接补要 {base}）'
        elif p < t and p > 0 and S.new_f < base:
            body = f'缺 `d = {d}` 个；上一个 `{p}` 个拿来变，其余删掉 → `f = {S.new_f}`（直接补要 {base}）'
        elif p == 0:
            body = f'缺 `d = {d}` 个；上一个字母也没有，没得借，直接补 → `f = {S.new_f}`'
        else:
            body = f'缺 `d = {d}` 个；借上一个并不更省，直接补 → `f = {S.new_f}`'
    return head + body + f'；`g = min(f, g) + cnt = {S.new_g}`'


def _ccolor(S, i, v):
    if 'index' in S and 'f' in S:
        if i == S['index']:
            return 'blue'
        if i == S['index'] - 1:
            return 'pink'
    return None


CONFIG = dict(
    num=3389, title='使字符频率相等的最少操作次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='枚举 t + 线性 DP（f / g 两个状态）',
    tags=['难度分 2940'],
    code='''
class Solution(object):
    def makeStringGood(self, s):
        
        cnt = [0] * 26
        for char in s:
            cnt[ord(char) - 97] += 1
        
        ma = max(cnt)
        res = len(s)

        for t in range(1, ma + 1):
            f = abs(cnt[0] - t)
            g = cnt[0]

            for index in range(1, 26):
                if cnt[index] >= t:
                    new_f = min(f, g) + cnt[index] - t
                else:
                    new_f = min(f, g) + t - cnt[index]
                    if cnt[index - 1] > t:
                        new_f = min(new_f, f + max(0, t - cnt[index] - (cnt[index - 1] - t)))
                    elif cnt[index - 1] < t:
                        new_f = min(new_f, g + max(0, t - cnt[index] - cnt[index - 1]))
                new_g = min(f, g) + cnt[index]

                f, g = new_f, new_g

            res = min(res, min(f, g))

        return res
''',
    call='Solution().makeStringGood("aaab")',
    expect=1,
    skip=['for char in s', 'cnt[ord(char)', 'for index in range', 'new_g = min', 'if cnt[index] >= t', 'else:',
          'new_f = min', 'if cnt[index - 1] > t', 'elif cnt[index - 1] < t'],
    max_steps=40,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='cnt', label='cnt（蓝 = 当前字母 index，粉 = 上一个字母 index−1）', cell=33,
             pointers={'index': 'blue'}, color=_ccolor, h=200),
        dict(type='text', fn=lambda S: f"`f = {S['f']}`（调成 t 个）　`g = {S['g']}`（调成 0 个）　`res = {S['res']}`" if 'f' in S and 'g' in S else '', size=30, h=70),
    ],
    watch=[('t', 't', 'orange'), ('index', 'index', 'blue'), ('f', 'f', 'cyan'), ('g', 'g', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt = [0] * 26': '`cnt[0]` 是 a 的次数，一共 26 个字母',
        'ma = max(cnt)': '`t` 最多枚举到最大次数 `ma = {ma}`',
        'res = len(s)': '`res` 的初值 `len(s) = {res}`：全部删光',
        'for t in range': lambda S, B, r: (f'枚举 `t = {S.t}`' if S.get('t') != B.get('t') or 't' not in B else '`t` 枚举完了'),
        'f = abs(cnt[0] - t)': '第 0 个字母前面没有可借的，只能增删：`f = |{cnt[0]} − {t}| = {f}`',
        'g = cnt[0]': '`g = cnt[0] = {g}`：把 a 全部删掉',
        'f, g = new_f, new_g': _roll,
        'res = min(res': '`t = {t}` 的最少操作 `min(f, g) = {min(f, g)}` → `res` = =={res}==',
        'return res': '最少操作 `{res}`',
    },
    cards=dict(
        one_liner='枚举每种字母的目标次数 t，f/g 两个状态记录“调成 t”和“调成 0”',
        complexity='时间 `O(n + 26·max(cnt))`，空间 `O(1)`',
        problem=['字符串 `s`，可删一个字符、加一个字符、把字母变成下一个字母（z 不能变 a）',
                 '要让每种字母出现次数都相等，求最少操作次数',
                 '本视频：`"aaab"` → `1`（把一个 a 变成 b）'],
        quote='修改操作不应该跨两个字符修改……对于跨两个字符修改的情况，完全可以先去掉准备修改的第index - 2种字符，然后再插入对应数量的第index种字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举 `t`：每种字母要么变成 `t` 个，要么全去掉',
              '`f[index]` 表示第 index 种字母==调成 t 个==，`g[index]` 表示==调成 0 个==',
              '字母数 `< t` 时，可以接受上一个字母多出来的（>t）或整个上一个字母（<t）变过来'],
        summary=['时间 `O(n + 26·max(cnt))`，空间 `O(1)`（f、g 滚动）',
                 '易错：分 `cnt[index-1] > t` 和 `< t` 两类，借来的数量算法不同',
                 '`g` 不接受上一个字母变来，所以 `g = min(f, g) + cnt[index]`',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神 f[i] 是“从 i 往后”的后缀 DP，这里是从前往后的 f/g 两状态'],
    ),
)

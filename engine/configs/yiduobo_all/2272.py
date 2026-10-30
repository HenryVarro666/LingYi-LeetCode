S0 = 'aababbb'


def _col(S, i, v):
    a, b = S.get('ma_char'), S.get('mi_char')
    if a is None:
        return None
    if v == a:
        return 'green'
    if v == b:
        return 'pink'
    return None


def _dim(S, i, v):
    a, b = S.get('ma_char'), S.get('mi_char')
    return a is not None and v not in (a, b)


def _text(S):
    if 'ma_char' not in S:
        return '先收集每个字母出现的下标，再枚举（出现最多的字母，出现最少的字母）'
    f, g = S.get('f'), S.get('g')
    if f is None:
        return f'这一对：`ma_char = {S["ma_char"]}`（+1），`mi_char = {S["mi_char"]}`（−1）'
    gs = '不存在' if g is not None and g <= -len(S0) else g
    return f'`f` = 以当前位置结尾的最大差 ==({f})==；`g` = 其中==至少含一个 mi_char== 的最大差 ==({gs})=='


CONFIG = dict(
    num=2272, title='最大波动的子字符串', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='枚举字母对 + f/g 双状态 + 按下标归并',
    tags=['灵神题单', '动态规划', '难度分 2516'],
    code='''
class Solution(object):
    def largestVariance(self, s):

        pos_dict = {}
        for index, char in enumerate(s):
            if char not in pos_dict:
                pos_dict[char] = []
            pos_dict[char].append(index)
        
        res = 0
        for ma_char, ma_pos in pos_dict.items():
            for mi_char, mi_pos in pos_dict.items():
                if ma_char == mi_char:
                    continue
                
                i = j = 0
                f = 0
                g = -len(s) - 1
                while i < len(ma_pos) and j < len(mi_pos):
                    if ma_pos[i] < mi_pos[j]:
                        f = max(f, 0) + 1
                        g += 1
                        i += 1
                    else:
                        g = max(f, g, 0) - 1
                        f = max(f, 0) - 1
                        j += 1
                
                    res = max(res, g)
                
                if i < len(ma_pos):
                    for index in range(i, len(ma_pos)):
                        f = max(f, 0) + 1
                        g += 1
                        res = max(res, g)
                else:
                    res = max(res, max(f, g, 0) - 1)
                    
        return res
''',
    call=f'Solution().largestVariance({S0!r})',
    expect=3,
    max_steps=48,
    skip=['pos_dict = {}', 'res = 0', 'continue', 'i = j = 0', 'f = 0', 'if char not in pos_dict', 'pos_dict[char] = []',
          'if ma_char == mi_char', 'for index, char in enumerate', 'f = max(f, 0) - 1', 'while i < len(ma_pos)', 'i += 1', 'j += 1'],
    views=[
        dict(type='string', var=lambda S: S0, label='s（绿 = ma_char，粉 = mi_char）', h=130, cell=70, color=_col, dim=_dim),
        dict(type='array', var=lambda S: S.get('ma_pos', []), label='ma_pos：ma_char 的下标', h=190, cell=70, pointers={'i': 'green'}, index=False),
        dict(type='array', var=lambda S: S.get('mi_pos', []), label='mi_pos：mi_char 的下标', h=190, cell=70, pointers={'j': 'pink'}, index=False),
        dict(type='text', fn=_text, size=24, h=80),
    ],
    watch=[('ma_char', 'ma_char', 'green'), ('mi_char', 'mi_char', 'pink'), 'i', 'j', ('f', 'f', 'blue'), ('g', 'g', 'cyan'), ('res', 'res', 'yellow')],
    captions={
        'for index, char in enumerate': lambda S, B, r: ('每个字符都收集完了' if S.get('index') == B.get('index') else f'先按字母收集下标：第 `{S.index}` 个字符是 `{S.char!r}`'),
        'pos_dict[char].append': '收集下标：第 `{index}` 个字符是 `{char!r}` → `pos_dict[{char!r}]` = {pos_dict[char]}',
        'for ma_char, ma_pos in': lambda S, B, r: ('所有字母对都枚举完了' if S.get('ma_char') == B.get('ma_char')
                                                   else f'选 `ma_char = {S.ma_char!r}` 当「出现最多」的字母，它的下标 `{S.ma_pos}`'),
        'for mi_char, mi_pos in': lambda S, B, r: (f'`ma_char = {S.ma_char!r}` 的所有搭档都试过了' if S.get('mi_char') == B.get('mi_char')
                                                   else f'`mi_char` 和 `ma_char` 都是 {S.mi_char!r}：同一个字母不能配对，跳过' if S.mi_char == S.ma_char
                                                   else f'再选 `mi_char = {S.mi_char!r}` 当「出现最少」的字母，下标 `{S.mi_pos}`'),
        'g = -len(s) - 1': '`f`：以当前位置结尾的最大差（ma 记 +1，mi 记 −1）；`g`：==至少含一个 mi== 的最大差，初值 `−len(s)−1` 表示「不存在」',
        'while i < len(ma_pos) and': lambda S, B, r: (f'两边都还有下标：`i = {S.i}`，`j = {S.j}`，按位置从左到右归并' if S.i < len(S.ma_pos) and S.j < len(S.mi_pos)
                                                      else '有一边用完了，归并结束'),
        'if ma_pos[i] < mi_pos[j]': lambda S, B, r: (f'下一个是 ma：位置 `{S.ma_pos[S.i]}` < `{S.mi_pos[S.j]}`，先处理 ma_char' if S.ma_pos[S.i] < S.mi_pos[S.j]
                                                     else f'下一个是 mi：位置 `{S.mi_pos[S.j]}` < `{S.ma_pos[S.i]}`，先处理 mi_char'),
        21: '遇到 ma：前面为负就丢掉，再 +1 → `f = {f}`（`g` 在后面加 1）',
        22: '`g` 已含 mi，接上 ma 一定赚，哪怕为负也不能丢 → `g = {g}`',
        34: '`g += 1` → `g = {g}`',
        'g = max(f, g, 0) - 1': '遇到 mi：`g = max(f, g, 0) − 1` = {g}（可以从 `f`、旧 `g` 或空串接上，含这个 mi，一定合法）',
        'res = max(res, g)': '只用 `g` 更新答案：`res = max({B.res}, {g}) = {res}`（`f` 可能是全 ma 的子串，波动其实是 0）',
        'if i < len(ma_pos)': lambda S, B, r: ('mi 用完了，ma 还剩下标：后面全是 +1，一路 `f += 1`、`g += 1`' if S.i < len(S.ma_pos)
                                               else 'ma 用完了，mi 可能还有剩余：补算最后一个 mi'),
        33: '剩余的 ma 都是 +1：`f = {f}`',
        32: lambda S, B, r: ('剩余的 ma 下标都处理完了' if S.get('index') == B.get('index') else f'补上剩下的 ma：下标 `{S.index}`'),
        'res = max(res, max(f, g, 0) - 1)': '`ma` 已经用完，再接上一个 mi：`max(f, g, 0) − 1` 是含 mi 的最大差，`res` → {res}',
        'return res': '所有字母对都试过，最大波动 =={res}==',
    },
    cards=dict(
        one_liner='枚举「最多」「最少」的字母，f/g 两个状态避免全是 ma 的假答案',
        complexity='时间 `O(26·n)`，空间 `O(n)`',
        problem=['波动 = 子串里出现最多的字符次数 − 出现最少的字符次数，求所有子串的最大波动',
                 '示例：`s = "aababbb"` → `3`（`babbb`：4 个 b − 1 个 a）',
                 '本视频沿用这个例子，只有 `a`、`b` 两种字母'],
        quote='若s[i]是mi_char，与情况2相反，就有g[i] = max(f[i - 1], g[i - 1], 0) - 1',
        quote_src='—— yiduobo 题解原文',
        idea=['先枚举 `ma_char` 和 `mi_char`，问题变成：找子串让 ma 个数 − mi 个数最大',
              '`f` 是普通最大子段和，但可能整段全是 ma；所以再设 `g`：至少含一个 mi',
              '其他字母不改变 `f`、`g`：只把两个字母的下标按位置归并着处理，跳过无关字符'],
        summary=['复杂度：枚举字母对 × 两个下标表之和，约 `O(26n)`',
                 '`g` 初值是 `−len(s)−1`，表示「还没出现过 mi」，别写成 0',
                 '`g` 遇到 ma 时 `g += 1`，不能因为 `g` 是负数就丢掉前面的部分',
                 '原文是 Python 2 风格但 Python 3 可直接运行（`items()`、`range` 都兼容），代码未作任何修改'],
    ),
)

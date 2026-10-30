STR = 'aabca'
LET = sorted(set(STR))


def _p2(S):
    return 'res' in S and 'char' in S and 'first' in S and S['char'] in S['first']


def _pi(S):
    return S['index'] if 'res' not in S and 'index' in S else None


def _pf(S):
    return S['first'][S['char']] if _p2(S) and S['_line'] == 24 else None


def _pl(S):
    return S['last'][S['char']] if _p2(S) and S['_line'] == 24 else None


def _win_a(S):
    return _pf(S) + 1 if _pf(S) is not None else None


def _win_b(S):
    return _pl(S) - 1 if _pl(S) is not None else None


def _s_color(S, k, v):
    if 'res' not in S:
        i = S.get('index')
        if i is None:
            return None
        return 'blue' if k == i else ('cyan' if k < i else None)
    return None


def _table(S):
    if 'cnt_list' not in S:
        return None
    n = len(S['s'])
    rows = [[d.get(c, 0) for c in LET] for d in S['cnt_list']]
    return rows + [[''] * len(LET) for _ in range(n - len(rows))]


def _mid_col(S):
    m = S.get('mid_char')
    return LET.index(m) if m in LET else None


def _t_color(S, i, j, v):
    if 'res' not in S or not _p2(S) or S['_line'] != 24:
        return None
    if j != _mid_col(S):
        return None
    if i == S['last'][S['char']] - 1:
        return 'orange'
    if i == S['first'][S['char']]:
        return 'cyan'
    return None


def _formula(S):
    if 'cnt_list' not in S:
        return '先一趟遍历记下每个字母的首次、末次位置，再建一张“前缀计数表”'
    if 'res' not in S:
        return f'`first = {S["first"]}`　`last = {S["last"]}`'
    if _p2(S) and S['_line'] == 24 and 'cnt' in S:
        f, l, m = S['first'][S['char']], S['last'][S['char']], S['mid_char']
        a, b = S['cnt_list'][l - 1].get(m, 0), S['cnt_list'][f].get(m, 0)
        return (f'两侧 `{S["char"]}`：首次 {f}、末次 {l}；中间 `{m}`：`cnt_list[{l - 1}][{m}] − cnt_list[{f}][{m}]` '
                f'= {a} − {b} = =={S["cnt"]}==')
    return '枚举两侧字母 a~z；出现不止一次的字母，才可能作回文子序列的两端'


CONFIG = dict(
    num=1930, title='长度为 3 的不同回文子序列', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举两侧 · 首末位置 + 前缀计数表',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1533'],
    code='''
class Solution(object):
    def countPalindromicSubsequence(self, s):
        first = {}
        last = {}
        cnt_list = []
        for index, char in enumerate(s):
            if char not in first:
                first[char] = index
            last[char] = index
            if index == 0:
                cnt_list.append({char : 1})
            else:
                cnt_list.append(cnt_list[-1].copy())
                cnt_list[-1][char] = cnt_list[-1].get(char, 0) + 1

        res = 0
        for asc in range(97, 123):
            char = chr(asc)
            if char in first and first[char] != last[char]:
                for mid_asc in range(97, 123):
                    mid_char = chr(mid_asc)
                    cnt = cnt_list[last[char] - 1].get(mid_char, 0) - cnt_list[first[char]].get(mid_char, 0)
                    if cnt > 0:
                        res += 1

        return res
''',
    call=f'Solution().countPalindromicSubsequence({STR!r})',
    expect=3,
    skip=['for asc in range', 'char = chr(asc)', 'if char in first and', 'for mid_asc in range', 'mid_char = chr',
          'cnt = cnt_list[last', 'if cnt > 0'],
    views=[
        dict(type='text', fn=_formula, size=26, h=90),
        dict(type='string', var='s', label='s（蓝 = 扫描位置；粉 / 橙 = 首次 / 末次；框 = 夹在中间）', cell=96,
             pointers={_pi: 'blue', _pf: 'pink', _pl: 'orange'},
             pointer_labels={_pi: 'index', _pf: 'first', _pl: 'last'},
             window=(_win_a, _win_b), color=_s_color, h=240),
        dict(type='table', var=_table, rows=[f'{i}:{c}' for i, c in enumerate(STR)], cols=LET, cell=64,
             label='cnt_list[i]：s[0..i] 里每个字母出现几次（前缀计数表）', color=_t_color, h=360),
    ],
    watch=['index', ('char', 'char', 'pink'), ('mid_char', 'mid_char', 'cyan'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'first = {}': '`first[c]`：字母 `c` ==第一次==出现的下标',
        'last = {}': '`last[c]`：字母 `c` ==最后一次==出现的下标',
        'cnt_list = []': '`cnt_list[i]`：前缀 `s[0..i]` 里每个字母出现的次数，相当于一张前缀和',
        'for index, char in enumerate(s)': lambda S, B, ret: ('第一遍扫描结束' if 'index' in B and S.index == B.index
                                                              else f"扫描 `s[{S.index}] = '{S.char}'`"),
        'if char not in first': lambda S, B, ret: (f"`'{S.char}'` 还没出现过 → 这是它的第一次" if S.char not in B.first
                                                   else f"`'{S.char}'` 之前出现过，`first` 保持不变"),
        'first[char] = index': "`first['{char}'] = {index}`：只在第一次出现时记录",
        'last[char] = index': "`last['{char}'] = {index}`：每次都覆盖，扫完就是最后一次",
        'if index == 0': lambda S, B, ret: ('第 0 个前缀没有“上一个”可抄' if S.index == 0 else '不是第 0 个，要在上一个前缀的基础上加'),
        'cnt_list.append({char : 1})': "第 0 个前缀：只有 `'{char}'` 一个，次数 1",
        'cnt_list.append(cnt_list[-1].copy())': '先==复制==上一个前缀的计数（必须 `copy`，否则所有行共用同一个字典）',
        'cnt_list[-1][char] =': "再把 `'{char}'` 的次数加一 → `cnt_list[{index}] = {cnt_list[-1]}`",
        'res = 0': '计数器 `res = 0`。下面枚举 a~z 当两侧字母 `char`：只有出现 ≥ 2 次的才可能；视频只演示命中的那几步',
        'res += 1': lambda S, B, ret: (
            f"两侧字母 `'{S.char}'`：首次 {S.first[S.char]}、末次 {S.last[S.char]} → 中间字母 `'{S.mid_char}'` 在 "
            f"`({S.first[S.char]}, {S.last[S.char]})` 里出现了 `cnt = {S.cnt}` 次，`cnt > 0` → 存在 "
            f"`{S.char}{S.mid_char}{S.char}`，`res` = =={S.res}=="),
        'return res': '`26 × 26` 种组合都试过了，返回 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='两侧字母取最外层的首末位置，数中间有几种不同字母',
        complexity='时间 `O(n·|Σ|)`，空间 `O(n·|Σ|)`，`|Σ| = 26`',
        problem=['数 `s` 中长度为 3 的==不同==回文子序列个数；相同内容只算一次',
                 '回文：第一个字母 = 第三个字母',
                 '示例：`"aabca"` → `3`（`aba`、`aaa`、`aca`）',
                 '本视频：`"aabca"`；字母 a~z 共 26 种，只演示命中的步骤'],
        quote='为了使得字符串中更容易出现枚举到的子序列，那么显然应该让两边的字符尽量靠边。换言之，对于枚举到的两边的字符，应该选择该字符串第一次出现和最后一次的位置作为两边。',
        quote_src='—— yiduobo 题解原文',
        idea=['为了不重复，枚举两侧字母 `char`（a~z），再枚举中间字母（a~z）',
              '`char` 取首次、末次出现位置，中间的选择最多',
              '“区间里有没有某字母”用前缀计数表做差：`cnt_list[last-1] − cnt_list[first]`',
              '只出现一次的字母（`first == last`）不能当两侧'],
        summary=['时间 `O(n·|Σ|)`：建表每步复制 26 项的字典，枚举 `26 × 26` 次',
                 '空间 `O(n·|Σ|)`，比灵神的位运算版多了前缀表',
                 '易错：`cnt_list[last[char] - 1]`，要减 1：末次位置本身是右端的 `char`，不能算作中间',
                 '易错：`cnt_list.append(cnt_list[-1].copy())` 必须 `copy`',
                 '原文为 Python 2 风格写法（`class Solution(object)`），代码未改，只删去了空行里的缩进空格',
                 '对比灵神：灵神枚举中间字母 + 位运算集合；yiduobo 是枚举两侧 + 前缀计数'],
    ),
)

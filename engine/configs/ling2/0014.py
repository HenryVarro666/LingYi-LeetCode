STRS = ['flower', 'flow', 'flight']


def _row(S):
    """当前这一行（for s in strs 没有下标，按字符串找回行号；示例里三个串互不相同）"""
    if S.get('_line') not in (5, 6, 7):
        return None
    s = S.get('s')
    strs = S.get('strs') or []
    return strs.index(s) if s in strs else None


def _color(S, i, j, v):
    col = S.get('j')
    if col is None:
        return None
    if j < col:
        return 'green'          # 已确认的公共前缀列
    if j == col and S.get('_line') != 4:
        r = _row(S)
        if r is None:
            return None
        s = S['strs'][r]
        ok = col < len(s) and s[col] == S['c']
        if S.get('_line') == 7 and i == r:
            return 'red'        # 就是这里缺失 / 不同
        if i < r or (i == r and S.get('_line') == 6 and ok):
            return 'cyan'       # 这一列已经比较过、和 c 相同
    return None


def _formula(S):
    if 'j' not in S:
        return '竖着看：每一列都相同，才属于公共前缀'
    j, c = S['j'], S['c']
    return f'第 `j = {j}` 列，标准字母 `c = s0[{j}] = \'{c}\'`；已确认前缀 `s0[:{j}]` = =={S["s0"][:j] or "（空）"}=='


def _if_cap(S, B, ret):
    s, j, c = S.s, S.j, S.c
    if j == len(s):
        return f'`"{s}"` 只有 {len(s)} 个字母：第 {j} 列==缺失== → 前缀到此为止'
    if s[j] != c:
        return f'`"{s}"[{j}] = \'{s[j]}\'` ≠ `c = \'{c}\'`：这一列==不全一样== → 前缀到此为止'
    return f'`"{s}"[{j}] = \'{s[j]}\'` = `c`，这一行没问题，继续往下看'


def _for_j(S, B, ret):
    if 'j' not in B or S.get('j') != B.get('j'):
        return f'从左到右看第 `j = {S.j}` 列，用第一个串的字母 `c = \'{S.c}\'` 当标准'
    return '`s0` 的每一列都看完了'


CONFIG = dict(
    num=14, title='最长公共前缀', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='竖着看 · 逐列比较',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        s0 = strs[0]
        for j, c in enumerate(s0):  # 从左到右
            for s in strs:  # 从上到下
                if j == len(s) or s[j] != c:  # 这一列有字母缺失或者不同
                    return s0[:j]  # 0 到 j-1 是公共前缀
        return s0
''',
    call=f'Solution().longestCommonPrefix({STRS})',
    expect='fl',
    views=[
        dict(type='text', fn=_formula),
        dict(type='grid', var='strs', label='strs 竖着排（绿 = 公共前缀列，青 = 本列已比较，红 = 缺失/不同）', h=470, cell=112,
             rows=lambda S: list(range(len(S['strs']))), cols=lambda S: list(range(max(len(x) for x in S['strs']))),
             color=_color, cursors=[(_row, 'j', 'yellow')]),
    ],
    watch=[('j', 'j', 'yellow'), ('c', 'c', 'cyan'), ('s', 's', 'blue'), ('s0', 's0')],
    captions={
        's0 = strs[0]': '拿第一个串 `s0 = "{s0}"` 当标准：公共前缀一定是它的前缀',
        'for j, c in': _for_j,
        'for s in strs': lambda S, B, ret: (f'从上到下，检查 `"{S.s}"` 的第 {S.j} 列' if B.get('s') != S.s or B.get('j') != S.j
                                            else f'第 {S.j} 列全是 `\'{S.c}\'` → ==这一列属于公共前缀==，看下一列'),
        'if j == len(s)': _if_cap,
        'return s0[:j]': '第 {j} 列不全一样 → 列 `0..{j - 1}` 才是公共前缀：返回 =={ret}==',
        'return s0': '每一列都相同 → 整个 `s0` 就是公共前缀',
    },
    cards=dict(
        one_liner='把字符串竖着排，从左到右一列一列看，第一列不全相同就停',
        complexity='时间 `O(nm)`，空间 `O(1)`（`m` 为最短串长度）',
        problem=['给一个字符串数组 `strs`，求它们的==最长公共前缀==',
                 '不存在公共前缀时返回空串 `""`',
                 '示例：`["flower","flow","flight"]` → `"fl"`'],
        quote='从左到右，竖着看，第一列全是 f，第二列全是 l，第三列就不全一样了，所以「最长公共前缀」是 fl。',
        quote_src='—— 灵茶山艾府题解',
        idea=['外层从左到右枚举列 `j`，以 `s0[j]` 为标准字母 `c`',
              '内层从上到下：==`j == len(s)`（缺失）或 `s[j] != c`（不同）== 就返回 `s0[:j]`',
              '没有中途返回 → 所有串都以 `s0` 为前缀，答案就是 `s0`'],
        result='返回 `"fl"`：第 2 列出现了 `o / o / i`，不全一样',
        summary=['时间 `O(nm)`：最多看 `m` 列，每列 `n` 个字母；空间 `O(1)`',
                 '易错：先判 `j == len(s)` 再取 `s[j]`，==短路求值防越界==',
                 '`return s0[:j]` 取的是列 `0..j-1`，不含出问题的第 `j` 列',
                 '另一种写法：`zip(*strs)` 按列打包，`len(set(col)) > 1` 就停'],
    ),
)

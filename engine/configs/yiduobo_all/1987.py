def _done(S):
    """已处理（从后往前）的字符个数：用 (zero_cnt, one_cnt) 在模拟序列里定位"""
    rev = S['binary'][::-1]
    zc = oc = 0
    if (zc, oc) == (S['zero_cnt'], S['one_cnt']):
        return 0
    for k, c in enumerate(rev):
        if c == '0':
            zc += oc + 1
        else:
            oc += zc + 1
        if (zc, oc) == (S['zero_cnt'], S['one_cnt']):
            return k + 1
    return len(rev)


def _cur(S):
    if 'zero_cnt' not in S or 'char' not in S:
        return None
    m = _done(S)
    return m if S['_line'] in (8, 9) else m - 1


def _color(S, i, v):
    cur = _cur(S)
    if cur is None:
        return None
    if i == cur:
        return 'blue'
    return 'green' if i < cur else None


def _top(S):
    if 'zero_cnt' not in S:
        return '从后往前扫：`zero_cnt` / `one_cnt` 是以 0 / 1 开头的不同子序列数'
    if 'char' not in S:
        return '先准备计数器'
    if S['_line'] >= 19:
        return f"以 1 开头：`one_cnt = {S['one_cnt']}`；有 0 → 再加单独的 `0`"
    return f"当前字符 `{S['char']}`：以 0 开头 =={S['zero_cnt']}==，以 1 开头 =={S['one_cnt']}=="


CONFIG = dict(
    num=1987, title='不同的好子序列数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='反向遍历 · 去重计数 DP',
    tags=['灵神题单', '难度分 2422'],
    code='''
class Solution(object):
    def numberOfUniqueGoodSubsequences(self, binary):

        zero_cnt = 0
        one_cnt = 0
        mod = 10 ** 9 + 7
        zero_flag = False
        for char in binary[::-1]:
            if char == '0':
                zero_cnt += one_cnt + 1
                if zero_cnt >= mod:
                    zero_cnt -= mod
                zero_flag = True
            else:
                one_cnt += zero_cnt + 1
                if one_cnt >= mod:
                    one_cnt -= mod
        
        res = one_cnt
        if zero_flag:
            res += 1
            if res >= mod:
                res -= mod
        return res
''',
    call='Solution().numberOfUniqueGoodSubsequences("1011")',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=28, h=90),
        dict(type='string', var='binary[::-1]', label='binary 反过来（蓝 = 当前字符，绿 = 已处理）', cell=110, h=210, color=_color),
        dict(type='text', fn=lambda S: ('`以 0 开头 = %s`   `以 1 开头 = %s`   `有 0：%s`' % (S['zero_cnt'], S['one_cnt'], '是' if S['zero_flag'] else '否')) if 'zero_flag' in S else '', size=30, h=100),
    ],
    watch=[('char', 'char', 'blue'), ('zero_cnt', 'zero_cnt', 'pink'), ('one_cnt', 'one_cnt', 'cyan'), ('zero_flag', 'zero_flag'), ('res', 'res', 'green')],
    captions={
        'zero_cnt = 0': '`zero_cnt`：已扫过的后缀里，==以 0 开头==的不同子序列数',
        'one_cnt = 0': '`one_cnt`：==以 1 开头==的不同子序列数。倒着扫，开头就是新加的字符',
        'mod =': '答案取模 `10^9 + 7`',
        'zero_flag = False': '`zero_flag`：二进制串里有没有 0，单独的 `"0"` 是合法的',
        'for char in': lambda S, B, r: ('扫描结束，只有以 1 开头的才合法' if _done(S) == len(S.binary) and S._line == 8 and 'char' in B and B.get('char') == S.char and _done(B) == len(S.binary) else f"从后往前取 `char = '{S.char}'`"),
        "if char == '0'": lambda S, B, r: ("`char = '0'`：把它接在所有已有子序列前面，再加单独的 `0`" if S.char == '0' else "`char = '1'`：把它接在所有已有子序列前面，再加单独的 `1`"),
        'zero_cnt += one_cnt': '`zero_cnt = {B.zero_cnt} + {one_cnt} + 1 = {zero_cnt}`：前面接 `0`，后面可跟任何已有子序列（0 开头 / 1 开头），再 +1 是单独的 `0`',
        'zero_flag = True': '出现了 `0`：最后要给答案补上单独的 `"0"`',
        'one_cnt += zero_cnt': '`one_cnt = {B.one_cnt} + {zero_cnt} + 1 = {one_cnt}`：前面接 `1`，后面接已有的 0 / 1 开头子序列，再 +1 是单独的 `1`',
        'if zero_cnt >= mod': '防止溢出：减法取模，不用 `%`',
        'if one_cnt >= mod': '防止溢出：减法取模，不用 `%`',
        'res = one_cnt': '以 `0` 开头的子序列有前导 0，全部不要；只留 `one_cnt = {one_cnt}`',
        'if zero_flag': lambda S, B, r: ('串里有 `0` → 单独的 `"0"` 也合法，答案 +1' if S.zero_flag else '串里没有 `0`，不用补'),
        'res += 1': '`res = {res}`：补上单独的 `"0"`',
        'return res': '不同的好子序列共 `{ret}` 个',
    },
    cards=dict(
        one_liner='倒着扫，开头是新加的字符，既去重又避开前导 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `binary` 的子序列：==非空，且没有前导 0==（单独的 `"0"` 除外）才是好的',
                 '统计==不同==的好子序列数，对 `10^9+7` 取模',
                 '示例：`"101"` → `5`；本视频：`"1011"`'],
        quote='对于去重，可以在动态规划的过程中通过状态转移方程来实现，而对于前导0，有一种常见的技巧是反向计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['从后往前扫，`f[i][j]` 表示倒数 `i` 个字符里、以 `j` 开头的合法子序列数',
              '字符 `char` 要么接在已有子序列前面，要么单独成一个：`f = f0 + f1 + 1`',
              '不会丢子序列：旧的 `char` 开头串，换成当前这个 `char` 得到同样的字符串'],
        summary=['时间 `O(n)`，空间 `O(1)`：只留 `zero_cnt`、`one_cnt` 两个数',
                 '以 0 开头的都不合法，答案是 `one_cnt`；有 `0` 再 +1 补单独的 `"0"`',
                 '易错：不能把 `"0"` 漏掉，也不能写成 `one_cnt + zero_cnt`',
                 '原文已是 Python 3 可运行的写法，代码未改动；取模用「减 mod」而不是 `%`'],
    ),
)

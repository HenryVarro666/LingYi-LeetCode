ORIG = [[0, 1, 1], [1, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 0]]
GROUP = ['blue', 'green', 'purple', 'cyan', 'pink']


def _bits(r):
    return ''.join(map(str, r))


def _comp(r):
    return ''.join('1' if x == 0 else '0' for x in r)


def _group(S, r):
    d = S.get('row_dict') or {}
    keys = list(d)
    for key in (_comp(S['matrix'][r]), _bits(S['matrix'][r])):
        if key in keys:
            return GROUP[keys.index(key) % len(GROUP)]
    return None


def _color(S, i, j, v):
    k = S.get('index')
    if k is None:
        return None
    line = S.get('_line')
    done = i < k or (i == k and line in (17, 19, 21))
    if done:
        return _group(S, i)
    if i == k:
        if line in (11, 14) and j == len(S.get('t', '')) - 1:
            return 'orange'
        return 'yellow'
    return None


def _text(S):
    k = S.get('index')
    if k is None:
        return '`t` = 这一行本身，`s` = 它的==互补行=='
    return f"第 {k} 行 `{_bits(S['matrix'][k])}`：`t` 照抄，`s` 取反（0 ↔ 1）"


def _check(S, B, ret):
    if S.s in S.row_dict:
        return f'`s = {S.s}` 在表里：键是某组首行的互补串 → 本行与那一行==完全一致=='
    return f'`s = {S.s}` 不在表里：前面没有和本行完全一致的组'


def _check_t(S, B, ret):
    if S.t in S.row_dict:
        return f'`t = {S.t}` 在表里：本行就是那一组首行的互补串 → 两行==正好互补=='
    return f'`t = {S.t}` 也不在表里：既没有一致的，也没有互补的 → 新的一组'


CONFIG = dict(
    num=1072, title='按列翻转得到最大值等行数', difficulty='Medium', category='哈希',
    author='yiduobo', technique='一致或互补的行翻转后同步 · 哈希计数',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def maxEqualRowsAfterFlips(self, matrix):
        m = len(matrix)
        row_dict = {}
        for index in range(m):
            s = ''
            t = ''
            for num in matrix[index]:
                if num == 0:
                    s += '1'
                    t += '0'
                else:
                    t += '1'
                    s += '0'

            if s in row_dict:
                row_dict[s] += 1
            elif t in row_dict:
                row_dict[t] += 1
            else:
                row_dict[s] = 1

        return max(row_dict.values())
''',
    call=f'Solution().maxEqualRowsAfterFlips({ORIG})',
    expect=3,
    skip=['for num in', 'if num == 0', "s += '1'", "t += '1'", "s = ''", "t = ''", 'else:'],
    views=[
        dict(type='text', h=70, size=28, fn=_text),
        dict(type='grid', var='matrix', h=430, cell=90, rows=[0, 1, 2, 3, 4], cols=[0, 1, 2], color=_color,
             label='matrix（黄 = 当前行，橙 = 刚读的数，同色 = 同一组）'),
        dict(type='text', h=80, size=32, fn=lambda S: (f"本行 `t = '{S['t']}'`　　互补行 `s = '{S['s']}'`" if 't' in S and 's' in S else '')),
        dict(type='map', var='row_dict', h=150, fmt=lambda k, v: f'{k} : {v}', label='row_dict（键 = 每组首行的互补串）'),
    ],
    watch=[('index', 'index', 'yellow'), ('s', 's', 'pink'), ('t', 't', 'blue'),
           ('max', 'max(row_dict.values()) if row_dict else 0', 'green')],
    captions={
        'm = len(matrix)': '`m = {m}` 行',
        'row_dict = {}': '`row_dict`：每一组（一致或互补的行）出现的次数',
        'for index in range(m)': lambda S, B, r: ('所有行都处理完了' if getattr(B, 'index', None) == S.index
                                                  else f'处理第 {S.index} 行 `{_bits(S.matrix[S.index])}`'),
        "t += '0'": '读到 `0`：`s` 追加 `1`，`t` 追加 `0` → `s = {s}`，`t = {t}`',
        "s += '0'": '读到 `1`：`t` 追加 `1`，`s` 追加 `0` → `s = {s}`，`t = {t}`',
        'if s in row_dict': _check,
        'row_dict[s] += 1': '`row_dict[{s}]` → {row_dict[s]}：完全一致的行，翻转后也完全一致',
        'elif t in row_dict': _check_t,
        'row_dict[t] += 1': '`row_dict[{t}]` → {row_dict[t]}：正好互补的行，翻转后仍互补，能同时变成全 0 / 全 1',
        'row_dict[s] = 1': '以本行的互补串 `s` 为键新建一组：`row_dict[{s}] = 1`',
        'return max': '次数最大的一组有 `{ret}` 行 → 答案 `{ret}`',
    },
    cards=dict(
        one_liner='初始一致或互补的两行，翻转任意列后仍然一致或互补',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的 01 矩阵，可以任选若干列，把列上每个格子翻转',
                 '求翻转后==行内所有值都相等==的行最多有几行',
                 '示例：`[[0,1],[1,0]]` → `2`；本视频 5 行 → `3`'],
        quote='若两行初始状况下完全一致，那么翻转之后也将是完全一致。同样地，若两行初始状态下正好互补，那么翻转之后也将是正好互补。',
        quote_src='—— yiduobo 题解原文',
        idea=['设最终把第 k 行翻成了全等，其他全等的行要么==与第 k 行一致==，要么==正好互补==',
              '所以答案 = 某一行「一致 + 互补」的行数的最大值',
              '每行生成本身 `t` 和互补 `s`：查到 `s` 或 `t` 就计数 +1，否则用 `s` 新建一组'],
        summary=['时间 `O(mn)`：每行拼两个长 n 的字符串；空间 `O(mn)`',
                 '一组只存一个键：先查 `s` 再查 `t`，都没有才新建，避免同一组被拆成两个键',
                 '易错：字符串 `+=` 在 C++/Java 里可能是 `O(n²)`，可以改用 StringBuilder',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：灵神把首位为 1 的行原地翻转，用 `tuple` 直接计数'],
    ),
)

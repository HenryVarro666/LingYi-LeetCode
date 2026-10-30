ORIG = [[0, 1, 1], [1, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 0]]
GROUP = ['blue', 'green', 'purple', 'cyan', 'pink']


def _ri(S):
    """当前 row 在 matrix 中的下标（快照里 row 和 matrix[i] 是同一个对象）"""
    row, mat = S.get('row'), S.get('matrix')
    if row is None or mat is None:
        return None
    for k, r in enumerate(mat):
        if r is row:
            return k
    return None


def _keys(S):
    out = []
    for r in S['matrix']:
        t = tuple(r)
        if t not in out:
            out.append(t)
    return out


def _color(S, i, j, v):
    k = _ri(S)
    if k is None:
        return None
    done = i < k or (i == k and S.get('_line') == 8)
    if done:
        cnt = S.get('cnt') or {}
        keys = [t for t in cnt]
        t = tuple(S['matrix'][i])
        return GROUP[keys.index(t) % len(GROUP)] if t in keys else None
    if i == k:
        if S.get('_line') == 7 and j == S.get('j'):
            return 'orange'
        return 'yellow'
    return None


def _bits(r):
    return ''.join(map(str, r))


def _row_text(S):
    k = _ri(S)
    if k is None:
        return '把==第一个数为 1== 的行全部翻转，互补的行就变成相同的行'
    cur = _bits(S['matrix'][k])
    orig = _bits(ORIG[k])
    if orig == cur:
        return f"第 {k} 行 `{orig}`" + ('：第一个数是 0，==不用翻转==' if ORIG[k][0] == 0 else '')
    return f"第 {k} 行 `{orig}` → 翻转成 `{cur}`（与原行==互补==）"


CONFIG = dict(
    num=1072, title='按列翻转得到最大值等行数', difficulty='Medium', category='哈希',
    author='灵茶山艾府', technique='逆向思维 · 相同或互补的行归一化后计数',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def maxEqualRowsAfterFlips(self, matrix: List[List[int]]) -> int:
        cnt = Counter()
        for row in matrix:
            if row[0]:  # 翻转第一个数为 1 的行
                for j in range(len(row)):
                    row[j] ^= 1
            cnt[tuple(row)] += 1
        return max(cnt.values())
''',
    call=f'Solution().maxEqualRowsAfterFlips({ORIG})',
    expect=3,
    skip=['for j in range'],
    views=[
        dict(type='text', h=70, size=28, fn=_row_text),
        dict(type='grid', var='matrix', h=430, cell=96, rows=[0, 1, 2, 3, 4], cols=[0, 1, 2], color=_color,
             label='matrix（原地翻转；黄 = 当前行，同色 = 同一组）'),
        dict(type='map', var='cnt', h=200, fmt=lambda k, v: f"{_bits(k)} : {v}", label='cnt（归一化后的行 → 出现次数）'),
    ],
    watch=[('row', 'row'), ('row[0]', 'row[0]', 'yellow'),
           ('max', 'max(cnt.values()) if cnt else 0', 'green')],
    captions={
        'cnt = Counter()': '`cnt` 统计每种（归一化后的）行出现几次',
        'for row in matrix': lambda S, B, r: ('所有行都统计完了' if _ri(B) == _ri(S)
                                              else f'看第 {_ri(S)} 行：`{_bits(S.row)}`'),
        'if row[0]': lambda S, B, r: (f'`row[0] = 1` → 把整行翻转，变成以 0 开头的==互补行==' if S.row[0]
                                      else '`row[0] = 0`：已经以 0 开头，不用翻转'),
        'row[j] ^= 1': '`row[{j}]` 异或 1：`{B.row[j]}` → `{row[j]}`',
        'cnt[tuple(row)] += 1': lambda S, B, r: (f'`{_bits(S.row)}` 出现 `{S.cnt[tuple(S.row)]}` 次：'
                                                 + ('==和前面的行相同或互补==，同一种翻转能让它们一起全等' if S.cnt[tuple(S.row)] > 1
                                                    else '新的一组')),
        'return max': '最大的一组有 `{ret}` 行：按这组的方式翻转列，这 `{ret}` 行都全 0 或全 1',
    },
    cards=dict(
        one_liner='相同或互补的行，一定能被同一组列翻转变成全 0 / 全 1',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的 01 矩阵，可以任选若干列，把列上每个格子翻转',
                 '求翻转后==行内所有值都相等==的行最多有几行',
                 '示例：`[[0,0,0],[0,0,1],[1,1,0]]` → `2`；本视频 5 行 → `3`'],
        quote='对于相同的行，或者「互补」的行，一定存在一种翻转方式，可以使这些行最终全为 0 或者全为 1。……为了统计互补的行，可以把第一个数为 1 的行全部翻转。',
        quote_src='—— 灵茶山艾府题解',
        idea=['倒着想：全 0 / 全 1 的行，翻转最后一列变成 `001` / `110`，仍然==互补==',
              '图论视角：相同或互补的行连边，答案 = 最大连通块大小',
              '不用建图：把首位为 1 的行翻转，互补行就变成相同行，`tuple` 放进哈希表计数'],
        summary=['时间 `O(mn)`：每个格子最多翻转一次；空间 `O(mn)` 存哈希键',
                 '关键：首位为 1 就整行翻转，==互补的两行映射到同一个键==',
                 '易错：list 不能当字典键，要转成 `tuple`',
                 '这份代码会原地修改 matrix；C++/Java 转字符串，Go 压成 uint64 数组'],
    ),
)

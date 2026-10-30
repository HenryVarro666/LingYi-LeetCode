G = [[1, 2, 3], [3, 1, 5], [3, 2, 1]]


def _bits(st):
    return {x for x in range(64) if st >> x & 1}


def _diag(S, i, j):
    return 'k' in S and 'n' in S and i - j + S['n'] == S['k']


def _seen(S, i, j):
    """这一步结束时，已经被加进 st 的对角线格子"""
    ln, cj = S.get('_line'), S.get('j')
    if not isinstance(cj, int):
        return False
    if ln == 13:
        return j < cj
    if ln == 19:
        return j > cj
    return False


def _cell(S, i, j, v):
    if S.get('_line') in (21, 6) or not _diag(S, i, j):
        return None
    if _seen(S, i, j):
        return 'cyan' if S['_line'] == 13 else 'orange'
    return 'blue'


def _ci(S):
    return S['k'] + S['j'] - S['n'] if S.get('_line') in (13, 19) else None


def _cj(S):
    return S['j'] if S.get('_line') in (13, 19) else None


def _c13(S):
    i, j = S.k + S.j - S.n, S.j
    prior = [S.grid[S.k + jj - S.n][jj] for jj in range(S.min_j, j)]
    t = S.ans[i][j]
    if not prior:
        return f'`({i},{j})` 左上没有数 → `top_left = {t}`；再把 `{S.grid[i][j]}` 加入 st'
    dup = '（重复只算一种）' if len(prior) != len(set(prior)) else ''
    return f'`({i},{j})` 左上 {prior}{dup} → `top_left = {t}`'


def _c19(S, B):
    i, j = S.k + S.j - S.n, S.j
    later = [S.grid[S.k + jj - S.n][jj] for jj in range(S.max_j, j, -1)]
    t = S.st.bit_count()
    top = B.ans[i][j]
    if not later:
        return f'`({i},{j})` 右下没有数 → `bottom_right = 0`，`|{top} − 0|` = =={S.ans[i][j]}=='
    dup = '（重复只算一种）' if len(later) != len(set(later)) else ''
    return f'`({i},{j})` 右下 {later}{dup} → `bottom_right = {t}`，`|{top} − {t}|` = =={S.ans[i][j]}=='


def _hint(S):
    ln = S.get('_line')
    st = S.get('st')
    if st is None or 'k' not in S:
        return '每条对角线：先左上→右下统计“左边有几种数”，再右下→左上统计“右边有几种数”'
    b = bin(st)[2:] if st else '0'
    s = f'`st = 0b{b}`，第 {sorted(_bits(st))} 位是 1 → {len(_bits(st))} 种不同的数' if st else '`st = 0`：空集合'
    if ln in (13, 10):
        return '左上方向：' + s
    if ln in (19, 16):
        return '右下方向：' + s
    return s


CONFIG = dict(
    num=2711, title='对角线上不同值的数量差', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前后缀分解 · 位运算集合',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1429'],
    code='''
class Solution:
    def differenceOfDistinctValues(self, grid: List[List[int]]) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        ans = [[0] * n for _ in range(m)]

        for k in range(1, m + n):
            min_j = max(n - k, 0)
            max_j = min(m + n - 1 - k, n - 1)

            st = 0
            for j in range(min_j, max_j + 1):
                i = k + j - n
                ans[i][j] = st.bit_count()  # 计算 st 中 1 的个数
                st |= 1 << grid[i][j]  # 把 grid[i][j] 加到 st 中

            st = 0
            for j in range(max_j, min_j - 1, -1):
                i = k + j - n
                ans[i][j] = abs(ans[i][j] - st.bit_count())
                st |= 1 << grid[i][j]
        return ans
''',
    call=f'Solution().differenceOfDistinctValues({G})',
    expect=[[1, 1, 0], [1, 0, 1], [0, 1, 1]],
    skip=[7, 8, 11, 12, 14, 17, 18, 20],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前对角线，青 = 已入集合的左上格，橙 = 已入集合的右下格）', cell=84, h=290,
             color=_cell, cursors=[(_ci, _cj, 'pink')]),
        dict(type='grid', var='ans', label='ans（先存 top_left，再变成 |top_left − bottom_right|）', cell=84, h=290),
        dict(type='set', var=lambda S: _bits(S['st']) if 'st' in S else None,
             label='st（二进制数：第 x 位为 1 ⇔ x 在集合里）', fmt=lambda x: str(x), h=110),
        dict(type='text', fn=_hint, size=24, h=70),
    ],
    watch=[('k', 'k', 'blue'), ('j', 'j', 'pink'), ('st', 'bin(st) if "st" in locals() else None', 'cyan'),
           ('ans[i][j]', 'ans[i][j] if "i" in locals() else None', 'green')],
    captions={
        'm, n = len': '`m = {m}`，`n = {n}`：共 `m + n − 1 = {m + n - 1}` 条对角线',
        'ans = [[0]': '`ans` 先放 `top_left`，再改成差的绝对值',
        'for k in range': lambda S, B, r: (f'第 `k = {S.k}` 条对角线（`i − j + n = {S.k}`）'
                                           if 'k' not in B or S.k != B.k else '对角线全部处理完'),
        10: '`st = 0`，==左上→右下==扫；`j` 取 `[{min_j}, {max_j}]`',
        13: lambda S, B, r: _c13(S),
        16: '`st = 0`，==右下→左上==反向再扫一遍',
        19: lambda S, B, r: _c19(S, B),
        'return ans': '每格都得到差的绝对值 → 返回 `ans`',
    },
    cards=dict(
        one_liner='一条对角线当一维数组：前缀、后缀各扫一遍数不同值',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计）',
        problem=['格子 `(r, c)` 的左上对角线、右下对角线上各有若干数',
                 '`answer[r][c] = |左上不同值个数 − 右下不同值个数|`',
                 '示例：`[[1,2,3],[3,1,5],[3,2,1]]` → `[[1,1,0],[1,0,1],[0,1,1]]`'],
        quote='考察某一条对角线 d，把它视作一维数组。……我们可以从左到右遍历 d，同时把元素加到一个哈希集合中。遍历到 d[i] 时，哈希集合的大小就是 topLeft。',
        quote_src='—— 灵茶山艾府题解（方法二，方法三用位运算替代集合）',
        idea=['暴力法每个格子都重新走一遍对角线；同一条对角线被反复遍历',
              '把对角线看成一维数组：从左往右扫，集合大小就是 `top_left`；从右往左扫就是 `bottom_right`',
              '值域 `≤ 50`：用 64 位整数当集合，`1 << x` 加入，`bit_count()` 数种类'],
        summary=['时间 `O(mn)`：每个格子访问两次；空间 `O(1)`',
                 '易错：==先写 ans 再把自己加入集合==，左上/右下都不含格子自己',
                 '第二遍要把 `ans[i][j]` 里的 top_left 减去 bottom_right 再取绝对值',
                 '方法一暴力 `O(mn·min(m,n))`；方法二用哈希集合；本视频是方法三（位运算）',
                 '同类：1329、3446 对角线遍历模板（`k = i − j + n`）'],
    ),
)

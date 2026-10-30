MAT = [[1, 9]]
_DN = {(0, 1): '东', (1, 1): '东南', (1, 0): '南', (1, -1): '西南', (0, -1): '西', (-1, -1): '西北', (-1, 0): '北', (-1, 1): '东北'}


def _gen(S):
    """生成阶段的格子：起点 (i,j) 黄，当前 (x,y) 粉（只在 15~22 行有意义）"""
    return S.get('_line') in range(14, 23)


def _col(S, a, b, v):
    if 'i' not in S or 'd' not in S:
        return None
    ln = S.get('_line')
    if ln in range(11, 23) and (a, b) == (S['i'], S['j']):
        return 'yellow'
    return None


def _top(S):
    if 'v' not in S or 'd' not in S or S.get('_line') not in range(14, 23):
        return ''
    d = S['d']
    return f"起点 `({S['i']},{S['j']})`，向{_DN[(S['dx'][d], S['dy'][d])]}延伸，当前数字 `v = {S['v']}`"


def _chk(S):
    if S.get('_line') in range(25, 36) and 'v' in S and 'x' in S:
        return f"检测 `v = {S['v']}`：`x = {S['x']}`，`x×x = {S['x'] * S['x']}`"
    return ''


CONFIG = dict(
    num=3044, title='出现频率最高的质数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='先哈希计数，再逐个检测质数',
    tags=['灵神题单', '难度分 1737'],
    code='''
class Solution(object):
    def mostFrequentPrime(self, mat):

        num_dict = {}
        m = len(mat)
        n = len(mat[0])

        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]

        for i in range(m):
            for j in range(n):
                for d in range(8):
                    x, y, v = i, j, mat[i][j]
                    while True:
                        x += dx[d]
                        y += dy[d]
                        if 0 <= x < m and 0 <= y < n:
                            v = v * 10 + mat[x][y]
                            num_dict[v] = num_dict.get(v, 0) + 1
                        else:
                            break

        res = -1
        for v in num_dict:
            x = 2
            flag = True
            while x * x <= v:
                if v % x == 0:
                    flag = False
                    break
                x += 1
            
            if flag and (res == -1 or num_dict[res] < num_dict[v] or (num_dict[res] == num_dict[v] and res < v)):
                res = v
        
        return res
''',
    call=f'Solution().mostFrequentPrime({MAT})',
    expect=19,
    max_steps=90,
    skip=['x, y, v = i, j', 'while True', 'x += dx[d]', 'y += dy[d]', 22, 'x += 1'],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='grid', var=lambda S: MAT, label='mat（黄 = 起点，粉 = 当前走到的格子）', cell=110, h=200,
             color=_col, cursors=[('x if _line in (15, 16, 17, 18, 19, 20) else None', 'y', 'pink')]),
        dict(type='map', var='num_dict', label='num_dict（所有生成的数字 → 出现次数，先不管是不是质数）', h=230),
        dict(type='text', fn=_chk, size=24),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('d', 'd'), ('v', 'v', 'yellow'), ('res', 'res', 'green')],
    captions={
        'num_dict = {}': '哈希表：==不管是不是质数==，先把所有生成的数字都计数',
        'dx = [': '八个方向的行偏移 `dx`',
        'dy = [': '八个方向的列偏移 `dy`，`d` 从 0 到 7 对应东、东南、南……',
        'for i in range(m)': '枚举起点所在行 `i = {i}`',
        'for j in range(n)': '起点 `({i},{j})`，数字 `{mat[i][j]}`',
        'for d in range(8)': lambda S, B, r: (f"方向 `d = {S.d}`：{_DN[(S.dx[S.d], S.dy[S.d])]}（`dx={S.dx[S.d]}`，`dy={S.dy[S.d]}`）"
                                              if 'd' in B and S.d != B.d or 'd' not in B else '8 个方向都走完了'),
        'if 0 <= x < m': lambda S, B, r: (f'沿方向走一步到 `({S.x},{S.y})`：在矩阵内 → 继续接数字' if 0 <= S.x < S.m and 0 <= S.y < S.n
                                          else f'沿方向走一步到 `({S.x},{S.y})`：出界 → ==这个方向结束==，换下一个'),
        'v = v * 10 + mat[x][y]': '接上 `mat[{x}][{y}] = {mat[x][y]}`：`{B.v} × 10 + {mat[x][y]}` = =={v}==',
        'num_dict[v] = num_dict.get': '`{v}` 出现次数 +1 → `num_dict[{v}] = {num_dict[v]}`',
        31: '`{v}` 有因子，不用再试了',
        'res = -1': '生成完毕，开始从 `num_dict` 里挑质数；`res = -1` 表示还没有',
        'for v in num_dict': '检测 `{v}`（出现 `{num_dict[v]}` 次）',
        'x = 2': '从 `x = 2` 开始试除',
        'flag = True': '先假定 `{v}` 是质数',
        'while x * x <= v': lambda S, B, r: (f'`x×x = {S.x * S.x} <= {S.v}`：继续试除' if S.x * S.x <= S.v
                                              else f'`x×x = {S.x * S.x} > {S.v}`：不会再有因子，结束试除'),
        'if v % x == 0': '`{v} % {x} = {v % x}` → {"==整除，不是质数==" if v % x == 0 else "不整除"}',
        'flag = False': '`{v}` 有因子 `{x}` → 不是质数',
        'x += 1': '`x` → {x}',
        'if flag and': lambda S, B, r: (f'`{S.v}` 不是质数，跳过' if not S.flag else
                                        (f'`{S.v}` 是质数，还没有候选 → 成为答案' if S.res == -1 else
                                         (f'`{S.v}` 是质数：出现 `{S.num_dict[S.v]}` 次，当前答案 `{S.res}` 出现 `{S.num_dict[S.res]}` 次 → '
                                          + ('==次数更多==，更新' if S.num_dict[S.res] < S.num_dict[S.v]
                                             else ('次数相同且更大，更新' if S.num_dict[S.res] == S.num_dict[S.v] and S.res < S.v
                                                   else '不更新'))))),
        'res = v': '`res = {res}`',
        'return res': '出现次数最多的质数（并列取最大）：`{res}`',
    },
    cards=dict(
        one_liner='先把所有生成的数字计数，最后再逐个检测质数',
        complexity='时间 `O(mnk·10^{k/2})`，空间 `O(mnk)`',
        problem=['`m × n` 矩阵，从每个格子出发沿 8 个方向之一直线走，沿途数字依次接成新数',
                 '返回所有生成的数里，==大于 10 的质数中出现频率最高==的；并列取最大；没有返回 `-1`',
                 '本视频：`[[1,9]]` → 生成 19、91 → 其中 19 是质数 → 答案 `19`'],
        quote='遍历矩阵中的每个数作为枚举的起点，然后向八个方向扩散，每次将当前数字加入到构造的数字的末位直到来到边界，在这个过程中将构造的所有数字都加入到哈希表中并统计出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模很小（最多 6×6，每个方向不超过 5 个数），可以暴力：`dx`、`dy` 数组表示 8 个方向',
              '生成的数字先==一律计数==，不判断质数',
              '枚举完再遍历哈希表，对每个数暴力试除；次数更多、或次数相同且更大就更新 `res`'],
        summary=['时间 `O(mnk·10^{k/2})`，空间 `O(mnk)`',
                 '易错：并列要取较大的质数；`res == -1` 时第一个质数直接成为答案',
                 '生成的数至少两位，所以一定大于 10，不用额外判断',
                 '对比灵神：灵神边生成边判断，并用 `val in cnt` 免去重复试除；这里先计数，最后每个不同的数只检测一次',
                 '原文代码已是 Python 3 可运行写法，未作修改'],
    ),
)

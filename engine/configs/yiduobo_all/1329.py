MAT = [[3, 3, 1], [2, 2, 1]]
PAL = {0: 'blue', -1: 'pink', -2: 'green', 1: 'purple', -3: 'cyan', 2: 'orange'}


def _mcell(S, i, j, v):
    """第一阶段：已收集进字典的格子，按所属对角线 (i-j) 着色"""
    ln, ci, cj = S.get('_line'), S.get('i'), S.get('j')
    if ln not in (9, 10, 11) or not isinstance(ci, int):
        return None
    if (i, j) < (ci, cj) or ((i, j) == (ci, cj) and ln == 11):
        return PAL.get(i - j)
    return None


def _rcell(S, i, j, v):
    """第二阶段：已填好的格子，颜色表示它取自哪条对角线"""
    if v:
        return PAL.get(i - j)
    return None


def _mc(S, k):
    if S.get('_line') in (9, 10, 11) and 'i' in S and 'j' in S:
        return (S['i'], S['j'])[k]
    return None


def _rc(S, k):
    if S.get('_line') in (18, 19) and 'i' in S and 'j' in S:
        return (S['i'], S['j'])[k]
    return None


CONFIG = dict(
    num=1329, title='将矩阵按对角线排序', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='字典按 i−j 分组 · 排序后从末尾 pop 填回',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1548'],
    code='''
class Solution(object):
    def diagonalSort(self, mat):

        num_dict = {}
        m = len(mat)
        n = len(mat[0])
        for i in range(m):
            for j in range(n):
                if i - j not in num_dict:
                    num_dict[i - j] = []
                num_dict[i - j].append(mat[i][j])
        
        for key in num_dict.keys():
            num_dict[key] = sorted(num_dict[key])
        res = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n):
                res[i][j] = num_dict[i - j][-1]
                num_dict[i - j].pop()
        
        return res
''',
    call=f'Solution().diagonalSort({MAT})',
    expect=[[2, 1, 1], [2, 3, 3]],
    skip=[5, 6, 8, 17],
    views=[
        dict(type='grid', var='mat', label='mat（颜色 = 所属对角线 i−j，已收集的格子上色）', cell=100, h=250,
             color=_mcell, cursors=[(lambda S: _mc(S, 0), lambda S: _mc(S, 1), 'yellow')]),
        dict(type='map', var='num_dict', label='num_dict（键 = i − j，值 = 这条对角线上的数）',
             fmt=lambda k, v: f'{k:>2}: {v}', h=170, font=26),
        dict(type='grid', var='res', label='res（从最后一行往上填；颜色 = 取自哪条对角线）', cell=100, h=250,
             color=_rcell, cursors=[(lambda S: _rc(S, 0), lambda S: _rc(S, 1), 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('key', 'key', 'pink')],
    captions={
        4: '`num_dict`：键是 `i − j`，同一条对角线上的格子键相同',
        7: lambda S, B, r: ('全部格子都收集完了' if 'i' in B and S.i == B.i else f'第 `{S.i}` 行（`m = {S.m}`，`n = {S.n}`）'),
        9: lambda S, B, r: (f'`({S.i},{S.j})` 的 `i − j = {S.i - S.j}`，字典里==还没有==这条对角线 → 先新建'
                            if (S.i - S.j) not in S.num_dict else
                            f'`({S.i},{S.j})` 的 `i − j = {S.i - S.j}`，已有这条对角线 → 直接追加'),
        10: '新建 `num_dict[{i - j}] = []`',
        11: '追加 `mat[{i}][{j}] = {mat[i][j]}` → `num_dict[{i - j}] = {num_dict[i - j]}`',
        13: lambda S, B, r: ('每条对角线都排好序了' if 'key' in B and S.key == B.key
                             else f'对角线 `{S.key}` 现在是 `{S.num_dict[S.key]}`'),
        14: '排序 → `num_dict[{key}] = {num_dict[key]}`（升序，最大的在末尾）',
        15: '`res` 先全 0。接着从最后一行往上、每行从左到右填',
        16: lambda S, B, r: ('每一行都填完了' if 'i' in B and S.i == B.i == 0 else f'填第 `{S.i}` 行'),
        18: '`res[{i}][{j}]` ← `num_dict[{i - j}][-1]` = =={res[i][j]}==：这条对角线剩下的最大数',
        19: '`pop` 掉它：之后填到的格子更靠左上，拿到更小的数 → `num_dict[{i - j}] = {num_dict[i - j]}`',
        21: '每条对角线都是左上小、右下大 → 返回 `res`',
    },
    cards=dict(
        one_liner='按 i−j 分组收集，排序后从下往上取最大的填回',
        complexity='时间 `O(mn log min(m,n))`，空间 `O(mn)`',
        problem=['`m × n` 矩阵，把每条右下方向的对角线上的数按==升序==排好',
                 '对角线从最上面一行或最左边一列出发，沿右下方向走',
                 '本视频：`[[3,3,1],[2,2,1]]` → `[[2,1,1],[2,3,3]]`'],
        quote='因此我们可以先根据行减列的值将矩阵中的所有格子分别收集起来，分别排序之后然后填充到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一条对角线上，行减列 `i − j` 都一样 → 用它当字典的键',
              '先扫整个矩阵，把每个数放进它的对角线列表；每个列表各自排序',
              '再从最后一行往上填：越靠右下越先填，每次 `pop` 当前最大的'],
        summary=['时间 `O(mn log min(m,n))`，空间 `O(mn)`（字典存了全部元素）',
                 '易错：填答案要从==最后一行往上==，才能保证右下拿到最大值',
                 '填完一个格子要 `pop` 掉，否则同一条对角线总取到同一个数',
                 '原文是 Python 2 风格，但可直接在 Python 3 运行，代码未改',
                 '灵神是按 `k = i − j` 一条条取出排序再放回，不用字典、空间更小'],
    ),
)

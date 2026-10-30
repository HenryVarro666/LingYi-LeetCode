_MAT = [[1, 3], [2, 4]]


def _inner(S):
    return S.get('_inner') or {}


def _grid_color(S, i, j, v):
    I = _inner(S)
    if 'x' in I and 'i' in I and I['i'] == i and I['x'] == v and I.get('_has_x', True):
        return 'yellow'
    return None


CONFIG = dict(
    num=1439, title='有序矩阵中的第 k 个最小数组和', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 回溯计数（剪枝）',
    tags=['二分算法', '常用数据结构', '难度分 2134'],
    code='''
class Solution:
    def kthSmallest(self, mat: List[List[int]], k: int) -> int:
        def check(s: int) -> bool:
            left_k = k
            # 返回是否找到 k 个子数组和
            def dfs(i: int, s: int) -> bool:
                if i < 0:  # 能递归到这里，说明数组和不超过二分的 s
                    nonlocal left_k
                    left_k -= 1
                    return left_k == 0  # 是否找到 k 个
                for x in mat[i]:  # 「枚举选哪个」，注意 mat[i] 是有序的
                    if x - mat[i][0] > s:  # 选 x 不选 mat[i][0]
                        break  # 剪枝：后面的元素更大，无需枚举
                    if dfs(i - 1, s - (x - mat[i][0])):  # 选 x 不选 mat[i][0]
                        return True  # 找到 k 个就一直返回 True，不再递归
                return False
            return dfs(len(mat) - 1, s - sl)  # 先把第一列的所有数都选上

        sl = sum(row[0] for row in mat)
        sr = sum(row[-1] for row in mat)
        return sl + bisect_left(range(sl, sr), True, key=check)
''',
    call='Solution().kthSmallest([[1, 3], [2, 4]], 3)',
    expect=5,
    views=[
        dict(type='grid', var=lambda S: _MAT, label='mat（黄 = 当前枚举的 x）', color=_grid_color, h=170, cell=70),
        dict(type='text', size=26, fn=lambda S: (
            f"二分的 `s` 满足：不超过 s 的数组和有 `f(s) ≥ k={S['k']}` 个吗？当前 `left_k = {S['left_k']}`（还要找几个）" if 'left_k' in S else '')),
        dict(type='text', size=26, fn=lambda S: (
            f"`sl = {S['sl']}`（第一列之和，最小的数组和），`sr = {S['sr']}`（最后一列之和）" if 'sl' in S and 'sr' in S else '')),
        dict(type='calls', h=240),
    ],
    watch=[('k', 'k', 'orange'), ('sl', 'sl', 'blue'), ('sr', 'sr', 'pink'), ('left_k', 'left_k', 'green')],
    max_steps=110,
    skip=['nonlocal left_k', 'left_k = k', 'for x in mat[i]'],
    captions={
        'sl = sum': '`sl` = 第一列之和 = =={sl}==：每行都选第一个数，这是最小的数组和',
        'sr = sum': '`sr` = 最后一列之和 = =={sr}==：一定有 `f(sr) ≥ k`，所以二分范围是 `[{sl}, {sr - 1}]`',
        'return sl + bisect_left': lambda S, B, r: (f'二分结束：最小的 s 满足 `f(s) ≥ k` → 答案 =={r}==' if r is not None else '`bisect_left` 二分 `s`：检查 `check(s)` 是否为 True'),
        'return dfs(len(mat) - 1': '检查 `s = {B.s}`：先把第一列都选上（和为 `sl`），剩余额度 `s - sl` = =={B.s - B.sl}==，从最后一行开始 `dfs`',
        'if i < 0': lambda S, B, r: ('`i < 0` → 每行都选好了，找到一个不超过 s 的数组和 → ==计数 -1==' if S.i < 0
                                      else f'`i = {S.i}`：第 {S.i} 行有序，从小到大「枚举选哪个」，剩余额度 `{S.s}`'),
        'left_k -= 1': '找到一个，`left_k` → {left_k}（还差几个）',
        'return left_k == 0': lambda S, B, r: (f'`left_k = {S.left_k}` → ==够 k 个了==，一路返回 True' if S.left_k == 0
                                                else f'`left_k = {S.left_k}` ≠ 0 → 还不够，回溯去找下一个'),
        'if x - mat[i][0] > s': lambda S, B, r: (f'选 `x = {S.x}` 比第一个多花 `{S.x - S.mat[S.i][0]}`，额度只剩 `{S.s}` → ==超了==，后面更大，剪枝' if S.x - S.mat[S.i][0] > S.s
                                                  else f'选 `x = {S.x}` 多花 `{S.x - S.mat[S.i][0]}` ≤ 额度 `{S.s}` → 可以选'),
        'break  #': '后面的元素更大，无需枚举，`break`',
        'if dfs(i - 1': '选了 `{B.x}`，额度变成 `{B.s - (B.x - B.mat[B.i][0])}`，递归到第 `{B.i - 1}` 行',
        'return True': '下层找够了 k 个 → 一路向上返回 True',
        'return False': '这一行枚举完了还不够 → 返回 False，回溯到上一行',
    },
    cards=dict(
        one_liner='二分数组和 s，回溯数一数不超过 s 的组合有几个',
        complexity='时间 `O(mk log U)`，空间 `O(m)`',
        problem=['`m × n` 矩阵每行非递减，从每行选一个数组成数组，求所有数组和中的第 `k` 小',
                 '示例：`mat=[[1,3,11],[2,4,6]], k=5` → `7`',
                 '本视频：`mat=[[1,3],[2,4]], k=3`：数组和 `3, 5, 5, 7` → 第 3 小是 `5`'],
        quote='设有 f(s) 个不超过 s 的数组和。由于随着 s 的增大，f(s) 不会减小，有单调性，可以二分。如果 f(s) ≥ k，说明答案至多为 s。',
        quote_src='—— 灵茶山艾府题解（算法二：二分答案）',
        result='`f(4) = 1 < 3 ≤ f(5) = 3` → 最小的 s 是 `5`，答案 `5`',
        idea=['二分答案 `s`：用回溯数「不超过 s 的数组和」有多少个，数到 k 个就停',
              '先把第一列都选上（最小和），回溯时只花「比第一个多出来的部分」',
              '剪枝：多出来的部分超过剩余额度就 `break`，因为行有序，后面更大'],
        summary=['时间 `O(mk log U)`，空间 `O(m)`；`U` = 最后一列之和 − 第一列之和',
                 '二分范围 `[sl, sr-1]`：`f(sr) ≥ k` 一定成立，`f(sl)` 不一定',
                 '二分出的答案一定是某个数组和：`f(s-1) < k ≤ f(s)` 只能由真实数组和造成',
                 '题解另有两种写法：暴力保留前 k 小（排序），以及最小堆（同 373 题）'],
    ),
)

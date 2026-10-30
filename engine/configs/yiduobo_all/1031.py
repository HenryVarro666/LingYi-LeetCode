def _col(l_first):
    def f(S, i, v):
        if 'end_pos' not in S:
            return None
        e, L, M = S['end_pos'], S['L'], S['M']
        right, left = (M, L) if l_first else (L, M)
        if e - right + 1 <= i <= e:
            return 'pink'
        if e - right - left + 1 <= i <= e - right:
            return 'blue'
        return None
    return f


def _dim(S, i, v):
    return 'end_pos' in S and i > S['end_pos']


def _txt(S):
    if 'end_pos' not in S:
        if 'res' in S:
            return f'初值：L、M 紧挨着放在最前面，`res = s[L + M − 1]` = =={S["res"]}=='
        return '`s[i]` = `A[0..i]` 的和（==闭区间==前缀和），`A[l..r]` 的和 = `s[r] − s[l − 1]`'
    e, s, L, M = S['end_pos'], S['s'], S['L'], S['M']
    return (f'end_pos = {e}：L 在前 `{S["max_l"]} + {s[e] - s[e - M]}` = =={S["max_l"] + s[e] - s[e - M]}==；'
            f'M 在前 `{S["max_m"]} + {s[e] - s[e - L]}` = =={S["max_m"] + s[e] - s[e - L]}==')


def _res(S, B, ret):
    e, s, L, M = S.end_pos, S.s, S.L, S.M
    a, b = S.max_l + s[e] - s[e - M], S.max_m + s[e] - s[e - L]
    if S.res > B.res:
        return f'`max_l + M段 = {a}`，`max_m + L段 = {b}` → `res` 刷新为 =={S.res}=='
    return f'`{a}` 和 `{b}` 都不超过 `{B.res}`，`res` 保持不变'


CONFIG = dict(
    num=1031, title='两个无重叠子数组的最大和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 结束位置后移只多一个选项',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1680'],
    code='''
class Solution(object):
    def maxSumTwoNoOverlap(self, A, L, M):

        s = [A[0]]
        for num in A[1:]:
            s.append(s[-1] + num)

        max_l = s[L - 1]
        max_m = s[M - 1]
        res = s[L + M - 1]
        for end_pos in range(L + M, len(A)):
            max_l = max(max_l, s[end_pos - M] - s[end_pos - M - L])
            max_m = max(max_m, s[end_pos - L] - s[end_pos - M - L])
            res = max(res, max_l + s[end_pos] - s[end_pos - M], max_m + s[end_pos] - s[end_pos - L])

        return res
''',
    call='Solution().maxSumTwoNoOverlap([3,8,1,3,2,1,8,9,0], 3, 2)',
    expect=29,
    skip=['s.append', 'for num in'],
    views=[
        dict(type='array', var='A', label='L 在前：粉 = 以 end_pos 结尾的 M，蓝 = 新多出的 L 选项',
             color=_col(True), dim=_dim, h=170),
        dict(type='array', var='A', label='M 在前：粉 = 以 end_pos 结尾的 L，蓝 = 新多出的 M 选项',
             color=_col(False), dim=_dim, h=170),
        dict(type='array', var='s', label='前缀和 s（s[i] 含 A[i]）', pointers={'end_pos': 'pink'}, h=190),
        dict(type='text', fn=_txt, size=27, h=90),
    ],
    watch=[('end_pos', 'end_pos', 'pink'), ('max_l', 'max_l', 'blue'), ('max_m', 'max_m', 'cyan'), ('res', 'res', 'green')],
    captions={
        's = [A[0]]': '先求前缀和 `s`，`s[i]` 是 `A[0]` 到 `A[i]` 的和',
        'max_l = s[L - 1]': '`max_l`：M 左边能放的最佳 L，一开始只有 `A[0..L−1]` 一种 → `{max_l}`',
        'max_m = s[M - 1]': '`max_m`：同理，最前面的 M 段和 = `{max_m}`',
        'res = s[L + M - 1]': '两段紧挨着放在最前面：`res = s[{L + M - 1}] = {res}`',
        'for end_pos in range': lambda S, B, ret: ((f'枚举 M 的结束位置 `end_pos = {S.end_pos}`' if 'end_pos' not in B
                                                     else f'`end_pos` 后移到 {S.end_pos}') if 'end_pos' not in B or S.end_pos != B.end_pos
                                                    else '枚举结束'),
        'max_l = max(': lambda S, B, ret: (f'相比上一轮只==多出一个== L 选项 `A[{S.end_pos - S.M - S.L + 1}..{S.end_pos - S.M}]`，和为 `{S.s[S.end_pos - S.M] - S.s[S.end_pos - S.M - S.L]}`'
                                           + (f' → `max_l = {S.max_l}`' if S.max_l != B.max_l else f'，`max_l` 仍是 {S.max_l}')),
        'max_m = max(': lambda S, B, ret: (f'反过来 M 在前：新多出的 M 段和 `{S.s[S.end_pos - S.L] - S.s[S.end_pos - S.M - S.L]}`'
                                           + (f' → `max_m = {S.max_m}`' if S.max_m != B.max_m else f'，`max_m` 仍是 {S.max_m}')),
        'res = max(res': _res,
        'return res': '答案 =={ret}==',
    },
    cards=dict(
        one_liner='结束位置每后移一步，另一段只多出一种选择',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在数组 `A` 中选长为 `L` 和长为 `M` 的两个==不重叠==子数组',
                 '两段先后顺序任意，求两段元素和的最大值',
                 '示例：`[3,8,1,3,2,1,8,9,0]`，L = 3，M = 2 → `29`（`[3,8,1]` + `[8,9]`）'],
        quote='可以发现，第二步相比第一步实际上就多出以A[N - M - 1]作为M的起点这种情况……更一般的，对于上面的求解过程，==每一步相比于前一步实际上就多出了一种选择==',
        quote_src='—— yiduobo 题解原文',
        idea=['先规定 L 在 M 前：枚举 M 的结束位置 `end_pos`，L 只能在 `A[0..end_pos−M]` 里',
              '`end_pos` 后移一步，L 的可选范围只多出 `A[end_pos−M−L+1..end_pos−M]`',
              '维护 `max_l` 只需和这个新选项比；M 在前的情况如法炮制，放进同一趟循环'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`s` 是闭区间前缀和：`A[l..r]` 的和 = `s[r] − s[l−1]`，注意下标',
                 '初值 `res = s[L+M−1]`：两段紧挨着放在开头的情况，循环从 `L+M` 开始',
                 '原文为 Python 2 风格写法，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神用带 0 的前缀和 `s[i] − s[j]`，yiduobo 先从后往前推导再翻转方向'],
    ),
)

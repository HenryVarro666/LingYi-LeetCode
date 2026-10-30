Q = [9, 5]
N = 7


def _color(S, i, v):
    if 'l' not in S:
        return None
    if i < S['l']:
        return 'red'
    if i >= S['r']:
        return 'green'
    return None


def _top(S):
    line = S['_line']
    if 'cnt' in S and 'mid' in S and line in (8, 9, 10, 11, 12):
        return f"x = `{S['mid']}`：目前累计需要 `cnt = {S['cnt']}` 间店（`n = {N}`）"
    if 'l' not in S:
        return f'`n = {N}`：x 越大越容易分完 → ==答案可二分=='
    l, r = S['l'], S['r']
    if l < r:
        return f'答案在 `[{l}, {r}]` 里：`{l}` 之前都不行，`{r}` 一定可行'
    return f'`l == r = {l}`：区间收成一点 → 答案 =={l}=='


def _per(S):
    if 'mid' in S and S['_line'] in (8, 9, 10, 11, 12, 14):
        m = S['mid']
        return [-(-q // m) for q in Q]
    return []


CONFIG = dict(
    num=2064, title='分配给商店的最多商品的最小值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分 x · 逐种商品统计店数',
    tags=['灵神题单·二分算法', '难度分 1886'],
    code='''
class Solution(object):
    def minimizedMaximum(self, n, quantities):

        l = 1
        r = max(quantities)
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for q in quantities:
                cnt += q // mid
                if q % mid != 0:
                    cnt += 1

            if cnt > n:
                l = mid + 1
            else:
                r = mid
        
        return l
''',
    call=f'Solution().minimizedMaximum({N}, {Q})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=27, h=80),
        dict(type='array', var=lambda S: list(range(1, max(Q) + 1)),
             label='候选 x（红 = 太小，绿 = 可行，灰 = 还没判断）',
             cell=70, index=False, color=_color, pointers={'l': 'red', 'mid': 'yellow', 'r': 'green'}, h=240),
        dict(type='array', var='quantities', label='quantities：各种商品的件数', cell=100, h=170),
        dict(type='array', var=_per, label='每种商品顶着 x 分，各要的店数', cell=100, index=False, h=170),
    ],
    watch=[('l', 'l', 'red'), ('r', 'r', 'green'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'cyan'), 'n'],
    captions={
        'l = 1': '`l = 1`：二分的左边界，每间店至少放 1 件才可能分完',
        'r = max': '`r = max(quantities) = {r}`：每种商品占一间店，一定可行',
        'while l < r': lambda S, B, ret: (f'`l = {S.l} < r = {S.r}`：区间还没收成一点 → 继续' if S.l < S.r
                                         else f'`l = r = {S.l}`：区间收成一点，==答案就是它=='),
        'mid = (l + r)': '`mid = ({l} + {r}) >> 1 = {mid}`：试试每间店至多放 `{mid}` 件',
        'cnt = 0': '`cnt` 记录分完所有商品需要的商店数',
        'cnt += q // mid': '`q = {q}`：顶着 `x = {mid}` 分，先分出 `{q} // {mid} = {q // mid}` 间满店 → `cnt` = =={cnt}==',
        'if q % mid != 0': lambda S, B, ret: (f'`{S.q} % {S.mid} = {S.q % S.mid} ≠ 0`：还剩一些放不满 → ==还要多一间店==' if S.q % S.mid
                                             else f'`{S.q} % {S.mid} = 0`：正好分完，不用多一间店'),
        'cnt += 1': '多开一间店放余下的：`cnt` = =={cnt}==',
        'if cnt > n': lambda S, B, ret: (f'`cnt = {S.cnt} > n = {S.n}`：店不够，`x = {S.mid}` ==太小=='
                                        if S.cnt > S.n else f'`cnt = {S.cnt} ≤ n = {S.n}`：`x = {S.mid}` ==可行=='),
        'l = mid + 1': '`x = {B.mid}` 不行，比它小的更不行 → `l = {l}`',
        'r = mid': '`x = {mid}` 可行，但可能还能更小 → `r = {r}`（`mid` 本身保留）',
        'return l': '`l` 就是最小的可行 x → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='x 越大越容易分完，二分 x，统计需要的店数 cnt 和 n 比',
        complexity='时间 `O(m log U)`，空间 `O(1)`',
        problem=['`n` 间商店，`quantities[i]` 是第 `i` 种商品的件数，一间店至多放一种',
                 '分完所有商品，使店里最大件数 `x` 最小',
                 '示例：`n = 6, [11, 6]` → `3`；本视频用 `n = 7, [9, 5]` → `3`'],
        quote='随着x的增大，完成分配的可能性就越高，也就是说本题的答案是符合二分的性质的。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每种商品都顶着 `x` 分，需要的店数是 `q / x` 向上取整',
              '`cnt > n`：x 太小，`l = mid + 1`；否则 x 可行，`r = mid`',
              '取整用 `q // mid`，有余数再 `+ 1`，等价于向上取整'],
        summary=['时间 `O(m log U)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `q / mid` 已改为 `q // mid`',
                 '闭区间 `[l, r]`：不可行 `l = mid + 1`，可行 `r = mid`，循环 `l < r`',
                 '对比灵神：灵神用开区间 + `(q + mx - 1) // mx` 一行算上取整'],
    ),
)

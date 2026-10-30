ARR = [2, -3, 4, -1, 5]


def _ix(S):
    return ARR.index(S['x']) if 'x' in S and S['x'] in ARR else None


def _fmt(v):
    return '-∞' if v == float('-inf') else str(v)


def _text(S):
    if 'f0' not in S:
        return '`f0`：以当前数结尾、==没删==；`f1`：以当前数结尾、==恰好删了一个=='
    return (f'`f0` = =={_fmt(S["f0"])}==（没删）　`f1` = =={_fmt(S["f1"])}==（删过一个）　`ans` = =={_fmt(S["ans"])}==')


def _cap_f1(S, B, ret):
    x = S.x
    if B.f0 == float('-inf'):
        return f'第一个数前面没有数可删：`f1` 仍是 =={_fmt(S.f1)}==（删掉 `{x}` 会让子数组为空，不合法）'
    keep = B.f1 + x
    dele = B.f0
    way = f'保留 `{x}`：`{_fmt(B.f1)} + {x}`' if keep >= dele else f'删掉 `{x}`：直接取上一步没删的 `f0 = {_fmt(B.f0)}`'
    return f'`f1 = max({_fmt(keep)}, {_fmt(dele)})` = =={_fmt(S.f1)}==，{way}（==先算 f1，它要用旧的 f0==）'


def _cap_f0(S, B, ret):
    if B.f0 > 0:
        return f'旧 `f0 = {B.f0}` > 0，接上 `{S.x}` → `f0 = {S.f0}`'
    return f'旧 `f0 = {_fmt(B.f0)}` 不为正，从 `{S.x}` 重新开始 → `f0 = {S.f0}`'


CONFIG = dict(
    num=1186, title='删除一次得到子数组最大和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（空间优化）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1799'],
    code='''
class Solution:
    def maximumSum(self, arr: List[int]) -> int:
        ans = f0 = f1 = -inf
        for x in arr:
            f1 = max(f1 + x, f0)  # 注：手动 if 比大小会更快 
            f0 = max(f0, 0) + x
            ans = max(ans, f0, f1)
        return ans
''',
    call=f'Solution().maximumSum({ARR})',
    expect=10,
    views=[
        dict(type='text', fn=_text, size=26, h=70),
        dict(type='array', var='arr', label='arr（蓝 = 当前 x）', cell=96, h=260,
             pointers={_ix: 'blue'}, pointer_labels={_ix: 'x'},
             color=lambda S, i, v: 'blue' if _ix(S) == i else None),
    ],
    watch=[('f0', 'f0', 'blue'), ('f1', 'f1', 'pink'), ('ans', 'ans', 'green'), ('x', 'x', 'yellow')],
    captions={
        'ans = f0 = f1': '三个都初始化为 `-inf`：「没有数字」不合法，取 max 时自然被淘汰',
        'f1 = max': _cap_f1,
        'f0 = max': _cap_f0,
        'ans = max': '`ans = max({B.ans}, f0={f0}, f1={f1})` = =={ans}==',
        'return ans': '所有位置、两种状态里的最大值 = =={ret}==',
    },
    cards=dict(
        one_liner='右端点 + 「删没删」两个状态，一遍扫完',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选一个非空子数组，可以（至多）删掉其中一个数，求剩余元素和的最大值',
                 '删完后不能为空',
                 '本视频：`[2,-3,4,-1,5]` → `10`（删掉 -3）'],
        quote='dfs(i,0) = max(dfs(i-1,0), 0) + arr[i]；dfs(i,1) = max(dfs(i-1,1) + arr[i], dfs(i-1,0))。请注意计算顺序！必须先算 f[1] 再算 f[0]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f0`：右端点是 `i`、不能删时的最大和，就是经典最大子数组和',
              '`f1`：右端点是 `i`、必须删一个：不删 `x` 就接着 `f1 + x`，删 `x` 就取上一步的 `f0`',
              '题解从记忆化搜索推到递推再压缩空间，这里演示最后的 O(1) 写法'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==必须先算 f1 再算 f0==，否则 f1 会用到新的 f0',
                 '初值 `-inf` 保证子数组非空：全是负数时不会靠删除得到 0',
                 '另有记忆化搜索、`f[i+1][j]` 二维递推两种写法，状态转移相同',
                 '延伸：至多/恰好/至少删 k 个'],
    ),
)

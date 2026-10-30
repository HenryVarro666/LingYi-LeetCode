def _inner(S):
    return S.get('_inner') or {}


def _cand_color(S, idx, v):
    I = _inner(S)
    if 'i' not in I or 'd' not in I:
        return None
    if I['d'] == 0:
        return None
    if 'j' in I and v == I['j']:
        return 'yellow'
    if I['d'] <= v <= I['i']:
        return 'blue'
    return None


def _cand_dim(S, idx, v):
    I = _inner(S)
    if 'i' not in I or 'd' not in I or I['d'] == 0:
        return False
    return not (I['d'] <= v <= I['i'])


def _info(S):
    I = _inner(S)
    if 'i' not in I:
        return '`dfs(i)`：还能从 `1..i` 中选数；倒着枚举，保证 path ==从大到小=='
    if 'd' not in I:
        return f"进入 `dfs({I['i']})`：还能从 `1..{I['i']}` 中选"
    if I['d'] == 0:
        return f"还要选 `d = 0` 个 → path `{S.get('path')}` 就是一个组合"
    lo = I['d']
    return (f"还要选 `d = {I['d']}` 个，可选范围 `1..{I['i']}`；j 只枚举 `{I['i']}..{lo}`"
            + (f"（`j < {lo}` 时后面不够选，==剪掉==）" if lo > 1 else ''))


def _cap_for(S, B, ret):
    # 字幕阶段拿不到单独的栈帧：S/B 里同名变量取最内层的值
    if 'j' in B and S.j == B.j:
        return f'`j` 已经试到 `d = {S.d}`，这一层枚举完 → 返回上一层'
    if S.j == S.i:
        tail = f'；`j < {S.d}` 时后面凑不够 {S.d} 个 → 不枚举（==剪枝==）' if S.d > 1 else ''
        return f'枚举下一个数 `j`：从 `i = {S.i}` 倒着到 `d = {S.d}`{tail} → 先试 `j = {S.j}`'
    return f'换下一个数：`j = {S.j}`'


CONFIG = dict(
    num=77, title='组合', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='组合型回溯 · 枚举选哪个 + 剪枝',
    tags=['面试经典150'],
    code='''
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        ans = []
        path = []

        # 枚举选哪个：在 1 到 i 中选一个数，加到 path 末尾
        def dfs(i: int) -> None:
            d = k - len(path)  # 还要选 d 个数
            if d == 0:  # 选好了
                ans.append(path.copy())
                return

            # 枚举的数不能太小，否则后面没有数可以选
            for j in range(i, d - 1, -1):
                path.append(j)
                dfs(j - 1)
                path.pop()  # 恢复现场

        dfs(n)  # 从 n 开始倒着枚举
        return ans
''',
    call='Solution().combine(3, 2)',
    expect=[[3, 2], [3, 1], [2, 1]],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)) if 'n' in S else None,
             label='1..n（蓝 = 本层可选的 j，黄 = 当前 j，暗 = 不能选）', cell=90, h=150,
             color=_cand_color, dim=_cand_dim, index=False),
        dict(type='stack', var='path', label='path（已选的数）', h=105),
        dict(type='calls', h=190),
        dict(type='stack', var='ans', label='ans', h=105),
    ],
    watch=[('i', lambda S: _inner(S).get('i'), 'blue'), ('d', lambda S: _inner(S).get('d'), 'cyan'),
           ('j', lambda S: _inner(S).get('j'), 'yellow'), ('path', 'path', 'green'), ('len(ans)', 'len(ans)')],
    captions={
        'dfs(n)': '从 `dfs({n})` 开始：path 里的数==从大到小==选，所以 `[2,3]` 和 `[3,2]` 只会出现一次',
        'd = k - len(path)': '还要选 `d = k − len(path) = {k} − {len(path)} = {d}` 个数',
        'if d == 0': lambda S, B, ret: ('`d == 0`：已经选够 `k` 个 → 这是一个组合' if S.d == 0
                                        else f'`d = {S.d}`，还没选够 → 继续枚举'),
        'ans.append': '复制 path 加入答案：`{ans[-1]}`（==要复制==，path 之后还会变）',
        '                return': '叶子：返回上一层',
        'for j in range': _cap_for,
        'path.append(j)': '选 `{j}` → path = `{path}`',
        'dfs(j - 1)': lambda S, B, ret: (f'递归 `dfs({B.j - 1})`：下一个数只能比 `{B.j}` 小，从 `1..{B.j - 1}` 里选'
                                         if B.j > 1 else '递归 `dfs(0)`：已经没有更小的数了'),
        'path.pop()': lambda S, B, ret: f'恢复现场：撤销 `{B.path[-1]}`，path 回到 `{S.path}`',
        'return ans': '共 `C(3,2) = {len(ret)}` 个组合',
    },
    skip=['ans = []', 'path = []'],
    max_steps=60,
    cards=dict(
        one_liner='倒着枚举下一个数选谁，剩下的数不够选就剪掉',
        complexity='时间 `O(k·C(n,k))`，空间 `O(k)`（不计返回值）',
        problem=['给定 `n` 和 `k`，返回 `[1, n]` 中所有 `k` 个数的组合（顺序任意）',
                 '示例：`n = 4, k = 2` → `[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`',
                 '本视频：`n = 3, k = 2` → 3 个组合'],
        quote='枚举选哪个：在 1 到 i 中选一个数，加到 path 末尾。==枚举的数不能太小，否则后面没有数可以选==。',
        quote_src='—— 灵茶山艾府题解代码注释（方法一）',
        idea=['`d = k − len(path)` 是还要选的个数，`d == 0` 就得到一个组合',
              '`dfs(i)`：下一个数从 `i` 倒着枚举到 `d`；选了 `j` 之后递归 `dfs(j − 1)`',
              '==剪枝==：`j < d` 时 `1..j` 不足 `d` 个数，一定凑不出组合，所以循环下界是 `d`'],
        result='得到 `[[3,2],[3,1],[2,1]]` ✓（顺序任意）',
        summary=['时间：路径长 `k` × 叶子数 `C(n,k)`；空间 `O(k)`',
                 '倒着枚举的好处：剩余可选数恰好是 `j`，剪枝条件写成 `range(i, d - 1, -1)` 很自然',
                 '易错：`ans.append(path.copy())`，直接 append path 最后会全是空列表',
                 '方法二「选或不选」：`i > d` 时才允许不选 `i`，同样能剪枝',
                 '同类题：216. 组合总和 III、22. 括号生成'],
    ),
)

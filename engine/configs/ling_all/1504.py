MAT = [[0, 1, 1], [1, 1, 1]]


def _r(S):
    if 'row' not in S:
        return -1
    return next(k for k, r in enumerate(S['mat']) if r is S['row'])


def _info(S):
    if 'f' not in S or 'left' not in S:
        return f"`heights = {S.get('heights')}`" if 'heights' in S else ''
    return f"底边第 `{_r(S)}` 行，右边界 `j = {S['j']}`：`f = f[left] + (j − left)×h`，`ans = {S['ans']}`"


CONFIG = dict(
    num=1504, title='统计全 1 子矩形', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='柱状图 + 单调栈 · 枚举右下角',
    tags=['灵神题单·单调栈'],
    code='''
class Solution:
    def numSubmat(self, mat: List[List[int]]) -> int:
        heights = [0] * len(mat[0])
        ans = 0
        for row in mat:
            for j, x in enumerate(row):
                if x == 0:
                    heights[j] = 0
                else:
                    heights[j] += 1

            # (j, f, heights[j])
            st = [(-1, 0, -1)]  # 哨兵，方便处理 left=-1 的情况
            for j, h in enumerate(heights):
                while st[-1][2] >= h:
                    st.pop()
                left, f, _ = st[-1]
                # 计算底边为 row，右边界为 j 的子矩形个数
                # 左边界 <= left 的矩形，每个矩形的右边界都可以扩展到 j，一共有 f 个
                # 左边界 >  left 的矩形，左边界有 j-left 种，高度有 h 种，一共有 (j-left)*h 个
                f += (j - left) * h
                ans += f
                st.append((j, f, h))
        return ans
''',
    call=f'Solution().numSubmat({MAT})',
    expect=12,
    views=[
        dict(type='grid', var='mat', h=190, cell=60, label='mat（当前底边那一行）',
             color=lambda S, i, j, v: ('blue' if i == _r(S) and 'j' in S and j == S['j'] else ('yellow' if i == _r(S) else None)) if 'row' in S else None),
        dict(type='array', var='heights', pointers={'j': 'blue'}, h=200, label='heights（以当前行为底的柱子高度）',
             color=lambda S, i, v: 'blue' if S.get('j') == i and 'f' in S else None),
        dict(type='stack', var='st', fmt=lambda t: f'j={t[0]} f={t[1]} h={t[2]}', label='st（j, f, h），栈顶在右', h=120, font=24),
        dict(type='text', fn=_info, size=24, h=60),
    ],
    watch=[('j', 'j', 'blue'), ('h', 'h', 'cyan'), ('f', 'f', 'yellow'), ('ans', 'ans', 'green')],
    skip=['for j, x in enumerate(row)', 'if x == 0', 'ans = 0'],
    captions={
        'heights = [0]': '`heights[j]` 是以当前行为底、第 `j` 列向上连续 1 的个数',
        'for row in mat': '处理下一行：把它当作矩形的==底边==',
        'if x == 0': lambda S, B, r: f"`mat[行][{S.j}] = {S.x}` → " + ('是 0，柱子断了，高度清零' if S.x == 0 else '是 1，柱子长高 1'),
        'heights[j] = 0': '`mat` 这格是 0，柱子断了，高度清零：`heights[{j}] = 0`',
        'heights[j] += 1': '`mat` 这格是 1，柱子长高 1：`heights[{j}] = {heights[j]}`',
        'st = [(-1, 0, -1)]': '新的一行，栈重置，哨兵 `(-1, 0, -1)` 表示 `left = -1`',
        'for j, h in enumerate(heights)': '枚举右边界 `j = {j}`，柱高 `h = {h}`',
        'while st[-1][2] >= h': lambda S, B, r: (
            f"栈顶高度 `{S.st[-1][2]}` ≥ `{S.h}` → ==弹出==：它不比当前矮，不是“左边第一个更矮”"
            if S.st[-1][2] >= S.h else f"栈顶高度 `{S.st[-1][2]}` < `{S.h}` → 找到 `left = {S.st[-1][0]}`，停止弹栈"),
        'st.pop()': '弹出栈顶，栈里剩 `{len(st)}` 项',
        'left, f, _ = st[-1]': '`left = {left}`：左边第一个更矮的柱子；`f = {f}`：右边界在 `left` 的矩形数',
        'f += (j - left) * h': '右边界为 `j` 的矩形数：`f[left]` 个延伸过来 + `({j} − {left}) × {h}` 个新的 → `f = ` =={f}==',
        'ans += f': '底边这一行、右边界为 `{j}` 的矩形都算上：`ans = {ans}`',
        'st.append': '`(j={j}, f={f}, h={h})` 入栈，供右边更高的柱子复用',
        'return ans': '所有行、所有右边界累加，共 =={ret}== 个全 1 子矩形',
    },
    cards=dict(
        one_liner='枚举右下角：左边界分两类，远的复用 f，近的直接乘',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['给一个 `m×n` 的 0/1 矩阵，数一数有多少个子矩形里全是 1',
                 '示例：`[[1,0,1],[1,1,0],[1,1,0]]` → `13`',
                 '本视频：`[[0,1,1],[1,1,1]]` → `12`'],
        quote='左边界 <= left 的矩形，每个矩形的右边界都可以扩展到 j，一共有 f 个；左边界 > left 的矩形，左边界有 j-left 种，高度有 h 种。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['逐行当作底边，算出每列向上的连续 1 的高度 `heights`，转成柱状图问题',
              '用单调栈找 `left`：左边第一个比 `heights[j]` 矮的柱子',
              '左边界 `≤ left`：复用 `f`；左边界 `> left`：`(j−left)×h` 个'],
        summary=['时间 `O(mn)`，空间 `O(n)`',
                 '易错：每换一行要重置栈，哨兵 `(-1, 0, -1)` 的高度 -1 保证不会被弹出',
                 '易错：弹栈条件是 `>= h`（相等也弹），否则相等高度会被算两遍',
                 '另一种写法（方法一）：枚举上下边界，压缩成「全 h 子数组」，`O(m²n)`'],
    ),
)

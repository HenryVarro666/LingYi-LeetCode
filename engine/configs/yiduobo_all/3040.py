NUMS = [4, 2, 3, 1, 3, 2, 4]
_L = lambda S: S['_inner'].get('left')
_R = lambda S: S['_inner'].get('right')


def _ncolor(S, k, v):
    l, r = _L(S), _R(S)
    if l is None or r is None or 'target' not in S['_inner']:
        return None
    return 'blue' if k == l else 'pink' if k == r else None


def _dim(S, k, v):
    l, r = _L(S), _R(S)
    return l is not None and r is not None and 'target' in S['_inner'] and not (l <= k <= r)


def _cell(S, i, j, v):
    I = S['_inner']
    if 'target' not in I:
        return None
    return 'yellow' if (i, j) == (I.get('left'), I.get('right')) else None


def _formula(S, B):
    I = B['_inner']
    if 'target' not in I:
        return '先用三种首操作之一定 `target`，每种都要把 `f` 重置为 0 再算'
    l, r, t = I['left'], I['right'], I['target']
    nums = S['nums']
    ln = B.get('_line')
    base = f'区间 `[{l}, {r}]`，`target = {t}`：'
    if ln == 21:
        return base + f'头尾 `{nums[l]} + {nums[r]}`'
    if ln == 26:
        return base + f'前两个 `{nums[l]} + {nums[l + 1]}`' if l + 1 <= r else base
    if ln == 31:
        return base + f'后两个 `{nums[r - 1]} + {nums[r]}`'
    return base + f'最多还能操作几次（上限 `{(r - l + 1) // 2}`）'


CONFIG = dict(
    num=3040, title='相同分数的最大操作数目 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP（记忆化搜索 + 达到上限就剪枝）',
    tags=['灵神题单', '动态规划', '难度分 1709'],
    code='''
class Solution(object):
    def maxOperations(self, nums):

        n = len(nums)
        if n == 2:
            return 1

        def calc(f, left, right, target):
            if f[left][right] == 0:
                if left == right:
                    f[left][right] = 0
                    return 0
                
                if left == right - 1:
                    if nums[left] + nums[right] == target:
                        f[left][right] = 1
                    else:
                        f[left][right] = 0
                    return f[left][right]
                
                if nums[left] + nums[right] == target:
                    f[left][right] = calc(f, left + 1, right - 1, target) + 1
                    if f[left][right] == (right - left + 1) // 2:
                        return f[left][right]
                
                if nums[left] + nums[left + 1] == target:
                    f[left][right] = max(f[left][right], calc(f, left + 2, right, target) + 1)
                    if f[left][right] == (right - left + 1) // 2:
                        return f[left][right]

                if nums[right] + nums[right - 1] == target:
                    f[left][right] = max(f[left][right], calc(f, left, right - 2, target) + 1)
        

            return f[left][right]
        

        f = [[0] * n for _ in range(n)]
        res = calc(f, 2, n - 1, nums[0] + nums[1])
        f = [[0] * n for _ in range(n)]
        res = max(res, calc(f, 0, n - 3, nums[-1] + nums[-2]))
        f = [[0] * n for _ in range(n)]
        res = max(res, calc(f, 1, n - 2, nums[0] + nums[-1]))
        return res + 1
''',
    call=f'Solution().maxOperations({NUMS!r})',
    expect=3,
    skip=['n = len(nums)', 'if n == 2', 'return 1'],
    max_steps=80,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = left，粉 = right，暗 = 区间外）', h=190, cell=70,
             pointers={_L: 'blue', _R: 'pink'}, pointer_labels={_L: 'left', _R: 'right'},
             color=_ncolor, dim=_dim),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[left][right]（黄 = 当前区间；0 = 还没算 / 不能操作）', h=250, cell=46,
             rows=lambda S: list(range(len(NUMS))), cols=lambda S: list(range(len(NUMS))), color=_cell),
        dict(type='calls', h=170, hide=('f',)),
    ],
    watch=[('left', _L, 'blue'), ('right', _R, 'pink'), ('target', lambda S: S['_inner'].get('target'), 'yellow'),
           ('res', 'res', 'green')],
    captions={
        'f = [[0] * n': '重置 `f` 全为 0：每个 `target` 单独算一遍，==不能共用上一次的表==',
        'res = calc(f, 2': '首操作删前两个：`target = nums[0] + nums[1] = {nums[0] + nums[1]}`，只需算 `f[2][n-1]`',
        'res = max(res, calc(f, 0': '首操作删后两个：`target = nums[-1] + nums[-2] = {nums[-1] + nums[-2]}`，只需算 `f[0][n-3]`',
        'res = max(res, calc(f, 1': '首操作删头尾：`target = nums[0] + nums[-1] = {nums[0] + nums[-1]}`，只需算 `f[1][n-2]`',
        'if f[left][right] == 0': lambda S, B, r: (f'`f[{B.left}][{B.right}] = 0`：还没算过（或值就是 0），进来算' if B.f[B.left][B.right] == 0
                                                   else f'`f[{B.left}][{B.right}] = {B.f[B.left][B.right]}` 已有值 → 直接返回，不重复算'),
        'if left == right:': lambda S, B, r: ('`left == right`：只剩 1 个数，无法操作 → 0' if B.left == B.right
                                              else f'`left = {B.left} ≠ right = {B.right}`：至少 2 个数'),
        'f[left][right] = 0': '只剩 1 个数，不能操作，`f = 0`',
        'if left == right - 1': lambda S, B, r: (f'只剩 2 个数 `{B.nums[B.left]}, {B.nums[B.right]}`：和为 `{B.nums[B.left] + B.nums[B.right]}`，只有等于 `target = {B.target}` 才能删一次'
                                                 if B.left == B.right - 1 else f'区间有 {B.right - B.left + 1} 个数，三种操作都试'),
        'f[left][right] = 1': '和等于 `target`：删掉这两个数 → ==1== 次',
        'f[left][right] = calc(f, left + 1': '头尾和等于 `target`：删头尾，子区间 `[{B.left + 1}, {B.right - 1}]`，`f` = 子问题 + 1',
        'f[left][right] = max(f[left][right], calc(f, left + 2': '前两个和等于 `target`：删前两个，子区间 `[{B.left + 2}, {B.right}]`，与已有答案取 ==max==',
        'f[left][right] = max(f[left][right], calc(f, left, right - 2': '后两个和等于 `target`：删后两个，子区间 `[{B.left}, {B.right - 2}]`，与已有答案取 ==max==',
        'if f[left][right] == (right - left + 1) // 2': lambda S, B, r: (
            f'`f = {B.f[B.left][B.right]}` 等于上限 `({B.right}-{B.left}+1)//2 = {(B.right - B.left + 1) // 2}`：==不可能更多了==，直接返回（剪枝）'
            if B.f[B.left][B.right] == (B.right - B.left + 1) // 2 else
            f'`f = {B.f[B.left][B.right]}` 还没到上限 `{(B.right - B.left + 1) // 2}`，继续试别的操作'),
        'return f[left][right]': '区间 `[{left}, {right}]` 的最大操作次数 =={ret}==',
        'return res + 1': '三个 `target` 取最大再 `+ 1`（最初选 target 的那次操作）= =={ret}==',
    },
    cards=dict(
        one_liner='首次操作选定 target，再对三种 target 各做一次记忆化搜索',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['每次可以删==前两个==、==后两个==、或==首尾==两个，分数是被删元素之和',
                 '要求所有操作的分数==相同==，求最多能操作几次',
                 '示例：`[3,2,1,2,3,4]` → `3`；本视频：`[4,2,3,1,3,2,4]` → `3`'],
        quote='具体实现上，可以采用枚举区间长度的动态规划，也可以采用记忆化搜索。在这里采用记忆化搜索相对更优，因为本题是从外向内逐步选取数字的……',
        quote_src='—— yiduobo 题解原文',
        idea=['三种首操作各给出一个 `target`，每个 `target` 单独做区间 DP',
              '`f[left][right]`：区间在 `target` 下的最大操作数，三种转移取 `max`',
              '做到 `(right-left+1)//2` 次就是上限，立刻返回；每个 `target` 前要把 `f` 重置为 0'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`；记忆化只会走到可达的状态',
                 '易错：三次计算前 `f` 必须==重置为 0==，最后别忘了 `+ 1`',
                 '易错：`f == 0` 既表示“没算过”也可能是真值 0，只是会重复计算，不会算错',
                 '对比灵神：灵神用 `@cache` 带 target 共用缓存，并用 `done` 全局剪枝；yiduobo 每个 target 重置 f，用区间上限剪枝',
                 '原文已是 Python 3 可运行写法（`//` 为整数除法），未做修改'],
    ),
)

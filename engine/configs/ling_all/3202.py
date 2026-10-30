def _cur(S):
    x = S.get('x')
    return x if isinstance(x, int) and x < S['k'] else None


def _txt(S):
    x = _cur(S)
    if x is None or S.get('_line', 0) < 7:
        return '`f[y][x]`：最后两项模 k 为 `y`、`x` 的子序列最长长度'
    return f'遇到 `x = {x}`：把「末两项 x,y」的子序列接一个 x，变成「末两项 y,x」，长度 +1：`f[y][{x}] = f[{x}][y] + 1`'


def _cell(S, r, c, v):
    x = _cur(S)
    if x is None or S.get('_line', 0) < 7:
        return None
    y = S.get('y')
    if c == x and (y is None or r == y):
        return 'yellow'
    if r == x and (y is None or c == y):
        return 'blue'
    return None


CONFIG = dict(
    num=3202, title='找出有效子序列的最大长度 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='模 k 同余 · 记录最后两项',
    tags=['灵神题单', '动态规划', '难度分 1974'],
    code='''
class Solution:
    def maximumLength(self, nums: List[int], k: int) -> int:
        f = [[0] * k for _ in range(k)]
        for x in nums:
            x %= k
            for y, fxy in enumerate(f[x]):
                f[y][x] = fxy + 1
        return max(map(max, f))
''',
    call='Solution().maximumLength([1,4,2,3,1,4], 3)',
    expect=4,
    max_steps=60,
    skip=['for y, fxy'],
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=80),
        dict(type='text', fn=_txt, size=24, h=100),
        dict(type='table', var='f', label='f[y][x]：行 = 倒数第二项 y，列 = 最后一项 x（黄 = 写入，蓝 = 读取）', h=300, cell=90,
             rows=lambda S: [f'y={i}' for i in range(S['k'])], cols=lambda S: [f'x={i}' for i in range(S['k'])],
             color=_cell),
    ],
    watch=[('x', 'x', 'pink'), ('y', 'y', 'blue'), ('fxy', 'fxy', 'yellow'), ('k', 'k', 'cyan')],
    captions={
        'f = [[0]': '`f[y][x]`：目前遍历过的数里，最后两项模 `k` 为 `y`、`x` 的子序列最长长度，共 `k×k` 格',
        'for x in nums': '从左到右遍历：遇到谁就处理谁，不用找下一个元素的位置',
        'x %= k': '偶数项同余、奇数项同余，所以先取模：`x = {x}`',
        'f[y][x] = fxy + 1': lambda S, B, r: (f'`y = {S.y}`：在「末两项 {S.x},{S.y}」的子序列后接一个 `{S.x}` → 变成「末两项 {S.y},{S.x}」，'
                                              f'`f[{S.y}][{S.x}] = {S.fxy} + 1` = =={S.f[S.y][S.x]}=='),
        'return max': '答案是整个 `f` 里的最大值 = =={ret}==',
    },
    cards=dict(
        one_liner='模 k 后，最后两项一定，整个子序列就一定',
        complexity='时间 `O(k² + nk)`，空间 `O(k²)`',
        problem=['有效子序列：相邻两项之和模 `k` 都相等',
                 '求 `nums` 的最长有效子序列长度',
                 '示例：`[1,4,2,3,1,4], k = 3` → `4`（`[1,4,1,4]`）'],
        quote='这意味着 a 与 c 关于模 k 同余。……有效子序列的偶数项都关于模 k 同余，奇数项都关于模 k 同余。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`(a+b) % k == (b+c) % k` 移项 → `a ≡ c`：隔一项同余',
              '所以子序列只由最后两项（模 k）决定，状态 `f[y][x]`',
              '遇到 `x`：接在末两项为 `x, y` 的后面 → 末两项变 `y, x`，`f[y][x] = f[x][y] + 1`'],
        summary=['时间 `O(k² + nk)`，空间 `O(k²)`',
                 '易错：先对 `nums[i]` 取模；`f[y][x]` 读的是转置位置 `f[x][y]`',
                 '头一个数也算：可当作接在「末两项 y,x」里只有 x 一项的子序列上',
                 '灵神方法二：枚举相邻和的余数 `m`，只记最后一项，空间 `O(k)`'],
    ),
)

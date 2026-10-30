MATRIX, TARGET = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3


def _flat(S):
    return [v for row in S['matrix'] for v in row]


def _rb_flat(S, i):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'blue'
    return None


def _legend(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = x0 + 22, (y0 + y1) / 2
    for c, s in [(T['red'], '红：< target'), (T['blue'], '蓝：> target'), (T['yellow'], '黄框：a[mid] 在矩阵里的位置')]:
        if c == T['yellow']:
            cv.rect((x, y - 14, x + 28, y + 14), outline=c, width=4, r=6)
        else:
            cv.rect((x, y - 14, x + 28, y + 14), fill=c, r=6, outline=T['border'])
        cv.text((x + 38, y), s, 23, T['muted'], anchor='lm')
        x += 38 + cv.tlen(s, 23) + 34


def _state(S):
    if 'mid' in S and 'x' in S and S['left'] < S['mid'] < S['right']:
        m, n = S['mid'], S['n']
        return f"a[{m}] = matrix[{m} // {n}][{m} % {n}] = matrix[{m // n}][{m % n}] = =={S['x']}=="
    if 'left' in S:
        return f"开区间 `({S['left']}, {S['right']})`   ·   target = =={S['target']}==   ·   a = 每行拼起来（不真的创建）"
    return ''


def _while(S, B, ret):
    if B.left + 1 < B.right:
        return f'开区间 `({B.left}, {B.right})` 非空 → 继续二分'
    return f'`left + 1 = right`：开区间为空 → 结束循环'


def _cmp(S, B, ret):
    if S.x < S.target:
        return f'`x = {S.x} < {S.target}`：a 递增 → ==mid 及左边都比 target 小==，染红'
    return f'`x = {S.x} > {S.target}`：a 递增 → ==mid 及右边都比 target 大==，染蓝'


CONFIG = dict(
    num=74, title='搜索二维矩阵', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='拉成一维数组 · 开区间二分',
    code='''
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        left, right = -1, m * n
        while left + 1 < right:
            mid = (left + right) // 2
            x = matrix[mid // n][mid % n]
            if x == target:
                return True
            if x < target:
                left = mid
            else:
                right = mid
        return False
''',
    call=f'Solution().searchMatrix({MATRIX}, {TARGET})',
    expect=True,
    views=[
        dict(type='text', fn=_state, size=27),
        dict(type='array', var=_flat, label='a', cell=70,
             pointers={'left': 'red', 'right': 'blue', 'mid': 'yellow'},
             window=('left + 1', 'right - 1'), window_color='yellow',
             color=lambda S, i, v: _rb_flat(S, i)),
        dict(type='grid', var='matrix', label='matrix', h=270, cell=70,
             cursors=[(lambda S: S['mid'] // S['n'], lambda S: S['mid'] % S['n'], 'yellow')],
             color=lambda S, i, j, v: _rb_flat(S, i * S['n'] + j)),
        dict(type='custom', draw=_legend, h=50),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('mid', 'mid', 'yellow'),
           ('x', 'x'), ('target', 'target'), ('n', 'n')],
    captions={
        3: '`m = {m}` 行、`n = {n}` 列：每行拼起来，得到长为 `m·n = {m * n}` 的==递增数组 a==',
        4: '在 a 上用开区间 `(-1, {right})` 二分：`-1` 和 `m·n` 都是虚拟位置',
        5: _while,
        6: '`mid = ({left} + {right}) // 2 = {mid}`',
        7: '`a[{mid}]` 在第 `{mid} // {n} = {mid // n}` 行、第 `{mid} % {n} = {mid % n}` 列 → `x = {x}`',
        8: lambda S, B, ret: (f'`x = {S.x}` 等于 target → ==找到了==' if S.x == S.target
                              else f'`x = {S.x} ≠ {S.target}`，再比大小'),
        9: '返回 `True`',
        10: _cmp,
        11: '`left = mid = {left}`，范围缩小到 `({left}, {right})`',
        13: '`right = mid = {right}`，范围缩小到 `({left}, {right})`',
        14: '区间空了也没找到 → 返回 `False`',
    },
    cards=dict(
        one_liner='把矩阵按行拼成一个递增数组，a[i] = matrix[i // n][i % n]',
        complexity='时间 `O(log(mn))`，空间 `O(1)`',
        problem=['`m × n` 矩阵：每行非严格递增，且==每行第一个数大于上一行最后一个数==',
                 '判断 `target` 是否在矩阵中；要求 `O(log(m·n))`',
                 '示例：`[[1,3,5,7],[10,11,16,20],[23,30,34,60]]`，`3` → `true`；`13` → `false`'],
        quote='如果把矩阵每一行拼在一起，我们可以得到一个递增数组。……==并不需要真的拼成一个长为 mn 的数组 a，而是将 a[i] 转换成矩阵中的行号和列号==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['拼接后 `a = [1,3,5,7,10,11,16,20,23,30,34,60]` 有序 → 直接二分',
              '下标换算：`a[i] = matrix[i // n][i % n]`，如 `i = 9` → 第 2 行第 1 列 = `30`',
              '开区间 `(-1, m·n)` 二分；碰到等于 target 立刻返回 `True`'],
        result='返回 `True`：`a[1] = matrix[0][1] = 3` ✓',
        summary=['时间 `O(log(mn))`，空间 `O(1)`',
                 '换算用的是==列数 n==：`i // n` 行、`i % n` 列，别写成 m',
                 '原题解还有库函数写法：`bisect_left(range(m * n), target, key=...)`',
                 '变形 240 题：没有“下一行更大”、改为每列递增 → 用排除法'],
    ),
)

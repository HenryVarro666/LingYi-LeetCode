MAT = [[1, 1, 9]]
_DIRN = {(1, 0): '南', (1, 1): '东南', (0, 1): '东', (-1, 1): '东北', (-1, 0): '北', (-1, -1): '西北', (0, -1): '西', (1, -1): '西南'}


def _info(S):
    """当前起点 (si,sj)、方向、已生成数字 val 对应的格子；is_prime 里外层 i 被遮住，改由 x,y,val 反推"""
    ln = S.get('_line')
    if 'dx' not in S or 'val' not in S or ln is None:
        return None
    inner = S.get('_inner', {})
    in_prime = 'm' not in inner and 'n' in inner
    if ln in (5, 6, 7, 8) and not in_prime:
        return None
    dx, dy, val = S['dx'], S['dy'], S['val']
    if ln == 8 and not in_prime:
        return None
    k = len(str(val)) - 1
    if in_prime or ln in (12, 13, 14, 15, 10, 11):
        x, y = S['x'], S['y']
        if ln in (14, 15):                       # 已经把 x,y 往前挪了，退回去
            if ln == 14:
                x, y = x - dx, y - dy
            else:
                x, y = x - dx, y
        si, sj = x - k * dx, y - k * dy
        return si, sj, dx, dy, val, k
    return None


def _color(S, i, j, v):
    r = _info(S)
    if r is None:
        if S.get('_line') in (6, 7, 8, 9) and 'j' in S and 'm' in S.get('_inner', {}) and (i, j) == (S['i'], S['j']):
            return 'yellow'
        return None
    si, sj, dx, dy, val, k = r
    for t in range(k + 1):
        if (si + t * dx, sj + t * dy) == (i, j):
            return 'yellow' if t == 0 else 'blue'
    return None


def _top(S):
    r = _info(S)
    if r is None:
        return ''
    si, sj, dx, dy, val, k = r
    return f"起点 `({si},{sj})`，向{_DIRN[(dx, dy)]}走 `{k}` 步 → `val = {val}`"


def _nextdir(S, B):
    if 'dx' in B and (S['dx'], S['dy']) == (B['dx'], B['dy']):
        raise ValueError  # 8 个方向都走完 → 默认字幕
    return f"方向 `({S['dx']},{S['dy']})` = {_DIRN[(S['dx'], S['dy'])]}：从起点往这个方向一直走到边界"


def _fin(S):
    if S.get('_line') in (17, 18, 19, 20, 21, 22, 23) and 'cnt' in S:
        return f"出现次数：`{dict(S['cnt'])}`，找次数最多的（并列取最大）"
    return ''


CONFIG = dict(
    num=3044, title='出现频率最高的质数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举 8 个方向 + Counter 计数',
    tags=['灵神题单', '难度分 1737'],
    code='''
class Solution:
    def mostFrequentPrime(self, mat: List[List[int]]) -> int:
        m, n = len(mat), len(mat[0])
        cnt = Counter()
        for i, row in enumerate(mat):
            for j, v in enumerate(row):
                for dx, dy in (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1):
                    x, y, val = i + dx, j + dy, v
                    while 0 <= x < m and 0 <= y < n:
                        val = val * 10 + mat[x][y]
                        # 如果 val 在 cnt 中，那么 val 一定是质数
                        if val in cnt or self.is_prime(val):
                            cnt[val] += 1
                        x += dx
                        y += dy

        ans, max_cnt = -1, 0
        for v, c in cnt.items():
            if c > max_cnt:
                ans, max_cnt = v, c
            elif c == max_cnt:
                ans = max(ans, v)
        return ans

    def is_prime(self, n: int) -> bool:
        return all(n % i for i in range(2, isqrt(n) + 1))
''',
    call=f'Solution().mostFrequentPrime({MAT})',
    expect=11,
    max_steps=72,
    skip=['x, y, val = i + dx'],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='grid', var=lambda S: MAT, label='mat（黄 = 起点，蓝 = 沿当前方向已经接上的数字）', cell=110, h=210,
             color=_color),
        dict(type='map', var='cnt', label='cnt（质数 → 出现次数）', h=200),
        dict(type='text', fn=_fin, size=24),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('dx,dy', '(dx, dy)'), ('val', 'val', 'yellow')],
    captions={
        'm, n = len': '矩阵 `{m} × {n}`',
        'cnt = Counter()': '`cnt` 统计每个质数出现了几次',
        'for i, row in enumerate': '起点所在行 `i = {i}`',
        'for j, v in enumerate': '起点 `({i},{j})`，数字 `v = {v}`',
        'for dx, dy in': lambda S, B, r: _nextdir(S, B),
        'while 0 <= x < m': lambda S, B, r: (f'`(x,y) = ({S.x},{S.y})` 在矩阵内 → 取下一个数字' if 0 <= S.x < S.m and 0 <= S.y < S.n
                                              else f'`(x,y) = ({S.x},{S.y})` 出界 → 这个方向走完了'),
        'val = val * 10 + mat[x][y]': '接上 `mat[{x}][{y}] = {mat[x][y]}`：`{B.val} × 10 + {mat[x][y]}` = =={val}==',
        'if val in cnt or self.is_prime(val)': lambda S, B, r: (f'`{S.val}` 已在 `cnt` 里 → 它一定是质数，==省掉一次试除==' if S.val in S.cnt
                                                                else f'`{S.val}` 还没出现过，调用 `is_prime` 判断'),
        'cnt[val] += 1': '`{val}` 是质数 → 出现次数 +1：`cnt[{val}] = {cnt[val]}`',
        'x += dx': '沿方向前进：`x` → {x}',
        'y += dy': '`y` → {y}',
        'ans, max_cnt = -1, 0': '`ans` 记录次数最多的质数；先设为 `-1`（没有质数就返回它）',
        'for v, c in cnt.items()': '遍历 `cnt`：`{v}` 出现了 `{c}` 次',
        'if c > max_cnt': lambda S, B, r: (f'`c = {S.c} > max_cnt = {S.max_cnt}`：==次数更多== → 更新答案' if S.c > S.max_cnt
                                           else f'`c = {S.c}` 不比 `max_cnt = {S.max_cnt}` 多，看是否并列'),
        'ans, max_cnt = v, c': '`ans = {ans}`，`max_cnt = {max_cnt}`',
        'elif c == max_cnt': lambda S, B, r: (f'`c == max_cnt = {S.max_cnt}`：次数并列 → 取较大的' if S.c == S.max_cnt
                                              else f'`c = {S.c} < max_cnt = {S.max_cnt}`：忽略'),
        'ans = max(ans, v)': '并列取最大：`ans = max({B.ans}, {v}) = {ans}`',
        'return ans': '次数最多的质数 `{ans}`（出现 `{max_cnt}` 次）',
        'return all(n % i': lambda S, B, r: f'`is_prime({S.n})`：`2 ~ isqrt({S.n})` 都不能整除 → `{r}`',
    },
    cards=dict(
        one_liner='八个方向各走一遍，每走一步得到一个新数；是质数就计数',
        complexity='时间 `O(mnk·10^{k/2})`，空间 `O(mnk)`',
        problem=['`m × n` 矩阵，从每个格子出发，沿 8 个方向之一直线走，沿途数字依次接在后面形成数',
                 '统计所有 ==大于 10 的质数== 的出现频率，返回频率最高的；并列取最大；没有返回 `-1`',
                 '本视频：`[[1,1,9]]` → 生成 11、119、19、11、91、911 → 质数 11 出现两次 → `11`'],
        quote='对于每个单元格，枚举八个方向，生成数字，统计其中质数个数。最后返回出现次数最多的质数，如果有多个这样的质数，返回最大的那个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['三层循环：起点 `(i,j)`、方向 `(dx,dy)`，再沿方向 `while` 前进，`val = val*10 + mat[x][y]`',
              '代码注释的小技巧：==`val in cnt` 说明它一定是质数==，不用再试除',
              '统计完后遍历 `cnt`：次数更大就更新；次数相同取较大的数'],
        summary=['时间 `O(mnk·10^{k/2})`，`k = max(m,n)`，空间 `O(mnk)`',
                 '易错：`val` 至少两位才会入计数（起点本身的一位数不算），所以大于 10 自然满足',
                 '易错：次数并列时返回==较大==的质数；没有任何质数返回 `-1`',
                 '`isqrt` 来自 `math`（Python 3.8+）'],
    ),
)

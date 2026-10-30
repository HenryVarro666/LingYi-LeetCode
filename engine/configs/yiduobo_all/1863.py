NUMS = [5, 1, 6]


def _bits(v, w=3):
    return [(v >> (w - 1 - k)) & 1 for k in range(w)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    inn = S['_inner']
    cur = inn.get('num')
    res = inn.get('res', 0)
    cv.text((x0 + 18, y0 + 4), '逐位看：某一位只要有一个数是 1，OR 的这一位就是 1', 24, T['muted'], bold=True)
    cell, gx, top = 92, x0 + 230, y0 + 64
    for k in range(3):
        cv.text((gx + k * cell + cell / 2, top), f'2^{2 - k}', 22, T['dim'], anchor='mm', mono=True)
    done = set()
    started = 'res' in inn
    for r, v in enumerate(nums):
        y = top + 28 + r * 62
        is_cur = cur is not None and v == cur and S['_line'] in (6, 7)
        cv.text((gx - 20, y + 26), f'nums[{r}] = {v}', 24, T['yellow'] if is_cur else T['text'], anchor='rm', mono=True, bold=is_cur)
        for k, bit in enumerate(_bits(v)):
            fill = (T['yellow'] if is_cur else T['blue']) if bit else (30, 36, 46)
            cv.rect((gx + k * cell + 4, y, gx + (k + 1) * cell - 4, y + 52), fill=fill, r=8)
            cv.text((gx + k * cell + cell / 2, y + 26), bit, 30, T['bg'] if bit else T['dim'], anchor='mm', bold=True, mono=True)
    yo = top + 28 + n * 62 + 8
    cv.line([(gx, yo - 4), (gx + 3 * cell, yo - 4)], T['border'], 2)
    cv.text((gx - 20, yo + 30), f'res = {res}', 24, T['green'], anchor='rm', mono=True, bold=True)
    for k, bit in enumerate(_bits(res)):
        cv.rect((gx + k * cell + 4, yo + 4, gx + (k + 1) * cell - 4, yo + 56), fill=T['green'] if bit else (30, 36, 46), r=8)
        cv.text((gx + k * cell + cell / 2, yo + 30), bit, 30, T['bg'] if bit else T['dim'], anchor='mm', bold=True, mono=True)
    ys = yo + 96
    if S['_line'] >= 9:
        cv.text((x0 + 24, ys), f'res << (n - 1) = {res} << {n - 1} = {res} × {2 ** (n - 1)} = {res << (n - 1)}', 28, T['yellow'], bold=True, mono=True)
        cv.text((x0 + 24, ys + 48), '每个出现过的位：2^(n-1) 个子集的这一位异或为 1', 24, T['muted'])


CONFIG = dict(
    num=1863, title='找出所有子集的异或总和再求和', difficulty='Easy', category='位运算',
    author='yiduobo', technique='按位分析 · 全部取或再左移 n-1 位',
    tags=['灵神核心路线', '灵神题单·位运算', '难度分 1372'],
    code='''
class Solution(object):
    def subsetXORSum(self, nums):

        n = len(nums)
        res = 0
        for num in nums:
            res |= num
        
        return res << (n - 1)
''',
    call='Solution().subsetXORSum([5, 1, 6])',
    expect=28,
    views=[dict(type='custom', draw=_draw, h=420)],
    watch=[('n', 'n', 'cyan'), ('num', 'num', 'yellow'), ('res', 'res', 'green')],
    skip=['n = len(nums)'],
    captions={
        'res = 0': '`res` 从 0 开始，用来累积所有数按位取或的结果',
        'for num in nums': lambda S, B, r: (f'依次取出 `nums` 里的数：现在是 `num = {S.num}`（二进制 `{bin(S.num)[2:].zfill(3)}`）' if S.get('num') != B.get('num')
                                            else '`nums` 取完了，循环结束：`res` 里记着所有出现过的 1 位'),
        'res |= num': lambda S, B, r: f'`res = {B.res} | {S.num} = {S.res}`：{S.num} 的二进制里有 1 的位，`res` 对应位就变成 1',
        'return res': lambda S, B, r: f'`{S.res} << ({S.n} - 1)` = `{S.res} × 2^{S.n - 1}` = =={r}==：每个出现过的位贡献 `2^(n-1)`',
    },
    cards=dict(
        one_liner='某一位上有 1，这一位总和就是 2^(n-1)：全部取或再左移 n-1 位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `nums` 所有子集的异或总和之和（空集为 0）',
                 '元素相同的不同子集要多次计数',
                 '示例：`[5,1,6]` → `28`'],
        before=[dict(heading='先按位拆开（cnt 个 1）', lines=[
            '设第 `i` 位上有 `cnt` 个 1，其余 `n - cnt` 个是 0',
            '异或结果为 1 ⟺ 选了奇数个 1：`C(cnt,1) + C(cnt,3) + ...` 种选法',
            '再乘上 0 的任意取舍：`× 2^(n - cnt)`']),
            dict(heading='用组合恒等式化简', lines=[
                '`C(cnt, k) = C(cnt-1, k-1) + C(cnt-1, k)`，奇数项拆开恰好拼出一整行',
                '奇数个 1 的选法 = `2^(cnt-1)`，再乘 `2^(n-cnt)` = ==`2^(n-1)`==',
                'cnt 是奇数还是偶数，结论一样；只要 `cnt >= 1`']),
        ],
        quote='只需要这些数中的第i位上有1，最终这一位上的和就是2^(n - 1)……可以利用或运算将nums中的数全部取或。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `i` 位全是 0 → 贡献 0；有 1 → 贡献 `2^(n-1) × 2^i`',
              '把所有数取或，得到的数的每个 1 位就是“有 1 的位”',
              '最后乘 `2^(n-1)`，即左移 `n - 1` 位'],
        result='`7 << 2 = 28` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res |= num`：只关心某位“有没有 1”，不用数有几个',
                 '易错：移位是 `n - 1` 位，不是 `n` 位',
                 '原文就是 Python 3 也能直接运行的写法，代码未改动',
                 '对比灵神：灵神用“拿出一个 1、其余随便选”证明，yiduobo 用组合数恒等式推导'],
    ),
)

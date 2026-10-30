A, Z, N_, K = 3, 2, 4, 7
ITEMS = [1] * A + [0] * Z + [-1] * N_


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(ITEMS)
    cell = min(80, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = y0 + 90
    cv.text((x0 + 18, y0 + 4), f'袋子里的物品（k = {K}，黄框 = 被选中的前 k 件）', 22, T['muted'], bold=True)
    for i, v in enumerate(ITEMS):
        X = sx + i * cell
        c = T['green'] if v == 1 else (T['cyan'] if v == 0 else T['pink'])
        cv.rect((X + 4, ys, X + cell - 4, ys + cell - 8), fill=c, r=12)
        cv.text((X + cell / 2, ys + cell / 2 - 4), v, 30, T['bg'], anchor='mm', bold=True, mono=True)
        if i < K:
            cv.rect((X + 1, ys - 4, X + cell - 1, ys + cell - 4), outline=T['yellow'], width=4, r=14)
    for lab, a, b, c in (('1', 0, A, T['green']), ('0', A, A + Z, T['cyan']), ('-1', A + Z, n, T['pink'])):
        xa, xb = sx + a * cell + 4, sx + b * cell - 4
        cv.line([(xa, ys + cell + 14), (xb, ys + cell + 14)], c, 4)
        cv.text(((xa + xb) / 2, ys + cell + 24), f'{lab} 的区间', 20, c, anchor='mt', bold=True)
    cv.text((x0 + 18, ys + cell + 100), '1 不够选 0，0 也不够才选 -1', 28, T['text'], bold=True)


def _case(S):
    k, a, z = S['k'], S['numOnes'], S['numZeros']
    if k <= a:
        return '情况一：`k <= numOnes`，全选 1'
    if k <= a + z:
        return '情况二：1 全选，用 0 补足'
    return '情况三：1、0 全选，还被迫选 -1'


CONFIG = dict(
    num=2600, title='K 件物品的最大和', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='分三种情况讨论 k',
    tags=[],
    code='''
class Solution(object):
    def kItemsWithMaximumSum(self, numOnes, numZeros, numNegOnes, k):

        if k <= numOnes:
            return k
        elif k <= numOnes + numZeros:
            return numOnes
        else:
            return numOnes - (k - numOnes - numZeros)
''',
    call='Solution().kItemsWithMaximumSum(3, 2, 4, 7)',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=_case, size=34),
        dict(type='text', fn=lambda S: f"`numOnes + numZeros = {S['numOnes'] + S['numZeros']}`，`k = {S['k']}`", size=30),
    ],
    watch=['numOnes', 'numZeros', 'numNegOnes', 'k'],
    captions={
        'if k <= numOnes:': '1 的数量 `{numOnes}`，`k = {k}`：{k} <= {numOnes} 吗？成立 → 全选 1，和就是 k；不成立 → 1 不够，再看 0',
        'return k': '全选 1：答案 `k` = =={ret}==',
        'elif k <= numOnes + numZeros': '1 全选了还不够，`k = {k}` 与 `numOnes + numZeros = {numOnes + numZeros}` 比：{k} <= {numOnes + numZeros} 吗？成立 → 用 0 补，不必选 -1；不成立 → ==被迫选 -1==',
        'return numOnes\n': '用 0 补足：和只有所有 1 的贡献 → =={ret}==',
        'else:': '1 和 0 都不够',
        'return numOnes - (': '被迫选 -1 的个数 `k − numOnes − numZeros = {k - numOnes - numZeros}`，答案 = 1 的数量 − -1 的数量 = `{numOnes} − {k - numOnes - numZeros}` = =={ret}==',
    },
    cards=dict(
        one_liner='1 不够选 0，0 也不够才选 -1：对 k 分三段讨论',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['袋子里有 `numOnes` 个 1、`numZeros` 个 0、`numNegOnes` 个 -1',
                 '恰好选 `k` 件，求数字之和的最大值',
                 '本视频：`1×3, 0×2, -1×4, k=7` → `1`'],
        quote='为了使得和最大，很明显应该先选择1，若1不够了再选择0，若0也不够了才选择-1。那么在这里就可以对k的大小进行讨论。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 不超过 1 的个数：全选 1，答案 `k`',
              '`k` 不超过 1 和 0 的个数之和：1 全选，0 补位，答案 `numOnes`',
              '再多：被迫选 `k - numOnes - numZeros` 个 -1，答案 `numOnes` 减去它'],
        summary=['时间、空间都是 `O(1)`',
                 '三个分支互斥，从小到大依次判断，`elif` 里不用再写下界',
                 '易错点：第三种情况要减的是 -1 的个数，不是 `k`',
                 '原文为 Python 2 风格，未改动，直接运行；`numNegOnes` 没有用到'],
    ),
)

BAT = [8, 1, 3, 2]
NN = 2
R0 = sum(BAT) // NN  # 二分右端点初值 7


def _counted(S):
    """已经计入 cnt 的电池个数（内层循环里按 b 的位置算，循环外全部算上）"""
    ln = S.get('_line')
    if 'mid' not in S or ln in (6, 7):
        return 0
    if ln == 8:
        return 0
    if ln in (11, 13) and 'b' in S:
        return BAT.index(S['b']) + 1
    return len(BAT)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mid = S.get('mid')
    cv.text((x0 + 18, y0 + 4), 'batteries：亮色 = 在 mid 轮里最多被消耗的电量 min(b, mid)', 24, T['muted'], bold=True)
    n = len(BAT)
    cell = min(150, (x1 - x0 - 200) / n)
    sx = x0 + 120 + ((x1 - x0 - 200) - cell * n) / 2
    base, top = y1 - 50, y0 + 70
    scale = (base - top) / max(BAT)
    k = _counted(S)
    for i, v in enumerate(BAT):
        X = sx + i * cell
        bw = cell * 0.6
        bx0, bx1 = X + (cell - bw) / 2, X + (cell + bw) / 2
        cv.rect((bx0, base - v * scale, bx1, base), fill=(60, 66, 76), r=4)
        if mid is not None and i < k:
            u = min(v, mid)
            col = T['orange'] if v >= mid else T['cyan']
            cv.rect((bx0, base - u * scale, bx1, base), fill=col, r=4)
            cv.text((X + cell / 2, base - u * scale + 6), f'+{u}', 24, T['bg'], anchor='mt', bold=True)
        cv.text((X + cell / 2, base - v * scale - 4), v, 26, T['text'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 6), i, 18, T['dim'], anchor='mt', mono=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if mid is not None:
        y = base - mid * scale
        cv.dashed((x0 + 110, y), (x1 - 30, y), T['yellow'], 3)
        cv.text((x0 + 100, y), f'mid={mid}', 22, T['yellow'], anchor='rm', bold=True)


def _cand(S, i, v):
    if 'l' not in S:
        return None
    if v < S['l'] or v == S['l'] == S['r']:
        return 'green'
    if v > S['r']:
        return 'red'
    if 'mid' in S and v == S['mid'] and S['_line'] not in (6,):
        return 'yellow'
    return None


def _top(S):
    if 'r' not in S:
        return ''
    l, r = S['l'], S['r']
    if l == r:
        return f'区间缩成一个点 `[{l}, {r}]` → 答案 =={l}=='
    if 'cnt' in S and 'mid' in S:
        return f"区间 `[{l}, {r}]`，试 `mid = {S['mid']}`：已消耗 `cnt = {S['cnt']}`，需要 `n * mid = {NN * S['mid']}`"
    return f'答案在闭区间 `[{l}, {r}]` 里'


def _while(S, B, ret):
    if S.l < S.r:
        return f'`{S.l} < {S.r}`：区间里还有不止一个候选，继续二分'
    return f'`l = r = {S.l}`：只剩一个候选，它就是答案'


def _if(S, B, ret):
    c, need = S.cnt, S.n * S.mid
    if c < need:
        return f'`cnt = {c} < n * mid = {need}`：电不够 → ==无论如何都撑不了 {S.mid} 轮=='
    return f'`cnt = {c} ≥ n * mid = {need}`：电够 → ==必然存在==一种方式撑 {S.mid} 轮'


CONFIG = dict(
    num=2141, title='同时运行 N 台电脑的最长时间', difficulty='Hard', category='二分查找',
    author='yiduobo', technique='二分答案 · 每个数最多消耗 res',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def maxRunTime(self, n, batteries):
        l = 1
        r = sum(batteries) // n

        while l < r:
            mid = (l + r + 1) >> 1
            cnt = 0
            for b in batteries:
                if b >= mid:
                    cnt += mid
                else:
                    cnt += b

            if cnt < n * mid:
                r = mid - 1
            else:
                l = mid

        return l
''',
    call=f'Solution().maxRunTime({NN}, {BAT})',
    expect=6,
    skip=['for b in batteries', 'if b >= mid'],
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var=lambda S: list(range(1, R0 + 1)), cell=70, index=False, h=150, color=_cand,
             label='候选答案 res（绿 = 能撑住，红 = 撑不住，黄 = mid）'),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'cyan'),
           ('n * mid', 'n * mid', 'green')],
    captions={
        'l = 1': '二分最终答案 res：下界 `l = 1`',
        'r = sum': '上界 `r = sum // n = {sum(batteries)} // {n} = {r}`：总电量平均分给 n 台',
        'while l < r': _while,
        'mid = (l + r + 1)': '`mid = ({l} + {r} + 1) >> 1 = {mid}`：==要加一==，否则 `l = mid` 可能死循环',
        'cnt = 0': '统计 mid 轮里所有电池==最多能被消耗多少==',
        'cnt += mid': '`b = {b} ≥ mid`：最多被消耗 ==mid== → `cnt += {mid}` = {cnt}',
        'cnt += b': '`b = {b} < mid`：可能被全部消耗 → `cnt += {b}` = {cnt}',
        'if cnt < n * mid': _if,
        'r = mid - 1': '答案 < {mid}：`r = mid - 1 = {r}`',
        'l = mid': '答案 ≥ {mid}：`l = mid = {l}`',
        'return l': '最多能运行 =={ret}== 分钟',
    },
    cards=dict(
        one_liner='二分答案 res：每个电池在 res 轮里最多被消耗 res',
        complexity='时间 `O(m log C)`，空间 `O(1)`',
        problem=['`n` 台电脑，`batteries[i]` 是第 `i` 个电池能供电的分钟数',
                 '任意整数时刻都能换电池，求 n 台电脑==同时==运行的最长分钟数',
                 '示例：`n = 2, [3,3,3]` → `4`；本视频：`n = 2, [8,1,3,2]` → `6`'],
        quote='问题就变成了给出若干正整数，每次将其中n个正整数减去1，问最多可以减多少轮。……对于每一个数，若其大于等于res，那么在这res轮操作里面，其最多被消耗掉res。',
        quote_src='—— yiduobo 题解原文',
        idea=['转化：每轮选 n 个数各减 1，问最多几轮',
              '直接贪心「每轮减最大的 n 个」数值太大，模拟不了，分析也复杂',
              '二分 res：`Σ min(b, res) ≥ res * n` 就能撑住，否则一定撑不住'],
        summary=['时间 `O(m log C)`，`C = sum / n`；空间 `O(1)`',
                 '`l = mid` 的二分，`mid` 要==向上取整== `(l + r + 1) >> 1`',
                 '充分性：大于等于 res 的数单独分配，小于 res 的从后面的数借来填补',
                 '原文为 Python 2 写法，`sum(batteries) / n` 已改为 `//`，并删去类型说明文档字符串'],
    ),
)

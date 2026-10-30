class _V:
    def __init__(self, fn, name):
        self.fn, self.name = fn, name

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return self.name


def _var(S):
    return S['merged'] if 'res' in S else S['occupiedIntervals']


def _out(S):
    if 'res' in S:
        return S['res']
    out = [list(p) for p in S.get('merged', [])]
    if 'now_x' in S:
        out.append([S['now_x'], S['now_y']])
    return out


def _cur(S):
    try:
        return _var(S).index([S['x'], S['y']])
    except Exception:
        return None


def _txt(S):
    fs, fe = S.get('freeStart'), S.get('freeEnd')
    free = f'空闲 `[{fs}, {fe}]`'
    if 'res' in S:
        return f'{free}　第二步：把合并后的区间减去空闲段 → `res = {S["res"]}`'
    if 'now_x' in S:
        return f'{free}　第一步：合并（绿 = 已定型 + 合并中的 `[{S["now_x"]}, {S["now_y"]}]`）'
    return f'{free}　先合并忙碌区间，再剔除空闲区间里的整数点'


def _merge_if(S, B, ret):
    x, ny = B.x, B.now_y
    if ny + 1 >= x:
        return f'`now_y + 1 = {ny + 1} ≥ x = {x}`：==重叠或相接==，用 `y` 更新终点'
    return f'`now_y + 1 = {ny + 1} < x = {x}`：中间有空档，`[now_x, now_y]` ==定型=='


def _free_if(S, B, ret):
    x, y = S.x, S.y
    if S.freeStart > y or S.freeEnd < x:
        return f'`[{x}, {y}]` 在空闲区间一侧：==不相交==，直接加入答案'
    return f'`[{x}, {y}]` 与空闲区间 `[{S.freeStart}, {S.freeEnd}]` 有重叠：求出重叠部分，两边的空隙留下'


CONFIG = dict(
    num=3975, title='筛选忙碌区间', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先合并，再逐段求与空闲区间的重叠',
    tags=['灵神题单', '贪心算法', '难度分 1533'],
    code='''
class Solution(object):
    def filterOccupiedIntervals(self, occupiedIntervals, freeStart, freeEnd):
        
        occupiedIntervals.sort()

        now_x, now_y = occupiedIntervals[0]
        merged = []
        for x, y in occupiedIntervals:
            if now_y + 1 >= x:
                now_y = max(now_y, y)
            else:
                merged.append([now_x, now_y])
                now_x, now_y = x, y
        
        merged.append([now_x, now_y])

        res = []
        for x, y in merged:
            if freeStart > y or freeEnd < x:
                res.append([x, y])
            else:
                overlap_x = max(x, freeStart)
                overlap_y = min(y, freeEnd)
                if x < overlap_x:
                    res.append([x, overlap_x - 1])
                if overlap_y < y:
                    res.append([overlap_y + 1, y])

        return res
''',
    call='Solution().filterOccupiedIntervals([[2,6],[4,8],[10,10],[10,12],[14,16]], 7, 11)',
    expect=[[2, 6], [12, 12], [14, 16]],
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='intervals', var=_V(_var, '区间（蓝，黄 = 当前）：先是输入，后是合并结果'), out=_V(_out, '结果（绿）：先是合并区间，后是最终 res'),
             pointer=_cur, label='数轴', h=450),
    ],
    watch=[('now_x', 'now_x', 'blue'), ('now_y', 'now_y', 'pink'), ('overlap_x', 'overlap_x', 'cyan'), ('overlap_y', 'overlap_y', 'orange'), ('res', 'res', 'green')],
    captions={
        'occupiedIntervals.sort()': '按起点排序：`{occupiedIntervals}`',
        'now_x, now_y = occupiedIntervals[0]': '`[now_x, now_y]` 记录正在合并的区间，从第一个开始：`[{now_x}, {now_y}]`',
        'merged = []': '`merged` 存放合并定型后的区间',
        'for x, y in occupiedIntervals': lambda S, B, rt: ('看区间 `[{}, {}]`'.format(S.x, S.y) if 'x' not in B or B.x != S.x or B.y != S.y else '区间都看完了'),
        'if now_y + 1 >= x': _merge_if,
        'now_y = max': '`now_y = max({B.now_y}, {y}) = {now_y}`：只需更新终点',
        'merged.append': '`[{now_x}, {now_y}]` 定型，放入 `merged`',
        'now_x, now_y = x, y': '开始合并新区间 `[{now_x}, {now_y}]`',
        'res = []': '合并完成：`merged = {merged}`。接着剔除空闲区间',
        'for x, y in merged': lambda S, B, rt: ('看合并区间 `[{}, {}]`'.format(S.x, S.y) if B.get('res') is None or B.x != S.x or B.y != S.y or len(B.res) != len(S.res) else '合并区间都处理完了'),
        'if freeStart > y': _free_if,
        'res.append([x, y])': '原样放入：`res = {res}`',
        'overlap_x = max': '重叠部分的起点 `max({x}, {freeStart}) = {overlap_x}`',
        'overlap_y = min': '重叠部分的终点 `min({y}, {freeEnd}) = {overlap_y}`',
        'if x < overlap_x': lambda S, B, rt: '`x = {}` 与 `overlap_x = {}`：{}'.format(S.x, S.overlap_x, '前面有空隙，这一段仍然忙碌' if S.x < S.overlap_x else '前面没有空隙'),
        'res.append([x, overlap_x - 1])': '前段 `[{x}, {overlap_x - 1}]` 加入答案',
        'if overlap_y < y': lambda S, B, rt: '`overlap_y = {}` 与 `y = {}`：{}'.format(S.overlap_y, S.y, '后面有空隙，这一段仍然忙碌' if S.overlap_y < S.y else '后面没有空隙'),
        'res.append([overlap_y + 1, y])': '后段 `[{overlap_y + 1}, {y}]` 加入答案',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='两步走：先把重叠/相接的区间合并，再逐段剔除空闲区间',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出若干忙碌区间（含端点），可能重叠，另给一个空闲区间 `[freeStart, freeEnd]`',
                 '先合并重叠或相连的忙碌区间，再移除空闲区间内的整数点',
                 '返回升序的剩余忙碌区间，没有则返回空列表',
                 '示例：`[[2,6],[4,8],[10,10],[10,12],[14,16]]`，`[7,11]` → `[[2,6],[12,12],[14,16]]`'],
        quote='若x小于等于now_y + 1，说明区间是重叠或者相连的，此时应该使用y来更新now_y，否则说明[now_x, now_y]已经定型，此时将其加入到合并后的区间数组中。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后用 `now_x, now_y` 记录合并中的区间，`now_y + 1 >= x` 就并入',
              '合并完得到 `merged`：它们互不重叠，可以逐个处理',
              '与空闲区间的重叠是 `[max(x, freeStart), min(y, freeEnd)]`，两侧的空隙就是留下的区间'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（多存了一个 `merged`）',
                 '相连也要合并，所以判断是 `now_y + 1 >= x`',
                 '合并结束后要把最后一个区间 `merged.append`，别漏',
                 '前段 `[x, overlap_x - 1]`、后段 `[overlap_y + 1, y]` 都要再判断是否非空',
                 '对比灵神：灵神边合并边处理，不存 `merged`；yiduobo 分成两趟，更好读'],
    ),
)

def _cur(S):
    try:
        return S['occupiedIntervals'].index([S['l'], S['r']])
    except Exception:
        return None


def _txt(S):
    fs, fe = S.get('freeStart'), S.get('freeEnd')
    free = f'空闲 `[{fs}, {fe}]`'
    if 'max_r' in S and 'left' in S:
        return f'{free}　当前合并区间 `[{S["left"]}, {S["max_r"]}]`　答案 `{S.get("ans")}`'
    return f'{free}　先合并忙碌区间（含相接），再把空闲段从中挖掉'


def _new(S, B, ret):
    l, mr = B.l, B.max_r
    if l - 1 > mr:
        return f'`l - 1 = {l - 1} > max_r = {mr}`：中间隔着空档，不相交也不相接 → ==发现新区间=='
    return f'`l - 1 = {l - 1} ≤ max_r = {mr}`：重叠或相接（如 `[1,1]`、`[2,2]`）→ 并入当前区间'


def _add_if(S, B, ret):
    l, r = S.l, S.r
    if r < S.freeStart or l > S.freeEnd:
        return f'`[{l}, {r}]` 在空闲 `[{S.freeStart}, {S.freeEnd}]` 的一侧：==不相交==，原样保留'
    return f'`[{l}, {r}]` 与空闲区间有交集：只留下空闲区间之外的前缀 / 后缀'


CONFIG = dict(
    num=3975, title='筛选忙碌区间', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='合并区间 + 挖掉空闲段（余留前后缀）',
    tags=['灵神题单', '贪心算法', '难度分 1533'],
    code='''
class Solution:
    def filterOccupiedIntervals(self, occupiedIntervals: list[list[int]], freeStart: int, freeEnd: int) -> list[list[int]]:
        occupiedIntervals.sort(key=lambda p: p[0])  # 按照左端点从小到大排序
        ans = []

        def add(l: int, r: int) -> None:
            if r < freeStart or l > freeEnd:  # 不相交
                ans.append([l, r])
                return
            if l < freeStart:
                ans.append([l, freeStart - 1])  # 余留前缀
            if r > freeEnd:
                ans.append([freeEnd + 1, r])  # 余留后缀

        left, max_r = occupiedIntervals[0]
        for l, r in occupiedIntervals[1:]:  # 从第二个区间开始
            if l - 1 > max_r:  # 发现一个新区间
                add(left, max_r)  # 先把旧的加入答案
                left = l  # 记录新区间左端点
            max_r = max(max_r, r)
        add(left, max_r)

        return ans
''',
    call='Solution().filterOccupiedIntervals([[2,6],[4,8],[10,10],[10,12],[14,16]], 7, 11)',
    expect=[[2, 6], [12, 12], [14, 16]],
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='intervals', var='occupiedIntervals', out='ans', pointer=_cur, label='数轴：蓝 = 忙碌区间（黄 = 当前），绿 = ans', h=440),
    ],
    watch=[('left', 'left', 'blue'), ('max_r', 'max_r', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'occupiedIntervals.sort': '按左端点排序：`{occupiedIntervals}`',
        'def add': '`add(l, r)`：把一个合并好的区间减去空闲段后放进 `ans`',
        'left, max_r = occupiedIntervals[0]': '第一个区间 `[{left}, {max_r}]` 当作当前合并区间：`left` 是左端点，`max_r` 是右端点最大值',
        'for l, r in': lambda S, B, rt: ('看下一个区间 `[{}, {}]`'.format(S.l, S.r) if 'l' not in B or 'r' not in B or B.l != S.l or B.r != S.r else '区间都看完了'),
        'if l - 1 > max_r': _new,
        'add(left, max_r)  #': '当前合并区间 `[{left}, {max_r}]` 已定型 → 交给 `add` 处理',
        'left = l': '新合并区间的左端点 `left` → =={left}==',
        'max_r = max': '`max_r = max({B.max_r}, {r}) = {max_r}`',
        'if r < freeStart': _add_if,
        'ans.append([l, r])': '原样加入：`ans` = `{ans}`',
        'if l < freeStart': lambda S, B, rt: '`l = {}` 与 `freeStart = {}`：{}'.format(S.l, S.freeStart, '左边有一段在空闲区间之前 → 余留前缀' if S.l < S.freeStart else '没有前缀可留'),
        'ans.append([l, freeStart - 1])': '余留前缀 `[{l}, {freeStart - 1}]`',
        'if r > freeEnd': lambda S, B, rt: '`r = {}` 与 `freeEnd = {}`：{}'.format(S.r, S.freeEnd, '右边有一段在空闲区间之后 → 余留后缀' if S.r > S.freeEnd else '没有后缀可留'),
        'ans.append([freeEnd + 1, r])': '余留后缀 `[{freeEnd + 1}, {r}]`',
        9: '这段已处理完，直接返回（结果都写进了 `ans`）',
        21: '最后一个合并区间 `[{left}, {max_r}]` 还没处理，再 `add` 一次',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='先合并忙碌区间（相接也算），再从每段里挖掉空闲区间',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计返回值）',
        problem=['忙碌区间可能重叠或相接（`[1,1]` 和 `[2,2]` 合并为 `[1,2]`）',
                 '先合并，再去掉空闲区间 `[freeStart, freeEnd]` 里的所有整数点',
                 '返回升序、互不重叠、个数最少的剩余忙碌区间',
                 '示例：`[[2,6],[4,8],[10,10],[10,12],[14,16]]`，空闲 `[7,11]` → `[[2,6],[12,12],[14,16]]`'],
        quote='对于一个合并后的区间 [l,r]：如果 r < freeStart 或者 l > freeEnd，两区间不相交，不变。否则：如果 l < freeStart，余留 [l, freeStart-1]；如果 r > freeEnd，另一个余留 [freeEnd+1, r]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合并模板同 56 题，只是「相接」也要合并：新区间条件是 `l - 1 > max_r`',
              '每合并出一段，就交给 `add`：与空闲区间比位置',
              '一段最多被空闲区间切成「前缀 + 后缀」两块'],
        summary=['时间 `O(n log n)`，瓶颈在排序',
                 '相接要合并：判断用 `l - 1 > max_r`，不是 `l > max_r`',
                 '循环结束后别忘了 `add(left, max_r)` 处理最后一段',
                 '`add` 里 `l < freeStart` 与 `r > freeEnd` 是两个独立的 if，一段可同时留前缀和后缀',
                 '写法二：把合并和挖空放进同一个循环，用 `i == n - 1` 判断收尾，思路相同'],
    ),
)

# setup 里的 Seq 只是普通 list，额外记下 for 循环当前走到的下标 pos（仅用于画图，不影响代码逻辑）
SETUP = '''
import copy
class Seq(list):
    def __init__(self, it):
        super().__init__(it)
        self.live = True
    def __iter__(self):
        return self._walk() if self.live else list.__iter__(self)
    def _walk(self):
        for i in range(len(self)):
            self.pos = i
            yield list.__getitem__(self, i)
        self.pos = len(self)
    def __deepcopy__(self, memo):
        c = Seq([copy.deepcopy(x, memo) for x in list.__iter__(self)])
        c.__dict__.update(self.__dict__)
        c.live = False
        return c
'''


def _cur(S):
    seq = S.get('intervals')
    p = getattr(seq, 'pos', None)
    return p if p is not None and p < len(seq) else None


def _if_cap(S, B, ret):
    p, ans = B.p, B.ans
    if not ans:
        return f'`ans` 为空 → `{p}` 直接成为第一个合并区间'
    r = ans[-1][1]
    if p[0] <= r:
        tail = '（端点相接也算）' if p[0] == r else ''
        return f'`p[0] = {p[0]}` ≤ 合并区间右端点 `{r}`：==相交，可以合并=={tail}'
    return f'`p[0] = {p[0]}` > `{r}`：不相交。后面的左端点只会更大 → 合并区间 `{ans[-1]}` ==固定下来=='


ORIG = sorted([[8, 10], [1, 3], [2, 6], [4, 5], [10, 12], [15, 18]])


def _cmp(S):
    if 'p' not in S or not S.get('ans') or _cur(S) is None:
        return ''
    p, r = S['p'], S['ans'][-1][1]
    return f'`p = {p}`　　`p[0] = {p[0]}` 对比 合并区间右端点 `ans[-1][1] = {r}`'


def _max_cap(S, B, ret):
    old, new, p = B.ans[-1][1], S.ans[-1][1], S.p
    if new != old:
        note = '（`ans` 存的就是 `intervals` 里那个列表，蓝色那条也跟着变）' if list(B.ans[-1]) in ORIG else '；左端点不用动（已排序）'
        return f'右端点 `max({old}, {p[1]}) = {new}` → 合并区间变成 `{S.ans[-1]}`{note}'
    return f'`{p}` 被完全包含：右端点仍是 `max({old}, {p[1]}) = {new}`'


CONFIG = dict(
    num=56, title='合并区间', difficulty='Medium', category='普通数组',
    author='灵茶山艾府', technique='排序 + 一次遍历',
    code='''
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda p: p[0])  # 按照左端点从小到大排序

        ans = []
        for p in intervals:
            if ans and p[0] <= ans[-1][1]:  # 左端点在合并区间内，可以合并
                ans[-1][1] = max(ans[-1][1], p[1])  # 更新合并区间的右端点
            else:  # 不相交，无法合并
                ans.append(p)  # 新的合并区间
        return ans
''',
    setup=SETUP,
    call='Solution().merge(Seq([[8, 10], [1, 3], [2, 6], [4, 5], [10, 12], [15, 18]]))',
    expect=[[1, 6], [8, 12], [15, 18]],
    views=[
        dict(type='text', fn=_cmp),
        dict(type='intervals', var='intervals', out='ans', pointer=_cur, label='数轴：蓝 = intervals（黄 = 当前 p），绿 = ans', h=440),
    ],
    watch=[('p', 'p', 'yellow'), ('ans[-1]', 'ans[-1]', 'green'), ('ans', 'ans', 'green')],
    captions={
        'intervals.sort': '按左端点从小到大排序：`{intervals}`',
        'ans = []': '`ans` 的最后一个区间 = ==当前正在合并的区间==',
        'for p in intervals': lambda S, B, ret: (f'看下一个区间 `p = {S.p}`' if _cur(S) is not None else '所有区间都看完了'),
        'if ans and p[0]': _if_cap,
        'ans[-1][1] = max': _max_cap,
        'ans.append(p)': '新的合并区间 `{p}` 加入 `ans`',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='按左端点排序后从左往右扫：接得上就延长右端点，接不上就开新区间',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计排序栈和返回值）',
        problem=['合并所有==重叠的区间==，返回一个不重叠的区间数组',
                 '端点相接也算重叠：`[1,4]` 和 `[4,5]` → `[1,5]`',
                 '示例：`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`',
                 '演示用 `[[8,10],[1,3],[2,6],[4,5],[10,12],[15,18]]`'],
        quote='把 intervals[0] 加入答案。注意，答案的最后一个区间表示当前正在合并的区间。……按照左端点排序后，合并的区间一定是 intervals 中的连续子数组。',
        quote_src='—— 灵茶山艾府题解「方法一：排序」',
        idea=['排序后，新区间的左端点 ≥ 合并区间的左端点 → ==只需要比较右端点==',
              '`p[0] ≤ ans[-1][1]`：相交，右端点取 `max`（被包含时不变）',
              '`p[0] > ans[-1][1]`：后面的区间更接不上 → 当前合并区间==固定==，开新的'],
        summary=['时间 `O(n log n)`，瓶颈在排序；合并只需一趟',
                 '判断用 `<=`：端点相接也要合并',
                 '右端点要取 `max`：`[1,6]` 遇到 `[4,5]` 不能缩成 `[1,5]`',
                 '`ans.append(p)` 存的是同一个列表：修改 `ans[-1]` 会同时改到 `intervals`（不影响答案）',
                 '题解另有「差分数组」「扫描线」做法；按右端点排序的话要倒着遍历'],
    ),
)

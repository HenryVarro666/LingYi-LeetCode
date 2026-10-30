CONFIG = dict(
    num=497, title='非重叠矩形中的随机点', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='面积前缀和 + 二分',
    tags=['随机化'],
    code='''
import random

class Solution(object):

    def __init__(self, rects):
        self.sum_list = []
        self.col_list = []
        self.point_list = []
        for rect in rects:
            x1, y1, x2, y2 = rect
            self.col_list.append(y2 - y1 + 1)
            self.point_list.append([x1, y1])
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            if not self.sum_list:
                self.sum_list.append(area)
            else:
                self.sum_list.append(self.sum_list[-1] + area)

    def pick(self):
        pos = random.randint(0, self.sum_list[-1] - 1)
        l = 0
        r = len(self.sum_list) - 1
        while l < r:
            mid = (l + r) // 2
            if pos >= self.sum_list[mid]:
                l = mid + 1
            else:
                r = mid

        if l > 0:
            pos -= self.sum_list[l - 1]
        return self.point_list[l][0] + pos // self.col_list[l], self.point_list[l][1] + pos % self.col_list[l]
''',
    setup='import random\nrandom.seed(3)',
    call='''s = Solution([[1, 1, 2, 2], [4, 3, 5, 5], [7, 0, 7, 1]])
out = []
out.append(s.pick())
out.append(s.pick())
out''',
    expect=[(2, 2), (5, 5)],
    views=[
        dict(type='array', var='self.sum_list', label='sum_list（面积前缀和：第 k 个矩形占编号 [sum[k-1], sum[k]) ）', cell=110, h=290,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}, window=('l', 'r')),
        dict(type='array', var='self.col_list', label='col_list（每个矩形的列数）', cell=110, h=160),
        dict(type='text', h=80, size=30, fn=lambda S: ('编号 `pos = {}`'.format(S['pos']) if 'pos' in S else '每个矩形的面积 = 它的整数点个数')),
        dict(type='calls', label='正在执行', h=90),
    ],
    watch=['pos', 'l', 'r', 'mid', 'area'],
    skip=['import random'],
    captions={
        'self.sum_list = []': '`sum_list`：面积的前缀和，单调递增，后面可以二分',
        'self.col_list = []': '`col_list`：每个矩形有几列，用来把编号翻译成坐标',
        'self.point_list = []': '`point_list`：每个矩形的左下角 `(x1, y1)`',
        'for rect in rects': lambda S, B, ret: ('第 {} 个矩形 `{}`'.format(len(S['self.sum_list']), S['rect']) if 'rect' in S and ('rect' not in B or B['rect'] != S['rect']) else '矩形都处理完了'),
        'x1, y1, x2, y2 = rect': '左下角 `({x1}, {y1})`，右上角 `({x2}, {y2})`',
        'self.col_list.append': '列数 = `y2 - y1 + 1` = `{y2 - y1 + 1}`',
        'self.point_list.append': '记下左下角 `[{x1}, {y1}]`',
        'area = ': '整点数（面积）= `{x2 - x1 + 1}` × `{y2 - y1 + 1}` = `{area}`',
        'if not self.sum_list': lambda S, B, ret: ('前缀和还是空的 → 第一个矩形，直接放面积' if not B['self.sum_list'] else '前缀和非空 → 在上一项基础上累加'),
        'self.sum_list.append(area)': '第一项就是 `area` = `{area}`',
        'self.sum_list.append(self.sum_list[-1] + area)': '上一项 `{self.sum_list[-2]}` + `{area}` = `{self.sum_list[-1]}`',
        'pos = random.randint': '所有点按编号 `0 ~ {self.sum_list[-1] - 1}` 排好，随机一个编号 `pos = {pos}`，每个点概率相同',
        'l = 0': '二分区间左端点 `l = 0`',
        'r = len(self.sum_list) - 1': '右端点 `r = {r}`：找 `pos` 落在哪个矩形',
        'while l < r': lambda S, B, ret: ('区间 `[{}, {}]` 还没收缩到一个矩形，继续二分'.format(S.l, S.r) if S.l < S.r else '`l == r = {}`：找到矩形 {}'.format(S.l, S.l)),
        'mid = (l + r) // 2': '取中点 `mid = {mid}`',
        'if pos >= self.sum_list[mid]': lambda S, B, ret: ('`pos = {}` ≥ `sum_list[{}] = {}`：前 {} 个矩形的编号都用完了，`pos` 在右边'.format(S.pos, S.mid, S['self.sum_list'][S.mid], S.mid + 1) if S.pos >= S['self.sum_list'][S.mid]
                                                           else '`pos = {}` < `sum_list[{}] = {}`：`pos` 在 `mid` 或它左边'.format(S.pos, S.mid, S['self.sum_list'][S.mid])),
        'l = mid + 1': '往右找：`l = {l}`',
        'r = mid': '`mid` 本身可能是答案，保留：`r = {r}`',
        'if l > 0': lambda S, B, ret: ('不是第 0 个矩形：要减去前面矩形占掉的编号' if S.l > 0 else '第 0 个矩形：编号起点就是 0，不用减'),
        'pos -= self.sum_list[l - 1]': '减去前缀和 `{self.sum_list[l - 1]}`，得到矩形内的编号 `pos = {pos}`',
        'return self.point_list': lambda S, B, ret: '按 行 = `pos // 列数`、列 = `pos % 列数`（列数 = {}）换成坐标：返回 `{}`'.format(S['self.col_list'][S.l], ret),
    },
    max_steps=90,
    cards=dict(
        one_liner='把所有矩形的整点连续编号，随机一个编号再翻译回坐标',
        complexity='构造 `O(n)`，`pick` 时间 `O(log n)`，空间 `O(n)`',
        problem=['给定若干互不重叠的矩形 `[x1, y1, x2, y2]`',
                 '`pick()`：在所有矩形覆盖的整数点中==等概率==随机取一个点',
                 '本视频：3 个矩形，面积 4、6、2'],
        quote='设面积和为sum，那么我们可以将矩形中的所有点按0到sum - 1进行编号，然后每次从0到sum - 1中随机出一个数，返回对应的点即可。',
        quote_src='—— yiduobo 题解',
        idea=['矩形不重叠，总点数 = 面积之和，给每个点一个唯一编号',
              '第 k 个矩形的编号起点就是面积前缀和，单调 → 二分定位矩形',
              '矩形内第 i 行第 j 列编号为 `i * col + j`，所以 `pos // col`、`pos % col` 还原坐标'],
        summary=['构造 `O(n)`，`pick` 二分 `O(log n)`，空间 `O(n)`',
                 '易错：点数是 `(x2-x1+1) * (y2-y1+1)`，边界上的整点也算',
                 '易错：二分后要减去 `sum_list[l-1]` 才是矩形内的编号',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`mid` 和 `pos // col` 两处）；原文用了 `random` 但没写 import，已补上',
                 '同类随机题：381、710、478'],
    ),
)

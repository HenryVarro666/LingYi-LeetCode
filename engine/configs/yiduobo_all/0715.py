def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'self.f：当前跟踪的区间（左闭右开，蓝色）；黄色 = 本次操作的 [left, right)', 24, T['muted'], bold=True)
    lo, hi = 8, 22
    L, R = x0 + 60, x1 - 60
    X = lambda v: L + (v - lo) / (hi - lo) * (R - L)
    base = y1 - 70
    f = S.get('self.f') or []
    # 上：本次操作区间
    if 'left' in S and 'right' in S and isinstance(S['left'], int) and isinstance(S['right'], int):
        a, b = S['left'], S['right']
        if 'self.f' in S and B.get('left') is not None or True:
            pass
        yy = y0 + 70
        cv.rect((X(a), yy, max(X(b), X(a) + 6), yy + 30), fill=T['yellow'], r=12)
        cv.text((X(a) - 8, yy + 15), a, 22, T['yellow'], anchor='rm', bold=True)
        cv.text((X(b) + 8, yy + 15), b, 22, T['yellow'], anchor='lm', bold=True)
    # 下：当前区间集合
    yy = y0 + 150
    for k, (a, b) in enumerate(f):
        cv.rect((X(a), yy + k * 52, max(X(b), X(a) + 6), yy + k * 52 + 30), fill=T['blue'], r=12)
        cv.text((X(a) - 8, yy + k * 52 + 15), a, 22, T['text'], anchor='rm', bold=True)
        cv.text((X(b) + 8, yy + k * 52 + 15), b, 22, T['text'], anchor='lm', bold=True)
    if not f:
        cv.text((x0 + 18, yy + 4), '（空）', 24, T['dim'])
    cv.line([(L, base), (R, base)], T['border'], 2)
    for v in range(lo, hi + 1):
        cv.text((X(v), base + 8), v, 18, T['dim'], anchor='mt', mono=True)


CONFIG = dict(
    num=715, title='Range 模块', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='有序区间数组 · 线性找左右边界',
    tags=['设计'],
    code='''
class RangeModule(object):

    def __init__(self):
        self.f = []

    def addRange(self, left, right):
        #print 'add %d %d' % (left, right)
        if not self.f:
            self.f = [[left, right]]
            #print self.f
        else:
            l = 0
            while l < len(self.f) and self.f[l][1] < left:
                l += 1
            
            if l == len(self.f):
                self.f.append([left, right])
                #print self.f
                return
            
            r = l
            while r < len(self.f) and self.f[r][0] <= right:
                r += 1
            
            if r == 0:
                self.f = [[left, right]] + self.f
            else:
                r -= 1
                left = min(left, self.f[l][0])
                right = max(right, self.f[r][1])
                self.f = self.f[:l] + [[left, right]] + self.f[r + 1:]
            #print self.f

    def queryRange(self, left, right):
        for index in range(len(self.f)):
            if self.f[index][0] <= left and self.f[index][1] >= right:
                return True

        return False

    def removeRange(self, left, right):
        #print 'remove %d %d' % (left, right)
        if not self.f:
            return

        l = 0
        while l < len(self.f) and self.f[l][1] <= left:
            l += 1
        
        if (l == 0 and right <= self.f[l][0]) or (l == len(self.f)):
            #print self.f
            return
        
        r = l
        while r < len(self.f) and self.f[r][0] < right:
            r += 1
        
        r -= 1
        tmp = []
        if left > self.f[l][0]:
            tmp.append([self.f[l][0], left])
        if right < self.f[r][1]:
            tmp.append([right, self.f[r][1]])
        
        self.f = self.f[:l] + tmp + self.f[r + 1:]
        #print self.f
''',
    call='''m = RangeModule()
m.addRange(10, 12)
m.addRange(16, 20)
m.addRange(11, 17)
m.removeRange(14, 16)
res = [m.queryRange(10, 14), m.queryRange(13, 15), m.queryRange(16, 17)]
res''',
    expect=[True, False, True],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='calls', h=90),
    ],
    watch=['left', 'right', ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('f', 'self.f', 'green')],
    skip=['self.f = []'],
    max_steps=90,
    captions={
        43: '要删的时候列表为空就直接返回；否则往下找被碰到的区间',
        12: '`l` 从 0 开始，找第一个会碰到新区间的位置',
        46: '`l` 从 0 开始，找第一个会被删除碰到的区间',
        54: '`r` 从 `l` 开始，找最后一个被碰到的区间',
        65: '拼接：前面不受影响的 + 残余 `{tmp}` + 后面不受影响的 → `{self.f}`',
        'if not self.f': lambda S, B, ret: ('区间列表为空 → 直接放入 `[{}, {}]`'.format(S.left, S.right) if not S['self.f'] else '列表非空，要找新区间和谁相交'),
        'self.f = [[left, right]]': '直接放入 `[{left}, {right}]`',
        'while l < len(self.f) and self.f[l][1] < left': lambda S, B, ret: ('区间 `{}` 的右端 {} < `left`={} → 整个在新区间左边，跳过'.format(S['self.f'][S.l], S['self.f'][S.l][1], S.left) if S.l < len(S['self.f']) and S['self.f'][S.l][1] < S.left else ('`l` = {}：没有更多区间可跳过了'.format(S.l) if S.l >= len(S['self.f']) else '区间 `{}` 的右端 {} ≥ `left`={} → 碰到新区间了，`l` = {}'.format(S['self.f'][S.l], S['self.f'][S.l][1], S.left, S.l))),
        'l += 1': '`l` → {l}',
        'if l == len(self.f)': lambda S, B, ret: ('所有区间都在左边 → 新区间追加到末尾' if S.l == len(S['self.f']) else '`l` = {}：有区间碰到新区间'.format(S.l)),
        'self.f.append': '追加 `[{left}, {right}]`，结束',
        'r = l': '从 `l` 开始往右找：哪些区间的左端点 ≤ `right`（也就是和新区间相交）',
        'while r < len(self.f) and self.f[r][0] <= right': lambda S, B, ret: ('第 {} 个区间左端 ≤ `right`={} → 相交，继续'.format(S.r, S.right) if S.r < len(S['self.f']) and S['self.f'][S.r][0] <= S.right else '`r` = {}：找到相交区间的右边界（不含）'.format(S.r)),
        'r += 1': '`r` → {r}',
        'if r == 0': lambda S, B, ret: ('`r` = 0 → 一个都不相交，新区间放到最前面' if S.r == 0 else '`r` = {} > 0：区间 {}..{} 都要和新区间合并'.format(S.r, S.l, S.r - 1)),
        'self.f = [[left, right]] + self.f': '新区间放到最前面',
        'r -= 1': '回退一格，`r` = {r} 是最后一个相交的区间',
        'left = min': '合并后左端 = min(新左端, 第 `l` 个区间的左端) = =={left}==',
        'right = max': '合并后右端 = max(新右端, 第 `r` 个区间的右端) = =={right}==',
        'self.f = self.f[:l]': '拼接：前面不相交的 + 合并后的 `[{left}, {right}]` + 后面不相交的 → `{self.f}`',
        'for index in range': '逐个区间检查是否整段包住 `[left, right)`',
        'if self.f[index][0] <= left and': lambda S, B, ret: ('区间 `{}` {}包住 `[{}, {}]`'.format(S['self.f'][S.index], '' if S['self.f'][S.index][0] <= S.left and S['self.f'][S.index][1] >= S.right else '没有', S.left, S.right)),
        'return True': '有一个区间整段包住 → 返回 ==True==',
        'return False': '没有任何区间整段包住 → 返回 ==False==',
        'while l < len(self.f) and self.f[l][1] <= left': lambda S, B, ret: 'l = {}：第一个右端点 > `left` 的区间（它才可能被删到）'.format(S.l),
        'if (l == 0 and': lambda S, B, ret: ('要删的范围没碰到任何区间 → 直接返回' if (S.l == 0 and S.right <= S['self.f'][S.l][0]) or S.l == len(S['self.f']) else '碰到了区间，继续算要保留的部分'),
        'while r < len(self.f) and self.f[r][0] < right': lambda S, B, ret: ('第 {} 个区间左端 < `right`={} → 被碰到，继续'.format(S.r, S.right) if S.r < len(S['self.f']) and S['self.f'][S.r][0] < S.right else '`r` = {}：被碰到的区间到此为止'.format(S.r)),
        'tmp = []': '`tmp` 放删除之后还剩下的两端残余',
        'if left > self.f[l][0]': lambda S, B, ret: ('第一个被碰到的区间左端 {} < `left`={} → 左边残余 `[{}, {}]` 要保留'.format(S['self.f'][S.l][0], S.left, S['self.f'][S.l][0], S.left) if S.left > S['self.f'][S.l][0] else '左边没有残余'),
        'tmp.append([self.f[l][0], left])': '保留左残余 `{tmp}`',
        'if right < self.f[r][1]': lambda S, B, ret: ('最后一个被碰到的区间右端 {} > `right`={} → 右边残余 `[{}, {}]` 要保留'.format(S['self.f'][S.r][1], S.right, S.right, S['self.f'][S.r][1]) if S.right < S['self.f'][S.r][1] else '右边没有残余'),
        'tmp.append([right, self.f[r][1]])': '保留右残余 `{tmp}`',
    },
    cards=dict(
        one_liner='用一个有序区间数组：线性找到左右边界，合并或拆分',
        complexity='每次操作 `O(n)`，空间 `O(n)`（n 为当前区间数）',
        problem=['`addRange(l, r)` 加入左闭右开区间 `[l, r)`，`removeRange` 删除，`queryRange` 问 `[l, r)` 是否被==完全跟踪==',
                 '示例：加 `[10,20)`，删 `[14,16)`',
                 '查询 `(10,14)` 真、`(13,15)` 假、`(16,17)` 真'],
        quote='我在这里用了比较偷懒的做法，没有使用任何高级数据结构，直接用数组来维护当前所有的区间，然后线性查找当前加入或删去的区间的左右边界位于现有的哪两个区间当中，然后执行区间合并或拆分的操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组里的区间互不相交、从左到右有序',
              '加入：找到第一个碰到新区间的 `l` 和最后一个 `r`，把 `l..r` 合并成 `min/max` 的大区间',
              '删除：同样找 `l..r`，只保留两端露在外面的残余'],
        summary=['每次操作线性扫描 `O(n)`；作者说更好的做法是平衡二叉树，或用动态开点线段树',
                 '易错：加入时用 `<` 与 `<=`（相邻也要合并），删除时用 `<=` 与 `<`（区间左闭右开）',
                 '`queryRange` 必须被==单个==区间整段包住，因为相邻区间已经合并',
                 '原文有被注释掉的 `print` 调试语句，原样保留；无需改成 Python 3',
                 '同类题：56 合并区间、2276 统计区间中的整数数目'],
    ),
)

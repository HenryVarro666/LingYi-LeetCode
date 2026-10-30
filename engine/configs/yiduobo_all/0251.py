def _pos(S):
    v = S.get('self.vec')
    if v is None:
        return ''
    if 'self.vec_p' not in S:
        return ''
    return f"`vec_p = {S['self.vec_p']}`，`iter_p = {S['self.iter_p']}`"


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'vec（行 = 子数组；蓝框 = 下一个要返回的位置 vec_p / iter_p）', 24, T['muted'], bold=True)
    vec = S.get('self.vec') or S.get('vec')
    if vec is None:
        return
    vp, ip = S.get('self.vec_p'), S.get('self.iter_p')
    cell, rowh = 64, 62
    y = y0 + 52
    for r, row in enumerate(vec):
        done = vp is not None and r < vp
        cur = vp is not None and r == vp
        cv.text((x0 + 30, y + rowh / 2 - 8), f'vec[{r}]', 22, T['blue'] if cur else T['dim'], anchor='lm', mono=True, bold=cur)
        if not row:
            cv.text((x0 + 150, y + rowh / 2 - 8), '[ ] 空子数组', 22, T['dim'], anchor='lm')
        for c, v in enumerate(row):
            X = x0 + 150 + c * cell
            used = done or (cur and ip is not None and c < ip)
            here = cur and ip is not None and c == ip
            fill = T['blue'] if here else ((60, 66, 76) if used else T['panel2'])
            cv.rect((X, y, X + cell - 6, y + rowh - 16), fill=fill, r=8, outline=T['border'], width=2)
            cv.text((X + (cell - 6) / 2, y + (rowh - 16) / 2), v, 26, T['bg'] if here else (T['dim'] if used else T['text']), anchor='mm', bold=True)
        y += rowh
    if vp is not None and vp >= len(vec):
        cv.text((x0 + 30, y + 10), '所有子数组都走完了：hasNext = False', 24, T['green'], anchor='lm', bold=True)


CONFIG = dict(
    num=251, title='展开二维向量', difficulty='Medium', category='设计',
    author='yiduobo', technique='两个指针 vec_p / iter_p · 不展开',
    code='''
class Vector2D(object):

    def __init__(self, vec):
        self.vec = vec[:]
        self.vec_p = 0
        self.iter_p = 0
        while self.vec_p < len(self.vec) and self.iter_p == len(self.vec[self.vec_p]):
            self.vec_p += 1

    def next(self):
        res = self.vec[self.vec_p][self.iter_p]
        self.iter_p += 1
        while self.vec_p < len(self.vec) and self.iter_p == len(self.vec[self.vec_p]):
            self.iter_p = 0
            self.vec_p += 1
        return res

    def hasNext(self):
        return self.vec_p != len(self.vec)
''',
    call='''v = Vector2D([[], [1, 2], [], [3]])
out = []
while v.hasNext():
    out.append(v.next())
out''',
    expect=[1, 2, 3],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=lambda S: _pos(S), size=30, h=60),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('vec_p', "self.vec_p", 'blue'), ('iter_p', "self.iter_p", 'pink'), ('res', 'res', 'green')],
    captions={
        'self.vec = vec[:]': '拷贝一份二维数组，==不展开==成一维',
        'self.vec_p = 0': '`vec_p`：当前在第几个子数组',
        'self.iter_p = 0': '`iter_p`：当前在子数组的第几个元素',
        'while self.vec_p < len(self.vec) and self.iter_p == len(self.vec[self.vec_p])': lambda S, B, ret: (
            f"`vec_p = {S['self.vec_p']}` 的子数组走完了（长度 {len(S['self.vec'][S['self.vec_p']])}）→ ==跳过它（可能是空数组）==" if S['self.vec_p'] < len(S['self.vec']) and S['self.iter_p'] == len(S['self.vec'][S['self.vec_p']])
            else ('`vec_p` 到头了，没有更多数' if S['self.vec_p'] >= len(S['self.vec']) else f"`iter_p = {S['self.iter_p']}` 还没走完这个子数组 → 停，指向下一个有数的位置")),
        'self.vec_p += 1': '换到下一个子数组：`vec_p` → {self.vec_p}',
        'res = self.vec': '取出当前位置的数：`vec[{self.vec_p}][{self.iter_p}]` = =={res}==',
        'self.iter_p += 1': '`iter_p` 后移一格 → {self.iter_p}',
        'self.iter_p = 0': '换行后 `iter_p` 归零',
        'return res': '`next` 返回 `{ret}`',
        'return self.vec_p != len(self.vec)': lambda S, B, ret: f"`vec_p = {S['self.vec_p']}`，共 {len(S['self.vec'])} 个子数组 → `hasNext` = ==" + ('还有' if ret else '没有了') + '==',
        'v = Vector2D': '构造：`[[], [1, 2], [], [3]]`，第一个子数组是空的',
        'out.append': '`out` 收集每次 `next` 的返回值',
    },
    cards=dict(
        one_liner='不展开：用两个指针记下走到哪个子数组的第几个数',
        complexity='`next` / `hasNext` 均摊 `O(1)`，空间 `O(1)`（不含拷贝）',
        problem=['实现迭代器 `Vector2D(vec)`：`next()` 返回下一个数，`hasNext()` 判断还有没有',
                 '二维数组里==可能有空的子数组==，要跳过',
                 '示例：`[[], [1,2], [], [3]]` 依次取出 `1, 2, 3`'],
        quote='不进行展开，而是使用两个变量vec_p和iter_p分别记录当前访问到哪个子数组的第几个元素，然后逐渐向后移动。……需要注意的是，题目中可能存在空的子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['两种做法：初始化时展开成一维，或不展开用两个指针；这里选==第二种==',
              '`vec_p` 指第几个子数组，`iter_p` 指其中第几个元素',
              '每次移动后立刻 `while` 跳过走完的（含空的）子数组，保证指针总指向一个真实的数'],
        summary=['`next` / `hasNext` 均摊 `O(1)`，只多存两个下标',
                 '易错：空子数组出现在开头、中间或结尾，构造函数里也要先跳一次',
                 '`hasNext` 只需判断 `vec_p != len(vec)`，因为指针总是停在有数的位置',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)

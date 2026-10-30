def _taken(S):
    v1, v2, p1, p2 = S['self.v1'], S['self.v2'], S['self.p1'], S['self.p2']
    out, i, j, f = [], 0, 0, True
    while i < p1 or j < p2:
        if (f or j == p2) and i < p1:
            out.append(v1[i]); i += 1
        else:
            out.append(v2[j]); j += 1
        f = not f
    return out


CONFIG = dict(
    num=281, title='锯齿迭代器', difficulty='Medium', category='设计',
    author='yiduobo', technique='两个指针 + 轮换标志',
    code='''
class ZigzagIterator(object):

    def __init__(self, v1, v2):
        self.v1 = v1[:]
        self.v2 = v2[:]
        self.p1 = self.p2 = 0
        self.flag = True

    def next(self):
        if (self.flag or self.p2 == len(self.v2)) and self.p1 < len(self.v1):
            res = self.v1[self.p1]
            self.p1 += 1
        else:
            res = self.v2[self.p2]
            self.p2 += 1

        self.flag = not self.flag
        return res

    def hasNext(self):
        return self.p1 < len(self.v1) or self.p2 < len(self.v2)
''',
    call='''z = ZigzagIterator([1, 2, 3], [4, 5])
out = []
while z.hasNext():
    out.append(z.next())
out''',
    expect=[1, 4, 2, 5, 3],
    views=[
        dict(type='array', var='self.v1', label='v1', pointers={'self.p1': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if i < S.get('self.p1', 0) else None),
        dict(type='array', var='self.v2', label='v2', pointers={'self.p2': 'pink'}, h=170,
             color=lambda S, i, v: 'green' if i < S.get('self.p2', 0) else None),
        dict(type='text', fn=lambda S: ('下一次轮到 ==v1==' if S.get('self.flag') else '下一次轮到 ==v2==') if 'self.flag' in S else '', h=60),
        dict(type='text', size=32, h=90, fn=lambda S: ('已取出（锯齿顺序）：==' + ' '.join(str(x) for x in _taken(S)) + '==') if 'self.v1' in S else ''),
    ],
    watch=[('p1', 'self.p1', 'blue'), ('p2', 'self.p2', 'pink'), ('flag', 'self.flag', 'yellow'), ('res', 'res', 'green')],
    captions={
        'self.v1 = v1': '复制 v1，两个数组各自保存',
        'self.p1 = self.p2': '`p1`、`p2` 分别记录 v1、v2 迭代到哪了，都从 0 开始',
        'self.flag = True': '`flag` 表示下一次该取哪边：==True 取 v1==，False 取 v2',
        'if (self.flag': lambda S, B, r: (
            f'`flag` = {B["self.flag"]}，`p2` = {B["self.p2"]}（v2 共 {len(B["self.v2"])} 个）'
            f'，`p1` = {B["self.p1"]}（v1 共 {len(B["self.v1"])} 个）'
            + ('：轮到 v1 且 v1 还有 → 取 v1' if (B['self.flag'] or B['self.p2'] == len(B['self.v2'])) and B['self.p1'] < len(B['self.v1'])
               else '：本轮不能取 v1（没轮到，或 v1 已空）→ 去 v2')),
        'res = self.v1': '取 v1 当前元素：`res` = =={res}==',
        'self.p1 += 1': 'v1 的进度前进：`p1` → {self.p1}',
        'res = self.v2': '取 v2 当前元素：`res` = =={res}==',
        'self.p2 += 1': 'v2 的进度前进：`p2` → {self.p2}',
        'self.flag = not': '轮换标志取反：`flag` → {self.flag}，下次换另一边',
        'return res': '返回 `{res}`',
        'return self.p1 <': lambda S, B, r: f'`p1 < len(v1)` 或 `p2 < len(v2)` 还有一边没取完 → {r}',
    },
    cards=dict(
        one_liner='两个进度指针 + 一个标志位，交替从两个数组取数',
        complexity='`next` / `hasNext` 均 `O(1)`，空间 `O(n)`',
        problem=['给两个一维数组 `v1`、`v2`，实现迭代器 `ZigzagIterator`，==交替==返回两个数组的元素',
                 '一个数组取完后，继续取另一个数组剩下的元素',
                 '`next()` 返回下一个元素，`hasNext()` 判断是否还有元素',
                 '示例：`v1=[1,2]`, `v2=[3,4,5,6]` → `1,3,2,4,5,6`',
                 '本视频：`[1,2,3]` 和 `[4,5]` → `1,4,2,5,3`'],
        quote='使用两个变量分别记录当前的v1和v2迭代的进度，同时再使用一个变量flag表示下一次迭代应该在v1中进行还是在v2中进行。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p1`、`p2` 是两个数组各自的读取位置',
              '`flag` 决定本轮读哪边；==每取一个就取反==',
              '轮到的那边已取完时，条件里的 `p2 == len(v2)` 让它继续读 v1，反过来则落到 else 读 v2'],
        summary=['`next` / `hasNext` 都是 `O(1)`，构造时复制两个数组，空间 `O(n)`',
                 '易错点：`flag` 为 False 但 v2 已取完时，要回头读 v1，所以条件里多了 `self.p2 == len(self.v2)`',
                 '原文为 Python 2 风格，只删去了 `__init__` 里的类型说明文档字符串'],
    ),
)

def _bs(S):
    if 'mid' in S and 'l' in S and 'r' in S:
        return f"二分：`l = {S['l']}`  `r = {S['r']}`  `mid = {S['mid']}`  `pos = {S.get('pos')}`"
    return '新数 `val = ' + str(S['val']) + '`' if 'val' in S else ''


CONFIG = dict(
    num=352, title='将数据流变为多个不相交区间', difficulty='Hard', category='设计',
    author='yiduobo', technique='有序区间列表 · 二分',
    code='''
class SummaryRanges(object):

    def __init__(self):
        self.interval_list = []

    def addNum(self, val):
        if not self.interval_list:
            self.interval_list = [[val, val]]
        
        elif val < self.interval_list[0][0]:
            if val == self.interval_list[0][0] - 1:
                self.interval_list[0][0] -= 1
            else:
                self.interval_list = [[val, val]] + self.interval_list
        
        elif val > self.interval_list[-1][0]:
            if val <= self.interval_list[-1][1]:
                pass
            elif val == self.interval_list[-1][1] + 1:
                self.interval_list[-1][1] += 1
            else:
                self.interval_list.append([val, val])

        else:
            l = 0
            r = len(self.interval_list) - 1
            pos = None
            while l <= r:
                mid = (l + r) // 2
                if self.interval_list[mid][0] == val:
                    return
                elif self.interval_list[mid][0] < val:
                    pos = mid
                    l = mid + 1
                else:
                    r = mid - 1

            if val <= self.interval_list[pos][1]:
                return
            
            if val == self.interval_list[pos][1] + 1:
                if self.interval_list[pos + 1][0] - 1 == val:
                    self.interval_list = self.interval_list[:pos] + [[self.interval_list[pos][0], self.interval_list[pos + 1][1]]] + self.interval_list[pos + 2:]
                else:
                    self.interval_list[pos][1] += 1
            elif self.interval_list[pos + 1][0] - 1 == val:
                self.interval_list[pos + 1][0] -= 1
            else:
                self.interval_list = self.interval_list[:pos + 1] + [[val, val]] + self.interval_list[pos + 1:]

    def getIntervals(self):
        return self.interval_list
''',
    call='''s = SummaryRanges()
s.addNum(1)
s.addNum(3)
s.addNum(7)
s.addNum(2)
s.addNum(6)
s.getIntervals()''',
    expect=[[1, 3], [6, 7]],
    max_steps=90,
    views=[
        dict(type='text', fn=_bs, h=70),
        dict(type='intervals', var='self.interval_list', label='interval_list（按左端点有序的不相交区间）', h=330),
        dict(type='text', fn=lambda S: ('`interval_list = ' + str(S['self.interval_list']).replace(' ', '') + '`') if 'self.interval_list' in S else '', h=70),
    ],
    watch=[('val', 'val', 'blue'), 'l', 'r', 'mid', ('pos', 'pos', 'pink')],
    captions={
        'self.interval_list = []': '用一个按左端点排序的 list 保存所有区间',
        'if not self.interval_list': lambda S, B, r: ('list 为空：第一个数直接成为区间 `[val, val]`' if not S.self.interval_list else '已有区间，继续分情况'),
        8: '空的时候：新建区间 `[{val}, {val}]`',
        'elif val < self.interval_list[0][0]': lambda S, B, r: (f'`{S.val}` 比最左区间的左端点 `{S.self.interval_list[0][0]}` 还小 → 只可能出现在最前面' if S.val < S.self.interval_list[0][0] else f'`{S.val}` 不在最左区间之前，看是否在最右'),
        'elif val > self.interval_list[-1][0]': lambda S, B, r: (f'`{S.val}` 大于最右区间左端点 `{S.self.interval_list[-1][0]}` → 只看最右区间' if S.val > S.self.interval_list[-1][0] else f'`{S.val}` 落在中间，需要二分找位置'),
        'elif val == self.interval_list[-1][1] + 1': lambda S, B, r: (f'`{S.val}` 刚好紧挨最右区间右端点 → 只需扩展右端点' if S.val == S.self.interval_list[-1][1] + 1 else f'`{S.val}` 不紧挨最右区间 → 要新开一个区间'),
        'self.interval_list.append([val, val])': '孤立的数：`[{val}, {val}]` 追加到尾部',
        'l = 0': '中间情况：在区间左端点上二分，找最后一个左端点 `<= val` 的区间 `pos`',
        'r = len(self': '`r` 指向最后一个区间：`r = {r}`',
        'pos = None': '`pos` 记录“最后一个左端点 <= val 的区间”，先设为空',
        'while l <= r': '`l = {l}`，`r = {r}`',
        'mid = (l + r) // 2': '`mid = ({l} + {r}) // 2 = {mid}`',
        'elif self.interval_list[mid][0] < val': lambda S, B, r: (f'`mid` 区间左端点 `{S.self.interval_list[S.mid][0]}` < `{S.val}`：它是候选，向右继续找' if S.self.interval_list[S.mid][0] < S.val else f'`mid` 区间左端点 `{S.self.interval_list[S.mid][0]}` > `{S.val}`：太靠右，向左找'),
        'pos = mid': '记下候选 `pos = {pos}`',
        'l = mid + 1': '`l` → {l}',
        'r = mid - 1': '`r` → {r}',
        'if val <= self.interval_list[pos][1]': lambda S, B, r: (f'`{S.val} <= {S.self.interval_list[S.pos][1]}`：已经在区间里，什么都不用做' if S.val <= S.self.interval_list[S.pos][1] else f'`{S.val}` 大于区间 `pos` 的右端点 `{S.self.interval_list[S.pos][1]}`：不在里面，看是否相邻'),
        'if val == self.interval_list[pos][1] + 1': lambda S, B, r: (f'`{S.val}` 紧挨 `pos` 区间右端点（{S.self.interval_list[S.pos][1]} + 1）' if S.val == S.self.interval_list[S.pos][1] + 1 else f'`{S.val}` 不紧挨 `pos` 区间右端点，再看右边那个区间'),
        42: lambda S, B, r: (f'同时紧挨右边区间的左端点 `{S.self.interval_list[S.pos + 1][0]}` → 两个区间被它连起来' if S.self.interval_list[S.pos + 1][0] - 1 == S.val else '右边区间不相邻：只扩展 `pos` 区间的右端点'),
        'self.interval_list = self.interval_list[:pos] + [[': '合并：`pos` 区间的左端点 + `pos+1` 区间的右端点，替换这两个区间 → `{self.interval_list}`',
        'self.interval_list[pos][1] += 1': '`pos` 区间右端点 +1 → `{self.interval_list}`',
        46: lambda S, B, r: (f'`{S.val}` 紧挨右边区间的左端点 `{S.self.interval_list[S.pos + 1][0]}`' if S.self.interval_list[S.pos + 1][0] - 1 == S.val else f'`{S.val}` 两边都不相邻 → 要新开区间'),
        'self.interval_list[pos + 1][0] -= 1': '右边区间的左端点 −1，把 `{val}` 吞进去 → `{self.interval_list}`',
        'self.interval_list[:pos + 1] + [[val, val]]': '插入 `[{val}, {val}]` 到 `pos` 与 `pos+1` 之间 → `{self.interval_list}`',
        'return self.interval_list': '直接返回有序区间列表 `{ret}`',
    },
    cards=dict(
        one_liner='有序区间列表 + 二分：新数要么新开、要么扩展、要么连接',
        complexity='`addNum` 最坏 `O(n)`（list 插入/删除），查找 `O(log n)`',
        problem=['数据流依次给出非负整数，随时用 `getIntervals` 返回当前所有数字组成的==不相交区间==列表（按起点升序）',
                 '例：依次加入 `1,3,7,2,6` → `[[1,3],[6,7]]`',
                 '加入 `2` 时，`[1,1]` 与 `[3,3]` 会被连成 `[1,3]`'],
        quote='对于新来的一个数，首先通过比较区间左端点找到这个数应该位于哪两个区间之间，然后判断……形成新的独立区间 / 融入左侧或者右侧的区间 / 连接两个区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间列表按左端点有序，先处理头部、尾部的特殊情况',
              '落在中间：二分找到最后一个左端点 `<= val` 的区间 `pos`',
              '看 `val` 与 `pos`、`pos+1` 是否相邻：都邻 → 合并；一边邻 → 扩展；都不邻 → 插入',
              '原文说明：平衡树可把 O(n) 的插入删除降到 O(log n)，这里偷懒用 list'],
        summary=['查找 `O(log n)`，list 插入/合并 `O(n)`，理论最坏 `O(n^2)`',
                 '易错：`val` 已在区间内要直接返回，别重复扩展',
                 '易错：同时邻接左右两区间时要合并，而不是只扩展一侧',
                 '原文为 Python 2 写法，二分里的 `/` 已改为 `//`，并删去了 `__init__` 的文档字符串'],
    ),
)

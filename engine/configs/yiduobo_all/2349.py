CONFIG = dict(
    num=2349, title='设计数字容器系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='每个数字一个堆 + 查询时懒处理',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1540'],
    code='''
class NumberContainers(object):

    def __init__(self):
        self.heap_dict = {}
        self.pos = {}

    def change(self, index, number):
        if self.pos.get(index, 0) == number:
            return
        
        if number not in self.heap_dict:
            self.heap_dict[number] = []

        self.pos[index] = number
        heapq.heappush(self.heap_dict[number], index)

    def find(self, number):
        while number in self.heap_dict and self.heap_dict[number] and self.pos.get(self.heap_dict[number][0], 0) != number:
            heapq.heappop(self.heap_dict[number])
        
        if number in self.heap_dict and self.heap_dict[number]:
            res = self.heap_dict[number][0]
        else:
            res = -1
        
        return res
''',
    call='''nc = NumberContainers()
out = [nc.find(10)]
nc.change(2, 10); nc.change(1, 10); nc.change(2, 10)
out.append(nc.find(10))
nc.change(1, 20)
out.append(nc.find(10))
out''',
    expect=[-1, 1, 2],
    views=[
        dict(type='map', var='self.pos', label='pos（下标 → 现在的数字）', fmt=lambda k, v: f'{k} → {v}', h=110),
        dict(type='map', var='self.heap_dict', label='heap_dict（数字 → 下标的堆，堆顶 = 最小下标）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['index', 'number', ('res', 'res', 'green'), ('out', 'out', 'orange')],
    captions={
        9: '相同就直接返回：不重复入堆',
        'self.heap_dict = {}': '`heap_dict`：每个数字一个堆，存它出现过的下标',
        'self.pos = {}': '`pos`：下标 → ==现在==的数字（下标可达 10^9，所以用哈希表）',
        'if self.pos.get(index, 0) == number': lambda S, B, r: (
            f'`change({S.index}, {S.number})`：下标 `{S.index}` 已经是 `{S.number}` → 什么都不用做' if S.get('self') and S.self.pos.get(S.index, 0) == S.number
            else f'`change({S.index}, {S.number})`：下标 `{S.index}` 现在不是 `{S.number}`，要放进去'),
        'if number not in self.heap_dict': lambda S, B, r: (f'数字 `{S.number}` 还没有堆，新建一个' if S.number not in S.self.heap_dict
                                                            else f'数字 `{S.number}` 已有堆'),
        'self.heap_dict[number] = []': '给 `{number}` 建一个空堆',
        'self.pos[index] = number': '`pos[{index}] = {number}`：更新下标现在的数字（旧数字的堆里不删，之后查询时再清理）',
        'heapq.heappush(self.heap_dict[number], index)': '把下标 `{index}` 放进数字 `{number}` 的堆',
        'while number in self.heap_dict': lambda S, B, r: (
            f'`find({S.number})`：这个数字没有堆（或堆空了）→ 不用清理' if not S.self.heap_dict.get(S.number) else
            (f'堆顶下标 `{S.self.heap_dict[S.number][0]}`，`pos` 里现在是 `{S.self.pos.get(S.self.heap_dict[S.number][0], 0)}`，不是 `{S.number}` → ==被替换掉了，要删=='
             if S.self.pos.get(S.self.heap_dict[S.number][0], 0) != S.number else
             f'堆顶下标 `{S.self.heap_dict[S.number][0]}`，`pos` 里正是 `{S.number}` → 有效，停止清理')),
        'heapq.heappop(self.heap_dict[number])': '堆顶和 `pos` 的记录不一致：弹出这条过期数据',
        'if number in self.heap_dict and self.heap_dict[number]': lambda S, B, r: (
            f'堆里还有下标，堆顶就是最小下标' if S.self.heap_dict.get(S.number) else f'没有这个数字 → 答案 `-1`'),
        'res = self.heap_dict[number][0]': '`res` = 堆顶 = =={res}==',
        'res = -1': '没有 `{number}` → `res = -1`',
        'return res': lambda S, B, r: f'返回 =={r}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='每个数字一个堆，被替换的下标等到查询时再清理',
        complexity='change `O(log q)`，find 均摊 `O(log q)`；空间 `O(q)`',
        problem=['`change(index, number)`：在下标处填数字，已有则替换',
                 '`find(number)`：返回该数字的最小下标，没有返回 `-1`',
                 '本视频：`find(10)=-1` → 填入 `2,1,2` → `find(10)=1` → `change(1,20)` → `find(10)=2`'],
        quote='由于是动态的最小值，那么第一想法就是使用堆来维护这些下标。在这里可以使用若干个堆，每个堆单独维护某一个特定数字的所有下标，那么堆顶自然就是要找的最小值了。',
        quote_src='—— yiduobo 题解原文',
        idea=['下标可达 `10^9`：用哈希表 `pos` 记录下标现在的数字',
              '作者说也可以==懒处理==：替换时不去旧堆里删，等 `find` 的结果和 `pos` 不一致再删',
              '`change` 时若下标本来就是这个数字，直接返回，避免重复入堆'],
        summary=['change `O(log q)`，find 每条过期数据最多弹一次，均摊 `O(log q)`',
                 '易错：`find` 必须比较堆顶下标在 `pos` 里的数字，不一致才弹',
                 '`pos.get(index, 0)`：数字至少为 1，所以用 `0` 表示该下标还没有数字',
                 '对比灵神：灵神 change 总是 push，yiduobo 多一个“相同就直接返回”的剪枝'],
    ),
)

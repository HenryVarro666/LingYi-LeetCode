CONFIG = dict(
    num=2349, title='设计数字容器系统', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + 懒删除堆',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1540'],
    code='''
class NumberContainers:
    def __init__(self):
        self.index_to_number = {}
        self.number_to_indices = defaultdict(list)

    def change(self, index: int, number: int) -> None:
        # 添加新数据
        self.index_to_number[index] = number
        heappush(self.number_to_indices[number], index)

    def find(self, number: int) -> int:
        indices = self.number_to_indices[number]
        while indices and self.index_to_number[indices[0]] != number:
            heappop(indices)  # 堆顶货不对板，说明是旧数据，删除
        return indices[0] if indices else -1
''',
    call='''nc = NumberContainers()
out = [nc.find(10)]
nc.change(2, 10); nc.change(1, 10); nc.change(3, 10)
out.append(nc.find(10))
nc.change(1, 20)
out.append(nc.find(10))
out''',
    expect=[-1, 1, 2],
    views=[
        dict(type='map', var='self.index_to_number', label='index_to_number（下标 → 现在的数字）', fmt=lambda k, v: f'{k} → {v}', h=110),
        dict(type='map', var='self.number_to_indices', label='number_to_indices（数字 → 下标的最小堆，含旧数据）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='heap', var='indices', label='indices（正在查询的堆）', top_color='blue', h=110),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['index', 'number', ('out', 'out', 'green')],
    captions={
        'self.index_to_number = {}': '哈希表：下标 → ==现在==放的数字',
        'self.number_to_indices = defaultdict(list)': '哈希表套最小堆：数字 → 它出现过的下标；堆顶 = 最小下标',
        'self.index_to_number[index] = number': lambda S, B, r: (
            f'`change({S.index}, {S.number})`：下标 `{S.index}` 原来是 `{B["self"].index_to_number[S.index]}`，现在改成 `{S.number}`（直接覆盖，旧数字的堆不动）'
            if S.index in B['self'].index_to_number else
            f'`change({S.index}, {S.number})`：下标 `{S.index}` 第一次放数字，记下是 `{S.number}`'),
        'heappush(self.number_to_indices[number], index)': lambda S, B, r: (
            f'把 `{S.index}` 放进数字 `{S.number}` 的堆（最小堆，堆顶是最小下标）。旧数字的堆里 ==不删== `{S.index}`，留给 find 懒处理'
            if any(S.index in v for k, v in B['self.number_to_indices'].items() if k != S.number) else
            f'把 `{S.index}` 放进数字 `{S.number}` 的堆（最小堆，堆顶是最小下标）'),
        'indices = self.number_to_indices[number]': '`find({number})`：取出数字 `{number}` 的堆',
        'while indices and': lambda S, B, r: (
            '堆是空的，没有这个数字' if not S.indices else
            (f'堆顶下标 `{S.indices[0]}`，现在放的是 `{S.self.index_to_number[S.indices[0]]}`，不是 `{S.number}` → ==旧数据，要删=='
             if S.self.index_to_number[S.indices[0]] != S.number else
             f'堆顶下标 `{S.indices[0]}`，现在放的正是 `{S.number}` → 货对板，停止')),
        'heappop(indices)': '堆顶货不对板：弹出，下一个再看（每条旧数据最多弹一次）',
        'return indices[0] if indices else -1': lambda S, B, r: (f'堆里没有 `{S.number}` → 返回 ==-1==' if r == -1 else f'堆顶就是最小下标 → 返回 =={r}=='),
    },
    max_steps=90,
    cards=dict(
        one_liner='换数字时不删旧下标，查询时发现堆顶货不对板再弹出',
        complexity='change `O(log q)`，find 均摊 `O(log q)`；空间 `O(q)`',
        problem=['`change(index, number)`：在下标处填数字，已有则替换',
                 '`find(number)`：返回该数字的最小下标，没有返回 `-1`',
                 '本视频：`find(10)=-1` → 填入 `2,1,3` → `find(10)=1` → `change(1,20)` → `find(10)=2`'],
        quote='numberToIndices 改成哈希表套最小堆。对于 change，不删除旧数据。对于 find，查看堆顶是否等于 number，若不相同，则意味着堆顶是之前没有删除的旧数据，弹出堆顶；否则堆顶就是答案。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`index_to_number` 记录每个下标==现在==的数字；每个数字一个最小堆存下标',
              '`change` 只管往新数字的堆里 push，旧数字的堆里留着过期下标',
              '`find` 检查堆顶：`index_to_number[堆顶] != number` 就是过期数据，弹掉'],
        summary=['change `O(log q)`；find 每条数据最多弹一次，均摊 `O(log q)`',
                 '“懒删除”：把删除推迟到查询时，省掉在堆中间删除元素的麻烦',
                 '方法一：哈希表 + 有序集合 `SortedSet`，真正删掉旧下标，需要第三方库',
                 '易错：堆里的下标可能同时属于多个数字，必须用 `index_to_number` 核对']),
)

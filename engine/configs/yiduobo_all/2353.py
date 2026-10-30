CALL = """fr = FoodRatings(['kimchi', 'miso', 'sushi', 'ramen'], ['korean', 'japanese', 'japanese', 'japanese'], [9, 12, 8, 14])
out = []
out.append(fr.highestRated('japanese'))
fr.changeRating('sushi', 16)
out.append(fr.highestRated('japanese'))
fr.changeRating('sushi', 5)
out.append(fr.highestRated('japanese'))
out"""


def _hp(v):
    return ' '.join(f'{-r}:{f}' for r, f in v)


CONFIG = dict(
    num=2353, title='设计食物评分系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='每菜系一个堆 + 哈希表对账',
    tags=['难度分 1782'],
    code='''
class FoodRatings(object):

    def __init__(self, foods, cuisines, ratings):

        self.f_map = {}
        self.f_reverse_map = {}
        sorted_foods = sorted(foods)
        for index, f in enumerate(sorted_foods):
            self.f_map[f] = index
            self.f_reverse_map[index] = f

        self.c_map = {}
        self.heap_dict = {}
        self.cuisine_dict = {}
        self.rating_dict = {}
        n = len(foods)
        cnt = 0
        for index in range(n):
            f_id = self.f_map[foods[index]]

            if cuisines[index] not in self.c_map:
                self.c_map[cuisines[index]] = cnt
                cnt += 1
            
            c_id = self.c_map[cuisines[index]]

            r = ratings[index]

            if c_id not in self.heap_dict:
                self.heap_dict[c_id] = []
            heapq.heappush(self.heap_dict[c_id], [-r, f_id])
            self.cuisine_dict[f_id] = c_id
            self.rating_dict[f_id] = r

    def changeRating(self, food, newRating):
        f_id = self.f_map[food]
        if self.rating_dict[f_id] == newRating:
            return

        c_id = self.cuisine_dict[f_id]
        heappush(self.heap_dict[c_id], [-newRating, f_id])
        self.rating_dict[f_id] = newRating

    def highestRated(self, cuisine):
        c_id = self.c_map[cuisine]
        while True:
            r, f_id = self.heap_dict[c_id][0]
            r = -r
            if self.rating_dict[f_id] == r:
                return self.f_reverse_map[f_id]
            
            heapq.heappop(self.heap_dict[c_id])
''',
    call=CALL,
    expect=['ramen', 'sushi', 'ramen'],
    views=[
        dict(type='map', var='self.f_map', label='f_map（食物名 → 编号，按字典序编号）',
             fmt=lambda k, v: f'{k} → {v}', h=110, font=26),
        dict(type='map', var='self.rating_dict', label='rating_dict（食物编号 → 当前评分）',
             fmt=lambda k, v: f'{k} → {v}', h=110, font=28),
        dict(type='map', var='self.heap_dict', label='heap_dict（菜系编号 → 堆，格式 评分:食物编号，最左 = 堆顶）',
             fmt=lambda k, v: f'{k} → {_hp(v)}', h=160, font=26),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=['food', 'newRating', 'f_id', 'c_id', ('out', 'out', 'green')],
    max_steps=130,
    skip=['self.f_reverse_map[index] = f', 'cnt += 1', 'n = len(foods)', 'cnt = 0', 'r = ratings[index]',
          'self.cuisine_dict[f_id] = c_id', 'self.cuisine_dict = {}', 'self.heap_dict = {}', 'self.c_map = {}', 'r = -r', 'while True'],
    captions={
        'self.f_reverse_map = {}': '食物名排序后编码成 `0, 1, 2…`：编号小 = 字典序小，堆里比编号就等于比字典序',
        'sorted_foods = sorted': '把食物按字典序排好',
        'self.f_map[f] = index': '`f_map[{f}]` = =={index}==，`f_reverse_map` 反查回名字',
        'self.rating_dict = {}': '`rating_dict`：每个食物（编号）==当前真实==的评分',
        'f_id = self.f_map[foods[index]]': '第 `{index}` 个食物的编号 `{f_id}`',
        'if cuisines[index] not in self.c_map': '这个菜系见过吗？没见过就给它新编号',
        'self.c_map[cuisines[index]] = cnt': '新菜系 `{cuisines[index]}` 编号 `{cnt}`',
        'c_id = self.c_map[cuisines[index]]': '菜系编号 `c_id = {c_id}`',
        'if c_id not in self.heap_dict': '每个菜系要有自己的堆',
        'heapq.heappush(self.heap_dict[c_id], [-r': '`[-评分, 食物编号]` 入堆：评分大排前，同分编号小（字典序小）排前',
        'self.rating_dict[f_id] = r': '记下真实评分：食物 `{f_id}` = `{r}`',
        'f_id = self.f_map[food]': '`{food}` 的编号是 `{f_id}`',
        'if self.rating_dict[f_id] == newRating': lambda S, B, r: (
            f'新评分 `{S.newRating}` 和现在一样，什么也不用做' if S['self.rating_dict'][S.f_id] == S.newRating
            else f'新评分 `{S.newRating}` ≠ 现在的 `{S["self.rating_dict"][S.f_id]}`，需要更新'),
        'c_id = self.cuisine_dict[f_id]': '查出食物 `{f_id}` 属于哪个菜系：`c_id = {c_id}`',
        'heappush(self.heap_dict[c_id], [-newRating': '把 `[{-newRating}, {f_id}]` 加进堆，旧记录留着，等它到堆顶再说',
        'self.rating_dict[f_id] = newRating': '`rating_dict` 里食物 `{f_id}` 的真实评分改成 =={newRating}==',
        'c_id = self.c_map[cuisine]': '找到菜系 `{cuisine}` 的堆：`c_id = {c_id}`',
        'while True': '一直检查堆顶，直到找到有效的',
        'r, f_id = self.heap_dict[c_id][0]': '看堆顶：记录里的评分 `{-r}`，食物编号 `{f_id}`',
        'r = -r': '取负还原评分 `{r}`',
        'if self.rating_dict[f_id] == r': lambda S, B, rr: (
            f'哈希表里食物 `{S.f_id}` 的评分是 `{S["self.rating_dict"][S.f_id]}`，和堆顶 `{S.r}` ==一致== → 它就是答案'
            if S['self.rating_dict'][S.f_id] == S.r
            else f'哈希表里食物 `{S.f_id}` 的评分是 `{S["self.rating_dict"][S.f_id]}`，堆顶是 `{S.r}`：==不一致==，评分已被改过'),
        'return self.f_reverse_map[f_id]': '用编号反查食物名，返回 =={ret}==',
        'heapq.heappop(self.heap_dict[c_id])': '堆顶已过期，弹出，继续看下一个',
        'out.append': '记录结果 `{out}`',
    },
    cards=dict(
        one_liner='每个菜系一个堆，堆顶对不上哈希表就弹掉',
        complexity='`changeRating` `O(log n)`，`highestRated` 均摊 `O(log n)`',
        problem=['`changeRating` 修改食物评分，`highestRated` 返回某菜系评分最高的食物',
                 '评分相同取字典序小的食物名',
                 '示例：日式 `miso 12 / sushi 8 / ramen 14`：最高依次是 `ramen`、`sushi`、`ramen`'],
        quote='找到该烹饪方式对应的堆，并通过哈希表检测当前堆顶食物的评分是否与堆中记录的一致。若不一致，说明这个食物的评分已经被修改过，不能作数，因此需要将该食物从堆顶弹出。',
        quote_src='—— yiduobo 题解原文',
        idea=['`rating_dict` 记每个食物当前得分，`cuisine_dict` 记食物属于哪个菜系',
              '修改评分：更新哈希表，再把新的（食物、评分）对加入对应堆',
              '查询：看堆顶，和哈希表对不上就弹，直到一致'],
        summary=['时间 `O(log n)` 量级，空间 `O(n + q)`',
                 '食物名先按字典序编号，堆里比较编号就等价于比较字典序，免去字符串比较',
                 '易错：堆存 `[-评分, 编号]`；评分没变时直接返回，避免多入一条',
                 '对比灵神：灵神直接把食物名放堆里；这里额外编号并多一个 `cuisine_dict`',
                 '原文已是 Python 3 可运行写法；`heappush` 为引擎预置，等价于 `heapq.heappush`'],
    ),
)

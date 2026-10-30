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
    author='灵茶山艾府', technique='哈希表 + 懒删除堆',
    tags=['难度分 1782'],
    code='''
class FoodRatings:
    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.food_map = {}
        self.cuisine_map = defaultdict(list)
        for food, cuisine, rating in zip(foods, cuisines, ratings):
            self.food_map[food] = [rating, cuisine]
            self.cuisine_map[cuisine].append((-rating, food))
        # 这样可以保证初始化是线性复杂度
        for h in self.cuisine_map.values():
            heapify(h)

    def changeRating(self, food: str, newRating: int) -> None:
        p = self.food_map[food]
        # 直接添加新数据，后面 highestRated 再删除旧的
        heappush(self.cuisine_map[p[1]], (-newRating, food))
        p[0] = newRating

    def highestRated(self, cuisine: str) -> str:
        h = self.cuisine_map[cuisine]
        # 堆顶的食物评分不等于其实际值
        while -h[0][0] != self.food_map[h[0][1]][0]:
            heappop(h)
        return h[0][1]
''',
    call=CALL,
    expect=['ramen', 'sushi', 'ramen'],
    views=[
        dict(type='map', var='self.food_map', label='food_map（食物 → [最新评分, 菜系]）',
             fmt=lambda k, v: f'{k} → {v[0]}', h=150, font=28),
        dict(type='map', var='self.cuisine_map', label='cuisine_map（菜系 → 堆，格式 评分:食物，最左 = 堆顶）',
             fmt=lambda k, v: f'{k} → {_hp(v)}', h=190, font=26),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=['food', 'newRating', 'cuisine', ('out', 'out', 'green')],
    max_steps=110,
    captions={
        'self.food_map = {}': '`food_map`：每个食物==当前真实==的评分和菜系',
        'self.cuisine_map = defaultdict': '`cuisine_map`：每个菜系一个堆，堆里存 `(-评分, 食物名)`',
        'self.food_map[food] = [rating, cuisine]': '记下 `{food}`：评分 `{rating}`，菜系 `{cuisine}`',
        'self.cuisine_map[cuisine].append': '先 `append`，取负评分：评分高的在前，同分时字典序小的在前',
        'for h in self.cuisine_map.values()': lambda S, B, r: '轮到下一个菜系的堆（没有了就结束）',
        'heapify(h)': '建完再统一堆化，初始化 `O(n)`',
        'p = self.food_map[food]': '取出 `{food}` 的记录 `{p}`（列表，可原地改）',
        'heappush(self.cuisine_map[p[1]]': '==懒更新==：新评分 `({-newRating}, {food})` 直接入堆，旧记录先不管',
        'p[0] = newRating': '`food_map` 里 `{food}` 的真实评分改成 =={newRating}==',
        'h = self.cuisine_map[cuisine]': '取出菜系 `{cuisine}` 的堆',
        'while -h[0][0]': lambda S, B, r: (
            f'堆顶 `{-S.h[0][0]}:{S.h[0][1]}`，真实评分是 `{S["self.food_map"][S.h[0][1]][0]}`：==不相等==，是旧数据 → 弹掉'
            if -S.h[0][0] != S['self.food_map'][S.h[0][1]][0]
            else f'堆顶 `{-S.h[0][0]}:{S.h[0][1]}` 与真实评分 `{S["self.food_map"][S.h[0][1]][0]}` 相等 → 有效，停止'),
        'heappop(h)': '弹出过期的堆顶',
        'return h[0][1]': '堆顶有效，最高评分的食物是 =={h[0][1]}==',
        'out.append': '记录结果 `{out}`',
    },
    cards=dict(
        one_liner='改评分只管入堆，过期的等到堆顶再弹',
        complexity='`changeRating` `O(log(n+q))`，`highestRated` 均摊 `O(log(n+q))`',
        problem=['`changeRating` 修改食物评分，`highestRated` 返回某菜系评分最高的食物',
                 '评分相同取字典序小的食物名',
                 '示例：日式 `miso 12 / sushi 8 / ramen 14`：最高依次是 `ramen`、`sushi`、`ramen`'],
        quote='changeRating：直接往 cuisineMap 中记录，不做任何删除操作。highestRated：查看堆顶的食物评分是否等于其实际值，若不相同则意味着对应的元素已被替换成了其他值，堆顶存的是旧数据，直接弹出堆顶。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['每个菜系一个最小堆，存 `(-评分, 食物名)`：评分大、名字小的排前面',
              '`food_map` 永远保存真实评分；堆里可能有同一食物的多个历史版本',
              '查询时对账：堆顶评分和真实评分不等就弹，等了才是答案'],
        summary=['初始化 `O(n)`（`heapify`），改分 `O(log(n+q))`，查询均摊 `O(log(n+q))`',
                 '空间 `O(n+q)`：改分一次多一条堆记录',
                 '易错：入堆要用 `-评分`，同分时比较食物名，字典序小的自然排前',
                 '写法一：`SortedList` 先 `discard` 旧数据再 `add` 新数据，每次 `O(log n)`'],
    ),
)

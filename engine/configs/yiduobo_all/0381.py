CONFIG = dict(
    num=381, title='O(1)时间插入、删除和获取随机元素-允许重复', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='list + dict 存位置集合',
    tags=['随机化'],
    code='''
import random

class RandomizedCollection(object):

    def __init__(self):
        self.pos_dict = {}
        self.num_list = []

    def insert(self, val):
        ret = False
        if val not in self.pos_dict:
            ret = True
            self.pos_dict[val] = set()

        self.pos_dict[val].add(len(self.num_list))
        self.num_list.append(val)
        return ret

    def remove(self, val):
        if val not in self.pos_dict:
            return False

        val_pos = self.pos_dict[val].pop()
        tmp = self.num_list[-1]
        self.num_list[val_pos] = tmp
        self.pos_dict[tmp].add(val_pos)
        self.pos_dict[tmp].remove(len(self.num_list) - 1)
        if not self.pos_dict[val]:
            self.pos_dict.pop(val)
        self.num_list.pop()

        return True

    def getRandom(self):
        return self.num_list[random.randint(0, len(self.num_list) - 1)]
''',
    setup='import random\nrandom.seed(0)',
    call='''c = RandomizedCollection()
res = [c.insert(1), c.insert(1), c.insert(2), c.remove(1), c.getRandom(), c.remove(2), c.remove(2)]
res''',
    expect=[True, False, True, True, 1, True, False],
    views=[
        dict(type='array', var='self.num_list', label='num_list（真正存元素的列表）', cell=96, h=170),
        dict(type='map', var='self.pos_dict', label='pos_dict（值 → 它在 num_list 里的所有下标）',
             fmt=lambda k, v: f'{k} → {sorted(v)}', h=170, font=34),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=['val', 'val_pos', 'tmp', ('ret', 'ret')],
    skip=['import random'],
    captions={
        'self.pos_dict = {}': '`pos_dict`：值 → ==下标集合==（有重复，所以不能只存一个下标）',
        'self.num_list = []': '`num_list`：所有元素按插入顺序放，随机取就是随机取下标',
        11: '`{val}` 出现过吗？没出现过 → 这次插入返回 `True`，出现过 → 只追加下标、返回 `False`',
        20: '`{val}` 在集合里吗？不在就没东西可删，返回 `False`',
        'ret = False': '先假设 `ret = False`（值已存在时就返回它）',
        'ret = True': '第一次出现：返回值记为 `True`',
        'self.pos_dict[val] = set()': '为 `{val}` 建一个空的下标集合',
        'self.pos_dict[val].add(len(self.num_list))': '新元素将放在末尾，下标 = `len(num_list)` = `{len(self.num_list)}`，记进 `{val}` 的集合',
        'self.num_list.append(val)': '把 `{val}` 真正追加到列表末尾',
        'return ret': '返回 `{ret}`',
        'return False': '集合里根本没有 `{val}`，删不了，返回 `False`',
        'val_pos = self.pos_dict[val].pop()': '从 `{val}` 的下标集合里随便弹出一个：要删的位置 `val_pos = {val_pos}`',
        'tmp = self.num_list[-1]': '列表末尾的元素 `tmp = {tmp}`：用它==补==到要删的位置，这样删除是 `O(1)`',
        'self.num_list[val_pos] = tmp': '`num_list[{val_pos}]` 改成 `{tmp}`（覆盖掉要删的值）',
        'self.pos_dict[tmp].add(val_pos)': '`{tmp}` 搬到了下标 `{val_pos}`：把新下标加进它的集合',
        'self.pos_dict[tmp].remove(len(self.num_list) - 1)': '`{tmp}` 原来的末尾下标 `{len(self.num_list) - 1}` 作废，从集合里删掉',
        'if not self.pos_dict[val]': lambda S, B, ret: ('`{}` 的下标集合空了 → 这个值已经一个不剩'.format(S.val) if not S['self.pos_dict'].get(S.val, {1})
                                                        else '`{}` 还有别的下标，保留'.format(S.val)),
        'self.pos_dict.pop(val)': '把空集合对应的键 `{val}` 删掉，否则下次 `insert` 会误判',
        'self.num_list.pop()': '弹掉末尾那份旧的 `{tmp}`，列表长度 -1',
        'return True': '删除成功，返回 `True`',
        'random.randint': '随机选一个下标，直接取值：每个下标等概率，所以重复多的值概率自然更大 → 返回 `{ret}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='dict 不存下标，而存“下标集合”，重复也能 O(1)',
        complexity='`insert` / `remove` / `getRandom` 平均都是 `O(1)`，空间 `O(n)`',
        problem=['设计 `RandomizedCollection`：允许重复元素',
                 '`insert(val)`：插入，值原本不存在返回 `true`',
                 '`remove(val)`：删除一个，存在返回 `true`',
                 '`getRandom()`：按元素个数等概率返回一个'],
        quote='这里有重复元素出现，那么之前使用dict储存元素在list中位置的操作就需要变成dict不直接储存元素在list中的位置，而是储存一个set，通过这个set储存元素在list中的位置。',
        quote_src='—— yiduobo 题解',
        idea=['上一题（380）：dict 存“值 → 下标”；这题值会重复，改成“值 → 下标集合”',
              '删除时用==末尾元素补洞==，保证 `list.pop()` 是 `O(1)`',
              '补洞后记得同步两份下标：新增 `val_pos`，删掉旧的末尾下标'],
        summary=['三个操作平均 `O(1)`，空间 `O(n)`',
                 '易错：删除后要把末尾元素的下标更新；集合空了要把键删掉',
                 '易错：删的值恰好就是末尾元素时，先 add 再 remove 的顺序也成立（集合里同一下标）',
                 '原文有 `:type` 文档字符串，已删去，代码其余照搬',
                 '前置题：380；同类随机题 710、497'],
    ),
)

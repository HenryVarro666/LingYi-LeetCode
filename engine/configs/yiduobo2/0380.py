OPS = '`insert(10)` → `insert(20)` → `insert(30)` → `remove(10)` → `insert(20)` → `getRandom()` → `remove(20)` → `getRandom()`'


def _in_remove(S):
    return 18 <= S.get('_line', 0) <= 25


def _pos_val(S):
    if not _in_remove(S):
        return None
    return S['self.num_dict'].get(S['val'])


def _last(S):
    if not (20 <= S.get('_line', 0) <= 23):
        return None
    return len(S['self.num_list']) - 1


def _col(S, i, v):
    if _in_remove(S) and S.get('tmp') is not None and v == S['tmp'] and S['_line'] >= 22 and i != len(S['self.num_list']) - 1:
        return 'cyan'
    if _in_remove(S) and v == S.get('val') and S['val'] in S['self.num_dict']:
        return 'red'
    return None


def _if10(S, B, ret):
    v = S.val
    if v in S.self.num_dict:
        return f'`insert({v})`：`{v}` 已经在 dict 里 → 重复了'
    return f'`insert({v})`：dict 里没有 `{v}` → 可以插入'


def _if18(S, B, ret):
    v = S.val
    if v not in S.self.num_dict:
        return f'`remove({v})`：dict 里没有 `{v}` → 无法删除'
    return f'`remove({v})`：查 dict 得到它在 list 中的下标 `{S.self.num_dict[v]}`'


def _swap_dict(S, B, ret):
    if S.tmp == S.val:
        return f'`{S.val}` 本身就在末尾：`num_dict[{S.tmp}]` 赋成自己的下标，==相当于不变=='
    return f'末尾的 `{S.tmp}` 要搬到 `{S.val}` 的位置：先改 dict，`num_dict[{S.tmp}] = {S.self.num_dict[S.tmp]}`'


CONFIG = dict(
    num=380, title='常数时间插入、删除和获取随机元素', difficulty='Medium', category='设计',
    author='yiduobo', technique='dict 存下标 + list · 删除时与末尾交换',
    tags=['字节30天', '面试经典150'],
    code='''
import random

class RandomizedSet(object):

    def __init__(self):
        self.num_dict = {}
        self.num_list = []

    def insert(self, val):
        if val in self.num_dict:
            return False

        self.num_dict[val] = len(self.num_list)
        self.num_list.append(val)
        return True

    def remove(self, val):
        if val not in self.num_dict:
            return False
        tmp = self.num_list[-1]
        self.num_dict[tmp] = self.num_dict[val]
        self.num_list[self.num_dict[val]] = tmp
        self.num_dict.pop(val)
        self.num_list.pop()
        return True

    def getRandom(self):
        return self.num_list[random.randint(0, len(self.num_list) - 1)]
''',
    setup='import random\nrandom.seed(2020)',
    call='''rs = RandomizedSet()
[rs.insert(10), rs.insert(20), rs.insert(30), rs.remove(10), rs.insert(20), rs.getRandom(), rs.remove(20), rs.getRandom()]''',
    expect=[True, True, True, True, False, 30, True, 30],
    views=[
        dict(type='text', size=22, h=86, lines=2, fn=lambda S: f'操作：{OPS}'),
        dict(type='array', var='self.num_list', cell=110, h=270, min_slots=4,
             label='num_list（红 = 要删的数，青 = 从末尾搬过来的数）',
             pointers={_pos_val: 'pink', _last: 'cyan'}, pointer_labels={_pos_val: 'val 的下标', _last: '末尾'},
             color=_col),
        dict(type='map', var='self.num_dict', font=30, h=130, label='num_dict：数 → 它在 num_list 里的下标',
             fmt=lambda k, v: f'{k} → {v}'),
        dict(type='text', size=26, fn=lambda S: '不变量：`num_list[num_dict[x]] == x`；删除 = ==和末尾交换再 pop=='),
    ],
    watch=[('val', 'val', 'pink'), ('tmp', 'tmp', 'cyan'), ('size', lambda S: len(S['self.num_list']), 'green')],
    captions={
        'self.num_dict = {}': '`num_dict`：哈希表，==O(1)== 判断存在、找到下标',
        'self.num_list = []': '`num_list`：线性结构，随机取元素要靠它',
        'if val in self.num_dict': _if10,
        11: '重复插入 → 返回 ==False==',
        'self.num_dict[val] = len(self.num_list)': '`{val}` 将放在 list 末尾，下标 `{self.num_dict[val]}` → 先记进 dict',
        'self.num_list.append(val)': '`{val}` 加到 list 末尾',
        15: '插入成功 → 返回 `True`',
        'if val not in self.num_dict': _if18,
        19: '要删的数不存在 → 返回 ==False==',
        'tmp = self.num_list[-1]': '记下 list 末尾的数 `tmp = {tmp}`',
        'self.num_dict[tmp] = self.num_dict[val]': _swap_dict,
        'self.num_list[self.num_dict[val]] = tmp': lambda S, B, r: (
            f'把 `{S.tmp}` 搬进下标 `{S.self.num_dict[S.val]}`，覆盖掉 `{S.val}`' if S.tmp != S.val
            else f'`{S.tmp}` 写回自己的位置（自己覆盖自己），接下来删掉末尾即可'),
        'self.num_dict.pop(val)': 'dict 里删掉 `{val}`',
        'self.num_list.pop()': 'list ==只删末尾== → `O(1)`，不用把后面的元素整体前移',
        25: '删除成功 → 返回 `True`',
        'random.randint': lambda S, B, r: (f'`getRandom()`：list 连续存放，随机下标 `randint(0, {len(S.self.num_list) - 1})` → 返回 =={r}=='),
    },
    cards=dict(
        one_liner='dict 记下标，list 存元素；删除时拿末尾元素来填坑',
        complexity='`insert`/`remove`/`getRandom` 均为 `O(1)`，空间 `O(n)`',
        problem=['实现 `RandomizedSet`：`insert(val)`、`remove(val)` 返回是否成功，`getRandom()` 等概率返回一个元素',
                 '三个操作都要==平均 O(1)==',
                 '本视频：插入 10/20/30，删 10，重复插 20，随机取，删末尾的 20，再随机取'],
        quote='到了这里，自然就想到==使用dict来保存每个数在list中的位置==。……对于删除操作，将待删除的元素与list的末尾进行交换，同时更新原始末尾元素在dict中的值，并截取掉list的末尾。',
        quote_src='—— yiduobo 题解原文',
        idea=['常数时间插入、删除 → 哈希表；随机取 → 需要 list 这种线性结构',
              '`insert`：加到 list 末尾，dict 记下标',
              '`remove`：末尾元素搬到被删元素的位置，再删掉 list 末尾；`getRandom` 随机一个下标'],
        summary=['三个操作都是 `O(1)`，空间 `O(n)`',
                 '易错：删的恰好是末尾（如 `remove(20)`）时，==先改 tmp 下标、再 pop val== 的顺序保证结果正确',
                 '不能直接 `list.remove(val)`：那是 `O(n)`',
                 '原文为 Python 2 写法：只删去了文档字符串和 LeetCode 模板注释；演示中固定了随机种子'],
    ),
)

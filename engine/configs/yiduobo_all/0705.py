def _true_set(S):
    f = S.get('self.f')
    if f is None:
        return None
    return {i for i, x in enumerate(f) if x}


def _info(S):
    f = S.get('self.f')
    if f is None:
        return '数组 `f` 还没创建'
    return f'`f` 共 `{len(f)}` 格，==下标即数字==；只有值为 `True` 的下标才在集合里'


CONFIG = dict(
    num=705, title='设计哈希集合', difficulty='Easy', category='设计',
    author='yiduobo', technique='直接寻址数组（占坑法）',
    code='''
class MyHashSet(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.f = [False] * 1000001

    def add(self, key):
        self.f[key] = True

    def remove(self, key):
        self.f[key] = False

    def contains(self, key):
        """
        Returns true if this set contains the specified element
        :type key: int
        :rtype: bool
        """
        return self.f[key]
''',
    call='''obj = MyHashSet()
r = [obj.add(1), obj.add(2), obj.contains(1), obj.contains(3), obj.add(2), obj.contains(2), obj.remove(2), obj.contains(2)]
r''',
    expect=[None, None, True, False, None, True, None, False],
    views=[
        dict(type='set', var=_true_set, label='集合里的数（= f 中为 True 的下标）', fmt=lambda x: str(x), h=150, font=34),
        dict(type='text', h=90, size=28, fn=_info),
        dict(type='calls', label='正在执行', h=200),
    ],
    watch=['key', ('f[key]', "self.f[key] if 'key' in S else ''", 'green')],
    skip=['"""', 'Initialize your data', 'Returns true if', ':type key', ':rtype'],
    captions={
        'self.f = [False]': '开一个 `1000001` 格的数组，全是 `False`：==下标就是数字==，数字范围 `0 ~ 10^6`',
        'self.f[key] = True': '`add({key})`：把第 `{key}` 格占上 → `f[{key}] = True`',
        'self.f[key] = False': '`remove({key})`：把第 `{key}` 格清空 → `f[{key}] = False`',
        'return self.f[key]': lambda S, B, r: '`contains({})`：直接看第 `{}` 格 → `{}`'.format(S.key, S.key, r) + ('（占着坑，在集合里）' if r else '（没占坑，不在集合里）'),
    },
    cards=dict(
        one_liner='数字范围只有 100 万：用数组下标直接当哈希，一格一个数',
        complexity='`add` / `remove` / `contains` 都是 `O(1)`；空间 `O(C)`，`C = 10^6`',
        problem=['不用内置哈希表，设计 `MyHashSet`',
                 '`add(key)` 加入、`remove(key)` 删除、`contains(key)` 判断是否存在',
                 '`key` 范围 `0 ~ 10^6`'],
        quote='设计哈希表的问题，经典做法有占坑法和链表法。注意到这里需要哈希的数字都在1到1000000之间，所以我选择了偷懒的做法，开一个1000001的数组初始化为false，用数组下标对应具体的数字。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字范围小 → 不用哈希函数，==下标本身就是哈希值==',
              '`add`：把那一格置 `True`；`remove`：置回 `False`',
              '`contains` 直接返回那一格，不会有冲突'],
        summary=['三种操作都是 `O(1)`，空间固定 `O(10^6)`',
                 '数组要开 `1000001` 格，因为 `key` 最大可以取到 `10^6`',
                 '占坑法的代价：范围很大时会浪费内存；通用做法是链表法（拉链）',
                 '原文为 Python 2 风格，无需任何改动即可在 Python 3 运行'],
    ),
)

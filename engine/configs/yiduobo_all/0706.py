def _kv(S):
    f = S.get('self.f')
    if f is None:
        return None
    return {i: x for i, x in enumerate(f) if x != -1}


def _info(S):
    f = S.get('self.f')
    if f is None:
        return '数组 `f` 还没创建'
    return f'`f` 共 `{len(f)}` 格，==下标即 key==，格子里存 value；`-1` 表示没有映射'


CONFIG = dict(
    num=706, title='设计哈希映射', difficulty='Easy', category='设计',
    author='yiduobo', technique='直接寻址数组（初始化为 -1）',
    code='''
class MyHashMap(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.f = [-1] * 1000001

    def put(self, key, value):
        """
        value will always be non-negative.
        :type key: int
        :type value: int
        :rtype: None
        """
        self.f[key] = value

    def get(self, key):
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        :type key: int
        :rtype: int
        """
        return self.f[key]

    def remove(self, key):
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        :type key: int
        :rtype: None
        """
        self.f[key] = -1
''',
    call='''obj = MyHashMap()
r = [obj.put(1, 1), obj.put(2, 2), obj.get(1), obj.get(3), obj.put(2, 1), obj.get(2), obj.remove(2), obj.get(2)]
r''',
    expect=[None, None, 1, -1, None, 1, None, -1],
    views=[
        dict(type='map', var=_kv, label='映射表（= f 中不是 -1 的格子：下标 → 值）', fmt=lambda k, v: f'{k} → {v}', h=150, font=34),
        dict(type='text', h=90, size=28, fn=_info),
        dict(type='calls', label='正在执行', h=200),
    ],
    watch=['key', 'value', ('f[key]', "self.f[key] if 'key' in S else ''", 'green')],
    skip=['"""', 'Initialize your data', 'value will always', ':type key', ':type value', ':rtype',
          'Returns the value', 'Removes the mapping'],
    captions={
        'self.f = [-1]': '开一个 `1000001` 格的数组，全是 `-1`：==下标即 key==，`-1` 表示「没有这个 key」',
        'self.f[key] = value': '`put({key}, {value})`：直接把第 `{key}` 格写成 `{value}`（已有就是覆盖）',
        'return self.f[key]': lambda S, B, r: '`get({})`：直接读第 `{}` 格 → `{}`'.format(S.key, S.key, r) + ('（没有映射）' if r == -1 else ''),
        'self.f[key] = -1': '`remove({key})`：把第 `{key}` 格写回 `-1`，映射就没了',
    },
    cards=dict(
        one_liner='key 范围有限：数组下标当 key，格子里直接存 value，-1 代表没有',
        complexity='`put` / `get` / `remove` 都是 `O(1)`；空间 `O(C)`，`C = 10^6`',
        problem=['不用内置哈希表，设计 `MyHashMap`',
                 '`put(key, value)` 写入或覆盖；`get(key)` 没有映射返回 `-1`；`remove(key)` 删除映射',
                 '`key`、`value` 范围 `0 ~ 10^6`，value 一定非负'],
        quote='与上一题类似，我在这里也是开了一个1000001的数组，用来保存下标到具体数值的映射，初始化为-1。当新来一个数时，将数组对应的元素置为这个数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 705 一样：下标直接当 key，不需要哈希函数',
              '`value` 一定非负，所以能用 `-1` 当「空」的标记',
              '`put` 直接写入；`get` 直接读取；`remove` 写回 `-1`'],
        summary=['三种操作都是 `O(1)`，空间固定 `O(10^6)`',
                 '初始值必须是 `-1`，正好对应「没有映射返回 -1」',
                 '能这样做的前提：value 非负，且 key 范围小',
                 '原文为 Python 2 风格，无需任何改动即可在 Python 3 运行'],
    ),
)

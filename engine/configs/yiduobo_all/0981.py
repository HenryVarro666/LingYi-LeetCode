def _ts(S):
    kt = S.get('self.kt') or {}
    k = S.get('key')
    return kt.get(k, []) if k is not None else []


def _vs(S):
    kv = S.get('self.kv') or {}
    k = S.get('key')
    return kv.get(k, []) if k is not None else []


def _color(S, i, v):
    if 'l' in S and 'r' in S and S['_inner'].get('l') is not None:
        if i < S['l']:
            return 'red'
        if i >= S['r']:
            return 'green'
    return None


def _top(S):
    if 'timestamp' not in S or 'value' in S:
        if 'value' in S:
            return f"`set({S['key']!r}, {S['value']!r}, {S['timestamp']})`：时间戳单调递增，==直接追加到末尾=="
        return '每个 key 存两个平行列表：时间戳列表 `kt[key]` 和值列表 `kv[key]`'
    t = S['timestamp']
    if 'l' in S and S['_inner'].get('l') is not None:
        return f"`get({S['key']!r}, {t})`：二分找第一个 `>= {t}` 的时间戳；红 = `< {t}`，绿 = `>= {t}`"
    return f"`get({S['key']!r}, {t})`：找 `<= {t}` 的最大时间戳对应的值"


def _if_mid(S, B, ret):
    a, t = S['self.kt'][S.key][S.mid], S.timestamp
    if a < t:
        return f'`kt[{S.mid}] = {a} < {t}`：答案在右边 → `l = mid + 1`'
    return f'`kt[{S.mid}] = {a} >= {t}`：`mid` 可能就是第一个 `>= {t}` 的 → `r = mid`'


def _if_eq(S, B, ret):
    a, t = S['self.kt'][S.key][S.l], S.timestamp
    if a == t:
        return f'`kt[{S.l}] = {a} == {t}`：恰好有这个时间戳 → 取它的值'
    return f'`kt[{S.l}] = {a} > {t}`：没有正好的时间戳 → 取==前一个== `l − 1 = {S.l - 1}`'


CONFIG = dict(
    num=981, title='基于时间的键值储存', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='哈希表 + 时间戳列表二分',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class TimeMap(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.kt = {}
        self.kv = {}

    def set(self, key, value, timestamp):
        if key not in self.kt:
            self.kt[key] = []
            self.kv[key] = []
        
        self.kt[key].append(timestamp)
        self.kv[key].append(value)

    def get(self, key, timestamp):
        if key not in self.kt:
            return ""
        
        if timestamp < self.kt[key][0]:
            return ""
        
        if timestamp >= self.kt[key][-1]:
            return self.kv[key][-1]
        
        l = 0
        r = len(self.kt[key])
        while l < r:
            mid = (l + r) >> 1
            if self.kt[key][mid] < timestamp:
                l = mid + 1
            else:
                r = mid
            
        if self.kt[key][l] == timestamp:
            return self.kv[key][l]
        else:
            return self.kv[key][l - 1]
''',
    call='''tm = TimeMap()
ans = [tm.set('foo', 'bar', 1), tm.set('foo', 'bar2', 4), tm.set('foo', 'bar3', 7), tm.set('foo', 'bar4', 9),
       tm.get('foo', 5), tm.get('foo', 7), tm.get('foo', 10), tm.get('foo', 0), tm.get('baz', 3)]
ans''',
    expect=[None, None, None, None, 'bar2', 'bar3', 'bar4', '', ''],
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=_ts, label='kt[key]：时间戳列表（单调递增）', cell=100, color=_color,
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, h=230),
        dict(type='array', var=_vs, label='kv[key]：对应的值', cell=100, h=170),
        dict(type='map', var='self.kt', label='self.kt', fmt=lambda k, v: f'{k!r}: {v}', h=110, font=28),
    ],
    watch=[('key', 'key', 'cyan'), ('timestamp', 'timestamp', 'orange'), ('l', 'l', 'blue'),
           ('mid', 'mid', 'yellow'), ('r', 'r', 'pink')],
    captions={
        'self.kt = {}': '`kt`：key → 时间戳列表',
        'self.kv = {}': '`kv`：key → 值列表，和 `kt` 下标一一对应',
        11: lambda S, B, r: (f'`{S.key!r}` 还没出现过 → 先建列表' if S.key not in S['self.kt'] else f'`{S.key!r}` 已有列表 → 直接追加'),
        19: lambda S, B, r: (f'`{S.key!r}` 从没 set 过' if S.key not in S['self.kt'] else f'`get({S.key!r}, {S.timestamp})`：key 存在'),
        20: 'key 不存在 → 返回 `""`',
        23: '比最早的时间戳还早 → 返回 `""`',
        'self.kt[key] = []': '`{key!r}` 第一次出现：新建两个空列表',
        'self.kt[key].append': '时间戳严格递增 → 追加后列表==仍然有序==：`{self.kt[key]}`',
        'self.kv[key].append': '值同步追加：`{self.kv[key]}`',
        'if timestamp < self.kt[key][0]': lambda S, B, r: (f'`{S.timestamp} < {S["self.kt"][S.key][0]}`：比最早的时间戳还早 → 没有值' if S.timestamp < S['self.kt'][S.key][0] else f'`{S.timestamp} >= {S["self.kt"][S.key][0]}`：不早于最早的时间戳'),
        'if timestamp >= self.kt[key][-1]': lambda S, B, r: (f'`{S.timestamp} >= {S["self.kt"][S.key][-1]}`：不早于最后一次 set → 直接取最后一个值' if S.timestamp >= S['self.kt'][S.key][-1] else f'`{S.timestamp} < {S["self.kt"][S.key][-1]}`：落在中间 → 二分'),
        'return self.kv[key][-1]': '返回 `{ret!r}`',
        'l = 0': '二分区间 `[l, r)`：`l = 0`',
        'r = len(self.kt[key])': '`r = {r}`',
        'while l < r': lambda S, B, r: ('`l < r`，区间非空 → 继续' if S.l < S.r else f'`l = r = {S.l}`：`kt[{S.l}]` 是第一个 `>= {S.timestamp}` 的时间戳'),
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'if self.kt[key][mid] < timestamp': _if_mid,
        'l = mid + 1': '`l` → {l}',
        'r = mid': '`r` → {r}',
        'if self.kt[key][l] == timestamp': _if_eq,
        'return self.kv[key][l]': '返回 `{ret!r}`',
        'return self.kv[key][l - 1]': '返回前一个时间戳的值 `{ret!r}`',
    },
    cards=dict(
        one_liner='时间戳单调递增：每个 key 一个有序列表，查询时二分',
        complexity='`set` 时间 `O(1)`，`get` 时间 `O(log n)`，空间 `O(n)`',
        problem=['实现 `TimeMap`：`set(key, value, timestamp)` 存下某时刻的值',
                 '`get(key, timestamp)` 返回 `timestamp_prev <= timestamp` 中==最大时间戳==对应的值，没有返回 `""`',
                 '保证所有 `set` 的 `timestamp` 严格递增',
                 '本视频：在 1/4/7/9 存 bar~bar4，查询 5、7、10、0 和不存在的 key'],
        quote='注意到时间戳单调递增，那么可以直接使用一个list来储存key对应的时间戳，然后在查询时就可以通过==二分查找==key对应的时间戳列表来迅速找到答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`kt[key]`、`kv[key]` 两个列表下标对应：同一次 `set` 的时间戳和值',
              '先特判：key 不存在 / 比最早还早 → `""`；不早于最后一个 → 最后的值',
              '否则二分出第一个 `>= timestamp` 的位置 `l`：相等取 `l`，否则取 `l − 1`'],
        summary=['`set` 只追加 `O(1)`，`get` 二分 `O(log n)`',
                 '两个特判保证二分时 `l` 落在 `[1, len−1]`，`l − 1` 不会越界',
                 '易错：要的是 ==`<= timestamp` 的最大==，不是 `>=` 的最小',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)

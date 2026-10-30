def _books(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '书堆：第 f 摞 = 看过 f 次的书（每摞最上面 = 最近看的）', 24, T['muted'], bold=True)
    fd = S.get('self.freq_to_dict')
    kv = S.get('self.key_to_value_and_freq') or {}
    if fd is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    if not fd:
        cv.text((x0 + 40, y0 + 80), '还没有书', 26, T['dim'])
        return
    mf = S.get('self.min_freq')
    cur = S.get('key')
    if S.get('_line') in (34, 35) and 'k' in S:
        old_v = (B.get('self.key_to_value_and_freq') or {}).get(S['k'], ['?'])[0]
        cv.rect((x1 - 250, y0 + 60, x1 - 30, y0 + 130), fill=(90, 40, 40), r=10, outline=T['red'], width=3)
        cv.text((x1 - 140, y0 + 95), f"淘汰 {S['k']}:{old_v}", 28, T['text'], anchor='mm', bold=True, mono=True)
    bfd = B.get('self.freq_to_dict') or {}
    freqs = sorted(fd)
    colw = min(200, (x1 - x0 - 60) / max(3, len(freqs)))
    bw, bh = colw * 0.72, 64
    base = y1 - 74
    for c, f in enumerate(freqs):
        X = x0 + 40 + c * colw + colw / 2
        keys = list(fd[f])
        is_min = f == mf
        cv.line([(X - bw / 2 - 12, base), (X + bw / 2 + 12, base)], T['orange'] if is_min else T['border'], 4)
        cv.text((X, base + 8), f'第 {f} 摞', 22, T['orange'] if is_min else T['muted'], anchor='mt', bold=True)
        if is_min:
            cv.text((X, base + 34), 'min_freq', 18, T['orange'], anchor='mt', bold=True, mono=True)
        if not keys:
            cv.text((X, base - 30), '（空）', 20, T['dim'], anchor='mm')
        old = list(bfd.get(f, {}))
        for r, k in enumerate(reversed(keys)):  # 从下往上画：最后一个 key 在最下面
            Y = base - 8 - (r + 1) * (bh + 8)
            new = k not in old
            fill = T['blue'] if k == cur else T['panel2']
            cv.rect((X - bw / 2, Y, X + bw / 2, Y + bh), fill=fill, r=8,
                    outline=T['yellow'] if new else T['border'], width=3 if new else 1)
            v = kv.get(k, ['?'])[0]
            cv.text((X, Y + bh / 2), f'{k}:{v}', 26, T['bg'] if k == cur else T['text'], anchor='mm', bold=True, mono=True)
            if r == 0 and len(keys) > 1:
                cv.text((X + bw / 2 + 6, Y + bh / 2), '最下', 17, T['dim'], anchor='lm')
            if r == len(keys) - 1 and len(keys) > 1:
                cv.text((X + bw / 2 + 6, Y + bh / 2), '最上', 17, T['dim'], anchor='lm')


def _op(S):
    fr = [f for f in S.get('_frames_names', [])]
    return fr


def _cap_get(S, B, ret):
    return f'==get({S.key})==：先用 `get_list` 找书，找到就顺便==往右挪一摞=='


def _cap_put(S, B, ret):
    return f'==put({S.key}, {S.value})==：先用 `get_list` 看看有没有这本书'


def _cap_nolst(S, B, ret):
    if not S.lst:
        return f'没有 `{S.key}` 这本书'
    return f'有这本书：`[value, freq] = {S.lst}`'


def _cap_min(S, B, ret):
    mf = S['self.min_freq']
    if not B['self.freq_to_dict'][mf]:
        return f'抽走后，最左边那摞（第 `{mf}` 摞）==空了== → `min_freq` 要加一'
    return f'最左边那摞（第 `{mf}` 摞）还有书，`min_freq` 不变'


def _cap_full(S, B, ret):
    n, cap = len(S['self.key_to_value_and_freq']), S['self.capacity']
    if n == cap:
        return f'已有 `{n}` 本 == `capacity`：==书太多了==，先腾位置'
    return f'已有 `{n}` 本 < `capacity = {cap}`：还放得下'


CONFIG = dict(
    num=460, title='LFU 缓存', difficulty='Hard', category='设计',
    author='灵茶山艾府', technique='哈希表 + 按频率分摞（OrderedDict）',
    tags=['热题173'],
    code='''
# 为方便读者理解核心逻辑，该写法没有删除空字典，删除空字典的写法见【Python 写法二】
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_value_and_freq = {}  # key -> [value, freq]
        # from collections import OrderedDict
        # OrderedDict = dict + 双向链表
        self.freq_to_dict = defaultdict(OrderedDict)  # freq -> OrderedDict（只保存 key）

    def get_list(self, key: int) -> Optional[List[int]]:
        lst = self.key_to_value_and_freq.get(key, None)
        if not lst:  # 没有这本书
            return None
        freq = lst[1]  # 获取这本书在第几摞
        del self.freq_to_dict[freq][key]  # 把这本书抽出来
        if not self.freq_to_dict[self.min_freq]:  # 最左边那摞书是空的
            self.min_freq += 1
        lst[1] += 1  # 看书次数 +1
        self.freq_to_dict[freq + 1][key] = None
        self.freq_to_dict[freq + 1].move_to_end(key, last=False)  # 放在右边这摞书的最上面
        return lst

    def get(self, key: int) -> int:
        lst = self.get_list(key)
        return lst[0] if lst else -1

    def put(self, key: int, value: int) -> None:
        lst = self.get_list(key)
        if lst:  # 有这本书
            lst[0] = value  # 更新 value
            return
        if len(self.key_to_value_and_freq) == self.capacity:  # 书太多了
            # 移除最左边那摞书的最下面的书
            k, _ = self.freq_to_dict[self.min_freq].popitem()
            del self.key_to_value_and_freq[k]
        self.key_to_value_and_freq[key] = [value, 1]  # 新书
        self.freq_to_dict[1][key] = None
        self.freq_to_dict[1].move_to_end(key, last=False)  # 放在「看过 1 次」的最上面
        self.min_freq = 1
''',
    call='''c = LFUCache(2)
c.put(1, 1)
c.put(2, 2)
c.get(1)
c.put(3, 3)
c.get(3)
c.put(4, 4)
c.get(1)''',
    expect=-1,
    views=[
        dict(type='custom', draw=_books, h=360),
        dict(type='map', var='self.key_to_value_and_freq', label='key_to_value_and_freq（key → [value, freq]）',
             fmt=lambda k, v: f'{k} → [{v[0]}, {v[1]}]', h=100),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=['key', 'value', ('min_freq', 'self.min_freq', 'orange'), ('capacity', 'self.capacity')],
    skip=['lst[1] += 1', 'self.freq_to_dict[freq + 1][key] = None', 'self.freq_to_dict[1][key] = None'],
    captions={
        'self.capacity = capacity': '`LFUCache({capacity})`：最多放 `{capacity}` 本书',
        'self.key_to_value_and_freq = {}': '哈希表：`key → [value, freq]`',
        'self.freq_to_dict = defaultdict': '`freq → OrderedDict`：每个 freq 一摞书，OrderedDict 记住==书的上下顺序==',
        24: _cap_get,
        28: _cap_put,
        'lst = self.key_to_value_and_freq.get': lambda S, B, ret: f'查哈希表：`{S.key}` → `{S.lst}`',
        'if not lst:  # 没有这本书': _cap_nolst,
        'return None': '返回 `None`',
        'freq = lst[1]': '这本书在第 `{freq}` 摞（看过 `{freq}` 次）',
        'del self.freq_to_dict[freq][key]': '从第 `{freq}` 摞==抽出== `{key}`',
        'if not self.freq_to_dict[self.min_freq]': _cap_min,
        'self.min_freq += 1': '`min_freq` → {self.min_freq}',
        'move_to_end(key, last=False)  # 放在右边': '看书次数 +1，放到==右边第 `{freq + 1}` 摞的最上面==（`move_to_end(last=False)` = 移到开头）',
        21: '返回这本书的 `[value, freq]`',
        'return lst[0] if lst else -1': lambda S, B, ret: f'`get` 返回 `{ret}`' + ('（没有这本书）' if ret == -1 else ''),
        'if lst:  # 有这本书': lambda S, B, ret: ('有这本书 → 只更新 value（`get_list` 已经挪过摞了）' if S.lst else '没有这本书 → 要放一本新书'),
        'lst[0] = value': '更新 value = {value}',
        'if len(self.key_to_value_and_freq) == self.capacity': _cap_full,
        'k, _ = self.freq_to_dict[self.min_freq].popitem()': lambda S, B, ret: (
            f'`popitem()` 弹出==最左边那摞（第 {S["self.min_freq"]} 摞）最下面==的书 `{S.k}`：看得最少里最久没看的'),
        'del self.key_to_value_and_freq[k]': '哈希表里也删掉 `{k}`',
        'self.key_to_value_and_freq[key] = [value, 1]': '新书 `{key}:{value}`，看过 1 次',
        'self.freq_to_dict[1].move_to_end': '放在第 1 摞（看过 1 次）的==最上面==',
        'self.min_freq = 1': '新书只看过 1 次 → `min_freq = 1`',
    },
    max_steps=75,
    cards=dict(
        one_liner='按看书次数分成若干摞书，淘汰最左边那摞最下面的书',
        complexity='`get` / `put` 均 `O(1)`；空间 `O(min(p, capacity))`',
        problem=['实现 `LFUCache(capacity)`、`get(key)`、`put(key, value)`，都要 `O(1)`',
                 '满了再放新书：淘汰==使用次数最少==的；次数相同淘汰==最久未使用==的',
                 '`get` / `put` 已有的 key 都会让它的使用次数 +1'],
        quote='问：为什么 minFreq 一定对应着最左边的非空的那摞书？答：在添加一本新书的情况下，这本新书一定是放在 freq=1 的那摞书上，此时我们把 minFreq 置为 1。',
        quote_src='—— 灵茶山艾府题解「答疑」（推荐先看写法二）',
        idea=['`freq_to_dict[f]`：第 `f` 摞书，OrderedDict 开头 = 最上面（最近看的）',
              '看一次书：从第 `f` 摞抽出，放到第 `f+1` 摞最上面；最左边空了就 `min_freq += 1`',
              '淘汰：第 `min_freq` 摞的最下面 = `popitem()`（弹出末尾）'],
        result='`get(1)` 返回 `-1`：1 和 3 都看过 2 次，1 更久没看 → 放 4 时被淘汰',
        summary=['`get` / `put` 均 `O(1)`：哈希表定位 + OrderedDict 的 `O(1)` 删除、移到开头、弹出末尾',
                 '易错：只有“抽出后最左边那摞空了”才 `min_freq += 1`；放新书时 `min_freq = 1`',
                 '易错：`put` 已有的 key 也算使用一次，所以 `put` 也要先 `get_list`',
                 '写法一：手写双向链表 + 每摞一个哨兵，思路完全相同'],
    ),
)

def _pts(s):
    return ' '.join(f'({a},{b},{c})' for a, b, c in sorted(s))


_ST = {'fresh': True}


def _fresh(S, B, r):
    _ST['fresh'] = True
    return '`nxt` 先拷贝 `cur`：==旧点也保留==（第 k 代可用 0..k-1 代全部的点）'


def _pair(S, B, r):
    if not _ST['fresh'] and all(S.get(k) == B.get(k) for k in 'xyzabc'):
        return '这一代的点对都枚举完了'
    _ST['fresh'] = False
    return f'取一对不同的点 `({S.x},{S.y},{S.z})` 和 `({S.a},{S.b},{S.c})`'


CONFIG = dict(
    num=3923, title='得到目标点的最少代数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 逐代枚举点对',
    tags=[],
    code='''
class Solution:
    def minGenerations(self, points: List[List[int]], target: List[int]) -> int:
        tar = tuple(target)
        cur = set(map(tuple, points))
        for ans in count(0):
            if tar in cur:
                return ans
            nxt = cur.copy()
            for (x, y, z), (a, b, c) in combinations(cur, 2):  # 枚举 cur 中的所有点对
                nxt.add(((x + a) // 2, (y + b) // 2, (z + c) // 2))
            if len(nxt) == len(cur):  # 没有产生新的点
                return -1
            cur = nxt
''',
    setup='from itertools import count',
    call='Solution().minGenerations([[0,0,0],[5,5,5]], [1,1,1])',
    expect=2,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"目标 `tar = {S['tar']}`　第 `{S['ans']}` 代开始前，`cur` 里有 =={len(S['cur'])}== 个点" if 'ans' in S and 'cur' in S else '')),
        dict(type='set', var='cur', label='cur（已有的点）', fmt=lambda p: f'{p[0]},{p[1]},{p[2]}', h=200),
        dict(type='set', var='nxt', label='nxt（下一代 = cur + 新生成的中点）', fmt=lambda p: f'{p[0]},{p[1]},{p[2]}', h=200),
        dict(type='text', size=26, fn=lambda S: (f"这一对 `({S['x']},{S['y']},{S['z']})` 和 `({S['a']},{S['b']},{S['c']})` → 中点 `(({S['x']}+{S['a']})//2, ({S['y']}+{S['b']})//2, ({S['z']}+{S['c']})//2)`" if 'x' in S and 'a' in S else '')),
    ],
    watch=[('ans', 'ans', 'green'), ('len(cur)', 'len(cur) if "cur" in dir() else 0', 'blue'), ('len(nxt)', 'len(nxt) if "nxt" in dir() else 0', 'pink')],
    captions={
        'tar = tuple': '目标转成元组 `tar = {tar}`，才能放进集合里查',
        'cur = set': '`cur` = 第 0 代的所有点，用集合存：查找 O(1)、自动去重',
        'for ans in count': '开始第 `{ans}` 轮：`ans` 就是已经过了几代',
        'if tar in cur': lambda S, B, r: (f'`tar = {S.tar}` 已经在 `cur` 里 → ==找到了=='
                                          if S.tar in S.cur else f'`tar = {S.tar}` 还不在 `cur` 里（{len(S.cur)} 个点），继续生成下一代'),
        'return ans': '第 `{ans}` 代时 `tar` 出现 → 最少代数 =={ret}==',
        'nxt = cur.copy': _fresh,
        'combinations(cur, 2)': _pair,
        'nxt.add': '中点 = 各维 `(x + a) // 2` 向下取整 → `({(x+a)//2},{(y+b)//2},{(z+c)//2})`，加进 `nxt`（已有就不变）',
        'if len(nxt) == len(cur)': lambda S, B, r: (f'`len(nxt) = {len(S.nxt)} == len(cur) = {len(S.cur)}` → ==没产生新点==，再循环也不会有'
                                                    if len(S.nxt) == len(S.cur) else f'`len(nxt) = {len(S.nxt)} > len(cur) = {len(S.cur)}` → 产生了新点，继续'),
        'return -1': '集合不再增长，`tar` 永远出现不了 → 返回 `-1`',
        'cur = nxt': '进入下一代：`cur` 现在有 `{len(cur)}` 个点',
    },
    cards=dict(
        one_liner='一代一代把所有点对的中点加进集合，直到出现目标或不再增长',
        complexity='时间 `O(U^9)`（`U = 7`），空间 `O(U^3)`',
        problem=['三维整数点，每一代把已有点两两（不同点）取中点（各维向下取整）加入',
                 '求目标点最早在第几代出现；一开始就有返回 `0`，永远出现不了返回 `-1`',
                 '示例：`[[0,0,0],[5,5,5]]`，目标 `[1,1,1]` → `2`'],
        quote='把所有点保存到一个哈希集合中，每次循环，枚举集合中的所有点对，生成新的点。如果没有生成新的点，那么继续循环也不会生成新的点，返回 -1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['坐标范围 `0..6`，所有点最多 `7^3 = 343` 个 → 直接模拟',
              '`nxt = cur.copy()`：新一代包含旧点，再加上所有点对的中点',
              '集合大小没变 = 没有新点 = 后面也不会有 → 返回 `-1`'],
        summary=['每轮至少多一个点，最多 `343` 轮，每轮枚举 `O(343^2)` 对 → `O(U^9)`',
                 '易错：目标要转成 `tuple` 才能在集合里查；`list` 不可哈希',
                 '易错：中点是向下取整的整数除法 `//`，不是 `/`',
                 '原文用到 `count`（itertools）：视频环境在 setup 里 `from itertools import count`，代码一字未改'],
    ),
)

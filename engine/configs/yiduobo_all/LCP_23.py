TARGET = [2, 4, 3, 1, 5]


def _tw(S):
    """target 里已经验证过的前缀数量"""
    if 'p' in S:
        return S['p']
    if 'k' in S:
        return S['k']
    return 0


def _tcolor(S, i, v):
    return 'green' if i < _tw(S) else None


def _fcolor(S, i, v):
    k = S.get('k')
    if k is None:
        return None
    return 'green' if i < k else None


CONFIG = dict(
    num='LCP 23', title='魔术排列', difficulty='Medium', category='模拟',
    author='yiduobo', technique='先定 k，再逐轮模拟洗牌',
    tags=[],
    code='''
class Solution(object):
    def isMagic(self, target):

        n = len(target)
        first = []
        for index in range(1, n + 1):
            if index % 2 == 0:
                first.append(index)
        for index in range(1, n + 1):
            if index % 2 == 1:
                first.append(index)
        
        k = 0
        while k < n and first[k] == target[k]:
            k += 1
        
        if k == n:
            return True
        
        if k == 0:
            return False
        
        p = k
        now = first[k:]
        while True:
            next = []
            for index in range(len(now)):
                if index % 2 == 1:
                    next.append(now[index])
            for index in range(len(now)):
                if index % 2 == 0:
                    next.append(now[index])

            if len(next) > k:
                for index in range(k):
                    if target[p + index] != next[index]:
                        return False
                now = next[k:]
                p += k
            else:
                for index in range(len(next)):
                    if target[p + index] != next[index]:
                        return False
                break
        
        return True
''',
    call=f'Solution().isMagic({TARGET})',
    expect=True,
    skip=['n = len(target)', 'first = []', 'for index in range', 'if index % 2', 'first.append', 'next.append',
          'next = []'],
    views=[
        dict(type='array', var='target', label='target（绿 = 已经对上的前缀；蓝箭头 = 这一轮要对的起点 p）', cell=96, h=190,
             pointers={'p': 'blue'}, color=_tcolor),
        dict(type='array', var='first', label='first：第一轮洗牌后的牌堆（绿 = 前 k 张，被取走）', cell=96, h=170,
             color=_fcolor),
        dict(type='array', var='now', label='now：当前牌堆', cell=96, h=160),
        dict(type='array', var=lambda S: S.get('next') if isinstance(S.get('next'), list) else None, label='next：洗牌之后的牌堆（取走前 k 张）', cell=96, h=160),
    ],
    watch=[('k', 'k', 'pink'), ('p', 'p', 'blue'), ('n', 'n')],
    captions={
        'k = 0': '第一轮洗牌已经做完：偶数位置的牌在前，奇数位置的在后 → `first = {first}`。`k` 从 0 开始数它和 target 的公共前缀',
        'k += 1': '`first[{k-1}] = target[{k-1}] = {target[k-1]}`，对上了：`k` → {k}',
        'while k < n and first[k] == target[k]': lambda S, B, r: (
            f'`first[{S.k}] = {S.first[S.k]}` ≠ `target[{S.k}] = {S.target[S.k]}` → 前缀到此为止，==唯一合法的 k 就是 {S.k}=='
            if S.k < S.n and S.first[S.k] != S.target[S.k] else
            f'`k = {S.k}`，整个 first 都对上了' if S.k >= S.n else
            f'`first[{S.k}] = {S.first[S.k]}` == `target[{S.k}]`，继续往后数前缀'),
        'if k == n': lambda S, B, r: ('第一轮洗牌后全部取走，正好等于 target → 返回 True' if S.k == S.n
                                      else '前缀没有覆盖 target，还要继续洗牌'),
        'if k == 0': lambda S, B, r: ('第一张就不匹配，取不出任何一张 → 返回 False' if S.k == 0
                                      else f'`k = {S.k} > 0`：k 已经确定，后面只需验证'),
        'return True': '全部验证通过 → `True`',
        'p = k': '`p` 记录 target 已经匹配到哪：前 `{k}` 张是第一轮取走的',
        'now = first[k:]': '取走前 `k = {k}` 张，剩下的牌继续洗：`now = {now}`',
        'while True': '再洗一轮：当前牌堆里第 2、4… 张放前面，第 1、3… 张放后面',
        'if len(next) > k': lambda S, B, r: (
            f'洗完有 `{len(S.next)}` 张 `> k = {S.k}` → 还能取满 k 张，逐张核对 `target[p..]`' if len(S.next) > S.k
            else f'洗完只剩 `{len(S.next)}` 张 `≤ k = {S.k}` → 这是最后一轮，全部取走核对'),
        'if target[p + index] != next[index]': lambda S, B, r: (
            f'`target[{S.p + S.index}] = {S.target[S.p + S.index]}` vs `next[{S.index}] = {S.next[S.index]}` → ==不等，返回 False=='
            if S.target[S.p + S.index] != S.next[S.index] else
            f'`target[{S.p + S.index}] = {S.target[S.p + S.index]}` == `next[{S.index}] = {S.next[S.index]}` → 匹配'),
        'now = next[k:]': '取走 `next` 的前 `{k}` 张，剩下 `{now}` 下一轮继续洗',
        'p += k': '`target` 又匹配了 `k` 张：`p` → {p}',
        'break': '最后一轮也匹配，跳出循环',
    },
    cards=dict(
        one_liner='k 在第一轮洗牌后就唯一确定，之后只管模拟',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['牌堆是 `1..n`，每轮先洗牌（偶数位置的牌放到前面，奇数位置的放到后面）',
                 '然后取走前 `k` 张；重复直到取完，取走的顺序要恰好等于 `target`',
                 '判断是否存在这样的 `k`',
                 '示例：`target=[2,4,3,1,5]` → `True`（`k = 2`）'],
        quote='在每次取走前k张牌之后，第k + 1张牌在下一轮必然会被洗到牌堆的后半部分去……题目中唯一合法的k在第一轮洗牌之后就已经确定下来了。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一轮洗牌的结果 `first` 是固定的，前缀能和 `target` 对上多长，`k` 就是多长',
              '`k` 小了或大了，第二轮都对不上 → 不用枚举 `k`',
              '定下 `k` 之后，每轮洗牌、取走前 `k` 张，和 `target` 对应段比较'],
        summary=['时间 `O(n²)`：最多洗 `n` 轮，每轮 `O(n)`',
                 '易错：`k == 0` 取不出牌，返回 False；`k == n` 一轮取完，返回 True',
                 '最后一轮牌数 `≤ k`，要全部取走，不能再按 k 张比较',
                 '原文为 Python 2 风格，代码在 Python 3 下可直接运行，未做修改'],
    ),
)

def _sel(S, i, v):
    now = S.get('self.now')
    if now is None:
        return None
    p = S['_inner'].get('p')
    if p is not None and p < len(now) and i == now[p]:
        return 'yellow'
    return 'green' if i in now else None


CONFIG = dict(
    num=1286, title='字母组合迭代器', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='设计 · 下标组合就地进位',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class CombinationIterator(object):

    def __init__(self, characters, combinationLength):
        self.char_list = characters[:]
        self.n = len(self.char_list)
        self.k = combinationLength
        self.now = None

    def next(self):
        if self.now is None:
            self.now = list(range(self.k))
            self.used = [True] * self.k + [False] * (self.n - self.k)
        else:
            self.rest_max = -1
            for index in range(self.n - 1, -1, -1):
                if not self.used[index]:
                    self.rest_max = index
                    break

            for index in range(self.k - 1, -1, -1):
                if self.now[index] < self.rest_max:
                    p = index
                    break
                self.used[self.now[index]] = False

            self.used[self.now[p]] = False
            self.now[p] += 1
            while self.used[self.now[p]]:
                self.now[p] += 1
            self.used[self.now[p]] = True
            tmp = self.now[p] + 1
            p += 1
            while p < self.k:
                while tmp < self.n and self.used[tmp]:
                    tmp += 1

                self.now[p] = tmp
                p += 1
                self.used[tmp] = True
                tmp += 1

        return ''.join([self.char_list[x] for x in self.now])

    def hasNext(self):
        return self.now != list(range(self.n - self.k, self.n))
''',
    call='''it = CombinationIterator("abcd", 3)
[it.next(), it.hasNext(), it.next(), it.next(), it.hasNext(), it.next(), it.hasNext()]''',
    expect=['abc', True, 'abd', 'acd', True, 'bcd', False],
    views=[
        dict(type='text', fn=lambda S: (f"当前组合 = `{''.join(S['self.char_list'][x] for x in S['self.now'])}`（下标 `{S['self.now']}`）" if S.get('self.now') else '还没有调用 `next`'), size=26, h=70),
        dict(type='array', var='self.char_list', label='characters（绿 = 当前组合选中的字母，黄 = 这次要进位的位置）', cell=80, h=190, color=_sel),
        dict(type='array', var='self.used', label='used（True = 已被当前组合占用）', cell=80, h=170),
        dict(type='array', var='self.now', label='now（组合里每个字母的下标）', cell=80, h=170, pointers={'p': 'pink'}),
    ],
    watch=[('k', 'self.k'), ('rest_max', lambda S: S.get('self.rest_max'), 'cyan'), ('p', lambda S: S['_inner'].get('p'), 'pink'),
           ('tmp', lambda S: S['_inner'].get('tmp'), 'yellow')],
    skip=['self.char_list = characters', 'self.n = len', 'self.k = combinationLength', 'self.now = None', 'tmp = self.now[p] + 1', 'for index in range', 'break', 'p += 1', 'tmp += 1', 'self.used[tmp] = True'],
    captions={
        'if self.now is None': lambda S, B, ret: ('第一次调用：还没有组合' if B.get('self.now') is None else '不是第一次：要从上一个组合算出下一个'),
        'self.now = list(range(self.k))': '第一个组合 = ==字典序最小的 k 个字母==，下标 `{self.now}`',
        'self.used = [True]': '`used` 标记哪些字母已被选中',
        'self.rest_max = -1': '找出==没被选中的最大下标== `rest_max`，作为能否进位的界限',
        'self.rest_max = index': '最右边的未选字母下标是 `{index}` → `rest_max = {index}`',
        'if not self.used[index]': '从右往左找第一个没被选的字母：下标 `{index}` 的 `used` 是 `{self.used[index]}`',
        'if self.now[index] < self.rest_max': lambda S, B, ret: (
            f'`now[{S.index}] = {S.self.now[S.index]} < rest_max = {S.rest_max}`：它还能往右换成更大的字母 → ==就是这一位=='
            if S.self.now[S.index] < S.rest_max else
            f'`now[{S.index}] = {S.self.now[S.index]}` 已经没有更大的可换，退回去换更高位'),
        'p = index': '要进位的位置 `p = {p}`：低位优先替换',
        'self.used[self.now[index]] = False': '这一位放弃它的字母，`used` 释放，留给后面重排',
        'self.used[self.now[p]] = False': '先把第 `p` 位当前的字母放回未使用',
        'self.now[p] += 1': '`now[{p}]` 换成更大的下标 `{self.now[p]}`',
        'while self.used[self.now[p]]': lambda S, B, ret: ('这个下标已被前面的位占用，继续往后找' if S.self.used[S.self.now[S.p]]
                                                           else '没被占用，可以用'),
        'self.used[self.now[p]] = True': '第 `p` 位定为 `{self.now[p]}`，标记占用',
        'while p < self.k': lambda S, B, ret: (f'后面还有位置要填：用剩下的字母==从小到大==排布' if S.p < S.self.k else '所有位置都填好了'),
        'while tmp < self.n and self.used[tmp]': '跳过被占用的下标 `tmp = {tmp}`',
        'self.now[p] = tmp': '第 `{p}` 位 = 最小的未用下标 `{tmp}`',
        'return \'\'.join': '本次组合：`{ret}`',
        'return self.now !=': lambda S, B, ret: ('还没到最大的 k 个字母 → 还有下一个，`True`' if ret else '已经是字典序最大的 k 个字母 → `False`'),
    },
    max_steps=75,
    cards=dict(
        one_liner='用下标数组表示组合，从后往前找能变大的那一位，其后重新从小到大排',
        complexity='`next` 时间 `O(n + k)`，`hasNext` `O(k)`，空间 `O(n)`',
        problem=['`CombinationIterator(characters, k)`：按字典序依次给出长度为 `k` 的组合',
                 '`next()` 返回下一个组合，`hasNext()` 判断是否还有',
                 '本视频：`"abcd"`、`k = 3` → `abc, abd, acd, bcd`'],
        quote='我们应当从后向前进行扫描，对于当前字符char，若未使用的字符中存在某个字符的字典序大于char，那么说明我们可以通用将char替换掉来得到答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一个组合是最小的 k 个字母，最后一个是最大的 k 个字母，`hasNext` 只要比较当前是否等于最后一个',
              '求下一个：优先替换低位。从后往前找第一个能换成更大未用字母的位置 `p`',
              '`p` 换成大于它的最小未用字母，`p` 之后用剩下的字母从小到大排'],
        summary=['`next` 每次 `O(n + k)`，`hasNext` `O(k)`，空间 `O(n)`',
                 '`used` 数组负责记录哪些字母被占用，退位时要及时释放',
                 '`rest_max` 是未选中的最大下标：当前位小于它才有更大的字母可换',
                 '原文为 Python 2 写法，`range(...)` 返回列表，已改为 `list(range(...))`（两处）',
                 '同类题：31. 下一个排列、77. 组合'],
    ),
)

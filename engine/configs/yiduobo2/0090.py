NUMS = [2, 1, 2]


# 只用于动画：让代码里的 list(...) 生成能记录 for 循环位置 k 的 TList（切片后仍是 TList）
TRACK = '''
_BL = list

class KList(_BL):
    pass

class TList(_BL):
    def __getitem__(self, i):
        r = _BL.__getitem__(self, i)
        return TList(r) if isinstance(i, slice) else r

    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield _BL.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(_BL.copy(self))
        c.k = getattr(self, 'k', None)
        return c

list = TList
'''


def _cap_for(S, B, ret):
    k = getattr(S.candidate, 'k', None)
    if isinstance(k, int):
        return f'枚举候选 `{list(S.candidate)}`：试 `num = {S.num}`'
    return f'候选 `{list(S.candidate)}` 都试完了 → 返回上一层'


def _k(S):
    return getattr(S.get('candidate'), 'k', None)


def _cap_if(S, B, ret):
    k = S.count_dict[S.num]
    if k > 0:
        return f'`count_dict[{S.num}] = {k} > 0`：`{S.num}` 还有剩 → 可以用'
    return f'`count_dict[{S.num}] = 0`：`{S.num}` ==用光了== → 跳过'


CONFIG = dict(
    num=90, title='子集 II', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯 · 计数字典 + 候选只往后取',
    tags=['字节30天'],
    code='''
class Solution(object):
    def subsetsWithDup(self, nums):
        res = []
        count_dict = {}
        for num in nums:
            count_dict[num] = count_dict.get(num, 0) + 1

        self.dfs(list(count_dict.keys()), count_dict, [], res)
        return res

    def dfs(self, candidate, count_dict, now, res):
        res.append(now[:])

        for index, num in enumerate(candidate):
            if count_dict[num] > 0:
                count_dict[num] -= 1
                now.append(num)
                self.dfs(candidate[index:], count_dict, now, res)
                now.pop()
                count_dict[num] += 1
''',
    setup=TRACK,
    call=f'Solution().subsetsWithDup({NUMS})',
    expect=[[], [2], [2, 2], [2, 2, 1], [2, 1], [1]],
    views=[
        dict(type='map', var='count_dict', label='count_dict（每个数还剩几个可用）', h=110, font=28,
             fmt=lambda k, v: f'{k}: 剩 {v}'),
        dict(type='array', var='candidate', label='candidate（这一层能选的数）', cell=90, h=200,
             pointers={_k: 'pink'}, pointer_labels={_k: 'index'}, color=lambda S, i, v: 'pink' if i == _k(S) else None),
        dict(type='stack', var='now', label='now（当前子集）', h=100),
        dict(type='calls', h=150, hide=('count_dict', 'res')),
        dict(type='stack', var='res', label='res', h=100, fmt=lambda p: str(p).replace(' ', '')),
    ],
    watch=[('num', 'num', 'pink'), ('now', 'now', 'yellow'), ('len(res)', 'len(res)', 'green')],
    skip=['res = []', 'count_dict = {}', 'for num in nums', 'now.append(num)'],
    captions={
        'for num in nums': lambda S, B, ret: (f'统计 `{S.num}` 出现的次数' if S.get('num') != B.get('num') or 'num' not in B
                                              else '统计完毕：==重复的数合并成「值 + 次数」=='),
        'count_dict[num] = count_dict.get': lambda S, B, ret: (f'统计次数：`count_dict[{S.num}] = {S.count_dict[S.num]}`'
                                                               + ('，==重复的数合并成「值 + 次数」==' if S.count_dict[S.num] > 1 else '')),
        'self.dfs(list(': '候选是去重后的 `{candidate}`，从空集开始搜索（==原文 `count_dict.keys()` 在 Python 3 不能切片，加了 `list()`==）',
        'res.append(now[:])': lambda S, B, ret: (f'==每个 now 都是一个答案==：复制 `{S.res[-1]}` 加入 res' if len(S.res) <= 2
                                                 else f'新子集 `{S.res[-1]}` 加入 res'),
        'for index, num in enumerate': _cap_for,
        'if count_dict[num] > 0': _cap_if,
        'count_dict[num] -= 1': '用掉一个 `{num}` 放进 now，还剩 {count_dict[num]} 个',
        'now.append(num)': '`now` → `{now}`',
        'self.dfs(candidate[index:]': lambda S, B, ret: (
            f'`now = {S.now}`；递归：候选变成 `candidate[{S.index}:]`，==只能选 {S.num} 及后面的数==，保证不重复'
            if len(S.res) <= 2 else f'`now = {S.now}`，递归：候选 `candidate[{S.index}:]`'),
        'now.pop()': '回溯：弹出 `{B.now[-1]}` → `{now}`',
        'count_dict[num] += 1': '把 `{num}` 还回去，又剩 {count_dict[num]} 个',
        'return res': '搜索结束，共 `{len(ret)}` 个子集，==没有重复==',
    },
    max_steps=70,
    cards=dict(
        one_liner='把重复的数合并成「值 + 次数」，每层只从当前候选往后挑，一个值最多用它出现的次数',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['整数数组 `nums` ==可能包含重复元素==，返回所有可能的子集（幂集）',
                 '解集==不能包含重复的子集==',
                 '示例：`[1,2,2]` → `[[],[1],[1,2],[1,2,2],[2],[2,2]]`',
                 f'本视频：`{NUMS}`（==不需要排序==）'],
        quote='还是类似的处理方法，==记录下上一轮操作的位置，然后这一轮从这个位置开始继续往后做==。由于nums中的数可以重复，因此还需要==用一个dict来记录当前情况下每个数使用了几次==。',
        quote_src='—— yiduobo 题解（78 题的升级版）',
        idea=['`count_dict`：每个不同的值还剩几个可用',
              '每进一层 dfs，当前 `now` 就是一个子集',
              '下一层的候选是 `candidate[index:]`：可以再选同一个值，但==不会回头==选前面的值',
              '同一个值选几次只看计数，`[2,1]` 和 `[1,2]` 不会都出现'],
        result='6 个子集，无重复 ✓',
        summary=['时间 `O(n·2^n)`，空间 `O(n)`',
                 '原文为 Python 2：`dict.keys()` 返回列表可切片，Python 3 返回视图，已改为 `list(count_dict.keys())`；并删去文档字符串',
                 '易错：回溯时 `now.pop()` 和 `count_dict[num] += 1` 要成对恢复',
                 '对比灵神：灵神先排序，「不选」时跳过所有相同的数；这里用计数，不用排序'],
    ),
)

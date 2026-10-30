NUMS, K = [3, 2, 3, 3, 1, 4, 1], 7


def _color(S, i, v):
    if 'index' not in S:
        return None
    if S['index'] <= i < S['p']:
        return 'green' if S['_line'] in (18, 19) else 'blue'
    return None


def _right(S):
    return S['p'] - 1 if 'p' in S else None


def _top(S):
    if 'index' not in S:
        return f'`k = {K}`：窗口是左闭右开 `[index, p)`，p 一直往右推'
    l, p = S['index'], S['p']
    keys = sorted(set(NUMS[l:p]))
    expr = ' + '.join(map(str, keys)) if keys else '0'
    return f"起点 `{l}`，窗口 `[{l}, {p})` 不同元素：`{expr} = {S['s']}`" + (f' ≥ {K}' if S['s'] >= K else f' < {K}')


def _inner(S, B, ret):
    if S.p < len(S.nums) and S.s < S.k:
        return f'`s = {S.s} < {S.k}`：不同元素和还不够 → 右边界 `p` 继续右移'
    if S.s >= S.k:
        return f'`s = {S.s} ≥ {S.k}`：起点 {S.index} 的==最小右边界==找到了'
    return '`p` 已到末尾，不能再扩'


CONFIG = dict(
    num=3795, title='不同元素和至少为 K 的最短子数组长度', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · 枚举左端点',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def minLength(self, nums, k):

        s = 0
        p = 0
        cnt = {}
        res = -1
        for index in range(len(nums)):
            while p < len(nums) and s < k:
                cnt[nums[p]] = cnt.get(nums[p], 0) + 1
                if cnt[nums[p]] == 1:
                    s += nums[p]
                p += 1

            if s < k:
                break

            if res == -1 or res > p - index:
                res = p - index

            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                s -= nums[index]

        return res
''',
    call=f'Solution().minLength({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（框 = 窗口 [index, p−1]，绿 = 用来更新答案）',
             pointers={'index': 'cyan', 'p': 'orange'}, window=('index', _right), color=_color, cell=110, h=300),
        dict(type='map', var='cnt', label='cnt（窗口内每种元素出现的次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
    ],
    watch=[('index', 'index', 'cyan'), ('p', 'p', 'orange'), ('s', 's', 'blue'), ('res', 'res', 'green')],
    captions={
        's = 0': '`s`：窗口中==不同==元素之和',
        'p = 0': '`p`：窗口右边界（不含），一开始窗口为空',
        'cnt = {}': '`cnt` 记录窗口中每种元素的出现次数',
        'res = -1': '`res = -1` 表示还没找到',
        'for index in range': lambda S, B, r: ('左边界枚举完毕' if 'index' in B and B.index == S.index
                                               else f'枚举左边界 `index = {S.index}`'),
        'while p < len(nums) and s < k': _inner,
        'cnt[nums[p]] = cnt.get': '`nums[{p}] = {nums[p]}` 进入窗口：`cnt[{nums[p]}]` → {cnt[nums[p]]}',
        'if cnt[nums[p]] == 1': lambda S, B, r: (f'次数从 0 变成 1：{S.nums[S.p]} ==首次出现==，要累加' if S.cnt[S.nums[S.p]] == 1
                                                 else f'{S.nums[S.p]} 已在窗口中，==和不变=='),
        's += nums[p]': '`s = {B.s} + {nums[p]} = {s}`',
        'p += 1': '`p` → {p}',
        'if s < k:': lambda S, B, r: ('`p` 到头了 s 仍不够：后面的起点更不可能 → 退出' if S.s < S.k
                                      else f'`s = {S.s} ≥ {S.k}`，窗口合法'),
        'if res == -1 or': lambda S, B, r: (f'窗口长 `p − index = {S.p - S.index}`，比 `res = {S.res}` 更短 → 更新' if S.res == -1 or S.res > S.p - S.index
                                            else f'窗口长 `{S.p - S.index}` 不比 `res = {S.res}` 短，不更新'),
        'res = p - index': '`res` → =={res}==',
        'cnt[nums[index]] -= 1': '左边界 `nums[{index}] = {nums[index]}` 移出：`cnt[{nums[index]}]` → {cnt[nums[index]]}',
        'if cnt[nums[index]] == 0': lambda S, B, r: (f'次数从 1 变成 0：{S.nums[S.index]} ==不再出现==，要减掉' if S.cnt[S.nums[S.index]] == 0
                                                     else f'窗口里还有 {S.nums[S.index]}，和不变'),
        's -= nums[index]': '`s = {B.s} − {nums[index]} = {s}`',
        'return res': '最短长度为 =={ret}==',
    },
    max_steps=75,
    cards=dict(
        one_liner='固定左端点找最小右边界；左端点右移时，右边界只会往右',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给正整数数组 `nums` 和整数 `k`',
                 '求一个最短子数组，其中==不同值之和==（重复只算一次）至少为 `k`，不存在返回 `-1`',
                 '示例：`[3,2,3,4], k = 5` → `2`；本视频 `[3,2,3,3,1,4,1], k = 7` → `3`'],
        quote='对于某个起点为left的子数组，若其满足条件的最小右边界为right，那么对于左边界为left + 1的子数组，其满足条件的最小右边界==必然大于等于right==。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层枚举左边界 `index`，内层把 `p` 推到刚好满足 `s ≥ k`',
              '`cnt` 从 0 变 1 时累加、从 1 变 0 时减去，其它情况只改次数',
              '若 `p` 到末尾 s 仍不够，后面的起点也不行，直接 break'],
        summary=['时间 `O(n)`：index 和 p 都只右移；空间 `O(n)`',
                 '窗口是左闭右开 `[index, p)`，长度是 `p − index`',
                 '易错：只有次数 0↔1 变化时才改 `s`',
                 '对比灵神：灵神枚举右端点、while 里缩左端点；这里枚举左端点、推右边界',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)

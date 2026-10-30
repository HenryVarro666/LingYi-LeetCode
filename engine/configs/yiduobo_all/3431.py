def _rng(S):
    r = []
    ft, lt = S.get('first_three'), S.get('last_two')
    f2, lo = S.get('first_two'), S.get('last_one')
    if ft is not None and lt is not None:
        r.append((ft, lt, 'pink'))
    if f2 is not None and lo is not None:
        r.append((f2, lo, 'orange'))
    return r


def _ncol(S, i, v):
    if 'index' in S and S.get('_line', 0) <= 24 and i == S['index']:
        return 'blue'
    return {1: 'cyan', 2: 'yellow', 3: 'pink'}.get(v)


def _lcol(S, i, v):
    if S.get('_line', 0) >= 23 and 'index' in S and i == S['index']:
        return 'blue'
    for a, b, c in ((_rng(S))):
        if S.get('_line', 0) >= 23 and a <= i < b and v == 1:
            return 'red'
    return None


def _txt(S):
    if 'first_three' not in S:
        return ''
    f = lambda k: S.get(k)
    return f"first_two = `{f('first_two')}`　last_two = `{f('last_two')}`　last_one = `{f('last_one')}`　first_three = `{f('first_three')}`"


CONFIG = dict(
    num=3431, title='对数字排序的最小解锁下标', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='两段区间必须全部解锁',
    code='''
class Solution(object):
    def minUnlockedIndices(self, nums, locked):
        
        first_three = None
        first_two = None
        last_two = None
        last_one = None
        for index, v in enumerate(nums):
            if v == 3 and first_three is None:
                first_three = index
            if v == 2:
                if first_two is None:
                    first_two = index
                last_two = index
            if v == 1:
                last_one = index
        
        if first_three is not None and last_one is not None and first_three < last_one:
            return -1
        
        res = 0
        if first_three is not None and last_two is not None:
            for index in range(first_three, last_two):
                if locked[index] == 1:
                    locked[index] = 0
                    res += 1
        
        if first_two is not None and last_one is not None:
            for index in range(first_two, last_one):
                if locked[index] == 1:
                    res += 1
        
        return res
''',
    call='Solution().minUnlockedIndices([2,1,2,1,2,3,2], [1,1,0,1,1,1,1])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='array', var='nums', label='nums（蓝 = 1，黄 = 2，粉 = 3）', pointers={'index': 'blue'}, color=_ncol, h=210),
        dict(type='array', var='locked', label='locked（红 = 区间内仍上锁，必须解锁）', color=_lcol, h=190),
    ],
    watch=[('res', 'res', 'green'), 'first_two', 'last_two', 'last_one', 'first_three'],
    captions={
        'first_three = None': '记录四个位置：第一个 3、第一个 2、最后一个 2、最后一个 1',
        'for index, v': '{"数组扫描完了，四个位置都记好了" if B.get("index") == index else "扫描 `index = " + str(index) + "`，`v = " + str(v) + "`"}',
        'if v == 3 and': '`v = {v}`：{"第一次见到 3 → 记下 first_three" if v == 3 and B.first_three is None else "不是第一个 3"}',
        'first_three = index': '`first_three = {first_three}`：这个 3 右边的 2 都要换到它前面',
        'if v == 2': '`v = {v}` {"是 2" if v == 2 else "不是 2"}',
        'if first_two is None': '`first_two` {"还没记过 → 记下第一个 2" if first_two is None else "已记过，不改"}',
        'first_two = index': '`first_two = {first_two}`：这个 2 左边没有别的 2，右边有 1 的话要换过去',
        'last_two = index': '`last_two = {last_two}`（持续更新到最后一个 2）',
        'if v == 1': '`v = {v}` {"是 1 → 更新 last_one" if v == 1 else "不是 1"}',
        'last_one = index': '`last_one = {last_one}`（持续更新到最后一个 1）',
        'if first_three is not None and last_one': '`first_three = {first_three}`，`last_one = {last_one}`：{"3 在 1 左边，3 和 1 差 2 不能直接交换 → 无解" if first_three < last_one else "3 都在 1 右边，有解"}',
        'res = 0': '`res` 记录要解锁的下标个数',
        'for index in range(first_three': '{"第一段检查完毕" if B.get("index") == index else "3 到最后一个 2 之间的位置都要能交换：检查 `index = " + str(index) + "`"}',
        'for index in range(first_two': '{"第二段检查完毕" if B.get("index") == index else "第一个 2 到最后一个 1 之间的位置都要能交换：检查 `index = " + str(index) + "`"}',
        'if locked[index] == 1': '`locked[{index}] = {locked[index]}` → {"上锁了，必须解锁" if locked[index] == 1 else "本来就没锁"}',
        'locked[index] = 0': '解锁下标 `{index}`',
        'res += 1': '`res` = =={res}==',
        'return res': '一共要解锁 `{res}` 个下标',
    },
    cards=dict(
        one_liner='1 左边的 2、3 右边的 2，经过的位置都必须解锁',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 只含 1、2、3，`locked` 是 0/1 数组',
                 '`nums[i] - nums[i+1] == 1` 且 `locked[i] == 0` 时可交换这两个数',
                 '每次可把一个 `locked` 从 1 改成 0，求让 `nums` 能排成非降序的最少操作数，不行返回 `-1`',
                 '示例：`[2,1,2,1,2,3,2]`，`locked=[1,1,0,1,1,1,1]` → `3`'],
        quote='3不能和1直接进行交换。如果nums中存在某个3出现在某个1的左侧，那么这个3是不可能交换到1的右侧去的，也就是说不可能让nums变为可排序的。',
        quote_src='—— yiduobo 题解原文',
        idea=['3 在 1 左边 → 直接 `-1`；否则 nums 是「一些 1，一些 3，2 穿插」',
              '1 左边的 2 要全部换到最后一个 1 后面：`[first_two, last_one)` 必须全解锁',
              '3 右边的 2 要全部换到第一个 3 前面：`[first_three, last_two)` 必须全解锁'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '区间右端点不用解锁，所以是 `range(a, b)`',
                 '两段区间重叠的位置只算一次：第一段把 locked 改 0，第二段就不再数它',
                 '原文为 Python 2 风格，逻辑未改'],
    ),
)

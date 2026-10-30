CONFIG = dict(
    num=3768, title='固定长度子数组中的最小逆序对数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='滑动窗口 + 离散化树状数组',
    tags=['树状数组', '难度分 2158'],
    code='''
class Solution(object):
    def minInversionCount(self, nums, k):
        
        mapping = {}
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = len(mapping) + 1
        
        nums = [mapping[x] for x in nums]

        def add(x, f, delta):
            while x < len(f):
                f[x] += delta
                x += x & -x
        
        def get(x, f):
            cnt = 0
            while x > 0:
                cnt += f[x]
                x -= x & -x
            return cnt

        f = [0] * (len(mapping) + 1)
        now = 0
        for index in range(k - 1, -1, -1):
            v = nums[index]
            now += get(v - 1, f)
            add(v, f, 1)

        res = now
        for index, v in enumerate(nums[k:]):
            now -= get(nums[index] - 1, f)
            add(nums[index], f, -1)

            now += k - 1 - get(v, f)
            add(v, f, 1)

            res = min(res, now)
        
        return res
''',
    call='Solution().minInversionCount([3,2,1,4], 3)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（已换成名次）', h=130,
             color=lambda S, i, v: 'blue' if 'now' in S and 'self' not in S.get('_inner', {}) and S.get('_line', 0) >= 28 and 'index' in S and (S['_line'] < 33 and i == S['index']) else None),
        dict(type='array', var='f', label='树状数组 f：窗口内各名次的出现次数（前缀和）', h=140,
             color=lambda S, i, v: 'yellow' if S.get('_line', 0) in (13, 14, 15, 19, 20, 21, 22) and i == S.get('x') else None),
        dict(type='text', fn=lambda S: (f"窗口逆序对 ==now==  = {S['now']}" + (f"，目前最小 res = {S['res']}" if 'res' in S else '') if 'now' in S else '【先算出前 k 个的逆序对，再一格格滑动修正】'), h=60),
    ],
    watch=[('now', 'now', 'yellow'), ('res', 'res', 'green'), 'index', 'v'],
    captions={
        'mapping = {}': '`mapping`：数值 → 名次（离散化）',
        'for v in sorted(nums)': '按从小到大扫，给每个新数值一个名次',
        'mapping[v] = len': '`mapping[{v}] = {mapping[v]}`：第 {mapping[v]} 小的不同数值',
        'nums = [mapping': '`nums` 换成名次：{nums}，逆序关系不变',
        'f = [0]': '树状数组 `f` 下标 1..{len(mapping)}，下标 = 名次',
        'now = 0': '`now` 记录窗口内的逆序对数',
        'for index in range(k - 1': '先建第一个窗口，从右往左一个个放进去',
        'v = nums[index]': '放入 `nums[{index}] = {v}`',
        'now += get(v - 1, f)': lambda S, B, r: f"`v` 放在已放入元素的左边，逆序对增加 = 已放入的比它小的个数，用 `get({B.v} - 1)` 查，加到 `now`",
        'add(v, f, 1)': '把 `{v}` 记入树状数组，`now` = =={now}==',
        'res = now': '第一个窗口的逆序对数 `{now}` 作为 `res` 起点',
        'for index, v in enumerate': '窗口左端 `nums[{index}]`，新进元素 `nums[{index + k}]`',
        'now -= get(': lambda S, B, r: f"`nums[{B.index}]` = {B.nums[B.index]} 移出：它在最左，带走窗口里比它小的个数，用 `get({B.nums[B.index]} - 1)` 查，从 `now` 减去",
        'add(nums[index], f, -1)': '`{nums[index]}` 从树状数组里去掉，`now` = =={now}==',
        'now += k - 1 - get(v, f)': lambda S, B, r: f"新进的 `{B.v}` 在最右，逆序对增加 = 窗口里大于它的个数 = `k - 1 - get({B.v})`（旧窗口剩 k-1 个，减去 <= {B.v} 的）",
        'add(v, f, 1)': '`{v}` 进窗口，`now` = =={now}==',
        'res = min': '`res = min({B.res}, {now}) = {res}`',
        'while x < len': '`x` 沿 `x += x & -x` 向上更新',
        'f[x] += delta': '`f[{x}]` 加 `{delta}`',
        'x += x & -x': '`x += x & -x` → {x}：跳到下一个会管到当前位置的格子',
        'cnt += f[x]': '累加 `f[{x}]`，`cnt` = {cnt}',
        'x -= x & -x': '`x -= x & -x` → {x}：去掉最低位的 1，继续向左拼前缀和',
        'return cnt': '前缀和 = `{cnt}`',
        'return res': '所有窗口里最小的逆序对数 = `{res}`',
    },
    skip=['cnt = 0', 'while x > 0', 'def ', 'mapping = {}', 'for v in sorted', 'if v not in mapping'],
    max_steps=130,
    cards=dict(
        one_liner='窗口滑一格：减去离开的，加上进来的，逆序对数立刻修正',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums` 和整数 `k`',
                 '逆序对：`i < j` 且 `nums[i] > nums[j]`',
                 '求所有长度为 `k` 的子数组里，逆序对数的最小值',
                 '示例：`[3,1,2,5,4]`，`k=3` → `0`；本视频用 `[3,2,1,4]` → `1`'],
        quote='看到固定长度为k的子数组，很自然就想到滑动窗口……实际上就是需要计算窗口内小于nums[index]的元素数目，不妨记为cnt。随着nums[index]从窗口中移除，逆序对的数目v应该减去cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['窗口向右滑一格：先把最左的 `nums[index]` 带走的逆序对减掉（窗口里比它小的个数）',
              '再加新元素：窗口里大于它的个数 = 窗口大小减去 `<=` 它的个数，区间长度固定所以一步到位',
              '数值大，先按从小到大编号离散化；树状数组天然能查「<= 某值」的个数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '第一个窗口从右往左放入：每放一个，加上已放入的比它小的个数',
                 '滑动时顺序是：减去离开的 → 移除 → 查新元素 → 加上 → 加入',
                 '原文已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神每个元素进窗口时先加再检查，并有 ans == 0 提前结束；yiduobo 先单独建第一个窗口'],
    ),
)

NUMS = [2, 6, 7, 3, 1, 7]
M, K = 3, 4


def _phase2(S):
    return 'index' in S and S.get('_line') in range(14, 24)


def _counted(S):
    return sum(S['cnt'].values()) if 'cnt' in S else 0


def RP(S):
    """进入窗口的位置"""
    line = S.get('_line')
    if _phase2(S):
        return S['index'] + K
    if line in (5, 6, 7) and 'v' in S:
        c = _counted(S)
        if line == 5:
            return c if c < K else None
        return c - 1
    return None


def LP(S):
    """离开窗口的位置"""
    return S['index'] if _phase2(S) and S.get('_line') in range(14, 22) else None


def WL(S):
    if _phase2(S):
        return S['index'] + (1 if S.get('_line') in (22, 23) else 0)
    if 'cnt' in S and S.get('_line') in range(5, 13):
        return 0
    return None


def WR(S):
    line = S.get('_line')
    if _phase2(S):
        return S['index'] + K
    if line in (5, 6, 7):
        return _counted(S) - 1
    if line in range(8, 13):
        return K - 1
    return None


def _color(S, i, v):
    if RP(S) == i and S.get('_line') in (6, 7, 15, 20):
        return 'green'
    if LP(S) == i and S.get('_line') in (16, 17, 18, 21):
        return 'red'
    return None


def _info(S):
    if 'cnt' not in S:
        return f'窗口长度 `k = {K}`，至少要有 `m = {M}` 种不同数字'
    extra = ''
    if S.get('_line') in (15, 16, 17, 18, 20, 21):
        extra = '（滑动中：暂时有 k+1 个数）'
    return f"窗口和 `s = {S.get('s', 0)}`，数字种数 `len(cnt) = {len(S['cnt'])}`{extra}"


def _for1(S, B, ret):
    if _counted(S) < K or S.get('v') != B.get('v'):
        return f'先把前 k 个数放进窗口：`v = {S.v}`'
    return f'前 `k = {K}` 个数都放进窗口了'


def _len1(S, B, ret):
    d = len(S.cnt)
    if d >= M:
        return f'第一个窗口有 `{d} ≥ m = {M}` 种数字 → 用它初始化答案'
    return f'第一个窗口只有 `{d} < m = {M}` 种数字'


def _for2(S, B, ret):
    if 'index' in S and S.index != B.get('index'):
        return f'窗口右移一格：`nums[{S.index + K}] = {S.v}` 要进来，`nums[{S.index}] = {S.nums[S.index]}` 要出去'
    return '窗口滑到底了'


def _zero(S, B, ret):
    o = S.nums[S.index]
    if S.cnt.get(o) == 0:
        return f'`cnt[{o}]` 变成了 0：窗口里已经没有 `{o}` 了'
    return f'`cnt[{o}] = {S.cnt[o]}`：窗口里还有 `{o}`，保留'


def _len2(S, B, ret):
    d = len(S.cnt)
    if d >= M:
        return f'`len(cnt) = {d} ≥ m = {M}`：窗口内至少有 m 种不同数字 → ==用 s 更新答案=='
    return f'`len(cnt) = {d} < m = {M}`：不满足，不更新'


CONFIG = dict(
    num=2841, title='几乎唯一子数组的最大和', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='定长滑动窗口 + 哈希计数',
    tags=['字节30天'],
    code='''
class Solution(object):
    def maxSum(self, nums, m, k):
        cnt = {}
        s = 0
        for v in nums[:k]:
            cnt[v] = cnt.get(v, 0) + 1
            s += v

        if len(cnt) >= m:
            res = s
        else:
            res = 0

        for index, v in enumerate(nums[k:]):
            cnt[v] = cnt.get(v, 0) + 1
            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                cnt.pop(nums[index])

            s += v
            s -= nums[index]
            if len(cnt) >= m:
                res = max(res, s)

        return res
''',
    call=f'Solution().maxSum({NUMS}, {M}, {K})',
    expect=18,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口，绿 = 进入，红 = 离开）', cell=90,
             pointers={RP: 'green', LP: 'pink'}, pointer_labels={RP: '进', LP: '出 index'},
             window=(WL, WR), color=_color),
        dict(type='text', h=60, fn=_info, size=27),
        dict(type='map', var='cnt', label='cnt（窗口中每种数字出现的次数）', h=140, font=28, fmt=lambda k, v: f'{k}: {v} 次'),
    ],
    watch=[('index', 'index', 'pink'), ('v', 'v', 'green'), ('s', 's', 'cyan'), ('len(cnt)', 'len(cnt)', 'purple'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '哈希表 `cnt` 记录窗口中==每种数字出现的次数==',
        4: '变量 `s` 记录窗口内数字之和',
        'for v in nums[:k]': _for1,
        6: '`cnt[{v}] = {cnt[v]}`',
        7: '`s += {v}` → `{s}`',
        9: _len1,
        'res = s': '`res = {res}`',
        'res = 0': '先令 `res = 0`（题目要求不存在时返回 0）',
        'for index, v in': _for2,
        15: '==先加右边==：`cnt[{v}] = {cnt[v]}`',
        'cnt[nums[index]] -= 1': '再减左边：`cnt[{nums[index]}]` 减一 → `{cnt[nums[index]]}`',
        'if cnt[nums[index]] == 0': _zero,
        'cnt.pop': '出现次数为 0 → `cnt.pop({nums[index]})`，==弹出哈希表==，否则 `len(cnt)` 会多算',
        20: '`s += {v}` → `{s}`',
        21: lambda S, B, ret: f'`s -= {S.nums[S.index]}` → `{S.s}`：窗口回到 k 个数 `{S.nums[S.index + 1:S.index + 1 + K]}`',
        22: _len2,
        'res = max': '`res = max({B.res}, {s}) = {res}`',
        'return res': '最大和为 =={ret}==',
    },
    cards=dict(
        one_liner='长度为 k 的窗口从左往右滑，哈希表的长度就是窗口里的数字种数',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['给你整数数组 `nums` 和正整数 `m`、`k`',
                 '长度为 `k` 且==至少有 `m` 个互不相同元素==的子数组叫“几乎唯一”，求它们的最大和（没有返回 0）',
                 '示例：`nums = [2,6,7,3,1,7], m = 3, k = 4` → `18`'],
        quote='当窗口向右滑动时，首先将右边界对应的数字在cnt中出现的次数加上1……然后将左边界对应的数字……在cnt中出现的次数减去1。==若这个数字出现次数变为了0，就将其弹出哈希表==。',
        quote_src='—— yiduobo 题解原文',
        idea=['先单独统计前 `k` 个数，得到第一个窗口的 `cnt`、`s` 和初始答案',
              '之后每次右移：加右边、减左边，次数为 0 就从哈希表 `pop` 掉',
              '`len(cnt) ≥ m` 说明窗口内至少有 m 种不同数字，用 `s` 更新答案'],
        result='运行结束，返回 `18`：`[2,6,7,3]` 和 `[7,3,1,7]` 的和都是 18',
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '易错：次数减到 0 必须 `pop`，否则 `len(cnt)` 偏大',
                 '`enumerate(nums[k:])` 的 `index` 从 0 开始，恰好就是要离开的左端点下标',
                 '对比灵神：灵神用一个循环写“入-更新-出”，yiduobo 先建好第一个窗口再滑动',
                 '原文为 Python 2 风格，只删去了 docstring，代码未改'],
    ),
)

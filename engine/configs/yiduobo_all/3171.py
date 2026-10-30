def _bits(v, w=4):
    return format(v, '0%db' % w)


def _freq(S):
    if 'freq' not in S:
        return ''
    nz = [f'位{d}:{c}' for d, c in enumerate(S['freq']) if c]
    return '`freq`（窗口内各二进制位上 1 的个数）：' + ('　'.join(nz) if nz else '全 0')


def _now(S):
    if 'now' not in S:
        return ''
    r = S['res']
    return f"窗口或值 `now = {_bits(S['now'])}` = =={S['now']}==　`k = {S['k']}`　`res` = =={'—' if r is None else r}=="


CONFIG = dict(
    num=3171, title='找到按位或最接近 K 的子数组', difficulty='Hard', category='位运算',
    author='yiduobo', technique='滑动窗口 · 二进制位计数 freq',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minimumDifference(self, nums, k):

        freq = [0] * 30
        now = 0
        p = 0
        res = None

        for index, v in enumerate(nums):
            now |= v

            for d in range(30):
                if v & (1 << d) == (1 << d):
                    freq[d] += 1

            if res is None or res > abs(now - k):
                res = abs(now - k)
            
            while p < index and now > k:
                for d in range(30):
                    if nums[p] & (1 << d) == (1 << d):
                        freq[d] -= 1
                        if freq[d] == 0:
                            now ^= (1 << d)
                p += 1
            
                if res is None or res > abs(now - k):
                    res = abs(now - k)

        return res
''',
    call='Solution().minimumDifference([1,4,8,1,3], 10)',
    expect=1,
    views=[
        dict(type='text', fn=_now, size=28, h=60),
        dict(type='array', var='nums', pointers={'p': 'pink', 'index': 'blue'}, window=('p', 'index'), h=240, label='nums（窗口 = p 到 index）',
             dim=lambda S, i, v: 'p' in S and not (S['p'] <= i <= S['index'])),
        dict(type='text', fn=_freq, size=26, h=70),
    ],
    watch=['index', 'p', ('now', 'now', 'cyan'), ('k', 'k', 'yellow'), ('res', 'res', 'green')],
    skip=['for d in range(30)', 'if v & (1 << d)', 'freq[d] += 1', 'if nums[p] & (1 << d)', 'freq[d] -= 1',
          'if freq[d] == 0', 'now ^= (1 << d)'],
    captions={
        'freq = [0]': '`freq[d]`：窗口里二进制第 `d` 位是 1 的元素个数（OR 没有逆运算，要靠计数删元素）',
        'now = 0': '`now` 是窗口内所有数的按位或，初始为 0',
        'p = 0': '`p` 是窗口左端点，`index` 是右端点',
        'res = None': '`res` 记最小差，先空着',
        'for index, v': lambda S, B, r: (f'`index = {S.index}`：右端点加入 `{S.v}`' if S.get('index') != B.get('index') else '数组走完，窗口扫描结束'),
        'now |= v': '`now |= {v}` → `now = {now}`；同时 `freq` 逐位加 1（`v` 里是 1 的位）',
        'if res is None or res > abs(now - k)': lambda S, B, r: (f'窗口 `[{S.p}..{S.index}]` 或值 `{S.now}`，差 `|{S.now} − {S.k}| = {abs(S.now - S.k)}`，和 `res` 比较'),
        'res = abs(now - k)': '更新：`res = {res}`',
        'while p < index and now > k': lambda S, B, r: (f'`now = {S.now} > k = {S.k}` 且窗口不止一个元素 → ==窗口或值太大，弹出左端点== 试试变小' if S.p < S.index and S.now > S.k
                                                        else (f'`now = {S.now} <= k = {S.k}`：不用再缩，换下一个右端点' if S.now <= S.k else f'窗口只剩一个元素 `{S.nums[S.p]}`（题目要求非空）→ 不能再缩')),
        'p += 1': '移出 `nums[{p-1}]`：它为 1 的位在 `freq` 里减 1，减到 0 的位从 `now` 里去掉 → `now = {now}`，`p = {p}`',
        'return res': '最小差 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='窗口或值越大越大，用 freq 记每一位的 1 的个数来删元素',
        complexity='时间 `O(30n)`，空间 `O(30)`',
        problem=['在 `nums` 中选连续非空子数组，使按位或与 `k` 的差绝对值最小',
                 '示例：`nums=[1,3,1,3], k=2` → `1`',
                 '本视频：`[1,4,8,1,3], k=10` → `1`'],
        quote='参与运算的数字越多，按位或的结果就越大……需要额外维护一个频率数组freq，其中freq[d]表示当前窗口内元素在二进制位d这一位上1的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['或值随窗口变长而变大 → 变长滑动窗口，`now > k` 就左端点右移',
              '删元素时不能直接异或：别的元素可能也有那一位，所以用 `freq[d]` 计数',
              '`freq[d]` 减到 0，说明窗口里没人有这一位 → 才把它从 `now` 去掉；每次移动都更新 `res`'],
        summary=['时间 `O(30n)`，空间 `O(30)`',
                 '易错：窗口必须非空，所以 `while p < index`',
                 '易错：右端点加入后先更新一次 `res`，再收缩',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神用 LogTrick 原地改 nums，不用 freq'],
    ),
)

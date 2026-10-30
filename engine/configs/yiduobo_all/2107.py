def _l(S):
    i = S.get('index')
    return 0 if i is None else i + 1


def _r(S):
    i = S.get('index')
    return S['k'] - 1 if i is None else i + S['k']


CONFIG = dict(
    num=2107, title='分享K个糖果后独特口味的数量', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='定长滑窗 · 统计窗口外',
    tags=['会员题'],
    code='''
class Solution(object):
    def shareCandies(self, candies, k):

        cnt = {}
        for v in candies[k:]:
            cnt[v] = cnt.get(v, 0) + 1
        
        res = len(cnt)
        for index, v in enumerate(candies[k:]):
            cnt[candies[index]] = cnt.get(candies[index], 0) + 1
            cnt[v] -= 1
            if cnt[v] == 0:
                cnt.pop(v)
            
            res = max(res, len(cnt))
        
        return res
''',
    call='Solution().shareCandies([1,2,2,3,4,3], 3)',
    expect=3,
    views=[
        dict(type='array', var='candies', label='candies（框 = 送出去的 k 个，框外 = 留给自己）', window=(_l, _r),
             pointers={'index+k': 'pink'}, h=210, cell=90),
        dict(type='map', var='cnt', label='cnt（框外每种口味的个数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', h=80, size=32,
             fn=lambda S: (f'窗口外有 `{len(S["cnt"])}` 种口味，目前最多 ==`{S["res"]}`== 种' if 'res' in S and 'cnt' in S
                           else '送出一段长 k 的连续糖果，使自己手里的口味最多')),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('len(cnt)', 'len(cnt)', 'cyan'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '`cnt` 记录==窗口外==每种口味的个数（和常规滑窗相反）',
        'for v in candies[k:]': lambda S, B, r: ('窗口外的糖果都记好了' if sum(B.cnt.values()) == len(S.candies) - S.k else f'先假设送出前 `k` 个，把剩下的 `{S.v}` 都记进 `cnt`'),
        'cnt[v] = cnt.get(v, 0) + 1': '`cnt[{v}] = {cnt[v]}`',
        'res = len(cnt)': '送出最前面 `k` 个时，手里有 `{res}` 种口味',
        'for index, v in enumerate(candies[k:])': lambda S, B, r: ('所有窗口都试完了' if 'index' in B and S.index == B.index else f'窗口右移一格：`candies[{S.index}] = {S.candies[S.index]}` 滑出窗口（回到手里），`candies[{S.index + S.k}] = {S.v}` 滑进窗口（送出去）'),
        'cnt[candies[index]] = ': '滑出的 `{candies[index]}` 回到窗口外：`cnt[{candies[index]}] = {cnt[candies[index]]}`',
        'cnt[v] -= 1': '滑进窗口的 `{v}` 被送走：窗口外少一个 → `cnt[{v}] = {cnt[v]}`',
        'if cnt[v] == 0': lambda S, B, r: (f'`{S.v}` 在窗口外一个不剩 → 这种口味==没了==，要删键' if S.cnt[S.v] == 0
                                           else f'`{S.v}` 窗口外还有 `{S.cnt[S.v]}` 个，口味数不变'),
        'cnt.pop(v)': '删掉键 `{v}`，`len(cnt)` 才是剩余口味数',
        'res = max': '手里 `{len(cnt)}` 种，`res = max({B.res}, {len(cnt)}) = {res}`',
        'return res': '最多能留 `{res}` 种口味',
    },
    max_steps=70,
    cards=dict(
        one_liner='滑窗反着用：维护窗口外的口味，窗口外越多越好',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `candies`，==送出==一段连续 `k` 个糖果，求自己手里剩下的最多口味种数',
                 '示例：`[1,2,2,3,4,3]`, `k = 3` → `3`（送出 `[1,2,2]`，剩 `3,4,3`）',
                 '本视频即该示例'],
        quote='本题要求从数组中移除一个子数组，使得数组中剩余数字的种类最多，属于是滑动窗口问题的反向版。与常规的滑动窗口问题不同，本题需要维护的是窗口滑动过程中在窗口外的每种数字的个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt` 统计窗口外：初始窗口放最前面 `k` 个',
              '窗口右移：左边滑出的数回到 `cnt`（+1），右边滑进的数从 `cnt` 扣掉（−1）',
              '扣到 0 要删键，用 `len(cnt)` 更新最大值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：窗口里的数不能算进种类，所以是 ==减==；减到 0 一定要 `pop`',
                 '初始状态（送出前 `k` 个）也是一个候选答案，所以 `res = len(cnt)` 在循环前',
                 '`k = 0` 时直接是全数组种类数，`enumerate(candies[k:])` 仍然成立'],
    ),
)

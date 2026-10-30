NUMS = [0, 1, 2, 2, 4, 4, 1]

CONFIG = dict(
    num=2404, title='出现最频繁的偶数元素', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 边统计边维护答案',
    tags=[],
    code='''
class Solution:
    def mostFrequentEven(self, nums: List[int]) -> int:
        ans = -1
        cnt = Counter()
        for x in nums:
            if x % 2: continue  # 跳过奇数
            cnt[x] += 1
            if cnt[x] > cnt[ans] or cnt[x] == cnt[ans] and x < ans:
                ans = x  # 出现次数最大的数中，值最小的
        return ans
''',
    call=f'Solution().mostFrequentEven({NUMS})',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', pointers={'x': 'blue'}, cell=96, h=190,
             color=lambda S, i, v: 'green' if 'ans' in S and v == S['ans'] and v % 2 == 0 else None,
             dim=lambda S, i, v: v % 2 == 1),
        dict(type='map', var='cnt', label='cnt（偶数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"当前答案 `ans = {S['ans']}`" + (f"，次数 `{S['cnt'][S['ans']]}`" if 'cnt' in S and S['ans'] in S['cnt'] else '') if 'ans' in S else ''),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = -1': '先假定没有偶数：`ans = -1`',
        'cnt = Counter()': '`cnt` 记录每个偶数出现了几次',
        'for x in nums': lambda S, B, ret: ('遍历结束' if 'x' in B and B.x == S.x and S.x == NUMS[-1] else f'取下一个数 `x = {S.x}`'),
        'if x % 2': lambda S, B, ret: (f'`{S.x}` 是奇数，跳过' if S.x % 2 else f'`{S.x}` 是偶数，要统计'),
        'cnt[x] += 1': '`cnt[{x}]` 加一 → `{cnt[x]}`',
        'if cnt[x] > cnt[ans]': lambda S, B, ret: (
            f'`cnt[{S.x}] = {S.cnt[S.x]}` 比当前答案 {S.ans} 的次数 `{S.cnt[S.ans]}` ==更多== → 更新' if S.cnt[S.x] > S.cnt[S.ans]
            else (f'次数相同（{S.cnt[S.x]}），且 `{S.x} < {S.ans}` → ==取更小的数==更新' if S.cnt[S.x] == S.cnt[S.ans] and S.x < S.ans
                  else f'次数相同（{S.cnt[S.x]}），但 `{S.x} > {S.ans}`，不更小 → 不更新' if S.cnt[S.x] == S.cnt[S.ans]
                  else f'`cnt[{S.x}] = {S.cnt[S.x]}`，没超过 `{S.ans}` 的 `{S.cnt[S.ans]}` 次→ 不更新')),
        'ans = x': '`ans = {ans}`：出现次数最大的数中值最小的',
        'return ans': '返回 `{ans}`：2 和它同样是 2 次时，4 比 2 大，保留 2',
    },
    cards=dict(
        one_liner='边统计边擂台：次数多者胜，次数相同取更小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['返回 `nums` 中出现次数最多的==偶数==；次数相同取最小的；没有偶数返回 `-1`',
                 '示例：`[0,1,2,2,4,4,1]` → `2`（2 和 4 都出现 2 次，取更小的）'],
        quote='用哈希表 cnt 统计每个偶数的出现次数，在统计的过程中，维护出现次数最大的最小元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遇到奇数直接跳过，偶数才计数',
              '每次计数后立刻和当前答案 `ans` 比：次数更大，或次数相同但值更小，就换掉',
              '`ans = -1` 时 `cnt[-1]` 是 0，所以第一个偶数一定能替换它'],
        summary=['时间 `O(n)`，空间 `O(n)`，只遍历一遍',
                 '易错：次数相同时要比较值，取更小的',
                 '没有偶数时 `ans` 一直是 `-1`',
                 '另一种写法：先 `Counter` 统计，再取 `max` 次数对应的 `min` 值，需要多遍历'],
    ),
)

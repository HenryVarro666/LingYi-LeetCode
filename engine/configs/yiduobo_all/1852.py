def _win(S):
    i = S.get('index')
    return 0 if i is None else i + 1


def _win_r(S):
    i = S.get('index')
    return S['k'] - 1 if i is None else i + S['k']


def _cnt_txt(S):
    if 'cnt' not in S:
        return ''
    return f'窗口里有 `{len(S["cnt"])}` 种不同的数字：' + '、'.join(str(x) for x in S['cnt'])


CONFIG = dict(
    num=1852, title='每个子数组的数字种类数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='定长滑窗 + 哈希表计数',
    tags=['会员题'],
    code='''
class Solution(object):
    def distinctNumbers(self, nums, k):

        cnt = {}
        for v in nums[:k]:
            cnt[v] = cnt.get(v, 0) + 1
        
        res = [len(cnt)]
        for index, v in enumerate(nums[k:]):
            cnt[v] = cnt.get(v, 0) + 1
            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                cnt.pop(nums[index])
            
            res.append(len(cnt))
        
        return res
''',
    call='Solution().distinctNumbers([1,2,3,2,2,1,3], 3)',
    expect=[3, 2, 2, 2, 3],
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前窗口，长 k）', window=(_win, _win_r),
             pointers={'index+k': 'blue'}, h=200, cell=90),
        dict(type='map', var='cnt', label='cnt（窗口内每个数字出现次数）', fmt=lambda k, v: f'{k}: {v}', h=160, font=34),
        dict(type='array', var='res', label='res（每个窗口的种类数）', h=150, cell=90),
        dict(type='text', h=70, size=30, fn=_cnt_txt),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('k', 'k'), ('len(cnt)', 'len(cnt)', 'green')],
    captions={
        'cnt = {}': '用哈希表 `cnt` 记录窗口里每种数字出现的次数',
        'for v in nums[:k]': lambda S, B, r: ('第一个窗口的数字都放好了' if sum(B.cnt.values()) == S.k else f'先把第一个窗口的数字 `{S.v}` 放进去'),
        'cnt[v] = cnt.get(v, 0) + 1': lambda S, B, r: (f'`{S.v}` 次数加一 → `cnt[{S.v}] = {S.cnt[S.v]}`'),
        'res = [len(cnt)]': '第一个窗口有 `{len(cnt)}` 种数字（哈希表的键数）→ `res = {res}`',
        'for index, v in enumerate(nums[k:])': lambda S, B, r: ('所有窗口都滑完了' if 'index' in B and S.index == B.index else f'窗口右移一格：右边进来 `{S.v}`（`nums[{S.index + S.k}]`），左边要出去 `nums[{S.index}] = {S.nums[S.index]}`'),
        'cnt[nums[index]] -= 1': '左边的 `{nums[index]}` 离开窗口：次数减一 → `{cnt[nums[index]]}`',
        'if cnt[nums[index]] == 0': lambda S, B, r: (f'`{S.nums[S.index]}` 次数变成 0：窗口里已经==没有它==了，要从表中删掉' if S.cnt[S.nums[S.index]] == 0
                                                     else f'`{S.nums[S.index]}` 还剩 `{S.cnt[S.nums[S.index]]}` 个，种类数不变'),
        'cnt.pop': '删掉键 `{nums[index]}`，否则 `len(cnt)` 会多算',
        'res.append(len(cnt))': '键的个数就是种类数：`len(cnt) = {len(cnt)}` → 加入 `res`',
        'return res': '每个窗口的种类数：`{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='定长窗口右移：进一个数、出一个数，键数就是种类数',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['给数组 `nums` 和 `k`，求每个长为 `k` 的连续子数组中==不同数字的个数==',
                 '示例：`[1,2,3,2,2,1,3]`, `k = 3` → `[3,2,2,2,3]`'],
        quote='非常标准的滑动窗口问题。维护一个长度为k的窗口，从数组左侧开始向右滑动，过程中使用哈希表记录当前窗口中每种数字出现的次数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先统计前 `k` 个数，得到第一个窗口的答案',
              '窗口右移：新数次数 +1，旧数次数 −1',
              '旧数次数减到 0 要==删键==，`len(cnt)` 才是种类数'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '易错：次数为 0 时必须 `pop`，只减不删会多算种类',
                 '`enumerate(nums[k:])` 里 `index` 对应要移出的 `nums[index]`，新进来的是 `nums[index+k]`',
                 '这是 VIP 题，思路同 3439、2107 等定长滑窗'],
    ),
)

NUMS = [1, 2, 1, 4]
K = 2
SN = sorted(NUMS)
N = len(SN)
VM = SN[-1]


def _live(S):
    return S.get('_line', 0) >= 34 and S.get('state') is not None and S.get('last') is not None


def _cell(S, r, c, v):
    if not _live(S):
        return None
    line = S['_line']
    if (r, c) == (S['state'], S['last']):
        return 'yellow'
    ns, cn = S.get('next_state'), S.get('check_num')
    if line >= 54 and ns is not None and cn is not None and (r, c) == (ns, cn):
        return 'green'
    return None


def _formula(S):
    if not _live(S):
        return '`f[state][last]` = 用了 `state` 里的数、最后用的数是 `last` 时的最小代价'
    gs = S.get('group_size')
    uc = S.get('used_cnt')
    if S['_line'] < 45 or uc is None:
        return f'处理可达状态 `state = {S["state"]:0{N}b}`（最后用的数 `last = {S["last"]}`，当前最小代价 {S.get("f")[S["state"]][S["last"]] if S.get("f") else "?"}）'
    pos_in_group = uc % gs
    return f'已用 `{uc}` 个数，当前组已放 `{uc} % {gs} = {pos_in_group}` 个' + ('，下一个要==开新组==' if pos_in_group == 0 else '，下一个只能选 ==比 last 大== 的数')


def _cap_new(S, B, ret):
    return f'已用 `{S.used_cnt}` 个数，`{S.used_cnt} % {S.group_size} = {S.used_cnt % S.group_size}` ' + ('→ 当前组是空的，新组可以选任意还没用完的数（从 0 起找）' if S.used_cnt % S.group_size == 0 else f'→ 当前组还没满，只能选比 `last = {S.last}` 大的数（组内严格递增，不重复）')


CONFIG = dict(
    num=1681, title='最小不兼容性', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按大小顺序放数的状压 DP',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minimumIncompatibility(self, nums, k):

        nums.sort()
        next = {}
        cnt = {}
        pos = {}
        now = 0
        n = len(nums)
        if k == n:
            return 0
        
        group_size = n // k
        for index in range(n):
            if nums[index] != now:
                next[now] = nums[index]
                now = nums[index]
                pos[nums[index]] = index
            
            cnt[nums[index]] = cnt.get(nums[index], 0) + 1
            
        max_state = 1 << n
        f = [[None] * (nums[-1] + 1) for _ in range(max_state)]
        f[0][0] = 0

        res = -1
        for state in range(max_state):
            for last in range(nums[-1] + 1):
                if f[state][last] is not None:
                    if state == max_state - 1:
                        if res == -1 or res > f[state][last]:
                            res = f[state][last]
                    else:
                        used = {}
                        used_cnt = 0
                        used_min = None
                        for index in range(n):
                            if state & (1 << index):
                                num = nums[index]
                                used[num] = used.get(num, 0) + 1
                                used_cnt += 1
                                if used_min is None:
                                    used_min = num
                    
                        if used_cnt % group_size == 0:
                            now = 0
                        else:
                            now = last
                    
                        while now in next:
                            check_num = next[now]
                            used_check_num = used.get(check_num, 0)
                            if used_check_num < cnt[check_num]:
                                next_state = state | (1 << (pos[check_num] + used_check_num))
                                next_cost = f[state][last]
                                if used_cnt % group_size == group_size - 1:
                                    next_cost += check_num - used_min
                                if f[next_state][check_num] is None or f[next_state][check_num] > next_cost:
                                    f[next_state][check_num] = next_cost
                        
                            now = check_num
                    
        return res
''',
    call=f'Solution().minimumIncompatibility({NUMS}, {K})',
    expect=4,
    skip=[8, 10, 45, 56, 58, 'if state == max_state - 1', 'nums.sort()', 'next = {}', 'cnt = {}', 'pos = {}', 'n = len(nums)', 'for index in range', 'if nums[index] != now', 'next[now] =',
          'now = nums[index]', 'pos[nums[index]] =', 'cnt[nums[index]] =', 'max_state = 1', 'f = [[None]', 'res = -1', 'for state in range', 'for last in range',
          'if f[state][last] is not None', 'used_cnt = 0', 'used_min = None', 'if state & (1 << index)', 'num = nums[index]', 'used[num] =',
          'used_cnt += 1', 'if used_min is None', 'used_min = num', 'check_num = next[now]', 'used_check_num =', 'next_cost = f[state][last]', 'now = check_num'],
    max_steps=54,
    views=[
        dict(type='text', fn=_formula, size=24, h=80),
        dict(type='array', var='nums', label='排序后的 nums（绿 = 已用进 state 的数）', h=170, cell=84,
             color=lambda S, i, v: ('green' if S.get('state') is not None and S.get('_line', 0) >= 34 and S['state'] >> i & 1 else None)),
        dict(type='table', var='f', label='f[state][last]：行 = state，列 = last', h=500, cell=46,
             rows=lambda S: [f'{k:0{N}b}' for k in range(2 ** N)], cols=lambda S: [f'{k}' for k in range(VM + 1)],
             color=_cell),
    ],
    watch=[('state', 'state', 'yellow'), ('last', 'last', 'blue'), ('now', 'now', 'pink'), ('next_cost', 'next_cost', 'green')],
    captions={
        'group_size = n // k': '`n = {n}`，分 `k = {k}` 组 → 每组 `group_size = {group_size}` 个数；`nums` 已排序，组内数从小到大放',
        'max_state = 1 << n': '`{n}` 个数 → `{max_state}` 种状态；`f[state][last]` 初值全是 None（不可达）',
        'f[0][0] = 0': '起点：什么都没选、`last = 0`，代价 0',
        'return 0': '每组只有一个数，不兼容性必为 0',
        'used = {}': lambda S, B, r: f'可达状态 `state = {S.state:0{S.n}b}`、`last = {S.last}`，它的最小代价是 `{S.f[S.state][S.last]}`；统计 state 里用了几个数、最小的是谁',
        'if res == -1 or res > f': '`res = {res}`，和这个终点的代价 `{f[state][last]}` 比，取小',
        'res = f[state][last]': '更新答案：`res = {res}`',
        'if used_cnt % group_size == 0': _cap_new,
        46: '已用 `{used_cnt}` 个，`{used_cnt} % {group_size} = 0` → 当前组是空的，开新组：从最小的数开始找（`now = 0`）',
        48: '已用 `{used_cnt}` 个，`{used_cnt} % {group_size} = {used_cnt % group_size}` → 当前组没满，接着放：只看比 `last = {last}` 大的数',
        'while now in next': lambda S, B, r: (f'`now = {S.now}` 后面还有更大的数 `{S.next[S.now]}` 可试' if S.now in S.next else '没有更大的数了，这个状态处理完'),
        'if used_check_num < cnt[check_num]': lambda S, B, r: (f'数字 `{S.check_num}` 一共 `{S.cnt[S.check_num]}` 个，已用 `{S.used_check_num}` 个 → 还有剩余，可以放' if S.used_check_num < S.cnt[S.check_num]
                                                               else f'数字 `{S.check_num}` 已经用完了，跳过'),
        'next_state = state': '放进第 `{used_check_num}` 个 `{check_num}`（下标 `{pos[check_num] + used_check_num}`）：同值的数按下标顺序放，避免重复状态 → `next_state = {next_state:0{n}b}`',
        'next_cost += check_num': '这个数放下后当前组刚好满 → 加上该组代价：最大 `{check_num}` − 最小 `{used_min}`（state 里的最小值一定在最后这一组）→ `next_cost = {next_cost}`',
        'if f[next_state][check_num] is None': lambda S, B, r: ('新状态不可达，或者新代价更小 → 更新' if (S.f[S.next_state][S.check_num] is None or S.f[S.next_state][S.check_num] > S.next_cost) else '已有更小的代价，不更新'),
        'f[next_state][check_num] = next_cost': '`f[{next_state:0{n}b}][{check_num}] = {next_cost}`',
        'return res': '最小不兼容性之和 = =={ret}==',
    },
    cards=dict(
        one_liner='排序后按从小到大放数，组满时一次结算代价',
        complexity='时间约 `O(2^n · n · V)`，空间 `O(2^n · V)`（`V` 为最大值，`n ≤ 16`）',
        problem=['把 `nums` 分成 `k` 个大小相同的子集，每个子集里==没有重复数字==',
                 '一个子集的不兼容性 = 最大值 − 最小值；求各子集之和的最小值，分不了返回 `-1`',
                 '示例：`nums = [1,2,1,4], k = 2` → `4`（`{1,2}` 和 `{1,4}`，1 + 3）'],
        quote='由于组中的数先后顺序其实是不敏感的，因此可以强制设定每一组中的数是从小到大添加进来的，于是可以先将数组从小到大进行排序。',
        quote_src='—— yiduobo 题解',
        idea=['`f[state][last]`：用了 `state` 表示的数、最后放的数是 `last` 的最小代价',
              '已用 `cnt` 个数，当前组里有 `cnt % group_size` 个：为 0 开新组，否则只能选比 `last` 大的',
              '组恰好放满时结算代价：最大是新放的数，最小就是 `state` 里最小的数'],
        summary=['时间约 `O(2^n · n · V)`；`n ≤ 16` 所以可行',
                 '原文为 Python 2 写法，`group_size = n / k` 已改为 `n // k`（整数除法）',
                 '易错：同值的数必须按下标顺序放（`pos[num] + used`），否则同一集合会有多种状态；终点 `res` 可能一直是 `-1`',
                 '「state 中的最小值必在最后一组」靠的是最小代价的性质：放别的组只会更大'],
    ),
)

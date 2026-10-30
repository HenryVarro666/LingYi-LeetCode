CONFIG = dict(
    num=3092, title='最高频率的 ID', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + 懒删除堆',
    tags=['难度分 1793'],
    setup='''
def heappush_max(h, x):
    h.append(x)
    heapq._siftdown_max(h, 0, len(h) - 1)
heappop_max = heapq._heappop_max
''',
    code='''
class Solution:
    def mostFrequentIDs(self, nums: List[int], freq: List[int]) -> List[int]:
        cnt = defaultdict(int)
        h = []
        ans = []
        for x, f in zip(nums, freq):
            cnt[x] += f
            heappush_max(h, (cnt[x], x))
            while h[0][0] != cnt[h[0][1]]:  # 堆顶保存的数据已经发生变化
                heappop_max(h)  # 删除
            ans.append(h[0][0])
        return ans
''',
    call='Solution().mostFrequentIDs([2,3,2,1], [3,2,-3,1])',
    expect=[3, 3, 2, 2],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前操作的 ID）', h=140,
             color=lambda S, i, v: 'blue' if 'ans' in S and i == len(S['ans']) else None,
             dim=lambda S, i, v: 'ans' in S and i < len(S['ans'])),
        dict(type='array', var='freq', label='freq', h=140,
             color=lambda S, i, v: 'blue' if 'ans' in S and i == len(S['ans']) else None,
             dim=lambda S, i, v: 'ans' in S and i < len(S['ans'])),
        dict(type='map', var='cnt', label='cnt（ID → 当前个数，最新值）', fmt=lambda k, v: f'{k} → {v}', h=130),
        dict(type='heap', var='h', label='h（最大堆，元素 = (个数, ID)）', fmt=lambda t: f'{t[0]},{t[1]}', h=180),
        dict(type='array', var='ans', label='ans', h=130),
    ],
    watch=['x', 'f', ('堆顶', 'h[0] if h else None', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'cnt = defaultdict': '`cnt[x]`：ID `x` 目前的个数（最新值）',
        'h = []': '最大堆 `h` 存 `(cnt[x], x)`，旧记录不删，等它冒到堆顶再说',
        'for x, f in zip': lambda S, B, r: ('所有操作处理完了' if len(S.ans) == len(S.nums) else f'第 {len(S.ans)+1} 步操作：ID `{S.x}` 的个数变化 `{S.f}`'),
        'ans = []': '`ans` 收集每步操作后的最高频率',
        'cnt[x] += f': '`cnt[{x}]` 从 `{cnt[x]-f}` 变成 =={cnt[x]}==',
        'heappush_max': '把最新记录 `({cnt[x]}, {x})` 直接入堆，不去找旧记录',
        'while h[0][0] != cnt': lambda S, B, r: (
            f'堆顶 `({S.h[0][0]}, {S.h[0][1]})`，但 `cnt[{S.h[0][1]}]` = {S.cnt[S.h[0][1]]}：==已过期==，要弹掉'
            if S.h[0][0] != S.cnt[S.h[0][1]]
            else f'堆顶 `({S.h[0][0]}, {S.h[0][1]})` 与 `cnt[{S.h[0][1]}]` = {S.cnt[S.h[0][1]]} 一致 → 有效，停止弹出'),
        'heappop_max(h)': '弹出过期的堆顶：它是旧数据，不是当前真实个数',
        'ans.append': '堆顶一定有效 → 最高频率 =={h[0][0]}==，记入 `ans`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='堆里旧数据不删，堆顶「货不对板」再弹',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums[i]` 是 ID，`freq[i]` 是该 ID 个数的增减量',
                 '每步操作后，返回出现次数最多的 ID 的==次数==；集合为空返回 0',
                 '示例：`[2,3,2,1]`，`[3,2,-3,1]` → `[3,3,2,2]`'],
        quote='在堆中查询 cnt[x] 的最大值时，如果堆顶保存的数据并不是目前实际的 cnt[x]，那么就弹出堆顶。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['哈希表 `cnt` 始终记着每个 ID 的真实个数',
              '每次更新后把新的 `(cnt[x], x)` 入最大堆，旧记录留着不管',
              '查询前先检查堆顶是否等于真实值，不等就弹掉，直到堆顶有效'],
        summary=['至多入堆 `n` 次，出堆也至多 `n` 次，总时间 `O(n log n)`',
                 '堆顶有效 ⇒ 它就是最大值：比它大的记录都已过期被弹掉',
                 '写法一：哈希表 + 有序集合 `SortedList`，记录各个个数',
                 '`heappush_max`/`heappop_max` 是 Python 3.14 新函数，视频里在 setup 补了等价实现'],
    ),
)

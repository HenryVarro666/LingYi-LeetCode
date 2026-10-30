def _hpline(S):
    if 'now' not in S:
        return ''
    return f"当前血量 `now` = =={S['now']}==" + ('' if S['now'] > 0 else '　≤ 0，撑不住了 → 要移动一个怪物')


CONFIG = dict(
    num='LCP 30', title='魔塔游戏', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='堆维护走过的怪物 · 血量 ≤ 0 就移走最狠的',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1900'],
    code='''
class Solution(object):
    def magicTower(self, nums):

        if sum(nums) < 0:
            return -1

        heap = []
        now = 1
        res = 0
        for num in nums:
            now += num
            if num < 0:
                heapq.heappush(heap, num)
                if now <= 0:
                    now -= heapq.heappop(heap)
                    res += 1
        
        return res
''',
    call='Solution().magicTower([10,-8,-3,-5,2,-6,25])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（红 = 怪物，蓝箭头 = 当前房间）', pointers={'nums.index(num)': 'blue'}, cell=90,
             color=lambda S, i, v: 'red' if v < 0 else 'green', h=230),
        dict(type='text', fn=_hpline, size=30, h=60),
        dict(type='heap', var='heap', label='heap（走过的怪物，堆顶 = 负得最多）', top_color='red', h=140),
    ],
    watch=[('num', 'num', 'blue'), ('now', 'now', 'green'), ('res', 'res', 'orange')],
    captions={
        'if sum(nums) < 0': lambda S, B, r: (f'所有房间都要走到：总和 `{sum(S.nums)}` < 0，血量最终必 ≤ 0 → ==返回 -1=='
                                            if sum(S.nums) < 0 else
                                            f'总和 `{sum(S.nums)}` ≥ 0，到末尾血量不会不够，往下走'),
        'heap = []': '堆里放走过的负数房间（怪物）',
        'now = 1': '`now` 表示当前血量，初始 `1`',
        'res = 0': '`res` 统计移动次数',
        'for num in nums': lambda S, B, r: ('所有房间都走完了' if B.get('num') == S.num and S.num == S.nums[-1] else f'走进房间 `{S.num}`'),
        'now += num': '不管正负，先加上：`now` {B.now} → =={now}==',
        'if num < 0': lambda S, B, r: (f'`{S.num}` 是怪物，要记下来' if S.num < 0 else f'`{S.num}` 是正数（或 0）：无条件加进血量，不会撑不住'),
        'heapq.heappush(heap, num)': '怪物 `{num}` 放进堆：以后需要时可以挪走它',
        'if now <= 0': lambda S, B, r: (f'`now = {S.now} ≤ 0`：撑不住了，要把之前某个怪物挪到最后' if S.now <= 0
                                        else f'`now = {S.now} > 0`：还撑得住'),
        'now -= heapq.heappop(heap)': lambda S, B, r: (f'挪==负得最多==的 `{B.heap[0]}`：同样一次操作，保有的血量最多；`now` → =={S.now}=='
                                                        + ('（就是刚走进的这个）' if B.heap[0] == S.num else '')),
        'res += 1': '移动了一次：`res` = =={res}==',
        'return res': '最少移动 =={ret}== 次',
    },
    max_steps=90,
    cards=dict(
        one_liner='血量 ≤ 0 时，把走过的最大怪物移到最后，血量补回来',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums[i]` 正数补血、负数扣血，初始血量 `1`，血量始终要为正',
                 '每次可把一个怪物房间挪到末尾，求最少次数，不行返回 `-1`',
                 '本视频：`[10,-8,-3,-5,2,-6,25]` → `2`'],
        quote='在这里显然应该移动负的最多的那个，因为在相同的操作次数下保有的血量是最多的。',
        quote_src='—— yiduobo 题解原文',
        idea=['所有房间都要走到：总和 `< 0` 直接 `-1`',
              '遍历时 `now += num`；负数同时进堆，`now <= 0` 就==从堆里去掉最负的那个==',
              '作者强调：只需从 `now` 里减去堆顶，==并不需要真的移动==，因为走到末尾时血量一定充足'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '判断条件是 `now <= 0`（血量要为正）',
                 '原文用到 `heapq`，引擎已注入，无需 import；其余写法与原文一致',
                 '对比灵神：灵神是先 `hp += x` 再判 `hp < 1`，写在 `if x < 0` 外面，yiduobo 写在里面'],
    ),
)

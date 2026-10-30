def _i(S):
    return S['nums'].index(S['x']) if 'x' in S and S['x'] in S['nums'] else None


def _hpline(S):
    if 'hp' not in S:
        return ''
    ok = S['hp'] >= 1
    return f"血量 `hp` = =={S['hp']}==" + ('' if ok else '　< 1，撑不住了 → 要反悔')


CONFIG = dict(
    num='LCP 30', title='魔塔游戏', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='反悔堆（扣血太多就把最大的扣血挪到末尾）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1900'],
    code='''
class Solution:
    def magicTower(self, nums: List[int]) -> int:
        if sum(nums) < 0:
            return -1
        ans = 0
        hp = 1
        h = []
        for x in nums:
            if x < 0:
                heappush(h, x)
            hp += x
            if hp < 1:
                # 这意味着 x < 0，所以前面必然会把 x 入堆
                # 所以堆必然不是空的，并且堆顶 <= x
                hp -= heappop(h)  # 反悔
                ans += 1
        return ans
''',
    call='Solution().magicTower([10,-8,-3,-5,2,-6,25])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（红 = 怪物，蓝箭头 = 当前房间）', pointers={'nums.index(x)': 'blue'}, cell=90,
             color=lambda S, i, v: 'red' if v < 0 else 'green', h=230),
        dict(type='text', fn=_hpline, size=30, h=60),
        dict(type='heap', var='h', label='h（访问过的怪物，堆顶 = 扣血最多）', top_color='red', h=140),
    ],
    watch=[('x', 'x', 'blue'), ('hp', 'hp', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'if sum(nums) < 0': lambda S, B, r: (f'总和 `{sum(S.nums)}` < 0：全部怪物挪到末尾血量也不够 → ==返回 -1=='
                                            if sum(S.nums) < 0 else
                                            f'总和 `{sum(S.nums)}` ≥ 0：把怪物都挪到末尾也能活到最后，有解'),
        'ans = 0': '`ans` 记录挪动次数',
        'hp = 1': '初始血量 `1`',
        'h = []': '`h` 小根堆：存走过的怪物（负数），堆顶 = ==扣血最多的那个==',
        'for x in nums': lambda S, B, r: ('所有房间都走完了' if B.get('x') == S.x and S.x == S.nums[-1] else f'进入房间 `{S.x}`'),
        'if x < 0': lambda S, B, r: (f'`{S.x} < 0`：是怪物' if S.x < 0 else f'`{S.x} ≥ 0`：补血或空房间，不用记'),
        'heappush(h, x)': '先记下这个怪物 `{x}`：以后撑不住，可以把它==反悔==挪到末尾',
        'hp += x': '先照常走：`hp` {B.hp} → =={hp}==',
        'if hp < 1': lambda S, B, r: (f'`hp = {S.hp} < 1`：撑不住了，要反悔' if S.hp < 1
                                      else f'`hp = {S.hp} ≥ 1`：还活着，继续走'),
        'hp -= heappop(h)': lambda S, B, r: (f'反悔：堆里扣血最多的是 `{B.h[0]}`' + ('，正好是当前这个怪物自己' if B.h[0] == S.x else '，比当前的更狠，挪它更划算')
                                             + f'，挪到末尾，扣掉的血加回来：`hp` → =={S.hp}=='),
        'ans += 1': '挪了一次：`ans` = =={ans}==',
        'return ans': '走完所有房间，最少挪动 =={ret}== 次',
    },
    max_steps=90,
    cards=dict(
        one_liner='先照常走，血量掉到 1 以下就反悔：把扣血最多的怪物挪到末尾',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums[i]` 正数补血、负数扣血，初始血量 `1`，按顺序走要保证血量始终为正',
                 '每次可把一个怪物房间挪到末尾，求最少挪几次，不行返回 `-1`',
                 '本视频：`[10,-8,-3,-5,2,-6,25]` → `2`'],
        quote='遍历数组，能加血就尽管加血，要扣血就直接扣血，但如果血量小于 1，我们就「反悔」：从前面的扣血中，拿出一个扣血量最大的数（最小的负数），移到数组的末尾，把之前扣掉的血重新加回来。',
        quote_src='—— 灵茶山艾府题解',
        idea=['总和 `< 0` 一定无解；否则把怪物全挪到末尾最后血量必为正',
              '走的时候==把怪物都扔进小根堆==，血量 `< 1` 就弹出堆顶（扣血最多）加回血',
              '不用真的挪到末尾：总和 `≥ 0`，末尾血量必然够'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`hp < 1` 一定是当前 `x < 0` 导致的，所以堆非空，且堆顶 `≤ x`，弹出后血量必回到正数',
                 '易错：先 `sum(nums) < 0` 判无解；挪动次数只统计弹出的次数',
                 '同类：反悔堆（§5.5）、反悔贪心（§1.9）'],
    ),
)

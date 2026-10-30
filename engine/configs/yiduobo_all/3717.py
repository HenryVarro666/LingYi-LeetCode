CONFIG = dict(
    num=3717, title='Minimum Operations to Make the Array Beautiful', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='滚动 dict DP · 枚举 x 的倍数',
    tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        ma = max(nums)
        f = {nums[0]: 0}
        for v in nums[1:]:
            g = {}
            for x in f:
                g[x] = f[x]
            f = {}

            for x in g:
                t = x
                while t < v:
                    t += x
                
                while t <= ma + x:
                    cost = g[x] + t - v
                    if t not in f or f[t] > cost:
                        f[t] = cost
                    t += x

        return min(f.values())
''',
    call='Solution().minOperations([3,8,12])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=150),
        dict(type='map', var='g', label='g（上一轮：末尾值 x → 最少操作）', fmt=lambda k, v: f'{k}: {v}', h=150, font=30),
        dict(type='map', var='f', label='f（本轮：末尾值 t → 最少操作）', fmt=lambda k, v: f'{k}: {v}', h=190, font=30),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"当前 `v={S['v']}`，上一个值 `x={S['x']}`，候选 `t={S['t']}`" if all(k in S for k in ('v', 'x', 't')) else '')),
    ],
    watch=['v', 'x', 't', 'cost'],
    max_steps=120,
    captions={
        'ma = max': '`ma = {ma}`：枚举 t 的上限是 `ma + x`',
        'f = {nums[0]: 0}': '第 0 个元素保持不变，操作数 0：`f = {f}`',
        'for v in nums[1:]': '处理下一个元素 `v = {v}`（它只能被增加）',
        'g[x] = f[x]': '把上一轮的状态复制到 `g`：`g[{x}] = {g[x]}`',
        'g = {}': '`g` 清空，准备接收上一轮状态',
        'f = {}': '`f` 清空，准备装本轮状态',
        'for x in g': '假设前一个元素最终为 `x = {x}`，它此前最少花 `{g[x]}` 次操作',
        't = x': '`t` 从 `x` 开始，找 `≥ v` 且是 `x` 的倍数的最小值',
        'while t < v': '`t = {t}` 是否小于 `v = {v}`？ → ' + '{"是，加 x 继续找" if t < v else "否，已经 ≥ v"}',
        't += x': '`t` 增加 `x`：{t}',
        'while t <= ma + x': '`t = {t} <= ma + x = {ma + x}`？ → ' + '{"在上限内，继续" if t <= ma + x else "超过上限，换下一个 x"}',
        'cost =': '把 `v` 加到 `t`：花 `t − v = {t - v}`，加上之前 `{g[x]}` → `cost = {cost}`',
        'if t not in f': '`f[{t}]` ' + '{"还没有，或旧值更大 → 更新" if t not in f or f[t] > cost else "已有更小的 " + str(f[t]) + "，不更新"}',
        'f[t] = cost': '`f[{t}] = {cost}`',
        'return min': '最后一个元素所有可能末值里取最小 → `{ret}`',
    },
    cards=dict(
        one_liner='贪心会错，改用 DP：f[x] 表示最后一个数变成 x 的最少操作',
        complexity='时间约 `O(n · V · log V)`（V 为值域），空间 `O(V)`',
        problem=['数组中从下标 1 起，每个元素都能被前一个整除，就是美丽数组',
                 '一次操作可把下标 `>= 1` 的某个元素 `+1`，求最少操作数',
                 '本视频：`[3,8,12]` → `4`（变成 `[3,12,12]`）'],
        quote='无法直接通过策略决定每个元素应该去适配其左侧的元素还是去适配其右侧的元素，因此需要使用动态规划进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心：`[3,8,12]` 变 `[3,9,18]` 要 7 次，而 `[3,12,12]` 只要 4 次',
              '`f[x]`：前缀变美丽，且末尾为 `x` 的最少操作',
              '转移：找 `≥ v` 的 `x` 的倍数 `t`，用 `f[x] + t − v` 更新 `f[t]`',
              '滚动数组省掉下标这一维，答案取 `min(f.values())`'],
        summary=['枚举上限 `ma + x` 作者自己也说没有严谨证明',
                 '`f` 与 `g` 滚动：每轮先把旧 `f` 复制成 `g` 再清空',
                 '更新前要判断 `t not in f or f[t] > cost`，保留最小值',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改；题面库里缺失，按文章撰写'],
    ),
)

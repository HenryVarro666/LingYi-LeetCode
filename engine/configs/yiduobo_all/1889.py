CONFIG = dict(
    num=1889, title='装包裹的最小浪费空间', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='箱子排序 + 单调指针 + 前缀和',
    tags=['贪心与思维', '双序列配对', '难度分 2214'],
    code='''
class Solution(object):
    def minWastedSpace(self, packages, boxes):

        box_info = []
        m = len(boxes)
        for index in range(m):
            for v in boxes[index]:
                box_info.append([v, index])
        
        box_info = sorted(box_info, key=lambda d:d[0])
        
        n = len(packages)
        sorted_packages = sorted(packages)
        s = [sorted_packages[0]]
        for package in sorted_packages[1:]:
            s.append(s[-1] + package)
        
        dealed = [-1] * m
        cost = [0] * m
        p = -1
        mod = 10 ** 9 + 7
        for v, index in box_info:
            while p + 1 < n and sorted_packages[p + 1] <= v:
                p += 1
            
            if p > dealed[index]:
                cnt = p - dealed[index]
                cost[index] += cnt * v - s[p]
                if dealed[index] >= 0:
                    cost[index] += s[dealed[index]]
                dealed[index] = p

        res = -1
        for index in range(m):
            if dealed[index] == n - 1 and (res == -1 or res > cost[index]):
                res = cost[index]
        
        if res != -1:
            res %= mod

        return res
''',
    call='Solution().minWastedSpace([2,3,5], [[4,8],[2,8]])',
    expect=6,
    max_steps=120,
    skip=['m = len(boxes)', 'mod = ', 'n = len(packages)', 'cost = [0] * m', 'p = -1', 's.append'],
    views=[
        dict(type='text', h=60, fn=lambda S: ('所有箱子 [尺寸, 供应商]：`' + str(S['box_info']) + '`') if 'box_info' in S else ''),
        dict(type='array', var='sorted_packages', label='排好序的包裹（p 指向已被覆盖的最右包裹）', h=150, pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if 'p' in S and i <= S['p'] else None),
        dict(type='array', var='dealed', label='dealed[组]：该组已处理到的包裹下标', h=120),
        dict(type='array', var='cost', label='cost[组]：该组累计浪费', h=120),
        dict(type='array', var='s', label='前缀和 s', h=110),
    ],
    watch=['v', 'index', ('p', 'p', 'blue'), 'cnt', ('res', 'res', 'green')],
    captions={
        'box_info.append': '把箱子 `{v}` 连同所属供应商 `{index}` 一起记下',
        'box_info = sorted': '所有箱子按尺寸从小到大排序：`{box_info}`',
        'sorted_packages = sorted': '包裹也从小到大排序：`{sorted_packages}`',
        's.append': '前缀和：`s` = {s}，后面用它快速求一段包裹的尺寸和',
        'dealed = [-1]': '`dealed[组]` = 该组已经处理到的最右包裹下标，初始 -1 = 还没处理',
        'while p + 1 < n': lambda S, B, r: (f'包裹 `{S.sorted_packages[S.p + 1]}` ≤ 箱子 `{S.v}` → 这个箱子能装，`p` 右移' if S.p + 1 < S.n and S.sorted_packages[S.p + 1] <= S.v else f'下一个包裹装不下（或已到头）→ 箱子 `{S.v}` 最多装到下标 `{S.p}`'),
        'p += 1': '`p` → {p}：包裹 [0..{p}] 都能装进 ≤ {v} 的箱子（p 只增不减，总共 O(n)）',
        'if p > dealed[index]': lambda S, B, r: (f'第 {S.index} 组之前处理到 `{S.dealed[S.index]}`，现在能到 `{S.p}` → 中间这段归当前箱子' if S.p > S.dealed[S.index] else f'第 {S.index} 组没有新包裹要装，跳过'),
        'cnt = ': '这个箱子要装 `{cnt}` 个包裹（下标 {dealed[index] + 1}..{p}）',
        'cost[index] += cnt * v': '浪费 += `{cnt}×{v} − s[{p}]`（包裹尺寸和）→ `cost[{index}] = {cost[index]}`',
        'cost[index] += s[': '前缀和多减了前面已处理的部分，补回 `s[{dealed[index]}]` → `cost[{index}] = {cost[index]}`',
        'dealed[index] = p': '第 {index} 组处理到 `{p}`：`dealed = {dealed}`',
        'if dealed[index] == n - 1': lambda S, B, r: (f'第 {S.index} 组处理到最后一个包裹，且浪费 `{S.cost[S.index]}` 更小 → 更新答案' if S.dealed[S.index] == S.n - 1 and (S.res == -1 or S.res > S.cost[S.index]) else (f'第 {S.index} 组没处理完所有包裹（装不下最大的）→ 忽略' if S.dealed[S.index] != S.n - 1 else f'第 {S.index} 组 `{S.cost[S.index]}` 不比当前答案小 → 不更新')),
        'res = cost[index]': '`res = {res}`',
        'res %= mod': '最后取余：`res = {res}`',
        'return res': '浪费空间最小 `{ret}`',
    },
    cards=dict(
        one_liner='箱子排序后用单调指针，一次扫完所有供应商',
        complexity='时间 `O(n log n + M log M)`，空间 `O(n + M)`',
        problem=['每个箱子装一个包裹，只能选一个供应商，箱子无限多',
                 '浪费 = 箱子尺寸 − 包裹尺寸，求总浪费最小，装不下返回 `-1`',
                 '示例：`[2,3,5]`，`[[4,8],[2,8]]` → `6`'],
        quote='为了使浪费的空间最小，很明显就应该选择容量最小的，但大于等于包裹大小的箱子。',
        quote_src='—— yiduobo 题解原文',
        idea=['所有箱子打上供应商标记后一起排序，包裹也排序',
              '指针 `p` 只增不减：当前箱子能装下到 `p` 的所有包裹',
              '`dealed[组]` 记录该组之前已经管到哪，新增的 `(dealed, p]` 这段就归当前箱子',
              '这段浪费 = `cnt × v` − 这段包裹尺寸和，用前缀和 `O(1)` 求'],
        summary=['时间 `O(n log n + M log M)`（排序为主），空间 `O(n + M)`',
                 '易错点：`dealed[index] == n - 1` 才说明该组能装下所有包裹',
                 '前缀和 `s[p] - s[dealed]` 的写法在代码里拆成了两步（先减 `s[p]`，再加回 `s[dealed]`）',
                 '原文为 Python 2 风格，除 `class Solution(object)` 外无需改动，代码一字未改',
                 '对比灵神：灵神对每个箱子二分，yiduobo 用单调指针合并所有箱子'],
    ),
)

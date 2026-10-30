CONFIG = dict(
    num=1345, title='跳跃游戏 IV', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='BFS + dict 记录同值位置（用完即删）',
    tags=['难度分 1810'],
    code='''
class Solution(object):
    def minJumps(self, arr):

        n = len(arr)
        if n == 1:
            return 0

        num_dict = {}
        for index, num in enumerate(arr):
            if num not in num_dict:
                num_dict[num] = []
            num_dict[num].append(index)
        
        
        q = [0]
        l = 0
        r = 1
        used = [False] * n
        used[0] = True

        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                if now >= 1 and not used[now - 1]:
                    q.append(now - 1)
                    used[now - 1] = True
                if now < n - 1 and not used[now + 1]:
                    q.append(now + 1)
                    used[now + 1] = True
                if arr[now] in num_dict:
                    for p in num_dict[arr[now]]:
                        if not used[p]:
                            q.append(p)
                            used[p] = True
                    num_dict.pop(arr[now])
                    
                if used[n - 1]:
                    return step

            l, r = r, len(q)
''',
    call='Solution().minJumps([7, 6, 9, 6, 9, 6, 9, 7, 5, 8])',
    expect=3,
    views=[
        dict(type='array', var='arr', label='arr（绿 = used；蓝 = 当前位置 now）', cell=70, h=170, pointers={'now': 'blue'},
             color=lambda S, i, v: ('blue' if i == S.get('now') else 'green' if S['used'][i] else None) if 'used' in S else None),
        dict(type='map', var='num_dict', label='num_dict（数值 → 位置列表）', h=170, font=24),
        dict(type='array', var='q', label='q（BFS 队列；蓝框 = 本轮 [l, r)）', cell=56, h=150,
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', lambda S: S['r'] - 1)),
        dict(type='text', h=60, fn=lambda S: f"当前轮次 `step` = =={S['step']}==" if 'step' in S else ''),
    ],
    watch=[('step', 'step', 'green'), ('now', 'now', 'blue'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), 'n'],
    captions={
        'if n == 1': lambda S, B, r: ('只有一个元素，已经在终点 → 0 步' if S.n == 1 else f'`n = {S.n} > 1`，需要搜索；终点下标是 `{S.n - 1}`'),
        'q = [0]': '先扫一遍建好 `num_dict`（见左图）。从位置 `0` 开始 BFS，队列 `q = [0]`',
        'l = 0': '`[l, r)` 是本轮要处理的队列区间',
        'used = [False]': '`used[i]` 记录位置 i 有没有入过队',
        'used[0] = True': '起点已经使用',
        'step = 0': '`step` 记录 BFS 轮次（= 已走步数）',
        'step += 1': '新的一轮：本轮每个位置再走一步 → `step = {step}`',
        'if now >= 1 and': lambda S, B, r: (f'向左：`{S.now - 1}` 没越界、没用过 → 入队' if S.now >= 1 and not B.used[S.now - 1]
                                           else (f'`now = 0` 不能向左' if S.now < 1 else f'向左：`{S.now - 1}` 已经用过')),
        'if now < n - 1 and': lambda S, B, r: (f'向右：`{S.now + 1}` 没越界、没用过 → 入队' if S.now < S.n - 1 and not B.used[S.now + 1]
                                              else (f'`now` 已是最右，不能向右' if S.now >= S.n - 1 else f'向右：`{S.now + 1}` 已经用过')),
        'if arr[now] in num_dict': lambda S, B, r: (f'`arr[{S.now}] = {S.arr[S.now]}` 的同值跳转还没用过 → 枚举所有同值位置 `{S.num_dict[S.arr[S.now]]}`'
                                                    if S.arr[S.now] in S.num_dict else f'`{S.arr[S.now]}` 的同值跳转已经用过，不再重复'),
        'for p in num_dict': '枚举同值位置 `p`',
        'if not used[p]': lambda S, B, r: (f'`p = {S.p}` 没用过 → 一步跳过去，入队' if not B.used[S.p] else f'`p = {S.p}` 已经用过，跳过'),
        'num_dict.pop': '同值位置全部处理完，把 `{arr[now]}` 从 dict 删掉：以后不会再做这个值的跳转',
        'if used[n - 1]': lambda S, B, r: (f'终点 `{S.n - 1}` 已经被走到 → 当前轮次 `step = {S.step}` 就是答案' if S.used[S.n - 1]
                                          else '终点还没走到，继续下一个位置'),
        'return step': '返回 =={step}==',
        'l, r = r, len(q)': '本轮结束，下一轮处理 `[{l}, {r})`',
    },
    skip=['num_dict[num].append', 'num_dict = {}', 'q.append', 'used[now - 1] = True', 'used[now + 1] = True', 'used[p] = True', 'if num not in num_dict', 'num_dict[num] = []', 'for index, num in enumerate'],
    max_steps=70,
    cards=dict(
        one_liner='同值跳转只需要执行一次，用完就从 dict 里删掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从下标 0 出发，每步可到 `i-1`、`i+1`，或任意 `arr[j] == arr[i]` 的位置 `j`',
                 '求到达最后一个位置的最少步数',
                 '本视频：`[7,6,9,6,9,6,9,7,5,8]` → `3`（0→7→8→9）'],
        quote='对于数值相同的跳转，只有执行一次的必要。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍，用 dict 存下「数值 → 位置列表」',
              '从 `0` 开始 BFS：向左、向右、同值跳转，三种走法都算一步',
              '同值跳转枚举完所有位置后，把这个数值从 dict 删掉，避免重复枚举'],
        summary=['时间 `O(n)`：每个位置至多入队一次，dict 里每个位置至多被枚举一次',
                 '`n == 1` 要单独返回 0',
                 '向右走保证必有解，所以不用考虑 `-1`',
                 '这里在入队后（而不是出队时）检查 `used[n-1]`，所以返回的 `step` 就是轮次',
                 '原文为 Python 2 风格，代码无需改动，逐字照搬'],
    ),
)

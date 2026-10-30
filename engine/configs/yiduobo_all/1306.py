CONFIG = dict(
    num=1306, title='跳跃游戏 III', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='BFS 从 start 出发', tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 1397'],
    code='''
class Solution(object):
    def canReach(self, arr, start):

        n = len(arr)
        used = [False] * n
        used[start] = True
        q = [start]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            if arr[now] == 0:
                return True
            l += 1
            if now - arr[now] >= 0 and not used[now - arr[now]]:
                q.append(now - arr[now])
                used[now - arr[now]] = True
                r += 1
            if now + arr[now] < n and not used[now + arr[now]]:
                q.append(now + arr[now])
                used[now + arr[now]] = True
                r += 1
            
        return False
''',
    call='Solution().canReach([4,2,3,0,3,1,2], 5)',
    expect=True,
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 已进过队列，蓝箭头 = 正在处理的 now，绿 = 目标 0）', cell=100, h=230,
             pointers={'now': 'blue'},
             color=lambda S, i, v: 'green' if v == 0 else ('blue' if S.get('used') and S['used'][i] else None)),
        dict(type='array', var=lambda S: S.get('q'), label='q（BFS 队列，l 指向下一个出队的）', cell=90, h=200,
             pointers={'l': 'blue'}, dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='text', h=70, fn=lambda S: (f"`now = {S['now']}`，`arr[now] = {S['arr'][S['now']]}` → 往前 `{S['now'] - S['arr'][S['now']]}`，往后 `{S['now'] + S['arr'][S['now']]}`"
                                               if 'now' in S else '')),
    ],
    watch=['start', 'now', 'l', 'r'],
    captions={
        'used = [False]': '`used[i]` 记录下标 i 有没有进过队列',
        'used[start] = True': '起点先标记已访问，放进队列：`q = [{start}]`',
        'while l < r': lambda S, B, r: ('队列里还有位置没试过，继续 bfs' if S.l < S.r else '队列空了：所有能跳到的位置都试过 → False'),
        'now = q[l]': '出队：取出位置 `now = {now}`',
        'if arr[now] == 0': lambda S, B, r: (f'`arr[{S.now}] = 0` → 跳到了 0，==返回 True=='
                                             if S.arr[S.now] == 0 else f'`arr[{S.now}] = {S.arr[S.now]}`，不是 0，试着往前、往后跳'),
        'if now - arr[now] >= 0': lambda S, B, r: (
            f'往前跳到 `{S.now - S.arr[S.now]}`：不越界且没访问过 → 入队' if (S.now - S.arr[S.now] >= 0 and not S.used[S.now - S.arr[S.now]])
            else f'往前跳到 `{S.now - S.arr[S.now]}`：越界或已访问 → 跳过'),
        'if now + arr[now] < n': lambda S, B, r: (
            f'往后跳到 `{S.now + S.arr[S.now]}`：不越界且没访问过 → 入队' if (S.now + S.arr[S.now] < S.n and not S.used[S.now + S.arr[S.now]])
            else f'往后跳到 `{S.now + S.arr[S.now]}`：越界或已访问 → 跳过'),
        'return False': '跳不到任何 0 → ==False==',
        'return True': '`start` 能跳到值为 0 的位置 → ==True==',
    },
    skip=['l += 1', 'r += 1', 'l = 0', 'r = 1', 'q = [start]', 'used = [False]'],
    cards=dict(
        one_liner='从 start 开始 BFS，每次往前或往后跳，跳到 0 就返回',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`arr` 非负，站在 `i` 可以跳到 `i + arr[i]` 或 `i - arr[i]`，不能出界',
                 '问能否从 `start` 跳到某个值为 0 的下标',
                 '示例：`arr=[4,2,3,0,3,1,2], start=5` → `true`'],
        quote='直接从start处开始进行bfs，每次都尝试往前跳或者往后跳。若当前不会跳出边界，且目的地没有被访问过，那么就目的地加入到bfs队列中。',
        quote_src='—— yiduobo 题解原文',
        idea=['队列放「还要扩展的位置」，`used` 保证每个位置只进一次队',
              '每次出队先看 `arr[now]` 是不是 0，是就直接返回 True',
              '否则往前、往后各试一步，合法且没访问过才入队'],
        summary=['时间 `O(n)`：每个位置最多入队一次',
                 '空间 `O(n)`：`used` 和队列 `q`',
                 '入队时就标记 `used`，避免重复入队',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '灵神用递归 DFS，思路相同，只是遍历顺序不同'],
    ),
)

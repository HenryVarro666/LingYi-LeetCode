B = 2


def _now(S):
    return S.get('now')


def _fnow(S):
    now = S.get('now')
    f = S.get('f')
    if now is None or f is None:
        return None
    return f[now]


def _info(S):
    now = S.get('now')
    if now is None:
        return '`f[now][b][pre_buy]`：now 子树预算 b、父节点买(1)/没买(0) 的最大收益；从叶子往上算'
    return f"员工 `{now}`：价格 `{S.present[now - 1]}`，明天 `{S.future[now - 1]}`；父节点买了就半价 `{S.present[now - 1] // 2}`"


_cnt = {}


def _cap_for(S, B, ret):
    now = B['now']
    k = _cnt.get(now, 0)
    _cnt[now] = k + 1
    ups = {1: [], 2: [1]}[now]
    if k < len(ups):
        return f'员工 `{ups[k]}` 是 `{now}` 的上司：把 `f[{now}]` 当一个物品组并入上司的背包'
    return f'`{now}` 没有（更多）上司了，这个员工处理完'


CONFIG = dict(
    num=3562, title='折扣价交易股票的最大利润', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP + 分组背包（拓扑序自底向上）',
    tags=['灵神题单', '难度分 2458'],
    code='''
class Solution(object):
    def maxProfit(self, n, present, future, hierarchy, budget):
        
        t = [[] for _ in range(n + 1)]
        ind = [0] * (n + 1)
        for x, y in hierarchy:
            t[y].append(x)
            ind[x] += 1
        
        q = deque()
        f = [[[0] * 2 for _ in range(budget + 1)] for _ in range(n + 1)]
        g = [[0] * (budget + 1) for _ in range(n + 1)]
        h = [[0] * (budget + 1) for _ in range(n + 1)]
        for index in range(1, n + 1):
            if ind[index] == 0:
                q.append(index)

        while q:
            now = q.popleft()
            for pre_buy in range(2):
                buy_cost = present[now - 1] // (pre_buy + 1)
                buy_reward = future[now - 1] - buy_cost

                for b in range(budget + 1):
                    f[now][b][pre_buy] = g[now][b]
                    if b >= buy_cost:
                        f[now][b][pre_buy] = max(f[now][b][pre_buy], h[now][b - buy_cost] + buy_reward)

            for pre in t[now]:
                ind[pre] -= 1
                if ind[pre] == 0:
                    q.append(pre)
                
                for b in range(budget, -1, -1):
                    for sub in range(b + 1):
                        g[pre][b] = max(g[pre][b], g[pre][b - sub] + f[now][sub][0])
                
                for b in range(budget - present[pre - 1] // 2, -1, -1):
                    for sub in range(b + 1):
                        h[pre][b] = max(h[pre][b], h[pre][b - sub] + f[now][sub][1])
    
        return f[1][budget][0]
''',
    call='Solution().maxProfit(2, [1, 2], [4, 5], [[1, 2]], 2)',
    expect=7,
    skip=['f[now][b][pre_buy] = g', 'if b >= buy_cost', 'for index in range', 'for b in range', 'for sub in range', 'for pre_buy', 'buy_reward =', 'if ind[index]', 'q.append(index)', 'for x, y', 't[y]', 'ind[x]'],
    max_steps=70,
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='queue', var='q', label='队列 q（入度为 0 的员工，先处理叶子）', h=130),
        dict(type='table', var='g', label='g[员工][b]：now 不买时，下属们分到 b 预算的最大收益', h=190, cell=70,
             rows=lambda S: [f'员工{i}' for i in range(len(S['g']))], cols=[str(b) for b in range(B + 1)]),
        dict(type='table', var='h', label='h[员工][b]：now 买了时（下属半价），下属们分到 b 的最大收益', h=190, cell=70,
             rows=lambda S: [f'员工{i}' for i in range(len(S['h']))], cols=[str(b) for b in range(B + 1)]),
        dict(type='table', var=_fnow, label='f[now][b][pre_buy]：行=预算 b，列=父节点没买(0)/买了(1)', h=170, cell=70,
             rows=[str(b) for b in range(B + 1)], cols=['0', '1']),
    ],
    watch=[('now', 'now', 'blue'), ('pre', 'pre', 'pink'), ('pre_buy', 'pre_buy', 'yellow'), ('buy_cost', 'buy_cost', 'orange')],
    captions={
        'q = deque()': '队列里放「所有下属都算完」的员工，先放入度为 0 的叶子',
        'f = [[[0]': '`f[now][b][pre_buy]` 三维：员工 × 预算 × 父节点买没买',
        'now = q.popleft()': '取出员工 `{now}`：它的下属都已经并入 `g`/`h`，可以算 `f[{now}]` 了',
        'buy_cost = present': '`pre_buy={pre_buy}`：价格 `{present[now-1]} // {pre_buy+1} = {buy_cost}`（父节点买了才半价）',
        'f[now][b][pre_buy] = max': '预算 `b={b}`：不买 = `g[{now}][{b}] = {g[now][b]}`；买 = `h[{b}-{buy_cost}] = {h[now][b-buy_cost]}` + 收益 `{buy_reward}`；取大 → `f[{now}][{b}][{pre_buy}] = {f[now][b][pre_buy]}`',
        'for pre in t[now]': _cap_for,
        'ind[pre] -= 1': '上司 `{pre}` 还剩 `{ind[pre]}` 个下属没算完',
        'if ind[pre] == 0': '`ind[{pre}] = {ind[pre]}`：=={"下属全算完 → 入队" if ind[pre] == 0 else "还要等别的下属"}==',
        'q.append(pre)': '上司 `{pre}` 入队，下一轮轮到它',
        'g[pre][b] = max': '上司不买：分 `sub={sub}` 给 `{now}`（它的父买=0），`g[{pre}][{b}] = {g[pre][b]}`',
        'h[pre][b] = max': '上司买了：`{now}` 可半价，分 `sub={sub}`，`h[{pre}][{b}] = {h[pre][b]}`（b 从 `budget-上司半价` 倒序，预留上司的钱）',
        'return f[1]': '答案：CEO 没有父节点，`f[1][{budget}][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='树形 DP：每个员工两种状态，孩子当分组背包并入',
        complexity='时间 `O(n·b^2)`，空间 `O(n·b)`',
        problem=['n 个员工组成一棵树，1 号是 CEO；买员工股票花 `present`，明天卖得 `future`',
                 '直属上级买了，自己就半价 `present // 2`',
                 '预算 `budget`，每支股只买一次，求最大收益',
                 '示例：`present=[1,2], future=[4,3], 1→2, budget=3` → `5`'],
        quote='令f[now][b][pre_buy]表示以now为根节点的子树中，如果有b的预算，且now的父亲节点购买状态为pre_buy时可以得到的最大收益，其中pre_buy为0表示父节点没买，为1则表示买了。',
        quote_src='—— yiduobo 题解',
        idea=['n 个点 n-1 条边且有根 → 一棵树；每个点「买/不买」二选一 → 树形 DP',
              '先算 now 不买：孩子们分预算，是背包问题，记为 `g[b]`；倒序遍历 b 省掉「第几个孩子」一维',
              '再算 now 买：先扣掉 `buy_cost`，孩子们用 `f[..][1]` 再做一遍背包，记为 `h[b]`',
              '递归版 Python 会超时，所以改成反向建图 + 拓扑序，自底向上'],
        summary=['时间 `O(n·b^2)`：每条边合并一次背包 `O(b^2)`',
                 '易错：`b` 必须倒序，否则同一个孩子被选多次',
                 '易错：买 now 时 `h` 要给 now 自己预留 `buy_cost`，所以 `b` 从 `budget - 半价` 起',
                 '拓扑序：入度 = 下属数，下属全算完才入队',
                 '另有灵神的「恰好 j」写法，把每个孩子当物品组，与此同源'],
    ),
)

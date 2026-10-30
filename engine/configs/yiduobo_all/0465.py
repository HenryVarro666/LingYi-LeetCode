CONFIG = dict(
    num=465, title='最优账单平衡', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='分正负两堆 · DFS 凑零',
    tags=['灵神题单', '状压 DP'],
    code='''
class Solution(object):
    def minTransfers(self, transactions):

        pos = {}
        neg = {}
        v = {}
        for x, y, z in transactions:
            if x not in v:
                v[x] = 0
            if y not in v:
                v[y] = 0
            v[x] -= z
            v[y] += z
        
        n = 0
        for u in v:
            if v[u] == 0:
                continue
            n += 1
            if v[u] > 0:
                pos[v[u]] = pos.get(v[u], 0) + 1
            else:
                neg[v[u]] = neg.get(v[u], 0) + 1

        global res
        res = n

        def dfs(level, now, cnt, pos, neg):
            global res
            if level == n:
                res = min(res, cnt)
                return

            if now == 0:
                delta = 0
            else:
                delta = 1

            if now <= 0:
                for num in pos:
                    if pos[num] > 0:
                        pos[num] -= 1
                        dfs(level + 1, now + num, cnt + delta, pos, neg)
                        pos[num] += 1
            else:
                for num in neg:
                    if neg[num] > 0:
                        neg[num] -= 1
                        dfs(level + 1, now + num, cnt + delta, pos, neg)
                        neg[num] += 1
        
            

        dfs(0, 0, 0, pos, neg)
        return res
''',
    call='Solution().minTransfers([[0,1,5],[2,3,5]])',
    expect=2,
    skip=['if x not in v', 'if y not in v', 'v[x] = 0', 'v[y] = 0', 'n += 1', 'if v[u] == 0', 'continue', 'delta = 0', 'delta = 1',
          'for num in pos', 'for num in neg', 'for x, y, z', 'for u in v', 'pos = {}', 'neg = {}', 'v = {}', 'n = 0', 'global res', 'else:'],
    views=[
        dict(type='map', var='v', label='v：每人净收支（正 = 该收钱，负 = 该付钱）', h=150, fmt=lambda k, x: f'{x:+d}'),
        dict(type='map', var='pos', label='pos：收钱人的金额 → 人数（还没用的）', h=150),
        dict(type='map', var='neg', label='neg：付钱人的金额 → 人数（还没用的）', h=150),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"已选 `{S['level']}` / `{S['n']}` 人，当前部分账目和 `now = {S['now']}`，交易数 `cnt = {S['cnt']}`"
                           if 'level' in S and 'now' in S else '')),
        dict(type='calls', h=230),
    ],
    watch=[('level', 'level', 'blue'), ('now', 'now', 'yellow'), ('cnt', 'cnt', 'pink')],
    captions={
        'v[x] -= z': '`{x}` 付出 `{z}`，`{y}` 收到 `{z}`：`v[{x}] = {v[x]}`',
        'v[y] += z': '`v[{y}] = {v[y]}`',
        'res = n': '先假设最坏：每人一次交易，`res = n = {n}`（上界）',
        'pos[v[u]] =': '收钱人 `{u}` 金额 `{v[u]}`：放进 `pos` → {pos}',
        'neg[v[u]] =': '付钱人 `{u}` 金额 `{v[u]}`：放进 `neg` → {neg}',
        'dfs(0, 0, 0': '开始 DFS：把所有人排成一串，每段和为 0 的就是一个独立部分',
        'if level == n': lambda S, B, r: (f'`level = {S.level} = n`：所有人都排完了 → ==更新答案==' if S.level == S.n
                                          else f'`level = {S.level} < n`，还有人没排，继续选'),
        'res = min(res, cnt)': '全排完了：这种分法的交易数就是 `cnt = {cnt}`，和已有最优取小',
        'if now == 0': lambda S, B, r: ('`now = 0`：账目和为 0 → 上一部分已平，新部分第一个人 ==不产生交易== (`delta = 0`)' if S.now == 0 else f'`now = {S.now} ≠ 0`：部分还没平，再加一个人就多一次交易 (`delta = 1`)'),
        'if now <= 0': lambda S, B, r: (f'`now = {S.now}`：账目和不为正 → 从 ==收钱的人==里选一个加入' if S.now <= 0
                                        else f'`now = {S.now} > 0`：账目和为正 → 从 ==付钱的人==里选一个加入'),
        'if pos[num] > 0': '`pos[{num}] = {pos[num]} > 0`：还有这个金额的人可选',
        'if neg[num] > 0': '`neg[{num}] = {neg[num]} > 0`：还有这个金额的人可选',
        'pos[num] -= 1': '选一个收 `{num}` 的人：`pos[{num}]` 减 1（回溯时再还回去）',
        'neg[num] -= 1': '选一个付 `{-num}` 的人：`neg[{num}]` 减 1（回溯时再还回去）',
        'dfs(level + 1, now + num, cnt + delta': '进入下一层：`now = {B.now}` 加上 `{num}`；==`now` 为 0 时上一部分已平，不加交易数==，否则 `cnt + 1`（这次 `cnt = {B.cnt + delta}`）',
        'pos[num] += 1': '回溯：把这个人放回 `pos`',
        'neg[num] += 1': '回溯：把这个人放回 `neg`',
        'return res': '最少交易次数 = ==`{res}`==',
    },
    cards=dict(
        one_liner='把人排成串，账目和归零就切一段：段越多，交易越少',
        complexity='DFS 指数级，`n` 很小（≤ 12）',
        problem=['`transactions[i] = [from, to, amount]` 表示 from 给 to 付了 amount 元',
                 '求清算所有债务所需的==最少转账次数==（只能点对点转账）',
                 '示例：`[[0,1,5],[2,3,5]]` → `2`'],
        quote='若总和为负，那么就选择一个收钱的人加入，反过来则选择一个给钱的人加入。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算每人净收支，为 0 的人不用管；其余分成收钱 `pos` 和付钱 `neg` 两堆',
              '一个和为 0 的部分有 `k` 个人，需要 `k - 1` 次交易 → 部分分得越多越省',
              '`now` 记录当前部分的账目和：为负选收钱的人、为正选付钱的人，每选一个交易数加 1',
              '`now == 0` 说明上一部分已平，换新部分的第一个人不算交易'],
        summary=['时间指数级（本题人数 ≤ 12），空间 `O(n)`',
                 '`delta` 在 `now == 0` 时为 0：每个部分的第一个人不产生交易，所以 `k` 人只算 `k - 1` 次',
                 '用「金额 → 人数」的字典代替人下标，相同金额的人只枚举一次，起到剪枝作用',
                 '对比灵神：灵神用状压 DP 枚举子集，`O(3^n)`；yiduobo 用 DFS 凑零',
                 '原文是 Python 2 风格，在 Python 3 下无需改动（`global res` 保留）'],
    ),
)

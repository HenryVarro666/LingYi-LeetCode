CONFIG = dict(
    num=1817, title='查找用户活跃分钟数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 + 集合去重 · 增量维护答案',
    tags=[],
    code='''
class Solution(object):
    def findingUsersActiveMinutes(self, logs, k):

        res = [0] * k
        used_minute = {}
        cnt_dict = {}
        for id, minute in logs:
            if id not in used_minute:
                used_minute[id] = set()
            if minute not in used_minute[id]:
                used_minute[id].add(minute)
                cnt_dict[id] = cnt_dict.get(id, 0) + 1
                if cnt_dict[id] == 1:
                    res[0] += 1
                else:
                    res[cnt_dict[id] - 2] -= 1
                    if cnt_dict[id] <= k:
                        res[cnt_dict[id] - 1] += 1
        
        return res
''',
    call='Solution().findingUsersActiveMinutes([[0,5],[1,2],[0,2],[0,5],[1,3]], 5)',
    expect=[0, 2, 0, 0, 0],
    views=[
        dict(type='text', fn=lambda S: (f"当前日志：用户 `{S['id']}` 在第 `{S['minute']}` 分钟活跃" if 'id' in S and 'minute' in S else 'logs[i] = [用户 id, 分钟]；res[j-1] = 活跃分钟数恰为 j 的用户数'), size=26, h=60),
        dict(type='array', var='logs', label='logs', h=215, cell=110,
             color=lambda S, i, v: 'blue' if 'id' in S and v == [S['id'], S['minute']] else None),
        dict(type='map', var='used_minute', label='used_minute（每个用户活跃过的分钟，集合去重）', h=190, fmt=lambda k, v: f'用户 {k}: {sorted(v)}'),
        dict(type='map', var='cnt_dict', label='cnt_dict（每个用户的活跃分钟数）', h=150, fmt=lambda k, v: f'用户 {k}: {v}'),
        dict(type='array', var='res', label='res（res[j-1] = 活跃分钟数恰为 j 的用户数）', h=200, cell=110),
    ],
    watch=['id', 'minute', ('res', 'res', 'green')],
    captions={
        'res = [0] * k': '`res` 长度为 `k = {k}`：`res[j-1]` 统计活跃分钟数恰好为 j 的用户数',
        'used_minute = {}': '`used_minute`：用户 → 他已活跃过的分钟集合（去重用）',
        'cnt_dict = {}': '`cnt_dict`：用户 → 当前活跃分钟数',
        'for id, minute in logs': lambda S, B, r: ('日志都处理完了，循环结束' if 'id' in B and (B.id, B.minute) == (S.id, S.minute)
                                                    else f'处理一条日志：用户 `{S.id}` 在第 `{S.minute}` 分钟活跃'),
        'if id not in used_minute': lambda S, B, r: (f'用户 `{S.id}` 第一次出现 → 先给他建一个空集合' if S.id not in B.used_minute
                                                      else f'用户 `{S.id}` 已有记录，不用新建'),
        'used_minute[id] = set()': '建好空集合 `used_minute[{id}]`',
        'if minute not in used_minute[id]': lambda S, B, r: (f'第 `{S.minute}` 分钟之前没记过 → ==新的活跃分钟=='
                                                              if S.minute not in S.used_minute[S.id]
                                                              else f'第 `{S.minute}` 分钟已经记过了 → ==同一分钟重复，忽略=='),
        'used_minute[id].add(minute)': '把 `{minute}` 加入用户 `{id}` 的集合',
        'cnt_dict[id] = cnt_dict.get': '用户 `{id}` 活跃分钟数 +1 → `{cnt_dict[id]}`',
        'if cnt_dict[id] == 1': lambda S, B, r: ('这是他的第 1 个活跃分钟 → 他以前不在任何一档里，直接加入第 1 档' if S.cnt_dict[S.id] == 1
                                                  else f'他已经活跃 `{S.cnt_dict[S.id]}` 分钟了 → 要从旧的一档挪到新的一档'),
        'res[0] += 1': '`res[0]` += 1：活跃 1 分钟的用户多了一个 → {res}',
        'res[cnt_dict[id] - 2] -= 1': '从旧的一档（活跃 `{cnt_dict[id] - 1}` 分钟）减去他：`res[{cnt_dict[id] - 2}]` -= 1 → {res}',
        'if cnt_dict[id] <= k': lambda S, B, r: (f'新的活跃分钟数 `{S.cnt_dict[S.id]}` ≤ k = {S.k} → 要记入新的一档' if S.cnt_dict[S.id] <= S.k
                                                 else f'新的活跃分钟数 `{S.cnt_dict[S.id]}` > k = {S.k} → 超出统计范围，不记'),
        'res[cnt_dict[id] - 1] += 1': '加入新的一档：`res[{cnt_dict[id] - 1}]` += 1 → {res}',
        'return res': '`res[j-1]` 就是活跃分钟数恰为 j 的用户数 → =={res}==',
    },
    cards=dict(
        one_liner='边读日志边维护答案：每个用户从一档挪到下一档',
        complexity='时间 `O(n)`，空间 `O(n)`（`n` 为日志条数）',
        problem=['`logs[i] = [id, time]`：用户 `id` 在第 `time` 分钟执行了操作；同一分钟的多次操作只算一次活跃分钟',
                 '返回长度为 `k` 的数组 `res`：`res[j]` 是活跃分钟数恰好为 `j+1` 的用户数',
                 '示例：`logs=[[0,5],[1,2],[0,2],[0,5],[1,3]]`，`k=5` → `[0,2,0,0,0]`'],
        quote='使用set来给每个用户活跃分钟数去重，然后使用哈希表统计每个用户活跃的分钟数目，并用这个数目更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个用户一个集合，同一分钟重复出现就跳过',
              '遇到新的活跃分钟，用户的分钟数 `c` 变成 `c+1`',
              '这时直接改答案：`res[c-1]` 减 1（离开旧档），`res[c]` 加 1（进入新档）——不用最后再遍历'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '下标偏移：活跃 `c` 分钟的用户在 `res[c-1]`，所以旧档是 `c-2`，新档是 `c-1`',
                 '分钟数超过 `k` 的用户只离开旧档，不进入任何档',
                 '原文为 Python 2 风格，本题无需改动，代码照搬原文'],
    ),
)

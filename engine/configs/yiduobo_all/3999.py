CONFIG = dict(
    num=3999, title='字符串变换后的最少分组数', difficulty='Hard', category='字符串',
    author='yiduobo', technique='循环移位取字典序最小 · 集合去重',
    tags=['灵神题单·字符串', '难度分 2162'],
    code='''
class Solution(object):
    def minimumGroups(self, words):
        
        vis = set()

        def reorder(arr):
            n = len(arr)
            arr.extend(arr)

            now = 0
            p = 1
            k = 0
            while p < n:
                if arr[now + k] == arr[p + k]:
                    k += 1
                    if k == n:
                        return arr[now:]
                elif arr[now + k] < arr[p + k]:
                    p += k + 1
                    k = 0
                else:
                    if arr[now] > arr[p + k]:
                        now = p + k
                        if now >= n:
                            return arr[p:p + n]
                    else:
                        now = p

                    p = now + 1
                    k = 0
            
            return arr[now: now + n]

        for w in words:
            E = []
            O = []
            for index, c in enumerate(w):
                if index % 2 == 0:
                    E.append(c)
                else:
                    O.append(c)
                    
            vis.add(''.join(reorder(E) + reorder(O)))

        return len(vis)
''',
    call='Solution().minimumGroups(["bbaab","aabbb","bbaaa"])',
    expect=2,
    views=[
        dict(type='array', var='arr', label='arr（E 或 O 复制一份拼在后面）：蓝 = now，粉 = p', pointers={'now': 'blue', 'p': 'pink'}, h=210, cell=64,
             color=lambda S, idx, v: ('blue' if idx == S.get('now') else 'pink' if idx == S.get('p') else None) if 'p' in S else None),
        dict(type='text', fn=lambda S: (f"对比 `arr[now+k]` 与 `arr[p+k]`：`now={S['now']}`，`p={S['p']}`，已相同 `k={S['k']}`" if 'k' in S and 'p' in S and 'now' in S else ''), h=70),
        dict(type='set', var='vis', label='vis（E、O 各自最小移位后拼接）', fmt=lambda x: x, h=120),
    ],
    watch=[('now', 'now', 'blue'), ('p', 'p', 'pink'), 'k', 'n', ('len(vis)', 'len(vis)', 'green')],
    captions={
        'n = len(arr)': '`n = {n}`：先记下原长度，再复制',
        'arr.extend(arr)': '把 `arr` 复制拼在自己后面：从任意位置取 `n` 个就是一种循环移位',
        'now = 0': '`now` 是目前字典序最小的起点',
        'p = 1': '`p` 是新的候选起点',
        12: '`k` 是 now、p 两段已经相同的长度',
        20: '`k` 清零，重新比较新的 now、p',
        30: '`k` 清零，重新比较新的 now、p',
        'while p < n': lambda S, B, r: f'`p = {S.p} < n = {S.n}`：还有候选起点' if S.p < S.n else f'`p = {S.p} >= n = {S.n}`：候选起点用完',
        'if arr[now + k] == arr[p + k]': lambda S, B, r: (f"`'{S.arr[S.now+S.k]}' == '{S.arr[S.p+S.k]}'` → 相同，继续比后一位" if S.arr[S.now+S.k] == S.arr[S.p+S.k] else f"`'{S.arr[S.now+S.k]}' != '{S.arr[S.p+S.k]}'` → 看谁更小"),
        'k += 1': '相同长度 `k` 增到 {k}',
        'if k == n': lambda S, B, r: (f'`k = {S.k} == n`：比满一圈，原串是周期串，`now` 开头就是最小的' if S.k == S.n else f'`k = {S.k} < n`：还没比满'),
        'return arr[now:]': '直接返回 `{ret}`',
        'elif arr[now + k] < arr[p + k]': lambda S, B, r: (f"`'{S.arr[S.now+S.k]}' < '{S.arr[S.p+S.k]}'` → now 更小" if S.arr[S.now+S.k] < S.arr[S.p+S.k] else f"`'{S.arr[S.now+S.k]}' > '{S.arr[S.p+S.k]}'` → p 这一侧更小"),
        'p += k + 1': 'now 更小：`p` 到 `p+k` 都不可能更优，`p` 跳到 {p}，`k` 清零',
        'if arr[now] > arr[p + k]': lambda S, B, r: (f"`arr[now] = '{S.arr[S.now]}' > arr[p+k] = '{S.arr[S.p+S.k]}'` → 直接把 `now` 跳到 `p+k`" if S.arr[S.now] > S.arr[S.p+S.k] else f"`arr[now] = '{S.arr[S.now]}'` 不大于 `arr[p+k]` → `now` 换成 `p`"),
        'now = p + k': '`now = p + k = {now}`：中间这些起点都比 now 差',
        'if now >= n': lambda S, B, r: (f'`now = {S.now} >= n = {S.n}`：起点跑出原串，直接取 `arr[p:p+n]`' if S.now >= S.n else f'`now = {S.now} < n`：还在原串里'),
        'return arr[p:p + n]': '返回 `{ret}`',
        27: '`now = p = {now}`',
        'p = now + 1': '`p` 重新从 `now + 1` 开始，`k` 清零',
        'return arr[now: now + n]': '最小移位：`{ret}`',
        'vis.add': 'E、O 各取最小移位后拼起来，加入集合 `vis`',
        'return len(vis)': '集合里有几种不同的规范形，就最少分几组：`{ret}`',
    },
    cards=dict(
        one_liner='循环移位成最小，同一组的串就变成同一个串',
        complexity='时间 `O(L)`，空间 `O(L)`，`L` 为所有字符串长度之和',
        problem=['把偶数位、奇数位两条子序列各自循环右移任意位，得到的串互相等价',
                 '把 `words` 分成最少的组，组内两两等价',
                 '本视频：`["bbaab","aabbb","bbaaa"]` → `2`'],
        quote='若两个字符串可以通过循环移动变为相同，那么这两个字符串通过循环移动得到的字典序最小的字符串也必然相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['拆成 `E`、`O` 两个字符串，各自移成字典序最小',
              '再拼回去放进集合，==集合大小就是答案==',
              '求最小移位：复制一份接在后面，找起点在原串内的==最小后缀==（和 1163 题同一套做法）'],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '`reorder` 会修改传入的 `arr`（`extend`），所以先记 `n`',
                 '`k == n` 说明是周期串；`now >= n` 说明最小起点已越过原串，取 `arr[p:p+n]`',
                 '对比灵神：灵神用 `i`、`j` 两指针 + `max(j, i+k)+1`；yiduobo 把后缀比较写成 `now/p/k` 三变量',
                 '同类题：1163 按字典序排在最后的子串'],
    ),
)

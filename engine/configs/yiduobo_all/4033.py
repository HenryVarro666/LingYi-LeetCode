CONFIG = dict(
    num=4033, title='有效 K 个不同元素子数组 I', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='双滑窗 + 满二叉树哈希前缀奇偶性',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·常用数据结构', '难度分 2314'],
    code='''
class Solution(object):
    def validSubarrays(self, nums, k, queries):
        n = len(nums)

        freq1 = {}
        freq2 = {}
        hit_k = []
        p1 = 0
        p2 = 0
        for index, v in enumerate(nums):
            if p1 < index:
                p1 = index
            while p1 < len(nums) and len(freq1) < k:
                freq1[nums[p1]] = freq1.get(nums[p1], 0) + 1
                p1 += 1

            if len(freq1) < k:
                hit_k.append([-1, -1])
                continue

            if p2 < index:
                p2 = index
            while p2 < len(nums) and len(freq2) < k + 1:
                freq2[nums[p2]] = freq2.get(nums[p2], 0) + 1
                p2 += 1

            hit_k.append([p1, p2 - 1])

            freq1[v] -= 1
            if freq1[v] == 0:
                freq1.pop(v)
            freq2[v] -= 1
            if freq2[v] == 0:
                freq2.pop(v)

        vid = {}
        m = 0
        for v in nums:
            if v not in vid:
                vid[v] = m
                m += 1

        p = 1
        while p < m:
            p <<= 1

        f = [0] * (p << 1)
        length = p
        nxt_id = p << 1
        node_dict = {}
        while length:
            for index in range(length, length << 1):
                if length < p:
                    node_dict[(f[index << 1], f[(index << 1) + 1])] = nxt_id
                    f[index] = nxt_id
                    nxt_id += 1
                else:
                    f[index] = (index - length) << 1
            length >>= 1

        prefix_id = [f[1]]
        for v in nums:
            index = vid[v] + p
            f[index] ^= 1
            while index > 1:
                brother = f[index ^ 1]
                if f[index] > brother:
                    key = (brother, f[index])
                else:
                    key = (f[index], brother)

                if key not in node_dict:
                    node_dict[key] = nxt_id
                    nxt_id += 1

                f[index >> 1] = node_dict[key]
                index >>= 1

            prefix_id.append(f[1])

        return [hit_k[x][0] <= y <= hit_k[x][1] and prefix_id[y + 1] == prefix_id[x] for x, y in queries]
''',
    call='Solution().validSubarrays([2,2,1], 1, [[0,1],[0,2],[1,2]])',
    expect=[True, False, False],
    views=[
        dict(type='array', var='nums', h=290, label='nums（蓝 = 当前 index，粉 = p1 / p2 窗口右端）',
             pointers={'index if _line < 38 else None': 'blue', 'p1 if _line < 38 else None': 'pink', 'p2 if _line < 38 else None': 'purple'},
             pointer_labels={'index if _line < 38 else None': 'index', 'p1 if _line < 38 else None': 'p1', 'p2 if _line < 38 else None': 'p2'},
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] and S['_line'] < 38 else None),
        dict(type='text', h=110, fn=lambda S: (f"`freq1 = {S['freq1']}`（至少 k 种的窗口）\n`freq2 = {S['freq2']}`（至少 k+1 种的窗口）" if 'freq1' in S and S['_line'] < 38 else '')),
        dict(type='array', var='f', h=260, label='f：满二叉树节点的哈希编号（下标 1 是根）', pointers={'index if _line > 50 else None': 'blue'}, pointer_labels={'index if _line > 50 else None': 'index'}),
        dict(type='array', var='prefix_id', h=170, label='prefix_id[j]：前 j 个数的奇偶状态编号'),
        dict(type='text', fn=lambda S: f"`hit_k = {S['hit_k']}`：每个左端点对应的右端点范围 `[p1, p2-1]`" if S.get('hit_k') else ''),
    ],
    watch=[('index', 'index', 'blue'), ('p1', 'p1', 'pink'), ('p2', 'p2', 'purple'), 'm', 'p', ('nxt_id', 'nxt_id', 'yellow')],
    skip=['f[index] = nxt_id', 'freq1[nums[p1]]', 'freq2[nums[p2]]', 'p = 1', 'm = 0', 'p1 += 1', 'p2 += 1', 'if p1 < index', 'if p2 < index', 'p1 = index', 'p2 = index', 'freq1.pop', 'freq2.pop', 'if freq1[v] == 0', 'if freq2[v] == 0', 'index >>= 1', 'while index > 1', 'if f[index] > brother', 'n = len(nums)', 'p <<= 1', 'nxt_id += 1', 'length >>= 1', 'if length < p', 'if v not in vid', 'for v in nums:\n        if', 'vid = {}', 'freq1 = {}', 'freq2 = {}', 'p1 = 0', 'p2 = 0', 'vid = {}', 'length = p'],
    max_steps=54,
    captions={
        'hit_k = []': '`hit_k[x]`：以 `x` 为左端点、恰好 k 种不同数字的右端点范围',
        'for index, v in enumerate(nums)': '第一遍：枚举左端点 `index = {index}`',
        'while p1 < len(nums) and len(freq1) < k': lambda S, B, r: (
            f'`freq1` 里只有 {len(S.freq1)} 种 < k={S.k}，把 `nums[{S.p1}]` 纳入窗口，`p1` 右移' if (S.p1 < len(S.nums) and len(S.freq1) < S.k)
            else f'`freq1` 已有 {len(S.freq1)} 种 >= k（或到末尾）：`p1` 停在「第 k 种数字刚进窗口」的下一格'),
        'if len(freq1) < k': lambda S, B, r: ('种类不够 k 种，这个左端点没有解 → 记 [-1, -1]' if len(S.freq1) < S.k else '种类够了，继续找 k+1 种的位置'),
        'while p2 < len(nums) and len(freq2) < k + 1': lambda S, B, r: (
            f'`freq2` 只有 {len(S.freq2)} 种 < k+1，纳入 `nums[{S.p2}]`，`p2` 右移' if (S.p2 < len(S.nums) and len(S.freq2) < S.k + 1)
            else f'`freq2` 已有 {len(S.freq2)} 种（或到末尾）：再往右就超过 k 种了'),
        'freq1[nums[p1]]': '`nums[{p1}]` 进入 `freq1`，`p1` 随后右移',
        'freq2[nums[p2]]': '`nums[{p2}]` 进入 `freq2`，`p2` 随后右移',
        'hit_k.append([p1, p2 - 1])': '右端点落在 `[p1, p2-1]` 里 → 恰好 k 种：记录 `{hit_k[-1]}`',
        'freq1[v] -= 1': '左端点右移，把 `{v}` 从 `freq1` 里扣掉一个',
        'freq2[v] -= 1': '`freq2` 同样扣掉 `{v}`',
        'vid[v] = m': '给第 {m} 种数字（`{v}`）编号 `{vid[v]}`',
        'while p < m': 'p = 不小于种类数 m 的最小 2 的幂，满二叉树叶子层有 `p` 个',
        'f = [0] * (p << 1)': '`f` 存满二叉树节点的哈希编号，下标 1 是根',
        'node_dict[(f[index << 1]': lambda S, B, r: f'非叶子节点：用左右孩子的编号二元组 `{(S.f[S.index << 1], S.f[(S.index << 1) + 1])}` 分配新编号 `{S.nxt_id}`',
        'f[index] = (index - length) << 1': '叶子节点：第 `{index - length}` 种数字，偶数次的编号是 `{f[index]}`（奇数次是 `{f[index] ^ 1}`）',
        'prefix_id = [f[1]]': '空前缀：根节点的编号 `{f[1]}` 代表「全部是偶数次」',
        'f[index] ^= 1': '这个数字出现次数奇偶翻转：叶子编号异或 1 → `f[{index}] = {f[index]}`',
        'brother = f[index ^ 1]': '兄弟节点 `index ^ 1` 的编号没变：`{brother}`',
        'key = ': '孩子编号二元组（小在前）：`{key}`',
        'if key not in node_dict': lambda S, B, r: ('这个二元组以前出现过 → 沿用旧编号' if S.key in S.node_dict else '没出现过 → 分配一个新编号'),
        'node_dict[key] = nxt_id': '新编号 `{nxt_id}` 给 `{key}`，`nxt_id` 加一',
        'f[index >> 1] = node_dict[key]': '父节点 `{index >> 1}` 的编号 = `{f[index >> 1]}`：往上一层继续改',
        'prefix_id.append(f[1])': '根节点编号就是当前前缀的奇偶状态：`prefix_id = {prefix_id}`',
        'return [hit_k': lambda S, B, r: f'查询 `[x, y]`：`y` 在 `hit_k[x]` 范围内（恰好 k 种），且 `prefix_id[y+1] == prefix_id[x]`（全是偶数次）→ =={r}=='.replace('{r}', str(r)),
    },
    cards=dict(
        one_liner='两个独立条件：滑窗管种类数，满二叉树哈希管奇偶',
        complexity='时间 `O((n + q) log n)`，空间 `O(n)`',
        problem=['给数组 `nums`、整数 `k` 和一批区间查询',
                 '区间有效：恰好 `k` 种不同数字，且每种出现次数都是偶数',
                 '示例：`[2,2,1], k=1`，查询 `[0,1],[0,2],[1,2]` → `[True, False, False]`'],
        quote='题目中对子数组有效的判别标准实际上是两个无关的部分，因此可以拆开来分别处理。',
        quote_src='—— yiduobo 题解',
        idea=['恰好 k 种：两个滑窗找出每个左端点的右端点范围 `[p1, p2-1]`',
              '偶数次：给每个前缀记录 01 串（每种数字出现次数的奇偶），前缀 `x` 与 `y+1` 相同则区间全是偶数次',
              '种类多无法压成整数，改用满二叉树，每个节点的编号是孩子编号二元组的哈希，根节点就是整串的唯一编号'],
        after=[dict(heading='树上哈希怎么改', lines=[
            '叶子：第 `k` 种数字的偶数 / 奇数状态编号为 `2k` / `2k+1`',
            '翻转奇偶只需 `f[index] ^= 1`',
            '沿父节点向上，用「孩子编号二元组」查 `node_dict`',
            '没见过的二元组分配新编号，见过的复用 → 相同状态编号相同'])],
        summary=['时间 `O(n + (n) log m)`：滑窗 `O(n)`，每次修改走一条 `log` 长的路径',
                 '易错点：二元组必须小的在前，保证同一状态只有一个编号',
                 '`p1` 比最小右端点多 1，但那个位置的数只出现 1 次，本来就过不了偶数检查',
                 '易错点：`p1`、`p2` 只增不减，每轮先 `if p < index` 追上左端点',
                 '与灵神的随机异或哈希不同，这里是确定性的编号，不会冲突',
                 '原文为 Python 2 写法，已删去 `:type` 文字说明（代码本身可在 Python 3 运行）'],
    ),
)

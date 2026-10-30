def _f(S):
    return ['∞' if v > 2000 else v for v in S['f']]


def _map(S):
    d = S.get('num_dict')
    if not d or S.get('f') is None:
        return '把 arr1、arr2 里的数 ==离散化==成 `1..cnt-1` 的排名，状态就小了'
    return '离散化（原值→排名）：' + '，'.join(f'{v}→{r}' for v, r in sorted(d.items())) + '　（排名 `j` 代表第 j 小的数）'


CONFIG = dict(
    num=1187, title='使数组严格递增', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='离散化 + f[j] 前缀最小值',
    tags=['灵神题单·动态规划', '难度分 2316'],
    code='''
class Solution(object):
    def makeArrayIncreasing(self, arr1, arr2):

        num_set = set()
        for num in arr1:
            num_set.add(num)
        for num in arr2:
            num_set.add(num)
        
        num_dict = {}
        cnt = 1
        for num in sorted(list(num_set)):
            num_dict[num] = cnt
            cnt += 1
        
        for index in range(len(arr1)):
            arr1[index] = num_dict[arr1[index]]

        arr2_set = set()
        for index in range(len(arr2)):
            arr2[index] = num_dict[arr2[index]]
            arr2_set.add(arr2[index])

        f = [2001] * cnt
        f[0] = 0
        for i in range(len(arr1)):
            min_s = f[0]
            for j in range(1, cnt):
                tmp = f[j]
                f[j] = 2001
                if j == arr1[i]:
                    f[j] = min(f[j], min_s)
                elif j in arr2_set:
                    f[j] = min(f[j], min_s + 1)
                min_s = min(min_s, tmp)
            f[0] = 2001

        res = min(f)
        if res > 2000:
            res = -1
        return res
''',
    call='Solution().makeArrayIncreasing([1,5,3], [1,3,2])',
    expect=1,
    skip=['num_set = set()', 'for num in arr1', 'for num in arr2', 'num_set.add', 'num_dict = {}', 'cnt = 1', 'for num in sorted',
          'num_dict[num] = cnt', 'cnt += 1', 'for index in range', 'arr1[index] =', 'arr2_set = set()', 'arr2[index] =', 'arr2_set.add',
          'tmp = f[j]', 'f[j] = 2001', 'elif j in arr2_set', 'for j in range(1, cnt)'],
    max_steps=110,
    views=[
        dict(type='text', fn=_map, size=22, h=60),
        dict(type='array', var='arr1', label='arr1（已换成排名；蓝 = 当前位 i）', h=190, cell=90, pointers={'i': 'blue'}, min_slots=5),
        dict(type='array', var=_f, label='f[j]：arr1 前 i 位变严格递增、且最后一位排名为 j 的最少操作（∞ = 不可能）', h=200, cell=90, pointers={'j': 'pink'}, min_slots=5,
             color=lambda S, j, v: 'green' if v != '∞' and S.get('j') == j else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('min_s', 'min_s', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = [2001] * cnt': lambda S, B, r: ('先把数收集起来排序，用排名代替原值（原值最大 `10^9`，但至多 `len(arr1)+len(arr2)` 个不同数）；'
                                             f'`f` 长度 `cnt = {S.cnt}`，`2001` 表示 ∞（操作数最多 2000）'),
        'f[0] = 0': '`f[0] = 0`：还没放任何数时，==「最后一位排名为 0」==，操作数为 0，相当于哨兵',
        'for i in range(len(arr1))': lambda S, B, r: (f'处理 `arr1` 的第 `i = {S.i}` 位（排名 `{S.arr1[S.i]}`）：算 `f` 的下一轮' if S.get('i') != B.get('i') or B.get('i') is None else '`arr1` 都处理完了'),
        'min_s = f[0]': '`min_s` = 上一轮 `f[0..j-1]` 的最小值，从 `f[0] = {min_s}` 开始',
        'if j == arr1[i]': lambda S, B, r: (
            f'`j = {S.j}` 恰好是 `arr1[{S.i}]` 的排名：不用替换，接在比它小的最优状态后面 → `f[{S.j}] = min_s` = {"∞" if S.min_s > 2000 else S.min_s}' if S.j == S.arr1[S.i]
            else (f'`j = {S.j}` 在 `arr2` 里出现过：可以替换成它，操作数 `min_s + 1`' if S.j in S.arr2_set
                  else f'`j = {S.j}` 既不是 `arr1[{S.i}]` 也不在 `arr2` 里 → 这个状态做不到，保持 ∞')),
        'f[j] = min(f[j], min_s)': '`f[{j}] = {"∞" if f[j] > 2000 else f[j]}`：不替换，操作数不增加',
        'f[j] = min(f[j], min_s + 1)': '`f[{j}] = {"∞" if f[j] > 2000 else f[j]}`：替换一次，操作数 `min_s + 1`',
        'min_s = min(min_s, tmp)': lambda S, B, r: f'`min_s` 加入上一轮的 `f[{S.j}]`（`{"∞" if S.tmp > 2000 else S.tmp}`）→ `min_s = {"∞" if S.min_s > 2000 else S.min_s}`，给 `j+1` 用',
        'f[0] = 2001': '这一轮 `arr1` 已经放了数，`f[0]` 作废（不再是空状态）',
        'res = min(f)': lambda S, B, r: f'所有最后一位排名里最小的操作数：`min(f) = {"∞" if S.res > 2000 else S.res}`',
        'if res > 2000': lambda S, B, r: ('`res` 不超过 2000 → 有解' if S.res <= 2000 else '`res` 仍是 ∞ → 无解'),
        'res = -1': '无解，返回 `-1`',
        'return res': '最少操作数 =={ret}==',
    },
    cards=dict(
        one_liner='离散化后 f[j]：最后一位排名为 j 的最少操作',
        complexity='时间 `O(n·(n+m))`，空间 `O(n+m)`',
        problem=['每次可把 `arr1[i]` 换成 `arr2` 里的任意一个数',
                 '求让 `arr1` ==严格递增==的最少操作数；不行返回 `-1`',
                 '本视频：`[1,5,3]`，`[1,3,2]` → `1`（5 换成 2）'],
        quote='数组中的每一位的取值范围都取决于上一位的大小，那么很自然想到使用动态规划来解决，令f[i][j]表示使arr1前i位严格递增，且最后一位大小为j时所需的最小操作次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数最大 `10^9`，但至多 `4000` 个不同数 → ==离散化==成排名',
              '`f[j]` 三种情况：等于 `arr1[i]`（不换）、在 `arr2` 里（换，+1）、否则 ∞',
              '转移都是「上一轮 `j` 之前的最小值」→ 用 `min_s` 边扫边维护，压缩掉 `i` 这一维'],
        summary=['时间 `O(n·(n+m))`，空间 `O(n+m)`',
                 '`2001` 当作 ∞：操作次数最多 2000；最后 `res > 2000` 就返回 `-1`',
                 '先用 `min_s` 转移、再把上一轮 `f[j]` 并入，顺序反了会用到本轮的值',
                 '每轮结束 `f[0] = 2001`：只有第一位之前才是空状态',
                 '对比灵神：灵神枚举「没被替换」的下标 + 二分；yiduobo 是离散化后的值域 DP'],
    ),
)

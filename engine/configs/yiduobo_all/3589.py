_NUMS = [4, 2, 3, 6, 5, 7]


def _isp(v):
    return v > 1 and all(v % d for d in range(2, int(v ** 0.5) + 1))


_PL = [(i, v) for i, v in enumerate(_NUMS) if _isp(v)]


def _c(S, i, v):
    if not _isp(v):
        return None
    k = [a for a, _ in _PL].index(i)
    if 'index' in S and 'p' in S and S['index'] <= k < S['p']:
        return 'cyan'
    return 'green'


def _eq(S):
    if 'index' not in S or 'p' not in S:
        return ''
    pl = S['prime_list']
    win = ', '.join(str(v) for _, v in pl[S['index']:S['p']])
    return f"以第 {S['index']} 个质数起头：窗口质数 [{win}]，`p = {S['p']}`（下一个不能加的）"


CONFIG = dict(
    num=3589, title='计数质数间隔平衡子数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='质数序列上的滑动窗口 + 单调队列',
    tags=['单调队列', '滑动窗口', '难度分 2235'],
    code='''
class Solution(object):
    def primeSubarray(self, nums, k):
        
        prime = [None] * 11
        for v in range(2, 11):
            if prime[v] is None:
                prime[v] = True
                for x in range(v + v, 11, v):
                    prime[x] = False
        
        prime_list = []
        for index, v in enumerate(nums):
            if prime[v]:
                prime_list.append((index, v))
        
        res = 0
        p = 0
        ma = deque()
        mi = deque()
        for index, (ori_index, v) in enumerate(prime_list):
            if p <= index:
                p = index + 1
                ma.append((ori_index, v))
                mi.append((ori_index, v))

            while p < len(prime_list) and abs(prime_list[p][1] - mi[0][1]) <= k and abs(ma[0][1] - prime_list[p][1]) <= k:
                while ma and ma[-1][1] <= prime_list[p][1]:
                    ma.pop()
                ma.append((prime_list[p][0], prime_list[p][1]))

                while mi and mi[-1][1] >= prime_list[p][1]:
                    mi.pop()
                mi.append((prime_list[p][0], prime_list[p][1]))
                
                p += 1
                

            if p - index > 1:
                if index == 0:
                    start_choice = ori_index + 1
                else:
                    start_choice = ori_index - prime_list[index - 1][0]
            
                if p == len(prime_list):
                    end_choice = len(nums) - prime_list[index + 1][0]
                else:
                    end_choice = prime_list[p][0] - prime_list[index + 1][0]

                res += start_choice * end_choice

            if ma and ma[0][0] == ori_index:
                ma.popleft()
            
            if mi and mi[0][0] == ori_index:
                mi.popleft()
        
        return res
''',
    call='Solution().primeSubarray([4,2,3,6,5,7], 2)',
    expect=7,
    skip=['prime[v] is None', 'prime[v] = True', 'for x in range(v + v', 'prime[x] = False', 'for v in range(2, 11)',
          'prime_list.append', 'res = 0', 'p = 0', 'mi = deque()', 'if prime[v]', 'for index, v in enumerate(nums)'],
    views=[
        dict(type='array', var='nums', label='nums（绿 = 质数，青 = 当前窗口里的质数）', color=_c, h=240,
             pointers={'ori_index': 'blue'}),
        dict(type='queue', var='ma', label='ma（原下标:值，队首 = 窗口最大质数）', fmt=lambda t: f'{t[0]}:{t[1]}', h=110),
        dict(type='queue', var='mi', label='mi（原下标:值，队首 = 窗口最小质数）', fmt=lambda t: f'{t[0]}:{t[1]}', h=110),
        dict(type='text', fn=_eq, h=70),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'orange'), ('start_choice', 'start_choice', 'cyan'),
           ('end_choice', 'end_choice', 'pink'), ('res', 'res', 'green')],
    captions={
        'prime = [None] * 11': '先用筛法标出质数表（这一段不逐行演示；原文筛到 50000，演示改小为 10）',
        'prime_list = []': '`prime_list`：只把质数挑出来，记 `(原下标, 值)` → ==后面只在质数上滑窗==',
        'res = 0': '`res` 累计答案',
        'p = 0': '`p`：窗口右边界（在质数序列里，不含）',
        'ma = deque()': '`res` 累计答案，`p` 是窗口右边界（质数序号，不含）；`ma` / `mi` 两个单调队列维护窗口内质数的最大 / 最小值',
        'for index, (ori_index, v)': '以第 `{index}` 个质数（原下标 `{ori_index}`，值 `{v}`）作窗口左端',
        'if p <= index': lambda S, B, r: (f'`p ≤ index`：窗口空了，从自己开始，`p = {S.index + 1}`，把它放进两个队列' if S.p <= S.index
                                         else f'`p = {S.p} > index`：窗口里已有质数，沿用上一轮的右边界'),
        'p = index + 1': '`p = {p}`：窗口里先放自己',
        'ma.append((ori_index, v))': '第一个质数同时是最大值、最小值',
        'mi.append((ori_index, v))': '第一个质数同时是最大值、最小值',
        'while p < len(prime_list) and abs': lambda S, B, r: (
            f'试着加第 `p = {S.p}` 个质数 `{S.prime_list[S.p][1]}`：和最小 `{S.mi[0][1]}`、最大 `{S.ma[0][1]}` 的差都 ≤ `{S.k}` → 能加'
            if S.p < len(S.prime_list) and abs(S.prime_list[S.p][1] - S.mi[0][1]) <= S.k and abs(S.ma[0][1] - S.prime_list[S.p][1]) <= S.k
            else ('质数用完了，停止' if S.p >= len(S.prime_list) else f'加 `{S.prime_list[S.p][1]}` 会让极差 > `{S.k}` → 窗口到此为止')),
        'while ma and ma[-1][1] <=': lambda S, B, r: (f'新质数 `{S.prime_list[S.p][1]}` ≥ `ma` 队尾 `{S.ma[-1][1]}` → 队尾永远当不了最大值，弹掉' if S.ma and S.ma[-1][1] <= S.prime_list[S.p][1] else '`ma` 队尾比新质数大（或队列空）→ 停止'),
        'ma.pop()': '`ma` 队尾弹出',
        'ma.append((prime_list[p][0]': '新质数入 `ma`：队列值保持递减',
        'while mi and mi[-1][1] >=': lambda S, B, r: (f'新质数 `{S.prime_list[S.p][1]}` ≤ `mi` 队尾 `{S.mi[-1][1]}` → 队尾永远当不了最小值，弹掉' if S.mi and S.mi[-1][1] >= S.prime_list[S.p][1] else '`mi` 队尾比新质数小（或队列空）→ 停止'),
        'mi.pop()': '`mi` 队尾弹出',
        'mi.append((prime_list[p][0]': '新质数入 `mi`：队列值保持递增',
        'p += 1': '右边界右移：`p = {p}`',
        'if p - index > 1': lambda S, B, r: (f'窗口里有 `{S.p - S.index}` 个质数 ≥ 2 → 有合法子数组' if S.p - S.index > 1
                                             else '窗口里只有 1 个质数 → 不合法，跳过'),
        'if index == 0': lambda S, B, r: ('第一个质数：左边没有别的质数' if S.index == 0 else '不是第一个质数：左端点不能越过前一个质数'),
        'start_choice = ori_index + 1': '左端点可选 `0..{ori_index}`，共 `{ori_index} + 1` = =={start_choice}== 种',
        'start_choice = ori_index - prime_list[index - 1][0]': '左端点只能在前一个质数之后到自己：`{ori_index} − {prime_list[index - 1][0]}` = =={start_choice}== 种',
        'if p == len(prime_list)': lambda S, B, r: ('窗口顶到最后一个质数：右端点可以一直走到数组末尾' if S.p == len(S.prime_list)
                                                    else '窗口后面还有质数：右端点最远到它的前一格'),
        'end_choice = len(nums) - prime_list[index + 1][0]': '右端点从第 2 个质数到末尾：`{len(nums)} − {prime_list[index + 1][0]}` = =={end_choice}== 种',
        'end_choice = prime_list[p][0] - prime_list[index + 1][0]': '右端点从第 2 个质数到下个质数前一格：`{prime_list[p][0]} − {prime_list[index + 1][0]}` = =={end_choice}== 种',
        'res += start_choice * end_choice': '左端点选法 × 右端点选法：`{start_choice} × {end_choice}` = {start_choice * end_choice}，`res` = =={res}==',
        'if ma and ma[0][0] == ori_index': lambda S, B, r: ('窗口左端的质数要离开：它正好是 `ma` 队首 → 出队' if S.ma and S.ma[0][0] == S.ori_index
                                                           else '它不是 `ma` 队首，不用动'),
        'ma.popleft()': '`ma` 队首出队',
        'if mi and mi[0][0] == ori_index': lambda S, B, r: ('它正好是 `mi` 队首 → 出队' if S.mi and S.mi[0][0] == S.ori_index
                                                           else '它不是 `mi` 队首，不用动'),
        'mi.popleft()': '`mi` 队首出队',
        'return res': '一共 =={ret}== 个质数间隔平衡子数组',
    },
    max_steps=150,
    cards=dict(
        one_liner='只在质数上滑窗：起头定了，左选法 × 右选法',
        complexity='时间 `O(n + M)`（M 为筛的范围），空间 `O(n + M)`',
        problem=['子数组要==至少有两个质数==，且最大质数 − 最小质数 ≤ `k`',
                 '数出这样的子数组个数',
                 '本视频：`[4,2,3,6,5,7]`，`k = 2` → `7`'],
        quote='这个问题可以利用堆或者单调队列求解。我一开始使用的堆实现的，但是被卡了常数，后来又改成单调队列实现。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把质数抽出来成 `prime_list`，非质数不影响答案，只在它上面滑窗',
              '以第 `index` 个质数起头，右边界 `p` 只增不减，两个单调队列给出窗口最大、最小',
              '数量 = ==左选法 × 右选法==：左端点在前一个质数之后，右端点在第 2 个质数到下一个不能加的质数之前'],
        summary=['时间 `O(n + M)`，每个质数至多入队出队一次',
                 '左选法 `ori_index − 前一个质数下标`，第一个质数时是 `ori_index + 1`',
                 '右选法到 `prime_list[p][0] − prime_list[index+1][0]`，`p` 到头则到数组末尾',
                 '原文为 Python 2 风格，除筛法范围外无需改动；原文 `50001` 为演示改成 `11`（示例最大值 7），否则逐行追踪太慢，筛法几行也不逐行演示',
                 '对比灵神：灵神在原数组上滑窗，用 `last2` 一次算出一批；yiduobo 抽出质数序列，乘法计数'],
    ),
)

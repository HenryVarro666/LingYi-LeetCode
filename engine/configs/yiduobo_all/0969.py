CONFIG = dict(
    num=969, title='煎饼排序', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='每轮把最大值翻到位',
    tags=['贪心算法', '构造题'],
    code='''
class Solution(object):
    def pancakeSort(self, arr):

        n = len(arr)
        res = []
        for target in range(n, 0, -1):
            for pos in range(n):
                if arr[pos] == target:
                    break
            if pos != target - 1:
                if pos != 0:
                    res.append(pos + 1)
                    l = 0
                    r = pos
                    while l < r:
                        arr[l], arr[r] = arr[r], arr[l]
                        l += 1
                        r -= 1

                l = 0
                r = target - 1
                while l < r:
                    arr[l], arr[r] = arr[r], arr[l]
                    l += 1
                    r -= 1
                
                res.append(target)
        
        return res
''',
    call='Solution().pancakeSort([3,2,4,1])',
    expect=[3, 4, 2, 3, 2],
    views=[
        dict(type='text', h=60, fn=lambda S: ('翻转序列 res = `' + str(S['res']) + '`  （每个数 k 表示翻转前 k 张）') if 'res' in S else ''),
        dict(type='array', var='arr', h=300, label='arr（煎饼堆，左边是顶）',
             pointers={'pos': 'yellow', 'l': 'blue', 'r': 'pink'},
             color=lambda S, i, v: 'green' if 'target' in S and i >= S['target'] else None),
    ],
    watch=[('target', 'target', 'purple'), ('pos', 'pos', 'yellow'), 'l', 'r'],
    skip=['l = 0', 'r = pos', 'r = target - 1'],
    max_steps=90,
    captions={
        'for target in': lambda S, B, r: ('n 轮都做完了，退出循环' if B.get('target') == S.target
                                         else f'第 {S.n - S.target + 1} 轮：要把最大值 `{S.target}` 放到下标 `{S.target - 1}`（绿色 = 已归位）'),
        'if arr[pos] == target': '找 `{target}` 的位置：`arr[{pos}] = {arr[pos]}`，{"找到了，pos = " + str(pos) if arr[pos] == target else "不是，继续往后找"}',
        'if pos != target - 1': lambda S, B, r: (f'`pos = {S.pos}` 已经等于 `target - 1 = {S.target - 1}` → 本来就在位置上，跳过' if S.pos == S.target - 1
                                                else f'`pos = {S.pos}` ≠ `{S.target - 1}`：还没归位，要翻两次'),
        'if pos != 0': lambda S, B, r: ('`pos = 0`：最大值已在最顶，不用第一次翻转' if S.pos == 0
                                        else f'`pos = {S.pos}`：先把 0 ~ {S.pos} 翻转，让 `{S.target}` 到最顶'),
        'res.append(pos + 1)': '记录翻转前 `pos + 1 = {pos + 1}` 张 → `res = {res}`',
        'arr[l], arr[r] = arr[r], arr[l]': '交换 `arr[{l}]` 和 `arr[{r}]`：{arr}',
        'res.append(target)': '再翻转前 `target = {target}` 张，`{target}` 落到下标 `{target - 1}` → `res = {res}`',
        'return res': '全部归位，返回 `res = {res}`',
    },
    cards=dict(
        one_liner='每轮：先把最大值翻到最顶，再整体翻到该去的位置',
        complexity='时间 `O(n^2)`，空间 `O(1)`（不计结果）',
        problem=['`arr` 是 1~n 的排列，每次可选 `k`，翻转前 `k` 个元素（像用锅铲翻煎饼）',
                 '返回一个能把 `arr` 排成升序的翻转序列 `k`，任一可行解即可',
                 '本视频：`[3,2,4,1]` → `[3,4,2,3,2]`'],
        quote='对于第k轮，当前最大值应该是n - k，那么我们首先通过一趟遍历找出n - k在数组中的位置pos。若pos = n - k - 1，说明n - k已经归位，那么继续进行下一轮，否则就想将0到pos反序，然后将0到n - k - 1反序。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目只要一个可行解，规模又小 → 构造：每轮把当前最大值归位',
              '翻 `pos+1` 张：最大值到最顶；再翻 `target` 张：最大值沉到下标 `target-1`',
              '归位的部分以后不再动，问题缩小一格，共 n 轮'],
        summary=['每轮一次查找加至多两次翻转，共 `O(n^2)` 时间',
                 '易错：返回的是翻转的==张数== `pos + 1`、`target`，不是下标',
                 '`pos == 0` 时最大值已在顶，省掉第一次翻转（不能翻 0 张）',
                 '原文已是 Python 3 可运行写法（只有 range 和 append），未作修改'],
    ),
)

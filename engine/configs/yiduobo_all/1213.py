CONFIG = dict(
    num=1213, title='三个有序数组的交集', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='遍历一个数组 + 两个指针',
    tags=['三指针'],
    code='''
class Solution(object):
    def arraysIntersection(self, arr1, arr2, arr3):

        p = q = 0
        res = []

        for num in arr1:
            while p < len(arr2) and arr2[p] < num:
                p += 1
            
            if p == len(arr2):
                break
            
            while q < len(arr3) and arr3[q] < num:
                q += 1
            
            if q == len(arr3):
                break
            
            if arr2[p] == arr3[q] == num:
                res.append(num)
        
        return res
''',
    call='Solution().arraysIntersection([1,2,3,4,5], [1,2,5,7,9], [1,3,4,5,8])',
    expect=[1, 5],
    views=[
        dict(type='array', var='arr1', label='arr1（逐个遍历 num）', pointers={'arr1.index(num)': 'green'}, pointer_labels={'arr1.index(num)': 'num'}, h=165,
             color=lambda S, i, v: 'green' if 'num' in S and v == S['num'] else None,
             dim=lambda S, i, v: 'num' in S and v < S['num']),
        dict(type='array', var='arr2', label='arr2（指针 p）', pointers={'p': 'blue'}, h=165,
             color=lambda S, i, v: 'blue' if S.get('p') == i else None),
        dict(type='array', var='arr3', label='arr3（指针 q）', pointers={'q': 'pink'}, h=165,
             color=lambda S, i, v: 'pink' if S.get('q') == i else None),
        dict(type='array', var='res', label='res（交集）', h=110, color=lambda S, i, v: 'yellow'),
    ],
    watch=['num', ('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'p = q = 0': 'p、q 分别记录 arr2、arr3 下一个要检测的下标：都从 `0` 开始',
        'for num in arr1': '遍历 arr1 的每个数：`num = {num}`，看 arr2、arr3 里有没有它',
        'while p < len(arr2)': lambda S, B, r: (f'`arr2[{S.p}] = {S.arr2[S.p]} < {S.num}` → 太小，不可能是交集' if S.p < len(S.arr2) and S.arr2[S.p] < S.num
                                                else ('arr2 已经走到头' if S.p >= len(S.arr2) else f'`arr2[{S.p}] = {S.arr2[S.p]} ≥ {S.num}`，p 停在这里')),
        'p += 1': '数组有序，小于 `num` 的数以后也用不上 → `p` 右移到 {p}（p 只增不减）',
        'if p == len(arr2)': lambda S, B, r: ('arr2 用完了，后面的 num 只会更大，不可能再有交集 → ==break==' if S.p == len(S.arr2)
                                               else '`p` 还没越界，继续看 arr3'),
        'while q < len(arr3)': lambda S, B, r: (f'`arr3[{S.q}] = {S.arr3[S.q]} < {S.num}` → 太小，跳过' if S.q < len(S.arr3) and S.arr3[S.q] < S.num
                                                else ('arr3 已经走到头' if S.q >= len(S.arr3) else f'`arr3[{S.q}] = {S.arr3[S.q]} ≥ {S.num}`，q 停在这里')),
        'q += 1': '同理，`q` 右移到 {q}（q 也只增不减）',
        'if q == len(arr3)': lambda S, B, r: ('arr3 用完了 → ==break==' if S.q == len(S.arr3) else '`q` 没越界，可以比较三个数'),
        'if arr2[p] == arr3[q] == num': lambda S, B, r: (f'`{S.arr2[S.p]} == {S.arr3[S.q]} == {S.num}` → ==三个数组都有它=='
                                                          if S.arr2[S.p] == S.arr3[S.q] == S.num
                                                          else f'`arr2[p] = {S.arr2[S.p]}`、`arr3[q] = {S.arr3[S.q]}`、`num = {S.num}` 不全相等 → 不是交集'),
        'res.append(num)': '`{num}` 加入结果：`res = {res}`',
        'return res': '三数组交集 `{res}`',
    },
    cards=dict(
        one_liner='遍历第一个数组，另外两个数组各用一个只增不减的指针',
        complexity='时间 `O(n1+n2+n3)`，空间 `O(1)`（不计结果）',
        problem=['给三个严格递增的整数数组 `arr1`、`arr2`、`arr3`',
                 '返回在三个数组里==都出现过==的整数，按递增顺序',
                 '示例：`[1,2,3,4,5]`、`[1,2,5,7,9]`、`[1,3,4,5,8]` → `[1,5]`'],
        quote='对第一个数组进行一趟遍历，同时使用两个变量p和q分别记录后面两个数组接下来需要检测的下标。根据单调性，随着遍历的进行，p和q也只会逐渐增大。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历 `arr1` 的每个 `num`，让 `p`、`q` 跳过 arr2、arr3 里比它小的数',
              '数组有序，`num` 只会变大，跳过的数以后也不会再用到',
              '`arr2[p]`、`arr3[q]` 和 `num` 三者相等才算交集'],
        summary=['时间 `O(n)`，三个数组各扫一遍',
                 '`p`、`q` 越界就直接 `break`：后面的 `num` 更大，不会再有交集',
                 '三个数相等才加入；不相等时 p、q 不回退，下一个 num 自然会继续推进',
                 '本题是 1198 题的弱化版，思路相同'],
    ),
)

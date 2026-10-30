def _ftxt(S):
    if 'f' not in S or 'i' not in S or 'now' not in S:
        return '`f[i]` = 以 `arr[i]` 为根节点的树有多少种形态'
    return f"`f[{S['i']}]`（根 = {S['now']}）累计 = =={S['f'][S['i']]}==（还没加上单独一个节点的 1）"


CONFIG = dict(
    num=823, title='带因子的二叉树', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='排序 + f[i] 枚举 arr[j]',
    tags=['灵神题单', '动态规划', '难度分 1900'],
    code='''
class Solution(object):
    def numFactoredBinaryTrees(self, arr):

        mod = 10 ** 9 + 7
        arr = sorted(arr)
        pos_dict = {}
        for index, num in enumerate(arr):
            pos_dict[num] = index
        f = [1]
        n = len(arr)
        for i in range(1, n):
            f.append(0)
            now = arr[i]
            for j in range(0, i):
                if arr[j] ** 2 <= now and now % arr[j] == 0:
                    tmp = now // arr[j]
                    if tmp in pos_dict:
                        pos = pos_dict[tmp]
                        if tmp == arr[j]:
                            f[i] += f[j] ** 2
                        else:
                            f[i] += f[pos] * f[j] * 2
                        f[i] %= mod
            f[i] = (f[i] + 1) % mod
        
        return sum(f) % mod
''',
    call='Solution().numFactoredBinaryTrees([10, 2, 4, 5, 20, 8])',
    expect=23,
    views=[
        dict(type='array', var='arr', label='arr（排序后）：j 枚举因子，i 是当前根', pointers={'i': 'blue', 'j': 'pink'}, h=190,
             color=lambda S, i, v: ('blue' if i == S['i'] else 'pink' if i == S.get('j') else None) if 'i' in S else None),
        dict(type='array', var='f', label='f[i]：以 arr[i] 为根的树有多少种形态', pointers={'i': 'blue'}, h=190,
             color=lambda S, i, v: 'green' if 'i' in S and i == S['i'] else None),
        dict(type='map', var='pos_dict', label='pos_dict：值 → 在 arr 中的位置', font=26, h=160,
             fmt=lambda k, v: f'{k}→{v}'),
        dict(type='text', fn=_ftxt, size=30, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'now', 'tmp'],
    captions={
        'arr = sorted': '先从小到大排序：左右孩子的值 ≤ 根的值，所以 `f[i]` 只会用到下标更小的 f',
        'pos_dict[num]': '记录每个值的位置：`pos_dict[{num}] = {index}`',
        'f = [1]': '最小的数没有因子可分解，`f[0] = 1`（只有它自己）',
        'for i in range': '开始算 `f[{i}]`',
        'f.append(0)': '给 `f[{i}]` 先放个 0，后面累加各种分解',
        'now = arr[i]': '当前根节点的值 `now = {now}`',
        'for j in range': '枚举 `arr[0]` 到 `arr[{i-1}]` 当作其中一个孩子',
        'if arr[j] ** 2 <= now': lambda S, B, r: (f'`{S.arr[S.j]}² = {S.arr[S.j]**2} ≤ {S.now}` 且 `{S.now} % {S.arr[S.j]} = 0` → {S.arr[S.j]} 是因子，往下看另一个因子' if S.arr[S.j] ** 2 <= S.now and S.now % S.arr[S.j] == 0
                                                  else (f'`{S.arr[S.j]}² = {S.arr[S.j]**2} > {S.now}`：只枚举平方 ≤ now 的，跳过' if S.arr[S.j] ** 2 > S.now
                                                        else f'`{S.now} % {S.arr[S.j]} ≠ 0`，不能整除，跳过')),
        'tmp = now': '另一个因子 `tmp = {now} // {arr[j]} = {tmp}`',
        'if tmp in pos_dict': lambda S, B, r: (f'`{S.tmp}` 在 arr 中 → 可以用 {S.arr[S.j]} 和 {S.tmp} 作左右孩子' if S.tmp in S.pos_dict
                                              else f'`{S.tmp}` 不在 arr 中，这个分解不成立'),
        'pos = pos_dict': '`tmp` 在 arr 中的位置 `pos = {pos}`',
        'if tmp == arr[j]': lambda S, B, r: (f'`tmp = arr[j] = {S.tmp}`：左右孩子相同，==不能交换== → 不乘 2' if S.tmp == S.arr[S.j]
                                            else f'`tmp = {S.tmp} ≠ arr[j] = {S.arr[S.j]}`：左右孩子不同，==可以交换== → 乘 2'),
        'f[i] += f[j] ** 2': '`f[j]² = {f[j]**2}`，`f[{i}]` → =={f[i]}==',
        'f[i] += f[pos]': '`f[pos] × f[j] × 2` = `{f[pos]} × {f[j]} × 2`，`f[{i}]` → =={f[i]}==',
        'f[i] %= mod': '取模，防止数字太大：`f[{i}] = {f[i]}`',
        'f[i] = (f[i] + 1)': '别忘了 `arr[i]` 单独一个节点也是一棵树：+1 → `f[{i}] = {f[i]}`',
        'return sum(f)': '答案 = f 数组之和 = =={sum(f)}==',
    },
    cards=dict(
        one_liner='排序后令 f[i] 为以 arr[i] 为根的树的形态数',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`arr` 中的整数都大于 1 且互不相同，每个数可以用任意次',
                 '非叶结点的值 = 两个子结点值之积，求能构成多少棵二叉树（对 `10^9+7` 取模）',
                 '本视频：`[10,2,4,5,20,8]` → `23`'],
        quote='若arr[i] % arr[j] == 0，且arr[i] / arr[j]也在arr当中，说明可以使用arr[j]以及arr[i] / arr[j]作为左右子树的根节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['因子都大于 1，孩子的值不会比根大 → 先 ==排序==，令 `f[i]` 表示以 `arr[i]` 为根的形态数',
              '枚举 `arr[j]`，若整除且商也在 arr 中：`f[i] += f[j] * f[pos[商]]`',
              '最后再 +1（`arr[i]` 单独一个节点），答案是 f 之和'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '只枚举 `arr[j]² ≤ arr[i]`，累加时乘 2；`arr[j]` 等于商时左右不能交换，不乘 2',
                 '原文为 Python 2 写法，其中整数除法 `/` 已改为 `//`',
                 '每次累加后取模，最后 +1 也要取模'],
    ),
)

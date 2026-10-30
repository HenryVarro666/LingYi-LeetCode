CONFIG = dict(
    num=1835, title='所有数对按位与结果的异或和', difficulty='Hard', category='位运算',
    author='yiduobo', technique='逐位 · 数对个数的奇偶',
    tags=['灵神题单', '难度分 1825'],
    code='''
class Solution(object):
    def getXORSum(self, arr1, arr2):

        maxn = max(max(arr1), max(arr2))
        pow2 = [1]
        while pow2[-1] + pow2[-1] <= maxn:
            pow2.append(pow2[-1] + pow2[-1])

        res = 0
        for p in pow2:
            cnt1 = cnt2 = 0
            for num in arr1:
                if num & p:
                    cnt1 += 1
            for num in arr2:
                if num & p:
                    cnt2 += 1
            
            if cnt1 % 2 == 1 and cnt2 % 2 == 1:
                res += p
        
        return res
''',
    call='Solution().getXORSum([1,2,4], [6,5])',
    expect=3,
    views=[
        dict(type='array', var='arr1', label='arr1', h=130),
        dict(type='array', var='arr2', label='arr2', h=130),
        dict(type='array', var='pow2', label='pow2（每个对应一个二进制位）', h=130,
             color=lambda S, i, v: 'yellow' if S.get('p') == v else None),
        dict(type='text', h=80, size=32, fn=lambda S: (
            f"位 `{S['p']}`：`arr1` 有 =={S['cnt1']}== 个、`arr2` 有 =={S['cnt2']}== 个这位是 1 → 数对 `{S['cnt1']}×{S['cnt2']}={S['cnt1']*S['cnt2']}` 个"
            if 'cnt1' in S and 'cnt2' in S else '逐位看：这一位上有奇数个 1，异或结果这位才是 1')),
    ],
    watch=['p', ('cnt1', 'cnt1', 'blue'), ('cnt2', 'cnt2', 'pink'), ('res', 'res', 'green')],
    captions={
        'maxn = max': '`maxn = {maxn}`：二进制位只需要看到最高位',
        'while pow2[-1]': '`pow2[-1] * 2 = {pow2[-1] * 2}` 还 `<= {maxn}` → 继续加一位',
        'pow2.append': '`pow2` = {pow2}',
        'res = 0': '`res` 按位累加答案',
        'for p in pow2': lambda S, B, r: (f'看这一位：`p` = {S.p}（二进制 `{S.p:b}`）' if S.p != B.get('p') else '三位都看完了'),
        'cnt1 = cnt2 = 0': '两个数组里，这一位是 1 的个数清零重数',
        'for num in arr1': lambda S, B, r: (f'`arr1` 里取 `{S.num}`' if S.num != B.get('num') else '`arr1` 数完了'),
        'for num in arr2': lambda S, B, r: (f'`arr2` 里取 `{S.num}`' if S.num != B.get('num') else '`arr2` 数完了'),
        'if num & p': lambda S, B, r: (f'`{S.num} & {S.p}` 非零 → 这位是 1' if S.num & S.p else f'`{S.num} & {S.p}` = 0 → 这位是 0'),
        'cnt1 += 1': '`arr1` 里这位是 1 的有 `cnt1` = =={cnt1}== 个',
        'cnt2 += 1': '`arr2` 里这位是 1 的有 `cnt2` = =={cnt2}== 个',
        'if cnt1 % 2 == 1': lambda S, B, r: (
            f'数对里这位是 1 的有 `{S.cnt1}×{S.cnt2}={S.cnt1*S.cnt2}` 个：' + ('奇数 → 异或后这位是 1' if S.cnt1 * S.cnt2 % 2 else '偶数 → 两两抵消，这位是 0')),
        'res += p': '这位是 1 → `res` 加上 `{p}` → =={res}==',
        'return res': '各位拼起来，答案 `{res}`',
    },
    cards=dict(
        one_liner='不枚举数对：看每一位，数对里 1 的个数是 p×q',
        complexity='时间 `O((n+m) log U)`，空间 `O(log U)`',
        problem=['对所有数对算 `arr1[i] & arr2[j]`，再把结果全部异或',
                 '数组长度到 `10^5`，两两枚举会超时',
                 '示例：`[1,2,3]`、`[6,5]` → `0`；本视频用 `[1,2,4]`、`[6,5]` → `3`'],
        quote='对于其中的某一位而言，其最终异或的结果可能是0或者1，这取决于之前的l1 * l2个结果中该位上的1是偶数个还是奇数个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`arr1` 有 p1 个数该位为 1，`arr2` 有 p2 个：与后该位是 1 的数对恰有 `p1×p2` 个',
              '异或只看奇偶：`p1×p2` 为奇，这一位就是 1',
              '于是枚举每一位，数两边的 1，奇奇才加 `p`'],
        summary=['时间 `O((n+m) log U)`，空间 `O(log U)`',
                 '原文是 Python 2 风格，在 Python 3 下可直接运行，未做改动',
                 '`pow2` 只造到不超过 `maxn` 的最高位，漏位会少算',
                 '对比灵神：灵神用分配律一行 `xor(a) & xor(b)`，yiduobo 是它的逐位推导'],
    ),
)

CONFIG = dict(
    num=2198, title='单因数三元组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按数值枚举 + 剩余可用次数',
    tags=[],
    code='''
class Solution(object):
    def singleDivisorTriplet(self, nums):

        cnt = [0] * 101
        for v in nums:
            cnt[v] += 1
        
        res = 0
        for i in range(1, 101):
            if cnt[i] > 0:
                cnt_i = cnt[i]
                cnt[i] -= 1
            else:
                continue

            for j in range(1, 101):
                if cnt[j] > 0:
                    cnt_j = cnt[j]
                    cnt[j] -= 1
                else:
                    continue

                for k in range(1, 101):
                    if cnt[k] == 0:
                        continue
                    
                    s = i + j + k
                    i_flag = j_flag = k_flag = 1
                    if s % i == 0:
                        i_flag = 0
                    if s % j == 0:
                        j_flag = 0
                    if s % k == 0:
                        k_flag = 0
                    
                    if i_flag + j_flag + k_flag == 2:
                        res += cnt_i * cnt_j * cnt[k]

                cnt[j] += 1
            
            cnt[i] += 1

        return res
''',
    call='Solution().singleDivisorTriplet([4,6,7,3,2])',
    expect=12,
    max_events=60000,
    views=[
        dict(type='map', var=lambda S: {v: c for v, c in enumerate(S['cnt']) if c} if 'cnt' in S else {},
             fmt=lambda k, v: f'数值 {k} : 剩 {v} 个', label='cnt（只列出剩余次数 > 0 的数值）', h=300),
        dict(type='text', size=34, fn=lambda S: (f"三元组 `({S['i']}, {S['j']}, {S['k']})`  和 `s` = =={S['s']}==" if 's' in S and 'k' in S else
                                                   (f"已选 `i = {S['i']}`、`j = {S['j']}`，枚举第三个数 `k`" if 'j' in S and 'cnt_j' in S else ''))),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'cyan'), ('s', 's', 'yellow'), ('res', 'res', 'green')],
    skip=['continue', 'else:', 'for j in range', 'for k in range', 'if cnt[j] > 0', 'if cnt[k] == 0', 'i_flag = j_flag', 'i_flag = 0', 'j_flag = 0', 'k_flag = 0', 'for i in range', 'if cnt[i] > 0'],
    captions={
        'cnt = [0]': '值域只有 1~100：按==数值==而不是下标来数，`cnt[v]` 是数值 v 的个数',
        'cnt[v] += 1': '数值 {v} 出现次数：`cnt[{v}]` = {cnt[v]}',
        'for i in range': '枚举三元组的第一个数值 `i`',
        'if cnt[i] > 0': '`cnt[{i}]` = {cnt[i]}：有这个数才能当 i；没有就跳过',
        'cnt_i = cnt[i]': '枚举到有数的 `i` = {i}（没有的数值直接跳过）。记下 i 的可用个数 `cnt_i` = {cnt_i}，然后用掉一个',
        'cnt[i] -= 1': '用掉一个 {i}，剩 `cnt[{i}]` = {cnt[i]}：防止 j、k 又选到同一个下标',
        'cnt_j = cnt[j]': '选 `j` = {j}，记下它的可用个数 `cnt_j` = {cnt_j}，然后用掉一个',
        'cnt[j] -= 1': '用掉一个 {j}，剩 `cnt[{j}]` = {cnt[j]}',
        's = i + j + k': '三个数 `{i} + {j} + {k}`，和 `s` = =={s}==',
        's % i': '`{s} % {i} = {s % i}` → {"整除" if s % i == 0 else "不整除"}',
        's % j': '`{s} % {j} = {s % j}` → {"整除" if s % j == 0 else "不整除"}',
        's % k': '`{s} % {k} = {s % k}` → {"整除" if s % k == 0 else "不整除"}',
        'if i_flag + j_flag + k_flag == 2': lambda S, B, r: (
            f'不整除的 flag 之和 = `{S.i_flag + S.j_flag + S.k_flag}`：==等于 2 才表示恰好 1 个整除==' + ('，满足' if S.i_flag + S.j_flag + S.k_flag == 2 else '，不满足')),
        'res += cnt_i': '满足：下标组合数 `{cnt_i} × {cnt_j} × {cnt[k]}` = {cnt_i * cnt_j * cnt[k]}，`res` = =={res}==',
        'cnt[j] += 1': '`j` 枚举完，把用掉的 {j} 还回去',
        'cnt[i] += 1': '`i` 枚举完，把用掉的 {i} 还回去',
        'return res': '共 =={res}== 个单因数三元组（下标有序）',
    },
    cards=dict(
        one_liner='数值范围只有 100：枚举数值，用剩余次数计数',
        complexity='时间 `O(C^3)`（C = 100），空间 `O(C)`',
        problem=['给正整数数组 `nums`，求下标互不相同的三元组 `(i, j, k)` 的个数',
                 '要求：三个数之和能被其中 ==恰好一个== 数整除',
                 '示例：`[4,6,7,3,2]` → `12`'],
        quote='数组长度比较大，但是具体数值的取值范围仅在1到100之间，因此可以通过数值而不是下标来考虑。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数每个数值出现几次，再三重循环枚举三个==数值==',
              '数值可能相同：选中就把可用次数减 1，枚举完再加回去',
              '满足条件就累加 `cnt_i * cnt_j * cnt[k]`（三个数的下标选法）'],
        summary=['时间 `O(C^3)`，C = 100；空间 `O(C)`',
                 '不能直接用哈希表里的次数：相同数值要记下枚举时的剩余次数',
                 '第三层用 `cnt[k]`（已扣除 i、j），前两层用事先保存的 `cnt_i`、`cnt_j`',
                 '三元组按下标有序计数，所以 (i,j,k) 的各种排列都会算一次'],
    ),
)

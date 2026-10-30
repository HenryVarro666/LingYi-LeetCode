CONFIG = dict(
    num=1814, title='统计一个数组中好对子的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='移项 · 哈希表统计差值',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countNicePairs(self, nums):

        delta_dict = {}
        for num in nums:
            tmp = num
            num_list = []
            while tmp:
                num_list.append(tmp % 10)
                tmp //= 10
            
            reverse = 0
            for digit in num_list:
                reverse = reverse * 10 + digit
            
            delta_dict[num - reverse] = delta_dict.get(num - reverse, 0) + 1
        
        res = 0
        mod = 10 ** 9 + 7
        for cnt in delta_dict.values():
            res = res + cnt * (cnt - 1) // 2
            res %= mod
        
        return res
''',
    call='Solution().countNicePairs([42,11,1,97])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前数）', h=170, cell=100,
             color=lambda S, i, v: 'blue' if S.get('num') == v and 'delta_dict' in S and i == S['nums'].index(v) and 'cnt' not in S else None),
        dict(type='map', var='delta_dict', label='delta_dict：num − rev(num) → 出现次数', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', size=30, h=120,
             fn=lambda S: (f"`{S['num']}` 的反转是 `{S['reverse']}`，差值 `{S['num']} − {S['reverse']}` = =={S['num'] - S['reverse']}=="
                           if S.get('_line') == 16 and 'reverse' in S
                           else (f"这一组差值有 `{S['cnt']}` 个数 → 选两个：`{S['cnt']}×({S['cnt']}−1)/2` = =={S['cnt']*(S['cnt']-1)//2}==" if 'cnt' in S
                                 else 'nums[i] + rev(nums[j]) = nums[j] + rev(nums[i])  ⇔  nums[i] − rev(nums[i]) = nums[j] − rev(nums[j])'))),
    ],
    watch=[('num', 'num', 'blue'), ('reverse', 'reverse', 'orange'), ('cnt', 'cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'delta_dict = {}': '`delta_dict` 用来数：每种差值 `num − rev(num)` 出现了几次',
        'for num in nums': lambda S, B, r: (f'取下一个数 `num = {S.num}`' if 'num' in S and ('num' not in B or S.num != B.num) else '数完了，开始统计对子'),
        'tmp = num': '用 `tmp` 一位位拆开 `num`',
        'num_list = []': '`num_list` 存各位数字，低位在前',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}`，还有数位' if S.tmp else '`tmp = 0`，数位拆完'),
        'num_list.append': '取个位 `{tmp % 10}`，`num_list = {num_list}`',
        'tmp //=': '去掉个位，`tmp = {tmp}`',
        'reverse = 0': '`reverse` 从 0 开始，把 `num_list` 按顺序拼回去',
        'for digit': lambda S, B, r: ('各位都拼完了，循环结束' if 'digit' in S and S.reverse == int(''.join(map(str, S.num_list))) and S.reverse > 0 else f'取 `digit = {S.digit}`'),
        'reverse = reverse * 10': '`reverse = {B.reverse}×10 + {digit}` = {reverse}（低位先进，所以得到反转数）',
        'delta_dict[num - reverse]': '差值 `{num} − {reverse}` = =={num - reverse}==：这个差值的计数 → `{delta_dict[num - reverse]}`',
        'res = 0': '`res` 累计好对子数',
        'mod =': '答案要对 `10^9 + 7` 取模',
        'for cnt in': lambda S, B, r: (f'某个差值出现了 `cnt = {S.cnt}` 次' if 'cnt' in S else ''),
        'res = res + cnt': '这组里任选两个都是好对子：`{cnt}×({cnt}−1)//2 = {cnt*(cnt-1)//2}`，`res` → {res}',
        'res %= mod': '取模（小数据没有变化）：`res = {res}`',
        'return res': '好对子一共 `{res}` 个',
    },
    cards=dict(
        one_liner='移项后，差值 num − rev(num) 相同的数两两都是好对子',
        complexity='时间 `O(n log C)`，空间 `O(n)`',
        problem=['`rev(x)` 是把 `x` 的数字反转，如 `rev(42)=24`',
                 '下标对 `(i, j)`（`i < j`）满足 `nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])` 就是好对子',
                 '统计好对子的个数（对 `10^9+7` 取模）',
                 '本视频：`[42,11,1,97]` → `2`'],
        quote='nums[i] - rev(nums[i]) = nums[j] - rev(nums[j])，可以发现，等式两侧的形式一致且只与一个数有关，因此可以一趟遍历，使用哈希表记录每个数在上面这个式子下的结果。',
        quote_src='—— yiduobo 题解原文',
        idea=['把含 i 的项移到一边、含 j 的项移到另一边',
              '每个数只需算一个差值 `num − rev(num)`',
              '某个差值出现 cnt 次，就有 `cnt×(cnt−1)/2` 个好对子'],
        summary=['时间 `O(n log C)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`tmp /= 10` 与 `cnt * (cnt - 1) / 2` 已改为整除 `//`',
                 '易错：先移项再数，不要两两枚举（`O(n²)` 会超时）',
                 '题面库里没有，题意按 LeetCode 原题与 yiduobo 文章整理'],
    ),
)

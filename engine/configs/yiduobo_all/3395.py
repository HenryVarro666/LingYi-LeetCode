def _col(S, i, v):
    idx = S.get('index')
    if idx is None or 'x' not in S:
        return None
    if i == idx:
        return 'yellow'
    return 'green' if v == S['x'] else None


def _ptr(S):
    return S.get('index') if 'x' in S else None


def _txt(S):
    if 'suffix_other' not in S:
        return '先预处理：每种数的总次数 `cnt`、前缀/后缀里「相同元素对」的数量'
    return (f'x = {S["x"]}：前缀 x×{S["prefix_x"]}、其他×{S["prefix_other"]}；'
            f'后缀 x×{S["suffix_x"]}、其他×{S["suffix_other"]}')


CONFIG = dict(
    num=3395, title='唯一中间众数子序列 I', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='按 x 的个数分类 + 枚举 y',
    tags=['灵神题单', '组合计数', '难度分 2800'],
    code='''
class Solution(object):
    def subsequencesWithMiddleMode(self, nums):
        
        n = len(nums)

        cnt = {}
        prefix_same_pair = []
        for index in range(n):
            v = nums[index]
            if index == 0:
                prefix_same_pair.append(0)
            else:
                prefix_same_pair.append(prefix_same_pair[-1] + cnt.get(v, 0))
            cnt[v] = cnt.get(v, 0) + 1
        
        cnt = {}
        suffix_same_pair = []
        for index in range(n - 1, -1, -1):
            v = nums[index]
            if index == n - 1:
                suffix_same_pair.append(0)
            else:
                suffix_same_pair.append(suffix_same_pair[-1] + cnt.get(v, 0))
            cnt[v] = cnt.get(v, 0) + 1
        suffix_same_pair.reverse()

        def calc_pair(cnt):
            if cnt < 2:
                return 0
            return cnt * (cnt - 1) // 2

        mod = 10 ** 9 + 7
        n = len(nums)
        res = 0
        prefix_cnt = {}
        for index, x in enumerate(nums):
            if index < 2:
                prefix_cnt[x] = prefix_cnt.get(x, 0) + 1
                continue
            if index > n - 3:
                break
            
            prefix_x = prefix_cnt.get(x, 0)
            suffix_x = cnt[x] - 1 - prefix_x
            prefix_other = index - prefix_x
            suffix_other = n - index - 1 - suffix_x

            prefix_x_pair = calc_pair(prefix_x)
            suffix_x_pair = calc_pair(suffix_x)

            res = (res + prefix_x_pair * suffix_x_pair) % mod

            res = (res + prefix_x_pair * suffix_x * suffix_other) % mod
            res = (res + suffix_x_pair * prefix_x * prefix_other) % mod

            res = (res + prefix_x_pair * calc_pair(suffix_other)) % mod
            res = (res + suffix_x_pair * calc_pair(prefix_other)) % mod
            res = (res + prefix_x * suffix_x * prefix_other * suffix_other) % mod

            for y in cnt:
                if x == y:
                    continue
                    
                prefix_y = prefix_cnt.get(y, 0)
                suffix_y = cnt[y] - prefix_y

                if prefix_y > 0 and suffix_other - suffix_y >= 2:
                    suffix_pair = calc_pair(suffix_other - suffix_y)
                    suffix_pair -= suffix_same_pair[index + 1]
                    suffix_pair += calc_pair(suffix_x) + calc_pair(suffix_y)
                    res = (res + prefix_x * prefix_y * suffix_pair) % mod
                    
                if suffix_y > 0 and prefix_other - prefix_y >= 2:
                    prefix_pair = calc_pair(prefix_other - prefix_y)
                    prefix_pair -= prefix_same_pair[index - 1]
                    prefix_pair += calc_pair(prefix_x) + calc_pair(prefix_y)
                    res = (res + suffix_x * suffix_y * prefix_pair) % mod
            
            prefix_cnt[x] = prefix_cnt.get(x, 0) + 1

        return res
''',
    call='Solution().subsequencesWithMiddleMode([1, 2, 2, 3, 4])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前中间数 x，绿 = 其他的 x）', color=_col, cell=84, h=170,
             pointers={_ptr: 'yellow'}, pointer_labels={_ptr: 'index'}),
        dict(type='map', var=lambda S: S['cnt'] if isinstance(S.get('cnt'), dict) else dict(Counter(S['nums'])), label='cnt：整个数组里各数的次数', h=130, font=26),
        dict(type='map', var='prefix_cnt', label='prefix_cnt：当前下标之前各数的次数', h=130, font=26),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=['prefix_x', 'suffix_x', 'prefix_other', 'suffix_other', 'prefix_x_pair', 'suffix_x_pair', ('res', 'res', 'green')],
    max_steps=130,
    skip=['v = nums[index]', 'if index == 0', 'if index == n - 1', 'if index < 2', 'prefix_same_pair.append(0)', 'suffix_same_pair.append(0)', 'prefix_other =',
          'prefix_pair -= prefix_same', 'suffix_pair -= suffix_same', 'cnt[v] = cnt.get(v, 0) + 1',
          'mod = 10', 'n = len(nums)', 'cnt = {}', 'prefix_cnt = {}', 'res = 0', 'suffix_same_pair.reverse()',
          'for index in range(n', 'if cnt < 2', 'return 0', 'return cnt *', 'continue', 'break', 'if x == y', 'prefix_y = prefix_cnt'],
    captions={
        'prefix_same_pair.append(prefix': '`prefix_same_pair` 追加：前缀里「相同元素对」数 = 上一项 + 已有 `{B.cnt.get(v, 0)}` 个同样的 `{v}` → {prefix_same_pair}',
        'suffix_same_pair.append(suffix': '`suffix_same_pair` 追加：从后往前同理 → {suffix_same_pair}',
        'for index, x in enumerate': lambda S, B, r: (f'`index = {S.index}`：左边不够 2 个，不能当中间数，只记入 `prefix_cnt`' if S.index < 2 else
                                                       f'`index = {S.index}`：右边不够 2 个' if S.index > S.n - 3 else f'枚举 `nums[{S.index}] = {S.x}` 作为中间的 x'),
        'if index < 2': lambda S, B, r: ('`index < 2`：左边不够 2 个，不能当中间数，只更新 `prefix_cnt` 后 continue' if S.index < 2
                                         else '`index ≥ 2`：左边够选 2 个，继续'),
        'prefix_cnt[x] = prefix_cnt.get(x, 0) + 1': lambda S, B, r: (f'把 `{S.x}` 记入 `prefix_cnt` → {S.prefix_cnt}' if S.index < 2 or S.get('res') is None or 'prefix_x' not in S
                                                                       else f'x 走到前缀里：`prefix_cnt[{S.x}]` → {S.prefix_cnt[S.x]}'),
        'if index > n - 3': lambda S, B, r: ('右边不够选 2 个 → 结束循环' if S.index > S.n - 3
                                            else '`index ≤ n-3`：右边还够选 2 个，继续'),
        'prefix_x = prefix_cnt': '`prefix_x`：前缀中 x 的个数 = {prefix_x}',
        'suffix_x = cnt[x]': '`suffix_x = cnt[x] − 1 − prefix_x = {suffix_x}`：减 1 是减去中间这个 x',
        'suffix_other =': '非 x 的个数：前缀 `prefix_other = {prefix_other}`（共 {index} 个），后缀 `suffix_other = {suffix_other}`（共 {n - index - 1} 个）',
        'prefix_x_pair =': lambda S, B, r: f'前缀选 2 个 x：`calc_pair({S.prefix_x}) = {S.prefix_x * (S.prefix_x - 1) // 2}`',
        'suffix_x_pair =': lambda S, B, r: f'后缀选 2 个 x：`calc_pair({S.suffix_x}) = {S.suffix_x * (S.suffix_x - 1) // 2}`',
        'prefix_x_pair * suffix_x_pair': '情况 1，5 个都是 x：前 2 后 2 → `{prefix_x_pair}×{suffix_x_pair}`，`res = {res}`',
        'prefix_x_pair * suffix_x * suffix_other': '情况 2，4 个 x（前 2 后 1）：后面再配一个非 x → `res = {res}`',
        'suffix_x_pair * prefix_x * prefix_other': '情况 2，4 个 x（前 1 后 2）：前面再配一个非 x → `res = {res}`',
        'prefix_x_pair * calc_pair(suffix_other)': '情况 3，3 个 x（前 2 后 0）：后面任选 2 个非 x → `res = {res}`',
        'suffix_x_pair * calc_pair(prefix_other)': '情况 3，3 个 x（前 0 后 2）：前面任选 2 个非 x → `res = {res}`',
        'prefix_x * suffix_x * prefix_other': '情况 3，3 个 x（前 1 后 1）：两边各配一个非 x → `res = {res}`',
        'for y in cnt': lambda S, B, r: ('`y` 枚举完了，换下一个 x' if 'y' in B and B.y == S.y else f'`y = {S.y}` 就是 x，跳过' if S.y == S.x else f'情况 4（只有 2 个 x）：枚举另一个数 `y = {S.y}`，看另一个 x 落在前缀还是后缀'),
        'suffix_y = cnt[y]': '`prefix_y = {prefix_y}`，`suffix_y = cnt[y] − prefix_y = {suffix_y}`：y 在前缀、后缀的个数',
        'if prefix_y > 0 and suffix_other': lambda S, B, r: (
            f'另一个 x 在前缀：前缀选 1 个 x、1 个 y；后缀要从「非 x 非 y」的 `{S.suffix_other - S.suffix_y}` 个里选 2 个不同的'
            + (' → 可行' if S.prefix_y > 0 and S.suffix_other - S.suffix_y >= 2 else ' → 不可行')),
        'suffix_pair = calc_pair(': lambda S, B, r: f'后缀「非 x 非 y」任选 2 个：`calc_pair({S.suffix_other - S.suffix_y})` = {(S.suffix_other - S.suffix_y) * (S.suffix_other - S.suffix_y - 1) // 2}',
        'suffix_pair += calc_pair': '其中相同的 2 个要去掉：减 `suffix_same_pair[index+1]`，再把重复减掉的 x、y 对加回 → `suffix_pair = {suffix_pair}`',
        'res = (res + prefix_x * prefix_y': '`res += prefix_x × prefix_y × suffix_pair` → `res = {res}`',
        'if suffix_y > 0 and prefix_other': lambda S, B, r: (
            f'另一个 x 在后缀：后缀选 1 个 x、1 个 y；前缀要从「非 x 非 y」的 `{S.prefix_other - S.prefix_y}` 个里选 2 个不同的'
            + (' → 可行' if S.suffix_y > 0 and S.prefix_other - S.prefix_y >= 2 else ' → 不可行')),
        'prefix_pair = calc_pair(': lambda S, B, r: f'前缀「非 x 非 y」任选 2 个：`calc_pair({S.prefix_other - S.prefix_y})` = {(S.prefix_other - S.prefix_y) * (S.prefix_other - S.prefix_y - 1) // 2}',
        'prefix_pair += calc_pair': '同样去掉相同的 2 个，加回重复减掉的 x、y 对 → `prefix_pair = {prefix_pair}`',
        'res = (res + suffix_x * suffix_y': '`res += suffix_x × suffix_y × prefix_pair` → `res = {res}`',
        'return res': '答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='按中间数 x 的个数分四类，2 个 x 的类枚举 y 排除重复',
        complexity='时间 `O(n²)`（`n ≤ 1000`），空间 `O(n)`',
        problem=['长度为 5 的子序列，中间元素是==唯一众数==才合法',
                 '求 `nums`（长度 ≤ 1000）中合法子序列的个数，模 `10^9+7`',
                 '本视频：`[1,2,2,3,4]` → `1`'],
        quote='一个自然的想法就是枚举 nums 中的每个元素 nums[index] 作为这个中间众数，计算合法的子序列数目，然后累加起来即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先预处理 `cnt` 和前/后缀的「相同元素对」数 `same_pair`',
              '子序列里有 5、4、3 个 x：x 必是唯一众数，直接乘法原理',
              '只有 2 个 x：另外 3 个数必须两两不同 → 枚举 y（与 x 同侧的那个），再从剩下的数里选互不相同的 2 个'],
        summary=['时间 `O(n²)`，空间 `O(n)`；`n ≤ 1000` 可以接受',
                 '2 个 x 的情况：「选两个不同的」= 任选 2 个 − 相同的对，要加回被多减的 x、y 对',
                 '`index < 2` 与 `index > n-3` 的位置不能当中间数',
                 '对比灵神：灵神反过来用总数减不合法，再把枚举 y 压成 O(1)；yiduobo 正向分类累加'],
    ),
)

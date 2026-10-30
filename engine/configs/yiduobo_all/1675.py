def _state(S):
    if 'max_a' not in S:
        return ''
    if 'p_max' not in S:
        return f"第一遍：每个数除尽因子 2 后取最大的奇数 ==max_a = {S['max_a']}=="
    t = S.get('tbd_list') or []
    s = f"最终范围 [`p_min = {S['p_min']}`, `p_max = {S['p_max']}`]，待定 `{t}`"
    if 'res' in S:
        s += f"，当前 ==res = {S['res']}=="
    return s


CONFIG = dict(
    num=1675, title='数组的最小偏移量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='贪心 · 固定最大奇数 + 枚举阈值',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minimumDeviation(self, nums):

        max_a = 0
        flag = True
        for index, num in enumerate(nums):
            while num & 1 == 0:
                num >>= 1
            
            if max_a != 0 and max_a != num:
                flag = False
            max_a = max(max_a, num)
        
        if flag:
            return 0

        p_max = p_min = max_a
        tbd_list = []
        for index, num in enumerate(nums):
            if num & 1:
                if num >= max_a:
                    p_max = max(p_max, num)
                elif num * 2 < max_a:
                    p_min = min(p_min, num * 2)
                else:
                    tbd_list.append(num)
            else:
                if num < max_a:
                    p_min = min(p_min, num)
                else:
                    while num & 1 == 0 and num > max_a:
                        num >>= 1
                    
                    if num == max_a:
                        continue
                    tbd_list.append(num)

        if not tbd_list:
            return p_max - p_min

        tbd_list.sort()
        res = max(p_max, tbd_list[-1]) - min(p_min, tbd_list[0])

        for index, num in enumerate(tbd_list):
            now_min = min(p_min, tbd_list[0] * 2)
            now_max = max(p_max, num * 2)
            if index < len(tbd_list) - 1:
                now_min = min(now_min, tbd_list[index + 1])
                now_max = max(now_max, tbd_list[-1])
            
            res = min(res, now_max - now_min)
        
        return res
''',
    call='Solution().minimumDeviation([8,5,7,9])',
    expect=3,
    views=[
        dict(type='text', fn=_state, size=26, h=60),
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums', h=190,
             color=lambda S, i, v: 'blue' if S.get('index') == i and 'tbd_list' in S else None),
        dict(type='array', var='tbd_list', label='tbd_list（待定：乘 2 还是不乘）', h=190,
             pointers={'index': 'pink'} if False else {}),
    ],
    skip=['max_a = 0', 'flag = True', 'num >>= 1', 'tbd_list = []'],
    watch=[('max_a', 'max_a', 'orange'), ('p_min', 'p_min', 'blue'), ('p_max', 'p_max', 'pink'),
           ('num', 'num', 'cyan'), ('res', 'res', 'green')],
    captions={
        'while num & 1 == 0:': lambda S, B, r: (f'`{S.num}` 是偶数 → 除以 2，一直除到奇数（写成 `a × 2^b`，取其中的 a）' if S.num % 2 == 0
                                                else f'`{S.num}` 已经是奇数，这个数的 a = =={S.num}=='),
        'max_a != 0 and max_a != num': lambda S, B, r: ('和前面的 a 不一样 → ==不可能全部变成同一个数==' if S.max_a != 0 and S.max_a != S.num
                                                        else '和前面的 a 一样（或是第一个数），暂时还可能全相同'),
        'max_a = max(max_a, num)': '`max_a = max({B.max_a}, {num}) = {max_a}`：记下最大的奇数 a',
        'if flag': lambda S, B, r: ('所有 a 都相同 → 全部变成 a，偏移量为 0' if S.flag
                                    else f'a 不全相同，答案 > 0；证明：==最大的 a={S.max_a} 一定出现在最优答案里=='),
        'p_max = p_min = max_a': '最大奇数 `{max_a}` 必在答案里，其余数都向它靠拢：`p_max = p_min = {max_a}`',
        'if num & 1:': lambda S, B, r: (f'`{S.num}` 是奇数：只能保持或乘 2' if S.num & 1 else f'`{S.num}` 是偶数：可以一路除以 2'),
        'if num >= max_a': lambda S, B, r: (f'奇数 `{S.num}` ≥ `max_a={S.max_a}` → ==保持不变==，它可能是最大值，更新 `p_max`' if S.num >= S.max_a
                                            else f'奇数 `{S.num}` < `max_a={S.max_a}`，还要看乘 2 以后怎样'),
        'p_max = max(p_max, num)': '`p_max = {p_max}`',
        'elif num * 2 < max_a': lambda S, B, r: (f'`{S.num}×2 = {S.num*2}` 仍小于 `{S.max_a}` → ==乘 2 更靠近 max_a==' if S.num * 2 < S.max_a
                                                 else f'`{S.num}×2 = {S.num*2}` 已经超过 `{S.max_a}`：乘不乘各有利弊，无法单独决定'),
        'p_min = min(p_min, num * 2)': '乘 2 后 `{num*2}` 可能成为最小值：`p_min = {p_min}`',
        'tbd_list.append(num)': '`{num}` 保持离 `{max_a}` 差 `{max_a-num}`，乘 2 离 `{max_a}` 差 `{abs(num*2-max_a)}`，还要看别的数 → ==先放进待定 tbd_list=={tbd_list}',
        'if num < max_a': lambda S, B, r: (f'偶数 `{S.num}` 比 `max_a={S.max_a}` 小 → 保持不变就行（再除只会更远）' if S.num < S.max_a
                                           else f'偶数 `{S.num}` 不小于 `max_a={S.max_a}` → 要往下除'),
        'p_min = min(p_min, num)': '偶数当最小值候选：`p_min = {p_min}`',
        'while num & 1 == 0 and num > max_a': '偶数比 `max_a` 大 → 一直除以 2，直到 ≤ max_a 或变奇数：`num = {num}`',
        'if num == max_a': lambda S, B, r: (f'除到了 `max_a={S.max_a}` → 已经确定，不用处理' if S.num == S.max_a
                                            else f'`{S.num}` < `max_a`，但再乘 2 就超过了 → 也要放进待定'),
        'continue': '这个数转成 `max_a`，继续下一个',
        'if not tbd_list': lambda S, B, r: ('没有待定的数，答案就是 `p_max - p_min`' if not S.tbd_list
                                            else f'还有待定的数 `{S.tbd_list}` → 需要找一个阈值'),
        'return p_max - p_min': '`p_max - p_min = {p_max} - {p_min}` = =={ret}==',
        'tbd_list.sort()': '排序：==小的数乘 2 才有意义，大的乘 2 只会让差更大==',
        'res = max(p_max': '都不乘 2：最大 `max({p_max}, {tbd_list[-1]})`，最小 `min({p_min}, {tbd_list[0]})` → `res = {res}`',
        'for index, num in enumerate(tbd_list)': '枚举阈值：`tbd_list[0..index]` 全部乘 2，后面的保持不变',
        'now_min = min(p_min, tbd_list[0] * 2)': '前缀都乘 2，最小值候选 `min({p_min}, {tbd_list[0]*2}) = {now_min}`',
        'now_max = max(p_max, num * 2)': '阈值 `{num}` 乘 2 = `{num*2}` 是被乘的最大数 → `now_max = {now_max}`',
        'if index < len(tbd_list) - 1': '后面是否还有没乘 2 的数？`index={index}`',
        'now_min = min(now_min, tbd_list[index + 1])': '没乘 2 的最小是 `{tbd_list[index+1]}` → `now_min = {now_min}`',
        'now_max = max(now_max, tbd_list[-1])': '没乘 2 的最大是 `{tbd_list[-1]}` → `now_max = {now_max}`',
        'res = min(res, now_max - now_min)': '阈值 `{num}`：偏移 `{now_max} - {now_min} = {now_max-now_min}`，`res = min({B.res}, {now_max-now_min}) = {res}`',
        'return res': '最小偏移量 =={res}==',
    },
    cards=dict(
        one_liner='把每个数写成 a×2^b：最大的 a 一定留在答案里，其余数向它靠拢',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['奇数可以 `×2`，偶数可以 `÷2`，次数不限',
                 '偏移量 = 数组最大值 − 最小值，求最小的偏移量',
                 '示例：`[1,2,3,4]` → `1`；本视频：`[8,5,7,9]` → `3`'],
        quote='若某种情况下max_a没有出现在答案中……将其转化为max_a：此时maximum可能会变小，但minimum不会发生变化，==答案可能更优但不会更差==。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数都是 `a × 2^b`，取值范围是 `a×2^k`（k 从 0 到 b），奇数只能 k=0 或 1',
              '证明最大的 a（`max_a`）必在答案里 → 其余数都尽量靠近它',
              '有些数乘 2 与否无法单独判断 → 放进 `tbd_list`，排序后枚举阈值：==≤阈值的乘 2，其余不变=='],
        summary=['时间 `O(n log n)`（排序 + 除 2），空间 `O(n)`',
                 '全部 a 相同时答案为 0，要先单独判断',
                 '待定数只能是「前缀乘 2、后缀不变」：若 y 乘 2 则比它小的 x 也必须乘 2',
                 '枚举到末尾时没有 `tbd_list[index+1]`，所以代码里要判断 `index < len - 1`',
                 '对比常见的堆解法：yiduobo 用数学推导，不用堆'],
    ),
)

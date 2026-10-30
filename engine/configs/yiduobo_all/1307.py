_I = lambda S: S['_inner']


def _same(S, B, k):
    try:
        return B[k] == S[k]
    except Exception:
        return False
_LV = lambda S: S['_inner'].get('level')


def _wts(S):
    pl = S['_inner'].get('param_list')
    return [f'{c}{p:+d}' for c, p in pl] if pl else []


def _asg(S):
    i = S['_inner']
    pl = i.get('param_list')
    if not pl:
        return []
    res = i.get('res', [])
    return [f'{c}={res[k]}' if k < len(res) else f'{c}=?' for k, (c, p) in enumerate(pl)]


def _info(S):
    i = S['_inner']
    pl = i.get('param_list')
    if pl is None or 'level' not in i:
        d = i.get('param_dict')
        if d is None:
            return '把竖式拆成位权：左边每个字母 × 权重，右边取负，总和 = 0'
        return '字母权重 `' + ' '.join(f'{c}:{p}' for c, p in d.items()) + '`（右边为负）'
    lv = i['level']
    ch, pa = pl[lv]
    r = f"已定部分之和 `now = {i['now']}`；处理 `{ch}`（权重 `{pa}`）"
    if 'mi' in i and 'ma' in i and i.get('upper') is not None:
        r += f"，取值范围 `{i['mi']}` ~ `{i['ma']}`"
    return r


CONFIG = dict(
    num=1307, title='口算难题', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='系数化简 + 上下界剪枝回溯',
    tags=['灵神题单', '链表树与回溯'],
    code="""
class Solution(object):
    def isSolvable(self, words, result):

        param_dict = {}
        first_set = set()
        for word in words:
            p = 1
            for index in range(len(word) - 1, -1, -1):
                char = word[index]
                param_dict[char] = param_dict.get(char, 0) + p
                p *= 10
            if len(word) > 1:
                first_set.add(word[0])

        p = 1
        for index in range(len(result) - 1, -1, -1):
            char = result[index]
            param_dict[char] = param_dict.get(char, 0) - p
            p *= 10
        
        if len(result) > 1:
            first_set.add(result[0])

        param_list = sorted(param_dict.items(), key=lambda d:-abs(d[1]))
        n = len(param_list)
        max_list = []
        min_list = []
        for p in range(1, n):
            max_used = [False] * 10
            min_used = [False] * 10
            ma = mi = 0
            for index in range(p, n):
                if param_list[index] == 0:
                    continue
                
                char, param = param_list[index]
                if param > 0:
                    for num in range(9, -1, -1):
                        if not max_used[num] and (num != 0 or char not in first_set):
                            max_used[num] = True
                            ma += param * num
                            break
                    for num in range(10):
                        if not min_used[num] and (num != 0 or char not in first_set):
                            min_used[num] = True
                            mi += param * num
                            break
                else:
                    for num in range(10):
                        if not max_used[num] and (num != 0 or char not in first_set):
                            max_used[num] = True
                            ma += param * num
                            break
                    for num in range(9, -1, -1):
                        if not min_used[num] and (num != 0 or char not in first_set):
                            min_used[num] = True
                            mi += param * num
                            break

            max_list.append(ma)
            min_list.append(mi)

        used = [False] * 10
        return self.dfs(0, n, 0, param_list, used, first_set, max_list, min_list, [])
     
    def dfs(self, level, n, now, param_list, used, first_set, max_list, min_list, res):
        char, param = param_list[level]
        if level == n - 1:
            if param < 0:
                if now < 0:
                    return False
                param = -param
                if now % param == 0:
                    tmp = now // param
                    if not used[tmp] and (tmp != 0 or char not in first_set):
                        return True
                    else:
                        return False
                else:
                   return False

            elif param > 0:
                if now > 0:
                    return False
                now = -now
                if now % param == 0:
                    tmp = now // param
                    if not used[tmp] and (tmp != 0 or char not in first_set):
                        return True
                    else:
                        return False
                else:
                    return False

            elif now != 0 or (n == 10 and not used[0] and char in first_set):
                return False
            else:
                return True
        
        char, param = param_list[level]
        if param == 0:
            if char not in first_set:
                return True
            for num in range(1, 10):
                if not used[num]:
                    used[num] = True
                    if self.dfs(level + 1, n, now, param_list, used, first_set, max_list, min_list):
                        return True
                    used[num] = False
            return False
        
        '''
        now + p * c + k = 0
        now + p * c + mi <= 0 <= now + p * c + ma
        p * c <= -now - mi
        p * c >= -now - ma
        '''

        if param > 0:
            upper = -now - min_list[level]
            if upper < 0:
                return False
            ma = min(upper // param, 9)
            
            bounder = -now - max_list[level]
            if param * 9 < bounder:
                return False
            elif bounder < 0:
                mi = 0
            else:
                mi = bounder // param
                if bounder % param != 0:
                    mi += 1
        else:
            upper = now + max_list[level]
            if upper < 0:
                return False
            ma = min(upper // -param, 9)

            bounder = now + min_list[level]
            if -param * 9 < bounder:
                return False
            elif bounder < 0:
                mi = 0
            else:
                mi = bounder // -param
                if bounder % -param != 0:
                    mi += 1

        for num in range(mi, ma + 1):
            if not used[num] and (num != 0 or char not in first_set):
                used[num] = True
                now += param * num
                res.append(num)
                if self.dfs(level + 1, n, now, param_list, used, first_set, max_list, min_list, res):
                    return True
                res.pop()
                now -= param * num
                used[num] = False
            
        return False
""",
    call='Solution().isSolvable(["AC","BC"], "EB")',
    expect=True,
    views=[
        dict(type='text', fn=_info, h=70),
        dict(type='array', var=_wts, label='param_list：字母+权重（按绝对值从大到小）', h=165, cell=90, pointers={_LV: 'pink'}, pointer_labels={_LV: 'level'}),
        dict(type='array', var=_asg, label='已确定的取值 res（? = 还没定）', h=125, cell=90, index=False,
             color=lambda S, i, v: 'green' if '?' not in v else None),
        dict(type='array', var=lambda S: S['_inner'].get('used', []), label='used[d]：数字 d 是否已被占用', h=140, cell=60,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='calls', h=90, hide=('isSolvable',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('mi', lambda S: S['_inner'].get('mi') if 'upper' in S['_inner'] else None, 'yellow'),
           ('ma', lambda S: S['_inner'].get('ma') if 'upper' in S['_inner'] else None, 'yellow'), ('level', _LV, 'pink')],
    skip=list(range(29, 60)) + [22, 74, 87, 158, 123, 138, 8, 10, 13, 18, 16, 28, 68, 69, 82, 83, 85, 153, 129, 144, 9, 11, 17, 19, 5, 6, 7, 12, 21, 25, 26, 27, 61, 63, 67, 100, 101, 112, 119, 121, 136, 126, 141, 128, 143, 132, 147, 133, 148, 152, 154],
    captions={
        10: '`{char}` 的权重加上 `{B.p}`（它在 `{word}` 里的位权）：`param_dict[{char!r}] = {param_dict[char]}`',
        13: '`{word[0]}` 是多位数的首字母 → ==不能为 0==，记入 `first_set`',
        18: '结果 `{result}` 放在等号右边 → 权重取==负==：`param_dict[{char!r}] = {param_dict[char]}`',
        22: '结果的首字母 `{result[0]}` 也不能为 0 → `first_set = {first_set}`（多位数的首字母不能为 0）',
        15: '各单词里字母的位权累加完：`param_dict = {param_dict}`（个位权重 1，十位 10……）',
        24: '位权取负后 `param_dict = {param_dict}`；首字母不能为 0：`first_set = {first_set}`。按绝对值从大到小排序，先定权重大的字母',
        28: lambda S, B, ret: ('`p` 循环结束：每个位置的上下界都备好了' if _same(S, B, 'p') and 'p' in B else f'`p = {S.p}`：假设前 `{S.p}` 个字母已定，估算 `param_list[{S.p}:]` 这些项之和的范围'),
        60: '`p = {p}`：后面各项之和最大 `{ma}`，最小 `{mi}`',
        64: '`max_list` / `min_list` 备好，开始 dfs：从权重最大的字母开始，一个个定数字',
        68: lambda S, B, ret: (f'`level = {S.level}` 是最后一个字母 → 它的值==由等式唯一确定==' if S.level == S.n - 1
                               else f'`level = {S.level}` < `{S.n - 1}`：还不是最后一个字母，要枚举取值'),
        69: lambda S, B, ret: f'看最后一个字母 `{S.char}` 的权重 `{S.param}`：' + ('为负' if S.param < 0 else '不为负 → 看下一个分支'),
        70: '`now < 0` → 无法凑成 0',
        71: '`now < 0` → 无法凑成 0，返回 False',
        72: '取 `param` 的绝对值',
        73: lambda S, B, ret: f'`now % param = {S.now} % {S.param}` ' + ('==整除== → 能解出整数' if S.now % S.param == 0 else '不整除 → 无解'),
        74: '最后一个字母的值 `tmp = now // param = {tmp}`',
        75: lambda S, B, ret: (f'最后一个字母 `{S.char} = now // param = {S.tmp}`，没被占用' + (' 且合法 → ==解存在==' if (S.tmp != 0 or S.char not in S.first_set) else '，但是首字母不能为 0 → 失败')) if not S.used[S.tmp] else f'最后一个字母 `{S.char} = {S.tmp}` 已被占用 → 失败',
        76: '最后一个字母的值合法 → 返回 True',
        78: '最后一个字母的值不合法 → 返回 False',
        80: '不能整除 → 返回 False',
        82: '权重 `{param}` 为正：要让 `now + param×{char} = 0`',
        83: '`now > 0` → 无法凑成 0',
        84: '`now > 0` → 返回 False',
        85: '`now` 取相反数，转成求 `now // param`',
        86: lambda S, B, ret: f'`now % param = {S.now} % {S.param}` ' + ('==整除== → 能解出整数' if S.now % S.param == 0 else '不整除 → 无解'),
        87: '最后一个字母的值 `tmp = now // param = {tmp}`',
        88: lambda S, B, ret: (f'最后一个字母 `{S.char} = now // param = {S.tmp}`，没被占用' + (' 且合法 → ==解存在==' if (S.tmp != 0 or S.char not in S.first_set) else '，但是首字母不能为 0 → 失败')) if not S.used[S.tmp] else f'最后一个字母 `{S.char} = {S.tmp}` 已被占用 → 失败',
        89: '最后一个字母的值合法 → 返回 True',
        91: '最后一个字母的值不合法 → 返回 False',
        93: '不能整除 → 返回 False',
        120: '第 `{level}` 个字母 `{char}`（权重 `{param}`）：`{param}×{char} <= -now - min_list[{level}] = {upper}`',
        123: '`{char}` 的上界：`min({upper} // {param}, 9) = {ma}`',
        125: '`{char}` 上界 `min({upper} // {param}, 9) = {ma}`；下界要满足 `{param}×{char} >= -now - max = {bounder}`',
        129: '下界为负 → `mi = 0`',
        131: '下界 `{bounder} / {param}` ==向上取整==（不整除则 +1）',
        135: '第 `{level}` 个字母 `{char}`（权重 `{param}`）：`{-param}×{char} <= now + max_list[{level}] = {upper}`',
        138: '`{char}` 的上界：`min({upper} // {-param}, 9) = {ma}`',
        140: '`{char}` 上界 `min({upper} // {-param}, 9) = {ma}`；下界要满足 `{-param}×{char} >= now + min = {bounder}`',
        144: '下界为负 → `mi = 0`',
        146: '下界 `{bounder} / {-param}` ==向上取整==（不整除则 +1）',
        122: '`upper < 0` → 范围为空，返回 False',
        127: '`{param}×9 < bounder` → 够不到下界，返回 False',
        137: '`upper < 0` → 范围为空，返回 False',
        142: '`-param×9 < bounder` → 够不到下界，返回 False',
        150: lambda S, B, ret: ('范围内的数都试完了' if (_same(S, B, 'num') and 'num' in B and B.get('_line') in (151, 159)) else f'`{S.char}` 只需在 `{S.mi}` ~ `{S.ma}` 之间试，`num = {S.num}`'),
        151: lambda S, B, ret: (f'`{S.num}` 已被占用 → 跳过' if S.used[S.num] else
                                f'`{S.num}` 是首字母不能为 0 → 跳过' if (S.num == 0 and S.char in S.first_set)
                                else f'`{S.num}` 没被占用，也合法 → 可以试'),
        153: '`now += {param}×{num}` → `now = {now}`；`{char} = {num}` 记入 `res`',
        155: '选定 `{char} = {num}`：`now += {param}×{num}` → `now = {now}`，带着它去定下一个字母',
        157: '后面无解 → ==回溯==：撤销 `{char} = {num}`',
        158: '`now` 还原为 `{now}`',
        159: '数字 `{num}` 重新可用，试下一个',
        161: '这个字母的范围内全都试完仍无解 → 返回 False',
        'return self.dfs(0': '开始 dfs',
    },
    max_steps=120,
    cards=dict(
        one_liner='把竖式化成「字母×权重之和 = 0」，用上下界剪枝回溯',
        complexity='最坏 `O(n·n!)`（n ≤ 10），剪枝后很快；空间 `O(n)`',
        problem=['给若干单词 `words` 和结果 `result`，每个字母对应一个数字，不同字母数字不同',
                 '==多位数不能有前导 0==；问 `sum(words) = result` 是否有解',
                 '示例：`SEND + MORE = MONEY` → `True`',
                 '本视频：`AC + BC = EB`'],
        quote='如果我们把整数拆开……化简之后可得 S*1000 + E*91 - N*90 + D - M*9000 - O*900 + R*10 - E*9 - Y = 0。可以发现，其中 -M*9000 这一项的系数的绝对值相比其他项大得多，这就决定了 M 的取值不能太大。',
        quote_src='—— yiduobo 题解',
        idea=['每个字母的权重 = 在各单词里的位权之和，结果里的字母取负 → ==总和为 0==',
              '按权重绝对值从大到小排序，先定权重大的字母',
              '后面各项之和有上下限（正权重取大值得上限、取小值得下限）→ 当前字母的取值被夹在一个小区间里',
              '最后一个字母不用枚举，由 `now` 直接解出'],
        result='找到一组合法的数字分配 ✓',
        summary=['时间最坏 `O(n·n!)`，剪枝后实际很快；空间 `O(n)`',
                 '首字母不能为 0：用 `first_set` 记录，单个数字的单词不算',
                 '上下界是先不考虑已用数字算出的，会略宽松，但不影响正确性',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)

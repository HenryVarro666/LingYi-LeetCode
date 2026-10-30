CONFIG = dict(
    num=1923, title='最长公共子路径', difficulty='Hard', category='字符串',
    author='yiduobo', technique='二分长度 + 双模数滚动哈希',
    tags=['字符串哈希', '难度分 2661'],
    code='''
class Solution(object):
    def longestCommonSubpath(self, n, paths):

        base = 100003
        mod1 = 10 ** 9 + 7
        mod2 = 2147483647

        l = 0
        r = 100000
        for path in paths:
            r = min(r, len(path))
        
        remove_base1 = [1]
        remove_base2 = [1]
        for _ in range(r + 1):
            remove_base1.append(remove_base1[-1] * base % mod1)
            remove_base2.append(remove_base2[-1] * base % mod2)

        while l < r:
            mid = (l + r + 1) >> 1

            common1 = set()
            common2 = set()
            flag = True
            first_flag = True
            for path in paths:
                now1 = 0
                now2 = 0
                for index in range(mid):
                    now1 = now1 * base + path[index]
                    now1 %= mod1
                    now2 = now2 * base + path[index]
                    now2 %= mod2
                
                h = set([(now1, now2)])
                for index in range(mid, len(path)):
                    now1 = now1 * base + path[index] - (remove_base1[mid] * path[index - mid] % mod1)
                    if now1 < 0:
                        now1 += mod1
                    now1 %= mod1

                    now2 = now2 * base + path[index] - (remove_base2[mid] * path[index - mid] % mod2)
                    if now2 < 0:
                        now2 += mod2
                    now2 %= mod2
                    
                    h.add((now1, now2))

                if first_flag:
                    common = h.copy()
                    first_flag = False
                else:
                    tuple_list = list(common)
                    for t in tuple_list:
                        if t not in h:
                            common.remove(t)

                if not common:
                    flag = False
                    break
            
            if flag:
                l = mid
            else:
                r = mid - 1
        
        return l
''',
    call='Solution().longestCommonSubpath(4, [[0,1,2,3],[2,3,1],[1,2,3]])',
    expect=2,
    max_steps=65,
    views=[
        dict(type='text', fn=lambda S: (f"二分长度 `l={S['l']}`，`r={S['r']}`" + (f"，试 `mid={S['mid']}`" if 'mid' in S else '')) if 'l' in S and 'r' in S else ''),
        dict(type='array', var='path', h=200, label='当前路径 path',
             window=('index-mid+1', 'index'),
             pointers={'index': 'blue'}),
        dict(type='set', var='common', h=220, label='common（各路径共有的哈希）', fmt=lambda x: f'({x[0] % 1000}, {x[1] % 1000})…'),
    ],
    watch=['l', 'r', 'mid', 'index', ('flag', 'flag', 'green'), ('|h|', 'len(h) if "h" in dir() else 0')],
    skip=['now1 %= mod1', 'now2 %= mod2'],
    captions={
        'first_flag = True': '`first_flag`：第一条路径直接作为初始候选集',
        'first_flag = False': '之后的路径都要和 `common` 取交集',
        'now1 = now1 * base + path[index] - ': '窗口右移：乘 base，加新元素 `{path[index]}`，减去移出的 `{path[index - mid]}` → `now1 = {now1}`',
        'base = 100003': '进制 `base`，两个模数 `mod1`、`mod2`：双哈希防冲突',
        'r = min(r, len(path))': '公共子路径不会比最短路径长：`r = {r}`',
        'remove_base1.append': '预处理 `base^k`：滑窗时用来去掉最左元素',
        'while l < r': lambda S, B, r: ('`l=%d < r=%d`：继续二分' % (S.l, S.r)) if S.l < S.r else '`l = r = %d`：二分结束' % S.l,
        'mid = (l + r + 1) >> 1': '`mid = (l + r + 1) >> 1 = {mid}`：==向上取整==，避免 `l = mid` 时死循环',
        'common1 = set()': '本轮检查：是否存在长为 `{mid}` 的子路径出现在每条路径里',
        'flag = True': '`flag` 表示当前长度是否可行',
        'for path in paths': '检查路径 `{path}`',
        'now1 = now1 * base + path[index]': '把前 `{mid}` 个元素按 `base` 进制算进哈希：`now1 = {now1}`',
        'h = set(': '第一个长 `{mid}` 的窗口哈希入集合 `h`',
        'h.add': '这条路径的所有长 `{mid}` 子路径哈希里新增一个，`h` 共 {len(h)} 个',
        'common = h.copy()': '第一条路径的哈希直接作为 `common`',
        'for t in tuple_list': '逐个检查 `common` 里的哈希是否也在当前路径的 `h` 里',
        'if t not in h': lambda S, B, r: '这个哈希%s当前路径 → %s' % ('不在' if S.t not in S.h else '在', '删掉' if S.t not in S.h else '保留'),
        'common.remove(t)': '不是每条路径都有 → 从 `common` 删除，剩 {len(common)} 个',
        'if not common': lambda S, B, r: ('`common` 空了 → 长度 `%d` 没有公共子路径' % S.mid) if not S.common else '`common` 还有 %d 个 → 继续下一条路径' % len(S.common),
        'flag = False': '长度 `{mid}` 不可行，不用再看别的路径',
        'if flag': lambda S, B, r: '`flag = %s`：长度 `%d` %s' % (S.flag, S.mid, '可行 → 答案 >= mid' if S.flag else '不可行 → 答案 < mid'),
        'l = mid': '可行 → `l = {l}`',
        'r = mid - 1': '不可行 → `r = {r}`',
        'return l': '最长公共子路径长度 `{l}`',
    },
    cards=dict(
        one_liner='长度可二分：对每个长度，用滚动哈希求各路径子路径交集',
        complexity='时间 `O(S log L)`（S 为总长，L 为最短路径长），空间 `O(S)`',
        problem=['`m` 条城市路径 `paths`，求所有路径都含有的最长公共连续子路径的长度，没有则 `0`',
                 '示例：`[[0,1,2,3,4],[2,3,4],[4,0,1,2,3]]` → `2`（`[2,3]`）',
                 '本视频：`[[0,1,2,3],[2,3,1],[1,2,3]]` → `2`'],
        quote='可以先二分答案，设当前处理的字符串长度为mid，那么就对每个字符串中所有长度为mid的子串按照某个base进制进行编码。……本题的数据好像还蛮强的，最后被迫用了两个质数分别做哈希。',
        quote_src='—— yiduobo 题解原文',
        idea=['本质是多字符串最长公共子串；正统做法是拼接后缀数组 + 二分，但很难写',
              '作者改用 rk：二分 `mid`，每条路径滚动算出所有长 `mid` 子路径的哈希',
              '`common` 逐条路径取交集，交集为空说明该长度不可行'],
        summary=['时间约 `O(S log L)`，空间 `O(S)`',
                 '`mid` 向上取整，配合 `l = mid`',
                 '滑窗：乘 base、加新元素、减 `base^mid × 旧元素`，减完要补模数',
                 '单模数会被卡，所以用 `(now1, now2)` 双哈希',
                 '原文为 Python 2 风格，只有类型说明文档字符串，本配置没有改动代码'],
    ),
)

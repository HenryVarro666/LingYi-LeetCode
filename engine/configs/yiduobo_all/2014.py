CONFIG = dict(
    num=2014, title='重复 K 次的最长子序列', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='按长度从长到短，字符降序的回溯枚举 + 计数剪枝',
    tags=['回溯', '字符串', '难度分 2558'],
    code='''
class Solution(object):
    def longestSubsequenceRepeatedK(self, s, k):

        self.res = []
        n = len(s) // k
        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        char_set = set()
        for char in char_dict:
            if char_dict[char] >= k:
                char_set.add(char)
        
        if len(char_set) == 0:
            return ""

        char_list = sorted(list(char_set), reverse=True)
        all_cnt = [char_dict[char] for char in char_list]

        now = []
        cnt_list = [0] * len(char_list)
        for res_l in range(n, 0, -1):
            if self.dfs(0, res_l, now, char_list, cnt_list, all_cnt, s, k):
                return "".join(now)

    def dfs(self, level, res_l, now, char_list, cnt_list, all_cnt, s, k):
        if level == res_l:
            p = 0
            cnt = 0
            flag = False
            for char in s:
                if char == now[p]:
                    p += 1
                    if p == len(now):
                        cnt += 1
                        p = 0
                        if cnt == k:
                            flag = True
                            break
            
            return flag
        
        for index, char in enumerate(char_list):
            now.append(char)
            cnt_list[index] += 1
            if cnt_list[index] * k <= all_cnt[index]:
                if self.dfs(level + 1, res_l, now, char_list, cnt_list, all_cnt, s, k):
                    return True
            cnt_list[index] -= 1
            now.pop()
        
        return False
''',
    call='Solution().longestSubsequenceRepeatedK("aabb", 2)',
    expect='b',
    views=[
        dict(type='string', var='s', label='s', cell=60, h=130),
        dict(type='array', var='char_list', label='char_list（降序：先试大的字符）', cell=60, h=130),
        dict(type='array', var='all_cnt', label='all_cnt（每个字符在 s 里的总数）', cell=60, h=100, index=False),
        dict(type='array', var='cnt_list', label='cnt_list（当前 now 里已用个数；要求 个数×k ≤ 总数）', cell=60, h=100, index=False),
        dict(type='array', var='now', label='now（正在枚举的 seq）', cell=60, h=100, index=False),
        dict(type='calls', h=130, hide=('char_list', 'cnt_list', 'all_cnt', 's', 'k', 'now')),
    ],
    watch=[('res_l', lambda S: S['_inner'].get('res_l'), 'blue'), ('level', lambda S: S['_inner'].get('level'), 'cyan'),
           ('p', lambda S: S['_inner'].get('p'), 'pink'), ('cnt', lambda S: S['_inner'].get('cnt'), 'green'), 'k'],
    skip=['self.res = []', 'char_dict = {}', 'char_set = set()', 'now = []', 'flag = False', 'for char in s:',
          'for char in char_dict:', 'enumerate(char_list)', 'for res_l in range', 'p = 0', 'cnt = 0',
          'flag = True', 'break', 'cnt_list[index] += 1', 'cnt_list[index] -= 1', 'char_dict[char] = char_dict.get', 'char_set.add',
          'all_cnt = [', 'cnt_list = [0]', 'p += 1', 'now.pop()', 'return True', 'if len(char_set) == 0'],
    captions={
        'n = len(s) // k': '`n = len(s) // k = {n}`：seq 重复 k 次不超过 s，所以 seq 长度至多 `{n}`',
        'if char_dict[char] >= k': lambda S, B, ret: (
            f"`'{S.char}'` 出现 {S.char_dict[S.char]} 次 >= k = {S.k} → 可能出现在 seq 里" if S.char_dict[S.char] >= S.k
            else f"`'{S.char}'` 只出现 {S.char_dict[S.char]} 次 < k → 不可能在 seq 里"),
        'char_list = sorted': '候选字符 `{char_set}`==从大到小==排序：先放大字符，先找到的就是字典序最大的 → `{char_list}`',
        'if self.dfs(0': lambda S, B, ret: f'枚举长度 `{S.res_l}` 的 seq：长的优先，找不到才缩短一位',
        'if level == res_l': lambda S, B, ret: (
            f'`level = {S.level} == res_l`：`now = {S.now}` 填满了 → 去 s 里数它出现几次' if S.level == S.res_l
            else f'`level = {S.level} < res_l = {S.res_l}`：还要继续填第 {S.level} 位'),
        'if char == now[p]': lambda S, B, ret: (
            f"`'{S.char}' == now[{S.p}] = '{S.now[S.p]}'` → 匹配上，`p` 后移" if S.char == S.now[S.p]
            else f"`'{S.char}' != now[{S.p}] = '{S.now[S.p]}'` → 这个字符跳过"),
        'if p == len(now)': lambda S, B, ret: (
            f'`p == len(now)`：now 完整匹配了一遍' if S.p == len(S.now) else f'`p = {S.p} < len(now)`：这一遍还没匹配完'),
        'cnt += 1': 'now 完整出现一次，`cnt` → {cnt}；`p` 清零开始下一遍',
        'if cnt == k': lambda S, B, ret: (
            f'`cnt = {S.cnt} == k`：now 在 s 里（作为子序列）重复了 k 次 → ==成功==' if S.cnt == S.k
            else f'`cnt = {S.cnt} < k = {S.k}`：还不够 k 次，继续扫 s'),
        'return flag': lambda S, B, ret: ('`flag = True`：找到合法 seq，一路返回 True' if S.flag
                                          else '扫完 s 也没凑够 k 次 → 这个 seq 不行，返回 False'),
        'now.append(char)': '先尝试放 `{char!r}` → `now = {now}`',
        'if cnt_list[index] * k <= all_cnt[index]': lambda S, B, ret: (
            f"`{S.cnt_list[S.index]} × {S.k} = {S.cnt_list[S.index] * S.k} <= {S.all_cnt[S.index]}`：数量还够 → 继续往下填"
            if S.cnt_list[S.index] * S.k <= S.all_cnt[S.index]
            else f"`{S.cnt_list[S.index]} × {S.k} = {S.cnt_list[S.index] * S.k} > {S.all_cnt[S.index]}`：s 里这个字符不够用 → ==剪枝==，不递归"),
        'if self.dfs(level + 1': '递归填下一位',
        'return False': '这一位的字符都试过了，没有合法的 → 返回 False，回溯到上一位',
        'return "".join(now)': '找到了：答案是 `{ret!r}`',
    },
    max_steps=120,
    cards=dict(
        one_liner='n < 8k：seq 至多 7 种字符，长的优先、大的优先地回溯枚举',
        complexity='时间约 `O(n·7^7)`（有剪枝），空间 `O(n)`',
        problem=['在 `s` 中找==重复 `k` 次==的最长子序列：`seq * k` 是 `s` 的子序列',
                 '长度相同取==字典序最大==，不存在返回空串',
                 '示例：`s="letsleetcode", k=2` → `"let"`',
                 '本视频：`s="aabb", k=2` → `"b"`'],
        quote='题目要找的是最长的，因此应该优先检测较长的子序列。除此之外，题目要找的是相同长度中字典序最大的那个，因此在枚举时应该优先尝试较大的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n < k*8`，所以 seq 长度至多 7，至多 7 种字符 → 直接暴力枚举 seq',
              '长度从 `len(s)//k` 往下试，每个长度里字符降序，先成功的就是答案',
              '剪枝：某字符在 seq 里的个数 × k 不能超过它在 s 里的总数',
              '合法性检查：扫一遍 s，数 seq 能完整匹配几次，到 k 次就成功'],
        result='长度 2 的 `ba`、`ab` 都不行，缩短到 1：`b` 重复 2 次成立，返回 `b`',
        summary=['时间大约 `O(n·7^7)`，剪枝后远小于此；空间 `O(n)`',
                 '候选字符降序 + 长度降序，第一个合法的就是答案，不用再比较',
                 '对比灵神：灵神用 `Counter` 把字符按 `freq // k` 展开成可重排的多重集，再用 permutations 枚举；yiduobo 用计数剪枝的回溯',
                 '原文为 Python 2 写法，`len(s) / k` 已改为 `len(s) // k`'],
    ),
)

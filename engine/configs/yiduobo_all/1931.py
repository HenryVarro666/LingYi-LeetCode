def _pat(k, m=3):
    d = []
    for _ in range(m):
        d.append('rgb'[k % 3])
        k //= 3
    return ''.join(reversed(d))


CONFIG = dict(
    num=1931, title='用三种不同颜色为网格涂色', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='本质相同状态归类 + 矩阵快速幂',
    tags=['灵神题单', '难度分 2170'],
    code='''
class Solution(object):
    def colorTheGrid(self, m, n):

        self.mod = 10 ** 9 + 7
        if m == 1:
            return 3 * sum(self.quickPow([[2]], 1, n - 1)[-1]) % self.mod
        elif m == 2:
            return 2 * sum(self.quickPow([[3]], 1, n)[-1]) % self.mod
        else:
            self.replace_list = [{0: 1, 1: 0}, {0: 2, 2: 0}, {1: 2, 2: 1}, {0: 1, 1: 2, 2: 0}, {0: 2, 2: 1, 1: 0}]
            self.pow3 = [1]
            for _ in range(m):
                self.pow3.append(self.pow3[-1] * 3)
            self.color_mapping = {}
            color_dict = {}
            
            self.dfs(0, m, [], -1, color_dict)

            color_info = color_dict.items()
            l = len(color_info)
            first_line = []
            color_index = {}
            base = [[0] * l for _ in range(l)]
            
            for index, (color, cnt) in enumerate(color_info):
                first_line.append(cnt)
                color_index[color] = index
            
            for color, cnt in color_info:
                next_line_color = {}
                self.dfs(0, m, [], color, next_line_color)
                for next_color, next_cnt in next_line_color.items():
                    base[color_index[color]][color_index[next_color]] = next_cnt

            final = self.quickPow(base, l, n - 1)
            res = [0] * l
            for i in range(l):
                for j in range(l):
                    res[j] += first_line[i] * final[i][j]
                    res[j] %= self.mod

            return sum(res) % self.mod
    
    def quickPow(self, base, l, n):
        if n == 0:
            ret = [[0] * l for _ in range(l)]
            for i in range(l):
                ret[i][i] = 1
            return ret

        if n == 1:
            return base
        
        tmp = self.quickPow(base, l, n // 2)
        ret = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    ret[i][k] += tmp[i][j] * tmp[j][k]
                    ret[i][k] %= self.mod
        
        if n % 2 == 0:
            return ret

        tmp = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    tmp[i][k] += ret[i][j] * base[j][k]
                    tmp[i][k] %= self.mod
        return tmp

    def check(self, num, final, color_dict):
        if num in color_dict:
            self.color_mapping[final] = num
            color_dict[num] += 1
            return True

        if num in self.color_mapping:
            self.color_mapping[final] = self.color_mapping[num]
            color_dict[self.color_mapping[final]] = color_dict.get(self.color_mapping[final], 0) + 1
            return True
        
        return False

    def dfs(self, level, m, now, last_line, color_dict):
        if level == m:
            final = 0
            reverse_final = 0
            for index, x in enumerate(now):
                final = final * 3 + x
                reverse_final += x * self.pow3[index]
            
            if self.check(final, final, color_dict) or self.check(reverse_final, final, color_dict):
                return

            for mapping in self.replace_list:
                num = 0
                reverse_num = 0
                for index, x in enumerate(now):
                    num = num * 3 + mapping.get(x, x)
                    reverse_num += mapping.get(x, x) * self.pow3[index]
                
                if self.check(num, final, color_dict) or self.check(reverse_num, final, color_dict):
                    return

            color_dict[final] = 1
            return

        for x in range(3):
            if last_line >= 0 and last_line // self.pow3[m - level - 1] % 3 == x:
                continue
            if level > 0 and now[-1] == x:
                continue
            now.append(x)
            self.dfs(level + 1, m, now, last_line, color_dict)
            now.pop()
''',
    call='Solution().colorTheGrid(3, 3)',
    expect=246,
    skip=[27, 52, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19, 21, 22, 25, 29, 30, 32, 36, 37, 38, 39, 40, 45, 46, 47, 48, 49, 55, 56, 57, 58, 59, 60, 65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 77, 78, 79, 80, 82, 83, 84, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 108, 110, 111, 112, 113, 114, 115, 116, 117],
    max_steps=80,
    views=[
        dict(type='text', h=70, size=26,
             fn=lambda S: '`r g b` = 0 1 2 三种颜色；==任意换色、整行翻转==后相同的行算「本质相同」'),
        dict(type='map', var='color_dict', label='color_dict：类的代表 → 行数（第二轮 = 下一行落入各类的数目）', h=170,
             fmt=lambda k, v: f'{_pat(k)} : {v}'),
        dict(type='array', var='first_line', label='first_line：第一行各类的数目', h=175, cell=100),
        dict(type='table', var='base', label='base[i][j]：上一行是类 i，下一行落入类 j 的方案数', h=230, cell=100),
    ],
    watch=[('l', 'l', 'green'), ('first_line', 'first_line', 'blue')],
    captions={
        17: '第一次 DFS：枚举所有合法的一行（相邻不同，共 12 种），把==本质相同==的归成一类',
        107: lambda S, B, r: f'`{_pat(S.final)}` 和已有的类对不上（换色、翻转都不行）→ ==新的一类==，它当代表，数目记 1',
        76: lambda S, B, r: f'这一行和某类的代表 `{_pat(S.num)}` 经换色/翻转后相同 → 归入该类，数目 +1',
        81: '这一行和之前归过类的某行本质相同（`color_mapping` 记着它们的归属）→ 归入同一类，数目 +1',
        20: '本质不同的类共 `l = {l}` 个（m = 3 时只有 2 类）',
        23: '`base[i][j]`：上一行是类 i 时，下一行落入类 j 的方案数；先全部置 0',
        26: '`first_line` 记第一行每个类有几个亚种：`{first_line}`',
        27: '`color_index` 把类的代表映射成下标 `{index}`',
        31: lambda S, B, r: f'对类 `{_pat(B.color)}` 再 DFS 一次：下一行每格的颜色都要和上一行同位置不同，统计落入各类的数目',
        33: lambda S, B, r: f'`base[{S.color_index[S.color]}][{S.color_index[S.next_color]}] = {S.next_cnt}`：类 `{_pat(S.color)}` 的下一行有 `{S.next_cnt}` 种落入类 `{_pat(S.next_color)}`',
        35: '`final = base^(n-1)`：行与行之间转移 `n-1 = {B.n - 1}` 次，用矩阵快速幂',
        51: lambda S, B, r: ('`n = 1`：只剩 1 次方 → 直接返回 `base`' if S.n == 1 else f'`n = {S.n}`：不是 1，先递归算一半次幂'),
        52: '`base^1 = base`',
        54: '先递归算 `base^({B.n // 2})`（原文 `n / 2` 已改为 `n // 2`）',
        62: lambda S, B, r: (f'`tmp × tmp` = `base^{S.n}`，`n` 是偶数 → 直接返回' if S.n % 2 == 0 else '`n` 是奇数 → 还要再乘一个 `base`'),
        63: '返回 `base^n`',
        42: '`first_line × final`：把各类的数目加起来 = 全部方案数 = =={ret}==',
    },
    cards=dict(
        one_liner='把本质相同的一列归成一类，只在少数几类之间转移',
        complexity='时间 `O(l·3^m + l^3·log n)`，`m = 5` 时 `l = 6`',
        problem=['`m × n` 的网格，用红、绿、蓝给每个格子涂色，相邻格子颜色不同',
                 '返回涂色方案数（对 `10^9+7` 取模），`1 ≤ m ≤ 5`，`1 ≤ n ≤ 1000`',
                 '示例：`m = 5, n = 5` → `580986`；本视频：`m = 3, n = 3` → `246`'],
        quote='对于每种本质不同的状态，都执行一次dfs，计算其下一行可行的本质不同状态有哪些，以及有多少个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`rbr` 和 `brb` 换一下颜色就一样，`rgrb` 和 `brgr` 翻转后一样 → ==本质相同==，转移结果也相同',
              '`m = 3` 只有 `rgr`、`rgb` 两类（各 6 个亚种）；`m = 5` 也只有 6 类，而不是 48 种',
              '用 DFS 自动归类，再对每类 DFS 一次统计下一行落入各类的数目 → 得到 `l × l` 的矩阵 `base`',
              '`first × base^(n-1)` 各项求和就是答案，`base` 的幂用快速幂'],
        summary=['时间 `O(l·3^m + l^3·log n)`，空间 `O(l^2)`',
                 '`m = 1`、`m = 2` 有现成公式（`3·2^(n-1)`、`6·3^(n-1)`），代码里单独处理',
                 '归类用两种变换：颜色互换 `replace_list` 和整行翻转（`reverse_final`）',
                 '原文为 Python 2 写法，整数除法 `/` 共两处已改为 `//`（`n / 2`、`last_line / pow3`）',
                 '对比灵神：灵神直接用 `3·2^(m-1)` 个合法列做状压 DP；yiduobo 先用代码找规律把状态压到 `l` 类'],
    ),
)

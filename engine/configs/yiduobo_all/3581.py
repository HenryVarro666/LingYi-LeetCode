CONFIG = dict(
    num=3581, title='计算数字中的奇数字母数量', difficulty='Easy', category='模拟',
    author='yiduobo', technique='哈希表 · 数位拆分 + 字符计数',
    tags=[],
    code='''
class Solution(object):
    def countOddLetters(self, n):

        words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        cnt = {}
        while n:
            d = n % 10
            n //= 10
            for char in words[d]:
                cnt[char] = cnt.get(char, 0) + 1
        
        res = 0
        for char in cnt:
            if cnt[char] % 2 == 1:
                res += 1
        
        return res
''',
    call='Solution().countOddLetters(41)',
    expect=5,
    views=[
        dict(type='text', size=28, h=110, fn=lambda S: (
            f"当前数位 `d = {S['d']}` → 单词 ==`{S['words'][S['d']]}`==，剩下的 n = `{S['n']}`" if 'd' in S
            else '先把每个数位拆出来，再数单词里每个字母的次数')),
        dict(type='map', var='cnt', label='cnt：字母 → 出现次数（奇数的会被统计）', fmt=lambda k, v: f"'{k}': {v}", h=330, font=34),
        dict(type='text', size=28, h=110, fn=lambda S: (
            f"奇数次的字母数 `res = {S['res']}`" if 'res' in S else '')),
    ],
    watch=['n', ('d', 'd', 'blue'), ('char', 'char', 'pink'), ('res', 'res', 'green')],
    captions={
        'words = [': '建立数字 0~9 到英文单词的对应表，下标就是数字',
        'cnt = {}': '`cnt` 记录拼接后的字符串里每个字母出现几次（不真的拼接）',
        'while n': lambda S, B, r: (f'`n = {S.n}` 不为 0，还有数位没拆' if S.n else '`n = 0`：所有数位都拆完了，开始数奇数'),
        'd = n % 10': '模 10 取出最低位：`d = {n} % 10 = {d}`，对应单词 =={words[d]}==',
        'n //= 10': '除以 10 去掉最低位：`n` → {n}（原文为 Python 2 的 `/`，这里用 `//`）',
        'for char in words[d]': lambda S, B, r: (f"单词 `{S.words[S.d]}` 的字母处理完了" if B.get('char') == S.get('char') and B.get('d') == S.get('d')
                                                 else f"逐个字母处理单词 `{S.words[S.d]}`：`char = '{S.char}'`"),
        'cnt[char] = cnt.get': "字母 `'{char}'` 出现次数加一 → `cnt['{char}'] = {cnt[char]}`",
        'res = 0': '`res` 统计出现==奇数次==的字母种数',
        'for char in cnt': lambda S, B, r: ('所有字母都检查完了' if B.get('char') == S.get('char') and B.get('res') == S.get('res') and S.get('res', 0) >= 5
                                            else f"检查字母 `'{S.char}'`：出现 {S.cnt[S.char]} 次"),
        'if cnt[char] % 2 == 1': lambda S, B, r: (f"`{S.cnt[S.char]} % 2 == 1` → ==奇数次==，计入答案" if S.cnt[S.char] % 2 == 1
                                                  else f"`{S.cnt[S.char]} % 2 == 0` → 偶数次，不计"),
        'res += 1': '奇数次的字母又多一个：`res = {res}`',
        'return res': '出现奇数次的字母共 `{res}` 种',
    },
    max_steps=90,
    cards=dict(
        one_liner='先拆数位统计字母次数，再数出现奇数次的字母',
        complexity='时间 `O(log n)`，空间 `O(1)`（字母表大小固定）',
        problem=['把整数 `n` 的每个数位换成小写英文单词，按顺序拼成字符串 `s`',
                 '返回 `s` 中==出现奇数次==的字母有几种',
                 '本视频：`n = 41` → `fourone` → `f o u r o n e` 中 `f u r n e` 奇数次，`o` 两次 → `5`'],
        quote='先建立0到9这些数字到英文单词的哈希表，接下来通过模10除以10的方法分离出n的每个数位，使用另一个哈希表cnt统计这些数位对应的单词中每种字符出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用真的拼字符串，只关心每个字母出现的==总次数==',
              '`n % 10` 取最低位，`n //= 10` 去掉最低位，直到 `n` 为 0',
              '数位顺序不影响字母次数，所以倒着拆也没关系',
              '最后遍历 `cnt`，次数为奇数的字母数 +1'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：`n` 为 0 时循环不执行，答案是 0（题目 n 为正整数，不会遇到）',
                 '原文为 Python 2 写法，整数除法 `n /= 10` 已改为 `n //= 10`',
                 '字母顺序无关，只要统计次数的奇偶性即可'],
    ),
)

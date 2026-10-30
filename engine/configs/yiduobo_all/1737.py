CONFIG = dict(
    num=1737, title='满足三条件之一需改变的最少字符数', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举分界字符 + 前缀和', tags=[],
    code='''
class Solution(object):
    def minCharacters(self, a, b):

        cnt_a = [0] * 26
        cnt_b = [0] * 26

        for char in a:
            cnt_a[ord(char) - 97] += 1
        for char in b:
            cnt_b[ord(char) - 97] += 1

        len_a = len(a)
        len_b = len(b)

        res = len_a + len_b
        sum_a = sum_b = 0
        for index in range(26):
            res = min(res, len_a - cnt_a[index] + len_b - cnt_b[index])
            if index > 0:
                res = min(res, min(len_a - sum_a + sum_b, len_b - sum_b + sum_a))

            sum_a += cnt_a[index]
            sum_b += cnt_b[index]
        
        return res
''',
    call="Solution().minCharacters('aba', 'caa')",
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"枚举字符 `{chr(97+S['index'])}`：三种代价 ==全变== `{S['len_a']-S['cnt_a'][S['index']]+S['len_b']-S['cnt_b'][S['index']]}`，==a<b== `{S['len_a']-S['sum_a']+S['sum_b']}`，==b<a== `{S['len_b']-S['sum_b']+S['sum_a']}`" if 'index' in S and 'sum_a' in S and S['index'] > 0 else ''), size=28, h=80),
        dict(type='array', var='cnt_a', label='cnt_a（a 中各字母个数）', pointers={'index': 'yellow'}, cell=36, h=230,
             color=lambda S, i, v: 'green' if v else None, dim=lambda S, i, v: v == 0),
        dict(type='array', var='cnt_b', label='cnt_b（b 中各字母个数）', pointers={'index': 'yellow'}, cell=36, h=230,
             color=lambda S, i, v: 'blue' if v else None, dim=lambda S, i, v: v == 0),
    ],
    watch=['len_a', 'len_b', ('sum_a', 'sum_a', 'green'), ('sum_b', 'sum_b', 'blue'), 'index', ('res', 'res', 'orange')],
    captions={
        'cnt_a = [0]': '`cnt_a` 数组：26 个字母各出现几次，`a` → 下标 0',
        'cnt_b = [0]': '`cnt_b` 同理，统计 b',
        'cnt_a[ord(char) - 97] += 1': '`{char}` 映射到下标 `{ord(char)-97}`，`cnt_a` 对应位置 +1',
        'cnt_b[ord(char) - 97] += 1': '`{char}` 映射到下标 `{ord(char)-97}`，`cnt_b` 对应位置 +1',
        'res = len_a + len_b': '初始答案取上界 `{res}`：每个字符都改一次',
        'sum_a = sum_b = 0': '`sum_a/sum_b`：a、b 中小于当前字符的个数（前缀和），每轮末尾累加；`index > 0` 才有“更小的字符”',
        'for index in range(26)': '枚举分界字符 `{chr(97+index)}`（下标 {index}）',
        'res = min(res, len_a - cnt_a': '全变：a、b 全变成 `{chr(97+index)}`，要改 `{len_a} - {cnt_a[index]} + {len_b} - {cnt_b[index]}` 个 → res = =={res}==',
        'if index > 0': '下标 0 没有“更小的字符”，条件 1、2 只能从 `b` 开始枚举' ,
        'res = min(res, min(': 'a 全小于 `{chr(97+index)}`：a 中 >= 它的 `{len_a - sum_a}` 个要改，b 中 < 它的 `{sum_b}` 个要改；反过来 `{len_b - sum_b + sum_a}` → res = =={res}==',
        'sum_a += cnt_a[index]': '前缀和更新：`sum_a` → {sum_a}（含当前字符，给下一个字符用）',
        'sum_b += cnt_b[index]': '`sum_b` → {sum_b}',
        'return res': '最少改动 `{res}` 次',
    },
    skip=['if index > 0', 'sum_a += cnt_a[index]', 'sum_b += cnt_b[index]'],
    max_steps=64,
    cards=dict(
        one_liner='枚举分界字符，三种变法取最小',
        complexity='时间 `O(n+26)`，空间 `O(26)`',
        problem=['给两个小写字母串 `a`、`b`，每次操作可把任一字符改成任意小写字母',
                 '目标满足其一：a 严格小于 b；b 严格小于 a；a、b 只含同一种字母',
                 '求最少操作数。示例：`a="aba", b="caa"` → `2`'],
        quote='由于a和b由小写字母组成，那么就可以枚举所有的小写字符char，然后基于char就有三种可能的变化',
        quote_src='—— yiduobo 题解原文',
        idea=['先用计数数组 `cnt_a`、`cnt_b` 统计各字母个数',
              '全变成 char：代价 `len - cnt[char]`，a、b 各算一次',
              'a 全 < char、b 全 >= char：代价 `len_a - sum_a + sum_b`，反过来对称',
              '前缀和 `sum_a`、`sum_b` 在枚举中顺手累加'],
        summary=['时间 `O(n+26)`，空间 `O(26)`',
                 '易错：分界字符不能是 `a`，因为没有比 a 更小的字符，所以 `index > 0` 才算条件 1、2',
                 '易错：前缀和要在比较之后再加当前字符，保证只含“小于”的部分',
                 '原文代码无需修改，直接运行'],
    ),
)

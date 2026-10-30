CONFIG = dict(
    num=2802, title='找出第K个幸运数字', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='特殊二进制 · 7 视为 2',
    tags=[],
    code='''
class Solution(object):
    def kthLuckyNumber(self, k):

        res = []
        while k:
            v = k % 2
            if v == 0:
                res.append('7')
                k -= 2
            else:
                res.append('4')
            
            k //= 2

        return ''.join(res[::-1])
''',
    call='Solution().kthLuckyNumber(10)',
    expect='477',
    views=[
        dict(type='text', fn=lambda S: ('幸运数字：只含数字 4 和 7。按大小：4, 7, 44, 47, 74, 77, 444, 447, 474, 477 ...　第 10 个是 ==477=='
                                        if 'k' in S else ''), size=24),
        dict(type='text', fn=lambda S: f"当前 `k = {S['k']}`　　`k` 的奇偶决定这一位：奇数 → ==4==，偶数 → ==7==（并先减 2）" if 'k' in S else '', size=26),
        dict(type='array', var='res', label='res（从最低位开始放，最后要倒转）', cell=100,
             color=lambda S, i, v: 'green' if v == '4' else 'orange'),
    ],
    watch=[('k', 'k', 'blue'), ('v', 'v'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 从==最低位==开始存放每一位数字',
        'while k': lambda S, B, r: (f'`k = {S.k}` 还不为 0，继续拆下一位' if S.k else '`k = 0`：所有位都拆完了'),
        'v = k % 2': '`v = {k} % 2 = {v}`：看 `k` 是奇数还是偶数',
        'if v == 0': lambda S, B, r: ('`v == 0`：4 当作 1，7 当作==没有进位的 2==；偶数说明这一位是 2，即 ==7==' if S.v == 0
                                      else '`v == 1`：这一位是 1，即 ==4=='),
        "res.append('7')": '这一位填 `7`：`res = {res}`',
        'k -= 2': '7 代表 2 而不是 0，先减去 2：`k = {k}`，再除以 2 才对得上',
        "res.append('4')": '这一位填 `4`：`res = {res}`',
        'k //= 2': '去掉已处理的最低位：`k` → {k}',
        'return': '`res` 是反的，倒转后得到 `"{ret}"`',
    },
    cards=dict(
        one_liner='把 4 当 1、7 当 2，就是一种没有 0 的二进制',
        complexity='时间 `O(log k)`，空间 `O(log k)`',
        problem=['幸运数字：每一位都只能是 ==4 或 7== 的正整数',
                 '把所有幸运数字从小到大排好，返回第 `k` 个（字符串）',
                 '本视频：`k = 10` → `"477"`（4,7,44,47,74,77,444,447,474,477）'],
        quote='将其视为某种特殊的二进制表示……将4视为1，而7则视为没有进位的2。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度为 `n` 的幸运数字有 `2^n` 个，每位 4 或 7 两种选择',
              '4=1，7=2（不是 0）：像二进制，但每位取值 1 或 2',
              '奇数 → 填 4；偶数 → 填 7，并先 `k -= 2`，再 `k //= 2`'],
        result='`k = 10` → `"477"` ✓',
        summary=['时间 `O(log k)`，空间 `O(log k)`',
                 '易错：偶数时要先 `k -= 2` 再除以 2，否则会错位',
                 '易错：从低位往高位生成，最后必须倒转 `res[::-1]`',
                 '原文为 Python 2 风格，`k /= 2` 为整数除法，已改为 `k //= 2`'],
    ),
)

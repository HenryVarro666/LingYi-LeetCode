CONFIG = dict(
    num=443, title='压缩字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='一趟扫描 + 原地写入',
    code='''
class Solution(object):
    def compress(self, chars):
        
        res_len = 0
        now = None
        cnt = 0
        for char in chars:
            if now == char:
                cnt += 1
            else:
                if now is not None:
                    chars[res_len] = now
                    res_len += 1
                    if cnt > 1:
                        cnt_len = 0
                        tmp = cnt
                        while tmp:
                            tmp //= 10
                            cnt_len += 1
                        tmp_len = cnt_len
                        while cnt:
                            chars[res_len + tmp_len - 1] = chr(cnt % 10 + 48)
                            tmp_len -= 1
                            cnt //= 10
                        res_len += cnt_len

                now = char
                cnt = 1

        if now:
            chars[res_len] = now
            res_len += 1
            if cnt > 1:
                cnt_len = 0
                tmp = cnt
                while tmp:
                    tmp //= 10
                    cnt_len += 1
                tmp_len = cnt_len
                while cnt:
                    chars[res_len + tmp_len - 1] = chr(cnt % 10 + 48)
                    tmp_len -= 1
                    cnt //= 10
                res_len += cnt_len

        return res_len
''',
    setup='chars = list("aabbbbbbbbbbc")',
    call='Solution().compress(chars)',
    expect=6,
    views=[
        dict(type='array', var='chars', label='chars（原地改写）', h=230, cell=64,
             pointers={'res_len': 'green'},
             color=lambda S, i, v: 'green' if 'res_len' in S and i < S['res_len'] else None),
        dict(type='text', h=120, fn=lambda S: f"当前字符 `{S['now']}` 连续 =={S['cnt']}== 次；已写入长度 `res_len = {S['res_len']}`" if S.get('now') else ''),
    ],
    watch=['now', 'cnt', ('res_len', 'res_len', 'green'), 'cnt_len', 'tmp_len'],
    skip=['res_len = 0', 'now = None', 'cnt = 0', 'cnt = 1', 'for char in chars', 'cnt_len = 0', 'tmp = cnt', 'cnt_len += 1', 'tmp_len -= 1'],
    max_steps=90,
    captions={
        'if now == char': '`char = {char}`，和当前统计的 `now = {now}` 比较：相同就累加次数，不同说明上一段结束',
        'cnt += 1': '`char = {char}` 和 `now = {now}` 相同：同一段又多一个，`cnt = {cnt}`',
        'chars[res_len] = now': '上一段结束：把字符 `{now}` 写到 `chars[{res_len}]`（写指针永远不超过读指针，不会覆盖没读的）',
        'if cnt > 1': '次数 `{cnt}` 大于 1 才需要写数字，等于 1 只写字符本身',
        'tmp //= 10': '先数位数：`tmp` 每次去掉一位 → {tmp}，位数 `cnt_len = {cnt_len+1}`',
        'chars[res_len + tmp_len - 1]': '逐位写数字：`cnt % 10` 是最低位，所以==从右往左写==，放到 `chars[{res_len + tmp_len - 1}]`，高位在左',
        'cnt //= 10': '去掉最低位，`cnt = {cnt}`',
        'res_len += cnt_len': '数字写完，写指针后移 `{cnt_len}` 位：`res_len = {res_len}`',
        'now = char': '开始统计新字符 `{char}`，`cnt` 重置为 1',
        'if now:': '循环结束，最后一段还没写入，需要同样处理一次',
        'return res_len': '压缩后长度 =={ret}==，`chars` 前 {ret} 位是 `{chars[:ret]}`',
    },
    cards=dict(
        one_liner='一趟扫描数连续次数，次数大于 1 就把数字逐位写回',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把字符数组 `chars` 原地压缩：连续相同字符写成 `字符 + 次数`',
                 '次数为 1 只写字符；次数 >= 10 要拆成多个字符',
                 '返回压缩后的长度',
                 '示例：`aabbbbbbbbbbc`（b 共 10 个）→ `a2b10c`，返回 `6`'],
        quote='一趟扫描统计每个字符连续出现的次数，若cnt大于1，那么就需要进行压缩。需要注意的是，在将cnt放入chars数组中时，如果使用mod 10取余的做法逐位放进去，那么需要将高位放在左边低位放在右边。',
        quote_src='—— yiduobo 题解',
        idea=['`now`、`cnt` 记录当前这一段的字符和长度',
              '字符变了，就把上一段写回 `chars[res_len]`，写指针只会落后于读指针',
              '写数字：先数出位数，再用 `% 10` 从右往左填，保证高位在左'],
        summary=['时间 `O(n)`，空间 `O(1)`（原地修改）',
                 '易错点：数字要从最低位往左填，否则 `10` 会写成 `01`',
                 '循环结束后最后一段还要再写一次',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`'],
    ),
)

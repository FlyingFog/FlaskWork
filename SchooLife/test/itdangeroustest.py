from itsdangerous import TimedJSONWebSignatureSerializer as Ser

s = Ser("aaaa" ,expires_in=3600)
token = s.dumps({'uid':1})
print(token)
token1 = str(token)
token1 = token1[2:-1]
print(token1)
token2 = token1.encode(encoding='utf-8')
print(type(token2))
data1 = s.loads(token2)
print(data1)
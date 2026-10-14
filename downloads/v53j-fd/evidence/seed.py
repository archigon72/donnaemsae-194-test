import json
def state():
  tx=[('t1','a1','329200','2026-01-02',0,'10','5000'),('t2','a1','0004G0','2026-01-02',1,'20','9000'),('t3','a2','0018C0','2026-03-03',0,'30','10000'),('t4','a1','0004G0','2026-06-01',0,'5','8800')]
  T=[]
  for i,a,c,d,o,q,p in tx: T.append(dict(transaction_id=i,account_id=a,code=c,cycle_id='cy-'+a+c,type='add_buy' if i=='t4' else 'initial_buy',trade_date=d,order_key=o,quantity=q,trade_price=p))
  return dict(schema_version=1,created_at='2026-10-14T00:00:00.000Z',accounts=[dict(account_id='a1',name='표본 일반',type='일반'),dict(account_id='a2',name='표본 ISA',type='ISA')],
    dividend_confirmations=[dict(account_id='a1',distribution_id='329200-20260929',amount='280',confirmed_at='2026-10-14T00:00:00Z')],transactions=T,dividend_uses=[],metadata=dict(app='donnaemsae-lab',scope='user-facts'))

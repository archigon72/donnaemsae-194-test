"""종목별 표시 JSON 생성기 (v5.3e 복구, GrokBot 자체 검증)
입력 : inputs/<code>.json (번들) + runtime_source.zip (period_bridge.py + 원본 adapter/Core) + presentation.py + facts_projection.py + data/catalog.json
출력 : data/<code>.json = {snapshot, ticker, periods{1개월,6개월,1년,전체}, presentations{...}[, core_note]}
규칙 : periods[k]      = period_bridge.run_period(번들+period=k, 시작, 종료)   (앱 Web Worker 직접지정과 같은 함수)
       presentations[k]= presentation.detail_presentation(periods[k], 번들)   (Worker와 같은 함수)
       snapshot        = catalog.snapshot (배포 기준점; phase-data.js가 일치 검사), 원 입력 기준점은 periods[k].proof_meta 에 보존
       시작·종료        = run_period 가 requested_period 를 정하는 규칙 그대로(마지막 유효 NAV 기준 1·6개월/1년, 전체=첫 유효 NAV)
       core_note       = 번들 meta.snapshot_id 별 고정 문구(ETF82 배치만)
계산식은 새로 만들지 않는다. 금융 계산은 모두 원본 adapter/Core 안에서만 일어난다.
사용 : python3 pipeline/build_ticker_json.py <site_root> <out_dir> [code ...]     (out_dir=site_root/data 이면 덮어씀)
"""
import sys,os,json,zipfile,tempfile,datetime
ROOT=os.path.abspath(sys.argv[1]);OUT=os.path.abspath(sys.argv[2]);ONLY=sys.argv[3:]
RT=tempfile.mkdtemp(prefix='rt-');zipfile.ZipFile(f'{ROOT}/runtime_source.zip').extractall(RT)
sys.path[:0]=[RT,ROOT];sys.dont_write_bytecode=True
import period_bridge as PB,adapter,presentation as P
PERIODS=['1개월','6개월','1년','전체']
NOTES={'ETF82_Grok_20261011':'2026-10-12 actual period_bridge/CORE execution on normalized ETF82 inputs. zeroin metadata missing as supplied. Existing 112 untouched.'}
CAT=json.load(open(f'{ROOT}/data/catalog.json'))
def window(b,k):
    nav,_=PB.normalize(b['nav_rows']);dates=sorted(adapter.day(r['gijunYmd']) for r in nav)
    if not dates:return None,None
    last=datetime.date.fromisoformat(dates[-1])
    s=str(adapter.shift_month(last,int(k[0]))) if k in('1개월','6개월') else str(adapter.shift_year(last,1)) if k=='1년' else dates[0]
    return s,dates[-1]
def build(code):
    b=json.load(open(f'{ROOT}/inputs/{code}.json'))
    out={'snapshot':CAT['snapshot'],'ticker':code,'periods':{},'presentations':{}}
    for k in PERIODS:
        bb=dict(b);bb['period']=k;s,e=window(b,k)
        v=json.loads(json.dumps(PB.run_period(bb,s,e)))
        out['periods'][k]=v;out['presentations'][k]=json.loads(json.dumps(P.detail_presentation(v,bb)))
    if b['meta'].get('snapshot_id') in NOTES:out['core_note']=NOTES[b['meta']['snapshot_id']]
    return out
if __name__=='__main__':
    os.makedirs(OUT,exist_ok=True)
    codes=ONLY or sorted(f[:-5] for f in os.listdir(f'{ROOT}/inputs') if f.endswith('.json'))
    for c in codes:
        open(f'{OUT}/{c}.json','w').write(json.dumps(build(c),ensure_ascii=False,separators=(',',':')))
    print('built',len(codes))

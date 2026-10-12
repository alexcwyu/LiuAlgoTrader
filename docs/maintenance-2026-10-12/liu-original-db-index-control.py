"""One-off compatibility proof using real rows from the original repository dump."""
import asyncio,json,os,ast,subprocess
from pathlib import Path
import asyncpg,pandas as pd
from liualgotrader.common.data_loader import SymbolData, _get_index_location
from liualgotrader.common.types import TimeScale
from liualgotrader.data.gemini import GeminiData

async def main():
 conn=await asyncpg.connect(Path('/Users/alex/workspaces/trading/.runtime/maintenance-2026-10-12/liu-owned-db-d744.dsn').read_text())
 try:
  symbol=await conn.fetchval('SELECT symbol FROM stock_ohlc ORDER BY symbol LIMIT 1')
  rows=await conn.fetch('SELECT symbol_date,open,high,low,close,volume FROM stock_ohlc WHERE symbol=$1 ORDER BY symbol_date LIMIT 64',symbol)
 finally:await conn.close()
 assert len(rows)>3
 frame=pd.DataFrame([dict(x) for x in rows]).set_index('symbol_date')
 frame.index=pd.to_datetime(frame.index)
 item=SymbolData(GeminiData(),symbol,TimeScale.day,1,prefetched_data=frame)
 key=frame.index[3]
 outer=lambda item,key,method='ffill':item._get_index(key,method)
 column=lambda item,key,method='ffill':item.close._get_index(key,method)
 baseline=bool(os.environ.get('LIU_INDEX_BASELINE'))
 if baseline:
  import liualgotrader.common.data_loader as owner
  source=subprocess.check_output(['git','show','d7442026:src/liualgotrader/common/data_loader.py'],text=True)
  original=next(n for n in ast.parse(source).body if isinstance(n,ast.ClassDef) and n.name=='SymbolData')
  nested=next(n for n in original.body if isinstance(n,ast.ClassDef) and n.name=='_Column')
  def original_method(nodes):
   node=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name=='_get_index')
   namespace=vars(owner).copy()
   exec(compile(ast.Module(body=[node],type_ignores=[]),'<genuine-original-method>','exec'),namespace)
   return namespace['_get_index']
  outer=original_method(original.body)
  legacy_column=original_method(nested.body)
  column=lambda item,key,method='ffill':legacy_column(item.close,key,method)
 results={'genuine_source':'original database/liu_dump.sql stock_ohlc COPY rows','symbol':symbol,'rows':len(rows),'checks':{}}
 for label,operation in [('symbol_exact',lambda:outer(item,key)),('column_exact',lambda:column(item,key)),('symbol_ffill',lambda:outer(item,key+pd.Timedelta(hours=1))),('column_nearest',lambda:column(item,key+pd.Timedelta(hours=1),method='nearest'))]:
  try:
   index=operation();assert index==3
   results['checks'][label]={'pass':True,'position':int(index)}
  except TypeError as exc:results['checks'][label]={'pass':False,'error':str(exc)}
 try:
  _get_index_location(frame.index,frame.index[0]-pd.Timedelta(days=1),'ffill')
  raise AssertionError('missing match did not raise')
 except KeyError:
  results['missing_match_preserves_KeyError']=True
 results['original_baseline_source_executed']=baseline
 path=Path(os.environ.get('LIU_INDEX_CONTROL_RESULT' ,'docs/maintenance-2026-10-12/liu-db-index-control-after.json'))
 path.write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
asyncio.run(main())

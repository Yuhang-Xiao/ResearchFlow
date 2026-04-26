from pathlib import Path
import pandas as pd, json, csv
base = Path(r'D:\桌面\codex\workflow1')
files = [
 ('cleaned', base/'data/03_primary/peanut_cleaned_analysis_ready.csv'),
 ('concentration', base/'data/04_feature/peanut_concentration_clean_table.csv'),
 ('count_panel', base/'data/04_feature/peanut_count_panel.csv'),
 ('belief_states', base/'data/04_feature/peanut_beta_binomial_belief_states.csv'),
 ('state_features', base/'data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv'),
 ('risk_table', base/'data/04_feature/peanut_edi_moe_risk_table.csv'),
 ('risk_summary', base/'data/04_feature/peanut_edi_moe_risk_summary.csv'),
]
outdir = Path(r'D:\桌面\codex\workflow1\outputs\工作包\20260426_1616_DQN文献增强建模方案与参数确认')
rows=[]
schema_rows=[]
for name,path in files:
    info={'name':name,'path':str(path),'exists':path.exists()}
    if path.exists():
        try:
            df=pd.read_csv(path, nrows=5000, encoding='utf-8-sig')
        except UnicodeDecodeError:
            df=pd.read_csv(path, nrows=5000)
        # count rows with chunking
        total=0
        for chunk in pd.read_csv(path, chunksize=200000, encoding='utf-8-sig'):
            total += len(chunk)
        info.update({'rows':total,'columns':len(df.columns),'sample_columns':' | '.join(map(str, df.columns[:40]))})
        for col in df.columns:
            nonnull = int(df[col].notna().sum())
            schema_rows.append({'table':name,'column':col,'sample_nonnull_first5000':nonnull,'dtype_sample':str(df[col].dtype),'sample_values':' | '.join(map(str, df[col].dropna().astype(str).head(5).tolist()))[:500]})
    rows.append(info)
pd.DataFrame(rows).to_csv(outdir/'02_表格输出/upstream_file_inventory.csv', index=False, encoding='utf-8-sig')
pd.DataFrame(schema_rows).to_csv(outdir/'02_表格输出/upstream_schema_inventory.csv', index=False, encoding='utf-8-sig')
# quick consistency checks
checks=[]
def read(path): return pd.read_csv(path, encoding='utf-8-sig')
cp=read(base/'data/04_feature/peanut_count_panel.csv')
bs=read(base/'data/04_feature/peanut_beta_binomial_belief_states.csv')
sf=read(base/'data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv')
conc=read(base/'data/04_feature/peanut_concentration_clean_table.csv')
risk=read(base/'data/04_feature/peanut_edi_moe_risk_table.csv')
checks.append({'check':'count_panel_rows','value':len(cp),'status':'info'})
checks.append({'check':'belief_state_rows','value':len(bs),'status':'pass' if len(bs)==len(cp) else 'fail'})
checks.append({'check':'state_feature_rows','value':len(sf),'status':'pass' if len(sf)==len(cp) else 'fail'})
for table_name,df in [('count_panel',cp),('belief_states',bs),('state_features',sf)]:
    checks.append({'check':f'{table_name}_duplicate_rows','value':int(df.duplicated().sum()),'status':'pass' if int(df.duplicated().sum())==0 else 'warn'})
# likely key cols
for dfname,df in [('count_panel',cp),('state_features',sf)]:
    checks.append({'check':f'{dfname}_columns','value':' | '.join(df.columns[:30]),'status':'info'})
checks.append({'check':'concentration_rows','value':len(conc),'status':'info'})
num_cols=[c for c in conc.columns if '浓度' in c or '数值' in c]
for c in num_cols[:8]:
    vals=pd.to_numeric(conc[c], errors='coerce')
    checks.append({'check':f'concentration_numeric_{c}_nonmissing','value':int(vals.notna().sum()),'status':'info'})
    checks.append({'check':f'concentration_numeric_{c}_negative','value':int((vals<0).sum()),'status':'pass' if int((vals<0).sum())==0 else 'fail'})
checks.append({'check':'risk_table_rows','value':len(risk),'status':'info'})
pd.DataFrame(checks).to_csv(outdir/'02_表格输出/upstream_consistency_checks.csv', index=False, encoding='utf-8-sig')
md=['# 上游产物审计摘要','']
for r in rows:
    md.append(f"- {r['name']}: exists={r['exists']}, rows={r.get('rows','NA')}, columns={r.get('columns','NA')}")
md.append('')
md.append('完整 schema 与一致性检查见 `02_表格输出/upstream_schema_inventory.csv` 和 `02_表格输出/upstream_consistency_checks.csv`。')
(outdir/'04_报告输出/upstream_output_audit_report.md').write_text('\n'.join(md), encoding='utf-8')
print('ok')

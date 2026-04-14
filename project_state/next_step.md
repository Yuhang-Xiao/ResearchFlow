# Next Step

After schema profiling, the next recommended task is to define raw data validation rules before cleaning or modeling. Start with checks for expected columns, row identity or composite key candidates, date parsing for `生产日期` and `通报时间`, missingness thresholds, mixed-type handling for `检测数值` and `法规限制`, and whether `判定结果` is expected to contain more than one class.

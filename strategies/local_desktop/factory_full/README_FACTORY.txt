STRATEGY FACTORY - how to run on your PC (Windows)
===================================================
Everything is Python 3. You already have Anaconda installed.

1) One-time install:
   pip install pandas numpy pyarrow scikit-learn

2) Put this folder next to your data. It expects your MT5 exports at:
   data\EURUSD_M1_export.csv  (copy from gravity_engine\data\)
   data\GBPUSD_M1_export.csv, XAUUSD, US500 same pattern

3) Run in this order:
   python prep.py            (parses CSVs -> data\clean\)
   python sweep.py           (GV-014 grid backtests)
   python wf.py              (walk-forward + 30-day OOS report)
   python gv15.py            (GV-015 Tunnel Rider backtest)
   python ml15.py            (ML meta-labeler on GV-015 signals)

Open any .py file with VS Code, Cursor, or Notepad - they are plain text.
ml15.py = the machine-learning overlay (scikit-learn HistGradientBoosting).

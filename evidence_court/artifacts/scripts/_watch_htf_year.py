import time, pathlib, sys
log = pathlib.Path(r"C:\Users\user\.grok\sessions\C%3A%5CUsers%5Cuser%5COneDrive%5CDesktop%5CThe%20Creator\019fe0d8-84db-7ce1-ac01-e289934264e3\terminal\call-52f5ad82-1443-42d7-a8a2-92ad79b0f655-213.log")
report = pathlib.Path(r"C:\Users\user\OneDrive\Desktop\The Creator\evidence_court\artifacts\htf_active_year_train_report.json")
partial = pathlib.Path(r"C:\Users\user\OneDrive\Desktop\The Creator\evidence_court\artifacts\path_state_teachers_htf_active_year.partial.json")
last = ""
while True:
    msg = None
    if report.exists():
        msg = "DONE"
        print(msg, flush=True)
        break
    if partial.exists():
        try:
            import json
            p = json.loads(partial.read_text(encoding="utf-8"))
            cur = f"HARVEST_DAY_{p.get('days_done')}_ex_{p.get('n_examples')}"
            if cur != last:
                last = cur
                # only print DONE/FAILED/CANCELLED style - monitor wants sparse
                pass
        except Exception:
            pass
    if log.exists():
        t = log.read_text(encoding="utf-8", errors="replace")
        if "No champion replace" in t or "replacing champion" in t or "promoted" in t.lower():
            if "Traceback" in t[-3000:]:
                print("FAILED", flush=True)
            else:
                # wait for report file
                pass
        if "Traceback" in t and "Error" in t[-1500:]:
            # might still be running; only fail if process done - check later
            pass
    time.sleep(120)

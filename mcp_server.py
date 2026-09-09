import sys
import json
from client import RCUEngine

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "rcu_cycle":
        rcu = RCUEngine()
        rcu.rcu_read_lock("t1")
        rcu.rcu_assign_pointer(params.get("val", 999))
        s1 = rcu.synchronize_rcu()
        rcu.rcu_read_unlock("t1")
        s2 = rcu.synchronize_rcu()
        return {"before_unlock": s1, "after_unlock": s2}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()

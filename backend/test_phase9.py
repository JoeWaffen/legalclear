import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.payments import check_access

def test():
    # 1. Subscription user always allowed
    r = check_access(
        {"subscription_status": "active",
         "free_doc_used": True})
    assert r["allowed"] == True
    assert r["payment_type"] == "subscription"
    print("1. Subscription access OK")

    # 2. Free doc not yet used
    r = check_access(
        {"subscription_status": "free",
         "free_doc_used": False})
    assert r["allowed"] == True
    assert r["payment_type"] == "free"
    print("2. Free doc access OK")

    # 3. Free doc used + payment confirmed
    r = check_access(
        {"subscription_status": "free",
         "free_doc_used": True},
        {"payment_status": "paid"})
    assert r["allowed"] == True
    assert r["payment_type"] == "payg"
    print("3. PAYG access OK")

    # 4. Free doc used + no payment
    r = check_access(
        {"subscription_status": "free",
         "free_doc_used": True},
        {"payment_status": "pending"})
    assert r["allowed"] == False
    print("4. Blocked access OK")

    print("\nALL PHASE 9 ASSERTIONS PASSED")

test()

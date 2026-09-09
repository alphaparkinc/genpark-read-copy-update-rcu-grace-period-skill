from client import RCUEngine

def main():
    print("=== Testing RCU Grace Period Engine ===")
    rcu = RCUEngine()
    rcu.rcu_read_lock("thread_1")
    val1 = rcu.rcu_dereference()
    print("Thread 1 dereference:", val1)

    # Writer updates pointer
    rcu.rcu_assign_pointer(500)

    # Grace period cannot finish while thread_1 is holding read lock
    sync_blocked = rcu.synchronize_rcu()
    print("Sync while locked:", sync_blocked)
    assert sync_blocked['grace_period_complete'] is False

    # Thread 1 unlocks
    rcu.rcu_read_unlock("thread_1")
    sync_passed = rcu.synchronize_rcu()
    print("Sync after unlock:", sync_passed)
    assert sync_passed['grace_period_complete'] is True

    print("RCU Engine verified successfully!")

if __name__ == '__main__':
    main()

class RCUEngine:
    """Read-Copy Update (RCU) Grace Period Engine."""
    def __init__(self):
        self.data_pointer = {"val": 100, "version": 1}
        self.reader_epochs = {}
        self.callbacks = []
        self.current_epoch = 0

    def rcu_read_lock(self, thread_id):
        self.reader_epochs[thread_id] = self.current_epoch

    def rcu_read_unlock(self, thread_id):
        self.reader_epochs[thread_id] = None

    def rcu_dereference(self):
        return dict(self.data_pointer)

    def rcu_assign_pointer(self, new_val):
        old_ptr = self.data_pointer
        self.data_pointer = {"val": new_val, "version": old_ptr["version"] + 1}
        self.current_epoch += 1

        reclaimed = []
        def reclaim(old_data):
            reclaimed.append(old_data['version'])

        self.callbacks.append({'epoch': self.current_epoch, 'fn': reclaim, 'arg': old_ptr})
        return self.data_pointer

    def synchronize_rcu(self):
        active_readers = [t for t, ep in self.reader_epochs.items() if ep is not None and ep < self.current_epoch]
        if not active_readers:
            executed = 0
            remaining_cbs = []
            for cb in self.callbacks:
                if cb['epoch'] <= self.current_epoch:
                    cb['fn'](cb['arg'])
                    executed += 1
                else:
                    remaining_cbs.append(cb)
            self.callbacks = remaining_cbs
            return {'grace_period_complete': True, 'callbacks_executed': executed}
        return {'grace_period_complete': False, 'blocked_by': active_readers}

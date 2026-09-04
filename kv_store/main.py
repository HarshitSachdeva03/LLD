import time
import concurrent.futures
from store import ThreadSafeKVStore


def simulate_client_worker(store: ThreadSafeKVStore, worker_id: int) -> None:
    """Simulates a client writing, reading, and waiting for TTL expiration."""
    key = f"user_{worker_id}_session"
    
    # 1. Set the key with a 1-second TTL
    print(f"[Worker {worker_id}] Setting {key} with TTL=1s")
    store.set(key, f"token_{worker_id}", ttl_seconds=1 if worker_id<3 else 2)
    
    # 2. Read immediately (Should succeed)
    val = store.get(key)
    print(f"[Worker {worker_id}] Immediate Read: {val}")
    
    # 3. Simulate time passing (Force thread to yield control)
    time.sleep(1.2)
    
    # 4. Read again to trigger Lazy Eviction (Should fail/return None)
    val_expired = store.get(key)
    print(f"[Worker {worker_id}] Read after 1.2s: {val_expired}")


if __name__ == "__main__":
    store = ThreadSafeKVStore()
    
    print("--- Starting Concurrent KV Store Test ---")
    
    # Spawn 3 concurrent worker threads to test our locking mechanism
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks to the thread pool
        futures = [
            executor.submit(simulate_client_worker, store, worker_id)
            for worker_id in range(1, 4)
        ]
        
        # Wait for all futures to finish execution
        concurrent.futures.wait(futures)
        
    print("--- Test Complete ---")
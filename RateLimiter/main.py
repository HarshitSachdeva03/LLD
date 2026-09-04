import concurrent.futures
import time
from models import RateLimitRule
from factory import AlgorithmType
from manager import RateLimiter


def simulate_client_traffic(limiter: RateLimiter, client_id: str, request_count: int, delay_sec: float) -> tuple[str, int, int]:
    """Simulates rapid incoming requests from a client thread."""
    allowed = 0
    blocked = 0

    for _ in range(request_count):
        if limiter.allow_request(client_id):
            allowed += 1
        else:
            blocked += 1
        time.sleep(delay_sec)

    return client_id, allowed, blocked


if __name__ == "__main__":
    # Rule: Max 5 requests per 2-second window
    rule = RateLimitRule(max_requests=5, time_window_seconds=2)
    
    # Easily swap AlgorithmType.FIXED_WINDOW or AlgorithmType.SLIDING_WINDOW_LOG
    limiter = RateLimiter(rule=rule, algo_type=AlgorithmType.SLIDING_WINDOW_LOG)

    clients = ["user_101", "user_202"]

    print("--- Executing Multi-Threaded Simulation ---")
    
    # Simulate concurrent thread execution across multiple worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(simulate_client_traffic, limiter, client, request_count=8, delay_sec=0.05)
            for client in clients
        ]

        for future in concurrent.futures.as_completed(futures):
            client_id, allowed, blocked = future.result()
            print(f"[{client_id}] Allowed: {allowed} | Blocked: {blocked}")
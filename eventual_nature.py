import uuid
import requests

US_IP = "34.63.169.199"
EU_IP = "35.205.122.149"
PORT = 8080

REGISTER_URL = f"http://{US_IP}:{PORT}/register"
LIST_URL = f"http://{EU_IP}:{PORT}/list"

ITERATIONS = 100
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 15


def unique_username() -> str:
    return f"user-{uuid.uuid4().hex}"


def extract_user_list(response: requests.Response) -> list[str]:
    data = response.json()
    if isinstance(data, dict) and isinstance(data.get("users"), list):
        return [str(x) for x in data["users"]]
    if isinstance(data, list):
        return [str(x) for x in data]
    return []


def main():
    misses = 0
    errors = 0

    print("Observing Eventual Consistency")
    print(f"Registering on US: {REGISTER_URL}")
    print(f"Listing from EU:   {LIST_URL}")
    print(f"Iterations: {ITERATIONS}\n")

    for i in range(ITERATIONS):
        username = unique_username()

        try:
            # Register on US
            r_reg = requests.post(
                REGISTER_URL,
                json={"username": username},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            print(f"added {username} to US server")

            # Immediately get list from EU node
            r_list = requests.get(
                LIST_URL,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )

            users = extract_user_list(r_list)
            print(f"Read {users} from EU server")
            found = username in users
            if not found:
                misses += 1

            if (i + 1) % 10 == 0:
                print(f"Progress {i+1}/{ITERATIONS} | misses: {misses} | errors: {errors}")

        except Exception as e:
            errors += 1
            print(f"Iteration {i+1}: ERROR - {type(e).__name__}: {e}")

    print("\nResults")
    print(f"Not found immediately (misses): {misses} / {ITERATIONS}")
    print(f"Request/processing errors:      {errors} / {ITERATIONS}")
    # Clearing
    r = requests.post(f"http://{US_IP}:8080/clear", timeout=10)
    print(US_IP, r.status_code, r.text)



if __name__ == "__main__":
    main()
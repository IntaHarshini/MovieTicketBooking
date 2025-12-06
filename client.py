import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))

    user_id = input("Enter your User ID (any name/number): ")
    print("\nCommands you can use:")
    print("   REQUEST 5                → book one seat")
    print("   REQUEST 2 3 4 5          → book multiple seats together")
    print("   CANCEL 3                 → cancel your seat")
    print("   CANCEL 1 5 8             → cancel multiple seats")
    print("   exit                     → close\n")

    try:
        while True:
            cmd = input(f"{user_id} > ").strip()
            if cmd.lower() == "exit":
                break
            if not cmd:
                continue
            parts = cmd.split()
            action = parts[0].upper()
            # THIS IS THE FIXED PART → allows 1 or more seats!
            if action in ["REQUEST", "CANCEL"] and len(parts) >= 2:
                # Send the full command exactly as typed (e.g., "REQUEST 2 3 4 5")
                message = " ".join(parts).upper()
                client.send(message.encode('utf-8'))

                response = client.recv(1024).decode('utf-8')
                status, msg = response.split("|", 1)
                if status in ["SUCCESS", "CANCELLED"]:
                    print(f"Success: {msg}")
                else:
                    print(f"Failed: {msg}")
            else:
                print("Invalid command! Examples:")
                print("   REQUEST 7")
                print("   REQUEST 1 2 3 4")
                print("   CANCEL 5")
                print("   CANCEL 2 8")

    except Exception as e:
        print("Server closed or error.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
import socket
import threading
from datetime import datetime

#theater Configuration
TOTAL_SEATS = 25 #example
seats = ["Available"] * TOTAL_SEATS
booked_by = ["-"] * TOTAL_SEATS
lock = threading.Lock()

def print_table():
    print("\n" + "="*60)
    print(f"     MOVIE TICKET BOOKING STATUS - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    print(f"{'Seat':<6} {'Status':<12} {'Booked By'}")
    print("-"*60)
    for i in range(TOTAL_SEATS):
        status = seats[i] if seats[i] == "Available" else "BOOKED"
        print(f"{i+1:<6} {status:<12} {booked_by[i]}")
    print("="*60 + "\n")

def handle_client(conn, addr):
    user_id = f"User-{addr[1]}"  #port num
    print(f"→ {user_id} connected from {addr}")

    try:
        while True:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data: break

            parts = data.split()
            action = parts[0].upper()

            with lock:  
                response = ""
                if action == "REQUEST":
                    wanted_seats = [int(x)-1 for x in parts[1:]] 
                    wanted_seats.sort()  # ← DEADLOCK PREVENTION (always lock in order)

                    #first check that all requested seats are free
                    all_available = True
                    for s in wanted_seats:
                        if not (0 <= s < TOTAL_SEATS) or seats[s] != "Available":
                            all_available = False
                            break

                    if all_available and wanted_seats:
                        #only if all are free then only book all
                        for s in wanted_seats:
                            seats[s] = "Booked"
                            booked_by[s] = user_id
                        seats_str = ",".join(str(x+1) for x in wanted_seats)
                        response = f"SUCCESS|Booked seats {seats_str} for {user_id}!"
                        print(f"GROUP BOOKING → {user_id} booked seats {seats_str}")
                    else:
                        response = "FAILED|One or more seats not available or invalid!"

                elif action == "CANCEL" and len(parts) >= 2:
                    #cancel one or more seats (only if booked by this user)
                    cancelled = []
                    for x in parts[1:]:
                        s = int(x) - 1
                        if 0 <= s < TOTAL_SEATS and booked_by[s] == user_id:
                            seats[s] = "Available"
                            booked_by[s] = "-"
                            cancelled.append(str(s+1))
                    if cancelled:
                        response = f"CANCELLED|Released seats {','.join(cancelled)}"
                        print(f"GROUP CANCEL → {user_id} released seats {','.join(cancelled)}")
                    else:
                        response = "FAILED|No seats cancelled (not yours or invalid)"
                else:
                    response = "FAILED|Invalid command!"

                print_table()
                conn.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print(f"← {user_id} disconnected\n")
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 , TCP protocol
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)# allowing reuse of protocol
    server.bind(("0.0.0.0", 5555)) # accepts connections froom any IP addresses , server port numb : 5555
    server.listen(10)
            #maximum 10 pending connection requests in queue
    print("MOVIE TICKET BOOKING SERVER STARTED")
    print("Waiting for users...\n")
    print_table()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
# Movie Ticket Booking System
**By Harshini Inta - 2303114**

A real-time, thread-safe movie ticket booking system using Python sockets and threading — just like BookMyShow!

Demonstrates 10 OS concepts: Multithreading, Mutex, Critical Section, Race Condition Prevention, Deadlock Avoidance (resource ordering), Atomic Booking, IPC, Concurrency, Resource Sharing & Release.

### HOW TO RUN THE PROJECT

1. Open Command Prompt / Terminal
2. Go to your project folder  
   Example: `cd path/to/your/project_folder`
3. Start the Server (run only once)  
   ```bash
   python3 server.py

You will see: MOVIE TICKET BOOKING SERVER STARTED

Keep this window open

4. Open new terminal windows/tabs (these are different users)
   
6. In each new window/tab, run the Client
   ```bash
   python3 client.py

7.Enter any name when asked

8.Use these commands:

  REQUEST 5                 → book one seat
  
  REQUEST 2 3 4 5           → book 4 seats together
  
  CANCEL 3                  → cancel your seat
  
  CANCEL 1 5 8              → cancel multiple seats
  
  exit                      → close client
  
9.Watch the server window → live seat table updates automatically!

To stop: Press Ctrl + C in the server window

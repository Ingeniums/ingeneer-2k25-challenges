import socket
import threading

# import random # Still not needed for ordered questions
import sys
import time

# --- Configuration ---
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 12376  # The port to listen on (choose an unused port)
FLAG = "1ng3neer2k25{1f_you_h4v3n't_trY-SYMbolic-Ex3cution}"  # Replace with your actual flag

# Define your questions and answers IN THE DESIRED ORDER
# Use lowercase for answers in the dictionary for case-insensitive comparison
QUESTIONS = [
    {
        "question": "Give me the values of a",
    },
    {
        "question": "Give me the values of b",
    },
    {
        "question": "Give me the values of c",
    },
    {
        "question": "Give me the values of d",
    },
]


# --- Helper Function to Send Data ---
def send_message(conn, message):
    """Helper to send a message to the client, adding a newline and encoding."""
    try:
        conn.sendall((message + "\n").encode("utf-8"))
    except socket.error as e:
        print(f"Error sending data: {e}")
        return False  # Indicate send failed
    return True  # Indicate send succeeded


# --- Helper Function to Receive Data ---
def receive_message(conn, buffer_size=1024):
    """Helper to receive data from the client, decode and strip."""
    try:
        # Adding a timeout in case the client sends incomplete data or stops
        conn.settimeout(300)  # Set a reasonable timeout (e.g., 5 minutes per question)
        data = conn.recv(buffer_size)
        conn.settimeout(None)  # Reset timeout
        if not data:  # Client disconnected
            return None
        return data.decode(
            "utf-8"
        ).strip()  # Decode and remove leading/trailing whitespace/newline
    except socket.timeout:
        print("Receive timeout")
        return None  # Indicate timeout (treat as disconnection)
    except socket.error as e:
        print(f"Error receiving data: {e}")
        return None  # Indicate an error or disconnection


# --- Handle Each Client Connection ---
def handle_client(conn, addr):
    """Handles the quiz logic for a single connected client."""
    print(f"Connection from {addr}")

    d = [[], [], [], []]

    try:
        if not send_message(
            conn,
            'In the renovations of Hogwarts, Dumbledore has decided to add a math class to the curriculum\n He said it was something about "character development for the students" or something.',
        ):
            return
        time.sleep(0.5)
        if not send_message(
            conn,
            f"In old-fashioned style, one day during class, you stumble upon a formula in your textbook, and the book says it has interesting properties\n but it cuts off suddenly.",
        ):
            return
        if not send_message(
            conn, "Intrigued by this formula, you started studying it."
        ):
            return
        if not send_message(
            conn, "The formula is as follows: D(n) = D(n - 1) + gcd(n, D(n - 1))\n"
        ):
            return
        time.sleep(1)

        all_correct = True  # Flag to track if all questions were answered correctly

        # Iterate through questions in the defined order
        for i, q_data in enumerate(QUESTIONS):
            question_text = q_data["question"]
            answered_correctly_for_this_question = False

            # Loop for the current question until answered correctly or disconnection
            for j in range(4):
                while not answered_correctly_for_this_question:
                    if not send_message(conn, f"\n{question_text}{j+1}"):
                        all_correct = False  # Treat send failure as challenge failure
                        break  # Exit inner loop
                    if not send_message(conn, "Your answer: "):
                        all_correct = False  # Treat send failure as challenge failure
                        break  # Exit inner loop

                    user_answer = receive_message(conn)

                    def is_number(s: str) -> bool:
                        try:
                            float(s)
                            return True
                        except ValueError:
                            return False
                    if (
                        user_answer is None or not is_number(user_answer)
                    ):  # Client disconnected during receiving or timeout
                        print(
                            f"Client {addr} disconnected or timed out during question {i + 1}"
                        )
                        all_correct = False  # Mark challenge as failed
                        break  # Exit inner loop

                    print(f"Received answer from {addr} for Q{i+1}: '{user_answer}'")

                    # Compare answers (case-insensitive)
                    if (
                        user_answer
                    ):
                        d[j].append(float(user_answer))
                        break
                        answered_correctly_for_this_question = (
                            True  # Exit inner loop and move to next question
                        )
                    else:
                        # Do NOT reveal the correct answer
                        if not send_message(
                            conn, "Incorrect. Please try again for this question."
                        ):
                            all_correct = False  # Treat send failure as challenge failure
                            break  # Exit inner loop
                        # The inner while loop continues, asking the same question again

                if (
                    not all_correct
                ):  # If we broke out of the inner loop due to disconnection/error
                    break  # Exit the outer question loop as well

        # --- Challenge Outcome ---
        if (
            all_correct
        ):  # If the outer loop completed without setting all_correct to False
            if not send_message(
                conn, "\nChecking answer..."
            ):
                return
            time.sleep(1)
            cheater = False
            # check for cheating!
            for arr in d:
                for el in arr:
                    for tarr in d:
                        for tel in tarr:
                            if el is tel:
                                continue  # skip self-comparison
                            if abs(el - tel) < 1e-3:
                                if not send_message(conn, "Answers should be different!"):
                                    return
                                return


            for i in range(len(d)):
                sm = d[0][i] + d[1][i] + d[2][i] + d[3][i]
                pd = d[0][i] * d[1][i] * d[2][i] * d[3][i]
                if not ((9.81 - sm) < 1e-3 and (9.81 - pd) < 1e-3):
                    if not send_message(conn, "Incorrect!"):
                        return
                    return
            if not send_message(conn, "Here is your flag:"):
                return
            if not send_message(conn, FLAG):
                return

        else:
            # Message for failure (either incorrect answer or disconnection)
            # An incorrect answer results in retry, so this branch is mainly for
            # disconnection during the process or final flag message send failure.
            if not send_message(conn, "\nChallenge failed or connection lost."):
                return
            if not send_message(conn, "Better luck next time!"):
                return

    except Exception as e:
        print(f"An error occurred with client {addr}: {e}")
        # Attempt to send an error message to the client before closing
        send_message(conn, "\nAn internal error occurred. Please try again.")

    finally:
        # Close the connection regardless of success or failure
        print(f"Closing connection from {addr}")
        try:
            conn.close()
        except socket.error as e:
            print(f"Error closing socket for {addr}: {e}")


# --- Main Server Logic ---
def run_server():
    """Sets up and runs the main server loop."""
    server_socket = None  # Initialize to None

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((HOST, PORT))

        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        print("Waiting for connections...")

        while True:
            conn, addr = server_socket.accept()

            client_handler = threading.Thread(target=handle_client, args=(conn, addr))
            client_handler.start()

    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        if server_socket:
            print("Closing server socket.")
            try:
                server_socket.close()
            except socket.error as e:
                print(f"Error closing server socket: {e}")


# --- Run the server ---
if __name__ == "__main__":
    run_server()


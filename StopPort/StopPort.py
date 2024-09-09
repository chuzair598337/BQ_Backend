import psutil


def stop_port(port):
    found_process = False
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            if proc.info['connections']:
                for conn in proc.info['connections']:
                    if conn.laddr.port == port:
                        try:
                            proc.terminate()
                            proc.wait(timeout=3)  # Wait for the process to terminate
                            print(
                                f"Process {proc.info['name']} with PID {proc.info['pid']} on port {port} has been terminated.")
                        except psutil.NoSuchProcess:
                            print(f"Process {proc.info['pid']} does not exist anymore.")
                        except psutil.AccessDenied:
                            print(f"Access denied when trying to terminate PID {proc.info['pid']}.")
                        except psutil.TimeoutExpired:
                            proc.kill()  # Forcefully kill if terminate fails
                            print(
                                f"Process {proc.info['name']} with PID {proc.info['pid']} on port {port} has been forcefully killed.")
                        found_process = True
                        break
        except (psutil.AccessDenied, psutil.NoSuchProcess, RuntimeError) as e:
            # Catch and handle errors related to access, non-existent processes, or system call failures
            print(f"Could not retrieve information for PID {proc.pid}: {e}")
        if found_process:
            break

    if not found_process:
        print(f"No process found using port {port}.")


if __name__ == '__main__':
    stop_port(8080)

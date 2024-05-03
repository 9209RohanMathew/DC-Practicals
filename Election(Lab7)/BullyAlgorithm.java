import java.util.ArrayList;
import java.util.Scanner;

class Process {
    int processId;
    boolean coordinator;
    boolean active;
    int priority;

    public Process(int processId, boolean active, int priority) {
        this.processId = processId;
        this.coordinator = false;
        this.active = active;
        this.priority = priority;
    }

    public void startElection(ArrayList<Process> processes) {
        for (Process p : processes) {
            if (p.processId > this.processId && p.active) {
                System.out.println("Election message is sent from " + this.processId + " to " + p.processId);
                p.handleElection();
            }
        }
        System.out.println("Final coordinator is " + this.processId);
        this.coordinator = true;
        announceCoordinator(processes);
    }

    public void handleElection() {
        // Dummy method for handling election message
        System.out.println("Process " + this.processId + " receives ELECTION message and sends OK message back");
    }

    public void announceCoordinator(ArrayList<Process> processes) {
        for (Process p : processes) {
            if (p.processId != this.processId && p.active) {
                System.out.println("Process " + p.processId + " receives coordinator announcement from Process " + this.processId);
            }
        }
    }
}

public class BullyAlgorithm {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Get the number of processes from the user
        System.out.print("Enter the number of processes: ");
        int numProcesses = scanner.nextInt();
        ArrayList<Process> processes = new ArrayList<>();

        // Initialize processes
        for (int i = 1; i <= numProcesses; i++) {
            System.out.println("For process " + i + ":");
            System.out.print("Status (1 for active, 0 for inactive): ");
            int status = scanner.nextInt();
            System.out.print("Priority: ");
            int priority = scanner.nextInt();
            processes.add(new Process(i, status == 1, priority));
        }

        // Find the process to initiate the election
        int initiatingProcess;
        do {
            System.out.print("Which process will initiate the election? (Enter process id): ");
            initiatingProcess = scanner.nextInt();
        } while (initiatingProcess < 1 || initiatingProcess > numProcesses);

        // Start election
        processes.get(initiatingProcess - 1).startElection(processes);
        scanner.close();
    }
}

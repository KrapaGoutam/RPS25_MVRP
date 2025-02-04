from qiskit_ibm_runtime import QiskitRuntimeService

# Replace "<your-token>" with your actual IBM Quantum token
GK_token = "5b54ce7addff77e8d1a989bedf44c7263c89cebf4c9aadec493cc1ccbddf1122450d1c212ba3d032539cefacfc3cb95b8c54ff690433ceb6d18e50d0f8ba380f"

# Save the IBM Quantum account
QiskitRuntimeService.save_account(
    token=GK_token,
    channel="ibm_quantum",
    overwrite=True  # Optional: Overwrites an existing saved account
)
